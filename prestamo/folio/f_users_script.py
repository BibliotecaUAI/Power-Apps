# Power BI → Obtener datos → Script de Python
# Trae los usuarios de FOLIO (alumnos, profesores, funcionarios) con su grupo (tipo de usuario).
# Copiar las 4 líneas de conexión (OKAPI_URL, TENANT, USUARIO, CLAVE) desde el script de f_items que ya funciona.

import re
import requests
import pandas as pd

OKAPI_URL = "https://COPIAR-DEL-SCRIPT-f_items"
TENANT = "COPIAR"
USUARIO = "COPIAR"
CLAVE = "COPIAR"

s = requests.Session()
s.headers.update({"X-Okapi-Tenant": TENANT, "Content-Type": "application/json", "Accept": "application/json"})

# Login (sirve para versiones nuevas y antiguas de FOLIO)
r = s.post(OKAPI_URL + "/authn/login-with-expiry", json={"username": USUARIO, "password": CLAVE})
if r.status_code == 404:
    r = s.post(OKAPI_URL + "/authn/login", json={"username": USUARIO, "password": CLAVE})
r.raise_for_status()
token = r.headers.get("x-okapi-token") or s.cookies.get("folioAccessToken")
if token:
    s.headers["X-Okapi-Token"] = token


def traer(ruta, clave):
    filas, offset = [], 0
    while True:
        resp = s.get(OKAPI_URL + ruta, params={"limit": 1000, "offset": offset, "query": "cql.allRecords=1 sortby id"})
        resp.raise_for_status()
        lote = resp.json().get(clave, [])
        filas += lote
        if len(lote) < 1000:
            return filas
        offset += 1000


grupos = {g["id"]: g.get("group", "") for g in traer("/groups", "usergroups")}
try:
    deptos = {d["id"]: d.get("name", "") for d in traer("/departments", "departments")}
except Exception:
    deptos = {}


def cuerpo(v):
    # solo números (7 a 9 dígitos): puede ser el RUT sin dígito verificador
    t = re.sub(r"[^0-9]", "", str(v or ""))
    return t if 7 <= len(t) <= 9 and str(v or "").strip().isdigit() else ""


def programa(u):
    cf = u.get("customFields") or {}
    for k, v in cf.items():
        if any(x in k.lower() for x in ("progr", "carrera", "career")):
            return str(v)
    return ""


def rut_norm(v):
    # "12.345.678-k" -> "12345678K"; devuelve "" si no parece RUT
    t = re.sub(r"[^0-9kK]", "", str(v or "")).upper()
    return t if re.fullmatch(r"\d{7,8}[0-9K]", t) else ""


filas = []
for u in traer("/users", "users"):
    p = u.get("personal", {}) or {}
    rut = rut_norm(u.get("barcode")) or rut_norm(u.get("externalSystemId")) or rut_norm(u.get("username"))
    filas.append({
        "id": u.get("id", ""),
        "rut": rut,
        "rutCuerpo": rut[:-1] if rut else (cuerpo(u.get("barcode")) or cuerpo(u.get("externalSystemId")) or cuerpo(u.get("username"))),
        "barcode": u.get("barcode", ""),
        "externalSystemId": u.get("externalSystemId", ""),
        "username": u.get("username", ""),
        "nombre": p.get("firstName", ""),
        "apellido": p.get("lastName", ""),
        "nombreSugerido": p.get("preferredFirstName", "") or p.get("firstName", ""),
        "correo": p.get("email", ""),
        "tipoUsuario": grupos.get(u.get("patronGroup", ""), ""),
        "unidadAcademica": ", ".join(deptos.get(d, "") for d in (u.get("departments") or [])),
        "programa": programa(u),
        "activo": "SI" if u.get("active") else "NO",
        "vence": u.get("expirationDate", ""),
    })

f_users = pd.DataFrame(filas)

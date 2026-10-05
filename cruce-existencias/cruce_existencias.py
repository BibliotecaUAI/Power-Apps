"""Completa las existencias (columnas T a W) de las filas de la Ficha de Descarte que no las tienen.

Uso:  python cruce_existencias.py  Ficha.xlsx  Cruce_Existencias_PP_2026.csv  Salida.xlsx  [--por-numero]

Regla (igual que se hace a mano en FOLIO): el código de barra lleva al título (HRID);
se cuentan los códigos distintos que tiene ese título, separados por biblioteca.
3 códigos distintos del título en Viña = Viña 3.
Con --por-numero solo se cuentan los códigos del mismo volumen/número.
"""
import re
import sys

import pandas as pd

HOJA = "Ficha descarte - Base"
BIBLIOTECAS = [  # (texto en FOLIO, columna de la ficha)
    ("Edif. A", "Pregrado A - Existencia"),
    ("Edif. F", "Pregrado F - Existencia"),
    ("Postgrado", "Posgrado - Existencia"),
    ("Viña", "Viña - Existencia"),
]
COLS_EX = [c for _, c in BIBLIOTECAS]


def norm_codigo(v):
    s = str(v).strip()
    return s[:-2] if s.endswith(".0") else s


def norm_volumen(v):
    """'Vol.9: No.1 (2006/Ene-Jul) c.2' → 'VOL.9:NO.1(2006/ENE-JUL)'. Quita la marca de copia."""
    s = "" if pd.isna(v) else str(v).upper()
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"(C|COP|COPIA|EJ|EJEMPLAR)\.?\d+$", "", s)
    return s


def biblioteca(texto):
    for clave, col in BIBLIOTECAS:
        if clave.lower() in str(texto).lower():
            return col
    return None


def main(ficha, csv, salida, por_numero=False):
    df = pd.read_excel(ficha, sheet_name=HOJA)
    df["Fila Excel"] = df.index + 2
    df = df.dropna(how="all", subset=df.columns[:35])
    pend = df[df[COLS_EX].isna().all(axis=1)].copy()
    pend["cod"] = pend["Codigo de Barra"].map(norm_codigo)

    ej = pd.read_csv(csv, sep=";", dtype=str, encoding="utf-8-sig").fillna("")
    ej["cod"] = ej["codigo"].str.strip()
    ej["vol"] = ej["copia"].map(norm_volumen)
    ej["col"] = ej["biblioteca"].map(biblioteca)
    clave_cols = ["hrid", "vol"] if por_numero else ["hrid"]
    conteo = (ej.dropna(subset=["col"]).groupby(clave_cols + ["col"])["cod"].nunique()
              .unstack("col").reindex(columns=COLS_EX).fillna(0).astype(int))
    por_cod = ej.drop_duplicates("cod").set_index("cod")
    por_cod_sin_ceros = ej.assign(k=ej["cod"].str.lstrip("0")).drop_duplicates("k").set_index("k")

    filas = []
    for _, r in pend.iterrows():
        c = r["cod"]
        it = por_cod.loc[c] if c in por_cod.index else (
            por_cod_sin_ceros.loc[c.lstrip("0")] if c.lstrip("0") in por_cod_sin_ceros.index else None)
        f = {"Fila Excel": r["Fila Excel"], "Codigo de Barra": r["Codigo de Barra"]}
        if it is None:
            f.update({"Estado": "No encontrado en FOLIO", "HRID": r["HRID"], "Título": r["Título"],
                      "Copia / Volumen": r["Copia"]})
        else:
            clave = (it["hrid"], it["vol"]) if por_numero else it["hrid"]
            ex = conteo.loc[clave] if clave in conteo.index else pd.Series(0, index=COLS_EX)
            f.update({"Estado": "OK", "HRID": it["hrid"], "Título": it["titulo"], "Copia / Volumen": it["copia"],
                      "Año": it["anio"], "Tipo de Material": it["tipo"],
                      "Biblioteca-Ubicación": f'{it["biblioteca"]} {it["ubicacion"]}'.strip()})
            f.update({col: int(ex[col]) for col in COLS_EX})
        filas.append(f)

    orden = ["Fila Excel", "Codigo de Barra", "Estado", "HRID", "Título", "Copia / Volumen", "Año",
             "Tipo de Material", "Biblioteca-Ubicación"] + COLS_EX
    res = pd.DataFrame(filas).reindex(columns=orden)
    with pd.ExcelWriter(salida, engine="openpyxl") as w:
        res.to_excel(w, sheet_name="Faltaban existencias", index=False)
        ej.drop(columns=["cod", "vol", "col"]).to_excel(w, sheet_name="Ejemplares FOLIO", index=False)
        for ws in w.book.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = min(
                    55, max(10, *(len(str(c.value or "")) + 2 for c in col[:300])))
    print(f"{len(res)} filas · OK: {(res['Estado'] == 'OK').sum()} · no encontradas: {(res['Estado'] != 'OK').sum()}")


if __name__ == "__main__":
    main(*sys.argv[1:4], por_numero="--por-numero" in sys.argv)

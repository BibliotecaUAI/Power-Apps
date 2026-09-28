F="font-family:Carlito,Calibri,sans-serif"
def fondo(oscuro):
    if oscuro:
        return ("radial-gradient(420px 260px at 18% 30%,#4A4D52 0%,transparent 70%),radial-gradient(520px 300px at 78% 70%,#3F4247 0%,transparent 70%),"
                "radial-gradient(300px 200px at 55% 20%,#5A5D63 0%,transparent 70%),linear-gradient(160deg,#1E1F22,#16171A)")
    return ("radial-gradient(420px 260px at 18% 30%,#C9CCD1 0%,transparent 70%),radial-gradient(520px 300px at 78% 70%,#D2D5D9 0%,transparent 70%),"
            "radial-gradient(300px 200px at 55% 20%,#BFC3C8 0%,transparent 70%),linear-gradient(160deg,#F4F4F5,#E9EAEC)")
VAR = {
 'A · Esmerilado': dict(cl="background:rgba(255,255,255,.55);backdrop-filter:blur(22px) saturate(150%);border:1px solid rgba(255,255,255,.85);box-shadow:0 16px 36px rgba(17,17,17,.12),inset 0 1px 0 rgba(255,255,255,.95)",
                         os="background:rgba(70,72,78,.45);backdrop-filter:blur(22px) saturate(150%);border:1px solid rgba(191,195,200,.30);box-shadow:0 16px 36px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.14)",
                         d="Lechoso y suave. El más elegante y legible."),
 'B · Cristal líquido': dict(cl="background:linear-gradient(135deg,rgba(255,255,255,.38),rgba(255,255,255,.12));backdrop-filter:blur(8px) saturate(180%);border:1px solid rgba(255,255,255,.95);box-shadow:0 16px 36px rgba(17,17,17,.10),inset 1px 1px 0 rgba(255,255,255,.95),inset -1px -1px 0 rgba(138,141,145,.35),inset 0 0 22px rgba(255,255,255,.35)",
                         os="background:linear-gradient(135deg,rgba(255,255,255,.14),rgba(255,255,255,.03));backdrop-filter:blur(8px) saturate(180%);border:1px solid rgba(255,255,255,.35);box-shadow:0 16px 36px rgba(0,0,0,.35),inset 1px 1px 0 rgba(255,255,255,.35),inset -1px -1px 0 rgba(0,0,0,.4),inset 0 0 22px rgba(255,255,255,.06)",
                         d="Más transparente, bordes que brillan. Lo más parecido a Liquid Glass."),
 'C · Humo': dict(cl="background:rgba(17,17,17,.08);backdrop-filter:blur(16px);border:1px solid rgba(17,17,17,.10);box-shadow:0 16px 36px rgba(17,17,17,.10),inset 0 1px 0 rgba(255,255,255,.7)",
                  os="background:rgba(0,0,0,.35);backdrop-filter:blur(16px);border:1px solid rgba(191,195,200,.18);box-shadow:0 16px 36px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.08)",
                  d="Vidrio ahumado, sobrio. Contraste alto."),
}
def muestra(nombre, estilo, oscuro, desc):
    tx = "#F2F2F3" if oscuro else "#111111"; sub = "#C4C7CC" if oscuro else "#3F4247"; mut = "#9A9DA2" if oscuro else "#8A8D91"
    brillo = "<div style='position:absolute;inset:0;border-radius:18px;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.35) 46%,transparent 60%);opacity:.5'></div>"
    return (f"<div style='position:relative;width:390px;height:190px;border-radius:18px;{estilo};overflow:hidden'>{brillo}"
            f"<div style='position:relative;padding:18px 22px'><div style='{F};font-size:10px;letter-spacing:1.5px;font-weight:700;color:{mut}'>{nombre.upper()}</div>"
            f"<div style='{F};font-size:17px;font-weight:700;color:{tx};margin-top:6px'>Préstamo</div><div style='{F};font-size:12px;font-style:italic;color:{sub}'>RUT o QR de la cédula y los libros</div>"
            f"<div style='{F};font-size:12px;color:{sub};margin-top:16px'>{desc}</div>"
            f"<div style='position:absolute;left:22px;right:22px;top:150px;display:flex;justify-content:space-between'><span style='{F};font-size:12px;font-weight:700;color:{tx}'>23 préstamos hoy</span>"
            f"<span style='{F};font-size:10px;letter-spacing:1.5px;font-weight:700;color:{tx}'>ABRIR →</span></div></div></div>")
def panel(oscuro):
    tit = "Modo oscuro (grafito, con matices)" if oscuro else "Modo claro"
    cards = ''.join(f"<div>{muestra(k, v['os' if oscuro else 'cl'], oscuro, v['d'])}</div>" for k,v in VAR.items())
    return (f"<div class='scr' data-l='vidrio_{'oscuro' if oscuro else 'claro'}' style='width:1300px;padding:26px 30px;box-sizing:border-box;background:{fondo(oscuro)};position:relative;overflow:hidden'>"
            f"<div style='position:absolute;left:300px;top:40px;{F};font-size:180px;font-weight:700;color:{'rgba(255,255,255,.06)' if oscuro else 'rgba(17,17,17,.06)'};letter-spacing:20px'>UAI</div>"
            f"<div style='position:relative;{F};font-size:17px;font-weight:700;color:{'#F2F2F3' if oscuro else '#111'}'>{tit}</div>"
            f"<div style='position:relative;{F};font-size:12px;font-style:italic;color:{'#C4C7CC' if oscuro else '#3F4247'};margin-bottom:16px'>Detrás de cada tarjeta hay formas plateadas y la palabra UAI para ver cuánto deja pasar el vidrio</div>"
            f"<div style='position:relative;display:flex;gap:24px'>{cards}</div></div>")
open('vidrio.html','w').write(f"<html><head><meta charset='utf-8'><link href='fonts/carlito.css' rel='stylesheet'></head><body style='margin:0'>{panel(False)}{panel(True)}</body></html>")

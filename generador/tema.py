
# Post-proceso de diseño v2: tema claro (esmerilado) / oscuro (humo), letra Calibri, textos 10-12,
# esquinas redondeadas, marcadores con destello en cada tarjeta, fondo con formas plateadas.
import re
import sys
sys.path.insert(0, '.')
from nav import cinta

CLARO = ('{bg: RGBA(240, 240, 241, 1), tx: ColorValue("#111111"), sub: ColorValue("#3F4247"), mut: ColorValue("#8A8D91"), '
         'inp: ColorValue("#FFFFFF"), inpRO: ColorValue("#F7F7F8"), line: RGBA(17, 17, 17, 0.14), lineStrong: ColorValue("#111111"), '
         'hBg: "radial-gradient(700px 420px at 20% 35%,#D2D5D9 0%,transparent 70%),radial-gradient(800px 460px at 85% 80%,#D8DBDF 0%,transparent 70%),'
         'radial-gradient(500px 300px at 60% 10%,#C9CCD1 0%,transparent 70%),linear-gradient(160deg,#F4F4F5,#EBECEE)", '
         'hGlass: "background:rgba(255,255,255,0.55);backdrop-filter:blur(22px) saturate(150%);-webkit-backdrop-filter:blur(22px) saturate(150%);'
         'box-shadow:0 16px 36px rgba(17,17,17,0.12),inset 0 1px 0 rgba(255,255,255,0.95)", '
         'hBorde: "1px solid rgba(255,255,255,0.85)", hTx: "#111111", hSub: "#3F4247", hMut: "#8A8D91", hLin: "rgba(17,17,17,0.08)", '
         'hPos: "#111111", hPosTx: "#FFFFFF"}')
OSCURO = ('{bg: RGBA(30, 31, 34, 1), tx: ColorValue("#F2F2F3"), sub: ColorValue("#C4C7CC"), mut: ColorValue("#9A9DA2"), '
          'inp: ColorValue("#2E3034"), inpRO: ColorValue("#26282B"), line: RGBA(191, 195, 200, 0.28), lineStrong: ColorValue("#BFC3C8"), '
          'hBg: "radial-gradient(700px 420px at 20% 35%,#4A4D52 0%,transparent 70%),radial-gradient(800px 460px at 85% 80%,#3F4247 0%,transparent 70%),'
          'radial-gradient(500px 300px at 60% 10%,#55585E 0%,transparent 70%),linear-gradient(160deg,#232428,#1A1B1E)", '
          'hGlass: "background:rgba(0,0,0,0.35);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);'
          'box-shadow:0 16px 36px rgba(0,0,0,0.45),inset 0 1px 0 rgba(255,255,255,0.08)", '
          'hBorde: "1px solid rgba(191,195,200,0.22)", hTx: "#F2F2F3", hSub: "#C4C7CC", hMut: "#9A9DA2", hLin: "rgba(191,195,200,0.16)", '
          'hPos: "#E6E7E9", hPosTx: "#111111"}')
SET_TEMA = 'Set(varT, If(varOscuro, ' + OSCURO + ', ' + CLARO + '))'

GLASS = 'border-radius:16px;overflow:hidden;position:relative;" & varT.hGlass & ";border:" & varT.hBorde & "'
LINEA = "<div style='height:3px;background:linear-gradient(90deg,#8A8D91,#FFFFFF,#BFC3C8,#FFFFFF,#8A8D91)'></div>"

HTML_REEMPLAZOS = [
    ("color:#FFFFFF;background:#1B2A4A", 'color:" & varT.hPosTx & ";background:" & varT.hPos & "'),
    ("background:#1B2A4A", 'background:" & varT.hPos & "'),
    ("background:#FFFFFF;border:1px solid #DADCDF;box-shadow:0 12px 28px rgba(17,17,17,0.10),0 2px 6px rgba(138,141,145,0.25)", GLASS),
    ("background:#FFFFFF;border:1px solid #DADCDF;box-shadow:0 12px 28px rgba(17,17,17,0.10)", GLASS),
    ("background:#FFFFFF;border:", 'border-radius:16px;" & varT.hGlass & ";border:'),
    (";box-shadow:0 12px 28px rgba(17,17,17,0.10),0 2px 6px rgba(138,141,145,0.25)", ""),
    ('"1px solid #DADCDF"', "varT.hBorde"),
    (LINEA, LINEA + cinta()),
    ("<div style='padding:14px 22px'>", "<div style='padding:14px 58px 14px 22px'>"),
    ("padding:14px 20px 8px;", "padding:14px 58px 8px 20px;"),
    ("solid #DADCDF", 'solid " & varT.hLin & "'),
    ("color:#3F4247", 'color:" & varT.hSub & "'),
    ("color:#1B2A4A", 'color:" & varT.hTx & "'),
    ("#8FA3C7", "#BFC3C8"),
    ("font-family:Segoe UI,Arial,sans-serif", "font-family:Calibri,Carlito,Segoe UI,sans-serif"),
    ("height:112px;box-sizing:border-box;padding:0 40px 0 104px;",
     "height:72px;margin:14px 18px 0 84px;border-radius:18px;overflow:hidden;box-shadow:0 14px 30px rgba(17,17,17,0.25);border:1px solid #3F4247;box-sizing:border-box;padding:0 26px;"),
    (";border-bottom:2px solid #BFC3C8'", "'"),
    ("font-size:26px", "font-size:20px"),
    ("font-size:24px", "font-size:20px"),
    ("font-size:22px", "font-size:18px"),
    ("font-size:28px", "font-size:22px"),
    ("font-size:18px;font-weight:700;color:#8A8D91", "font-size:14px;font-weight:700;color:#8A8D91"),
    ("font-size:15px", "font-size:14px"),
]

PROP_MAP = {
    'Color': {'#111111': 'varT.tx', '#1B2A4A': 'varT.tx', '#3F4247': 'varT.sub'},
    'Fill': {'#FFFFFF': 'varT.inp', '#F7F7F8': 'varT.inpRO', '#DADCDF': 'varT.line', '#1B2A4A': 'ColorValue("#3F4247")'},
    'BorderColor': {'#BFC3C8': 'varT.line', '#DADCDF': 'varT.line', '#1B2A4A': 'varT.lineStrong', '#111111': 'varT.lineStrong'},
    'FocusedBorderColor': {'#111111': 'varT.lineStrong'},
    'HoverFill': {'#F7F7F8': 'varT.inpRO'},
    'ChevronBackground': {'#FFFFFF': 'varT.inp'},
    'ChevronFill': {'#3F4247': 'varT.sub'},
}
TALLAS = {7: 9, 8: 9, 9: 10, 10: 10, 11: 12, 12: 12, 13: 12, 14: 11, 15: 12, 16: 11, 18: 12}


def html_fix(txt):
    for a, z in HTML_REEMPLAZOS:
        txt = txt.replace(a, z)
    # color #111111 → tema, salvo sobre fondos plateados (etiquetas plata)
    txt = re.sub(r"color:#111111(?!;background:linear-gradient)(?!;border)", 'color:" & varT.hTx & "', txt)
    # botones grandes con fondo metálico: esquinas redondeadas
    txt = re.sub(r"<div style='height:(\d+)px;background:linear-gradient\(115deg,", r"<div style='height:\1px;border-radius:14px;background:linear-gradient(115deg,", txt)
    return txt


def fondo(sfx):
    return f'''      - htmlFondo_{sfx}:
          Control: HtmlViewer@2.1.0
          Properties:
            Fill: =RGBA(0, 0, 0, 0)
            Height: =768
            HtmlText: ="<div style='width:1366px;height:768px;background:" & varT.hBg & "'></div>"
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =1366
            X: =0
            Y: =0'''


def aplicar(path, sfx):
    lines = open(path).read().split('\n')
    out = []
    en_html = False
    tipo = ''
    nombre = ''
    for l in lines:
        m = re.match(r'^      - ([^:]+):$', l)
        if m:
            nombre = m.group(1)
        m = re.match(r'^          Control: (\S+)', l)
        if m:
            tipo = m.group(1).split('@')[0]
        prop = re.match(r'^            ([A-Za-z]+): (.*)$', l)
        if prop:
            en_html = prop.group(1) == 'HtmlText'
        if en_html:
            l = html_fix(l)
        elif prop:
            p, v = prop.group(1), prop.group(2)
            if p in PROP_MAP:
                for hexa, var in PROP_MAP[p].items():
                    v = v.replace(f'ColorValue("{hexa}")', var)
                if p == 'Fill' and tipo == 'Rectangle':
                    v = v.replace('ColorValue("#111111")', 'varT.lineStrong')
                l = f'            {p}: {v}'
            if p == 'Font' and 'Courier' not in v:
                l = '            Font: ="Calibri"'
            if p == 'Size' and re.fullmatch(r'=\d+', v):
                l = f'            Size: ={TALLAS.get(int(v[1:]), int(v[1:]))}'
            if p.startswith('Radius') and v == '=0':
                l = f'            {p}: =12'
            if nombre == 'lblCardHRID' and p == 'X':
                l = '            X: =1060'
        elif not l.startswith('            ') and not l.startswith('              '):
            en_html = False
        # propiedades de la pantalla
        if l == '      Fill: =ColorValue("#FFFFFF")':
            l = '      Fill: =varT.bg'
        if l.startswith('      OnVisible: ='):
            l = '      OnVisible: =' + SET_TEMA + '; ' + l[len('      OnVisible: ='):]
        out.append(l)
        if l == '    Children:':
            out.extend(fondo(sfx).split('\n'))
    t = '\n'.join(out)
    t = t.replace('TEMA_OSCURO', OSCURO).replace('TEMA_CLARO', CLARO)
    # valores de una línea con ': ' o ' #' → bloque literal (YAML)
    final = []
    for l in t.split('\n'):
        m = re.match(r'^( +)([A-Za-z]+): (=.*)$', l)
        if m and (': ' in m.group(3) or ' #' in m.group(3)):
            final.append(f'{m.group(1)}{m.group(2)}: |-')
            final.append(' ' * (len(m.group(1)) + 2) + m.group(3))
        else:
            final.append(l)
    # todo HtmlViewer con fondo transparente (para que se vea el vidrio)
    txt = '\n'.join(final)
    bloques = re.split(r'(?m)^(?=      - )', txt)
    for k, b in enumerate(bloques):
        if 'Control: HtmlViewer' in b and '\n            Fill:' not in b:
            bloques[k] = b.replace('          Properties:\n', '          Properties:\n            Fill: =RGBA(0, 0, 0, 0)\n', 1)
    open(path, 'w').write(''.join(bloques))

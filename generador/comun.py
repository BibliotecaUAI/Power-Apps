
# Piezas comunes para las pantallas de Préstamo y Devolución
import sys
sys.path.insert(0, '.')
from tabs import label  # noqa: F401
from nav import header, rail, pantalla  # noqa: F401

ON = "<div style='height:%dpx;background:linear-gradient(115deg,#0B0B0C 0%%,#111111 38%%,#35373B 50%%,#111111 62%%,#0B0B0C 100%%);border-top:1px solid #8A8D91;box-shadow:0 6px 14px rgba(17,17,17,0.25)'></div>"
OFF = "<div style='height:%dpx;background:linear-gradient(115deg,#BFC3C8 0%%,#DADCDF 50%%,#BFC3C8 100%%)'></div>"
CARD = ("<div style='margin:6px;height:%dpx;box-sizing:border-box;background:#FFFFFF;border:%s;"
        "box-shadow:0 12px 28px rgba(17,17,17,0.10),0 2px 6px rgba(138,141,145,0.25);font-family:Segoe UI,Arial,sans-serif;position:relative;overflow:hidden'>"
        "<div style='height:3px;background:linear-gradient(90deg,#8A8D91,#FFFFFF,#BFC3C8,#FFFFFF,#8A8D91)'></div><div style='padding:14px 22px'>")
NORM = 'Upper(Substitute(Substitute(Substitute({x}, ".", ""), "-", ""), " ", ""))'
ESC = 'Substitute(Substitute({x}, "&", "&amp;"), "<", "&lt;")'
BIBLIOTECAS = '["Biblioteca Viña", "Biblioteca Posgrado", "Biblioteca Pregrado A", "Biblioteca Pregrado F"]'


def ind(s, n=14):
    return '\n'.join(' ' * n + l for l in s.strip('\n').split('\n'))


def html(n, x, y, w, h, formula, visible=None):
    v = f'            Visible: ={visible}\n' if visible else ''
    return f'''      - {n}:
          Control: HtmlViewer@2.1.0
          Properties:
            Fill: =RGBA(0, 0, 0, 0)
            Height: ={h}
            HtmlText: |-
{ind('=' + formula)}
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
{v}            Width: ={w}
            X: ={x}
            Y: ={y}'''


def boton(n, x, y, w, h, text, onselect, displaymode='DisplayMode.Edit', dark=True, size=13):
    if dark:
        borde = '            BorderThickness: =0'
        colors = '''            Color: =ColorValue("#FFFFFF")
            DisabledColor: =ColorValue("#FFFFFF")
            DisabledFill: =RGBA(0, 0, 0, 0)'''
        fill = '''            Fill: =RGBA(0, 0, 0, 0)'''
        hover = '''            HoverColor: =ColorValue("#FFFFFF")
            HoverFill: =RGBA(191, 195, 200, 0.18)'''
        pressed = '            PressedFill: =RGBA(27, 42, 74, 0.55)'
    else:
        borde = '''            BorderColor: =ColorValue("#BFC3C8")
            BorderThickness: =1'''
        colors = '            Color: =ColorValue("#111111")'
        fill = '            Fill: =ColorValue("#FFFFFF")'
        hover = '''            HoverColor: =ColorValue("#FFFFFF")
            HoverFill: =ColorValue("#111111")'''
        pressed = '            PressedFill: =ColorValue("#3F4247")'
    return f'''      - {n}:
          Control: Classic/Button@2.2.0
          Properties:
{borde}
{colors}
            DisplayMode: ={displaymode}
{fill}
            Font: =Font.'Segoe UI'
            FontWeight: ={'FontWeight.Bold' if dark else 'FontWeight.Normal'}
            Height: ={h}
{hover}
            OnSelect: |-
{ind('=' + onselect)}
{pressed}
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: ={size}
            Text: ={text}
            Width: ={w}
            X: ={x}
            Y: ={y}'''


def fondo(n, boton_n, x, y, w, h):
    return html(n, x, y, w, h, f'If({boton_n}.DisplayMode = DisplayMode.Disabled, "{OFF % h}", "{ON % h}")')


def oculto(n, onselect):
    return f'''      - {n}:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =0
            Color: =RGBA(0, 0, 0, 0)
            Fill: =RGBA(0, 0, 0, 0)
            Height: =1
            HoverFill: =RGBA(0, 0, 0, 0)
            OnSelect: |-
{ind('=' + onselect)}
            PressedFill: =RGBA(0, 0, 0, 0)
            TabIndex: =-1
            Text: =""
            Width: =1
            X: =0
            Y: =0'''


def entrada(n, x, y, w, hint, onchange, h=52, multilinea=False):
    extra = '''            Font: =Font.'Courier New'
            Mode: =TextMode.MultiLine
            PaddingTop: =10
''' if multilinea else '''            Font: =Font.'Segoe UI'
'''
    return f'''      - {n}:
          Control: Classic/TextInput@2.3.2
          Properties:
            BorderColor: =ColorValue("#111111")
            BorderThickness: =2
            Color: =ColorValue("#1B2A4A")
            Default: =""
            Fill: =ColorValue("#FFFFFF")
            FocusedBorderColor: =ColorValue("#111111")
            FocusedBorderThickness: =2
{extra}            Height: ={h}
            HintText: ="{hint}"
            OnChange: |-
{ind('=' + onchange)}
            PaddingLeft: =14
            PaddingRight: =56
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: ={11 if multilinea else 16}
            Width: ={w}
            X: ={x}
            Y: ={y}'''


def lista(n, x, y, w, items, default):
    items_yaml = ('|-\n              =' + items) if ': ' in items else '=' + items
    return f'''      - {n}:
          Control: Classic/DropDown@2.3.1
          Properties:
            BorderColor: =ColorValue("#BFC3C8")
            BorderThickness: =1
            ChevronBackground: =ColorValue("#FFFFFF")
            ChevronFill: =ColorValue("#3F4247")
            Color: =ColorValue("#111111")
            Default: ={default}
            Fill: =ColorValue("#FFFFFF")
            Font: =Font.'Segoe UI'
            Height: =30
            HoverFill: =ColorValue("#F7F7F8")
            Items: {items_yaml}
            PaddingLeft: =8
            SelectionColor: =ColorValue("#FFFFFF")
            SelectionFill: =ColorValue("#111111")
            Size: =9
            Width: ={w}
            X: ={x}
            Y: ={y}'''


def texto(n, x, y, w):
    return f'''      - {n}:
          Control: Classic/TextInput@2.3.2
          Properties:
            BorderColor: =ColorValue("#BFC3C8")
            BorderThickness: =1
            Color: =ColorValue("#111111")
            Default: =""
            Fill: =ColorValue("#FFFFFF")
            Font: =Font.'Segoe UI'
            Height: =30
            PaddingLeft: =8
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: =9
            Width: ={w}
            X: ={x}
            Y: ={y}'''


def badge(t, plata=False):
    if plata:
        return ("<span style='display:inline-block;padding:2px 7px;font-size:9px;font-weight:700;letter-spacing:.5px;color:#111111;"
                f"background:linear-gradient(115deg,#8A8D91,#FFFFFF 50%,#BFC3C8);border:1px solid #8A8D91'>{t}</span>")
    return f"<span style='display:inline-block;padding:2px 7px;font-size:9px;font-weight:700;letter-spacing:.5px;color:#FFFFFF;background:#1B2A4A'>{t}</span>"


def borde_destellante(w, h):
    """SVG animado (borde rojo que parpadea) para poner encima de una tarjeta."""
    return ("<img style='position:absolute;left:0;top:0' src='data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 "
            f"width=%22{w}%22 height=%22{h}%22><rect x=%227%22 y=%227%22 rx=%2218%22 width=%22{w - 14}%22 height=%22{h - 14}%22 fill=%22none%22 "
            "stroke=%22%23B3261E%22 stroke-width=%224%22><animate attributeName=%22stroke-opacity%22 values=%221;0.1;1%22 dur=%221s%22 "
            "repeatCount=%22indefinite%22/></rect></svg>'/>")


def validar(path, screen):
    import yaml
    import re
    raw = open(path).read()
    for i, l in enumerate(raw.split('\n')):
        m = re.match(r'\s+[A-Za-z.]+: (=.*)$', l)
        if m and (' #' in m.group(1) or ': ' in m.group(1)):
            print('RIESGO', i + 1, l[:100])
    d = yaml.safe_load(raw)
    ch = d['Screens'][screen]['Children']
    for c in ch:
        (n, p), = c.items()
        for k, v in p['Properties'].items():
            v = str(v)
            assert v.startswith('='), (n, k)
            t = re.sub(r'"(?:[^"]|"")*"', '""', v)
            if t.count('"') % 2:
                print('COMILLAS', n, k)
            for a, z in ['()', '{}']:
                if t.count(a) != t.count(z):
                    print('DESBALANCE', n, k, a, t.count(a), t.count(z))
    print(path.split('/')[-1], len(ch), 'controles')

# Menú lateral, encabezado e Inicio para todas las pantallas
from tabs import label

SILVER = "background:linear-gradient(115deg,#0B0B0C 0%,#111111 38%,#35373B 50%,#111111 62%,#0B0B0C 100%)"
SILVER_V = SILVER.replace('115deg', '180deg')
ITEMS = [('⌂', 'Inicio', 'scrInicio'), ('▤', 'Descarte', 'scrDescarteB'), ('↗', 'Préstamo', 'scrPrestamo'),
         ('↙', 'Devolución', 'scrDevolucion'), ('▦', 'Morosos', 'scrPanel'), ('▣', 'Inventario', 'scrInventario')]
SCREENS = [s for _, _, s in ITEMS]

def q(s):  # texto HTML dentro de un literal Power Fx
    return s.replace('"', '""')

def rail_html(active, abierto):
    w = 216 if abierto else 58
    items = ''
    for ic, t, _ in ITEMS:
        on = t == active
        caja = ("background:linear-gradient(135deg,#35373B,#111111);box-shadow:inset 0 1px 0 rgba(255,255,255,0.18),0 4px 10px rgba(0,0,0,0.35);color:#FFFFFF;"
                if on else "color:#8A8D91;")
        nombre = (f"<span style='margin-left:14px;font-size:12px;font-weight:{700 if on else 400};letter-spacing:1px'>{t}</span>" if abierto else '')
        items += (f"<div style='height:56px;display:flex;align-items:center;padding-left:7px'><div style='height:44px;{'width:200px;' if abierto else 'width:44px;'}border-radius:12px;display:flex;align-items:center;"
                  f"{'padding-left:12px;box-sizing:border-box;' if abierto else 'justify-content:center;'}{caja}'><span style='font-size:18px;width:20px;text-align:center'>{ic}</span>{nombre}</div></div>")
    menu = "<span style='margin-left:14px;font-size:10px;letter-spacing:2px'>MENÚ</span>" if abierto else ''
    return (f"<div style='margin:14px 0 0 14px;width:{w}px;height:740px;border-radius:18px;{SILVER_V};border:1px solid #3F4247;box-shadow:0 14px 30px rgba(17,17,17,0.28);"
            f"font-family:Calibri,Carlito,Segoe UI,sans-serif;position:relative;overflow:hidden;box-sizing:border-box'>"
            f"<div style='height:84px;display:flex;align-items:center;justify-content:{'flex-start' if abierto else 'center'};{'padding-left:20px;' if abierto else ''}color:#FFFFFF;font-weight:700;font-size:14px;letter-spacing:2px;box-sizing:border-box'>{'UAI · BIBLIOTECAS' if abierto else 'UAI'}</div>"
            f"<div style='height:56px;display:flex;align-items:center;padding-left:{20 if abierto else 19}px;color:#BFC3C8;font-size:18px;border-top:1px solid rgba(191,195,200,0.22)'>☰{menu}</div>"
            f"{items}"
            f"<div style='position:absolute;left:0;right:0;bottom:16px;display:flex;align-items:center;justify-content:{'flex-start' if abierto else 'center'};{'padding-left:20px;' if abierto else ''}color:#BFC3C8;font-size:18px'>◐"
            f"{'<span style=margin-left:14px;font-size:11px;letter-spacing:1px>Modo claro / oscuro</span>' if abierto else ''}</div></div>")

def boton_invisible(n, x, y, w, h, onselect, visible=None, fill='RGBA(0, 0, 0, 0)', hover='RGBA(191, 195, 200, 0.12)'):
    s = f'''      - {n}:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =0
            Color: =RGBA(0, 0, 0, 0)
            Fill: ={fill}
            Height: ={h}
            HoverFill: ={hover}
            OnSelect: ={onselect}
            PressedFill: =RGBA(191, 195, 200, 0.25)
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            TabIndex: =-1
            Text: =""
'''
    if visible: s += f'            Visible: ={visible}\n'
    s += f'''            Width: ={w}
            X: ={x}
            Y: ={y}'''
    return s

ORDEN = [s for _, _, s in ITEMS]


def transicion(desde, hacia):
    """Inicio: Fade · Morosos: UnCover · avanzar en el menú: Cover · retroceder: CoverRight."""
    if hacia == 'scrInicio':
        return 'Fade'
    if hacia == 'scrPanel':
        return 'UnCover'
    i = next((k for k, (_, t, _s) in enumerate(ITEMS) if t == desde), 0)
    return 'Cover' if ORDEN.index(hacia) >= i else 'CoverRight'


def rail(sfx, active):
    """Controles del menú; van AL FINAL de la lista para quedar encima de todo."""
    out = [
        brillo(sfx),
        boton_invisible(f'btnCerrarMenu_{sfx}', 0, 0, 1366, 768, 'Set(varMenu, false)', visible='varMenu',
                        fill='RGBA(17, 17, 17, 0.35)', hover='RGBA(17, 17, 17, 0.35)'),
        f'''      - htmlMenu_{sfx}:
          Control: HtmlViewer@2.1.0
          Properties:
            Fill: =RGBA(0, 0, 0, 0)
            Height: =768
            HtmlText: |-
              =If(varMenu, "{q(rail_html(active, True))}", "{q(rail_html(active, False))}")
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =If(varMenu, 244, 86)
            X: =0
            Y: =0''',
        boton_invisible(f'btnMenu_{sfx}', 14, 98, 'If(varMenu, 216, 58)', 56, 'Set(varMenu, !varMenu)'),
        boton_invisible(f'btnTema_{sfx}', 14, 700, 'If(varMenu, 216, 58)', 48, 'Set(varOscuro, !varOscuro); Set(varT, If(varOscuro, TEMA_OSCURO, TEMA_CLARO))'),
    ]
    for i, (_, t, scr) in enumerate(ITEMS):
        n = f"btnIr{t.replace('é','e').replace('ó','o')}_{sfx}"
        out.append(boton_invisible(n, 14, 154 + 56 * i, 'If(varMenu, 216, 58)', 56,
                                   f'Set(varMenu, false); Navigate({scr}, ScreenTransition.{transicion(active, scr)})'))
    return '\n'.join(out)

KPI_PRESTAMO = [
    ('CountRows(Filter(colPrestamos, !IsBlank(IdPrestamo) && FechaPrestamo = Text(Today(), "yyyy-mm-dd")))', 'PRÉSTAMOS HOY', "#FFFFFF"),
    ('CountRows(Filter(colPrestamos, !IsBlank(IdPrestamo) && FechaDevolucion = Text(Today(), "yyyy-mm-dd")))', 'DEVOLUCIONES HOY', "#FFFFFF"),
    ('CountRows(Distinct(Filter(colPrestamos, Estado = "Activo" && !IsBlank(FechaVencimiento) && DateValue(FechaVencimiento) < Today()), RUT))', 'MOROSOS', "#BFC3C8"),
]

def header(sfx, titulo, kpis=KPI_PRESTAMO):
    partes = []
    for i, (expr, lab, col) in enumerate(kpis):
        borde = "border-right:1px solid #3F4247;" if i < len(kpis) - 1 else ""
        partes.append(f'"<div style=\'padding:0 26px;{borde}\'><div style=\'font-size:24px;font-weight:700;color:{col}\'>" & {expr} & "</div><div style=\'font-size:9px;letter-spacing:1.5px;color:#8A8D91;font-weight:600\'>{lab}</div></div>"')
    return f'''      - htmlHeader_{sfx}:
          Control: HtmlViewer@2.1.0
          Properties:
            Fill: =RGBA(0, 0, 0, 0)
            Height: =114
            HtmlText: |-
              ="<div style='height:112px;box-sizing:border-box;padding:0 40px 0 104px;{SILVER};font-family:Segoe UI,Arial,sans-serif;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #BFC3C8'>" &
              "<div><div style='font-size:10px;letter-spacing:3px;color:#BFC3C8;font-weight:600'>UNIVERSIDAD ADOLFO IBÁÑEZ · BIBLIOTECAS UAI</div>" &
              "<div style='font-size:28px;font-weight:700;color:#FFFFFF;margin-top:4px'>{titulo}</div></div><div style='display:flex;align-items:center'>" &
              {(" & ").join(partes)} &
              "</div></div>"
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =1366'''

CARGA = 'ClearCollect(colPrestamos, tblPrestamos); Set(varMenu, false)'

def pantalla(nombre, onvisible, controles):
    return f'''Screens:
  {nombre}:
    Properties:
      Fill: =ColorValue("#FFFFFF")
      OnVisible: ={onvisible}
    Children:
''' + '\n'.join(controles) + '\n'

F_HTML = "font-family:Calibri,Carlito,Segoe UI,sans-serif"


def tarjeta(sfx, i, x, y, w, h, icono, titulo, desc, kpi_expr, destino):
    n = titulo.replace('é', 'e').replace('ó', 'o')
    corte = 26
    html = ('"<div style=\'position:relative;margin:6px;width:' + str(w) + 'px;height:' + str(h) + 'px;box-sizing:border-box;border-radius:16px;overflow:hidden;' + F_HTML + ';" & varT.hGlass & ";border:" & varT.hBorde & ";'
            + 'clip-path:polygon(0 0,calc(100% - ' + str(corte) + 'px) 0,100% ' + str(corte) + 'px,100% 100%,0 100%)\'>'
            + '<div style=\'position:absolute;right:0;top:0;width:' + str(corte) + 'px;height:' + str(corte) + 'px;background:linear-gradient(225deg,transparent 50%,#BFC3C8 50%,#FFFFFF 75%,#DADCDF)\'></div>'
            + cinta(40, 64, 'left:22px;top:0')
            + '<div style=\'position:absolute;left:22px;top:14px;width:40px;text-align:center;color:#FFFFFF;font-size:16px;z-index:3\'>' + icono + '</div>'
            + '<div style=\'position:absolute;right:40px;top:16px;font-size:10px;letter-spacing:1.5px;font-weight:700;color:" & varT.hMut & "\'>0' + str(i + 1) + '</div>'
            + '<div style=\'position:absolute;left:78px;top:18px;right:40px\'><div style=\'font-size:17px;font-weight:700;color:" & varT.hTx & "\'>' + titulo + '</div>'
            + '<div style=\'font-size:12px;font-style:italic;color:" & varT.hSub & ";margin-top:3px\'>' + desc + '</div></div>'
            + '<div style=\'position:absolute;left:22px;right:22px;bottom:14px;display:flex;justify-content:space-between;align-items:center\'>'
            + '<span style=\'font-size:12px;font-weight:700;color:" & varT.hTx & "\'>" & ' + kpi_expr + ' & "</span>'
            + '<span style=\'font-size:10px;letter-spacing:1.5px;font-weight:700;color:" & varT.hTx & "\'>ABRIR →</span></div></div>"')
    return '\n'.join([f'''      - htmlTarjeta{n}_{sfx}:
          Control: HtmlViewer@2.1.0
          Properties:
            Fill: =RGBA(0, 0, 0, 0)
            Height: ={h + 12}
            HtmlText: |-
              ={html}
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: ={w + 12}
            X: ={x - 6}
            Y: ={y - 6}''',
        boton_invisible(f'btnTarjeta{n}_{sfx}', x, y, w, h, f'Navigate({destino}, ScreenTransition.{transicion("Inicio", destino)})',
                        hover='RGBA(191, 195, 200, 0.10)')])


def inicio():
    hoy = 'Text(Today(), "yyyy-mm-dd")'
    tarjetas = [
        ('▤', 'Descarte', 'Escanear y registrar material, libro a libro o en tanda',
         'CountRows(colFicha) & " en la ficha · " & Coalesce(varContador, 0) & " en esta sesión"', 'scrDescarteB'),
        ('↗', 'Préstamo', 'RUT o QR de la cédula y los libros; plazo automático',
         f'CountRows(Filter(colPrestamos, !IsBlank(IdPrestamo) && FechaPrestamo = {hoy})) & " préstamos hoy"', 'scrPrestamo'),
        ('↙', 'Devolución', 'Libro a libro o el buzón completo; detecta morosos',
         f'CountRows(Filter(colPrestamos, !IsBlank(IdPrestamo) && FechaDevolucion = {hoy})) & " devoluciones hoy"', 'scrDevolucion'),
        ('◎', 'Morosos', 'Usuarios morosos reales de FOLIO, por nivel y biblioteca',
         'If(IsEmpty(colMorosos), "Ver lista actualizada", Text(varMorTotal, "#,##0") & " morosos en FOLIO")', 'scrPanel'),
        ('▣', 'Inventario', 'Toma de inventario de la colección', '"Próximamente"', 'scrInventario'),
    ]
    pos = [(96, 170, 404, 150), (514, 170, 404, 150), (932, 170, 416, 150), (96, 334, 620, 150), (728, 334, 620, 150)]
    ctrls = [header('0', 'Inicio'),
             label('lblSaludo_0', '="Hola, " & First(Split(User().FullName, " ")).Value & ". ¿Qué quieres hacer hoy?"', 96, 112, 700, h=22, size=12, color='#111111'),
             label('lblFecha_0', '=Text(Today(), "dddd d ""de"" mmmm ""de"" yyyy", "es-CL") & " · elige un módulo o usa el menú"', 96, 134, 700, h=18, size=10, color='#3F4247', bold=False)]
    for i, (p, t) in enumerate(zip(pos, tarjetas)):
        ctrls.append(tarjeta('0', i, *p, *t))
    fila = ('"<tr><td style=\'padding:8px;border-bottom:1px solid " & varT.hLin & "\'>" & Text(DateValue(FechaPrestamo), "dd-mm") & "</td>'
            '<td style=\'padding:8px;border-bottom:1px solid " & varT.hLin & "\'>" & Nombre & " " & Apellido & "</td>'
            '<td style=\'padding:8px;border-bottom:1px solid " & varT.hLin & "\'>" & Titulo & "</td>'
            '<td style=\'padding:8px;border-bottom:1px solid " & varT.hLin & "\'>" & If(Estado = "Activo" && !IsBlank(FechaVencimiento) && DateValue(FechaVencimiento) < Today(), '
            '"<span style=\'padding:2px 9px;border-radius:999px;font-size:10px;font-weight:700;background:#B3261E;color:#FFFFFF\'>MOROSO</span>", '
            '"<span style=\'padding:2px 9px;border-radius:999px;font-size:10px;font-weight:700;background:" & varT.hPos & ";color:" & varT.hPosTx & "\'>" & Upper(Estado) & "</span>") & "</td></tr>"')
    act = ('"<div style=\'position:relative;margin:6px;height:238px;box-sizing:border-box;border-radius:16px;overflow:hidden;' + F_HTML + ';" & varT.hGlass & ";border:" & varT.hBorde & "\'>'
           + cinta() + '<div style=\'padding:14px 22px\'><div style=\'font-size:15px;font-weight:700;color:" & varT.hTx & "\'>Actividad reciente</div>'
           '<div style=\'font-size:12px;font-style:italic;color:" & varT.hSub & "\'>Últimos préstamos registrados en la app</div>'
           '<table style=\'width:100%;border-collapse:collapse;font-size:12px;color:" & varT.hTx & ";margin-top:6px\'><tr style=\'text-align:left;font-size:10px;letter-spacing:1.2px;color:" & varT.hMut & "\'>'
           '<th style=\'padding:6px 8px\'>FECHA</th><th style=\'padding:6px 8px\'>USUARIO</th><th style=\'padding:6px 8px\'>TÍTULO</th><th style=\'padding:6px 8px\'>ESTADO</th></tr>" & '
           'Concat(FirstN(Sort(Filter(colPrestamos, !IsBlank(IdPrestamo)), IdPrestamo, SortOrder.Descending), 4), ' + fila + ') & "</table></div></div>"')
    ctrls.append(f'''      - htmlActividad_0:
          Control: HtmlViewer@2.1.0
          Properties:
            Fill: =RGBA(0, 0, 0, 0)
            Height: =250
            HtmlText: |-
              ={act}
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =1264
            X: =90
            Y: =498''')
    ctrls.append(rail('0', 'Inicio'))
    return pantalla('scrInicio', 'ClearCollect(colPrestamos, tblPrestamos); ClearCollect(colFicha, tblFichaDescarte); Set(varMenu, false)', ctrls)


def en_construccion(scr, sfx, titulo, texto):
    aviso = f'''      - htmlProximamente_{sfx}:
          Control: HtmlViewer@2.1.0
          Properties:
            Height: =300
            HtmlText: |-
              ="<div style='margin:6px;height:280px;box-sizing:border-box;background:#FFFFFF;border:1px solid #DADCDF;box-shadow:0 12px 28px rgba(17,17,17,0.10);font-family:Segoe UI,Arial,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center'><div style='font-size:10px;letter-spacing:3px;color:#8A8D91;font-weight:700'>EN CONSTRUCCIÓN</div><div style='font-size:26px;font-weight:700;color:#111111;margin-top:10px'>{titulo}</div><div style='font-size:12px;color:#3F4247;margin-top:8px'>{texto}</div></div>"
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =900
            X: =283
            Y: =260'''
    return pantalla(scr, CARGA, [header(sfx, titulo), aviso, rail(sfx, titulo)])


BRILLO_SVG = ("<img style='display:block' src='data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%221366%22 height=%22112%22>"
              "<defs><clipPath id=%22c%22><rect x=%2284%22 y=%2214%22 width=%221264%22 height=%2272%22 rx=%2218%22/></clipPath>"
              "<linearGradient id=%22g%22 x1=%220%22 x2=%221%22><stop offset=%220%22 stop-color=%22white%22 stop-opacity=%220%22/>"
              "<stop offset=%220.5%22 stop-color=%22white%22 stop-opacity=%220.22%22/><stop offset=%221%22 stop-color=%22white%22 stop-opacity=%220%22/></linearGradient></defs>"
              "<g clip-path=%22url(%23c)%22><rect y=%2214%22 width=%22220%22 height=%2272%22 fill=%22url(%23g)%22 transform=%22skewX(-20)%22>"
              "<animate attributeName=%22x%22 values=%22-300;1700;1700%22 keyTimes=%220;0.5;1%22 dur=%227s%22 repeatCount=%22indefinite%22/></rect></g></svg>'/>")

# Marcador (cinta) con destello, para las tarjetas
def cinta(w=24, h=36, pos="right:22px;top:0"):
    return (f"<img style='position:absolute;{pos};z-index:2' src='data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 "
            f"width=%22{w}%22 height=%22{h}%22><defs><linearGradient id=%22r%22 x1=%220%22 y1=%220%22 x2=%221%22 y2=%221%22>"
            "<stop offset=%220%22 stop-color=%22%230B0B0C%22/><stop offset=%220.5%22 stop-color=%22%2335373B%22/><stop offset=%221%22 stop-color=%22%23111111%22/></linearGradient>"
            "<linearGradient id=%22s%22 x1=%220%22 x2=%221%22><stop offset=%220%22 stop-color=%22white%22 stop-opacity=%220%22/><stop offset=%220.5%22 stop-color=%22white%22 stop-opacity=%220.85%22/>"
            f"<stop offset=%221%22 stop-color=%22white%22 stop-opacity=%220%22/></linearGradient><clipPath id=%22k%22><polygon points=%220,0 {w},0 {w},{h} {w//2},{int(h*0.78)} 0,{h}%22/></clipPath></defs>"
            f"<g clip-path=%22url(%23k)%22><rect width=%22{w}%22 height=%22{h}%22 fill=%22url(%23r)%22/><rect x=%22-20%22 width=%2212%22 height=%22{h}%22 fill=%22url(%23s)%22 transform=%22skewX(-15)%22>"
            f"<animate attributeName=%22x%22 values=%22-20;{w + 20};{w + 20}%22 keyTimes=%220;0.3;1%22 dur=%224s%22 repeatCount=%22indefinite%22/></rect></g>"
            f"<polygon points=%220,0 {w},0 {w},{h} {w//2},{int(h*0.78)} 0,{h}%22 fill=%22none%22 stroke=%22%238A8D91%22 stroke-width=%221%22/></svg>'/>")

def brillo(sfx):
    """Reflejo plateado que cruza el encabezado cada 7 segundos."""
    return f'''      - htmlBrillo_{sfx}:
          Control: HtmlViewer@2.1.0
          Properties:
            Fill: =RGBA(0, 0, 0, 0)
            Height: =112
            HtmlText: |-
              ="{BRILLO_SVG}"
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =1366
            X: =0
            Y: =0'''

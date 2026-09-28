import re, sys
sys.path.insert(0, '.')
from tabs import tabs, label, switch

SRC = 'base.txt'
OUT1 = '/home/user/Power-Apps/descarte/Pantalla_1_Lectura_1a1.txt'
OUT2 = '/home/user/Power-Apps/descarte/Pantalla_2_Lectura_Masiva.txt'
S1, S2 = 'scrDescarteB', 'scrDescarteMasiva'

L = open(SRC).read().rstrip('\n').split('\n')
start = next(i for i, l in enumerate(L) if l.startswith('      - '))
head, body = L[:start], L[start:]
blocks = []
for l in body:
    if l.startswith('      - '):
        blocks.append([l])
    else:
        blocks[-1].append(l)

def name(b): return b[0].strip()[2:-1]
def prop(b, p):
    for l in b:
        m = re.match(r'            %s: =(-?\d+)$' % p, l)
        if m: return int(m.group(1))
def setp(b, p, v):
    for i, l in enumerate(b):
        if l.startswith('            %s: ' % p):
            b[i] = '            %s: %s' % (p, v); return
    raise KeyError((name(b), p))
def addp(b, p, v):
    # insert keeping alphabetical order within Properties
    idx = [i for i, l in enumerate(b) if re.match(r'            [A-Za-z]', l)]
    pos = next((i for i in idx if b[i].strip().split(':')[0] > p), idx[-1] + 1)
    b.insert(pos, '            %s: %s' % (p, v))
byname = {}

# ---------- Pantalla 1: lectura 1 a 1 ----------
blocks = [b for b in blocks if name(b) not in {'lineStepper', 'dotPaso1', 'dotPaso2', 'dotPaso3', 'dotPaso4'}]
for b in blocks:
    x, y = prop(b, 'X'), prop(b, 'Y')
    if x is not None and y is not None and x < 620 and 130 <= y <= 700:
        setp(b, 'Y', '=%d' % (y + 40))
    byname[name(b)] = b
setp(byname['drpCruce_1'], 'Default', '="Esta en archivo"')
setp(byname['lbl_drpCruce_1'], 'Text', '="ACTIVO FIJO · SI POR DEFECTO"')
setp(byname['lbl_drpUnidadDescarte_1'], 'Text', '="BIBLIOTECA"')
setp(byname['txtEscaneo_1'], 'Width', '=360')
r = byname['btnRafaga_1']
setp(r, 'Fill', '=RGBA(0, 0, 0, 0)')
setp(r, 'HoverFill', '=RGBA(191, 195, 200, 0.18)')
setp(r, 'PressedFill', '=RGBA(27, 42, 74, 0.55)')
setp(r, 'Text', '=If(varRafaga, "●  ESCÁNER · ON", "○  ESCÁNER · OFF")')
addp(byname['txtEscaneo_1'], 'PaddingRight', '=56')


# ---------- Pantalla 2: lectura masiva ----------
def copy(n, new=None, sets=None, adds=None):
    b = [l for l in byname[n]]
    b = '\n'.join(b).replace('_1:', '_2:').replace('drpCriterio_1', 'drpCriterio_2').split('\n')
    b[0] = '      - %s:' % (new or n.replace('_1', '_2'))
    for k, v in (sets or {}).items(): setp(b, k, v)
    for k, v in (adds or {}).items(): addp(b, k, v)
    return '\n'.join(b)

hdr = '\n'.join(byname['htmlHeader']).replace('- htmlHeader:', '- htmlHeader_2:')
VARS = {'drpUnidadDescarte': 'varLoteBiblioteca', 'drpInventario': 'varLoteInventario', 'drpCriterio': 'varLoteCriterio', 'drpJustificacion': 'varLoteJustificacion'}
for base, v in VARS.items():
    addp(byname[base + '_1'], 'Default', '=' + v)
    addp(byname[base + '_1'], 'OnChange', '=Set(%s, Self.Selected.Value)' % v)
lote = [
    copy('lblPasoLote', 'lblPasoLote_2'),
    copy('lbl_drpUnidadDescarte_1'),
    copy('drpUnidadDescarte_1'),
    copy('lbl_drpInventario_1'),
    copy('drpInventario_1'),
    copy('lbl_drpCriterio_1'),
    copy('drpCriterio_1'),
    copy('lbl_drpJustificacion_1'),
    copy('drpJustificacion_1'),
]

CODIGOS = 'Distinct(Filter(Split(Substitute(Substitute(Substitute(Substitute(Substitute(txtTanda_2.Text, Char(13), Char(10)), Char(9), Char(10)), ",", Char(10)), ";", Char(10)), " ", Char(10)), Char(10)), !IsBlank(Trim(Value))), Trim(Value))'
LOTE_OK = '!IsBlank(drpUnidadDescarte_2.Selected.Value) && !IsBlank(drpJustificacion_2.Selected.Value) && !IsBlank(drpInventario_2.Selected.Value)'
NLISTOS = 'CountIf(colTanda, Estado = "Listo")'
SILVER_ON = "<div style='height:%dpx;background:linear-gradient(115deg,#0B0B0C 0%%,#111111 38%%,#35373B 50%%,#111111 62%%,#0B0B0C 100%%);border-top:1px solid #8A8D91;box-shadow:0 6px 14px rgba(17,17,17,0.25)'></div>"
SILVER_OFF = "<div style='height:%dpx;background:linear-gradient(115deg,#BFC3C8 0%%,#DADCDF 50%%,#BFC3C8 100%%)'></div>"

def fondo(n, boton, x, y, w, h):
    return f'''      - {n}:
          Control: HtmlViewer@2.1.0
          Properties:
            Height: ={h}
            HtmlText: |-
              =If({boton}.DisplayMode = DisplayMode.Disabled, "{SILVER_OFF % h}", "{SILVER_ON % h}")
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: ={w}
            X: ={x}
            Y: ={y}'''

def boton_negro(n, text, displaymode, onselect, x, y, w, h, size=12):
    body = '\n'.join('              ' + l for l in ('=' + onselect.strip('\n')).split('\n'))
    return f'''      - {n}:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =0
            Color: =ColorValue("#FFFFFF")
            DisabledColor: =ColorValue("#FFFFFF")
            DisabledFill: =RGBA(0, 0, 0, 0)
            DisplayMode: ={displaymode}
            Fill: =RGBA(0, 0, 0, 0)
            Font: =Font.'Segoe UI'
            FontWeight: =FontWeight.Bold
            Height: ={h}
            HoverColor: =ColorValue("#FFFFFF")
            HoverFill: =RGBA(191, 195, 200, 0.18)
            OnSelect: |-
{body}
            PressedFill: =RGBA(27, 42, 74, 0.55)
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: ={size}
            Text: ={text}
            Width: ={w}
            X: ={x}
            Y: ={y}'''

BUSCAR = f'''
Set(varNTanda, CountRows({CODIGOS}));
ClearCollect(colCodigos, FirstN({CODIGOS}, 200));
If(
    IsEmpty(colCodigos),
        Notify("Escanee o pegue al menos un código.", NotificationType.Warning),
    If(varNTanda > 200, Notify("Se buscan solo los primeros 200 códigos. Guarde y luego siga con el resto.", NotificationType.Warning));
    Set(varBuscandoTanda, true);
    Set(varT0, Now());
    Clear(colTanda);
    ClearCollect(colFicha, tblFichaDescarte);
    ForAll(
        Sequence(CountRows(colCodigos)) As i,
        With(
            {{cod: Index(colCodigos, i.Value).Value}},
            With(
                {{r: IfError(Text('Copiade:BuscarLibroFOLIO'.Run(cod).datos), "")}},
                With(
                    {{j: ParseJSON(If(IsBlank(r), "{{}}", r))}},
                    Collect(
                        colTanda,
                        {{
                            Orden: i.Value,
                            Codigo: cod,
                            Estado: If(cod in colFicha.'Codigo de Barra', "Ya en ficha", IsBlank(r), "Error", Text(j.encontrado) = "SI", "Listo", "No en FOLIO"),
                            HRID: Text(j.hrid),
                            copia: Text(j.copia),
                            Tipo: Text(j.tipo),
                            Ubicacion: Text(j.ubicacion),
                            Titulo: Text(j.titulo),
                            Autor: Text(j.autor),
                            Idioma: Text(j.idioma),
                            Fecha: Text(j.fecha),
                            Anio: Text(j.anio),
                            PA: Coalesce(Value(j.exA), 0),
                            PF: Coalesce(Value(j.exF), 0),
                            Pos: Coalesce(Value(j.exP), 0),
                            Vina: Coalesce(Value(j.exV), 0)
                        }}
                    )
                )
            )
        )
    );
    Set(varSegTanda, DateDiff(varT0, Now(), TimeUnit.Seconds));
    Set(varBuscandoTanda, false)
)'''

GUARDAR = '''
Set(varGuardandoTanda, true);
Clear(colGuardados);
Clear(colFallidos);
With(
    {
        base: Coalesce(Max(colFicha, Value(Número)), 0),
        L: Sort(Filter(colTanda, Estado = "Listo"), Orden)
    },
    ForAll(
        Sequence(CountRows(L)) As i,
        With(
            {t: Index(L, i.Value)},
            IfError(
                Collect(
                    colGuardados,
                    Patch(
                        tblFichaDescarte,
                        Defaults(tblFichaDescarte),
                        {
                            Número: Text(base + i.Value),
                            'Item ingresado en la base de biblioteca': "SI",
                            HRID: t.HRID,
                            'Codigo de Barra': t.Codigo,
                            'Cruce Archivo activo Fijo (Finanzas)': "Esta en archivo",
                            'Valor Neto': "",
                            copia: t.copia,
                            'Tipo de Material': t.Tipo,
                            'Biblioteca-Ubicacion-Colección': t.Ubicacion,
                            Título: t.Titulo,
                            Autor: t.Autor,
                            Idioma: t.Idioma,
                            'Vinculado UAI (SI/NO)': "NO",
                            'Fecha registro (ingresado en la base)': t.Fecha,
                            'Número de POL *': "",
                            'Unidad Academica o Centro de Costo *': "Desconocida",
                            'Año de edición': t.Anio,
                            'Diferenciador de título por ficha descarte': If(IsBlank(t.HRID) || t.HRID in colFicha.HRID || (i.Value > 1 && t.HRID in FirstN(L, i.Value - 1).HRID), 0, 1),
                            'Unidad de descarte': drpUnidadDescarte_2.Selected.Value,
                            'Pregrado  A - Existencia': t.PA,
                            'Pregrado  F - Existencia': t.PF,
                            'Posgrado - Existencia': t.Pos,
                            'Viña - Existencia': t.Vina,
                            'Informar a Finanzas (SI/NO)': "SI",
                            'Forma de Adquisición': "Desconocida",
                            'Bibliografía de programas académicos (SI/NO)': "Por confirmar",
                            'Obra en Volúmenes - Parte de una Colección (SI/NO)': "NO",
                            'Criterios de Descarte': drpCriterio_2.Selected.Value,
                            'Justificaciones para aplicar Descarte': drpJustificacion_2.Selected.Value,
                            'Relación Inventario': drpInventario_2.Selected.Value,
                            'Observaciones respecto de la justificación al Descarte': txtObsTanda_2.Text,
                            'Información para no Descartar': "",
                            'Decisión Final Descarte SI/NO': Blank()
                        }
                    )
                );
                true,
                Collect(colFallidos, {Codigo: t.Codigo});
                false
            )
        )
    )
);
ClearCollect(colFicha, tblFichaDescarte);
UpdateIf(colTanda, Codigo in colGuardados.'Codigo de Barra', {Estado: "Guardado"});
UpdateIf(colTanda, Codigo in colFallidos.Codigo, {Estado: "Error"});
If(CountRows(colGuardados) > 0,
    If(IsBlank(varInicio), Set(varInicio, Now()));
    Set(varContador, Coalesce(varContador, 0) + CountRows(colGuardados));
    Set(varUltimo, Last(colGuardados).Número & " — tanda de " & CountRows(colGuardados) & " libros")
);
Set(varGuardandoTanda, false);
If(
    IsEmpty(colFallidos),
        Notify("Guardados " & CountRows(colGuardados) & " libros en la ficha.", NotificationType.Success, 3000),
    Notify("Guardados " & CountRows(colGuardados) & ". No se pudieron guardar " & CountRows(colFallidos) & " (quedan en rojo; presione guardar de nuevo para reintentar).", NotificationType.Error)
)'''
# reintento: los "Error" de guardado vuelven a "Listo" antes de guardar
GUARDAR = GUARDAR.replace('Set(varGuardandoTanda, true);', 'Set(varGuardandoTanda, true);\nUpdateIf(colTanda, Estado = "Error" && Codigo in colFallidos.Codigo, {Estado: "Listo"});', 1)
# mover Clear(colFallidos) después del UpdateIf de reintento
GUARDAR = GUARDAR.replace('Clear(colGuardados);\nClear(colFallidos);', 'Clear(colGuardados);\nClear(colFallidos);')

VACIAR = '''
Clear(colTanda);
Clear(colCodigos);
Clear(colFallidos);
Set(varTandaTexto, "");
Reset(txtTanda_2);
Reset(txtObsTanda_2);
SetFocus(txtTanda_2)'''

def badge(color, txt):
    return f"<span style='display:inline-block;padding:2px 7px;margin-left:4px;font-size:9px;font-weight:700;letter-spacing:.5px;color:#FFFFFF;background:{color}'>{txt}</span>"

COLOR_ESTADO = 'Switch(Estado, "Listo", "#1B2A4A", "Ya en ficha", "#8A8D91", "Guardado", "#111111", "#B3261E")'
PREVIA = f'''=With(
    {{T: Sort(colTanda, Orden)}},
    "<div style='margin:10px 12px;height:448px;box-sizing:border-box;background:#FFFFFF;border:1px solid #DADCDF;box-shadow:0 12px 28px rgba(17,17,17,0.10),0 2px 6px rgba(138,141,145,0.25);font-family:Segoe UI,Arial,sans-serif;display:flex;flex-direction:column'>" &
    "<div style='height:3px;background:linear-gradient(90deg,#8A8D91,#FFFFFF,#BFC3C8,#FFFFFF,#8A8D91)'></div>" &
    "<div style='padding:14px 20px 8px;display:flex;justify-content:space-between;align-items:flex-start'>" &
    "<div><div style='font-size:15px;font-weight:700;color:#111111'>Vista previa de la tanda</div>" &
    "<div style='font-size:11px;color:#3F4247;margin-top:2px'>Revise antes de guardar. Título, autor y existencias vienen de FOLIO.</div></div>" &
    "<div style='white-space:nowrap'>" &
    If(CountIf(T, Estado = "Listo") > 0, "{badge('#1B2A4A', '" & CountIf(T, Estado = "Listo") & " LISTOS')}", "") &
    If(CountIf(T, Estado = "Guardado") > 0, "{badge('#111111', '" & CountIf(T, Estado = "Guardado") & " GUARDADOS')}", "") &
    If(CountIf(T, Estado = "Ya en ficha") > 0, "{badge('#8A8D91', '" & CountIf(T, Estado = "Ya en ficha") & " YA EN FICHA')}", "") &
    If(CountIf(T, Estado = "No en FOLIO") > 0, "{badge('#B3261E', '" & CountIf(T, Estado = "No en FOLIO") & " NO EN FOLIO')}", "") &
    If(CountIf(T, Estado = "Error") > 0, "{badge('#B3261E', '" & CountIf(T, Estado = "Error") & " CON ERROR')}", "") &
    "</div></div>" &
    If(
        IsEmpty(T),
        "<div style='flex:1;display:flex;align-items:center;justify-content:center;font-size:12px;color:#8A8D91;padding:0 40px;text-align:center'>" &
        If(varBuscandoTanda, "Buscando en FOLIO…", "Escanee o pegue los códigos a la izquierda y presione 1 · BUSCAR EN FOLIO.") & "</div>",
        "<div style='flex:1;overflow-y:auto;padding:0 20px 12px'><table style='width:100%;border-collapse:collapse;font-size:11px;color:#111111'>" &
        "<tr style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;font-weight:700;text-align:left;border-bottom:1px solid #111111'>" &
        "<th style='padding:6px 6px'>CÓDIGO</th><th style='padding:6px 6px'>TÍTULO</th><th style='padding:6px 6px'>A·F·POS·VIÑA</th><th style='padding:6px 6px'>ESTADO</th></tr>" &
        Concat(
            T,
            "<tr style='border-bottom:1px solid #DADCDF'>" &
            "<td style='padding:6px;font-weight:700'>" & Substitute(Substitute(Codigo, "&", "&amp;"), "<", "&lt;") & "</td>" &
            "<td style='padding:6px'>" & If(IsBlank(Titulo), "—", Substitute(Substitute(Titulo, "&", "&amp;"), "<", "&lt;")) & "</td>" &
            "<td style='padding:6px;white-space:nowrap'>" & If(Estado = "No en FOLIO" || Estado = "Error", "—", PA & "·" & PF & "·" & Pos & "·" & Vina) & "</td>" &
            "<td style='padding:6px'><span style='display:inline-block;padding:2px 7px;font-size:9px;font-weight:700;color:#FFFFFF;background:" & {COLOR_ESTADO} & "'>" & Upper(Estado) & "</span></td></tr>"
        ) &
        "</table></div>"
    ) &
    "</div>"
)'''

def indent(s, n=14):
    return '\n'.join(' ' * n + l for l in s.split('\n'))

controles2 = [
    hdr,
    switch('2', True, S1, 'Pegue o escanee muchos códigos'),
    *lote,
    label('lblPasoCodigos_2', '="Códigos de la tanda"', 80, 324, 250, h=20, size=11, color='#111111'),
    label('lblConteo_2', f'=CountRows({CODIGOS}) & " CÓDIGOS · MÁX. 200"', 340, 328, 240, color='#8A8D91', align='Right'),
    f'''      - txtTanda_2:
          Control: Classic/TextInput@2.3.2
          Properties:
            BorderColor: =ColorValue("#1B2A4A")
            Color: =ColorValue("#1B2A4A")
            Default: =varTandaTexto
            Fill: =ColorValue("#FFFFFF")
            FocusedBorderColor: =ColorValue("#111111")
            FocusedBorderThickness: =2
            Font: =Font.'Courier New'
            Height: =200
            HintText: ="Escanee o pegue un código por línea…"
            Mode: =TextMode.MultiLine
            PaddingLeft: =14
            PaddingRight: =60
            PaddingTop: =10
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: =11
            Width: =500
            X: =80
            Y: =348''',
    label('lbl_txtObsTanda_2', '="OBSERVACIONES (SE APLICA A TODA LA TANDA)"', 80, 556, 500),
    f'''      - txtObsTanda_2:
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
            Width: =500
            X: =80
            Y: =570''',
    fondo('htmlBuscarFondo_2', 'btnBuscarTanda_2', 80, 614, 500, 48),
    boton_negro('btnBuscarTanda_2',
                'If(varBuscandoTanda, "BUSCANDO EN FOLIO…", "1 · BUSCAR EN FOLIO   →")',
                'If(varBuscandoTanda || varGuardandoTanda, DisplayMode.Disabled, DisplayMode.Edit)',
                BUSCAR, 80, 614, 500, 48),
    f'''      - barProgresoFondo_2:
          Control: Rectangle@2.3.0
          Properties:
            Fill: =ColorValue("#DADCDF")
            Height: =4
            Visible: =varBuscandoTanda || !IsEmpty(colTanda)
            Width: =500
            X: =80
            Y: =668
      - barProgreso_2:
          Control: Rectangle@2.3.0
          Properties:
            Fill: =ColorValue("#1B2A4A")
            Height: =4
            Visible: =varBuscandoTanda || !IsEmpty(colTanda)
            Width: =500 * Min(CountRows(colTanda) / Max(CountRows(colCodigos), 1), 1)
            X: =80
            Y: =668''',
    label('lblProgreso_2',
          '=If(varBuscandoTanda, "Buscando… " & CountRows(colTanda) & " de " & CountRows(colCodigos), IsEmpty(colTanda), "", CountRows(colTanda) & " procesados en " & varSegTanda & " s · " & CountIf(colTanda, Estado = "Listo") & " listos · " & CountIf(colTanda, Estado = "Ya en ficha") & " ya en ficha · " & CountIf(colTanda, Estado = "No en FOLIO") & " no encontrados")',
          80, 678, 500, h=16, size=8, color='#3F4247', bold=False),
    f'''      - htmlPrevia_2:
          Control: HtmlViewer@2.1.0
          Properties:
            Height: =472
            HtmlText: |-
{indent(PREVIA)}
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =710
            X: =628
            Y: =156''',
    fondo('htmlGuardarFondo_2', 'btnGuardarTanda_2', 640, 640, 516, 56),
    boton_negro('btnGuardarTanda_2',
                f'If(varGuardandoTanda, "GUARDANDO…", "2 · GUARDAR " & {NLISTOS} & " EN LA FICHA   →")',
                f'If({NLISTOS} > 0 && {LOTE_OK} && !varBuscandoTanda && !varGuardandoTanda, DisplayMode.Edit, DisplayMode.Disabled)',
                GUARDAR, 640, 640, 516, 56, size=13),
    f'''      - btnVaciar_2:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =ColorValue("#BFC3C8")
            BorderThickness: =1
            Color: =ColorValue("#111111")
            DisplayMode: =If(varBuscandoTanda || varGuardandoTanda, DisplayMode.Disabled, DisplayMode.Edit)
            Fill: =ColorValue("#FFFFFF")
            Font: =Font.'Segoe UI'
            Height: =56
            HoverColor: =ColorValue("#FFFFFF")
            HoverFill: =ColorValue("#111111")
            OnSelect: |-
{indent('=' + VACIAR.strip())}
            PressedFill: =ColorValue("#3F4247")
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: =11
            Text: ="Vaciar tanda"
            Width: =156
            X: =1170
            Y: =640''',
    label('lblUltimo_2', '=If(IsBlank(varUltimo), "Aún no se guarda ningún libro en esta sesión.", "Último guardado: N° " & varUltimo)',
          640, 704, 686, h=18, size=9, color='#3F4247', bold=False),
]
screen2 = f'''Screens:
  {S2}:
    Properties:
      Fill: =ColorValue("#FFFFFF")
      OnVisible: =ClearCollect(colFicha, tblFichaDescarte); SetFocus(txtTanda_2)
    Children:
''' + '\n'.join(controles2) + '\n'
open(OUT2, 'w').write(screen2)

# ---------- escribir pantalla 1 ----------
extra_top = switch('1', False, S2, 'Escanee libro por libro').split('\n')
extra_scan = label('lblFuentes_1', '="LECTOR · CÁMARA · TECLADO"', 380, 342, 200, align='Right').split('\n')
fondo_rafaga = fondo('htmlRafagaFondo_1', 'btnRafaga_1', 452, 362, 128, 52).split('\n')
out = []
for b in blocks:
    out += b
    if name(b) == 'htmlHeader': out += extra_top
    if name(b) == 'btnRafaga_1': out[len(out)-len(b):len(out)-len(b)] = fondo_rafaga
    if name(b) == 'lblPasoEscanear': out += extra_scan
open(OUT1, 'w').write('\n'.join(head + out) + '\n')

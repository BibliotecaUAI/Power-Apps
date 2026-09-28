
# Genera pantallas/6_Panel.txt → pantalla de MOROSOS (datos reales de FOLIO vía flujo ListaMorososFOLIO)
from comun import (label, header, rail, pantalla, CARD, ESC, html, boton, fondo, oculto, lista, badge, validar)

NIVEL = 'If(Dias < 61, "Nivel 0", Dias < 731, "Nivel 1", Dias < 1825, "Nivel 2", "Nivel 3")'

CARGAR = '''
Set(varCargandoMor, true);
Set(varResMor, IfError(Text(ListaMorososFOLIO.Run("todos").datos), Notify("Error del flujo ListaMorososFOLIO: " & FirstError.Message, NotificationType.Error); Blank()));
Set(varCargandoMor, false);
If(
    IsBlank(varResMor),
        Notify("El flujo ListaMorososFOLIO respondió vacío: revise la caja Respond (ver instrucciones).", NotificationType.Warning),
    With(
        {j: With({o: ParseJSON(If(IsBlank(varResMor), "{}", varResMor))}, If(IsBlank(Text(o.datos)), o, ParseJSON(Text(o.datos))))},
        Set(varMorTotal, Coalesce(Value(Text(j.total)), 0));
        Set(varMorLibros, Coalesce(Value(Text(j.libros)), 0));
        ClearCollect(
            colMorosos,
            ForAll(
                Table(j.lista),
                {
                    RUT: Text(ThisRecord.Value.rut),
                    Nombre: Text(ThisRecord.Value.nombre),
                    Correo: Text(ThisRecord.Value.correo),
                    Tipo: Text(ThisRecord.Value.tipo),
                    Biblioteca: Text(ThisRecord.Value.bib),
                    Libros: Coalesce(Value(Text(ThisRecord.Value.n)), 0),
                    Dias: Coalesce(Value(Text(ThisRecord.Value.dias)), 0)
                }
            )
        );
        Set(varMorFecha, Now())
    )
);
Select(btnFiltrar_6)'''

FILTRAR = '''
ClearCollect(
    colMorVista,
    Sort(
        Filter(
            AddColumns(colMorosos, Nivel, ''' + NIVEL + '''),
            (IsBlank(txtBuscarMor_6.Text) || Lower(txtBuscarMor_6.Text) in Lower(Nombre) || txtBuscarMor_6.Text in RUT),
            (IsBlank(drpNivelMor_6.Selected.Value) || drpNivelMor_6.Selected.Value = "Todos los niveles" || Nivel = drpNivelMor_6.Selected.Value),
            (IsBlank(drpBibMor_6.Selected.Value) || drpBibMor_6.Selected.Value = "Todas las bibliotecas" || Biblioteca = drpBibMor_6.Selected.Value)
        ),
        Dias,
        SortOrder.Descending
    )
)'''

CORREO = ('"<div style=\'font-family:Segoe UI,Arial,sans-serif;color:#111111\'><div style=\'background:#111111;color:#FFFFFF;padding:18px 22px\'>'
          '<div style=\'font-size:10px;letter-spacing:3px;color:#BFC3C8\'>BIBLIOTECAS UAI</div><div style=\'font-size:20px;font-weight:700\'>Usuarios morosos en FOLIO</div></div>'
          '<div style=\'padding:18px 22px\'><p>" & CountRows(colMorVista) & " usuarios · filtro: " & drpNivelMor_6.Selected.Value & " · " & drpBibMor_6.Selected.Value & "</p>'
          '<table style=\'border-collapse:collapse;font-size:12px\'><tr style=\'border-bottom:1px solid #111111;text-align:left\'><th style=\'padding:5px 8px\'>RUT</th><th style=\'padding:5px 8px\'>Nombre</th>'
          '<th style=\'padding:5px 8px\'>Correo</th><th style=\'padding:5px 8px\'>Libros</th><th style=\'padding:5px 8px\'>Días</th><th style=\'padding:5px 8px\'>Nivel</th></tr>" & '
          'Concat(colMorVista, "<tr style=\'border-bottom:1px solid #DADCDF\'><td style=\'padding:5px 8px\'>" & RUT & "</td><td style=\'padding:5px 8px\'>" & Nombre & "</td><td style=\'padding:5px 8px\'>" & Correo & '
          '"</td><td style=\'padding:5px 8px\'>" & Libros & "</td><td style=\'padding:5px 8px\'>" & Dias & "</td><td style=\'padding:5px 8px\'>" & Nivel & "</td></tr>") & "</table></div></div>"')

ENVIAR = '''
IfError(
    Office365Outlook.SendEmailV2(
        Coalesce(varCorreoPrueba, "pablo.salas.marin@uai.cl"),
        "Morosos FOLIO · " & Text(Today(), "dd-mm-yyyy"),
        ''' + CORREO + '''
    );
    Notify("Lista enviada a " & Coalesce(varCorreoPrueba, "pablo.salas.marin@uai.cl"), NotificationType.Success, 3000),
    Notify("No se pudo enviar el correo.", NotificationType.Error)
)'''


def kpi(valor, etiqueta, plata=False):
    color = '#111111'
    return ("<div style='flex:1;padding:4px 18px;border-right:1px solid #DADCDF'><div style='font-size:26px;font-weight:700;color:" + color + "'>\" & "
            + valor + " & \"</div><div style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;font-weight:700'>" + etiqueta + "</div></div>")


KPIS = ('"' + CARD % (96, '1px solid #DADCDF') + "<div style='display:flex;align-items:center'>"
        + kpi('Text(varMorTotal, "#,##0")', 'USUARIOS MOROSOS EN FOLIO')
        + kpi('Text(varMorLibros, "#,##0")', 'LIBROS VENCIDOS')
        + kpi('CountRows(Filter(colMorosos, Dias >= 731))', 'CON MÁS DE 2 AÑOS')
        + kpi('CountRows(Filter(colMorosos, Dias >= 1825))', 'CON MÁS DE 5 AÑOS')
        + "</div></div></div>\"")

fila = ('"<tr style=\'border-bottom:1px solid #DADCDF;" & If(Dias >= 731, "box-shadow:inset 3px 0 0 #B3261E;", "") & "\'>'
        '<td style=\'padding:6px;font-weight:700\'>" & ' + ESC.format(x='RUT')
        + ' & "</td><td style=\'padding:6px\'>" & ' + ESC.format(x='Nombre')
        + ' & "</td><td style=\'padding:6px\'>" & ' + ESC.format(x='Tipo')
        + ' & "</td><td style=\'padding:6px\'>" & ' + ESC.format(x='Biblioteca')
        + ' & "</td><td style=\'padding:6px;text-align:center\'>" & Libros & "</td><td style=\'padding:6px;text-align:center\'>" & Text(Dias, "#,##0")'
        + ' & "</td><td style=\'padding:6px\'>" & If(Nivel = "Nivel 0", "' + badge('" & Upper(Nivel) & "') + '", "' + badge('" & Upper(Nivel) & "', True) + '") & "</td></tr>"')
vacio = "<div style='padding:70px 0;text-align:center;font-size:12px;color:#8A8D91'>%s</div>"
TABLA = ('"' + CARD % (416, '1px solid #DADCDF')
         + "<div style='display:flex;justify-content:space-between;align-items:baseline'><div style='font-size:15px;font-weight:700;color:#111111'>Usuarios morosos</div>"
         + "<div style='font-size:10px;color:#8A8D91'>\" & CountRows(colMorVista) & \" en la vista · se muestran los 150 con más días\" & If(IsBlank(varMorFecha), \"\", \" · consultado \" & Text(varMorFecha, \"hh:mm\")) & \"</div></div>\" & "
         + 'If(IsEmpty(colMorVista), If(varCargandoMor, "' + vacio % 'Consultando FOLIO…' + '", "' + vacio % 'Sin datos. Presione ACTUALIZAR DESDE FOLIO.' + '"), '
         + '"<div style=\'margin-top:10px;max-height:340px;overflow-y:auto\'><table style=\'width:100%;border-collapse:collapse;font-size:11px;color:#111111\'>'
         + "<tr style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;border-bottom:1px solid #111111;text-align:left'><th style='padding:6px'>RUT</th><th style='padding:6px'>NOMBRE</th>"
         + "<th style='padding:6px'>TIPO</th><th style='padding:6px'>BIBLIOTECA</th><th style='padding:6px'>LIBROS</th><th style='padding:6px'>DÍAS</th><th style='padding:6px'>NIVEL</th></tr>\" & "
         + 'Concat(FirstN(colMorVista, 150), ' + fila + ') & "</table></div>") & "</div></div>"')

texto_buscar = '''      - txtBuscarMor_6:
          Control: Classic/TextInput@2.3.2
          Properties:
            BorderColor: =ColorValue("#BFC3C8")
            BorderThickness: =1
            Color: =ColorValue("#111111")
            Default: =""
            Fill: =ColorValue("#FFFFFF")
            Font: =Font.'Segoe UI'
            Height: =30
            HintText: ="Buscar por nombre o RUT…"
            OnChange: =Select(btnFiltrar_6)
            PaddingLeft: =8
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: =9
            Width: =330
            X: =104
            Y: =142'''


def con_onchange(bloque):
    return bloque.replace('            Fill: =ColorValue("#FFFFFF")\n', '            Fill: =ColorValue("#FFFFFF")\n', 1).replace(
        '            PaddingLeft: =8\n', '            OnChange: =Select(btnFiltrar_6)\n            PaddingLeft: =8\n', 1)


ctrls = [
    header('6', 'Morosos'),
    texto_buscar,
    con_onchange(lista('drpNivelMor_6', 446, 142, 190, '["Todos los niveles", "Nivel 0", "Nivel 1", "Nivel 2", "Nivel 3"]', '"Todos los niveles"')),
    con_onchange(lista('drpBibMor_6', 648, 142, 240,
                       'Ungroup(Table({x: Table({Value: "Todas las bibliotecas"})}, {x: Sort(Distinct(Filter(colMorosos, !IsBlank(Biblioteca)), Biblioteca), Value)}), x)',
                       '"Todas las bibliotecas"')),
    label('lblNiveles_6', '="Nivel 0: hasta 60 días · Nivel 1: hasta 2 años · Nivel 2: hasta 5 años · Nivel 3: más de 5 años"',
          900, 142, 430, h=30, size=7, color='#8A8D91', bold=False),
    html('htmlKpis_6', 98, 180, 1240, 108, KPIS),
    html('htmlTabla_6', 98, 290, 1240, 428, TABLA),
    fondo('htmlActualizarFondo_6', 'btnActualizar_6', 104, 722, 400, 40),
    boton('btnActualizar_6', 104, 722, 400, 40, 'If(varCargandoMor, "CONSULTANDO FOLIO…", "↻  ACTUALIZAR DESDE FOLIO")', CARGAR,
          displaymode='If(varCargandoMor, DisplayMode.Disabled, DisplayMode.Edit)', size=10),
    label('lblDiag_6', '=If(varCargandoMor, "Consultando FOLIO…", IsBlank(varResMor), "Diagnóstico · FOLIO aún no responde (presione Actualizar).", IsEmpty(colMorVista), "Diagnóstico · recibidos " & CountRows(colMorosos) & " morosos, en vista " & CountRows(colMorVista) & " · respuesta (" & Len(varResMor) & " car.): " & Left(varResMor, 260), "")',
          520, 722, 820, h=40, size=8, color='#B3261E', bold=False),
    oculto('btnFiltrar_6', FILTRAR),
    oculto('btnCargar_6', CARGAR),
    rail('6', 'Morosos'),
]
ONV = ('ClearCollect(colPrestamos, tblPrestamos); Set(varCorreoPrueba, "pablo.salas.marin@uai.cl"); Set(varMenu, false); '
       'If(IsEmpty(colMorosos), Select(btnCargar_6), Select(btnFiltrar_6))')
OUT = '/home/user/Power-Apps/pantallas/6_Panel.txt'
open(OUT, 'w').write(pantalla('scrPanel', ONV, ctrls))
validar(OUT, 'scrPanel')


# Genera pantallas/6_Panel.txt → pantalla de MOROSOS (datos reales de FOLIO vía flujo ListaMorososFOLIO)
from comun import (label, header, rail, pantalla, CARD, ESC, html, boton, fondo, oculto, lista, badge, validar)

SIN_TILDES = ('Substitute(Substitute(Substitute(Substitute(Substitute(Substitute(Substitute({x}, "á", "a"), "é", "e"), "í", "i"), '
              '"ó", "o"), "ú", "u"), "ü", "u"), "ñ", "n")')
NIVEL = 'If(Dias < 61, "Nivel 0", Dias < 731, "Nivel 1", Dias < 1825, "Nivel 2", "Nivel 3")'

CARGAR = '''
Set(varCargandoMor, true);
Set(varResMor, IfError(Text(ListaMorososFOLIO.Run("todos").datos), Notify("Error del flujo ListaMorososFOLIO: " & FirstError.Message, NotificationType.Error); Blank()));
Set(varCargandoMor, false);
If(
    IsBlank(varResMor),
        Notify("El flujo ListaMorososFOLIO respondió vacío: revise la caja Respond (ver instrucciones).", NotificationType.Warning),
    With(
        {j: IfError(ParseJSON(Text(ParseJSON(varResMor).datos)), ParseJSON(varResMor))},
        With(
            {filas: IfError(Table(j.lista), Table(j))},
            Set(varMorTotal, Coalesce(IfError(Value(Text(j.total)), Blank()), IfError(Value(Text(First(filas).Value.total)), Blank()), CountRows(filas)));
            Set(varMorLibros, Coalesce(IfError(Value(Text(j.libros)), Blank()), IfError(Value(Text(First(filas).Value.libros)), Blank()), 0));
        ClearCollect(
            colMorosos,
            ForAll(
                filas,
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
    )
);
Select(btnFiltrar_6)'''

FILTRAR = '''
ClearCollect(
    colMorVista,
    Sort(
        Filter(
            AddColumns(colMorosos, Nivel, ''' + NIVEL + '''),
            (IsBlank(Trim(txtBuscarMor_6.Text)) || ''' + SIN_TILDES.format(x='Lower(Trim(txtBuscarMor_6.Text))') + ''' in ''' + SIN_TILDES.format(x='Lower(Nombre)') + '''
                || Upper(Substitute(Substitute(Substitute(Trim(txtBuscarMor_6.Text), ".", ""), "-", ""), " ", "")) in Upper(Substitute(Substitute(RUT, ".", ""), "-", ""))),
            (IsBlank(drpNivelMor_6.Selected.Value) || drpNivelMor_6.Selected.Value = "Todos los niveles" || Nivel = drpNivelMor_6.Selected.Value),
            (IsBlank(drpBibMor_6.Selected.Value) || drpBibMor_6.Selected.Value = "Todas las bibliotecas" || Biblioteca = drpBibMor_6.Selected.Value)
        ),
        Dias,
        SortOrder.Descending
    )
)'''

FILTRAR = FILTRAR + ''';
If(CountRows(colMorVista) = 1, Set(varSelRut, First(colMorVista).RUT); Select(btnDetalle_6))'''

DETALLE = '''
If(
    !IsBlank(varSelRut),
    Set(varCargandoDet, true);
    Set(varResDet, IfError(Text(DetalleMorosoFOLIO.Run(varSelRut).datos), Notify("Error del flujo DetalleMorosoFOLIO: " & FirstError.Message, NotificationType.Error); Blank()));
    Set(varCargandoDet, false);
    With(
        {j: IfError(ParseJSON(Text(ParseJSON(varResDet).datos)), ParseJSON(If(IsBlank(varResDet), "{}", varResDet)))},
        Set(varDet, {RUT: Text(j.rut), Nombre: Text(j.nombre), Apellido: Text(j.apellido), Correo: Text(j.correo), Tipo: Text(j.tipo),
                     Para: IfError(Text(j.para), ""), Html: IfError(Text(j.html), "")});
        ClearCollect(
            colDet,
            ForAll(
                IfError(Table(j.lista), Table(ParseJSON("[]"))),
                {
                    Titulo: Text(ThisRecord.Value.titulo),
                    Codigo: Text(ThisRecord.Value.codigo),
                    Bib: Text(ThisRecord.Value.bib),
                    Vence: Text(ThisRecord.Value.vence),
                    Dias: Coalesce(Value(Text(ThisRecord.Value.dias)), 0)
                }
            )
        )
    )
)'''

TD = "padding:6px 8px;border-bottom:1px solid #DADCDF"
CORREO_DET = (
    '"<div style=\'font-family:Calibri,Segoe UI,Arial,sans-serif;font-size:14px;color:#111111;max-width:720px\'>'
    '<p>Estimado/a " & Trim(varDet.Nombre & " " & varDet.Apellido) & ":</p>'
    '<p>Junto con saludar, me comunico con usted para solicitar la devolución de el/los préstamos a su nombre, '
    'que se encuentran vencidos desde la fecha que se indica a continuación:</p>'
    '<table style=\'border-collapse:collapse;font-size:13px;width:100%\'><tr style=\'background:#111111;color:#FFFFFF\'>'
    '<th style=\'padding:7px 8px;text-align:left\'>Título</th><th style=\'padding:7px 8px;text-align:center\'>Código</th>'
    '<th style=\'padding:7px 8px;text-align:left\'>Biblioteca</th><th style=\'padding:7px 8px;text-align:center\'>Vencido desde</th>'
    '<th style=\'padding:7px 8px;text-align:center\'>Días de atraso</th></tr>" & '
    'Concat(colDet, "<tr><td style=\'' + TD + '\'>" & Titulo & "</td><td style=\'' + TD + ';text-align:center\'>" & Codigo & '
    '"</td><td style=\'' + TD + '\'>" & Bib & "</td><td style=\'' + TD + ';text-align:center\'>" & Vence & '
    '"</td><td style=\'' + TD + ';text-align:center\'>" & Dias & "</td></tr>") & '
    '"</table><p>Solicitamos que realice la devolución en cualquiera de nuestras Bibliotecas a la brevedad, '
    'para evitar las sanciones que puedan restringir tus requerimientos en bibliotecas.</p>'
    '<p>Atentamente,<br>Bibliotecas UAI</p></div>"')

ENVIAR_DET = '''
With(
    {dest: If(drpDestino_6.Selected.Value = "Al correo del usuario", varDet.Correo, Coalesce(varCorreoPrueba, "pablo.salas.marin@uai.cl"))},
    If(
        IsEmpty(colDet) || IsBlank(dest),
            Notify("Primero elija un usuario con libros vencidos.", NotificationType.Warning),
        IfError(
            Office365Outlook.SendEmailV2(dest, "Bibliotecas UAI: Solicitud de devolución de material", ''' + CORREO_DET + ''', {Cc: "pablo.salas.marin@uai.cl", Importance: "Normal"});
            Notify("Correo enviado a " & dest, NotificationType.Success, 3000);
            true,
            Notify("No se pudo enviar el correo: " & FirstError.Message, NotificationType.Error)
        )
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
        '<td style=\'padding:6px;text-align:left;font-weight:700\'>" & ' + ESC.format(x='RUT')
        + ' & "</td><td style=\'padding:6px;text-align:left\'>" & ' + ESC.format(x='Nombre')
        + ' & "</td><td style=\'padding:6px;text-align:left\'>" & ' + ESC.format(x='Tipo')
        + ' & "</td><td style=\'padding:6px;text-align:center\'>" & Libros & "</td><td style=\'padding:6px;text-align:center\'>" & Text(Dias, "#,##0")'
        + ' & "</td><td style=\'padding:6px;text-align:center\'><span style=\'display:inline-block;padding:1px 10px;border-radius:999px;font-size:11px;'
          'border:1px solid #BFC3C8;box-shadow:0 0 6px rgba(191,195,200,0.55),inset 0 0 4px rgba(255,255,255,0.6)\'>" & Nivel & "</span></td></tr>"')
vacio = "<div style='padding:70px 0;text-align:center;font-size:12px;color:#8A8D91'>%s</div>"
TABLA = ('"' + CARD % (416, '1px solid #DADCDF')
         + "<div style='display:flex;justify-content:space-between;align-items:baseline'><div style='font-size:15px;font-weight:700;color:#111111'>Usuarios morosos</div>"
         + "<div style='font-size:10px;color:#8A8D91'>\" & CountRows(colMorVista) & \" en la vista · se muestran hasta 300 · use el buscador\" & If(IsBlank(varMorFecha), \"\", \" · consultado \" & Text(varMorFecha, \"hh:mm\")) & \"</div></div>\" & "
         + 'If(IsEmpty(colMorVista), If(varCargandoMor, "' + vacio % 'Consultando FOLIO…' + '", "' + vacio % 'Sin datos. Presione ACTUALIZAR DESDE FOLIO.' + '"), '
         + '"<div style=\'margin-top:10px;max-height:340px;overflow-y:auto\'><table style=\'width:100%;border-collapse:collapse;table-layout:fixed;font-size:11px;color:#111111\'>'
         + "<colgroup><col style='width:105px'><col><col style='width:120px'><col style='width:62px'><col style='width:62px'><col style='width:82px'></colgroup>"
         + "<tr style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;border-bottom:1px solid #111111'><th style='padding:6px;text-align:left'>RUT</th><th style='padding:6px;text-align:left'>NOMBRE</th>"
         + "<th style='padding:6px;text-align:left'>TIPO</th><th style='padding:6px;text-align:center'>LIBROS</th><th style='padding:6px;text-align:center'>DÍAS</th><th style='padding:6px;text-align:center'>NIVEL</th></tr>\" & "
         + 'Concat(FirstN(colMorVista, 300), ' + fila + ') & "</table></div>") & "</div></div>"')

fila_det = ('"<tr style=\'border-bottom:1px solid #DADCDF\'><td style=\'padding:5px 4px;text-align:left\'>" & ' + ESC.format(x='Titulo')
            + ' & "<div style=\'font-size:9px;color:#8A8D91\'>" & Codigo & " · " & ' + ESC.format(x='Bib') + ' & "</div></td>'
            '<td style=\'padding:5px 4px;text-align:center;white-space:nowrap\'>" & Vence & "</td>'
            '<td style=\'padding:5px 4px;text-align:center;font-weight:700;color:#B3261E\'>" & Text(Dias, "#,##0") & "</td></tr>"')
DETALLE_HTML = ('"' + CARD % (416, '1px solid #DADCDF')
    + "<div style='font-size:15px;font-weight:700;color:#111111'>Detalle de morosidad</div>"
    + "<div style='font-size:11px;font-style:italic;color:#3F4247'>Elija un usuario (o búsquelo) y presione Ver detalle</div>"
    + "<div style='height:44px'></div>\" & "
    + 'If(varCargandoDet, "<div style=\'padding:40px 0;text-align:center;font-size:12px;color:#8A8D91\'>Consultando FOLIO…</div>", '
    + 'IsBlank(varDet.Nombre), "<div style=\'padding:40px 0;text-align:center;font-size:12px;color:#8A8D91\'>Sin usuario seleccionado.</div>", '
    + '"<div style=\'font-size:14px;font-weight:700;color:#111111\'>" & varDet.Nombre & " " & varDet.Apellido & "</div>'
    + "<div style='font-size:11px;color:#3F4247'>RUT \" & varDet.RUT & \" · \" & Coalesce(varDet.Tipo, \"Usuario\") & \"</div>"
    + "<div style='font-size:11px;font-style:italic;color:#3F4247;margin-bottom:6px'>\" & Coalesce(varDet.Correo, \"sin correo registrado\") & \"</div>"
    + "<div style='max-height:160px;overflow-y:auto'><table style='width:100%;border-collapse:collapse;table-layout:fixed;font-size:11px;color:#111111'>"
    + "<colgroup><col><col style='width:78px'><col style='width:52px'></colgroup>"
    + "<tr style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;border-bottom:1px solid #111111'><th style='padding:5px 4px;text-align:left'>LIBRO</th>"
    + "<th style='padding:5px 4px;text-align:center'>VENCIÓ</th><th style='padding:5px 4px;text-align:center'>DÍAS</th></tr>\" & "
    + 'Concat(colDet, ' + fila_det + ') & "</table></div>") & "</div></div>"')

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
    html('htmlTabla_6', 98, 290, 800, 428, TABLA),
    html('htmlDetalle_6', 904, 290, 434, 428, DETALLE_HTML),
    lista('drpSelMor_6', 926, 348, 290, 'ForAll(FirstN(colMorVista, 500), {Value: Nombre & " · " & RUT})', '""'),
    boton('btnVerDet_6', 1224, 348, 92, 30, 'If(varCargandoDet, "…", "Ver detalle")',
          'Set(varSelRut, Last(Split(drpSelMor_6.Selected.Value, " · ")).Value); Select(btnDetalle_6)',
          displaymode='If(IsBlank(drpSelMor_6.Selected.Value) || varCargandoDet, DisplayMode.Disabled, DisplayMode.Edit)', dark=False, size=9),
    label('lblDestino_6', '="ENVIAR A"', 926, 628, 80, h=30, size=7),
    lista('drpDestino_6', 1000, 628, 316, '["A mi correo (prueba)", "Al correo del usuario"]', '"A mi correo (prueba)"'),
    fondo('htmlEnviarFondo_6', 'btnEnviarDet_6', 926, 666, 390, 40),
    boton('btnEnviarDet_6', 926, 666, 390, 40, '"✉  ENVIAR CORREO DE MOROSIDAD"', ENVIAR_DET,
          displaymode='If(IsEmpty(colDet), DisplayMode.Disabled, DisplayMode.Edit)', size=10),
    oculto('btnDetalle_6', DETALLE),
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

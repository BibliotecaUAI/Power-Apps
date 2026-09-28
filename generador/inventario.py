
# Genera pantallas/7_Inventario.txt (toma de inventario: escanear estante, cruzar con FOLIO, informe por correo)
from comun import (label, header, rail, pantalla, CARD, ESC, BIBLIOTECAS, html, boton, fondo, oculto,
                   entrada, lista, texto, badge, validar)

CODIGOS = ('Distinct(Filter(Split(Substitute(Substitute(Substitute(Substitute(Substitute(txtPegarInv_7.Text, Char(13), Char(10)), Char(9), Char(10)), ",", Char(10)), ";", Char(10)), " ", Char(10)), Char(10)), '
           '!IsBlank(Trim(Value))), Trim(Value))')

PROCESAR = '''
Set(varBuscandoInv, true);
Set(varRepetidosInv, Coalesce(varRepetidosInv, 0) + CountRows(Filter(colCodInv, Value in colInv.Codigo)));
ClearCollect(colCodNuevos, Filter(colCodInv, !(Value in colInv.Codigo)));
Set(varInvBase, CountRows(colInv));
ForAll(
    Sequence(CountRows(colCodNuevos)) As i,
    With(
        {c: Index(colCodNuevos, i.Value)},
        With(
            {r: IfError(Text('Copiade:BuscarLibroFOLIO'.Run(c.Value).datos), "")},
            With(
                {j: ParseJSON(If(IsBlank(r), "{}", r))},
                With(
                    {enc: IfError(Text(j.encontrado), "") = "SI", ubic: IfError(Text(j.ubicacion), ""), esperada: Lower(Trim(txtUbicInv_7.Text))},
                    Collect(
                        colInv,
                        {
                            Orden: varInvBase + i.Value,
                            Codigo: c.Value,
                            Titulo: If(enc, IfError(Text(j.titulo), ""), "—"),
                            Autor: If(enc, IfError(Text(j.autor), ""), ""),
                            Tipo: If(enc, IfError(Text(j.tipo), ""), ""),
                            Ubic: ubic,
                            Hora: Text(Now(), "hh:mm"),
                            Estado: If(IsBlank(r), "ERROR", !enc, "NO EN FOLIO", !IsBlank(esperada) && !(esperada in Lower(ubic)), "OTRA UBICACIÓN", "OK")
                        }
                    )
                )
            )
        )
    )
);
Set(varBuscandoInv, false);
Clear(colCodInv)'''

ESCANEAR = '''
ClearCollect(colCodInv, {Value: varEntradaInv});
Select(btnProcesarInv_7);
Set(varEntradaInv, Blank());
Reset(txtInv_7);
SetFocus(txtInv_7)'''

PEGAR = '''
ClearCollect(colCodInv, ''' + CODIGOS + ''');
If(IsEmpty(colCodInv), Notify("Pegue al menos un código.", NotificationType.Warning), Select(btnProcesarInv_7));
Reset(txtPegarInv_7)'''

VACIAR = '''
Clear(colInv);
Clear(colCodInv);
Set(varRepetidosInv, 0);
Reset(txtInv_7);
Reset(txtPegarInv_7);
SetFocus(txtInv_7)'''

n_tot = 'CountRows(colInv)'
n_ok = 'CountRows(Filter(colInv, Estado = "OK"))'
n_otra = 'CountRows(Filter(colInv, Estado = "OTRA UBICACIÓN"))'
n_no = 'CountRows(Filter(colInv, Estado = "NO EN FOLIO" || Estado = "ERROR"))'

TD = "padding:6px 8px;border-bottom:1px solid #DADCDF"
CORREO = (
    '"<div style=\'font-family:Calibri,Segoe UI,Arial,sans-serif;font-size:14px;color:#111111;max-width:820px\'>'
    '<p><b>Inventario · " & drpBibInv_7.Selected.Value & If(IsBlank(Trim(txtUbicInv_7.Text)), "", " · " & Trim(txtUbicInv_7.Text)) & "</b><br>'
    '" & Text(Now(), "dd-mm-yyyy hh:mm") & " · " & User().FullName & "</p>'
    '<p>Escaneados: <b>" & ' + n_tot + ' & "</b> · En su lugar: <b>" & ' + n_ok + ' & "</b> · Otra ubicación: <b>" & ' + n_otra
    + ' & "</b> · No encontrados en FOLIO: <b>" & ' + n_no + ' & "</b> · Repetidos: <b>" & Coalesce(varRepetidosInv, 0) & "</b></p>'
    '<table style=\'border-collapse:collapse;font-size:12px;width:100%\'><tr style=\'background:#111111;color:#FFFFFF\'>'
    '<th style=\'padding:7px 8px;text-align:center\'>N°</th><th style=\'padding:7px 8px;text-align:center\'>Código</th>'
    '<th style=\'padding:7px 8px;text-align:left\'>Título</th><th style=\'padding:7px 8px;text-align:left\'>Ubicación en FOLIO</th>'
    '<th style=\'padding:7px 8px;text-align:center\'>Estado</th></tr>" & '
    'Concat(Sort(colInv, Orden), "<tr><td style=\'' + TD + ';text-align:center\'>" & Orden & "</td><td style=\'' + TD + ';text-align:center\'>" & Codigo & '
    '"</td><td style=\'' + TD + '\'>" & Titulo & "</td><td style=\'' + TD + '\'>" & Ubic & '
    '"</td><td style=\'' + TD + ';text-align:center;font-weight:700\'>" & Estado & "</td></tr>") & '
    '"</table><p>Bibliotecas UAI</p></div>"')

ENVIAR = '''
IfError(
    Office365Outlook.SendEmailV2(
        Coalesce(varCorreoPrueba, User().Email),
        "Inventario " & drpBibInv_7.Selected.Value & If(IsBlank(Trim(txtUbicInv_7.Text)), "", " · " & Trim(txtUbicInv_7.Text)) & " · " & Text(Today(), "dd-mm-yyyy"),
        ''' + CORREO + ''',
        {Cc: "pablo.salas.marin@uai.cl", Importance: "Normal"}
    );
    Set(varUltimoInv, ''' + n_tot + ''' & " libros enviados · " & Text(Now(), "hh:mm"));
    Notify("Informe enviado a " & Coalesce(varCorreoPrueba, User().Email), NotificationType.Success, 3000);
    true,
    Notify("No se pudo enviar el informe: " & FirstError.Message, NotificationType.Error)
)'''

estado = ('If(Estado = "OK", "' + badge('EN SU LUGAR') + '", Estado = "OTRA UBICACIÓN", "' + badge('OTRA UBICACIÓN', True)
          + '", Estado = "NO EN FOLIO", "' + badge('NO EN FOLIO', True) + '", "' + badge('ERROR', True) + '")')
sub = "<div style='font-size:9px;color:#8A8D91'>"
fila = ('"<tr style=\'border-bottom:1px solid #DADCDF;vertical-align:top\'>'
        '<td style=\'padding:7px 6px;text-align:center;color:#8A8D91\'>" & Orden & "</td>'
        '<td style=\'padding:7px 6px;font-weight:700;text-align:left\'>" & ' + ESC.format(x='Codigo')
        + ' & "</td><td style=\'padding:7px 6px;text-align:left\'><b>" & ' + ESC.format(x='Titulo') + ' & "</b>"'
        + ' & If(IsBlank(Autor) && IsBlank(Tipo), "", "' + sub + '" & ' + ESC.format(x='Autor') + ' & If(IsBlank(Tipo), "", " · " & ' + ESC.format(x='Tipo') + ') & "</div>")'
        + ' & "</td><td style=\'padding:7px 6px;text-align:left\'>" & If(IsBlank(Ubic), "—", ' + ESC.format(x='Ubic') + ')'
        + ' & "</td><td style=\'padding:7px 6px;text-align:center\'>" & ' + estado + ' & "</td></tr>"')

def kpi(valor, etiqueta):
    return ("<div style='flex:1;padding:2px 14px;border-right:1px solid #DADCDF'><div style='font-size:22px;font-weight:700;color:#111111'>\" & "
            + valor + " & \"</div><div style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;font-weight:700'>" + etiqueta + "</div></div>")

msg = "<div style='padding:60px 0;text-align:center;font-size:12px;color:#8A8D91'>Elija dónde está inventariando y escanee los libros del estante, uno tras otro.</div>"
TABLA = (
    '"' + CARD % (474, "1px solid #DADCDF")
    + "<div style='display:flex;justify-content:space-between;align-items:baseline'><div style='font-size:15px;font-weight:700;color:#111111'>Libros inventariados</div>"
    + "<div style='font-size:10px;font-style:italic;color:#8A8D91'>\" & If(varBuscandoInv, \"Consultando FOLIO…\", \"el último escaneado aparece arriba\") & \"</div></div>"
    + "<div style='display:flex;margin:10px 0 8px;border-top:1px solid #DADCDF;border-bottom:1px solid #DADCDF;padding:8px 0'>"
    + kpi(n_tot, 'ESCANEADOS') + kpi(n_ok, 'EN SU LUGAR') + kpi(n_otra, 'OTRA UBICACIÓN') + kpi(n_no, 'NO EN FOLIO') + kpi('Coalesce(varRepetidosInv, 0)', 'REPETIDOS')
    + "</div>\" & "
    + 'If(IsEmpty(colInv), "' + msg + '", '
    + '"<div style=\'max-height:318px;overflow-y:auto\'><table style=\'width:100%;border-collapse:collapse;table-layout:fixed;font-size:11px;color:#111111\'>'
    + "<colgroup><col style='width:38px'><col style='width:96px'><col><col style='width:170px'><col style='width:112px'></colgroup>"
    + "<tr style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;border-bottom:1px solid #111111'>"
    + "<th style='padding:6px;text-align:center'>N°</th><th style='padding:6px;text-align:left'>CÓDIGO</th><th style='padding:6px;text-align:left'>LIBRO</th>"
    + "<th style='padding:6px;text-align:left'>UBICACIÓN EN FOLIO</th><th style='padding:6px;text-align:center'>ESTADO</th></tr>\" & "
    + 'Concat(Sort(colInv, Orden, SortOrder.Descending), ' + fila + ') & "</table></div>") & "</div></div>"')

ctrls = [
    header('7', 'Inventario'),
    label('lblAviso_7', '="INVENTARIO · SE CRUZA CON FOLIO · EL INFORME LLEGA POR CORREO"', 104, 128, 480, h=16, size=7),
    label('lblPaso1_7', '="1 · Dónde"', 104, 158, 300, h=22, size=11, color='#111111'),
    label('lblCapBib_7', '="BIBLIOTECA"', 104, 184, 200),
    lista('drpBibInv_7', 104, 198, 200, BIBLIOTECAS, '"Biblioteca Viña"'),
    label('lblCapUbic_7', '="UBICACIÓN ESPERADA (OPCIONAL) · EJ.: COLECCIÓN GENERAL"', 320, 184, 260),
    texto('txtUbicInv_7', 320, 198, 260),
    label('lblPaso2_7', '="2 · Escanear"', 104, 244, 300, h=22, size=11, color='#111111'),
    label('lblCap2_7', '="CON LECTOR O PISTOLA DE CÓDIGO DE BARRAS · UNO TRAS OTRO"', 104, 270, 476),
    entrada('txtInv_7', 104, 286, 476, 'Código de barras del libro…',
            'If(!IsBlank(Trim(Self.Text)), Set(varEntradaInv, Trim(Self.Text)); Select(btnEscanearInv_7))'),
    label('lblCap3_7', '="O PEGUE UNA LISTA (DE UN LECTOR CON MEMORIA O UN EXCEL)"', 104, 356, 476),
    entrada('txtPegarInv_7', 104, 372, 476, 'Un código por línea…', 'false', h=150, multilinea=True),
    boton('btnPegarInv_7', 104, 530, 476, 36, 'If(varBuscandoInv, "CONSULTANDO FOLIO…", "AGREGAR LISTA PEGADA   →")', PEGAR,
          displaymode='If(varBuscandoInv, DisplayMode.Disabled, DisplayMode.Edit)', dark=False, size=10),
    label('lblAyuda_7', '="En su lugar: la ubicación de FOLIO contiene lo escrito en Ubicación esperada (si la deja vacía, todo lo encontrado queda En su lugar)."',
          104, 574, 476, h=32, size=8, color='#8A8D91', bold=False),
    html('htmlTabla_7', 634, 144, 698, 486, TABLA),
    boton('btnQuitarInv_7', 1190, 150, 120, 26, '"Quitar último"', 'Remove(colInv, Last(Sort(colInv, Orden)))',
          displaymode='If(IsEmpty(colInv), DisplayMode.Disabled, DisplayMode.Edit)', dark=False, size=8),
    fondo('htmlEnviarFondo_7', 'btnEnviarInv_7', 640, 640, 516, 56),
    boton('btnEnviarInv_7', 640, 640, 516, 56, '"ENVIAR INFORME (" & ' + n_tot + ' & ")   →"', ENVIAR,
          displaymode='If(IsEmpty(colInv) || varBuscandoInv, DisplayMode.Disabled, DisplayMode.Edit)'),
    boton('btnVaciarInv_7', 1170, 640, 156, 56, '"Vaciar"', VACIAR, dark=False, size=11),
    label('lblUltimo_7', '=If(IsBlank(varUltimoInv), "Aún no se envía ningún informe en esta sesión.", "Último informe: " & varUltimoInv)',
          640, 706, 686, h=18, size=9, color='#3F4247', bold=False),
    oculto('btnEscanearInv_7', ESCANEAR),
    oculto('btnProcesarInv_7', PROCESAR),
    rail('7', 'Inventario'),
]
ONV = ('If(!varInvIniciado, ClearCollect(colInv, {Orden: 0, Codigo: "", Titulo: "", Autor: "", Tipo: "", Ubic: "", Hora: "", Estado: ""}); '
       'Clear(colInv); ClearCollect(colCodInv, {Value: ""}); Clear(colCodInv); Set(varRepetidosInv, 0); Set(varInvIniciado, true)); '
       'Set(varMenu, false); SetFocus(txtInv_7)')
OUT = '/home/user/Power-Apps/pantallas/7_Inventario.txt'
open(OUT, 'w').write(pantalla('scrInventario', ONV, ctrls))
validar(OUT, 'scrInventario')

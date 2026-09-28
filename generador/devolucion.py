
# Genera pantallas/5_Devolucion.txt (devolución ficticia: cruza con tblPrestamos)
from comun import (label, header, rail, pantalla, CARD, ESC, html, boton, fondo, entrada, badge, validar)

CODIGOS = ('Distinct(Filter(Split(Substitute(Substitute(Substitute(Substitute(Substitute(txtDevol_5.Text, Char(13), Char(10)), Char(9), Char(10)), ",", Char(10)), ";", Char(10)), " ", Char(10)), Char(10)), '
           '!IsBlank(Trim(Value))), Trim(Value))')

REVISAR = '''
ClearCollect(colPrestamos, tblPrestamos);
ClearCollect(colCodDevol, ''' + CODIGOS + ''');
Clear(colDevol);
ForAll(
    Sequence(CountRows(colCodDevol)) As i,
    With(
        {cod: Index(colCodDevol, i.Value).Value},
        With(
            {p: LookUp(colPrestamos, CodigoBarra = cod && Estado = "Activo"),
             b: ParseJSON(Coalesce(IfError(Text('Copiade:BuscarLibroFOLIO'.Run(cod).datos), ""), "{}"))},
            With(
                {atraso: If(IsBlank(p) || IsBlank(p.FechaVencimiento), 0, Max(0, DateDiff(DateValue(p.FechaVencimiento), Today(), TimeUnit.Days)))},
                Collect(
                    colDevol,
                    {
                        Orden: i.Value,
                        Codigo: cod,
                        Id: If(IsBlank(p), "", p.IdPrestamo),
                        Titulo: Coalesce(If(IsBlank(p), "", p.Titulo), IfError(Text(b.titulo), ""), "—"),
                        Autor: IfError(Text(b.autor), ""),
                        Anio: IfError(Text(b.anio), ""),
                        TipoMat: Coalesce(If(IsBlank(p), "", p.TipoMaterial), IfError(Text(b.tipo), "")),
                        Ubic: IfError(Text(b.ubicacion), ""),
                        BibPrest: If(IsBlank(p), "", p.Biblioteca),
                        Correo: If(IsBlank(p), "", p.Correo),
                        Unidad: If(IsBlank(p), "", Coalesce(p.Programa, p.UnidadAcademica)),
                        Usuario: If(IsBlank(p), "—", p.Nombre & " " & p.Apellido),
                        RUT: If(IsBlank(p), "", p.RUT),
                        Prestado: If(IsBlank(p), "", p.FechaPrestamo),
                        Vence: If(IsBlank(p), "", p.FechaVencimiento),
                        ObsPrevia: If(IsBlank(p), "", p.Observaciones),
                        Atraso: atraso,
                        Estado: If(IsBlank(p), "NO ESTABA PRESTADO", atraso > 0, "ATRASADO", "A TIEMPO")
                    }
                )
            )
        )
    )
);
If(IsEmpty(colDevol), Notify("Escanee o pegue al menos un código.", NotificationType.Warning))'''

REGISTRAR = '''
Set(varDevolviendo, true);
Clear(colDevueltos);
Set(varQuienDevolvio, Concat(Distinct(Filter(colDevol, Estado = "A TIEMPO" || Estado = "ATRASADO"), Usuario), Value, ", "));
ForAll(
    Filter(colDevol, Estado = "A TIEMPO" || Estado = "ATRASADO") As x,
    IfError(
        Collect(
            colDevueltos,
            Patch(
                tblPrestamos,
                LookUp(colPrestamos, IdPrestamo = x.Id),
                {
                    FechaDevolucion: Text(Today(), "yyyy-mm-dd"),
                    Estado: "Devuelto",
                    DiasAtraso: Text(x.Atraso),
                    Observaciones: x.ObsPrevia & If(IsBlank(x.ObsPrevia), "", " | ") & "Devuelto el " & Text(Today(), "dd-mm-yyyy") & " por " & x.Usuario & " (RUT " & x.RUT & ")" & If(x.Atraso > 0, " con " & x.Atraso & " días de atraso: MOROSO", " a tiempo")
                }
            )
        );
        true,
        Notify("No se pudo registrar " & x.Codigo & ": " & FirstError.Message, NotificationType.Error)
    )
);
ClearCollect(colPrestamos, tblPrestamos);
UpdateIf(colDevol, Id in colDevueltos.IdPrestamo, {Estado: "DEVUELTO"});
Set(varDevolviendo, false);
If(
    !IsEmpty(colDevueltos),
    Set(varUltimaDevol, CountRows(colDevueltos) & " devolución(es) de " & varQuienDevolvio & " · " & Text(Now(), "hh:mm"));
    Notify("Devoluciones registradas: " & CountRows(colDevueltos), NotificationType.Success, 3000)
)'''

VACIAR = '''
Set(varDevolTexto, "");
Clear(colDevol);
Clear(colCodDevol);
Reset(txtDevol_5);
SetFocus(txtDevol_5)'''

n_listos = 'CountRows(Filter(colDevol, Estado = "A TIEMPO" || Estado = "ATRASADO"))'
n_atr = 'CountRows(Filter(colDevol, Estado = "ATRASADO"))'
n_dev = 'CountRows(Filter(colDevol, Estado = "DEVUELTO"))'
n_no = 'CountRows(Filter(colDevol, Estado = "NO ESTABA PRESTADO"))'

estado = ('If(Estado = "A TIEMPO", "' + badge('A TIEMPO') + '", Estado = "DEVUELTO", "' + badge('DEVUELTO') + '", Estado = "ATRASADO", "'
          + badge('MOROSO · " & Atraso & If(Atraso = 1, " DÍA", " DÍAS") & "', True) + '", "' + badge('NO ESTABA PRESTADO', True) + '")')
sub = "<div style='font-size:9px;color:#8A8D91'>"
fila = ('"<tr style=\'border-bottom:1px solid #DADCDF;vertical-align:top;" & If(Estado = "ATRASADO", "outline:2px solid #B3261E;outline-offset:-2px;", "") & "\'>'
        '<td style=\'padding:7px 6px;font-weight:700;text-align:left\'>" & ' + ESC.format(x='Codigo')
        + ' & "</td><td style=\'padding:7px 6px;text-align:left\'><b>" & ' + ESC.format(x='Titulo') + ' & "</b>"'
        + ' & If(IsBlank(Autor), "", "' + sub + '" & ' + ESC.format(x='Autor') + ' & If(IsBlank(Anio), "", " · " & Anio) & "</div>")'
        + ' & If(IsBlank(TipoMat) && IsBlank(Ubic), "", "' + sub + '" & ' + ESC.format(x='TipoMat') + ' & If(IsBlank(Ubic), "", " · " & ' + ESC.format(x='Ubic') + ') & "</div>")'
        + ' & "</td><td style=\'padding:7px 6px;text-align:left\'><b>" & ' + ESC.format(x='Usuario') + ' & "</b>"'
        + ' & If(IsBlank(RUT), "", "' + sub + 'RUT " & RUT & "</div>")'
        + ' & If(IsBlank(Unidad), "", "' + sub + '" & ' + ESC.format(x='Unidad') + ' & "</div>")'
        + ' & If(IsBlank(Correo), "", "<div style=\'font-size:9px;color:#8A8D91;font-style:italic\'>" & Correo & "</div>")'
        + ' & "</td><td style=\'padding:7px 6px;text-align:center\'>" & If(IsBlank(Prestado), "—", Text(DateValue(Prestado), "dd-mm-yy")) & If(IsBlank(BibPrest), "", "' + sub + '" & ' + ESC.format(x='BibPrest') + ' & "</div>")'
        + ' & "</td><td style=\'padding:7px 6px;text-align:center\'>" & If(IsBlank(Vence), "—", Text(DateValue(Vence), "dd-mm-yy")) & "</td>'
        '<td style=\'padding:7px 6px;text-align:center\'>" & ' + estado + ' & "</td></tr>"')
msg = "<div style='padding:60px 0;text-align:center;font-size:12px;color:#8A8D91'>Escanee o pegue los códigos y presione 1 · REVISAR.</div>"
PREVIA = (
    '"' + CARD % (474, "1px solid #DADCDF")
    + "<div style='display:flex;justify-content:space-between;align-items:center'><div style='font-size:15px;font-weight:700;color:#111111'>Libros devueltos</div><div>\" & "
    + 'If(' + n_listos + ' > 0, "' + badge('" & ' + n_listos + ' & " LISTOS') + '", "") & " " & '
    + 'If(' + n_atr + ' > 0, "' + badge('" & ' + n_atr + ' & " ATRASADOS', True) + '", "") & " " & '
    + 'If(' + n_dev + ' > 0, "' + badge('" & ' + n_dev + ' & " DEVUELTOS') + '", "") & "</div></div>'
    + "<div style='font-size:11px;color:#3F4247;margin:2px 0 10px'>Se cruza con los préstamos registrados. Se registra quién lo tenía, cuándo lo pidió y si lo devuelve moroso.</div>\" & "
    + 'If(IsEmpty(colDevol), "' + msg + '", '
    + '"<div style=\'max-height:380px;overflow-y:auto\'><table style=\'width:100%;border-collapse:collapse;table-layout:fixed;font-size:11px;color:#111111\'>'
    + "<colgroup><col style='width:84px'><col><col style='width:170px'><col style='width:78px'><col style='width:62px'><col style='width:104px'></colgroup>"
    + "<tr style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;border-bottom:1px solid #111111'>"
    + "<th style='padding:6px;text-align:left'>CÓDIGO</th><th style='padding:6px;text-align:left'>LIBRO</th><th style='padding:6px;text-align:left'>QUIÉN LO DEVUELVE</th><th style='padding:6px;text-align:center'>PRESTADO</th><th style='padding:6px;text-align:center'>VENCÍA</th><th style='padding:6px;text-align:center'>ESTADO</th></tr>\" & "
    + 'Concat(Sort(colDevol, Orden), ' + fila + ') & "</table></div>") & "</div></div>"')

ctrls = [
    header('5', 'Devolución'),
    label('lblAviso_5', '="DEVOLUCIÓN FICTICIA · SE REGISTRA EN EXCEL, NO EN FOLIO"', 104, 128, 480, h=16, size=7),
    label('lblPaso_5', '="Libros devueltos"', 104, 158, 300, h=22, size=11, color='#111111'),
    label('lblCap_5', '="UNO O MUCHOS · ESCANEE O PEGUE UN CÓDIGO POR LÍNEA"', 104, 184, 476),
    entrada('txtDevol_5', 104, 200, 476, 'Escanee o pegue los códigos…', 'false', h=250, multilinea=True),
    fondo('htmlRevisarFondo_5', 'btnRevisar_5', 104, 466, 476, 48),
    boton('btnRevisar_5', 104, 466, 476, 48, '"1 · REVISAR   →"', REVISAR,
          displaymode='If(varDevolviendo, DisplayMode.Disabled, DisplayMode.Edit)', size=12),
    label('lblResumen_5', '=If(IsEmpty(colDevol), "", CountRows(colDevol) & " revisados · " & ' + n_listos + ' & " listos · " & ' + n_atr + ' & " atrasados · " & ' + n_no + ' & " no estaban prestados")',
          104, 522, 476, h=16, size=8, color='#3F4247', bold=False),
    html('htmlPrevia_5', 634, 144, 698, 486, PREVIA),
    fondo('htmlRegistrarFondo_5', 'btnRegistrar_5', 640, 640, 516, 56),
    boton('btnRegistrar_5', 640, 640, 516, 56,
          'If(varDevolviendo, "REGISTRANDO…", "2 · REGISTRAR " & ' + n_listos + ' & " DEVOLUCIONES   →")', REGISTRAR,
          displaymode='If(' + n_listos + ' > 0 && !varDevolviendo, DisplayMode.Edit, DisplayMode.Disabled)'),
    boton('btnVaciar_5', 1170, 640, 156, 56, '"Vaciar"', VACIAR, dark=False, size=11),
    label('lblUltimo_5', '=If(IsBlank(varUltimaDevol), "Aún no se registra ninguna devolución en esta sesión.", "Última: " & varUltimaDevol)',
          640, 706, 686, h=18, size=9, color='#3F4247', bold=False),
    rail('5', 'Devolución'),
]
ONV = 'ClearCollect(colPrestamos, tblPrestamos); Set(varMenu, false); SetFocus(txtDevol_5)'
OUT = '/home/user/Power-Apps/pantallas/5_Devolucion.txt'
open(OUT, 'w').write(pantalla('scrDevolucion', ONV, ctrls))
validar(OUT, 'scrDevolucion')

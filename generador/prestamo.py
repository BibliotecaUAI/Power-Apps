
# Genera pantallas/4_Prestamo.txt (préstamo ficticio en Excel)
from comun import (label, header, rail, pantalla, CARD, NORM, ESC, BIBLIOTECAS, html, boton, fondo, oculto,
                   entrada, lista, texto, badge, borde_destellante, validar)

Q = '"'
VENCIDOS_U = 'CountRows(Filter(colPrestamos, RUT = varUsuario.RUT && Estado = "Activo" && !IsBlank(FechaVencimiento) && DateValue(FechaVencimiento) < Today()))'
ACTIVOS_U = 'CountRows(Filter(colPrestamos, RUT = varUsuario.RUT && Estado = "Activo"))'
RUN = 'If("RUN=" in t, First(Split(Last(Split(t, "RUN=")).Value, "&")).Value, t)'

BUSCAR_USUARIO = '''
With(
    {t: Coalesce(varEntradaUsuario, "")},
    With(
        {r: ''' + NORM.format(x=RUN) + '''},
        If(
            !IsBlank(r),
            Set(varBuscandoUsuario, true);
            Set(varResUsuario, IfError(Text(BuscarUsuarioFOLIO.Run(r).datos), Notify("Error del flujo BuscarUsuarioFOLIO: " & FirstError.Message, NotificationType.Error); Blank()));
            Set(varBuscandoUsuario, false);
            With(
                {j: ParseJSON(If(IsBlank(varResUsuario), "{}", varResUsuario)), u: LookUp(colUsuarios, ''' + NORM.format(x='RUT') + ''' = r)},
                Set(
                    varUsuario,
                    If(
                        Text(j.encontrado) = "SI",
                            {
                                RUT: With({x: If(IsBlank(Text(j.rut)), r, Text(j.rut))}, Left(x, Len(x) - 1) & "-" & Right(x, 1)),
                                Nombre: Text(j.nombre),
                                Apellido: Text(j.apellido),
                                NombreSugerido: Coalesce(Text(j.nombreSugerido), Text(j.nombre)),
                                TipoUsuario: Text(j.tipoUsuario),
                                UnidadAcademica: Text(j.unidadAcademica),
                                Programa: Text(j.programa),
                                Correo: Text(j.correo),
                                MorososFolio: Coalesce(Value(Text(j.morososFolio)), 0),
                                Origen: "FOLIO"
                            },
                        !IsBlank(u),
                            {
                                RUT: u.RUT,
                                Nombre: u.Nombre,
                                Apellido: u.Apellido,
                                NombreSugerido: u.NombreSugerido,
                                TipoUsuario: u.TipoUsuario,
                                UnidadAcademica: u.UnidadAcademica,
                                Programa: u.Programa,
                                Correo: u.Correo,
                                MorososFolio: 0,
                                Origen: "EXCEL"
                            }
                    )
                )
            );
            If(
                IsBlank(varUsuario),
                    Set(varMoroso, false);
                    Notify("El RUT " & r & " no se encontró en FOLIO ni en la hoja Usuarios.", NotificationType.Warning);
                    Reset(txtUsuario_4);
                    SetFocus(txtUsuario_4),
                Set(varMoroso, ''' + VENCIDOS_U + ''' + varUsuario.MorososFolio > 0);
                If(varMoroso, Notify(varUsuario.Nombre & " tiene préstamos vencidos.", NotificationType.Warning));
                SetFocus(txtLibro_4)
            )
        )
    )
);
Set(varEntradaUsuario, Blank())'''

AGREGAR_LIBRO = '''
With(
    {cod: Coalesce(varEntradaLibro, ""), n: CountRows(colCarrito) + 1},
    If(
        IsBlank(cod),
            false,
        cod in colCarrito.Codigo,
            Notify("Ese libro ya está en la lista.", NotificationType.Warning),
        Set(varBuscandoLibro, true);
        Set(varResLibro, IfError(Text('Copiade:BuscarLibroFOLIO'.Run(cod).datos), Notify("Error del flujo de libros: " & FirstError.Message, NotificationType.Error); Blank()));
        Set(varBuscandoLibro, false);
        With(
            {j: ParseJSON(If(IsBlank(varResLibro), "{}", varResLibro))},
            With(
                {enc: Text(j.encontrado) = "SI", tipo: Text(j.tipo), ubic: Text(j.ubicacion)},
                With(
                    {pl: If(IsBlank(LookUp(colPlazos, TipoMaterial = tipo)), LookUp(colPlazos, TipoMaterial = "(cualquier otro tipo)"), LookUp(colPlazos, TipoMaterial = tipo))},
                    With(
                        {sala: Text(pl.SoloSala) = "SI" || "histór" in Lower(ubic) || "histor" in Lower(ubic), dias: Coalesce(Value(pl.Dias), 28)},
                        Collect(
                            colCarrito,
                            {
                                Orden: n,
                                Codigo: cod,
                                Titulo: If(enc, Text(j.titulo), "—"),
                                Tipo: If(enc, tipo, "—"),
                                Dias: If(sala, 0, dias),
                                Vence: If(sala || !enc, "", Text(DateAdd(Today(), dias, TimeUnit.Days), "yyyy-mm-dd")),
                                Estado: If(!enc, "NO EN FOLIO", sala, "SOLO SALA", cod in Filter(colPrestamos, Estado = "Activo").CodigoBarra, "YA PRESTADO", "LISTO")
                            }
                        )
                    )
                )
            )
        )
    )
);
Set(varEntradaLibro, Blank());
Reset(txtLibro_4);
SetFocus(txtLibro_4)'''

CORREO_HTML = (
    '"<div style=\'font-family:Segoe UI,Arial,sans-serif;color:#111111\'>'
    '<div style=\'background:#111111;color:#FFFFFF;padding:18px 22px\'><div style=\'font-size:10px;letter-spacing:3px;color:#BFC3C8\'>BIBLIOTECAS UAI</div>'
    '<div style=\'font-size:20px;font-weight:700\'>Resumen de tu préstamo</div></div>'
    '<div style=\'padding:18px 22px\'><p>Hola " & Coalesce(varUsuario.NombreSugerido, varUsuario.Nombre) & ", registramos este préstamo a tu nombre (prueba):</p>'
    '<table style=\'border-collapse:collapse;font-size:13px\'><tr style=\'border-bottom:1px solid #111111;text-align:left\'>'
    '<th style=\'padding:6px 10px\'>Título</th><th style=\'padding:6px 10px\'>Código</th><th style=\'padding:6px 10px\'>Devolver antes del</th></tr>" & '
    'Concat(colRegistrados, "<tr style=\'border-bottom:1px solid #DADCDF\'><td style=\'padding:6px 10px\'>" & Titulo & "</td>'
    '<td style=\'padding:6px 10px\'>" & CodigoBarra & "</td><td style=\'padding:6px 10px\'><b>" & Text(DateValue(FechaVencimiento), "dd-mm-yyyy") & "</b></td></tr>") & '
    '"</table><p style=\'color:#3F4247;font-size:12px\'>" & drpBiblioteca_4.Selected.Value & " · " & Text(Now(), "dd-mm-yyyy hh:mm") & "</p></div></div>"')

REGISTRAR = '''
Set(varRegistrando, true);
Clear(colRegistrados);
With(
    {L: Filter(colCarrito, Estado = "LISTO"), base: Text(Now(), "yyyymmddhhmmss")},
    ForAll(
        L As x,
        IfError(
            Collect(
                colRegistrados,
                Patch(
                    tblPrestamos,
                    Defaults(tblPrestamos),
                    {
                        IdPrestamo: "P" & base & "-" & x.Orden,
                        RUT: varUsuario.RUT,
                        Nombre: varUsuario.Nombre,
                        Apellido: varUsuario.Apellido,
                        NombreSugerido: varUsuario.NombreSugerido,
                        UnidadAcademica: varUsuario.UnidadAcademica,
                        Programa: varUsuario.Programa,
                        Correo: varUsuario.Correo,
                        CodigoBarra: x.Codigo,
                        Titulo: x.Titulo,
                        TipoMaterial: x.Tipo,
                        Biblioteca: drpBiblioteca_4.Selected.Value,
                        FechaPrestamo: Text(Today(), "yyyy-mm-dd"),
                        FechaVencimiento: x.Vence,
                        FechaDevolucion: "",
                        Estado: "Activo",
                        DiasAtraso: "0",
                        CorreoEnviado: If(drpCorreo_4.Selected.Value = "Enviar resumen", "SI", "NO"),
                        RegistradoPor: User().Email,
                        Observaciones: txtObs_4.Text
                    }
                )
            );
            true,
            Notify("No se pudo registrar " & x.Codigo & ": " & FirstError.Message, NotificationType.Error)
        )
    )
);
If(
    drpCorreo_4.Selected.Value = "Enviar resumen" && !IsEmpty(colRegistrados),
    IfError(
        Office365Outlook.SendEmailV2(
            Coalesce(varCorreoPrueba, varUsuario.Correo),
            "Resumen de tu préstamo · Bibliotecas UAI",
            ''' + CORREO_HTML + '''
        );
        true,
        Notify("Préstamo guardado, pero no se pudo enviar el correo.", NotificationType.Warning)
    )
);
ClearCollect(colPrestamos, tblPrestamos);
If(
    !IsEmpty(colRegistrados),
    Set(varUltimoPrestamo, CountRows(colRegistrados) & " libro(s) a " & varUsuario.Nombre & " " & varUsuario.Apellido & " · " & Text(Now(), "hh:mm"));
    Notify("Préstamo registrado: " & CountRows(colRegistrados) & " libro(s).", NotificationType.Success, 3000);
    Clear(colCarrito);
    Set(varUsuario, Blank());
    Set(varMoroso, false);
    Reset(txtUsuario_4);
    Reset(txtLibro_4);
    Reset(txtObs_4);
    SetFocus(txtUsuario_4)
);
Set(varRegistrando, false)'''

CANCELAR = '''
Clear(colCarrito);
Set(varUsuario, Blank());
Set(varMoroso, false);
Reset(txtUsuario_4);
Reset(txtLibro_4);
Reset(txtObs_4);
SetFocus(txtUsuario_4)'''

# Tarjeta del usuario
vacia = (CARD % (150, "1px solid #DADCDF")
         + "<div style='font-size:9px;letter-spacing:1.5px;color:#8A8D91;font-weight:700'>○  ESPERANDO USUARIO</div>"
         + "<div style='font-size:18px;font-weight:700;color:#8A8D91;margin-top:14px'>Escanee el QR de la cédula o digite el RUT.</div></div></div>")
DARKG = "background:linear-gradient(115deg,#0B0B0C 0%,#111111 38%,#35373B 50%,#111111 62%,#0B0B0C 100%)"
FNT = "font-family:Calibri,Carlito,Segoe UI,sans-serif"
chip = lambda expr: ("<span style='display:inline-block;padding:3px 10px;margin-right:6px;border-radius:999px;background:rgba(255,255,255,0.08);"
                     "border:1px solid rgba(191,195,200,0.35);font-size:11px;color:#E6E7E9'>\" & " + expr + " & \"</span>")
stat = lambda expr, lab, rojo: ("<div style='width:86px;height:60px;border-radius:12px;background:rgba(255,255,255,0.06);border:1px solid rgba(191,195,200,0.25);"
                                "display:flex;flex-direction:column;align-items:center;justify-content:center'><div style='font-size:20px;font-weight:700;color:\" & "
                                + rojo + " & \"'>\" & " + expr + " & \"</div><div style='font-size:10px;font-style:italic;color:#BFC3C8'>" + lab + "</div></div>")
VENC_TOTAL = '(' + VENCIDOS_U + ' + varUsuario.MorososFolio)'
llena = ("<div style='position:relative;margin:6px;height:150px;box-sizing:border-box;border-radius:18px;overflow:hidden;" + FNT + ";" + DARKG + ";"
         "border:\" & If(varMoroso, \"1.5px solid #B3261E;box-shadow:0 0 0 4px rgba(179,38,30,0.16),0 0 22px rgba(179,38,30,0.35)\", \"1px solid #3F4247;box-shadow:0 14px 30px rgba(17,17,17,0.25)\") & \"'>"
         "<div style='position:absolute;right:0;top:0;bottom:0;width:10px;background:repeating-linear-gradient(180deg,rgba(191,195,200,0.5) 0 2px,transparent 2px 5px,rgba(191,195,200,0.3) 5px 6px,transparent 6px 9px)'></div>"
         "<div style='position:absolute;left:22px;top:26px;width:96px;height:96px;border-radius:50%;background:linear-gradient(135deg,#8A8D91,#FFFFFF 45%,#BFC3C8);padding:3px;box-sizing:border-box'>"
         "<div style='width:100%;height:100%;border-radius:50%;background:linear-gradient(135deg,#35373B,#111111);display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;color:#FFFFFF'>"
         "\" & Upper(Left(varUsuario.Nombre, 1) & Left(varUsuario.Apellido, 1)) & \"</div></div>"
         "<div style='position:absolute;left:138px;top:22px;right:330px'><div style='font-size:10px;letter-spacing:2px;font-weight:700;color:#BFC3C8'>CARNÉ DE BIBLIOTECA · \" & varUsuario.Origen & \"</div>"
         "<div style='font-size:20px;font-weight:700;color:#FFFFFF;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>\" & varUsuario.Nombre & \" \" & varUsuario.Apellido & \"</div>"
         "<div style='font-size:12px;font-style:italic;color:#BFC3C8;margin-bottom:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>\" & varUsuario.UnidadAcademica & If(IsBlank(varUsuario.Programa), \"\", \" · \" & varUsuario.Programa) & \"</div>"
         + chip('"RUT " & varUsuario.RUT') + chip('Coalesce(varUsuario.TipoUsuario, "Usuario")') + "</div>"
         "<div style='position:absolute;right:28px;top:38px;display:flex;gap:10px;align-items:center'>"
         + stat(ACTIVOS_U, 'activos', '"#FFFFFF"') + stat(VENC_TOTAL, 'vencidos', 'If(' + VENC_TOTAL + ' > 0, "#FF6B5E", "#FFFFFF")')
         + "<div style='width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;text-align:center;font-size:11px;font-weight:700;letter-spacing:1.5px;"
         "\" & If(varMoroso, \"border:2px solid #B3261E;box-shadow:0 0 14px rgba(179,38,30,0.6),inset 0 0 10px rgba(179,38,30,0.35);color:#FF8A80\", \"border:2px solid #BFC3C8;box-shadow:inset 0 0 10px rgba(255,255,255,0.15);color:#FFFFFF\") & \"'>"
         "\" & If(varMoroso, \"MOROSO\", \"AL DÍA\") & \"</div></div></div>")
USUARIO_CARD = 'If(\n    IsBlank(varUsuario),\n    "' + vacia + '",\n    "' + llena + '"\n)'

# Tarjeta de libros
listos = 'CountRows(Filter(colCarrito, Estado = "LISTO"))'
nolistos = 'CountRows(Filter(colCarrito, Estado <> "LISTO"))'
plazo = 'If(Estado = "LISTO", "' + badge('" & Dias & If(Dias = 1, " DÍA", " DÍAS") & "') + '", "' + badge('" & Estado & "', True) + '")'
fila = ('"<tr style=\'border-bottom:1px solid #DADCDF\'><td style=\'padding:7px 6px;font-weight:700\'>" & ' + ESC.format(x='Codigo')
        + ' & "</td><td style=\'padding:7px 6px\'>" & ' + ESC.format(x='Titulo')
        + ' & "</td><td style=\'padding:7px 6px\'>" & ' + ESC.format(x='Tipo')
        + ' & "</td><td style=\'padding:7px 6px\'>" & ' + plazo
        + ' & "</td><td style=\'padding:7px 6px\'>" & If(IsBlank(Vence), "—", Text(DateValue(Vence), "dd-mm-yyyy")) & "</td></tr>"')
msg = "<div style='padding:40px 0;text-align:center;font-size:12px;color:#8A8D91'>%s</div>"
LIBROS_CARD = (
    '"' + CARD % (308, "1px solid #DADCDF")
    + "<div style='display:flex;justify-content:space-between;align-items:center'><div style='font-size:15px;font-weight:700;color:#111111'>Libros a prestar</div>"
    + "<div style='margin-right:130px'>\" & "
    + 'If(' + listos + ' > 0, "' + badge('" & ' + listos + ' & " LISTOS') + '", "") & " " & '
    + 'If(' + nolistos + ' > 0, "' + badge('" & ' + nolistos + ' & " NO SE PRESTAN', True) + '", "") & "</div></div>" & '
    + 'If(IsEmpty(colCarrito), If(varBuscandoLibro, "' + msg % 'Buscando en FOLIO…' + '", "' + msg % 'Escanee los libros uno tras otro. Se suman aquí con su plazo.' + '"), '
    + '"<div style=\'margin-top:10px;max-height:230px;overflow-y:auto\'><table style=\'width:100%;border-collapse:collapse;font-size:11px;color:#111111\'>'
    + "<tr style='font-size:8px;letter-spacing:1.5px;color:#8A8D91;border-bottom:1px solid #111111;text-align:left'>"
    + "<th style='padding:6px'>CÓDIGO</th><th style='padding:6px'>TÍTULO</th><th style='padding:6px'>TIPO</th><th style='padding:6px'>PLAZO</th><th style='padding:6px'>VENCE</th></tr>\" & "
    + 'Concat(Sort(colCarrito, Orden), ' + fila + ') & "</table></div>") & "</div></div>"')

ctrls = [
    header('4', 'Préstamo'),
    label('lblAviso_4', '="PRÉSTAMO FICTICIO · SE REGISTRA EN EXCEL, NO EN FOLIO"', 104, 128, 480, h=16, size=7),
    label('lblPaso1_4', '="1 · Usuario"', 104, 158, 300, h=22, size=11, color='#111111'),
    label('lblCap1_4', '="ESCANEE EL QR DE LA CÉDULA O DIGITE EL RUT + ENTER"', 104, 184, 476),
    entrada('txtUsuario_4', 104, 200, 476, 'RUT o QR de la cédula…',
            'If(!IsBlank(Trim(Self.Text)), Set(varEntradaUsuario, Trim(Self.Text)); Select(btnBuscarUsuario_4))'),
    label('lblPaso2_4', '="2 · Libros"', 104, 272, 300, h=22, size=11, color='#111111'),
    label('lblCap2_4', '="ESCANEE UNO TRAS OTRO · SE SUMAN A LA LISTA"', 104, 298, 476),
    entrada('txtLibro_4', 104, 314, 476, 'Código de barras del libro…',
            'If(!IsBlank(Trim(Self.Text)), Set(varEntradaLibro, Trim(Self.Text)); Select(btnAgregarLibro_4))'),
    label('lblPaso3_4', '="3 · Condiciones"', 104, 386, 300, h=22, size=11, color='#111111'),
    label('lblCapBib_4', '="BIBLIOTECA"', 104, 412, 230),
    lista('drpBiblioteca_4', 104, 426, 230, BIBLIOTECAS, '"Biblioteca Viña"'),
    label('lblCapCorreo_4', '="CORREO AL USUARIO"', 350, 412, 230),
    lista('drpCorreo_4', 350, 426, 230, '["Enviar resumen", "No enviar"]', '"Enviar resumen"'),
    label('lblCapObs_4', '="OBSERVACIONES"', 104, 466, 476),
    texto('txtObs_4', 104, 480, 476),
    label('lblPlazos_4', '="Plazos según la hoja Plazos del Excel: libro 28 días · iPad 14 · Kindle 28 · calculadora, test y mapa 1 día · colección histórica solo sala."',
          104, 522, 476, h=32, size=8, color='#8A8D91', bold=False),
    html('htmlUsuario_4', 634, 144, 698, 162, USUARIO_CARD),
    html('htmlMoroso_4', 634, 144, 698, 162, '"' + borde_destellante(698, 162) + '"', visible='varMoroso && !IsBlank(varUsuario)'),
    html('htmlLibros_4', 634, 310, 698, 320, LIBROS_CARD),
    boton('btnQuitar_4', 1190, 330, 120, 26, '"Quitar último"', 'Remove(colCarrito, Last(Sort(colCarrito, Orden)))',
          displaymode='If(IsEmpty(colCarrito), DisplayMode.Disabled, DisplayMode.Edit)', dark=False, size=8),
    fondo('htmlRegistrarFondo_4', 'btnRegistrar_4', 640, 640, 516, 56),
    boton('btnRegistrar_4', 640, 640, 516, 56,
          'If(varRegistrando, "REGISTRANDO…", "REGISTRAR PRÉSTAMO (" & ' + listos + ' & ")   →")', REGISTRAR,
          displaymode='If(!IsBlank(varUsuario) && ' + listos + ' > 0 && !varRegistrando && !varBuscandoLibro, DisplayMode.Edit, DisplayMode.Disabled)'),
    boton('btnCancelar_4', 1170, 640, 156, 56, '"Cancelar"', CANCELAR, dark=False, size=11),
    label('lblUltimo_4', '=If(IsBlank(varUltimoPrestamo), "Aún no se registra ningún préstamo en esta sesión.", "Último: " & varUltimoPrestamo)',
          640, 706, 686, h=18, size=9, color='#3F4247', bold=False),
    oculto('btnBuscarUsuario_4', BUSCAR_USUARIO),
    oculto('btnAgregarLibro_4', AGREGAR_LIBRO),
    rail('4', 'Préstamo'),
]
ONV = ('ClearCollect(colPrestamos, tblPrestamos); ClearCollect(colUsuarios, tblUsuarios); ClearCollect(colPlazos, tblPlazos); '
       'Set(varCorreoPrueba, "pablo.salas.marin@uai.cl"); Set(varMenu, false); SetFocus(txtUsuario_4)')
OUT = '/home/user/Power-Apps/pantallas/4_Prestamo.txt'
open(OUT, 'w').write(pantalla('scrPrestamo', ONV, ctrls))
validar(OUT, 'scrPrestamo')

# Genera camara/*.txt: un botón de cámara (lector de código de barras) por buscador, para pegar en cada pantalla
R = '/home/user/Power-Apps/camara/'
V = 'Trim(First(Self.Barcodes).Value)'
def cam(n, x, y, onscan, w=48, h=44, dm=None):
    extra = f'      DisplayMode: ={dm}\n' if dm else ''
    return f'''- {n}:
    Control: BarcodeReader@0.0.30
    Properties:
      Color: =ColorValue("#FFFFFF")
{extra}      Fill: =ColorValue("#111111")
      Height: ={h}
      OnScan: |-
        =If(!IsBlank(First(Self.Barcodes).Value), {onscan})
      Text: ="📷"
      Width: ={w}
      X: ={x}
      Y: ={y}
'''
LINEA = lambda box, var: f'Set({var}, {box}.Text & If(IsBlank({box}.Text) || EndsWith({box}.Text, Char(10)), "", Char(10)) & {V} & Char(10)); Reset({box})'
RUN = f'With({{t: {V}}}, If("RUN=" in t, First(Split(Last(Split(t, "RUN=")).Value, "&")).Value, t))'
ARCH = {
 '1_Camara_Descarte.txt': [cam('barCamara_1', 388, 366, f'Set(varEntrada, {V}); Select(btnProcesarEscaneo)', dm='If(varBuscando, DisplayMode.Disabled, DisplayMode.Edit)')],
 '2_Camara_Descarte_masiva.txt': [cam('barCamara_2', 528, 352, LINEA('txtTanda_2', 'varTandaTexto'), dm='If(varBuscandoTanda || varGuardandoTanda, DisplayMode.Disabled, DisplayMode.Edit)')],
 '3_Camara_Prestamo.txt': [cam('barCamaraUsuario_4', 528, 204, f'Set(varEntradaUsuario, {V}); Select(btnBuscarUsuario_4)'),
                           cam('barCamaraLibro_4', 528, 318, f'Set(varEntradaLibro, {V}); Select(btnAgregarLibro_4)')],
 '4_Camara_Devolucion.txt': [cam('barCamara_5', 528, 204, LINEA('txtDevol_5', 'varDevolTexto'))],
 '5_Camara_Morosos.txt': [cam('barCamara_6', 398, 144, f'Set(varBuscarMor, {RUN}); Reset(txtBuscarMor_6); Select(btnFiltrar_6)', w=34, h=26)],
 '6_Camara_Inventario.txt': [cam('barCamara_7', 528, 290, f'Set(varEntradaInv, {V}); Select(btnEscanearInv_7)', dm='If(varBuscandoInv, DisplayMode.Disabled, DisplayMode.Edit)')],
}
import os, glob
for f in glob.glob(R + '*.txt'): os.remove(f)
for a, cs in ARCH.items():
    open(R + a, 'w').write(''.join(cs))

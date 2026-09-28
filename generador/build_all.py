import subprocess, os, sys
sys.path.insert(0, '.')
subprocess.run(['python3', 'build.py'], check=True)
from nav import rail, inicio, en_construccion
R = '/home/user/Power-Apps'
os.makedirs(R + '/pantallas', exist_ok=True)
def descarte(src, dst, sfx, onv_old):
    t = open(src).read()
    assert "padding:0 40px;background" in t
    t = t.replace("padding:0 40px;background", "padding:0 40px 0 104px;background")
    t = t.replace(onv_old, onv_old + '; Set(varMenu, false)')
    t = t.rstrip('\n') + '\n' + rail(sfx, 'Descarte') + '\n'
    open(dst, 'w').write(t); os.remove(src)
descarte(R + '/descarte/Pantalla_1_Lectura_1a1.txt', R + '/pantallas/2_Descarte_1a1.txt', '1',
         'OnVisible: =ClearCollect(colFicha, tblFichaDescarte); Set(varEntrada, Blank()); SetFocus(txtEscaneo_1)')
descarte(R + '/descarte/Pantalla_2_Lectura_Masiva.txt', R + '/pantallas/3_Descarte_Masiva.txt', '2',
         'OnVisible: =ClearCollect(colFicha, tblFichaDescarte); SetFocus(txtTanda_2)')
open(R + '/pantallas/1_Inicio.txt', 'w').write(inicio())

subprocess.run(['python3', 'prestamo.py'], check=True)
subprocess.run(['python3', 'devolucion.py'], check=True)
subprocess.run(['python3', 'inventario.py'], check=True)

subprocess.run(['python3', 'morosos.py'], check=True)

# Nombres finales de las pantallas
import glob, re
NOMBRES = {'scrInicio': 'Inicio', 'scrDescarteB': 'Descarte', 'scrDescarteMasiva': 'Descarte masiva',
           'scrPrestamo': 'Préstamo', 'scrDevolucion': 'Devolución', 'scrPanel': 'Morosos', 'scrInventario': 'Inventario'}
ARCH = {'1_Inicio.txt': '1_Inicio.txt', '2_Descarte_1a1.txt': '2_Descarte.txt', '3_Descarte_Masiva.txt': '3_Descarte_masiva.txt',
        '4_Prestamo.txt': '4_Prestamo.txt', '5_Devolucion.txt': '5_Devolucion.txt', '6_Panel.txt': '6_Morosos.txt', '7_Inventario.txt': '7_Inventario.txt'}
for viejo, nuevo in ARCH.items():
    p = R + '/pantallas/' + viejo
    t = open(p).read()
    for a, z in NOMBRES.items():
        t = t.replace('Navigate(' + a + ',', "Navigate('" + z + "',")
        t = re.sub(r'^  ' + a + ':$', '  ' + ("'" + z + "'" if ' ' in z else z) + ':', t, flags=re.M)
    os.remove(p)
    open(R + '/pantallas/' + nuevo, 'w').write(t)

# Diseño v2 (tema claro/oscuro, vidrio, marcadores)
import tema
for arch, sfx in [('1_Inicio.txt', '0'), ('2_Descarte.txt', '1'), ('3_Descarte_masiva.txt', '2'), ('4_Prestamo.txt', '4'),
                  ('5_Devolucion.txt', '5'), ('6_Morosos.txt', '6'), ('7_Inventario.txt', '7')]:
    tema.aplicar(R + '/pantallas/' + arch, sfx)

# Descarte 1 a 1: enviar todos los ejemplares del título (misma biblioteca) a Lectura masiva
from comun import boton as _boton
TODOS = 'Filter(Split(IfError(Text(ParseJSON(varRes).todos), ""), ","), !IsBlank(Trim(Value)) && !(Trim(Value) in colFicha.\'Codigo de Barra\'))'
_b = _boton('btnTodos_1', 640, 728, 686, 32,
            '"＋  AGREGAR LOS " & CountRows(' + TODOS + ') & " EJEMPLARES DE ESTE TÍTULO (MISMA BIBLIOTECA) A LECTURA MASIVA   →"',
            'Set(varTandaTexto, Concat(' + TODOS + ', Trim(Value) & Char(10))); Navigate(\'Descarte masiva\', ScreenTransition.Fade)',
            dark=False, size=9)
_b = _b.replace('          Properties:\n', '          Properties:\n            Visible: =!IsBlank(varRes) && CountRows(' + TODOS + ') > 1\n', 1)
_p = R + '/pantallas/2_Descarte.txt'
_t = open(_p).read()
_i = _t.index('      - btnProcesarEscaneo:')
open(_p, 'w').write(_t[:_i] + _b.rstrip('\n') + '\n' + _t[_i:])

# Buscadores que la cámara rellena (Default = variable)
def set_default(arch, ctrl, expr):
    p = R + '/pantallas/' + arch
    t = open(p).read()
    i = t.index('- ' + ctrl + ':')
    j = t.index('Default: =""', i)
    assert j - i < 600, ctrl
    open(p, 'w').write(t[:j] + 'Default: =' + expr + t[j + len('Default: =""'):])
set_default('5_Devolucion.txt', 'txtDevol_5', 'varDevolTexto')
set_default('6_Morosos.txt', 'txtBuscarMor_6', 'varBuscarMor')

# Cámara (lector de código de barras) dentro de cada buscador, justo después del cuadro de texto
import importlib.util
spec = importlib.util.spec_from_file_location('camara', 'camara.py'); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
DONDE = {'1_Camara_Descarte.txt': ('2_Descarte.txt', ['txtEscaneo_1']), '2_Camara_Descarte_masiva.txt': ('3_Descarte_masiva.txt', ['txtTanda_2']),
         '3_Camara_Prestamo.txt': ('4_Prestamo.txt', ['txtUsuario_4', 'txtLibro_4']), '4_Camara_Devolucion.txt': ('5_Devolucion.txt', ['txtDevol_5']),
         '5_Camara_Morosos.txt': ('6_Morosos.txt', ['txtBuscarMor_6']), '6_Camara_Inventario.txt': ('7_Inventario.txt', ['txtInv_7'])}
for a, (arch, cajas) in DONDE.items():
    p = R + '/pantallas/' + arch
    t = open(p).read()
    for caja, ctrl in zip(cajas, cm.ARCH[a]):
        bloque = ''.join('      ' + l + '\n' for l in ctrl.rstrip('\n').split('\n'))
        i = t.index('      - ' + caja + ':')
        j = t.find('\n      - ', i + 1)
        j = len(t) if j < 0 else j + 1
        t = t[:j] + bloque + t[j:]
    open(p, 'w').write(t)

# Un solo archivo con toda la app (pegar de una vez)
out = ['Screens:']
for f in ['1_Inicio.txt', '2_Descarte.txt', '3_Descarte_masiva.txt', '4_Prestamo.txt', '5_Devolucion.txt', '6_Morosos.txt', '7_Inventario.txt']:
    out += open(R + '/pantallas/' + f).read().rstrip('\n').split('\n')[1:]
open(R + '/pantallas/0_APP_COMPLETA.txt', 'w').write('\n'.join(out) + '\n')

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


# ---------- Ficha de Descarte PP 2026: nombres de columnas, formatos y valores automáticos ----------
def ficha2026(path):
    t = open(path).read()
    R = [
        ("'Pregrado  A - Existencia'", "'Pregrado A - Existencia'"),
        ("'Pregrado  F - Existencia'", "'Pregrado F - Existencia'"),
        ("'Año de edición'", "'Año de edicion'"),
        ('["Biblioteca Viña", "Biblioteca Posgrado", "Biblioteca Pregrado A", "Biblioteca Pregrado F"]',
         '["(automático)", "Biblioteca Viña del Mar", "Biblioteca Postgrado", "Biblioteca Pregrado Edif. A", "Biblioteca Pregrado Edif. F"]'),
        ('["Inventario 2017", "Inventario 2021", "Inventario 2023", "Inventario 2024", "Sin Inventariar"]',
         '["NO", "Inventario 2017", "Inventario 2021", "Inventario 2023", "Inventario 2024", "Sin Inventariar"]'),
        ('["Contenido", "Contexto", "Estado de Conservación", "Limpieza y depuración"]',
         '["(automático)", "Contenido", "Contexto", "Estado de Conservación", "Limpieza y depuración"]'),
        ('Justificacion: "Duplicidad"}', 'Justificacion: "Duplicidad (redundancia)"}'),
    ]
    for a, b in R:
        t = t.replace(a, b)
    import re as _re
    t = _re.sub(r'\n( +)(\{Criterio: "Contenido", Justificacion: "Disponibilidad de ediciones anteriores"\},)',
                lambda m: '\n' + m.group(1) + '{Criterio: "(automático)", Justificacion: "(automático)"},\n' + m.group(1) + m.group(2), t)
    open(path, 'w').write(t)

def ficha2026_1a1(path):
    t = open(path).read()
    R = [
        # varItem: biblioteca y criterio automático desde FOLIO
        ("'Año de edicion': Text(j.anio)\n", "'Año de edicion': Text(j.anio),\n                                      Bib: IfError(Text(j.bib), \"\"),\n                                      Crit: IfError(Text(j.crit), \"\")\n"),
        # si el código ya está en la ficha pero sin datos, se completa esa fila
        ("                              tblFichaDescarte,\n                              Defaults(tblFichaDescarte),",
         "                              tblFichaDescarte,\n                              If(IsBlank(LookUp(colFicha, Text('Codigo de Barra') = varCodigo)), Defaults(tblFichaDescarte), LookUp(colFicha, Text('Codigo de Barra') = varCodigo)),"),
        ("                                  Número: Text(Coalesce(Max(colFicha, Value(Número)), 0) + 1),\n", ""),
        ("HRID: hrid,", "HRID: IfError(Text(Value(hrid)), hrid),"),
        ("'Item ingresado en la base de biblioteca': If(enc, \"SI\", \"NO\"),", "'Item ingresado en la base de biblioteca': Right(Substitute(If(enc, varItem.'Fecha registro (ingresado en la base)', txtFechaReg_1.Text), \"-\", \"/\"), 4),"),
        ("copia: If(enc, varItem.copia, txtCopia_1.Text),", "Copia: If(enc, varItem.copia, txtCopia_1.Text),"),
        ("'Biblioteca-Ubicacion-Colección': If(enc, varItem.'Biblioteca-Ubicacion-Colección', txtUbicacion_1.Text),",
         "'Biblioteca-Ubicacion-Colección': Substitute(If(enc, varItem.'Biblioteca-Ubicacion-Colección', txtUbicacion_1.Text), \" - \", \" \"),"),
        ("'Fecha registro (ingresado en la base)': If(enc, varItem.'Fecha registro (ingresado en la base)', txtFechaReg_1.Text),",
         "'Fecha registro (ingresado en la base)': Substitute(If(enc, varItem.'Fecha registro (ingresado en la base)', txtFechaReg_1.Text), \"-\", \"/\"),"),
        ("'Número de POL *': txtPOL_1.Text,", "'Número de POL *': Coalesce(txtPOL_1.Text, \"-1\"),"),
        ("'Diferenciador de título por ficha descarte': If(IsBlank(hrid), If(titulo in colFicha.Título, 0, 1), If(hrid in colFicha.HRID, 0, 1)),",
         "'Diferenciador de título por ficha descarte': If(IsBlank(hrid), If(titulo in colFicha.Título, 0, 1), If(IfError(Text(Value(hrid)), hrid) in ForAll(Filter(colFicha, !IsBlank('Item ingresado en la base de biblioteca')), Text(HRID)).Value, 0, 1)),"),
        ("'Unidad de descarte': drpUnidadDescarte_1.Selected.Value,",
         "'Unidad de descarte': If(drpUnidadDescarte_1.Selected.Value = \"(automático)\", Coalesce(varItem.Bib, \"\"), drpUnidadDescarte_1.Selected.Value),"),
        ("'Criterios de Descarte': drpCriterio_1.Selected.Value,",
         "'Criterios de Descarte': If(drpCriterio_1.Selected.Value = \"(automático)\", If(IsBlank(varItem.Crit), \"\", First(Split(varItem.Crit, \"|\")).Value), drpCriterio_1.Selected.Value),"),
        ("'Justificaciones para aplicar Descarte': drpJustificacion_1.Selected.Value,",
         "'Justificaciones para aplicar Descarte': If(drpJustificacion_1.Selected.Value = \"(automático)\", If(IsBlank(varItem.Crit), \"\", Last(Split(varItem.Crit, \"|\")).Value), drpJustificacion_1.Selected.Value),"),
        ("'Decisión Final Descarte SI/NO': Blank()", "'Decisión Final Descarte SI/NO': \"SI\""),
        ("Collect(colFicha, varNuevo);", "ClearCollect(colFicha, tblFichaDescarte);"),
        ("Set(varUltimo, varNuevo.Número & \" — \" & titulo);", "Set(varUltimo, varNuevo.'Codigo de Barra' & \" — \" & titulo);"),
        ("Notify(\"Guardado N° \" & varNuevo.Número, NotificationType.Success, 2000);", "Notify(\"Guardado \" & varNuevo.'Codigo de Barra', NotificationType.Success, 2000);"),
        ("Set(varDuplicado, cod in colFicha.'Codigo de Barra');",
         "Set(varDuplicado, cod in ForAll(Filter(colFicha, !IsBlank('Item ingresado en la base de biblioteca')), Text('Codigo de Barra')).Value);"),
        # valores por defecto de la ficha 2026
        ('Items: =["Esta en archivo", "No esta en archivo"]', 'Items: =["Si", "No"]'),
        ('Default: ="Esta en archivo"', 'Default: =If(varItem.\'Tipo de Material\' = "Issue", "No", "Si")'),
        ('Default: =If(drpFormaAdq_1.Selected.Value = "Compra" || drpCruce_1.Selected.Value = "Esta en archivo", "SI", "NO")', 'Default: =If(drpFormaAdq_1.Selected.Value = "Compra", "SI", "NO")'),
        ('Default: ="Por confirmar"', 'Default: ="NO"'),
    ]
    for a, b in R:
        n = t.count(a)
        assert n >= 1, a[:70]
        t = t.replace(a, b)
    # Unidad académica: None por defecto
    t = t.replace('Default: ="Desconocida"\n', 'Default: ="None"\n', 1)
    t = t.replace('Items: =["Facultad de Artes Liberales",', 'Items: =["None", "Facultad de Artes Liberales",', 1)
    # Obra en volúmenes: SI en revistas
    i = t.index('- drpVolumenes_1:'); j = t.index('Default: ="NO"', i)
    t = t[:j] + 'Default: =If(varItem.\'Tipo de Material\' = "Issue", "SI", "NO")' + t[j + len('Default: ="NO"'):]
    open(path, 'w').write(t)

ficha2026(R + '/pantallas/2_Descarte.txt')
ficha2026(R + '/pantallas/3_Descarte_masiva.txt')
ficha2026_1a1(R + '/pantallas/2_Descarte.txt')

# Descarte 1 a 1: enviar todos los ejemplares del título (misma biblioteca) a Lectura masiva
from comun import boton as _boton
TODOS = 'Filter(Split(IfError(Text(ParseJSON(varRes).todos), ""), ","), !IsBlank(Trim(Value)) && !(Trim(Value) in ForAll(Filter(colFicha, !IsBlank(\'Item ingresado en la base de biblioteca\')), Text(\'Codigo de Barra\')).Value))'
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

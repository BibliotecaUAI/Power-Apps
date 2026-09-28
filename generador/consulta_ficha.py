# Genera una consulta DAX para completar un grupo de filas de la Ficha 2026.
# Uso: python3 consulta_ficha.py FILA_INICIAL archivo_codigos.txt salida.txt
# - Códigos solo numéricos con menos de 6 dígitos se completan con ceros (5587 -> 005587).
# - Códigos con guion (revistas, ej. 36729-10) quedan igual.
# - Repetidos: la fila queda solo con el código y "REPETIDO: revisar" en Observaciones.
import re, sys
BASE = __file__.replace('generador/consulta_ficha.py', 'descarte/revistas/Ficha2026_v4_pegar_en_B610.txt')
def norm(c):
    c = c.strip()
    return c.zfill(6) if re.fullmatch(r'\d{1,5}', c) else c
def generar(fila0, codigos):
    t = open(BASE).read()
    vistos, filas = set(), []
    for k, c in enumerate(codigos):
        n = norm(c)
        filas.append('{ %d, "%s", "%s" }' % (fila0 + k, '' if n in vistos else n, n))
        vistos.add(n)
    t = re.sub(r'DATATABLE \( "fila", INTEGER, "cod", STRING, \{.*?\} \)\n',
               'DATATABLE ( "fila", INTEGER, "cod", STRING, "orig", STRING, { ' + ', '.join(filas) + ' } )\n', t, count=1, flags=re.S)
    t = t.replace('"Codigo de Barra", [cod],', '"Codigo de Barra", [orig],')
    t = t.replace('"Observaciones respecto de la justificación al Descarte", "",',
                  '"Observaciones respecto de la justificación al Descarte", IF ( [cod] = "", "REPETIDO: revisar", "" ),')
    t = t.replace('"Decisión Final Descarte SI/NO", "SI",', '"Decisión Final Descarte SI/NO", IF ( [cod] = "", "", "SI" ),')
    assert '[orig]' in t and 'REPETIDO' in t
    return t
if __name__ == '__main__':
    fila0 = int(sys.argv[1]); cods = [l for l in open(sys.argv[2]).read().split() if l.strip()]
    open(sys.argv[3], 'w').write(generar(fila0, cods))

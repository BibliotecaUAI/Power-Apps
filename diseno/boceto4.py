# Boceto v4: fluido, elegante, letra tipo Calibri (Carlito), textos 10-12 pt, vidrio + modo oscuro
def tema(oscuro):
    if oscuro:
        return dict(bg="radial-gradient(1200px 600px at 85% -10%,#3F4247 0%,transparent 60%),radial-gradient(900px 500px at 10% 110%,#2a2c30 0%,transparent 60%),#0B0B0C",
                    glass="rgba(40,42,46,0.55)", gb="rgba(191,195,200,0.22)", hi="rgba(255,255,255,0.10)",
                    tx="#F2F2F3", sub="#BFC3C8", mut="#8A8D91", line="rgba(191,195,200,0.18)", inp="rgba(255,255,255,0.06)", pos="#8FA3C7")
    return dict(bg="radial-gradient(1100px 560px at 88% -12%,#DADCDF 0%,transparent 62%),radial-gradient(900px 520px at 6% 112%,#E3E5E8 0%,transparent 60%),#F4F4F5",
                glass="rgba(255,255,255,0.62)", gb="rgba(255,255,255,0.9)", hi="rgba(255,255,255,0.9)",
                tx="#111111", sub="#3F4247", mut="#8A8D91", line="rgba(17,17,17,0.08)", inp="rgba(255,255,255,0.85)", pos="#1B2A4A")
F = "font-family:Carlito,Calibri,sans-serif"
DARK = "background:linear-gradient(115deg,#0B0B0C 0%,#111111 38%,#35373B 50%,#111111 62%,#0B0B0C 100%)"
SHINE = ("<div style='position:absolute;inset:0;background:linear-gradient(105deg,transparent 30%,rgba(255,255,255,0.55) 45%,transparent 60%);"
         "mix-blend-mode:screen;opacity:.55'></div>")
ITEMS = [('⌂','Inicio'),('▤','Descarte'),('↗','Préstamo'),('↙','Devolución'),('◎','Morosos'),('▣','Inventario')]

def css(t):
    return f"""
    .g{{background:{t['glass']};border:1px solid {t['gb']};border-radius:16px;backdrop-filter:blur(18px) saturate(140%);-webkit-backdrop-filter:blur(18px) saturate(140%);
        box-shadow:0 18px 40px rgba(17,17,17,0.10),0 2px 6px rgba(17,17,17,0.06),inset 0 1px 0 {t['hi']};position:absolute;overflow:hidden}}
    .g:before{{content:'';position:absolute;left:0;right:0;top:0;height:46%;background:linear-gradient(180deg,{t['hi']} 0%,transparent 100%);opacity:.35;pointer-events:none}}
    .h1{{{F};font-weight:700;font-size:15px;color:{t['tx']}}}
    .h2{{{F};font-style:italic;font-size:12px;color:{t['sub']}}}
    .p{{{F};font-size:12px;color:{t['sub']}}}
    .cap{{{F};font-size:10px;font-weight:700;letter-spacing:1.2px;color:{t['mut']};text-transform:uppercase}}
    .in{{position:absolute;box-sizing:border-box;height:34px;border-radius:10px;background:{t['inp']};border:1px solid {t['line']};{F};font-size:12px;color:{t['tx']};
         display:flex;align-items:center;padding:0 12px;box-shadow:inset 0 1px 2px rgba(17,17,17,0.06)}}
    .pill{{display:inline-block;padding:2px 9px;border-radius:999px;{F};font-size:10px;font-weight:700;letter-spacing:.4px}}
    .pos{{background:{t['pos']};color:#fff}}
    .pl{{background:linear-gradient(115deg,#8A8D91,#FFFFFF 50%,#BFC3C8);color:#111;border:1px solid #8A8D91}}
    table{{width:100%;border-collapse:collapse;{F};font-size:12px;color:{t['tx']}}}
    th{{text-align:left;font-size:10px;letter-spacing:1.2px;color:{t['mut']};font-weight:700;padding:7px 8px;border-bottom:1px solid {t['line']}}}
    td{{padding:8px;border-bottom:1px solid {t['line']}}}
    """

def header(t, titulo, sub):
    k=''.join(f"<div style='padding:0 20px;{'border-right:1px solid rgba(191,195,200,.25)' if i<2 else ''}'><div style='{F};font-size:20px;font-weight:700;color:{c}'>{v}</div><div style='{F};font-size:10px;letter-spacing:1.2px;color:#8A8D91;font-weight:700'>{l}</div></div>"
              for i,(v,l,c) in enumerate([('23','PRÉSTAMOS HOY','#fff'),('41','DEVOLUCIONES HOY','#fff'),('1.284','MOROSOS FOLIO','#BFC3C8')]))
    return (f"<div style='position:absolute;left:84px;top:14px;right:18px;height:72px;border-radius:18px;{DARK};border:1px solid #3F4247;box-shadow:0 14px 30px rgba(17,17,17,.25);overflow:hidden;display:flex;justify-content:space-between;align-items:center;padding:0 26px'>"
            f"{SHINE}<div style='position:relative'><div style='{F};font-size:10px;letter-spacing:2.5px;color:#BFC3C8;font-weight:700'>BIBLIOTECAS UAI</div>"
            f"<div style='{F};font-size:22px;font-weight:700;color:#fff;line-height:1.1'>{titulo}</div><div style='{F};font-size:12px;font-style:italic;color:#BFC3C8'>{sub}</div></div>"
            f"<div style='display:flex;position:relative'>{k}</div></div>")

def rail(t, active):
    it=''
    for ic,n in ITEMS:
        on=n==active
        it+=(f"<div style='width:44px;height:44px;margin:6px auto;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;"
             f"color:{'#fff' if on else '#8A8D91'};{'background:linear-gradient(135deg,#35373B,#111);box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 4px 10px rgba(0,0,0,.3);' if on else ''}'>{ic}</div>")
    return (f"<div style='position:absolute;left:14px;top:14px;bottom:14px;width:58px;border-radius:18px;{DARK.replace('115deg','180deg')};border:1px solid #3F4247;"
            f"box-shadow:0 14px 30px rgba(17,17,17,.25);padding-top:10px;box-sizing:border-box'>"
            f"<div style='{F};text-align:center;color:#fff;font-weight:700;font-size:13px;letter-spacing:1.5px;margin:12px 0 14px'>UAI</div>"
            f"<div style='height:1px;background:rgba(191,195,200,.25);margin:0 10px 8px'></div>{it}"
            f"<div style='position:absolute;bottom:14px;left:0;right:0;text-align:center;color:#BFC3C8;font-size:16px'>◐</div></div>")

def marcador(x,y,w,h,ic,tit,desc,kpi,num,t):
    return (f"<div class='g' style='left:{x}px;top:{y}px;width:{w}px;height:{h}px;clip-path:polygon(0 0,calc(100% - 26px) 0,100% 26px,100% 100%,0 100%)'>"
            f"<div style='position:absolute;right:0;top:0;width:26px;height:26px;background:linear-gradient(225deg,transparent 50%,#BFC3C8 50%,#FFFFFF 75%,#DADCDF)'></div>"
            f"<div style='position:absolute;left:22px;top:0;width:40px;height:64px;{DARK.replace('115deg','160deg')};clip-path:polygon(0 0,100% 0,100% 100%,50% 82%,0 100%);display:flex;justify-content:center;padding-top:16px;box-sizing:border-box;color:#fff;font-size:16px;overflow:hidden'>"
            f"{ic}<div style='position:absolute;inset:0;background:linear-gradient(160deg,transparent 35%,rgba(255,255,255,.55) 50%,transparent 65%)'></div></div>"
            f"<div style='position:absolute;right:38px;top:16px' class='cap'>0{num}</div>"
            f"<div style='position:absolute;left:78px;top:18px;right:40px'><div class='h1' style='font-size:17px'>{tit}</div><div class='h2' style='margin-top:3px'>{desc}</div></div>"
            f"<div style='position:absolute;left:22px;right:22px;bottom:14px;display:flex;justify-content:space-between;align-items:center'>"
            f"<span class='p' style='font-weight:700;color:{t['pos']}'>{kpi}</span><span class='cap' style='color:{t['tx']}'>Abrir →</span></div></div>")

def inicio(oscuro):
    t=tema(oscuro)
    tiles=[('▤','Descarte','Escanear y registrar material, libro a libro o en tanda','412 en la ficha · 23 hoy'),
           ('↗','Préstamo','RUT o QR de la cédula y los libros; plazo automático','23 préstamos hoy'),
           ('↙','Devolución','Libro a libro o el buzón completo; detecta morosos','41 devoluciones hoy'),
           ('◎','Morosos','Usuarios morosos reales de FOLIO','1.284 en FOLIO'),
           ('▣','Inventario','Toma de inventario de la colección','Próximamente')]
    pos=[(84,172,404,150),(502,172,404,150),(920,172,428,150),(84,338,628,150),(726,338,622,150)]
    b=header(t,'Inicio','Hola, Pablo · lunes 28 de septiembre')+rail(t,'Inicio')
    b+=f"<div style='position:absolute;left:86px;top:114px'><div class='h1'>¿Qué quieres hacer hoy?</div><div class='h2'>Elige un módulo o usa el menú de la izquierda</div></div>"
    b+=f"<div style='position:absolute;right:20px;top:118px;display:flex;align-items:center;gap:8px' class='p'><span class='cap'>Modo oscuro</span>{switch(oscuro)}</div>"
    for i,(p,tl) in enumerate(zip(pos,tiles)): b+=marcador(*p,*tl,i+1,t)
    b+=(f"<div class='g' style='left:84px;top:506px;width:1264px;height:246px'><div style='padding:16px 22px'><div class='h1'>Actividad reciente</div><div class='h2'>Últimos movimientos de hoy</div>"
        "<table style='margin-top:8px'><tr><th>HORA</th><th>MÓDULO</th><th>DETALLE</th><th>ESTADO</th></tr>"
        f"<tr><td>10:42</td><td>Préstamo</td><td>2 libros a Tomás Fuentes</td><td><span class='pill pos'>REGISTRADO</span></td></tr>"
        f"<tr><td>10:31</td><td>Devolución</td><td>Manual de derecho civil — Martina Rojas</td><td><span class='pill pl'>MOROSO · 5 DÍAS</span></td></tr>"
        f"<tr><td>10:12</td><td>Descarte</td><td>Tanda de 45 libros · Biblioteca Viña</td><td><span class='pill pos'>GUARDADO</span></td></tr></table></div></div>")
    return screen(b,t,'v4_inicio_'+('oscuro' if oscuro else 'claro'),oscuro)

def switch(on):
    return (f"<div style='width:40px;height:22px;border-radius:11px;position:relative;{DARK + ';' if on else 'background:#DADCDF;'}border:1px solid #BFC3C8'>"
            f"<div style='position:absolute;top:2px;left:{20 if on else 2}px;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.35)'></div></div>")

def prestamo():
    t=tema(False)
    b=header(t,'Préstamo','Préstamo ficticio · se registra en Excel')+rail(t,'Préstamo')
    b+=(f"<div class='g' style='left:84px;top:104px;width:470px;height:560px'><div style='padding:18px 22px'>"
        f"<div class='h1'>1 · Usuario</div><div class='h2'>Escanee el QR de la cédula o digite el RUT</div>"
        f"<div class='in' style='position:relative;margin-top:8px;width:100%'>20.456.789-K<span style='margin-left:auto;font-size:15px'>⌗</span></div>"
        f"<div class='h1' style='margin-top:22px'>2 · Libros</div><div class='h2'>Escanee uno tras otro; se suman a la lista</div>"
        f"<div class='in' style='position:relative;margin-top:8px;width:100%;color:{t['mut']}'>Código de barras…<span style='margin-left:auto;font-size:15px;color:{t['tx']}'>⌗</span></div>"
        f"<div class='h1' style='margin-top:22px'>3 · Condiciones</div><div class='h2'>Plazo según el tipo de material</div>"
        f"<div style='display:flex;gap:10px;margin-top:8px'><div style='flex:1'><div class='cap'>Biblioteca</div><div class='in' style='position:relative;margin-top:4px'>Biblioteca Viña<span style='margin-left:auto'>⌄</span></div></div>"
        f"<div style='flex:1'><div class='cap'>Correo al usuario</div><div class='in' style='position:relative;margin-top:4px'>Enviar resumen<span style='margin-left:auto'>⌄</span></div></div></div>"
        f"<div class='cap' style='margin-top:12px'>Observaciones</div><div class='in' style='position:relative;margin-top:4px'></div>"
        f"<div class='p' style='margin-top:14px;font-style:italic;color:{t['mut']}'>Libro 28 días · iPad 14 · Kindle 28 · calculadora, test y mapa 1 día · colección histórica solo sala</div></div></div>")
    b+=(f"<div class='g' style='left:570px;top:104px;width:778px;height:150px;border:1.5px solid #B3261E;box-shadow:0 0 0 3px rgba(179,38,30,.12),0 18px 40px rgba(17,17,17,.10)'><div style='padding:18px 22px'>"
        f"<div class='cap' style='color:{t['pos']}'>● Usuario encontrado en FOLIO</div><div class='h1' style='font-size:19px;margin-top:4px'>Tomás Fuentes Díaz</div>"
        f"<div class='h2'>RUT 19.874.302-5 · Pregrado · Facultad de Derecho · Derecho</div>"
        f"<div style='display:flex;gap:26px;margin-top:10px;align-items:center' class='p'><span><b style='color:{t['tx']}'>2</b> préstamos activos</span><span><b style='color:{t['tx']}'>1</b> vencido hace 10 días</span><span style='margin-left:auto' class='pill pl'>MOROSO</span></div></div></div>")
    rows=[('000101','Imposición fiscal en los países en desarrollo','Libro','28 DÍAS','26-10-2026',1),('IP-014','iPad 10ª gen. N° 14','iPad','14 DÍAS','12-10-2026',1),
          ('CA-203','Calculadora Casio fx-991','Calculadora','1 DÍA','29-09-2026',1),('H-00931','Crónica del Reino de Chile (1865)','Col. histórica','SOLO SALA','—',0)]
    tr=''.join(f"<tr><td><b>{a}</b></td><td>{b_}</td><td>{c}</td><td><span class='pill {'pos' if ok else 'pl'}'>{d}</span></td><td>{e}</td><td style='color:{t['mut']}'>✕</td></tr>" for a,b_,c,d,e,ok in rows)
    b+=(f"<div class='g' style='left:570px;top:268px;width:778px;height:396px'><div style='padding:18px 22px'><div style='display:flex;justify-content:space-between;align-items:center'>"
        f"<div><div class='h1'>Libros a prestar</div><div class='h2'>Datos desde FOLIO</div></div><div><span class='pill pos'>3 LISTOS</span> <span class='pill pl'>1 SOLO SALA</span></div></div>"
        f"<table style='margin-top:10px'><tr><th>CÓDIGO</th><th>TÍTULO</th><th>TIPO</th><th>PLAZO</th><th>VENCE</th><th></th></tr>{tr}</table></div></div>")
    b+=(f"<div style='position:absolute;left:570px;top:680px;width:590px;height:48px;border-radius:14px;{DARK};border:1px solid #3F4247;box-shadow:0 10px 22px rgba(17,17,17,.25);overflow:hidden;display:flex;align-items:center;justify-content:center;{F};font-size:13px;font-weight:700;letter-spacing:2px;color:#fff'>{SHINE}<span style='position:relative'>REGISTRAR PRÉSTAMO (3) →</span></div>"
        f"<div class='g' style='left:1174px;top:680px;width:174px;height:48px;display:flex;align-items:center;justify-content:center'><span class='p' style='color:{t['tx']}'>Cancelar</span></div>")
    return screen(b,t,'v4_prestamo',False)

def morosos():
    t=tema(True)
    b=header(t,'Morosos','Datos reales de FOLIO · consultado 10:42')+rail(t,'Morosos')
    b+=(f"<div class='in' style='left:84px;top:104px;width:330px;color:{t['mut']}'>⌕ Buscar por nombre o RUT…</div>"
        f"<div class='in' style='left:426px;top:104px;width:190px'>Todos los niveles<span style='margin-left:auto'>⌄</span></div>"
        f"<div class='in' style='left:628px;top:104px;width:230px'>Todas las bibliotecas<span style='margin-left:auto'>⌄</span></div>"
        f"<div style='position:absolute;right:20px;top:110px;display:flex;align-items:center;gap:8px'><span class='cap'>Modo oscuro</span>{switch(True)}</div>")
    kp=[('1.284','Usuarios morosos'),('2.031','Libros vencidos'),('317','Más de 2 años'),('2','Vencidos de prueba')]
    for i,(v,l) in enumerate(kp):
        b+=f"<div class='g' style='left:{84+i*318}px;top:152px;width:304px;height:84px'><div style='padding:14px 20px'><div style='{F};font-size:26px;font-weight:700;color:{t['tx']}'>{v}</div><div class='h2'>{l}</div></div></div>"
    rows=[('10891774-1','Tomás Fuentes Díaz','Pregrado','Biblioteca Viña',3,'2.110','NIVEL 3'),('17654321-K','Camila Soto Vera','Postgrado','Biblioteca Postgrado',1,'940','NIVEL 2'),
          ('19874302-5','Diego Rojas Muñoz','Pregrado','Pregrado Edif. A',2,'412','NIVEL 1'),('20456789-K','Martina Pérez León','Pregrado','Pregrado Edif. F',1,'35','NIVEL 0'),
          ('15234876-2','Andrés Silva Toro','Académico','Biblioteca Viña',4,'28','NIVEL 0')]
    tr=''.join(f"<tr style='{'box-shadow:inset 3px 0 0 #B3261E' if n in ('NIVEL 3','NIVEL 2') else ''}'><td><b>{a}</b></td><td>{b_}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f_}</td><td><span class='pill {'pos' if n=='NIVEL 0' else 'pl'}'>{n}</span></td></tr>" for a,b_,c,d,e,f_,n in rows)
    b+=(f"<div class='g' style='left:84px;top:250px;width:1264px;height:430px'><div style='padding:18px 22px'><div class='h1'>Usuarios morosos</div><div class='h2'>Ordenados por días de atraso · la línea roja marca más de 2 años</div>"
        f"<table style='margin-top:10px'><tr><th>RUT</th><th>NOMBRE</th><th>TIPO</th><th>BIBLIOTECA</th><th>LIBROS</th><th>DÍAS</th><th>NIVEL</th></tr>{tr}</table></div></div>")
    b+=(f"<div style='position:absolute;left:84px;top:694px;width:320px;height:44px;border-radius:14px;background:linear-gradient(115deg,#8A8D91,#FFFFFF 50%,#BFC3C8);border:1px solid #8A8D91;display:flex;align-items:center;justify-content:center;{F};font-size:12px;font-weight:700;letter-spacing:2px;color:#111'>↻  ACTUALIZAR DESDE FOLIO</div>")
    return screen(b,t,'v4_morosos_oscuro',True)

def screen(body,t,label,oscuro):
    return (f"<div class='scr' data-l='{label}' style='position:relative;width:1366px;height:768px;overflow:hidden;background:{t['bg']};margin-bottom:24px'>"
            f"<style>{css(t).replace('.g','.'+label+' .g').replace('.h1','.'+label+' .h1').replace('.h2','.'+label+' .h2')}</style><div class='{label}'>"
            f"<style>.{label} .p{{{css(t).split('.p{')[1].split('}')[0]}}} .{label} .cap{{{css(t).split('.cap{')[1].split('}')[0]}}} .{label} .in{{{css(t).split('.in{')[1].split('}')[0]}}} .{label} td{{{css(t).split('td{')[1].split('}')[0]}}} .{label} th{{{css(t).split('th{')[1].split('}')[0]}}} .{label} table{{{css(t).split('table{')[1].split('}')[0]}}} .{label} .pos{{{css(t).split('.pos{')[1].split('}')[0]}}}</style>"
            f"{body}</div></div>")

html = f"<html><head><meta charset='utf-8'><link href='fonts/carlito.css' rel='stylesheet'></head><body style='margin:0;background:#DADCDF'>{inicio(False)}{inicio(True)}{prestamo()}{morosos()}</body></html>"
open('boceto4.html','w').write(html)

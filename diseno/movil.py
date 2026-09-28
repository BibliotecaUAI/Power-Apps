F="font-family:Carlito,Calibri,sans-serif"
DARK="background:linear-gradient(115deg,#0B0B0C 0%,#111111 38%,#35373B 50%,#111111 62%,#0B0B0C 100%)"
def T(o):
    return dict(bg="#141416" if o else "#FFFFFF", franja="#F2F2F3" if o else "#111111", marca="#26272B" if o else "#E6E7E9",
        glass=("background:rgba(38,39,43,.55);border:1px solid rgba(191,195,200,.22);box-shadow:0 12px 26px rgba(0,0,0,.45)" if o else
               "background:rgba(255,255,255,.62);backdrop-filter:blur(18px);border:1px solid rgba(255,255,255,.85);box-shadow:0 12px 26px rgba(17,17,17,.12),inset 0 1px 0 #fff"),
        tx="#F2F2F3" if o else "#111", sub="#C4C7CC" if o else "#3F4247", mut="#9A9DA2" if o else "#8A8D91",
        inp="#2E3034" if o else "#fff", line="rgba(191,195,200,.2)" if o else "rgba(17,17,17,.10)", pos="#E6E7E9" if o else "#111", posTx="#111" if o else "#fff")
CINTA=("<div style='position:absolute;right:16px;top:0;width:18px;height:28px;%s;clip-path:polygon(0 0,100%% 0,100%% 100%%,50%% 78%%,0 100%%)'>"
       "<div style='position:absolute;inset:0;background:linear-gradient(160deg,transparent 35%%,rgba(255,255,255,.6) 50%%,transparent 65%%)'></div></div>") % DARK
def fondo(t): return (f"<div style='position:absolute;inset:0;background:{t['bg']}'></div><div style='position:absolute;left:0;top:0;bottom:0;width:6px;background:{t['franja']}'></div>"
                      f"<div style='position:absolute;right:-6px;top:260px;writing-mode:vertical-rl;font-family:Arial Black,Arial;font-weight:900;font-size:150px;color:{t['marca']}'>UAI</div>")
def header(t,tit,sub):
    return (f"<div style='position:absolute;left:14px;right:14px;top:44px;height:64px;border-radius:18px;{DARK};border:1px solid #3F4247;box-shadow:0 10px 22px rgba(17,17,17,.3);padding:10px 16px;box-sizing:border-box;overflow:hidden'>"
            "<div style='position:absolute;inset:0;background:linear-gradient(105deg,transparent 30%,rgba(255,255,255,.35) 46%,transparent 60%);opacity:.5'></div>"
            f"<div style='position:relative;{F};font-size:9px;letter-spacing:2px;color:#BFC3C8;font-weight:700'>BIBLIOTECAS UAI</div>"
            f"<div style='position:relative;{F};font-size:18px;font-weight:700;color:#fff;line-height:1.1'>{tit}</div><div style='position:relative;{F};font-size:11px;font-style:italic;color:#BFC3C8'>{sub}</div>"
            f"<div style='position:absolute;right:16px;top:20px;width:24px;height:24px;border-radius:50%;border:1px solid #8A8D91;color:#BFC3C8;display:flex;align-items:center;justify-content:center;font-size:13px'>◐</div></div>")
def tabbar(t,act):
    it=''.join(f"<div style='flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;color:{'#fff' if n==act else '#8A8D91'}'>"
               f"<div style='width:40px;height:30px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;{'background:linear-gradient(135deg,#35373B,#111);' if n==act else ''}'>{i}</div><div style='{F};font-size:9px'>{n}</div></div>"
               for i,n in [('⌂','Inicio'),('▤','Descarte'),('↗','Préstamo'),('↙','Devolución'),('◎','Morosos')])
    return f"<div style='position:absolute;left:14px;right:14px;bottom:18px;height:62px;border-radius:20px;{DARK};border:1px solid #3F4247;box-shadow:0 10px 22px rgba(17,17,17,.35);display:flex;align-items:center;padding:0 6px'>{it}</div>"
def card(t,x,y,w,h,inner,cinta=True):
    return f"<div style='position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:16px;{t['glass']};overflow:hidden;box-sizing:border-box'>{CINTA if cinta else ''}<div style='padding:12px 14px'>{inner}</div></div>"
def phone(label,body):
    return f"<div class='scr' data-l='{label}' style='display:inline-block;margin:10px;vertical-align:top'><div style='position:relative;width:390px;height:844px;border-radius:44px;overflow:hidden;box-shadow:0 0 0 10px #111,0 0 0 11px #3F4247'>{body}<div style='position:absolute;left:50%;top:10px;transform:translateX(-50%);width:110px;height:28px;border-radius:14px;background:#000'></div></div></div>"
def inicio(o):
    t=T(o); b=fondo(t)+header(t,'Inicio','Hola, Pablo · lunes 28 sept.')
    tiles=[('▤','Descarte','412 en ficha'),('↗','Préstamo','23 hoy'),('↙','Devolución','41 hoy'),('◎','Morosos','1.284 FOLIO')]
    for k,(ic,n,kp) in enumerate(tiles):
        x=14+(k%2)*187; y=124+(k//2)*136
        b+=card(t,x,y,175,124,f"<div style='width:34px;height:34px;border-radius:10px;{DARK};color:#fff;display:flex;align-items:center;justify-content:center;font-size:16px'>{ic}</div>"
               f"<div style='{F};font-size:15px;font-weight:700;color:{t['tx']};margin-top:10px'>{n}</div><div style='{F};font-size:11px;font-style:italic;color:{t['sub']}'>{kp}</div>")
    b+=card(t,14,404,362,120,f"<div style='{F};font-size:15px;font-weight:700;color:{t['tx']}'>Inventario</div><div style='{F};font-size:11px;font-style:italic;color:{t['sub']}'>Próximamente</div>")
    rows=''.join(f"<div style='display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid {t['line']};{F};font-size:12px;color:{t['tx']}'><span>{a}</span>{bb}</div>"
                 for a,bb in [('Tomás F. · 2 libros',f"<span style='padding:1px 8px;border-radius:9px;background:{t['pos']};color:{t['posTx']};font-size:10px;font-weight:700'>REGISTRADO</span>"),
                              ('Martina R. · devolución',"<span style='padding:1px 8px;border-radius:9px;background:#B3261E;color:#fff;font-size:10px;font-weight:700'>MOROSO</span>")])
    b+=card(t,14,536,362,140,f"<div style='{F};font-size:15px;font-weight:700;color:{t['tx']}'>Actividad reciente</div>{rows}")
    return phone('movil_inicio_'+('oscuro' if o else 'claro'), b+tabbar(t,'Inicio'))
def prestamo(o):
    t=T(o); b=fondo(t)+header(t,'Préstamo','Ficticio · se registra en Excel')
    b+=(f"<div style='position:absolute;left:14px;right:14px;top:122px;height:40px;border-radius:12px;background:{t['inp']};border:1px solid {t['line']};{F};font-size:13px;color:{t['tx']};display:flex;align-items:center;padding:0 12px'>19.874.302-5<span style='margin-left:auto;width:30px;height:30px;border-radius:8px;{DARK};color:#fff;display:flex;align-items:center;justify-content:center'>⌗</span></div>")
    b+=(f"<div style='position:absolute;left:14px;right:14px;top:174px;height:132px;border-radius:18px;{DARK};border:1.5px solid #B3261E;box-shadow:0 0 18px rgba(179,38,30,.35);overflow:hidden'>"
        f"<div style='position:absolute;left:14px;top:18px;width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#8A8D91,#fff 45%,#BFC3C8);padding:2px;box-sizing:border-box'><div style='width:100%;height:100%;border-radius:50%;background:#111;color:#fff;{F};font-weight:700;font-size:20px;display:flex;align-items:center;justify-content:center'>TF</div></div>"
        f"<div style='position:absolute;left:88px;top:16px;right:12px'><div style='{F};font-size:9px;letter-spacing:1.5px;color:#BFC3C8;font-weight:700'>CARNÉ · FOLIO</div><div style='{F};font-size:17px;font-weight:700;color:#fff'>Tomás Fuentes Díaz</div><div style='{F};font-size:11px;font-style:italic;color:#BFC3C8'>Pregrado · Derecho</div></div>"
        f"<div style='position:absolute;left:14px;right:14px;bottom:12px;display:flex;gap:8px;{F}'><div style='flex:1;border-radius:10px;background:rgba(255,255,255,.07);border:1px solid rgba(191,195,200,.25);color:#fff;text-align:center;padding:4px 0'><b>2</b> <span style='font-size:10px;color:#BFC3C8'>activos</span></div>"
        f"<div style='flex:1;border-radius:10px;background:rgba(255,255,255,.07);border:1px solid rgba(191,195,200,.25);color:#FF6B5E;text-align:center;padding:4px 0'><b>1</b> <span style='font-size:10px;color:#BFC3C8'>vencido</span></div>"
        f"<div style='flex:1;border-radius:10px;border:1.5px solid #B3261E;color:#FF8A80;text-align:center;padding:4px 0;font-size:11px;font-weight:700'>MOROSO</div></div></div>")
    b+=(f"<div style='position:absolute;left:14px;right:14px;top:318px;height:40px;border-radius:12px;background:{t['inp']};border:1px solid {t['line']};{F};font-size:13px;color:{t['mut']};display:flex;align-items:center;padding:0 12px'>Código del libro…<span style='margin-left:auto;width:30px;height:30px;border-radius:8px;{DARK};color:#fff;display:flex;align-items:center;justify-content:center'>⌗</span></div>")
    libs=''.join(f"<div style='display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid {t['line']};{F}'><div><div style='font-size:12px;font-weight:700;color:{t['tx']}'>{a}</div><div style='font-size:10px;font-style:italic;color:{t['sub']}'>{c} · vence {d}</div></div>"
                 f"<span style='padding:1px 8px;border-radius:9px;font-size:10px;font-weight:700;{('background:'+t['pos']+';color:'+t['posTx']) if ok else 'background:linear-gradient(115deg,#8A8D91,#fff 50%,#BFC3C8);color:#111'}'>{e}</span></div>"
                 for a,c,d,e,ok in [('Imposición fiscal…','Libro','26-10','28 DÍAS',1),('iPad N° 14','iPad','12-10','14 DÍAS',1),('Crónica del Reino…','Col. histórica','—','SOLO SALA',0)])
    b+=card(t,14,370,362,260,f"<div style='{F};font-size:15px;font-weight:700;color:{t['tx']}'>Libros a prestar</div>{libs}")
    b+=(f"<div style='position:absolute;left:14px;right:14px;top:642px;height:50px;border-radius:14px;{DARK};border:1px solid #3F4247;color:#fff;{F};font-size:13px;font-weight:700;letter-spacing:2px;display:flex;align-items:center;justify-content:center'>REGISTRAR (2) →</div>")
    return phone('movil_prestamo_'+('oscuro' if o else 'claro'), b+tabbar(t,'Préstamo'))
html="<html><head><meta charset='utf-8'><link href='fonts/carlito.css' rel='stylesheet'></head><body style='margin:0;background:#DADCDF;padding:10px;white-space:nowrap'>"+inicio(False)+prestamo(False)+inicio(True)+prestamo(True)+"</body></html>"
open('movil.html','w').write(html)

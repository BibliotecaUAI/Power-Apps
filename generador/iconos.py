S='stroke="currentColor" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
def sv(p): return f'<svg width="22" height="22" viewBox="0 0 24 24" {S}>{p}</svg>'
LIN = {
 'Inicio': sv('<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
 'Descarte': sv('<path d="M4 7h16"/><path d="M9 7V4h6v3"/><path d="M6 7l1 13h10l1-13"/><path d="M10 11v6M14 11v6"/>'),
 'Préstamo': sv('<path d="M4 5h9a2 2 0 0 1 2 2v12H6a2 2 0 0 1-2-2z"/><path d="M15 12h6M18 9l3 3-3 3"/>'),
 'Devolución': sv('<path d="M11 5h9v14h-9a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z"/><path d="M9 12H3M6 9l-3 3 3 3"/>'),
 'Morosos': sv('<circle cx="12" cy="13" r="7"/><path d="M12 9v4l2.5 2"/><path d="M5 4l-2 2M19 4l2 2"/>'),
 'Inventario': sv('<path d="M4 6v12M7 6v12M10 6v12M14 6v12M17 6v12M20 6v12"/><path d="M2 3h4M18 3h4M2 21h4M18 21h4"/>'),
}
F='fill="currentColor"'
def sf(p): return f'<svg width="22" height="22" viewBox="0 0 24 24" {F}>{p}</svg>'
SOL = {
 'Inicio': sf('<path d="M12 3l9 7v11h-6v-6H9v6H3V10z"/>'),
 'Descarte': sf('<path d="M9 2h6v2h5v3H4V4h5z"/><path d="M5 8h14l-1 14H6z"/>'),
 'Préstamo': sf('<path d="M3 4h10a2 2 0 0 1 2 2v14H5a2 2 0 0 1-2-2z"/><path d="M16 11h4V8l4 4-4 4v-3h-4z"/>'),
 'Devolución': sf('<path d="M11 4h10v16H11a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M8 11H4V8l-4 4 4 4v-3h4z"/>'),
 'Morosos': sf('<path d="M12 2L1 21h22z"/><rect x="11" y="9" width="2" height="6" fill="#111"/><rect x="11" y="17" width="2" height="2" fill="#111"/>'),
 'Inventario': sf('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M6 8v8M8.5 8v8M11 8v8M14 8v8M17 8v8" stroke="#111" stroke-width="1.3"/>'),
}
UNI_A = {'Inicio':'⌂','Descarte':'▤','Préstamo':'↗','Devolución':'↙','Morosos':'▦','Inventario':'▣'}
UNI_B = {'Inicio':'⌂','Descarte':'⊘','Préstamo':'⇥','Devolución':'⇤','Morosos':'⚑','Inventario':'☷'}
UNI_C = {'Inicio':'◉','Descarte':'✕','Préstamo':'➜','Devolución':'⟲','Morosos':'⏱','Inventario':'▥'}
opts=[('A · Actual',UNI_A,False),('B · Símbolos nuevos',UNI_B,False),('C · Símbolos modernos',UNI_C,False),('D · Íconos de línea (recomendado)',LIN,True),('E · Íconos rellenos',SOL,True)]
def rail(d,svg):
    it=''
    for i,t in enumerate(['Inicio','Descarte','Préstamo','Devolución','Morosos','Inventario']):
        on=i==2
        box="background:linear-gradient(135deg,#35373B,#111);box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 4px 10px rgba(0,0,0,.35);color:#fff;" if on else "color:#8A8D91;"
        ic=d[t] if svg else f"<span style='font-size:18px'>{d[t]}</span>"
        it+=f"<div style='height:52px;display:flex;align-items:center;padding-left:7px'><div style='width:178px;height:42px;border-radius:12px;display:flex;align-items:center;padding-left:12px;box-sizing:border-box;{box}'><span style='width:22px;display:flex;justify-content:center'>{ic}</span><span style='margin-left:14px;font-size:12px;letter-spacing:1px;font-weight:{700 if on else 400}'>{t}</span></div></div>"
    return it
cols=''.join(f"<div style='margin:10px'><div style='font:700 13px Calibri,Carlito,sans-serif;color:#111;margin:0 0 8px 4px'>{n}</div><div style='width:196px;padding:12px 0;border-radius:18px;background:linear-gradient(180deg,#0B0B0C,#111 38%,#35373B 50%,#111 62%,#0B0B0C);font-family:Calibri,Carlito,sans-serif'>{rail(d,s)}</div></div>" for n,d,s in opts)
open('iconos.html','w').write(f"<html><body style='margin:0;background:#EDEDED'><div style='display:flex;padding:14px'>{cols}</div></body></html>")

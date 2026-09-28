def btn(n, txt, x, on, sel):
    return f'''      - {n}:
          Control: Classic/Button@2.2.0
          Properties:
            BorderColor: =ColorValue("#111111")
            BorderThickness: =1
            Color: =ColorValue("{'#FFFFFF' if on else '#111111'}")
            Fill: =ColorValue("{'#111111' if on else '#FFFFFF'}")
            Font: =Font.'Segoe UI'
            FontWeight: =FontWeight.Bold
            Height: =30
            HoverColor: =ColorValue("#FFFFFF")
            HoverFill: =ColorValue("{'#111111' if on else '#3F4247'}")
            OnSelect: ={sel}
            PressedFill: =ColorValue("#3F4247")
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Size: =9
            Text: ="{txt}"
            Width: =150
            X: ={x}
            Y: =124'''

def label(n, text, x, y, w, h=14, size=7, color="#8A8D91", bold=True, align=None):
    text_line = ('|-\n              ' + text) if (': ' in text or ' #' in text) else text
    s = f'''      - {n}:
          Control: Label@2.5.1
          Properties:
'''
    if align: s += f'            Align: =Align.{align}\n'
    s += f'''            Color: =ColorValue("{color}")
            Font: =Font.'Segoe UI'
'''
    if bold: s += '            FontWeight: =FontWeight.Bold\n'
    s += f'''            Height: ={h}
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Size: ={size}
            Text: {text_line}
            Width: ={w}
            X: ={x}
            Y: ={y}'''
    return s

def tabs(sfx, uno, otra, hint):
    nav = f'Navigate({otra}, ScreenTransition.None)'
    return '\n'.join([
        btn(f'btnModo1a1_{sfx}', 'LECTURA 1 A 1', 80, uno, 'false' if uno else nav),
        btn(f'btnModoMasiva_{sfx}', 'LECTURA MASIVA', 229, not uno, nav if uno else 'false'),
        label(f'lblModoHint_{sfx}', f'="{hint}"', 394, 124, 220, h=30, size=8),
    ])

def switch(sfx, masiva, otra, hint):
    track = ("background:linear-gradient(115deg,#0B0B0C 0%,#35373B 50%,#111111 100%);border:1px solid #8A8D91"
             if masiva else "background:#DADCDF;border:1px solid #BFC3C8")
    knob = "left:23px" if masiva else "left:2px"
    c1, c2 = ("#8A8D91", "#111111") if masiva else ("#111111", "#8A8D91")
    html = (f"<div style='height:30px;display:flex;align-items:center;font-family:Segoe UI,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:1.5px'>"
            f"<span style='color:{c1}'>LECTURA 1 A 1</span>"
            f"<div style='margin:0 12px;width:46px;height:24px;border-radius:12px;box-sizing:border-box;position:relative;{track}'>"
            f"<div style='position:absolute;top:2px;{knob};width:18px;height:18px;border-radius:50%;background:#FFFFFF;box-shadow:0 1px 3px rgba(0,0,0,0.35)'></div></div>"
            f"<span style='color:{c2}'>LECTURA MASIVA</span></div>")
    return '\n'.join([
        f'''      - htmlSwitch_{sfx}:
          Control: HtmlViewer@2.1.0
          Properties:
            Height: =30
            HtmlText: |-
              ="{html}"
            PaddingBottom: =0
            PaddingLeft: =0
            PaddingRight: =0
            PaddingTop: =0
            Width: =300
            X: =80
            Y: =124''',
        f'''      - btnSwitch_{sfx}:
          Control: Classic/Button@2.2.0
          Properties:
            BorderThickness: =0
            Color: =RGBA(0, 0, 0, 0)
            Fill: =RGBA(0, 0, 0, 0)
            Height: =30
            HoverFill: =RGBA(191, 195, 200, 0.12)
            OnSelect: =Navigate({otra}, ScreenTransition.Fade)
            PressedFill: =RGBA(191, 195, 200, 0.25)
            RadiusBottomLeft: =0
            RadiusBottomRight: =0
            RadiusTopLeft: =0
            RadiusTopRight: =0
            Text: =""
            Width: =300
            X: =80
            Y: =124''',
        label(f'lblModoHint_{sfx}', f'="{hint}"', 400, 124, 210, h=30, size=8),
    ])

# Gera a sobreposição transparente (PNG) da capa com foto: tools/overlay.py spec.json saida.html
import json, sys, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
D=os.path.dirname(os.path.abspath(__file__)); F=D+'/node_modules/@fontsource'
e=html.escape
s=json.load(open(sys.argv[1],encoding='utf-8')); out=sys.argv[2]
n=len(s.get('slides',[]))+2 if s.get('kind')=='carousel' else None
title=s.get('title') or s.get('statement'); sub=s.get('subtitle') or s.get('sub','')
ff=''
for fam,d,ws in [('DM Serif Display','dm-serif-display',[400]),('Source Sans 3','source-sans-3',[400,600,700])]:
    for w in ws:
        for sb in ['latin','latin-ext']:
            ff+=f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{F}/{d}/files/{d}-{sb}-{w}-normal.woff2')}}"
css=ff+"""
html,body{margin:0;background:transparent}
.p{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:'Source Sans 3',sans-serif;color:#EFEBE2}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,26,35,.55) 0%,rgba(22,26,35,0) 22%,rgba(22,26,35,0) 38%,rgba(22,26,35,.82) 62%,rgba(22,26,35,.96) 100%)}
.frame{position:absolute;inset:26px;border:2px solid rgba(205,191,152,.55);border-radius:28px}
.top{position:absolute;left:88px;top:84px;display:flex;align-items:center;gap:22px}
.top img{height:92px}
.lab{font-weight:700;letter-spacing:.2em;font-size:27px;color:#E3D6B3;text-transform:uppercase}
.bot{position:absolute;left:88px;right:88px;bottom:150px;display:flex;flex-direction:column;gap:26px}
.t{font-family:'DM Serif Display',serif;font-size:80px;line-height:1.04;margin:0;text-wrap:balance}
.sub{font-size:35px;line-height:1.35;color:#E4DFD3;margin:0}
.swipe{font-size:28px;font-weight:700;letter-spacing:.14em;color:#E3D6B3;text-transform:uppercase}
.foot{position:absolute;left:88px;right:88px;bottom:64px;display:flex;justify-content:space-between;align-items:center;font-size:26px;color:#D5CCB6;font-weight:600}
.foot img{height:40px}
"""
right='@wellingtoncampos.advogado'+(f' · 1/{n}' if n else '')
swipe='<div class="swipe">Arraste para o lado →</div>' if n else ''
body=f'''<div class="p"><div class="shade"></div><div class="frame"></div>
<div class="top"><img src="file://{D}/logo-mark.png" alt=""><div class="lab">{e(s['label'])}</div></div>
<div class="bot"><h1 class="t">{e(title)}</h1>{f'<p class="sub">{e(sub)}</p>' if sub else ''}{swipe}</div>
<div class="foot"><img src="file://{D}/logo-word.png" alt="Wellington Campos"><span>{right}</span></div></div>'''
open(out,'w',encoding='utf-8').write(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>')

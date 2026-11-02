import json, sys, html, os
D=os.path.dirname(os.path.abspath(__file__)); F=D+'/node_modules/@fontsource'
def ff():
    s=''
    for fam,d,ws in [('DM Serif Display','dm-serif-display',[400]),('Source Sans 3','source-sans-3',[400,600,700])]:
        for w in ws:
            for sub in ['latin','latin-ext']:
                s+=f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{F}/{d}/files/{d}-{sub}-{w}-normal.woff2')}}"
    return s
CSS=ff()+"""
body{margin:0}
.p{width:1080px;height:1350px;box-sizing:border-box;background:radial-gradient(120% 90% at 30% 0%,#3A4458 0%,#232A38 55%,#161A23 100%);color:#EFEBE2;padding:84px 88px 64px;display:flex;flex-direction:column;font-family:'Source Sans 3',sans-serif;position:relative;overflow:hidden}
.p:before{content:'';position:absolute;inset:26px;border:2px solid rgba(205,191,152,.35);border-radius:28px;pointer-events:none}
.top{display:flex;align-items:center;gap:22px}
.top img{height:92px}
.lab{font-weight:700;letter-spacing:.2em;font-size:27px;color:#CDBF98;text-transform:uppercase}
.q{font-family:'DM Serif Display',serif;font-size:74px;line-height:1.08;margin:52px 0 0;max-width:880px;text-wrap:balance}
.t{font-family:'DM Serif Display',serif;font-size:84px;line-height:1.04;margin:0;text-wrap:balance}
.sub{font-size:36px;line-height:1.35;color:#D9D3C4;margin:28px 0 0;max-width:840px}
.stamp{position:absolute;right:92px;transform:rotate(-8deg);border:8px solid currentColor;font-weight:700;font-size:92px;letter-spacing:.08em;padding:2px 32px;border-radius:14px}
.box{margin-top:auto;background:#EFEBE2;color:#1C2230;border-radius:24px;padding:44px 48px;display:flex;flex-direction:column;gap:18px}
.box h2{margin:0;font-family:'DM Serif Display',serif;font-weight:400;font-size:46px;line-height:1.1}
.box p{margin:0;font-size:33px;line-height:1.4}
.src{font-size:25px;color:#6B6450;font-weight:700;letter-spacing:.04em}
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:38px;font-size:26px;color:#BDB49C;font-weight:600}
.foot img{height:40px}
.mid{margin:auto 0;display:flex;flex-direction:column;gap:30px}
.num{font-family:'DM Serif Display',serif;font-size:120px;line-height:.9;color:#CDBF98}
.h{font-family:'DM Serif Display',serif;font-size:64px;line-height:1.08;margin:0;text-wrap:balance}
.txt{font-size:38px;line-height:1.45;color:#E4DFD3;margin:0}
.swipe{font-size:28px;font-weight:700;letter-spacing:.14em;color:#CDBF98;text-transform:uppercase}
.mark{height:150px;align-self:flex-start}
.disc{font-size:24px;color:#A9A08A;line-height:1.4}
.light .p{background:radial-gradient(120% 90% at 20% 0%,#FBF8F2 0%,#F3EDE2 60%,#E9E1D2 100%);color:#1F2633}
.light .p:before{border-color:rgba(140,117,80,.45)}
.light .lab,.light .num,.light .swipe{color:#8C7550}
.light .sub,.light .txt,.light ul.l{color:#3A4150}
.light .box{background:#1F2633;color:#F3EDE2}
.light .src{color:#CDBF98}
.light .foot{color:#6E6556}
.light .disc{color:#7A7262}
.art{color:#CDBF98;opacity:.92;display:flex}
.light .art{color:#9A7E4E}
.art svg{width:100%;height:100%}
.art-single{width:230px;height:230px;flex:0 1 230px;min-height:0;margin:30px 0 24px;align-self:flex-end}
.art-single.left{align-self:flex-start}
.art-cover{position:absolute;right:70px;bottom:150px;width:330px;height:330px;opacity:.85}
ul.l{margin:0;padding-left:34px;display:flex;flex-direction:column;gap:14px;font-size:36px;line-height:1.4;color:#E4DFD3}
"""
THEME='dark'
def logo(name): return f"file://{D}/{name}{'-dark' if THEME=='light' else ''}.png"
def page(inner, idx=None, total=None):
    right='@wellingtoncampos.advogado'+(f' · {idx}/{total}' if idx else '')
    return f'<div class="p">{inner}<div class="foot"><img src="{logo('logo-word')}" alt="Wellington Campos"><span>{right}</span></div></div>'
def top(label): return f'<div class="top"><img src="{logo('logo-mark')}" alt=""><div class="lab">{label}</div></div>'
e=html.escape
def art(name, cls):
    if not name: return ''
    svg=open(f'{D}/ilustracoes/{name}.svg').read()
    return f'<div class="art {cls}" aria-hidden="true">{svg}</div>'
def single(s):
    stamp=''
    if s.get('stamp'):
        mito=s['stamp'].upper()=='MITO'
        col=('#C9442B' if mito else '#2F7D52') if THEME=='light' else ('#F0705A' if mito else '#8FD3A6')
        stamp=f'<div class="stamp" style="color:{col};top:{s.get("stampTop",540)}px">{e(s["stamp"])}</div>'
    box=f'<div class="box"><h2>{e(s["boxTitle"])}</h2><p>{e(s["boxText"])}</p>'+(f'<div class="src">{e(s["source"])}</div>' if s.get('source') else '')+'</div>'
    big=' style="font-size:%dpx"'%s['size'] if s.get('size') else ''
    sub=f'<p class="sub">{e(s["sub"])}</p>' if s.get('sub') else ''
    il=art(s.get('art'), 'art-single'+(' left' if s.get('stamp') else ''))
    return [page(top(e(s['label']))+f'<div class="q"{big}>{e(s["statement"])}</div>'+sub+stamp+il+box)]
def carousel(s):
    sl=s['slides']; n=len(sl)+2; out=[]
    out.append(page(top(e(s['label']))+f'<div class="mid"><h1 class="t">{e(s["title"])}</h1><p class="sub">{e(s["subtitle"])}</p><div class="swipe">Arraste para o lado →</div></div>'+art(s.get('art'),'art-cover'),1,n))
    for i,x in enumerate(sl):
        out.append(page(top(e(s['label']))+f'<div class="mid"><div class="num">{i+1:02d}</div><h2 class="h">{e(x["h"])}</h2><p class="txt">{e(x["t"])}</p></div>',i+2,n))
    items=''.join(f'<li>{e(b)}</li>' for b in s['summary'])
    out.append(page(top('Resumo')+f'<div class="mid"><h2 class="h">{e(s["summaryTitle"])}</h2><ul class="l">{items}</ul><p class="disc">Conteúdo informativo, que não substitui a análise de um advogado sobre o seu caso.</p></div>',n,n))
    return out
spec=json.load(open(sys.argv[1],encoding='utf-8')); outdir=sys.argv[2]; os.makedirs(outdir,exist_ok=True)
THEME=spec.get('theme') or ('dark' if spec['kind']=='carousel' else 'light')
pages=single(spec) if spec['kind']=='single' else carousel(spec)
for i,p in enumerate(pages,1):
    open(f'{outdir}/{spec["id"]}-{i}.html','w',encoding='utf-8').write(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{THEME}">{p}</body></html>')
print(len(pages))

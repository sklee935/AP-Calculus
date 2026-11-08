"""Render canonical lesson JSON to editable HTML and deterministic SVG assets."""
from pathlib import Path
import argparse,hashlib,html,json,re,xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]; IG=ROOT/'instagram'
NAVY='#17243b';BLUE='#2463eb';RED='#ce4444';GRAY='#7b8798'
plt.rcParams.update({'svg.hashsalt':'AP-CALCULUS-AB','svg.fonttype':'path','mathtext.fontset':'stix','font.family':'STIXGeneral','font.size':23})

def math_svg(tex):
    # Accept standard TeX single-token fractions as well as braced fractions.
    def braced_fractions(text):
        def atom(pos):
            while pos<len(text) and text[pos].isspace():pos+=1
            start=pos
            if text[pos]=='{':
                depth=1;pos+=1
                while depth:
                    if text[pos]=='{':depth+=1
                    if text[pos]=='}':depth-=1
                    pos+=1
                return text[start:pos],pos
            if text[pos]=='\\':
                pos+=1
                while pos<len(text) and text[pos].isalpha():pos+=1
            else:pos+=1
            return '{'+text[start:pos]+'}',pos
        out='';pos=0
        while pos<len(text):
            if text.startswith('\\frac',pos):
                a,end=atom(pos+5);b,end=atom(end)
                out+='\\frac'+braced_fractions(a)+braced_fractions(b);pos=end
            else:out+=text[pos];pos+=1
        return out
    tex=braced_fractions(tex)
    tex=re.sub(r'\\sqrt\s*([0-9A-Za-z])',r'\\sqrt{\1}',tex)
    tex=re.sub(r'\\ge(?![A-Za-z])',r'\\geq',tex)
    tex=re.sub(r'\\le(?![A-Za-z])',r'\\leq',tex)
    tex=re.sub(r'\\ne(?![A-Za-z])',r'\\neq',tex)
    tex=tex.replace(r'\not\Rightarrow',r'\nRightarrow')
    tex=tex.replace(r'\big|','|')
    key=hashlib.sha256(tex.encode()).hexdigest()[:18]
    path=IG/'assets/math'/f'{key}.svg';path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists():
        math_to_image('$'+tex+'$',str(path),prop=FontProperties(family='STIXGeneral',size=54),format='svg',color=NAVY)
        tree=ET.parse(path);root=tree.getroot()
        for el in list(root.iter()):
            if el.attrib.get('id')=='patch_1':
                for parent in root.iter():
                    if el in list(parent):parent.remove(el);break
        tree.write(path,encoding='utf-8',xml_declaration=True)
        path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    root=ET.parse(path).getroot();box=[float(v) for v in root.attrib['viewBox'].split()]
    return path,box[2],box[3]

def graph_svg(spec):
    key=hashlib.sha256(('graph-style-v2:'+json.dumps(spec,sort_keys=True)).encode()).hexdigest()[:18]
    path=IG/'assets/graphs'/f'{key}.svg';path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():return path
    fig,ax=plt.subplots(figsize=(9.2,3.45),dpi=100)
    fig.patch.set_alpha(0);ax.set_facecolor('none')
    x=sp.Symbol('x',real=True);a,b=spec['xlim'];colors={'blue':BLUE,'red':RED,'gray':GRAY,'navy':NAVY,'gold':'#a56a2b'}
    ax.axhline(0,color='#bcc8d4',lw=1);ax.axvline(0,color='#bcc8d4',lw=1)
    if spec.get('mode')=='slopefield':
        ymin,ymax=spec.get('ylim',[-2,4]);X,Y=np.meshgrid(np.linspace(a,b,14),np.linspace(ymin,ymax,9))
        sy=sp.Symbol('y',real=True);fn=sp.lambdify((x,sy),sp.sympify(spec['slope'],locals={'x':x,'y':sy}),'numpy')
        S=fn(X,Y)+np.zeros_like(X);N=np.sqrt(1+S*S)
        ax.quiver(X,Y,1/N,S/N,angles='xy',pivot='middle',headlength=0,headwidth=0,headaxislength=0,color='#8f9bae',scale=25,width=.0025)
    for c in spec.get('curves',[]):
        lo,hi=c.get('domain',[a,b]);z=np.linspace(lo,hi,600)
        expr=sp.sympify(c['expr'],locals={'x':x})
        with np.errstate(all='ignore'):values=np.asarray(sp.lambdify(x,expr,'numpy')(z))+np.zeros_like(z)
        if spec.get('ylim'):
            bottom,top=spec['ylim'];values=np.where((values<bottom-2*(top-bottom))|(values>top+2*(top-bottom)),np.nan,values)
        ax.plot(z,values,color=colors.get(c.get('color','blue'),BLUE),lw=3.3,label=c.get('label'),ls=c.get('style','-'))
    if spec.get('shade'):
        sh=spec['shade'];z=np.linspace(*sh['interval'],300)
        f=sp.lambdify(x,sp.sympify(sh['top'],locals={'x':x}),'numpy');g=sp.lambdify(x,sp.sympify(sh['bottom'],locals={'x':x}),'numpy')
        ax.fill_between(z,f(z)+np.zeros_like(z),g(z)+np.zeros_like(z),color='#dfeaff',zorder=0)
    for px,py in spec.get('holes',[]):ax.scatter([px],[py],facecolor='#fafbf8',edgecolor=BLUE,s=160,lw=2.8,zorder=6)
    for px,py in spec.get('points',[]):ax.scatter([px],[py],color=RED,s=65,zorder=7)
    for px in spec.get('vlines',[]):ax.axvline(px,color=GRAY,ls='--',lw=1.5)
    ax.set_xlim(a,b)
    if spec.get('ylim'):ax.set_ylim(*spec['ylim'])
    for name in ['top','right']:ax.spines[name].set_visible(False)
    for name in ['left','bottom']:ax.spines[name].set_color('#bcc8d4')
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.tick_params(labelsize=32,colors=NAVY,length=4)
    ax.set_xlabel(spec.get('xlabel','x'),fontsize=32,color=NAVY,labelpad=0)
    if spec.get('ylabel'):ax.set_ylabel(spec['ylabel'],fontsize=32,color=NAVY,rotation=0,labelpad=spec.get('ylabelpad',8))
    if any(c.get('label') for c in spec.get('curves',[])):ax.legend(loc=spec.get('legend','best'),fontsize=30,frameon=False,ncol=2)
    fig.tight_layout(pad=.5);fig.savefig(path,format='svg',transparent=True,metadata={'Date':None});plt.close(fig)
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    return path

def visual_html(spec):
    if not spec:return ''
    if spec['kind']=='graph':
        p=graph_svg(spec);return f'<img class="graph" data-natural-width="662.4" data-natural-height="248.4" data-base-font="30" src="../../assets/graphs/{p.name}" alt="Mathematical graph described in the lesson alt text">'
    if spec['kind']=='table':
        heads=''.join('<th>'+html.escape(str(x))+'</th>' for x in spec['headers'])
        rows=''.join('<tr>'+''.join('<td>'+html.escape(str(c))+'</td>' for c in row)+'</tr>' for row in spec['rows'])
        return f'<table class="values-table"><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table>'
    raise ValueError('Unknown visual kind '+spec['kind'])

def plain_math(tex):
    from latex2mathml.converter import convert
    root=ET.fromstring(convert(tex))
    def rec(el):
        tag=el.tag.rsplit('}',1)[-1];children=list(el)
        if tag=='mfrac':return '('+rec(children[0])+')/('+rec(children[1])+')'
        if tag=='msqrt':return 'sqrt('+''.join(rec(c) for c in children)+')'
        if tag=='msup':return rec(children[0])+'^('+rec(children[1])+')'
        if tag=='msub':return rec(children[0])+'_('+rec(children[1])+')'
        if tag=='msubsup':return rec(children[0])+'_('+rec(children[1])+')^('+rec(children[2])+')'
        return (el.text or '')+''.join(rec(c) for c in children)
    return rec(root)

def build_lesson(path):
    lesson=json.loads(path.read_text());out=IG/'exports'/lesson['id'];out.mkdir(parents=True,exist_ok=True)
    cards=[]
    for slide in lesson['slides']:
        math=[]
        for tex in slide['math']:
            svg,w,h=math_svg(tex);desired=min(900,w*1.45)
            math.append(f'<img class="formula" data-natural-width="{w}" data-natural-height="{h}" data-base-font="54" style="width:{desired:.2f}px" src="../../assets/math/{svg.name}" alt="{html.escape(plain_math(tex),quote=True)}">')
        visual=visual_html(slide.get('visual'))
        desc_en=slide['alt_text']['en'];desc_ko=slide['alt_text']['ko']
        if slide['math']:
            plain='; '.join(plain_math(x) for x in slide['math']);desc_en+=' Math: '+plain;desc_ko+=' 수식: '+plain
        label=f"{lesson['id']} · {slide['number']:02d}/08"
        cards.append(f'''<section class="card {'cover' if slide['number']==1 else ''} {'with-visual' if visual else ''} {'mistake' if slide['number']==7 else ''}" data-slide="{slide['number']}" aria-label="{html.escape(desc_en+' / '+desc_ko,quote=True)}">
<div class="topline"><span>AP CALCULUS AB</span><span>UNIT {lesson['unit']} · LESSON {lesson['number']:02d}</span></div>
<main class="card-content" data-boundary>
<header class="heading"><h1 lang="en">{html.escape(slide['title']['en'])}</h1><h2 lang="ko">{html.escape(slide['title']['ko'])}</h2></header>
<div class="board {'has-visual' if visual else ''}">{''.join(math)}{visual}</div>
<div class="explanation"><p lang="en" class="en">{html.escape(slide['notes']['en'])}</p><p lang="ko" class="ko">{html.escape(slide['notes']['ko'])}</p></div>
</main><footer><span>{'CHECK THE CONDITION' if slide['number']==2 else 'REASON BEFORE RULES'}</span><span>{label}</span></footer>
</section>''')
    source_hash=hashlib.sha256(path.read_bytes()).hexdigest()
    markup=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="lesson-source-sha256" content="{source_hash}"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{lesson['id']} {html.escape(lesson['title']['en'])}</title><link rel="stylesheet" href="../../templates/card.css"></head><body>{''.join(cards)}</body></html>'''
    (out/'lesson.html').write_text(markup)
    caption=lesson['caption']['en']+'\n\n──────────\n\n'+lesson['caption']['ko']+'\n\n#APCalculusAB #Calculus #미적분 #수학공부\n'
    (out/'caption.txt').write_text(caption)
    alt=[]
    for slide in lesson['slides']:
        formulas='; '.join(plain_math(t) for t in slide['math'])
        row={'card':slide['number'],**slide['alt_text']}
        if formulas:row['en']+=' Math: '+formulas;row['ko']+=' 수식: '+formulas
        alt.append(row)
    (out/'alt-text.json').write_text(json.dumps(alt,ensure_ascii=False,indent=2))
    print(lesson['id'],'HTML SVG caption alt-text')

def select_lessons(spec):
    paths=sorted((IG/'lessons').glob('L*.json'))
    if spec=='all':return paths
    wanted=set(spec.split(','));chosen=[p for p in paths if p.stem in wanted]
    assert {p.stem for p in chosen}==wanted,('Unknown lesson selection',spec)
    return chosen

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--lessons',default='all');args=parser.parse_args()
    paths=select_lessons(args.lessons);assert paths,'No matching lesson JSON'
    for path in paths:build_lesson(path)

"""Read-only checks of bilingual scripts, source links, math, captions and exports."""
from pathlib import Path
import argparse,ast,hashlib,json,re
import sympy as sp
from PIL import Image

ROOT=Path(__file__).resolve().parents[2];IG=ROOT/'instagram'
x,y,t,h=sp.symbols('x y t h',real=True)
ENV={k:getattr(sp,k) for k in ['limit','diff','integrate','solve','simplify','factor','expand','sin','cos','tan','sec','asin','acos','atan','exp','log','sqrt','Abs','Rational','Integer','pi','oo']}
ENV.update(x=x,y=y,t=t,h=h,min=min,max=max)
ALLOWED=(ast.Expression,ast.Constant,ast.Name,ast.Load,ast.Call,ast.Attribute,ast.Subscript,ast.BinOp,ast.UnaryOp,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow,ast.USub,ast.UAdd,ast.List,ast.Tuple,ast.Dict,ast.keyword,ast.Compare,ast.Eq,ast.NotEq,ast.Gt,ast.Lt,ast.GtE,ast.LtE)

def calc(text):
    tree=ast.parse(str(text),mode='eval')
    for node in ast.walk(tree):
        assert isinstance(node,ALLOWED),('Unsupported math expression node',type(node).__name__)
        if isinstance(node,ast.Name):assert node.id in ENV,('Unknown math name',node.id)
        if isinstance(node,ast.Attribute):assert node.attr=='subs','Only substitution attributes are permitted'
    return sp.sympify(eval(compile(tree,'<lesson-math>','eval'),{'__builtins__':{}},ENV))

def equivalent(a,b):
    if a==b:return True
    if a in (sp.oo,-sp.oo) or b in (sp.oo,-sp.oo):return False
    d=sp.simplify(a-b)
    return d==0 or (not d.free_symbols and bool(d.is_finite) and abs(float(d.evalf(30)))<1e-10)

def validate(selection='all',exports=False,complete=False):
    course=json.loads((IG/'course.json').read_text());meta=course['lessons'];assert len(meta)==60
    assert [m['id'] for m in meta]==[f'L{n:02d}' for n in range(1,61)]
    assert [sum(m['unit']==u for m in meta) for u in range(1,9)]==[8,8,6,6,8,10,6,8]
    for i,m in enumerate(meta):assert m['week']==i//3+1 and m['day']==['Monday','Wednesday','Friday'][i%3]
    bank={q['source_id'] if 'source_id' in q else q['id']:q for q in json.loads((ROOT/'ap-calculus-ab/content/question_bank.json').read_text())['questions']}
    paths=sorted((IG/'lessons').glob('L*.json'))
    if selection!='all':
        requested=set(selection.split(','));paths=[p for p in paths if p.stem in requested]
        assert {p.stem for p in paths}==requested,('Unknown lesson selection',selection)
    assert paths,'No lesson scripts found'
    if complete:assert len(paths)==60,('Expected complete course',len(paths))
    checks=0;pngs=0
    css_hash=hashlib.sha256((IG/'templates/card.css').read_bytes()).hexdigest()
    for path in paths:
        d=json.loads(path.read_text());m=meta[d['number']-1]
        assert d['id']==m['id'] and d['unit']==m['unit'] and d['title']==m['title']
        assert d['prerequisites']==m['prerequisites']
        assert len(d['slides'])==8 and [s['number'] for s in d['slides']]==list(range(1,9))
        for ref in d['source_question_ids']:assert ref in bank,(d['id'],'unknown source',ref)
        assert len(d['verification'])>=2
        for v in d['verification']:
            a=calc(v['expression']);b=calc(v['expected']);assert equivalent(a,b),(d['id'],v,a,b);checks+=1
        for s in d['slides']:
            assert isinstance(s['math'],list) and all(isinstance(tex,str) and tex.strip() for tex in s['math']),(d['id'],'invalid formula list')
            for key in ['title','notes','alt_text']:
                assert set(s[key])=={'en','ko'} and all(s[key].values()),(d['id'],s['number'],key)
            assert re.search('[가-힣]',s['title']['ko']+s['notes']['ko'])
            assert not any(c in s['notes']['en']+s['notes']['ko'] for c in ['\ufffd','□','❑'])
            assert s['math'] or s.get('visual'),(d['id'],s['number'],'mathematical content missing')
            if s.get('visual') and s['visual']['kind']=='table':
                assert all(len(row)==len(s['visual']['headers']) for row in s['visual']['rows'])
            if s.get('visual') and s['visual']['kind']=='graph':
                v=s['visual']
                for px,py in v.get('holes',[]):
                    assert any(equivalent(sp.sympify(c['expr'],locals=ENV).subs(x,sp.Rational(str(px))),sp.Rational(str(py))) for c in v['curves']),(d['id'],'hole not on nearby curve')
        assert d['slides'][7]['math']==d['self_check']['math']
        assert all(d['self_check']['answer'][lang] in d['caption'][lang] for lang in ['en','ko'])
        assert len(d['caption']['en']+d['caption']['ko'])<2100,(d['id'],'caption too long')
        if exports:
            folder=IG/'exports'/d['id'];manifest=json.loads((folder/'manifest.json').read_text())
            assert manifest['source_sha256']==hashlib.sha256(path.read_bytes()).hexdigest(),(d['id'],'stale lesson export')
            assert manifest['css_sha256']==css_hash,(d['id'],'stale styling')
            assert manifest['cards']==8 and manifest['overflow'] is False
            for n in range(1,9):
                im=folder/f'{n:02d}.png'
                with Image.open(im) as image:assert image.size==(1080,1350) and image.mode in ('RGB','RGBA')
                assert hashlib.sha256(im.read_bytes()).hexdigest()==manifest['png_sha256'][f'{n:02d}.png']
                pngs+=1
            alt=json.loads((folder/'alt-text.json').read_text());assert len(alt)==8
            for s,a in zip(d['slides'],alt):
                assert a['card']==s['number'] and all(s['alt_text'][lang] in a[lang] for lang in ['en','ko'])
            caption=(folder/'caption.txt').read_text()
            assert len(caption)<=2200 and all(d['caption'][lang] in caption for lang in ['en','ko'])
    result={'lessons':len(paths),'slides':len(paths)*8,'math_checks':checks,'pngs':pngs,'read_only':True}
    print(json.dumps(result,ensure_ascii=False));return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--lessons',default='all');parser.add_argument('--exports',action='store_true');parser.add_argument('--complete',action='store_true');a=parser.parse_args();validate(a.lessons,a.exports,a.complete)

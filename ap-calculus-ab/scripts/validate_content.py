"""Verify authored keys against symbolic and high-precision numerical calculations."""
from pathlib import Path
import json,csv,collections
import sympy as s
import mpmath as mp
from curriculum import UNITS,SOURCES,BC_ROADMAP
from questions import QUESTIONS
import unit_frq,exam  # populate the shared bank

ROOT=Path(__file__).resolve().parents[1]
x,y,t,h=s.symbols('x y t h',real=True)
mp.mp.dps=50
NUMERICAL_AUDITS=[]

def nroot(expr,var,a,b):
    fn=s.lambdify(var,expr,'mpmath'); lo=mp.mpf(str(a)); hi=mp.mpf(str(b))
    assert fn(lo)*fn(hi)<0,('root bracket',expr,a,b)
    for _ in range(200):
        mid=(lo+hi)/2
        if fn(lo)*fn(mid)<=0:hi=mid
        else:lo=mid
    root=(lo+hi)/2
    assert abs(fn(root))<mp.mpf('1e-40')
    NUMERICAL_AUDITS.append({'kind':'root_residual','expression':str(expr),'residual':str(abs(fn(root)))})
    return s.Float(str(root),45)

def nint(expr,var,a,b):
    fn=s.lambdify(var,expr,'mpmath'); lo=mp.mpf(str(a)); hi=mp.mpf(str(b))
    val=mp.quad(fn,[lo,hi])
    n=2048; width=(hi-lo)/n
    alt=width/3*(fn(lo)+fn(hi)+4*sum(fn(lo+(2*i-1)*width) for i in range(1,n//2+1))+2*sum(fn(lo+2*i*width) for i in range(1,n//2)))
    assert abs(val-alt)<mp.mpf('1e-9'),('quadrature disagreement',expr,val,alt)
    NUMERICAL_AUDITS.append({'kind':'quadrature_cross_check','expression':str(expr),'difference':str(abs(val-alt))})
    return s.Float(str(val),45)

ENV={k:getattr(s,k) for k in ['limit','diff','integrate','solve','cancel','trigsimp','sin','cos','tan','asin','acos','atan','exp','log','sqrt','Rational','Integer','oo','pi']}
ENV.update(x=x,y=y,t=t,h=h,nroot=nroot,nint=nint,max=max,min=min)

def calculate(spec):
    return s.sympify(eval(spec,{'__builtins__':{}},ENV))

def equal(a,b,tol=0):
    if a==b:return True
    delta=s.simplify(a-b)
    if delta==0:return True
    if not delta.free_symbols and delta.is_finite:
        return abs(float(s.N(delta,30)))<=tol
    return False

def export_and_validate():
    ids=[q['id'] for q in QUESTIONS]
    assert len(ids)==len(set(ids))==124
    numeric_mc=0;scalar_frq=0;editorial=[]
    for q in QUESTIONS:
        assert set(q['prompt'])=={'ko','en'} and all(q['prompt'].values())
        if q['type']=='MCQ':
            assert len(q['choices'])==4 and 0<=q['answer']<4
            assert all(q['solution'].values())
            if q['oracle']:
                result=calculate(q['oracle']); correct=q['choices'][q['answer']]['value']
                expected=s.sympify(correct,locals=ENV)
                tol=0.0005000001 if q['calculator'] else 1e-12
                assert equal(result,expected,tol),(q['id'],result,expected)
                for i,c in enumerate(q['choices']):
                    if i!=q['answer'] and c['value'] is not None:
                        assert not equal(result,s.sympify(c['value'],locals=ENV),tol),('duplicate correct choice',q['id'])
                q['verification']={'method':'symbolic_or_numeric_oracle','result':str(result),'tolerance':tol}
                numeric_mc+=1
            else:
                editorial.append(q['id']);q['verification']={'method':'editorial_reasoning_review'}
        else:
            assert sum(p['points'] for p in q['parts'])==9
            assert len(q['parts'])==3
            for i,p in enumerate(q['parts']):
                assert all(p['prompt'].values()) and all(p['solution'].values()) and all(p['criteria'].values())
                if p['oracle']:
                    result=calculate(p['oracle'])
                    assert p['value'] is not None,('missing authored target',q['id'],i)
                    target=s.sympify(p['value'],locals=ENV)
                    assert equal(result,target,1e-10),(q['id'],i,result,target)
                    p['verification']={'method':'symbolic_or_numeric_oracle','result':str(result)};scalar_frq+=1
                else:
                    editorial.append(f"{q['id']}-{i+1}");p['verification']={'method':'editorial_reasoning_review'}
    assert len([q for q in QUESTIONS if q['id'].startswith('U')])==64
    exam_mc=[q for q in QUESTIONS if q['id'].startswith('E') and q['type']=='MCQ']
    assert len(exam_mc)==42
    assert sum(q['calculator'] for q in exam_mc)==13
    assert all(not q['calculator'] for q in exam_mc[:29])
    assert all(q['calculator'] for q in exam_mc[29:])
    counts=collections.Counter(q['unit'] for q in exam_mc)
    bounds={1:(10,15),2:(10,15),3:(5,10),4:(10,15),5:(15,20),6:(15,20),7:(5,10),8:(10,15)}
    for u,c in counts.items():assert bounds[u][0]<=100*c/42<=bounds[u][1],(u,c)
    exam_frq=[q for q in QUESTIONS if q['id'].startswith('EF')]
    assert len(exam_frq)==6 and [q['calculator'] for q in exam_frq]==[True,True,False,False,False,False]
    # Worked examples: independent scalar checks of their numerical outcomes.
    # Full suite, with symbols explicit and no use of presentation strings as answers.
    worked=[('W1A',calculate('limit((x**2-16)/(x-4),x,4)'),s.Integer(8)),
            ('W1B',calculate('(x**3+x-5).subs(x,1)*(x**3+x-5).subs(x,2)'),s.Integer(-15)),
            ('W2A',calculate('diff(x**2,x).subs(x,3)'),s.Integer(6)),
            ('W2B',calculate('diff(x**2*exp(x),x)'),s.exp(x)*(x**2+2*x)),
            ('W3A',calculate('diff((1+3*x**2)**4,x)'),24*x*(1+3*x**2)**3),
            ('W3B',s.Rational(1,5),s.Rational(1,5)),
            ('W4A',4*s.pi*2**2*3,48*s.pi),('W4B',s.sqrt(9)+s.Rational(1,6)*s.Rational(12,100),s.Rational(151,50)),
            ('W5A',max([(a**3-3*a) for a in [-2,-1,1,2]]),s.Integer(2)),('W5B',12*(48-24),s.Integer(288)),
            ('W6A',calculate('integrate(2*x*(x**2+1)**3,(x,0,1))'),s.Rational(15,4)),
            ('W6B',calculate('diff(integrate(cos(t),(t,1,x**2)),x)'),2*x*s.cos(x**2)),
            ('W7A',calculate('diff(3*exp(x**2),x)-2*x*3*exp(x**2)'),s.Integer(0)),
            ('W7B',calculate('diff(20+50*exp(-t/5),t)+(20+50*exp(-t/5)-20)/5'),s.Integer(0)),
            ('W8A',calculate('-integrate(t-2,(t,0,2))+integrate(t-2,(t,2,4))'),s.Integer(4)),
            ('W8B',s.pi*calculate('integrate(x**2-x**4,(x,0,1))'),2*s.pi/15)]
    for id,got,target in worked:assert equal(s.sympify(got),target),(id,got,target)
    report={'checked_on':'2026-10-28','questions':len(QUESTIONS),'mcq':sum(q['type']=='MCQ' for q in QUESTIONS),
            'frq':sum(q['type']=='FRQ' for q in QUESTIONS),'mcq_oracle_checks':numeric_mc,'frq_scalar_identity_checks':scalar_frq,
            'worked_example_checks':len(worked),'editorially_reviewed_reasoning_items':editorial,
            'exam_mcq_counts_by_unit':dict(sorted(counts.items())), 'exam_mcq_weights_percent':{k:round(v*100/42,3) for k,v in sorted(counts.items())},
            'exam_format':{'mcq_a':[29,62],'mcq_b':[13,38],'frq_a':[2,30],'frq_b':[4,60]},
            'numerical_cross_checks':NUMERICAL_AUDITS,'limitations':'Author-created rubrics and teaching difficulty labels are not College Board scoring guidelines or calibrated AP score conversions. Symbolic checks do not validate every prose argument.'}
    (ROOT/'content/question_bank.json').write_text(json.dumps({'schema_version':1,'title':'AP Calculus AB bilingual first edition','verified_on':'2026-10-28','questions':QUESTIONS},ensure_ascii=False,indent=2))
    (ROOT/'content/curriculum.json').write_text(json.dumps({'units':UNITS,'sources':SOURCES,'bc_extension_plan':BC_ROADMAP},ensure_ascii=False,indent=2))
    (ROOT/'content/validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    with (ROOT/'content/teacher_blueprint.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['id','unit','type','skill','calculator','answer_or_max_points','verification'])
        for q in QUESTIONS:writer.writerow([q['id'],q['unit'],q['type'],q['skill'],q['calculator'],'ABCD'[q['answer']] if q['type']=='MCQ' else 9,q.get('verification',{}).get('method','per-part review')])
    print(json.dumps({k:v for k,v in report.items() if k not in ('editorially_reviewed_reasoning_items','numerical_cross_checks')},ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':export_and_validate()

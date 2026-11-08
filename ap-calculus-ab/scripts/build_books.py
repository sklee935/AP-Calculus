"""Build three editable DOCX books and browser-readable sources from one question bank."""
from pathlib import Path
import copy,json,re,collections,csv,zipfile,uuid
import sympy as s
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement,parse_xml
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from latex2mathml.converter import convert as latex_to_mathml
import mathml2omml
from curriculum import UNITS,SOURCES,BC_ROADMAP,bi
from validate_content import export_and_validate,ENV
from questions import QUESTIONS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables';ASSETS=ROOT/'assets'
FONT='Noto Sans CJK KR'; MATHFONT='Cambria Math'
MATH_CACHE={}

def fmt(expr):
    return '$'+s.latex(s.sympify(expr,locals=ENV))+'$'

def choice_text(c,lang):return c['text'][lang] if 'text' in c else fmt(c['value'])

def setfont(run,size=None,bold=None,color='000000'):
    run.font.name=FONT
    rp=run._element.get_or_add_rPr();rf=rp.get_or_add_rFonts()
    for name in ['ascii','hAnsi','eastAsia','cs']:rf.set(qn('w:'+name),FONT)
    run.font.color.rgb=RGBColor.from_string(color)
    if size:run.font.size=Pt(size)
    if bold is not None:run.bold=bold

def math_element(tex):
    if tex not in MATH_CACHE:
        ml=latex_to_mathml(tex)
        xml=mathml2omml.convert(ml)
        xml=xml.replace('<m:oMath>','<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">',1)
        el=parse_xml(xml)
        # The converter adds presentation boxes around every mrow. Unwrap them
        # for interoperability with headless Office renderers.
        for box in reversed(list(el.iter(qn('m:box')))):
            parent=box.getparent();index=parent.index(box);content=box.find(qn('m:e'))
            if content is not None:
                for child in list(content):parent.insert(index,child);index+=1
            parent.remove(box)
        # A limit must be a function object with an operand. Otherwise LibreOffice
        # imports the word 'lim' as an incomplete command and paints placeholders.
        for sub in list(el.iter(qn('m:sSub'))):
            base=sub.find(qn('m:e'))
            if base is None or ''.join(base.itertext())!='lim':continue
            parent=sub.getparent();idx=parent.index(sub)
            fun=OxmlElement('m:func');name=OxmlElement('m:fName');low=OxmlElement('m:limLow')
            e=OxmlElement('m:e')
            for child in list(base):e.append(child)
            low.append(e);limit=OxmlElement('m:lim')
            for child in list(sub.find(qn('m:sub'))):limit.append(child)
            low.append(limit);name.append(low);fun.append(name);body=OxmlElement('m:e')
            siblings=list(parent)[idx+1:]
            for sibling in siblings:
                if sibling.tag==qn('m:r') and ''.join(sibling.itertext()) in ['=','<','>','≤','≥','⇒']:break
                if sibling.tag==qn('m:sSub') and ''.join(sibling.find(qn('m:e')).itertext())=='lim':break
                body.append(sibling)
            fun.append(body);parent.replace(sub,fun)
        # Square roots require an explicit hidden degree field in interoperable
        # OMML. The upstream converter omits both the property and the field.
        for rad in el.iter(qn('m:rad')):
            if rad.find(qn('m:deg')) is None:
                pr=OxmlElement('m:radPr');hide=OxmlElement('m:degHide');hide.set(qn('m:val'),'1');pr.append(hide)
                rad.insert(0,pr);rad.insert(1,OxmlElement('m:deg'))
        for r in el.iter(qn('m:r')):
            wr=OxmlElement('w:rPr');fonts=OxmlElement('w:rFonts')
            fonts.set(qn('w:ascii'),MATHFONT);fonts.set(qn('w:hAnsi'),MATHFONT)
            wr.append(fonts);sz=OxmlElement('w:sz');sz.set(qn('w:val'),'21');wr.append(sz);r.insert(0,wr)
        MATH_CACHE[tex]=el
    return copy.deepcopy(MATH_CACHE[tex])

def embed_font(path):
    """Embed an OFL-licensed CJK font, avoiding system font dependencies."""
    from lxml import etree
    font=ASSETS/'fonts/NotoSansCJKkr-BookSubset.otf'
    if not font.exists():
        from fontTools import subset
        chars=set()
        for p in (ROOT/'scripts').glob('*.py'):chars.update(p.read_text())
        for p in (ROOT/'content').glob('*.json'):chars.update(p.read_text())
        chars.update(''.join(chr(i) for i in range(32,127)))
        options=subset.Options();options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
        ft=subset.load_font(str(ASSETS/'fonts/NotoSansCJKkr-Regular.otf'),options)
        sub=subset.Subsetter(options=options);sub.populate(text=''.join(chars));sub.subset(ft);subset.save_font(ft,str(font),options)
    with zipfile.ZipFile(path) as z:data={n:z.read(n) for n in z.namelist()}
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
    key=uuid.UUID('c5c041cd-5824-49a5-aa48-ded7e4b33df8');mask=key.bytes[::-1]
    blob=bytearray(font.read_bytes())
    for i in range(32):blob[i]^=mask[i%16]
    docfont=etree.Element(qn('w:font'),nsmap=ns);docfont.set(qn('w:name'),FONT)
    em=etree.SubElement(docfont,qn('w:embedRegular'));em.set(qn('r:id'),'rIdAPFont');em.set(qn('w:fontKey'),'{'+str(key).upper()+'}');em.set(qn('w:subsetted'),'1')
    fonttable=etree.fromstring(data['word/fontTable.xml']);fonttable.append(docfont);data['word/fontTable.xml']=etree.tostring(fonttable,xml_declaration=True,encoding='UTF-8',standalone=True)
    relns='http://schemas.openxmlformats.org/package/2006/relationships'
    relpath='word/_rels/fontTable.xml.rels'
    rels=etree.fromstring(data[relpath]) if relpath in data else etree.Element('{'+relns+'}Relationships',nsmap={None:relns})
    rel=etree.SubElement(rels,'{'+relns+'}Relationship');rel.set('Id','rIdAPFont');rel.set('Type',ns['r']+'/font');rel.set('Target','fonts/APNoto.odttf');data[relpath]=etree.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
    data['word/fonts/APNoto.odttf']=bytes(blob)
    ctns='http://schemas.openxmlformats.org/package/2006/content-types';cts=etree.fromstring(data['[Content_Types].xml'])
    ct=etree.SubElement(cts,'{'+ctns+'}Default');ct.set('Extension','odttf');ct.set('ContentType','application/vnd.openxmlformats-officedocument.obfuscatedFont');data['[Content_Types].xml']=etree.tostring(cts,xml_declaration=True,encoding='UTF-8',standalone=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for n,v in data.items():z.writestr(n,v)

def save_book(doc,path):doc.save(path);embed_font(path)

def rich(p,value,size=10.5,bold=False,color='000000'):
    assert value.count('$')%2==0,('unpaired math delimiter',value)
    for i,piece in enumerate(re.split(r'\$([^$]+)\$',value)):
        if i%2:
            # Standalone exponents after units belong to the preceding text run,
            # rather than to an Office equation with a missing base placeholder.
            if re.fullmatch(r'\^[0-9]+',piece):
                run=p.add_run(piece[1:]);setfont(run,size,bold,color);run.font.superscript=True
                continue
            try:p._p.append(math_element(piece))
            except Exception as e:raise ValueError(f'Math conversion failed: {piece}') from e
        elif piece:setfont(p.add_run(piece),size,bold,color)
    return p

def para(doc,text='',style=None,size=None,bold=None,color='000000'):
    sizes={'Title':27,'Heading 1':20,'Heading 2':13,'Heading 3':11}
    if size is None:size=sizes.get(style,10.5)
    if bold is None:bold=style in sizes
    return rich(doc.add_paragraph(style=style),text,size,bold,color)

def newpage(doc,title,subtitle=None):
    p=doc.add_paragraph(style='Heading 1')
    p.paragraph_format.page_break_before=len(doc.paragraphs)>1
    rich(p,title,20,True)
    if subtitle:para(doc,subtitle,size=9.5,color='555555')

def field(p,code):
    run=p.add_run();f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),code);run._r.addnext(f)

def setup(lang,teacher=False):
    d=Document();sec=d.sections[0]
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=sec.bottom_margin=Inches(.67)
    sec.left_margin=sec.right_margin=Inches(.73)
    sec.header_distance=Inches(.28);sec.footer_distance=Inches(.3)
    for name,size,bold in [('Normal',10.5,False),('Title',27,True),('Heading 1',20,True),('Heading 2',13,True),('Heading 3',11,True)]:
        st=d.styles[name];st.font.name=FONT;st.font.size=Pt(size);st.font.bold=bold;st.font.color.rgb=RGBColor(0,0,0)
        rf=st.element.get_or_add_rPr().get_or_add_rFonts()
        for k in ['ascii','hAnsi','eastAsia','cs']:rf.set(qn('w:'+k),FONT)
        for attr in list(rf.attrib):
            if 'theme' in attr.lower():del rf.attrib[attr]
        for border in list(st.element.findall('.//'+qn('w:pBdr'))):border.getparent().remove(border)
        pf=st.paragraph_format;pf.line_spacing=1.12;pf.space_after=Pt(6)
        if name.startswith('Heading'):pf.keep_with_next=True;pf.space_before=Pt(9)
    d.styles['Normal'].paragraph_format.widow_control=True
    mathpr=OxmlElement('m:mathPr');mf=OxmlElement('m:mathFont');mf.set(qn('m:val'),MATHFONT);mathpr.append(mf);d.settings.element.append(mathpr)
    hp=sec.header.paragraphs[0];rich(hp,'AP CALCULUS AB     '+('교사용 해설서' if teacher else ('한글판 학생용 교재' if lang=='ko' else 'STUDENT EDITION')),8.5,color='555555')
    foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    rich(foot,'2027 준비   |   ' if lang=='ko' else '2027 preparation   |   ',8,color='555555');field(foot,'PAGE')
    d.core_properties.title='AP Calculus AB '+('Teacher Guide' if teacher else ('Korean Student Book' if lang=='ko' else 'English Student Book'))
    d.core_properties.subject='Original bilingual calculus teaching materials'
    d.core_properties.author='';d.core_properties.keywords='AP Calculus AB, original practice, bilingual'
    return d

def table(doc,headers,rows,widths=None):
    tab=doc.add_table(rows=1,cols=len(headers));tab.alignment=WD_TABLE_ALIGNMENT.CENTER;tab.autofit=False
    widths=widths or [7.04/len(headers)]*len(headers)
    for i,w in enumerate(widths):tab.columns[i].width=Inches(w)
    for i,h in enumerate(headers):rich(tab.rows[0].cells[i].paragraphs[0],str(h),9,True)
    for row in rows:
        cells=tab.add_row().cells
        for i,v in enumerate(row):rich(cells[i].paragraphs[0],str(v),9)
    for ri,row in enumerate(tab.rows):
        trpr=row._tr.get_or_add_trPr();cs=OxmlElement('w:cantSplit');trpr.append(cs)
        if ri==0:
            repeat=OxmlElement('w:tblHeader');trpr.append(repeat)
        for i,cell in enumerate(row.cells):
            cell.width=Inches(widths[i]);cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            pr=cell._tc.get_or_add_tcPr();borders=OxmlElement('w:tcBorders')
            for edge in ['top','left','bottom','right','insideH','insideV']:
                el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
            pr.append(borders);margins=OxmlElement('w:tcMar')
            for k in ['top','left','bottom','right']:
                el=OxmlElement('w:'+k);el.set(qn('w:w'),'70');el.set(qn('w:type'),'dxa');margins.append(el)
            pr.append(margins)
            if ri==0:
                shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'DDE8F0');pr.append(shade)
            for p in cell.paragraphs:p.paragraph_format.space_after=Pt(3);p.paragraph_format.space_before=Pt(3)
    para(doc,'',size=3).paragraph_format.space_after=Pt(2)
    return tab

def figures():
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160})
    for key in ['accumulation','hole','derivative','area','slopefield','tangent','inverse','motion']:
        fig,ax=plt.subplots(figsize=(6.3,2.35));ax.axhline(0,color='#888888',lw=.6);ax.axvline(0,color='#888888',lw=.6)
        if key=='accumulation':
            ax.plot([0,1,3,4],[0,2,0,-2],color='#1e4c66',lw=2);ax.scatter([0,1,3,4],[0,2,0,-2],color='#1e4c66',s=20)
            ax.set(xticks=range(5),yticks=range(-2,3),ylim=(-2.5,2.6),xlim=(-.3,4.4),ylabel='f(x)',xlabel='x')
        elif key=='hole':
            ax.plot([-1,1,3],[0,2,0],color='#1e4c66',lw=2);ax.scatter([1],[2],facecolor='white',edgecolor='#1e4c66',s=65,zorder=5);ax.scatter([1],[4],color='#1e4c66',s=38)
            ax.set(xticks=range(-1,4),yticks=range(5),xlim=(-1.3,3.3),ylim=(-.3,4.5),xlabel='x',ylabel='g(x)')
        elif key=='derivative':
            ax.plot([0,1,3,4],[0,2,-2,0],color='#1e4c66',lw=2);ax.scatter([0,1,3,4],[0,2,-2,0],color='#1e4c66',s=20)
            ax.set(xticks=range(5),yticks=range(-2,3),xlabel='x',ylabel="f '(x)",xlim=(-.3,4.3),ylim=(-2.5,2.5))
        elif key=='area':
            z=np.linspace(0,1,200);ax.plot(z,z,label='y = x',color='#1e4c66');ax.plot(z,z*z,label='y = x²',color='#9b603d');ax.fill_between(z,z*z,z,color='#d7e4eb');ax.legend(loc='upper left',frameon=False)
            ax.set(xlim=(-.1,1.1),ylim=(-.1,1.1),xlabel='x',ylabel='y')
        elif key=='slopefield':
            X,Y=np.meshgrid(np.linspace(-1.5,1.5,13),np.linspace(-.2,4,12));S=X*(Y-1);N=np.sqrt(1+S*S)
            ax.quiver(X,Y,1/N,S/N,angles='xy',pivot='middle',headlength=0,headwidth=0,headaxislength=0,color='#7c8790',scale=24,width=.002)
            z=np.linspace(-1.2,1.2,120);ax.plot(z,1+2*np.exp(z*z/2),color='#1e4c66',lw=2)
            ax.set(xlim=(-1.6,1.6),ylim=(-.3,4.4),xlabel='x',ylabel='y',title="y' = x(y - 1)")
        elif key=='tangent':
            z=np.linspace(-.5,3.5,200);ax.plot(z,z*z,color='#1e4c66',label='f(x) = x²');ax.plot(z,4*z-4,color='#9b603d',ls='--',label='tangent at x = 2');ax.scatter([2],[4],color='#1e4c66');ax.legend(frameon=False,loc='upper left');ax.set(xlabel='x',ylabel='y',ylim=(-2,12))
        elif key=='inverse':
            z=np.linspace(-1.4,1.4,200);w=z**3+z;ax.plot(z,w,label='f',color='#1e4c66');ax.plot(w,z,label='inverse',color='#9b603d');ax.plot([-4,4],[-4,4],ls='--',color='#888888',lw=.7);ax.legend(frameon=False);ax.set(xlim=(-4,4),ylim=(-4,4),xlabel='x',ylabel='y')
        elif key=='motion':
            z=np.linspace(0,4,200);ax.plot(z,3*z*z-12*z+9,color='#1e4c66',label='velocity');ax.plot(z,6*z-12,color='#9b603d',label='acceleration');ax.legend(frameon=False);ax.set(xlabel='t',ylabel='rate',xlim=(0,4))
        fig.tight_layout(pad=.6);fig.savefig(ASSETS/f'{key}.png',dpi=220);plt.close(fig)

def image(doc,name,width=5.15):
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    run=p.add_run();run.add_picture(str(ASSETS/f'{name}.png'),width=Inches(width))
    p.paragraph_format.space_after=Pt(5)
    drawing=run._r.xpath('.//wp:docPr')[0];drawing.set('descr',f'Original mathematical diagram {name}; coordinates and labels are shown on axes.')

def data_table(doc,data):
    if data:table(doc,data['headers'],data['rows'])

def sources_page(doc,lang):
    newpage(doc,'출처와 BC 확장 계획' if lang=='ko' else 'Sources and the BC extension plan')
    para(doc,'공식 범위 확인일 2026년 10월 28일' if lang=='ko' else 'Official framework checked October 28 2026',size=9.5)
    for src in SOURCES:
        para(doc,src['title'],bold=True)
        # Native hyperlinks keep long URLs from disrupting page layout.
        p=doc.add_paragraph();hlink=OxmlElement('w:hyperlink')
        rid=doc.part.relate_to(src['url'],'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True);hlink.set(qn('r:id'),rid)
        run=OxmlElement('w:r');rp=OxmlElement('w:rPr');color=OxmlElement('w:color');color.set(qn('w:val'),'1E4C66');rp.append(color);run.append(rp);txt=OxmlElement('w:t');txt.text='College Board 공식 자료 열기' if lang=='ko' else 'Open the official College Board source';run.append(txt);hlink.append(run);p._p.append(hlink)
    para(doc,'BC로 확장하는 순서' if lang=='ko' else 'Sequence for the BC extension',style='Heading 2')
    for i,item in enumerate(BC_ROADMAP):para(doc,str(i+1)+'. '+item[lang],size=10)

def reference_pages(doc,lang):
    newpage(doc,'미분과 적분 공식 점검' if lang=='ko' else 'Derivative and integral reference')
    para(doc,bi('공식은 정의역과 함께 사용한다. 아래 식에서 각도는 라디안이며, 적분상수는 C이다. 합성함수에서는 연쇄법칙이나 치환을 추가로 적용한다.','Use each formula on its valid domain. Angles are radians and C is an integration constant. Compositions require an additional chain factor or substitution.')[lang])
    formulas=[r'(x^n)\prime=nx^{n-1}',r'(\ln|x|)\prime=\frac1x\quad(x\ne0)',r'(a^x)\prime=a^x\ln a\quad(a>0)',
              r'(\tan x)\prime=\sec^2x,\quad(\cot x)\prime=-\csc^2x',r'(\sec x)\prime=\sec x\tan x,\quad(\csc x)\prime=-\csc x\cot x',
              r'(\arcsin x)\prime=\frac1{\sqrt{1-x^2}},\quad(\arctan x)\prime=\frac1{1+x^2}',
              r'\int x^n\,dx=\frac{x^{n+1}}{n+1}+C\quad(n\ne-1)',r'\int\frac1x\,dx=\ln|x|+C',
              r'\int e^x\,dx=e^x+C,\quad\int\cos x\,dx=\sin x+C',r'\int\sin x\,dx=-\cos x+C',
              r'\int\frac{1}{1+x^2}\,dx=\arctan x+C',r'\int\frac1{\sqrt{1-x^2}}\,dx=\arcsin x+C']
    for f in formulas:para(doc,'$'+f+'$')
    newpage(doc,'수업에서 사용하는 한영 용어' if lang=='ko' else 'Bilingual calculus vocabulary')
    table(doc,['English','한국어'],[
        ['limit / one-sided limit','극한 / 한쪽 극한'],['continuity / differentiability','연속성 / 미분가능성'],['derivative / second derivative','도함수 / 둘째 도함수'],
        ['average rate / instantaneous rate','평균변화율 / 순간변화율'],['tangent line / linearization','접선 / 선형근사'],['implicit / inverse function','음함수 / 역함수'],
        ['critical number / local extremum','임계수 / 극값'],['absolute maximum and minimum','절대최댓값과 절대최솟값'],['concavity / inflection point','오목성 / 변곡점'],
        ['mean value theorem','평균값정리'],['extreme value theorem','최대최소정리'],['intermediate value theorem','중간값정리'],['antiderivative / definite integral','원시함수 / 정적분'],
        ['accumulation / net change','누적 / 순변화'],['Riemann sum / trapezoidal sum','리만합 / 사다리꼴합'],['fundamental theorem of calculus','미적분의 기본정리'],
        ['slope field / equilibrium solution','기울기장 / 평형해'],['separation of variables','변수분리'],['displacement / total distance','변위 / 총 이동거리'],['cross section / washer','단면 / 와셔']],widths=[4,3.04])

def intro(doc,lang,teacher=False):
    p=doc.add_paragraph(style='Title');rich(p,'AP Calculus AB',27,True)
    para(doc,('교사용 해설과 채점기준' if teacher else ('개념과 문제풀이 한글판' if lang=='ko' else 'Concepts and practice English edition')),style='Heading 1')
    para(doc,'2027 시험 대비 초판' if lang=='ko' else 'First edition for the 2027 exam',size=12,bold=True)
    opening=bi('이 교재는 미적분을 배우고 AP Calculus AB 시험을 준비하는 고등학생과 이를 지도하는 교사를 위한 자체 제작 자료이다. 여덟 단원을 짧은 개념 설명과 예제로 배우고, 연습문제에서 풀이를 설명한 뒤 실전 시간에 맞춰 적용하도록 구성했다.','This independently authored book supports high-school students learning calculus and teachers preparing them for AP Calculus AB. Learn through concise notes and worked examples, explain reasoning in unit practice, and then apply those skills under exam timing.')
    para(doc,opening[lang])
    table(doc,['구성','수량'] if lang=='ko' else ['Component','Count'],[
        ['개념 단원과 해설 예제' if lang=='ko' else 'Units and worked examples','8 / 16'],
        ['선수학습 진단 객관식' if lang=='ko' else 'Prerequisite diagnostic MCQ','12'],
        ['단원 연습 객관식과 서술형' if lang=='ko' else 'Unit practice MCQ and FRQ','48 / 16'],
        ['실전 모의고사 객관식과 서술형' if lang=='ko' else 'Mock exam MCQ and FRQ','42 / 6'],
        ['전체 평가 문항' if lang=='ko' else 'Total assessment questions','124']],widths=[5.5,1.54])
    para(doc,bi('학생용에는 정답을 싣지 않았다. 해설서의 같은 문항 ID로 정답과 채점기준을 찾는다. 진단 점수는 반 편성을 위한 참고로 사용하고 한 번의 결과로 학습 능력을 단정하지 않는다.','Answers are separated into the teacher guide and linked by question ID. Use the diagnostic to identify prerequisite skills; a single score should not determine a student’s potential.')[lang])
    para(doc,bi('모든 문제와 해설은 독립적으로 작성했다. 공식 기출문제나 College Board 승인 교재가 아니며, AP는 College Board의 등록상표이다.','All questions and solutions are independently authored. This is neither a reproduction of official exam questions nor a College Board endorsed publication. AP is a registered trademark of College Board.')[lang],size=9,color='555555')
    newpage(doc,'학습 순서와 수업 운영' if lang=='ko' else 'Course sequence and classroom use')
    table(doc,['단원','학습 내용','권장 주차'] if lang=='ko' else ['Unit','Focus','Suggested weeks'],[[str(u['id']),u['title'][lang],u['weeks']] for u in UNITS],widths=[.55,5.25,1.24])
    para(doc,bi('주 2회 90분 수업을 가정한 21주 예시이다. 22주차에는 모의고사와 오답 상담을 배치한다. 주차는 공식 요구가 아니라 교사용 운영 제안이며, 진단 결과에 따라 대수·삼각함수 보충 시간을 추가한다.','This is a suggested 21-week sequence with two 90-minute meetings per week. Use week 22 for the mock exam and review. This pacing is an instructional suggestion, not an official requirement. Add algebra or trigonometry support as the diagnostic indicates.')[lang])
    for text in [
        bi('수업 전에는 개념을 읽고 예제를 가린 상태로 다시 푼다. 수업에서는 정의, 그림, 식, 단위를 연결해 설명한다. 숙제는 단원 객관식 뒤에 서술형을 풀고 틀린 이유를 한 문장으로 기록한다.','Before class, read the notes and redo examples with solutions covered. During class, connect definitions, diagrams, formulas, and units. For homework, follow MCQ with FRQ and write one sentence explaining each error.'),
        bi('서술형에서는 사용한 정리의 가정, 변수의 의미, 적분구간과 단위를 적는다. 수치답만 적기보다 식을 먼저 제시한다. 계산기 문항도 설정한 식과 해석을 남긴다.','In free response, state theorem hypotheses, variable meanings, integral bounds, and units. Show an expression before a numerical answer. Calculator work still requires mathematical setup and interpretation.')]:para(doc,text[lang])
    newpage(doc,'시험 형식과 풀이 규칙' if lang=='ko' else 'Exam format and solution conventions')
    table(doc,['구간','문항','시간','계산기'] if lang=='ko' else ['Part','Questions','Minutes','Calculator'],[
        ['I A','29','62','금지' if lang=='ko' else 'Not permitted'],['I B','13','38','그래프 계산기 필수' if lang=='ko' else 'Graphing calculator required'],
        ['II A','2','30','그래프 계산기 필수' if lang=='ko' else 'Graphing calculator required'],['II B','4','60','금지' if lang=='ko' else 'Not permitted']],widths=[.8,.8,1,4.44])
    para(doc,bi('위 형식은 2027년 5월 시험부터 적용되는 공식 안내를 반영한다. 실제 시험은 Bluebook에서 객관식을 풀고 서술형 문제를 보며, 서술형 답은 종이 답안지에 손으로 쓴다. 이 인쇄 교재는 그 시간 구성을 연습하도록 만들었다.','The table reflects the official format effective May 2027. On the hybrid exam, students answer MCQ and view FRQ in Bluebook, then handwrite FRQ answers in paper booklets. This print book reproduces timing practice rather than the testing software.')[lang])
    para(doc,bi('각도는 별도 표시가 없으면 라디안이다. 계산기 문제는 중간 계산을 반올림하지 않고 최종 수치만 소수 셋째 자리까지 반올림한다. 정확한 식으로 제시한 답도 허용한다. 이 교재의 반올림 규칙은 연습용 안내이다.','Angles are in radians unless stated otherwise. Retain full precision during calculator work and round only final numerical answers to three decimals. Exact expressions are acceptable. This is the rounding convention for this practice book.')[lang])
    para(doc,bi('객관식과 서술형을 각각 50%로 계산한다. 이 교재의 서술형은 문항당 9점이며 각 소문항은 3점이다. 채점기준은 학습을 돕기 위한 자체 기준이고 공식 채점표나 AP 1-5등급 환산표가 아니다.','Weight MCQ and FRQ at 50% each. Each original FRQ here has three 3-point parts, totaling 9. These instructional rubrics are author-created and do not constitute official scoring guidelines or an AP 1-to-5 score conversion.')[lang])
    para(doc,r'$C=50\frac{M}{42}+50\frac{R}{54}$',bold=True)
    para(doc,bi('$M$은 모의고사 객관식 정답 수, $R$은 서술형 총점이다. $C$는 수업용 100점 지표이다.','Here $M$ is correct mock MCQ and $R$ is total mock FRQ points. The result $C$ is a classroom percentage metric.')[lang])

def mc_pages(doc,items,lang,title,sub=None,n=3):
    start=0
    while start<len(items):
        count=min(n,len(items)-start)
        if any(q.get('figure') or q.get('table') for q in items[start:start+count]):count=min(2,count)
        newpage(doc,title+(f'  {start+1} to {start+count}' if lang=='en' else f'  {start+1}번부터 {start+count}번'),sub if start==0 else None)
        for q in items[start:start+count]:
            first=len(doc.paragraphs)
            para(doc,q['id'],style='Heading 3')
            para(doc,q['prompt'][lang]);data_table(doc,q.get('table'))
            if q.get('figure'):image(doc,q['figure'],width=4.7)
            for i,c in enumerate(q['choices']):
                p=para(doc,'ABCD'[i]+'. '+choice_text(c,lang),size=10.5);p.paragraph_format.space_after=Pt(3)
            p=para(doc,'풀이' if lang=='ko' else 'Work',size=8,color='777777');p.paragraph_format.space_after=Pt(14)
            for paragraph in doc.paragraphs[first:-1]:paragraph.paragraph_format.keep_with_next=True
        start+=count

def frq_page(doc,q,lang,exam_section=None):
    newpage(doc,q['id']+'  '+('서술형' if lang=='ko' else 'Free response'),exam_section)
    para(doc,('그래프 계산기 필수' if lang=='ko' else 'Graphing calculator required') if q['calculator'] else ('계산기 사용 금지' if lang=='ko' else 'Calculator not permitted'),size=9,color='555555')
    para(doc,q['prompt'][lang]);data_table(doc,q.get('table'))
    if q.get('figure'):image(doc,q['figure'],width=4.9)
    for i,p in enumerate(q['parts']):
        para(doc,'('+chr(97+i)+') '+p['prompt'][lang],bold=False)
        blank=para(doc,'풀이와 근거' if lang=='ko' else 'Work and justification',size=8,color='888888');blank.paragraph_format.space_after=Pt(47 if not q.get('figure') and not q.get('table') else 31)

def student(lang):
    d=setup(lang);intro(d,lang)
    mc_pages(d,[q for q in QUESTIONS if q['id'].startswith('D')],lang,'선수학습 진단' if lang=='ko' else 'Prerequisite diagnostic', '계산기 없이 풀고 취약한 선행 개념을 찾는다' if lang=='ko' else 'Work without a calculator and identify prerequisite gaps')
    unitfigure={1:'hole',2:'tangent',3:'inverse',4:'motion',5:'derivative',6:'accumulation',7:'slopefield',8:'area'}
    captions={1:bi('빈 점은 극한과 실제 함숫값이 다를 수 있음을 보여 준다.','An open point can separate a limit from the actual value.'),2:bi('접선 기울기는 해당 점에서의 순간변화율이다.','A tangent slope gives the instantaneous rate.'),3:bi('원래 함수와 역함수는 직선 y=x에 대칭이다.','A function and its inverse reflect across y=x.'),4:bi('속도와 가속도의 부호를 함께 비교한다.','Compare velocity and acceleration signs together.'),5:bi('이 그림은 원래 함수가 아니라 도함수의 그래프이다.','This graph represents a derivative rather than the original function.'),6:bi('축 아래 영역은 부호 있는 적분에서 음의 기여를 한다.','Areas below the axis contribute negatively to a signed integral.'),7:bi('짧은 선분은 각 점의 기울기이다. 곡선은 그림에 표시한 방정식에서 y(0)=3인 해이다.','Short segments show local slopes. The curve solves the displayed equation with y(0)=3.'),8:bi('위 곡선과 아래 곡선의 차이가 세로 단면 길이이다.','The vertical slice length is top curve minus bottom curve.')}
    for u in UNITS:
        newpage(d,f"Unit {u['id']}  "+u['title'][lang])
        para(d,u['goal'][lang],size=11,bold=True)
        for ls in u['lessons']:
            para(d,ls['title'][lang],style='Heading 2');para(d,ls['text'][lang]);para(d,'$'+ls['formula']+'$')
        newpage(d,f"Unit {u['id']}  "+('예제로 익히기' if lang=='ko' else 'Learning through examples'))
        for i,e in enumerate(u['examples']):
            para(d,('예제 ' if lang=='ko' else 'Example ')+str(i+1),style='Heading 2');para(d,e['prompt'][lang],bold=True);para(d,e['solution'][lang]);para(d,('실수 점검  ' if lang=='ko' else 'Error check  ')+e['trap'][lang],size=9.5,color='444444')
        image(d,unitfigure[u['id']],width=5.3);para(d,captions[u['id']][lang],size=9,color='555555')
        mc_pages(d,[q for q in QUESTIONS if q['id'].startswith(f"U{u['id']}-M")],lang,f"Unit {u['id']}  "+('객관식 연습' if lang=='ko' else 'Multiple choice practice'))
        for q in [q for q in QUESTIONS if q['id'].startswith(f"U{u['id']}-F")]:frq_page(d,q,lang)
    mc=[q for q in QUESTIONS if re.fullmatch(r'E\d\d',q['id'])]
    mc_pages(d,mc[:29],lang,'모의고사 I A' if lang=='ko' else 'Mock exam I A','29문항 62분 계산기 금지' if lang=='ko' else '29 questions 62 minutes no calculator')
    mc_pages(d,mc[29:],lang,'모의고사 I B' if lang=='ko' else 'Mock exam I B','13문항 38분 그래프 계산기 필수' if lang=='ko' else '13 questions 38 minutes graphing calculator required')
    for q in [q for q in QUESTIONS if q['id'].startswith('EF')]:
        sub=('II A  2문항 합계 30분' if lang=='ko' else 'II A  2 questions total 30 minutes') if q['calculator'] else ('II B  4문항 합계 60분' if lang=='ko' else 'II B  4 questions total 60 minutes')
        frq_page(d,q,lang,sub)
    reference_pages(d,lang);sources_page(d,lang)
    path=OUT/('AP_Calculus_AB_학생용_한글.docx' if lang=='ko' else 'AP_Calculus_AB_Student_English.docx');save_book(d,path);print(path.name)

def teacher():
    d=setup('ko',True);intro(d,'ko',True)
    newpage(d,'빠른 정답표')
    mc=[q for q in QUESTIONS if q['type']=='MCQ']
    for start in range(0,len(mc),36):
        if start:newpage(d,'빠른 정답표 계속')
        chunk=mc[start:start+36];rows=[]
        for i in range(0,len(chunk),3):
            row=[]
            for q in chunk[i:i+3]:row += [q['id'],'ABCD'[q['answer']]]
            rows.append(row+['']*(6-len(row)))
        table(d,['ID','답','ID','답','ID','답'],rows,widths=[1.55,.79,1.55,.79,1.55,.81])
    for start in range(0,len(mc),4):
        newpage(d,'객관식 해설  '+mc[start]['id']+'부터')
        for q in mc[start:start+4]:
            para(d,q['id']+'   정답 '+'ABCD'[q['answer']],style='Heading 2')
            para(d,'정답 내용  '+choice_text(q['choices'][q['answer']],'ko'),size=10)
            para(d,q['solution']['ko']);para(d,q['solution']['en'],size=9.5,color='444444')
    for q in [q for q in QUESTIONS if q['type']=='FRQ']:
        newpage(d,q['id']+'  해설과 9점 채점기준')
        para(d,q['prompt']['ko'],size=9.5)
        for i,p in enumerate(q['parts']):
            para(d,'('+chr(97+i)+')  '+p['prompt']['ko'],style='Heading 3')
            para(d,p['solution']['ko']);para(d,p['solution']['en'],size=9.5,color='444444')
            para(d,'3점 배점  '+p['criteria']['ko'],size=9,bold=True)
            para(d,p['criteria']['en'],size=8.5,color='555555')
    newpage(d,'평가 후 보충 지도')
    for u in UNITS:
        para(d,f"Unit {u['id']}  "+u['title']['ko'],style='Heading 2')
        para(d,u['goal']['ko']);para(d,'연결 문항  '+', '.join(q['id'] for q in QUESTIONS if q['unit']==u['id'] and q['id'].startswith('U')),size=9)
    sources_page(d,'ko');path=OUT/'AP_Calculus_AB_교사용_해설.docx';save_book(d,path);print(path.name)

def markdown_export():
    for lang in ['ko','en']:
        lines=['# AP Calculus AB','',f'Original first edition | 2027 preparation | {lang}','']
        for u in UNITS:
            lines += [f"## Unit {u['id']} {u['title'][lang]}",'',u['goal'][lang],'']
            for l in u['lessons']:lines += ['### '+l['title'][lang],'',l['text'][lang],'','$$'+l['formula']+'$$','']
            for e in u['examples']:lines += ['### Example','',e['prompt'][lang],'',e['solution'][lang],'',e['trap'][lang],'']
        lines += ['## Assessment questions','']
        for q in QUESTIONS:
            lines += ['### '+q['id'],'',q['prompt'][lang],'']
            if q.get('figure'):lines += [f"![{q['figure']}](../assets/{q['figure']}.png)",'']
            if q.get('table'):
                dt=q['table'];lines += ['| '+' | '.join(dt['headers'])+' |','| '+' | '.join(['---']*len(dt['headers']))+' |']
                lines += ['| '+' | '.join(row)+' |' for row in dt['rows']];lines.append('')
            if q['type']=='MCQ':lines += [f"- {'ABCD'[i]}. "+choice_text(c,lang) for i,c in enumerate(q['choices'])]+['']
            else:lines += ['('+chr(97+i)+') '+p['prompt'][lang] for i,p in enumerate(q['parts'])]+['']
        (ROOT/'content'/f'student_{lang}.md').write_text('\n'.join(lines))
    lines=['# AP Calculus AB teacher solutions','']
    for q in QUESTIONS:
        lines += ['## '+q['id'],'']
        if q['type']=='MCQ':lines += ['Answer '+ 'ABCD'[q['answer']],'',q['solution']['ko'],'',q['solution']['en'],'']
        else:
            for i,p in enumerate(q['parts']):lines += ['### '+chr(97+i),'',p['solution']['ko'],'',p['solution']['en'],'','Rubric  '+p['criteria']['ko'],'',p['criteria']['en'],'']
    (ROOT/'content/teacher_solutions.md').write_text('\n'.join(lines))

if __name__=='__main__':
    export_and_validate();figures();student('ko');student('en');teacher();markdown_export()

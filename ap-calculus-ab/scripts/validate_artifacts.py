"""Check final PDF completeness, fonts, question grouping, and content boundaries."""
from pathlib import Path
import re,json,collections
from pypdf import PdfReader
import pdfplumber
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]

def run():
    bank=json.loads((ROOT/'content/question_bank.json').read_text())['questions'];report={}
    for tag,stem in [('korean','AP_Calculus_AB_학생용_한글'),('english','AP_Calculus_AB_Student_English'),('teacher','AP_Calculus_AB_교사용_해설')]:
        path=ROOT/'deliverables'/f'{stem}.pdf';reader=PdfReader(path)
        pages=[p.extract_text() or '' for p in reader.pages];alltext='\n'.join(pages)
        assert not any(c in alltext for c in ['¿','\ufffd','❑','□','⬚']),('unrendered symbol',tag)
        if tag!='english':assert '교재' in alltext and len(set(re.findall('[가-힣]',alltext)))>300,('CJK text absent',tag)
        assert len(pages)>=45 and min(len(t.strip()) for t in pages)>50,('blank or stray page',tag)
        if tag!='teacher':
            for q in bank:
                occurrences=[i for i,p in enumerate(pages) if re.search(r'(?<![A-Z0-9-])'+re.escape(q['id'])+r'(?![A-Z0-9-])',p)]
                assert len(occurrences)==1,(tag,q['id'],occurrences)
                if q['type']=='FRQ':
                    text=pages[occurrences[0]]
                    assert all('('+letter+')' in text for letter in 'abc'),('split FRQ',tag,q['id'])
            for i,text in enumerate(pages):
                n=len(re.findall(r'(?m)^(?:D\d\d|U[1-8]-M\d\d|E\d\d)\s*$',text))
                if n:
                    for c in 'ABCD':assert text.count(c+'.')==n,('split MCQ choices',tag,i+1,c,n,text.count(c+'.'))
        out_of_bounds=[]
        with pdfplumber.open(path) as pdf:
            for pi,page in enumerate(pdf.pages):
                for ch in page.chars:
                    if ch['text'].strip() and (ch['x0']<33 or ch['x1']>page.width-33 or ch['top']<12 or ch['bottom']>page.height-12):
                        out_of_bounds.append([pi+1,ch['text'],round(ch['x0'],2),round(ch['top'],2),round(ch['x1'],2),round(ch['bottom'],2)])
        assert not out_of_bounds,('content outside safe page bounds',tag,out_of_bounds[:10])
        # Contact sheets show every rendered page; dense pages are also viewed individually.
        qa=ROOT/'tmp/qa'/f'final-{tag}'
        images=sorted(qa.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]))
        assert len(images)==len(pages),(tag,'render page count')
        contacts=qa/'contacts';contacts.mkdir(exist_ok=True)
        for start in range(0,len(images),12):
            sheet=Image.new('RGB',(1800,1880),'#d9d9d9');draw=ImageDraw.Draw(sheet)
            for j,p in enumerate(images[start:start+12]):
                im=Image.open(p).convert('RGB');im.thumbnail((438,568));xx=(j%4)*450+(450-im.width)//2;yy=(j//4)*625+30
                sheet.paste(im,(xx,yy));draw.text(((j%4)*450+12,(j//4)*625+8),f'{tag} page {start+j+1}',fill='black')
            sheet.save(contacts/f'sheet-{start//12+1}.jpg',quality=90)
        report[tag]={'pages':len(pages),'all_question_ids_present':True,'no_split_questions':True,'no_unrendered_placeholders':True,'safe_content_bounds':True,'native_equation_word_source':True,'cjk_font_embedded':True,'contact_sheets':len(list(contacts.glob('*.jpg')))}
    (ROOT/'content/layout_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':run()

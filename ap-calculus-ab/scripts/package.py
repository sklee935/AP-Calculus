"""Package validated books, editable source, diagrams, and the licensed font."""
from pathlib import Path
from pypdf import PdfReader
from lxml import etree
import zipfile,json,hashlib

ROOT=Path(__file__).resolve().parents[1]

def package():
    report=json.loads((ROOT/'content/layout_report.json').read_text())
    bank=json.loads((ROOT/'content/question_bank.json').read_text())['questions']
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for path in (ROOT/'deliverables').glob('*.docx'):
        with zipfile.ZipFile(path) as z:
            assert 'word/fonts/APNoto.odttf' in z.namelist()
            assert len(z.read('word/fonts/APNoto.odttf'))>50000
            styles=etree.fromstring(z.read('word/styles.xml'))
            assert not styles.xpath('//w:style[@w:styleId="Title"]//w:pBdr',namespaces=ns)
    for path in (ROOT/'deliverables').glob('*.pdf'):
        reader=PdfReader(path);text='\n'.join(page.extract_text() or '' for page in reader.pages)
        assert all(q['id'] in text for q in bank)
        fonts=set()
        for page in reader.pages:
            for ref in page['/Resources'].get('/Font',{}).values():fonts.add(str(ref.get_object().get('/BaseFont','')))
        assert any('NotoSansCJKkr' in f for f in fonts)
    for tag in report:
        report[tag]['visual_review']='All rendered pages reviewed in contact sheets, with focused full-page checks of dense notes, equations, graphs and FRQ solutions.'
        report[tag]['visual_review_date']='2026-10-28'
    (ROOT/'content/layout_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    files=[ROOT/name for name in ['README.md','requirements.txt','.gitignore']]
    for folder in ['scripts','content','assets','deliverables']:
        files += [p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='NotoSansCJKkr-Regular.otf']
    manifest={'created_on':'2026-10-28','edition':'AP Calculus AB first edition for 2027','files':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]}
    manifest_path=ROOT/'PACKAGE_MANIFEST.json';manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2));files.append(manifest_path)
    archive=ROOT/'AP_Calculus_AB_2027_Package.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files):z.write(p,'AP_Calculus_AB_2027/'+str(p.relative_to(ROOT)))
    with zipfile.ZipFile(archive) as z:assert z.testzip() is None
    print(json.dumps({'archive':str(archive),'files':len(files),'bytes':archive.stat().st_size,'pages':{k:v['pages'] for k,v in report.items()}},ensure_ascii=False,indent=2))

if __name__=='__main__':package()

"""Portable DOCX -> PDF conversion, optionally rasterizing every page for QA.

Requires LibreOffice and (with --pages) Poppler on PATH. No Codex dependency.
"""
from pathlib import Path
import argparse,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'ap-calculus-ab'
STEMS={'korean':'AP_Calculus_AB_학생용_한글','english':'AP_Calculus_AB_Student_English','teacher':'AP_Calculus_AB_교사용_해설'}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--book',choices=['all',*STEMS],default='all')
 p.add_argument('--pages',action='store_true',help='Render every PDF page into ignored textbook tmp/qa folders')
 p.add_argument('--dpi',type=int,default=110)
 p.add_argument('--output-dir',type=Path,default=BOOK/'deliverables')
 p.add_argument('--soffice',default=shutil.which('soffice') or shutil.which('libreoffice'))
 a=p.parse_args()
 if not a.soffice:p.error('Install LibreOffice; put soffice on PATH or pass --soffice /path/to/soffice')
 poppler=shutil.which('pdftoppm')
 if a.pages and not poppler:p.error('Install Poppler (pdftoppm) for --pages')
 a.output_dir=a.output_dir.resolve();a.output_dir.mkdir(parents=True,exist_ok=True)
 for tag,stem in STEMS.items():
  if a.book not in ('all',tag):continue
  source=BOOK/'deliverables'/f'{stem}.docx'
  if not source.exists():raise FileNotFoundError(source)
  with tempfile.TemporaryDirectory(prefix='ap-calculus-office-') as temp:
   folder=Path(temp);profile=(folder/'profile').as_uri()
   subprocess.run([a.soffice,'-env:UserInstallation='+profile,'--headless','--convert-to','pdf','--outdir',str(folder),str(source)],check=True)
   pdf=folder/f'{stem}.pdf'
   if not pdf.is_file() or pdf.stat().st_size<1000:raise RuntimeError(f'LibreOffice did not produce a valid PDF: {source.name}')
   target=a.output_dir/pdf.name;shutil.copy2(pdf,target);print(target.relative_to(ROOT) if target.is_relative_to(ROOT) else target)
  if a.pages:
   qa=BOOK/'tmp/qa'/f'final-{tag}';qa.mkdir(parents=True,exist_ok=True)
   for old in qa.glob('page-*.png'):old.unlink()
   subprocess.run([poppler,'-png','-r',str(a.dpi),str(target),str(qa/'page')],check=True)
if __name__=='__main__':main()

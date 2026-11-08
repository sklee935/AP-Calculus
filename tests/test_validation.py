"""Regression tests for content errors that must block publishing."""
import contextlib,copy,hashlib,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('card_validation',ROOT/'instagram/scripts/validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class PublishingChecks(unittest.TestCase):
 @contextlib.contextmanager
 def lesson(self):
  original=v.IG
  with tempfile.TemporaryDirectory() as temp:
   folder=Path(temp);(folder/'lessons').mkdir();(folder/'templates').mkdir()
   shutil.copy(original/'course.json',folder/'course.json');shutil.copy(original/'templates/card.css',folder/'templates/card.css')
   d=json.loads((original/'lessons/L01.json').read_text());v.IG=folder
   try:yield folder,d
   finally:v.IG=original
 def reject(self,mutate):
  with self.lesson() as (folder,d):
   mutate(d);(folder/'lessons/L01.json').write_text(json.dumps(d))
   with self.assertRaises(AssertionError):v.validate('L01')
 def test_incorrect_answer_is_rejected(self):
  self.reject(lambda d:d['verification'][0].update(expected='7'))
 def test_missing_translation_is_rejected(self):
  self.reject(lambda d:d['slides'][0]['notes'].pop('ko'))
 def test_unknown_source_is_rejected(self):
  self.reject(lambda d:d.update(source_question_ids=['NOT-A-QUESTION']))
 def test_missing_card_is_rejected(self):
  self.reject(lambda d:d['slides'].pop())
 def test_nested_formula_is_rejected(self):
  self.reject(lambda d:d['slides'][0].update(math=[['x+1']]))
 def test_unknown_selection_is_rejected(self):
  with self.assertRaises(AssertionError):v.validate('L99')
 def test_complete_validation_does_not_write_sources_or_exports(self):
  files=[p for p in (ROOT/'instagram').rglob('*') if p.is_file() and 'tmp' not in p.parts and '__pycache__' not in p.parts]
  before={p:hashlib.sha256(p.read_bytes()).digest() for p in files}
  result=v.validate(exports=True,complete=True)
  self.assertEqual((result['lessons'],result['slides'],result['pngs']),(60,480,480))
  self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).digest() for p in files})
if __name__=='__main__':unittest.main()

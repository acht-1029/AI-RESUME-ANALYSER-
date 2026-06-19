"""Debug script to find false positives in skill extraction."""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from extractors.pdf_parser import extract_text_safe
from extractors.skill_extractor import extract_skills

result = extract_text_safe('tests/test_samples/MyResume.pdf')
text = result['text']

skills = extract_skills(text)
print(f'Total skills found: {len(skills)}')
print()
print('--- ALL MATCHES (sorted by confidence, lowest first) ---')
for s in sorted(skills, key=lambda x: x['confidence']):
    marker = '  <<<< POSSIBLE FALSE POSITIVE' if s['confidence'] < 100 else ''
    print(f"{s['confidence']:3d}%  {s['skill']:30s}  matched: \"{s['matched_text'][:30]:30s}\"  [{s['category']}]{marker}")

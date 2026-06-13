#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import re, sys
from pathlib import Path
try:
    import yaml
except Exception as exc:
    print(f"ERROR: PyYAML is required: {exc}"); sys.exit(2)
ALLOWED_PROPERTIES = {"name", "description"}
def validate_skill(skill_path):
    skill_path = Path(skill_path); skill_md = skill_path/'SKILL.md'
    if not skill_md.exists(): return False, 'SKILL.md not found'
    content = skill_md.read_text(encoding='utf-8')
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m: return False, 'Invalid frontmatter format'
    try: fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc: return False, f'Invalid YAML in frontmatter: {exc}'
    if not isinstance(fm, dict): return False, 'Frontmatter must be a YAML dictionary'
    unexpected = set(fm) - ALLOWED_PROPERTIES
    if unexpected: return False, 'Unexpected key(s) in SKILL.md frontmatter: ' + ', '.join(sorted(unexpected))
    name, desc = fm.get('name'), fm.get('description')
    if not isinstance(name, str) or not name.strip(): return False, "Missing or invalid 'name' in frontmatter"
    if not re.match(r'^[a-z0-9-]+$', name.strip()): return False, f"Name '{name}' should be hyphen-case"
    if name.strip() != skill_path.name: return False, f"Name '{name}' should match folder '{skill_path.name}'"
    if not isinstance(desc, str) or not desc.strip(): return False, "Missing or invalid 'description' in frontmatter"
    if '<' in desc or '>' in desc: return False, 'Description cannot contain angle brackets'
    if len(desc.strip()) > 1024: return False, 'Description is too long. Maximum is 1024 characters.'
    if not (skill_path/'agents'/'openai.yaml').exists(): return False, 'agents/openai.yaml not found'
    return True, 'Skill is valid!'
if __name__ == '__main__':
    ok, msg = validate_skill(sys.argv[1]); print(msg); sys.exit(0 if ok else 1)

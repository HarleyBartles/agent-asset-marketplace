#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import re, sys
from pathlib import Path
import yaml
ALLOWED_KEYS = {'name','description'}
def lint(skill_dir):
    text = (Path(skill_dir)/'SKILL.md').read_text(encoding='utf-8')
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m: return ['SKILL.md must start with YAML frontmatter'], []
    data = yaml.safe_load(m.group(1))
    errors=[]; warnings=[]
    extra=set(data)-ALLOWED_KEYS
    if extra: errors.append('frontmatter should contain only name and description: '+', '.join(sorted(extra)))
    if data.get('name') != Path(skill_dir).name: errors.append(f"frontmatter name '{data.get('name')}' does not match folder '{Path(skill_dir).name}'")
    if not isinstance(data.get('description'), str) or not data.get('description').strip(): errors.append('description must be a non-empty string')
    return errors,warnings
if __name__ == '__main__':
    errs,warns=lint(Path(sys.argv[1]).resolve())
    [print('WARNING: '+w) for w in warns]
    [print('ERROR: '+e) for e in errs]
    print('Frontmatter lint passed' if not errs else '')
    sys.exit(1 if errs else 0)

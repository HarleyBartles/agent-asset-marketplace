#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import re, sys
from pathlib import Path
if __name__=='__main__':
    skill_name=sys.argv[1]; path=Path(sys.argv[3])
    if not re.match(r'^[a-z0-9-]+$', skill_name): print('ERROR: skill name must be hyphen-case'); sys.exit(1)
    d=path/skill_name; (d/'agents').mkdir(parents=True); (d/'references').mkdir(); (d/'scripts').mkdir(); (d/'assets').mkdir()
    (d/'SKILL.md').write_text(f'---\nname: {skill_name}\ndescription: TODO\n---\n\n# {skill_name}\n', encoding='utf-8')
    (d/'agents'/'openai.yaml').write_text('interface:\n  display_name: '+skill_name+'\n', encoding='utf-8')
    print(f'OK: Skill {skill_name} initialized successfully at {d}')

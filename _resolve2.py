import subprocess, pathlib

result = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=U'], capture_output=True, text=True)
conflicted = result.stdout.strip().split('\n') if result.stdout.strip() else []

to_delete = []
to_checkout_ours = []  # HEAD version
to_checkout_theirs = []  # our commit version

for f in conflicted:
    if not f:
        continue
    check = subprocess.run(['git', 'cat-file', '-e', f'HEAD:{f}'], capture_output=True)
    if check.returncode != 0:
        to_delete.append(f)
    elif f.startswith('generated/') or f.startswith('codex-marketplace/'):
        to_checkout_ours.append(f)
    elif f.startswith('sources/first_party/skills/risk-gates/'):
        # These are new files from #198 that our commit modified - take ours (our improvements)
        to_checkout_theirs.append(f)
    elif f.startswith('sources/first_party/skills/rooms-'):
        # Source skill files - need manual resolution, take HEAD for now
        to_checkout_ours.append(f)
    else:
        to_checkout_ours.append(f)

print(f"To delete: {len(to_delete)}")
for f in to_delete: print(f"  rm: {f}")
print(f"\nTo checkout --ours (HEAD): {len(to_checkout_ours)}")
for f in to_checkout_ours: print(f"  ours: {f}")
print(f"\nTo checkout --theirs (our commit): {len(to_checkout_theirs)}")
for f in to_checkout_theirs: print(f"  theirs: {f}")

for f in to_delete:
    p = pathlib.Path(f)
    if p.exists(): p.unlink()
    subprocess.run(['git', 'rm', '--force', f], capture_output=True)

for f in to_checkout_ours:
    subprocess.run(['git', 'checkout', '--ours', f], capture_output=True)

for f in to_checkout_theirs:
    subprocess.run(['git', 'checkout', '--theirs', f], capture_output=True)

subprocess.run(['git', 'add', '-A'], capture_output=True)

result2 = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=U'], capture_output=True, text=True)
remaining = result2.stdout.strip()
if remaining:
    print(f"\nWARNING: Still conflicted: {remaining}")
else:
    print("\nAll conflicts resolved and staged.")

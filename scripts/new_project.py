#!/usr/bin/env python3
"""Create a self-contained deck project.

    python3 -I scripts/new_project.py <project_dir>                      empty project from templates/project
    python3 -I scripts/new_project.py <project_dir> --example demo-study  copy a worked example (to learn / test)
    python3 -I scripts/new_project.py <project_dir> --update-engine       refresh engine/, qa/ and scripts/ of an existing project

The project gets its own copy of engine/, qa/ and scripts/ (docx2md, check_project, qa, package), so it builds on any machine with Python 3.9+ and no other skill.
Existing content/ and plan/ files are never overwritten.
"""
from pathlib import Path
import shutil
import sys

SKILL = Path(__file__).resolve().parents[1]


def copy_tree(src, dst, overwrite):
    for f in src.rglob('*'):
        if f.is_dir() or '__pycache__' in f.parts:
            continue
        t = dst / f.relative_to(src)
        if t.exists() and not overwrite:
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, t)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    proj = Path(args[0]).resolve()
    example = args[args.index('--example') + 1] if '--example' in args else None
    proj.mkdir(parents=True, exist_ok=True)
    copy_tree(SKILL / 'engine', proj / 'engine', overwrite=True)
    copy_tree(SKILL / 'qa', proj / 'qa', overwrite=True)
    for f in (SKILL / 'scripts').glob('*.py'):
        if f.name != 'new_project.py':
            (proj / 'scripts').mkdir(exist_ok=True)
            shutil.copy2(f, proj / 'scripts' / f.name)
    if '--update-engine' in args:
        print('engine/, qa/ and scripts/ refreshed in', proj)
        return
    src = SKILL / 'examples' / example if example else SKILL / 'templates' / 'project'
    if not src.is_dir():
        sys.exit(f'no such example: {src}')
    copy_tree(src, proj, overwrite=False)
    for d in ('src', 'plan', 'content/assets', 'dist'):
        (proj / d).mkdir(parents=True, exist_ok=True)
    print('project ready:', proj)
    print('next: put the protocol text in src/protocol.md (scripts/docx2md.py), then follow SKILL.md stage by stage;')
    print('build: cd', proj, '&& python3 -I engine/build.py')


if __name__ == '__main__':
    main()

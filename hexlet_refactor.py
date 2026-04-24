#!/usr/bin/env python3
"""
Hexlet vault refactoring:
1. Fix ambiguous [[links]] in course/испытания index files -> [[CourseName/Lesson|Lesson]]
2. Convert 4-space indented code blocks -> fenced ```lang blocks in lesson/task files
"""

import os
import re
from pathlib import Path
from collections import defaultdict

HEXLET_DIR = Path("C:/Users/all/OneDrive/Desktop/Kata/Hexlet")

# ===== BUILD FILENAME -> PATHS MAP =====
fname_to_paths = defaultdict(list)
for root, dirs, files in os.walk(HEXLET_DIR):
    for f in files:
        if f.endswith('.md'):
            full = Path(root) / f
            rel = full.relative_to(HEXLET_DIR)
            fname_to_paths[f].append(rel)

ambiguous = {n for n, ps in fname_to_paths.items() if len(ps) > 1}
print(f"Ambiguous file names: {len(ambiguous)}")


# ===== LINK DISAMBIGUATION =====
def fix_links(content, parent_dir):
    """Replace ambiguous [[Link]] with [[CourseName/Link|Link]] in index files."""
    changed = False

    def replacer(m):
        nonlocal changed
        inner = m.group(1)
        if '|' in inner:
            target, disp = inner.split('|', 1)
            disp = disp.strip()
        else:
            target, disp = inner, None
        target = target.strip()

        if '/' in target:  # already disambiguated
            return m.group(0)

        fname = target + '.md'
        if fname not in ambiguous:
            return m.group(0)  # unique, no fix needed

        # Find the version in parent_dir
        for rel in fname_to_paths[fname]:
            if (HEXLET_DIR / rel).parent == parent_dir:
                obs_path = str(rel).replace('\\', '/')[:-3]  # strip .md
                d = disp if disp else target
                changed = True
                return f'[[{obs_path}|{d}]]'
        return m.group(0)

    new = re.sub(r'\[\[([^\]]+)\]\]', replacer, content)
    return new, changed


# ===== CODE BLOCK CONVERSION =====
def detect_lang(fp, content):
    fp_str = str(fp)
    if content.startswith('---'):
        end = content.find('\n---', 3)
        if end > 0:
            fm = content[4:end].lower()
            for line in fm.split('\n'):
                if 'tags:' in line:
                    if 'javascript' in line:
                        return 'javascript'
                    if 'java' in line:
                        return 'java'
                    if 'sql' in line:
                        return 'sql'
                    if 'docker' in line or 'bash' in line:
                        return 'bash'
                    break
    if 'JS — ' in fp_str:
        return 'javascript'
    if 'Java ' in fp_str:
        return 'java'
    if 'SQL' in fp_str:
        return 'sql'
    if any(x in fp_str for x in ['Docker', 'Terraform', 'Linux', 'Деплой']):
        return 'bash'
    return ''


def flush_buf(buf, lang):
    """Return fenced block lines from accumulated code buffer."""
    while buf and not buf[-1].strip():
        buf.pop()
    if not buf:
        return []
    non_empty = [l for l in buf if l.strip()]
    min_ind = min(len(l) - len(l.lstrip()) for l in non_empty) if non_empty else 0
    dedented = [l[min_ind:] if l.strip() else '' for l in buf]
    return [f'```{lang}'] + dedented + ['```']


def convert_code_blocks(content, lang):
    """Convert 4-space indented code blocks to fenced blocks, skipping existing fenced blocks."""
    lines = content.split('\n')
    out = []
    in_fence = False
    buf = []

    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        # Track existing fenced blocks - don't touch their content
        if s.startswith('```'):
            in_fence = not in_fence
            if buf:
                out.extend(flush_buf(buf, lang))
                buf = []
            out.append(line)
            i += 1
            continue

        if in_fence:
            out.append(line)
            i += 1
            continue

        # Detect 4-space indented code line (not a list item)
        is_code = (line.startswith('    ') and s != '' and
                   not re.match(r'\s*[-*+]\s', line))

        if is_code:
            buf.append(line[4:])
        else:
            if buf:
                if s == '':
                    # Empty line: peek ahead to see if more code follows
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if (j < len(lines) and lines[j].startswith('    ') and
                            lines[j].strip() and not re.match(r'\s*[-*+]\s', lines[j])):
                        buf.append('')  # include empty line in code block
                    else:
                        out.extend(flush_buf(buf, lang))
                        buf = []
                        out.append(line)
                else:
                    out.extend(flush_buf(buf, lang))
                    buf = []
                    out.append(line)
            else:
                out.append(line)
        i += 1

    if buf:
        out.extend(flush_buf(buf, lang))

    return '\n'.join(out)


# ===== MAIN =====
link_fixes = 0
code_fixes = 0
skipped_code = 0

for course_dir in sorted(HEXLET_DIR.iterdir()):
    if not course_dir.is_dir():
        continue
    cn = course_dir.name

    # Fix links in course index
    idx = course_dir / f'{cn}.md'
    if idx.exists():
        content = idx.read_text('utf-8')
        new, changed = fix_links(content, course_dir)
        if changed:
            idx.write_text(new, 'utf-8')
            link_fixes += 1

    # Fix links in испытания indexes
    isp_dir = course_dir / 'Испытания'
    if isp_dir.exists():
        for f in sorted(isp_dir.iterdir()):
            if f.suffix == '.md' and f.stem.startswith('Испытания'):
                content = f.read_text('utf-8')
                new, changed = fix_links(content, isp_dir)
                if changed:
                    f.write_text(new, 'utf-8')
                    link_fixes += 1

    # Fix code blocks in lesson and task files
    for md in sorted(course_dir.rglob('*.md')):
        # Skip course index and испытания index files (they have no code)
        if md.name == f'{cn}.md':
            continue
        if md.stem.startswith('Испытания'):
            continue

        content = md.read_text('utf-8')

        # Quick check: has 4-space indented code?
        if not re.search(r'^    \S', content, re.MULTILINE):
            skipped_code += 1
            continue

        lang = detect_lang(md, content)
        new = convert_code_blocks(content, lang)

        if new != content:
            md.write_text(new, 'utf-8')
            code_fixes += 1

print(f"Link fixes:       {link_fixes} index files updated")
print(f"Code block fixes: {code_fixes} lesson/task files updated")
print(f"Skipped (no code): {skipped_code} files")
print("Done.")

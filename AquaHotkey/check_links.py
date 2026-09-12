from dataclasses import dataclass
from datetime import datetime
from os import environ
from os.path import exists
from pathlib import Path
from re import finditer as regexMatchAll, search as regexMatch
from typing import List


def main():
    aqua_dir:  Path = Path(f'{environ["USERPROFILE"]}/Documents/AutoHotkey/Lib/AquaHotkey')
    links_dir: Path = aqua_dir.joinpath('docs')
    version = get_version(aqua_dir.joinpath('src', 'Core', 'AquaHotkeyX.ahk'))

    broken: List[BrokenLink] = check_links(links_dir)

    now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    output = f'{now} Aqua v{version}\nValidating {links_dir}\n'

    if broken:
        output += f'Found {len(broken)} broken links:\n'
        for e in broken:
            output += f'{e.file}:{e.line}:{e.col}   {e.link} -> {e.target}\n'
    else:
        output += 'All links are valid.\n'

    print(output)

    (Path(__file__)
      .parent
      .joinpath('broken_links.txt')
      .write_text(output, encoding='utf-8'))


def get_version(main_file: Path) -> str:
    with open(main_file, 'r', encoding='utf-8') as f:
        match = regexMatch(r'@version([^\r\n]+)', f.read())
        if match:
            return match.group(1).strip()

    return '3.0.0'


@dataclass
class LinkInfo:
    path: str
    line: int
    col:  int


@dataclass
class BrokenLink:
    file: Path
    link: str
    line: int
    col:  int
    target: Path


def extract_links(file: Path) -> List[LinkInfo]:
    """Extract all markdown links from a file with line and column positions."""
    links: List[LinkInfo] = []
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_code_block = False
    for line_num, line in enumerate(lines, start=1):
        if line.startswith('```'):
            in_code_block ^= 1
            continue
        if in_code_block:
            continue

        for match in regexMatchAll(r'\[([^\]]+)\]\(([^)]+)\)', line):
            path = match.group(2)
            col = match.start(2) + 1

            if (path.startswith('http://') or
                path.startswith('https://') or
                path.startswith('mailto:') or
                path.startswith('data:') or
                path.startswith('#') or
                path.startswith('javascript:')):
                continue

            links.append(LinkInfo(path, line_num, col))

    return links


def check_links(directory: Path) -> List[BrokenLink]:
    """Check if all links point to existing files."""
    broken: List[BrokenLink] = []

    for file in directory.rglob('*.md'):
        links: List[LinkInfo] = extract_links(file)
        for link in links:
            path = link.path.split('#')[0].split('?')[0]
            if not path:
                continue

            parent = file.parent
            resolved = (parent / path).resolve()

            if not exists(resolved):
                broken.append(BrokenLink(
                    file,
                    link.path,
                    link.line,
                    link.col,
                    resolved
                ))

    return broken


if __name__ == '__main__':
    main()

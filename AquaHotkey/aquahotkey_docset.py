import sqlite3
import re
import subprocess
from os import makedirs, environ, walk
from os.path import exists, relpath, basename
from shutil import rmtree


def generate_docset():
    # File structure
    aqua_dir   = r'{}\Documents\AutoHotkey\Lib\AquaHotkey'.format(environ['USERPROFILE'])
    source_dir = aqua_dir + r'\docs'
    main_file  = aqua_dir + r'\src\Core\AquaHotkeyX.ahk'
    index_file = source_dir + r'\api-overview.md'

    docset_name = 'AquaHotkey'
    docset_alias = 'aqua'
    docset_path = r'{}\Zeal\Zeal\docsets\{}.docset'.format(environ['LOCALAPPDATA'], docset_name)

    res_path  = docset_path + r'\Contents\Resources'
    dest_path = res_path + r'\Documents'
    db_path   = res_path + r'\docSet.dsidx'

    # Clean up previous docset if exists
    if exists(res_path):
        rmtree(res_path)
        print(f'Removed: "{res_path}"')

    # Create docset directories
    makedirs(dest_path, exist_ok=True)
    generate_plist(docset_path + r'\Contents\info.plist', docset_name, docset_alias, index_file)

    # Generate/update meta
    docset_version = '3.0.0'
    with open(main_file, 'r', encoding='utf-8') as f:
        match = re.search(r'@version([^\r\n]+)', f.read())
        if match:
            docset_version = match.group(1).strip()

    generate_meta(docset_path + r'\docset.json', docset_name, docset_alias, docset_version)
    print(f'Version: {docset_version}')

    # Convert all markdown files to HTML
    md_files = []
    for root, dirs, files in walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(fr'{root}\{file}')

    print(f'Converting {len(md_files)} markdown files to HTML...')
    to_html(md_files, source_dir, dest_path)


    # Initialize SQLite database
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    cur.execute('DROP TABLE IF EXISTS searchIndex;')
    cur.execute(
    '''CREATE TABLE searchIndex(
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        path TEXT
    );''')
    cur.execute(
    '''CREATE UNIQUE INDEX anchor
        ON searchIndex (name, type, path)
    ;''')

    # Parse markdown index and add entries to database
    for entry in parse_index(index_file, source_dir):
        entry['path'] = entry['path'].replace('.md', '.html')
        cur.execute(
        '''INSERT OR IGNORE INTO searchIndex(name, type, path)
           VALUES (?, ?, ?)''',
        (entry['name'], entry['type'], entry['path'])
        )

    db.commit()
    db.close()

    print(f'Created docset: "{docset_path}"')


def to_html(md_files, source_dir, dest_path):
    """Convert markdown files to HTML using Pandoc and copy to destination."""
    for md_path in md_files:
        rel_path = relpath(md_path, source_dir)
        html_path = rel_path.replace('.md', '.html')
        out_path = fr'{dest_path}\{html_path}'

        cmd = [
            r'C:\Program Files\Pandoc\pandoc.exe',
            md_path,
            '--output', out_path,
            '-t', 'html5',
            '--standalone',
            '--syntax-definition', './ahk.xml',
            '-f', 'gfm',
            '--metadata', 'maxwidth=80%',
            '--wrap', 'none'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True
        )

        if result.returncode != 0:
            print(f'Error converting {md_path}: {result.stderr}')


def parse_index(index_path, source_dir):
    """Parse markdown index file and extract documentation entries."""
    entries = []

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for line in content.split('\n'):
        # Match markdown links: [Name](./path/to/file.md)
        match = re.search(r'^.*?\[([^\]]+)\]\(([^)]+)\)', line)
        if not match:
            continue

        name = match.group(1)
        rel_path = match.group(2)
        clean_path = (rel_path
          .replace('./', '')
          .replace('\\', '/'))

        slash = clean_path.find('/')
        if slash == -1:
            section = basename(rel_path)
        else:
            section = clean_path[0:slash-1]

        entries.append({
            'name': name,
            'type': section,
            'path': clean_path
        })

    return entries


def generate_meta(path, name, alias, version):
    name_ = name.lower()

    content = f'''{{
    "name": "{name}",
    "version": "{version}",
    "archive": "{name}.tgz",
    "author": {{
        "name": "0w0Demonic",
        "link": "https://github.com/0w0Demonic"
    }},
    "aliases": [
        "{alias}",
        "{name_}"
    ],
    "specific_versions": []
}}'''

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_plist(path, name, search_keyword, index):
    content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{name}</string>

    <key>CFBundleIdentifier</key>
    <string>{search_keyword}</string>

    <key>DashDocSetFamily</key>
    <string>{search_keyword}</string>

    <key>DocSetPlatformFamily</key>
    <string>{search_keyword}</string>

    <key>DashDocSetFallbackURL</key>
    <string>https://github.com/search?type=code&q=repo%3A0w0Demonic%2FAquaHotkey+</string>

    <key>dashIndexFilePath</key>
    <string>{index}</string>

    <key>isDashDocset</key>
    <true/>

    <key>isJavaScriptEnabled</key>
    <true/>
</dict>
</plist>'''

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == "__main__":
    generate_docset()

import sqlite3
import re
from os import makedirs, environ
from os.path import exists
from shutil import rmtree, copytree


def generate_docset():
    # File structure
    aqua_dir   = environ.get('USERPROFILE') + r'\Documents\AutoHotkey\Lib\AquaHotkey'
    source_dir = aqua_dir + r'\docs'
    main_file  = aqua_dir + r'\src\Core\AquaHotkeyX.ahk'
    index_file = fr'{source_dir}\api-overview.md'

    docset_name = 'AquaHotkey'
    docset_alias = 'aqua'
    docset_path = environ.get('LOCALAPPDATA') \
                + r'\Zeal\Zeal\docsets' \
                + '\\' + docset_name + '.docset'

    res_path  = docset_path + r'\Contents\Resources'
    dest_path = res_path + r'\Documents'
    db_path   = res_path + r'\docSet.dsidx'

    # Clean up previous docset if exists
    if exists(res_path):
        rmtree(res_path)
        print(f'Removed: "{res_path}"')

    # Create docset directories
    makedirs(dest_path, exist_ok=True)
    generate_plist(docset_path + r'\Contents\info.plist', docset_name, docset_alias)

    # Generate/update meta
    docset_version = '3.0.0'
    with open(main_file, 'r', encoding='utf-8') as f:
        match = re.search(r'@version([^\r\n]+)', f.read())
        if match:
            docset_version = match.group(1).strip()

    generate_meta(docset_path + r'\docset.json', docset_name, docset_alias, docset_version)
    print(f'Version: {docset_version}')

    copytree(
        source_dir, dest_path,
        dirs_exist_ok=True
    )
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

    for entry in parse_markdown_index(index_file, source_dir):
        cur.execute(
            '''INSERT OR IGNORE INTO searchIndex(name, type, path)
               VALUES (?, ?, ?)''',
            (entry['name'], entry['type'], entry['path']))

    db.commit()
    db.close()

    # Compress for publication
    # import tarfile
    # import json
    # with tarfile.open(docset_name + '.tgz', 'w:gz') as tar:
    #    tar.add(docset_name, arcname=docset_name)

    print(f'Created docset: "{docset_path}"')


def parse_markdown_index(index_path, source_dir):
    """Parse markdown index file and extract documentation entries."""
    entries = []

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for line in content.split('\n'):
        # Match markdown links: [Name](./path/to/file.md)
        match = re.search(r'^.*?\[([^\]]+)\]\(([^\)]+)\)', line)
        if not match:
            continue

        name = match.group(1)
        rel_path = match.group(2)
        clean_path = (rel_path
          .replace('./', '')
          .replace('\\', '/'))

        section = clean_path.split('/')[0]

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


def generate_plist(path, name, search_keyword):
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
    <string>https://www.google.com/search?q=site%3Aahx-docs</string>

    <key>dashIndexFilePath</key>
    <string>index.md</string>

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

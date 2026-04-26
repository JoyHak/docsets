import sqlite3
from os import makedirs, listdir, environ
from os.path import exists
from shutil import rmtree, copy
from re import search as regexMatch
from bs4 import BeautifulSoup

# noinspection SpellCheckingInspection
def generate_docset():
    global sections

    # File structure
    source_dir  = 'chm'
    docset_name = 'XYplorer'
    docset_alias = 'xy'
    docset_path = environ.get('LOCALAPPDATA') \
                + r'\Zeal\Zeal\docsets' \
                + '\\' + docset_name + '.docset'

    res_path    = docset_path + r'\Contents\Resources'  # meta, resources
    dest_path   = res_path + r'\Documents'
    db_path     = res_path + r'\docSet.dsidx'           # docset index
    hhk_path    = fr'{source_dir}\{docset_name}.hhk'    # keywords definition

    # Clean up previous docset if exists
    if exists(res_path):
        rmtree(res_path)
        print(fr'Removed: "{res_path}"')

    # Create docset directories
    makedirs(dest_path, exist_ok=True)
    generate_plist(docset_path + r'\Contents\info.plist', docset_name, docset_alias)

    # Generate/update meta
    docset_version = '28.10.0000'
    with open(fr'{source_dir}\idh_intro.htm', 'r', encoding='utf-8') as f:
        match = regexMatch(r'Help for XYplorer ([^ ]+)', f.read())
        if match:
            docset_version = match.group(1)

    generate_meta(docset_path + r'\docset.json', docset_name, docset_alias, docset_version)
    print(f'Version: {docset_version}')

    # Copy all relevant files
    for file in listdir(source_dir):
        if file.endswith(('.htm', '.html', '.css', '.js', '.png')):
            copy(fr'{source_dir}\{file}', dest_path)

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

    # Parse Keyword Index for all definitions
    with open(hhk_path, 'r', encoding='utf-8') as f:
        hhk_content = f.read()

    soup = BeautifulSoup(hhk_content, 'html.parser')
    for li in soup.find('ul').find_all('li'):
        obj = li.find('object')
        if not obj:
            continue

        name_param  = obj.find('param', {'name': 'Name'})
        local_param = obj.find('param', {'name': 'Local'})
        if not name_param or not local_param:
            continue

        name = name_param['value']
        path = local_param['value']
        file = path.split('#')[0]
        section = sections.get(file, 'Advanced')

        cur.execute(
         '''INSERT OR IGNORE INTO searchIndex(name, type, path)
            VALUES (?, ?, ?)''',
            (name, section, path))

        # print(f'Indexed: {name} ({section}) -> {path}')

    db.commit()
    db.close()

    # Compress for publication
    # import tarfile
    # import json
    # with tarfile.open('XYplorer.tgz', 'w:gz') as tar:
    #    tar.add(docset_name, arcname=docset_name)

    print(f'Created docset: "{docset_path}"')

# based on .\chm\XYplorer.hhc
# noinspection SpellCheckingInspection
sections = {
    "idh_scripting_comref.htm": "Command",
    "idh_scripting_comref_get.htm": "Get",
    "idh_scripting.htm": "Scripting",
    "idh_commandlineswitches.htm": "CLI",
    "idh_variables.htm": "Variable",
    "idh_intro.htm": "Start",
    "idh_install.htm": "Start",
    "idh_removal.htm": "Start",
    "idh_glossary.htm": "Start",
    "idh_settings.htm": "Config",
    "idh_mls.htm": "Config",
    "idh_short.htm": "Config",
    "idh_startupini.htm": "Config",
    "idh_tweaks.htm": "Config",
    "idh_menfile.htm": "Menu",
    "idh_menedit.htm": "Menu",
    "idh_menview.htm": "Menu",
    "idh_mengo.htm": "Menu",
    "idh_menfav.htm": "Menu",
    "idh_mentags.htm": "Menu",
    "idh_menuser.htm": "Menu",
    "idh_menscripting.htm": "Menu",
    "idh_menpanes.htm": "Menu",
    "idh_mentabsets.htm": "Menu",
    "idh_mentools.htm": "Menu",
    "idh_menwindow.htm": "Menu",
    "idh_menhelp.htm": "Menu",
    "idh_raf.htm": "Main",
    "idh_quicknamesearch.htm": "Main",
    "idh_visualfilters.htm": "Main",
    "idh_lfb.htm": "Main",
    "idh_colorfilters.htm": "Main",
    "idh_tags.htm": "Main",
    "idh_addressbar.htm": "Main",
    "idh_toolbar.htm": "Main",
    "idh_tabs.htm": "Main",
    "idh_tabsets.htm": "Main",
    "idh_bc.htm": "Main",
    "idh_treeview.htm": "Main",
    "idh_minitree.htm": "Main",
    "idh_glider.htm": "Main",
    "idh_listview.htm": "Main",
    "idh_hoverbox.htm": "Main",
    "idh_customcolumns.htm": "Main",
    "idh_dual_pane.htm": "Main",
    "idh_syncfolders.htm": "Main",
    "idh_catalog.htm": "Main",
    "idh_clickandsearch.htm": "Main",
    "idh_status.htm": "Main",
    "idh_statusbarbuttons.htm": "Main",
    "idh_panel.htm": "Main",
    "idh_fileinfo.htm": "Main",
    "idh_iptabversion.htm": "Main",
    "idh_ipmeta.htm": "Main",
    "idh_prev.htm": "Main",
    "idh_fileview.htm": "Main",
    "idh_iptags.htm": "Main",
    "idh_find.htm": "Main",
    "idh_report.htm": "Main",
    "idh_preview.htm": "Main",
    "idh_floatingpreview.htm": "Main",
    "idh_previewpane.htm": "Main",
    "idh_searchtemplates.htm": "Main",
    "idh_flatview.htm": "Main",
    "idh_darkmode.htm": "Main",
    "idh_ghostfilter.htm": "Main",
    "idh_paperfolders.htm": "Main",
    "idh_virtualfolders.htm": "Main",
    "idh_fvs.htm": "Main",
    "idh_cfi.htm": "Main",
    "idh_cks.htm": "Main",
    "idh_mencustom.htm": "Main",
    "idh_mendd.htm": "Main",
    "idh_copyfiles.htm": "Main",
    "idh_richop.htm": "Main",
    "idh_backup.htm": "Main",
    "idh_undo.htm": "Main",
    "idh_recyclebin.htm": "Main",
    "idh_portabledevices.htm": "Main",
    "idh_adminsettings.htm": "Advanced",
    "idh_fileassociations.htm": "Advanced",
    "idh_pom.htm": "Advanced",
    "idh_user_defined_commands.htm": "Advanced",
    "idh_hamburger.htm": "Advanced",
    "idh_reg.htm": "Legal",
    "idh_contact.htm": "Legal",
    "idh_disclaimer.htm": "Legal",
    "idh_copyright.htm": "Legal"
}

def generate_meta(path, name, alias, version):
    name_ = name.lower()

    content = f'''{{
    "name": "{name}",
    "version": "{version}",
    "archive": "{name}.tgz",
    "author": {{
        "name": "Rafaello",
        "link": "https://github.com/JoyHak"
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
    <string>https://www.google.com/search?q=site%3Axyplorer.com </string>

    <key>dashIndexFilePath</key>
    <string>idh_scripting_comref.htm</string>

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

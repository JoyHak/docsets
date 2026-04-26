#!/usr/bin/env python3
import os
import shutil
import sqlite3
import tarfile
import json
from bs4 import BeautifulSoup

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

def generate_docset():
    global sections

    source_dir  = 'Chm'
    docset_name = 'XYplorer.docset'
    res_path    = os.path.join(docset_name, 'Contents', 'Resources')  # meta + resources
    dest_path   = os.path.join(res_path,    'Documents')     # resources
    db_path     = os.path.join(res_path,    'docSet.dsidx')  # database
    hhk_path    = os.path.join(source_dir,  'XYplorer.hhk')  # keywords
    
    # Clean up previous docset if exists
    if os.path.exists(res_path):
        shutil.rmtree(res_path)

    # Create docset directories
    os.makedirs(dest_path, exist_ok=True)

    # Copy all relevant files
    for file in os.listdir(source_dir):
        if file.endswith(('.htm', '.html', '.css', '.js', '.png')):
            shutil.copy(os.path.join(source_dir, file), dest_path)

    # Initialize SQLite database
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    cur.execute('DROP TABLE IF EXISTS searchIndex;')
    cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    # Parse Keyword Index for all definitions
    with open(hhk_path, 'r', encoding='utf-8') as f:
        hhk_content = f.read()

    soup = BeautifulSoup(hhk_content, 'html.parser')
    ul = soup.find('ul')

    if ul:
        for li in ul.find_all('li'):
            obj = li.find('object')
            if obj:
                name_param  = obj.find('param', {'name': 'Name'})
                local_param = obj.find('param', {'name': 'Local'})
                if name_param and local_param:
                    name = name_param['value']
                    path = local_param['value']
                    file = path.split('#')[0]
                    section = sections.get(file, 'Advanced')

                    cur.execute(
                        'INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                        (name, section, path))

                    print(f'Indexed: {name} ({section}) -> {path}')

    db.commit()
    db.close()

    # Compress for publication
    # with tarfile.open('XYplorer.tgz', 'w:gz') as tar:
    #    tar.add(docset_name, arcname=docset_name)

    print("XYplorer docset generated successfully")

if __name__ == "__main__":
    generate_docset()

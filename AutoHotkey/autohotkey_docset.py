import sqlite3
# from os import makedirs, walk, environ
from os import makedirs, environ
# from os.path import exists, relpath, dirname
from os.path import exists
# from shutil import rmtree, copy
from shutil import rmtree, copytree, ignore_patterns
from re import search as regexMatch
from bs4 import BeautifulSoup

# noinspection SpellCheckingInspection
def generate_docset():
    global sections

    # File structure
    source_dir  = 'chm'
    docset_name = 'AutoHotkey'
    docset_alias = 'ahk'
    docset_path = environ.get('LOCALAPPDATA') \
                + r'\Zeal\Zeal\docsets' \
                + '\\' + docset_name + '.docset'

    res_path    = docset_path + r'\Contents\Resources'  # meta, resources
    dest_path   = res_path + r'\Documents'
    db_path     = res_path + r'\docSet.dsidx'           # docset index
    hhk_path    = fr'{source_dir}\Index.hhk'    # keywords definition

    # Clean up previous docset if exists
    if exists(res_path):
        rmtree(res_path)
        print(fr'Removed: "{res_path}"')

    # Create docset directories
    makedirs(dest_path, exist_ok=True)
    generate_plist(docset_path + r'\Contents\info.plist', docset_name, docset_alias)

    # Generate/update meta
    docset_version = '2.0.21'
    with open(fr'{source_dir}\docs\index.htm', 'r', encoding='utf-8') as f:
        match = regexMatch(r'<!--ver-->([^<]+)<!--\/ver-->', f.read())
        if match:
            docset_version = match.group(1)

    generate_meta(docset_path + r'\docset.json', docset_name, docset_alias, docset_version)
    print(f'Version: {docset_version}')

    # Copy all relevant files recursively
    # for root, dirs, files in walk(source_dir):
    #     for file in files:
    #         if file.endswith(('.htm', '.html', '.css', '.js', '.png', '.ahk', '.eot', '.svg', '.ttf', '.woff')):
    #             src_path    = fr'{root}\{file}'
    #             rel_path    = relpath(src_path, source_dir)
    #             target_path = fr'{dest_path}\{rel_path}'
    #
    #             makedirs(dirname(target_path), exist_ok=True)
    #             copy(src_path, target_path)

    copytree(
        source_dir, dest_path,
        ignore=ignore_patterns('$*', '#*', '_NUL', '*.hhk'),
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
    # with tarfile.open('AutoHotkey.tgz', 'w:gz') as tar:
    #    tar.add(docset_name, arcname=docset_name)

    print(f'Created docset: "{docset_path}"')

# based on .\chm\docs\static\source\data_toc.js
# noinspection SpellCheckingInspection
sections = {
    "docs/Compat.htm": "External",
    "docs/Concepts.htm": "Syntax",
    "docs/FAQ.htm": "Frequently Asked Questions",
    "docs/Functions.htm": "Syntax",
    "docs/HotkeyFeatures.htm": "Advanced",
    "docs/Hotkeys.htm": "Syntax",
    "docs/Hotstrings.htm": "Syntax",
    "docs/KeyList.htm": "Syntax",
    "docs/Language.htm": "Syntax",
    "docs/ObjList.htm": "Object",
    "docs/Objects.htm": "Syntax",
    "docs/Program.htm": "Syntax",
    "docs/Scripts.htm": "Syntax",
    "docs/Tutorial.htm": "Tutorial",
    "docs/Variables.htm": "Syntax",
    "docs/howto/Install.htm": "Tutorial",
    "docs/howto/ManageWindows.htm": "Tutorial",
    "docs/howto/RunExamples.htm": "Tutorial",
    "docs/howto/RunPrograms.htm": "Tutorial",
    "docs/howto/SendKeys.htm": "Tutorial",
    "docs/howto/WriteHotkeys.htm": "Tutorial",
    "docs/index.htm": "Quick Reference",
    "docs/lib/A_Clipboard.htm": "Environment",
    "docs/lib/A_HotkeyModifierTimeout.htm": "Input",
    "docs/lib/A_MaxHotkeysPerInterval.htm": "Input",
    "docs/lib/A_MenuMaskKey.htm": "Input",
    "docs/lib/Any.htm": "Object",
    "docs/lib/Array.htm": "Object",
    "docs/lib/Block.htm": "Statement",
    "docs/lib/BlockInput.htm": "Input",
    "docs/lib/Break.htm": "Statement",
    "docs/lib/Buffer.htm": "External",
    "docs/lib/CallbackCreate.htm": "External",
    "docs/lib/CaretGetPos.htm": "Input",
    "docs/lib/Catch.htm": "Statement",
    "docs/lib/Chr.htm": "String",
    "docs/lib/Class.htm": "Object",
    "docs/lib/Click.htm": "Input",
    "docs/lib/ClipWait.htm": "Environment",
    "docs/lib/ClipboardAll.htm": "Environment",
    "docs/lib/ComCall.htm": "External",
    "docs/lib/ComObjActive.htm": "External",
    "docs/lib/ComObjArray.htm": "External",
    "docs/lib/ComObjConnect.htm": "External",
    "docs/lib/ComObjFlags.htm": "External",
    "docs/lib/ComObjFromPtr.htm": "External",
    "docs/lib/ComObjGet.htm": "External",
    "docs/lib/ComObjQuery.htm": "External",
    "docs/lib/ComObjType.htm": "External",
    "docs/lib/ComObjValue.htm": "External",
    "docs/lib/ComObject.htm": "External",
    "docs/lib/ComValue.htm": "External",
    "docs/lib/Continue.htm": "Statement",
    "docs/lib/Control.htm": "Window",
    "docs/lib/ControlAddItem.htm": "Window",
    "docs/lib/ControlChooseIndex.htm": "Window",
    "docs/lib/ControlChooseString.htm": "Window",
    "docs/lib/ControlClick.htm": "Input",
    "docs/lib/ControlDeleteItem.htm": "Window",
    "docs/lib/ControlFindItem.htm": "Window",
    "docs/lib/ControlFocus.htm": "Window",
    "docs/lib/ControlGetChecked.htm": "Window",
    "docs/lib/ControlGetChoice.htm": "Window",
    "docs/lib/ControlGetClassNN.htm": "Window",
    "docs/lib/ControlGetEnabled.htm": "Window",
    "docs/lib/ControlGetFocus.htm": "Window",
    "docs/lib/ControlGetHwnd.htm": "Window",
    "docs/lib/ControlGetIndex.htm": "Window",
    "docs/lib/ControlGetItems.htm": "Window",
    "docs/lib/ControlGetPos.htm": "Window",
    "docs/lib/ControlGetStyle.htm": "Window",
    "docs/lib/ControlGetText.htm": "Window",
    "docs/lib/ControlGetVisible.htm": "Window",
    "docs/lib/ControlHide.htm": "Window",
    "docs/lib/ControlHideDropDown.htm": "Window",
    "docs/lib/ControlMove.htm": "Window",
    "docs/lib/ControlSend.htm": "Input",
    "docs/lib/ControlSetChecked.htm": "Window",
    "docs/lib/ControlSetEnabled.htm": "Window",
    "docs/lib/ControlSetStyle.htm": "Window",
    "docs/lib/ControlSetText.htm": "Window",
    "docs/lib/ControlShow.htm": "Window",
    "docs/lib/ControlShowDropDown.htm": "Window",
    "docs/lib/CoordMode.htm": "Input",
    "docs/lib/Critical.htm": "Statement",
    "docs/lib/DateAdd.htm": "Math",
    "docs/lib/DateDiff.htm": "Math",
    "docs/lib/DetectHiddenText.htm": "Window",
    "docs/lib/DetectHiddenWindows.htm": "Window",
    "docs/lib/DirCopy.htm": "File",
    "docs/lib/DirCreate.htm": "File",
    "docs/lib/DirDelete.htm": "File",
    "docs/lib/DirExist.htm": "File",
    "docs/lib/DirMove.htm": "File",
    "docs/lib/DirSelect.htm": "GUI",
    "docs/lib/DllCall.htm": "External",
    "docs/lib/Download.htm": "Misc",
    "docs/lib/Drive.htm": "Drive",
    "docs/lib/DriveEject.htm": "Drive",
    "docs/lib/DriveGetCapacity.htm": "Drive",
    "docs/lib/DriveGetFileSystem.htm": "Drive",
    "docs/lib/DriveGetLabel.htm": "Drive",
    "docs/lib/DriveGetList.htm": "Drive",
    "docs/lib/DriveGetSerial.htm": "Drive",
    "docs/lib/DriveGetSpaceFree.htm": "Drive",
    "docs/lib/DriveGetStatus.htm": "Drive",
    "docs/lib/DriveGetStatusCD.htm": "Drive",
    "docs/lib/DriveGetType.htm": "Drive",
    "docs/lib/DriveLock.htm": "Drive",
    "docs/lib/DriveSetLabel.htm": "Drive",
    "docs/lib/DriveUnlock.htm": "Drive",
    "docs/lib/Edit.htm": "Misc",
    "docs/lib/EditGetCurrentCol.htm": "Window",
    "docs/lib/EditGetCurrentLine.htm": "Window",
    "docs/lib/EditGetLine.htm": "Window",
    "docs/lib/EditGetLineCount.htm": "Window",
    "docs/lib/EditGetSelectedText.htm": "Window",
    "docs/lib/EditPaste.htm": "Window",
    "docs/lib/Else.htm": "Statement",
    "docs/lib/Enumerator.htm": "Object",
    "docs/lib/EnvGet.htm": "Environment",
    "docs/lib/EnvSet.htm": "Environment",
    "docs/lib/Error.htm": "Object",
    "docs/lib/Exit.htm": "Statement",
    "docs/lib/ExitApp.htm": "Statement",
    "docs/lib/File.htm": "Object",
    "docs/lib/FileAppend.htm": "File",
    "docs/lib/FileCopy.htm": "File",
    "docs/lib/FileCreateShortcut.htm": "File",
    "docs/lib/FileDelete.htm": "File",
    "docs/lib/FileEncoding.htm": "File",
    "docs/lib/FileExist.htm": "File",
    "docs/lib/FileGetAttrib.htm": "File",
    "docs/lib/FileGetShortcut.htm": "File",
    "docs/lib/FileGetSize.htm": "File",
    "docs/lib/FileGetTime.htm": "File",
    "docs/lib/FileGetVersion.htm": "File",
    "docs/lib/FileInstall.htm": "File",
    "docs/lib/FileMove.htm": "File",
    "docs/lib/FileOpen.htm": "File",
    "docs/lib/FileRead.htm": "File",
    "docs/lib/FileRecycle.htm": "File",
    "docs/lib/FileRecycleEmpty.htm": "File",
    "docs/lib/FileSelect.htm": "GUI",
    "docs/lib/FileSetAttrib.htm": "File",
    "docs/lib/FileSetTime.htm": "File",
    "docs/lib/Float.htm": "Math",
    "docs/lib/For.htm": "Statement",
    "docs/lib/Format.htm": "String",
    "docs/lib/FormatTime.htm": "String",
    "docs/lib/Func.htm": "Object",
    "docs/lib/GetKeyName.htm": "Input",
    "docs/lib/GetKeySC.htm": "Input",
    "docs/lib/GetKeyState.htm": "Input",
    "docs/lib/GetKeyVK.htm": "Input",
    "docs/lib/GetMethod.htm": "Misc",
    "docs/lib/Goto.htm": "Statement",
    "docs/lib/GroupActivate.htm": "Window",
    "docs/lib/GroupAdd.htm": "Window",
    "docs/lib/GroupClose.htm": "Window",
    "docs/lib/GroupDeactivate.htm": "Window",
    "docs/lib/Gui.htm": "GUI",
    "docs/lib/GuiControl.htm": "GUI",
    "docs/lib/GuiControls.htm": "GUI",
    "docs/lib/GuiCtrlFromHwnd.htm": "GUI",
    "docs/lib/GuiFromHwnd.htm": "GUI",
    "docs/lib/GuiOnCommand.htm": "GUI",
    "docs/lib/GuiOnEvent.htm": "GUI",
    "docs/lib/GuiOnNotify.htm": "GUI",
    "docs/lib/HasBase.htm": "Misc",
    "docs/lib/HasMethod.htm": "Misc",
    "docs/lib/HasProp.htm": "Misc",
    "docs/lib/HotIf.htm": "Input",
    "docs/lib/Hotkey.htm": "Input",
    "docs/lib/Hotstring.htm": "Input",
    "docs/lib/If.htm": "Statement",
    "docs/lib/ImageSearch.htm": "Screen",
    "docs/lib/InStr.htm": "String",
    "docs/lib/IniDelete.htm": "File",
    "docs/lib/IniRead.htm": "File",
    "docs/lib/IniWrite.htm": "File",
    "docs/lib/InputBox.htm": "GUI",
    "docs/lib/InputHook.htm": "Input",
    "docs/lib/InstallKeybdHook.htm": "Input",
    "docs/lib/InstallMouseHook.htm": "Input",
    "docs/lib/Integer.htm": "Math",
    "docs/lib/Is.htm": "Misc",
    "docs/lib/IsLabel.htm": "Misc",
    "docs/lib/IsObject.htm": "Misc",
    "docs/lib/IsSet.htm": "Misc",
    "docs/lib/KeyHistory.htm": "Input",
    "docs/lib/KeyWait.htm": "Input",
    "docs/lib/ListHotkeys.htm": "Input",
    "docs/lib/ListLines.htm": "Misc",
    "docs/lib/ListVars.htm": "Misc",
    "docs/lib/ListView.htm": "GUI",
    "docs/lib/ListViewGetContent.htm": "Window",
    "docs/lib/LoadPicture.htm": "GUI",
    "docs/lib/Loop.htm": "Statement",
    "docs/lib/LoopFiles.htm": "File",
    "docs/lib/LoopParse.htm": "String",
    "docs/lib/LoopRead.htm": "File",
    "docs/lib/LoopReg.htm": "Registry",
    "docs/lib/Map.htm": "Object",
    "docs/lib/Math.htm": "Math",
    "docs/lib/Menu.htm": "GUI",
    "docs/lib/MenuFromHandle.htm": "GUI",
    "docs/lib/MenuSelect.htm": "Window",
    "docs/lib/Monitor.htm": "Monitor",
    "docs/lib/MonitorGet.htm": "Monitor",
    "docs/lib/MonitorGetCount.htm": "Monitor",
    "docs/lib/MonitorGetName.htm": "Monitor",
    "docs/lib/MonitorGetPrimary.htm": "Monitor",
    "docs/lib/MonitorGetWorkArea.htm": "Monitor",
    "docs/lib/MouseClick.htm": "Input",
    "docs/lib/MouseClickDrag.htm": "Input",
    "docs/lib/MouseGetPos.htm": "Input",
    "docs/lib/MouseMove.htm": "Input",
    "docs/lib/MsgBox.htm": "GUI",
    "docs/lib/NumGet.htm": "External",
    "docs/lib/NumPut.htm": "External",
    "docs/lib/Number.htm": "Math",
    "docs/lib/ObjAddRef.htm": "External",
    "docs/lib/ObjBindMethod.htm": "Advanced",
    "docs/lib/Object.htm": "Object",
    "docs/lib/OnClipboardChange.htm": "Environment",
    "docs/lib/OnError.htm": "Statement",
    "docs/lib/OnExit.htm": "Statement",
    "docs/lib/OnMessage.htm": "GUI",
    "docs/lib/Ord.htm": "String",
    "docs/lib/OutputDebug.htm": "Misc",
    "docs/lib/Pause.htm": "Statement",
    "docs/lib/Persistent.htm": "Misc",
    "docs/lib/PixelGetColor.htm": "Screen",
    "docs/lib/PixelSearch.htm": "Screen",
    "docs/lib/PostMessage.htm": "Window",
    "docs/lib/Process.htm": "Process",
    "docs/lib/ProcessClose.htm": "Process",
    "docs/lib/ProcessExist.htm": "Process",
    "docs/lib/ProcessGetName.htm": "Process",
    "docs/lib/ProcessGetParent.htm": "Process",
    "docs/lib/ProcessSetPriority.htm": "Process",
    "docs/lib/ProcessWait.htm": "Process",
    "docs/lib/ProcessWaitClose.htm": "Process",
    "docs/lib/Random.htm": "Math",
    "docs/lib/RegCreateKey.htm": "Registry",
    "docs/lib/RegDelete.htm": "Registry",
    "docs/lib/RegDeleteKey.htm": "Registry",
    "docs/lib/RegExMatch.htm": "String",
    "docs/lib/RegExReplace.htm": "String",
    "docs/lib/RegRead.htm": "Registry",
    "docs/lib/RegWrite.htm": "Registry",
    "docs/lib/Reload.htm": "Statement",
    "docs/lib/Return.htm": "Statement",
    "docs/lib/Run.htm": "Process",
    "docs/lib/RunAs.htm": "Process",
    "docs/lib/Send.htm": "Input",
    "docs/lib/SendLevel.htm": "Input",
    "docs/lib/SendMessage.htm": "Window",
    "docs/lib/SendMode.htm": "Input",
    "docs/lib/SetControlDelay.htm": "Window",
    "docs/lib/SetDefaultMouseSpeed.htm": "Input",
    "docs/lib/SetKeyDelay.htm": "Input",
    "docs/lib/SetMouseDelay.htm": "Input",
    "docs/lib/SetNumScrollCapsLockState.htm": "Input",
    "docs/lib/SetRegView.htm": "Registry",
    "docs/lib/SetStoreCapsLockMode.htm": "Input",
    "docs/lib/SetTimer.htm": "Statement",
    "docs/lib/SetTitleMatchMode.htm": "Window",
    "docs/lib/SetWinDelay.htm": "Window",
    "docs/lib/SetWorkingDir.htm": "File",
    "docs/lib/Shutdown.htm": "Process",
    "docs/lib/Sleep.htm": "Statement",
    "docs/lib/Sort.htm": "String",
    "docs/lib/Sound.htm": "Sound",
    "docs/lib/SoundBeep.htm": "Sound",
    "docs/lib/SoundGetInterface.htm": "Sound",
    "docs/lib/SoundGetMute.htm": "Sound",
    "docs/lib/SoundGetName.htm": "Sound",
    "docs/lib/SoundGetVolume.htm": "Sound",
    "docs/lib/SoundPlay.htm": "Sound",
    "docs/lib/SoundSetMute.htm": "Sound",
    "docs/lib/SoundSetVolume.htm": "Sound",
    "docs/lib/SplitPath.htm": "File",
    "docs/lib/StatusBarGetText.htm": "Window",
    "docs/lib/StatusBarWait.htm": "Window",
    "docs/lib/StrCompare.htm": "String",
    "docs/lib/StrGet.htm": "String",
    "docs/lib/StrLen.htm": "String",
    "docs/lib/StrLower.htm": "String",
    "docs/lib/StrPtr.htm": "String",
    "docs/lib/StrPut.htm": "String",
    "docs/lib/StrReplace.htm": "String",
    "docs/lib/StrSplit.htm": "String",
    "docs/lib/String.htm": "String",
    "docs/lib/SubStr.htm": "String",
    "docs/lib/Suspend.htm": "Input",
    "docs/lib/Switch.htm": "Statement",
    "docs/lib/SysGet.htm": "Environment",
    "docs/lib/SysGetIPAddresses.htm": "Environment",
    "docs/lib/Thread.htm": "Statement",
    "docs/lib/Throw.htm": "Statement",
    "docs/lib/ToolTip.htm": "GUI",
    "docs/lib/TraySetIcon.htm": "GUI",
    "docs/lib/TrayTip.htm": "GUI",
    "docs/lib/TreeView.htm": "GUI",
    "docs/lib/Trim.htm": "String",
    "docs/lib/Try.htm": "Statement",
    "docs/lib/Type.htm": "Advanced",
    "docs/lib/Until.htm": "Statement",
    "docs/lib/VarSetStrCapacity.htm": "String",
    "docs/lib/VerCompare.htm": "String",
    "docs/lib/While.htm": "Statement",
    "docs/lib/Win.htm": "Window",
    "docs/lib/WinActivate.htm": "Window",
    "docs/lib/WinActivateBottom.htm": "Window",
    "docs/lib/WinActive.htm": "Window",
    "docs/lib/WinClose.htm": "Window",
    "docs/lib/WinExist.htm": "Window",
    "docs/lib/WinGetClass.htm": "Window",
    "docs/lib/WinGetClientPos.htm": "Window",
    "docs/lib/WinGetControls.htm": "Window",
    "docs/lib/WinGetControlsHwnd.htm": "Window",
    "docs/lib/WinGetCount.htm": "Window",
    "docs/lib/WinGetID.htm": "Window",
    "docs/lib/WinGetIDLast.htm": "Window",
    "docs/lib/WinGetList.htm": "Window",
    "docs/lib/WinGetMinMax.htm": "Window",
    "docs/lib/WinGetPID.htm": "Window",
    "docs/lib/WinGetPos.htm": "Window",
    "docs/lib/WinGetProcessName.htm": "Window",
    "docs/lib/WinGetProcessPath.htm": "Window",
    "docs/lib/WinGetStyle.htm": "Window",
    "docs/lib/WinGetText.htm": "Window",
    "docs/lib/WinGetTitle.htm": "Window",
    "docs/lib/WinGetTransColor.htm": "Window",
    "docs/lib/WinGetTransparent.htm": "Window",
    "docs/lib/WinHide.htm": "Window",
    "docs/lib/WinKill.htm": "Window",
    "docs/lib/WinMaximize.htm": "Window",
    "docs/lib/WinMinimize.htm": "Window",
    "docs/lib/WinMinimizeAll.htm": "Window",
    "docs/lib/WinMove.htm": "Window",
    "docs/lib/WinMoveBottom.htm": "Window",
    "docs/lib/WinMoveTop.htm": "Window",
    "docs/lib/WinRedraw.htm": "Window",
    "docs/lib/WinRestore.htm": "Window",
    "docs/lib/WinSetAlwaysOnTop.htm": "Window",
    "docs/lib/WinSetEnabled.htm": "Window",
    "docs/lib/WinSetRegion.htm": "Window",
    "docs/lib/WinSetStyle.htm": "Window",
    "docs/lib/WinSetTitle.htm": "Window",
    "docs/lib/WinSetTransColor.htm": "Window",
    "docs/lib/WinSetTransparent.htm": "Window",
    "docs/lib/WinShow.htm": "Window",
    "docs/lib/WinWait.htm": "Window",
    "docs/lib/WinWaitActive.htm": "Window",
    "docs/lib/WinWaitClose.htm": "Window",
    "docs/lib/_ClipboardTimeout.htm": "Directive",
    "docs/lib/_DllLoad.htm": "Directive",
    "docs/lib/_ErrorStdOut.htm": "Directive",
    "docs/lib/_HotIf.htm": "Directive",
    "docs/lib/_HotIfTimeout.htm": "Directive",
    "docs/lib/_Hotstring.htm": "Directive",
    "docs/lib/_Include.htm": "Directive",
    "docs/lib/_InputLevel.htm": "Directive",
    "docs/lib/_MaxThreads.htm": "Directive",
    "docs/lib/_MaxThreadsBuffer.htm": "Directive",
    "docs/lib/_MaxThreadsPerHotkey.htm": "Directive",
    "docs/lib/_NoTrayIcon.htm": "Directive",
    "docs/lib/_Requires.htm": "Directive",
    "docs/lib/_SingleInstance.htm": "Directive",
    "docs/lib/_SuspendExempt.htm": "Directive",
    "docs/lib/_UseHook.htm": "Directive",
    "docs/lib/_Warn.htm": "Directive",
    "docs/lib/_WinActivateForce.htm": "Directive",
    "docs/lib/index.htm": "Function",
    "docs/license.htm": "Advanced",
    "docs/misc/Ahk2ExeDirectives.htm": "Syntax",
    "docs/misc/ControlID.htm": "Window",
    "docs/misc/DPIScaling.htm": "Environment",
    "docs/misc/Editors.htm": "Syntax",
    "docs/misc/EscapeChar.htm": "Advanced",
    "docs/misc/FontsStandard.htm": "GUI",
    "docs/misc/Functor.htm": "Object",
    "docs/misc/ImageHandles.htm": "GUI",
    "docs/misc/Labels.htm": "Syntax",
    "docs/misc/Languages.htm": "Advanced",
    "docs/misc/LongPaths.htm": "File",
    "docs/misc/Macros.htm": "Advanced",
    "docs/misc/Override.htm": "Advanced",
    "docs/misc/Performance.htm": "Advanced",
    "docs/misc/RegEx-QuickRef.htm": "String",
    "docs/misc/RegExCallout.htm": "Advanced",
    "docs/misc/Remap.htm": "Syntax",
    "docs/misc/RemapController.htm": "Advanced",
    "docs/misc/SendMessage.htm": "Advanced",
    "docs/misc/SendMessageList.htm": "Advanced",
    "docs/misc/Styles.htm": "GUI",
    "docs/misc/Threads.htm": "Syntax",
    "docs/misc/WinTitle.htm": "Window",
    "docs/misc/Winamp.htm": "Advanced",
    "docs/misc/remove-userchoice.reg": "Advanced",
    "docs/scripts/index.htm": "Advanced",
    "docs/search.htm": "Advanced",
    "docs/settings.htm": "Advanced",
    "docs/AHKL_DBGPClients.htm": "Advanced",
    "docs/ChangeLog.htm": "Change",
    "docs/v1-changes.htm": "Change",
    "docs/v2-changes.htm": "Change",
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
    <string>https://www.autohotkey.com/docs/v2/</string>

    <key>dashIndexFilePath</key>
    <string>docs/index.htm</string>

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

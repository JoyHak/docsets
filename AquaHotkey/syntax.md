```ahk
variable
%deref%
Fn(A_AhkPath, %deref%)
Function(%deref%, MsgBox(), [1, 2, 3])
a.Method(%deref%, MsgBox(), [1, 2, 3])
a.__PrivateMethod()
a.__Item[0x1]
a.__item
a.__get(m)
MsgBox()
this.Method('data')
super.Method(Integer(1))
Array.Push(Float(1.333))
Any
Any.member
Any.Push(1, 2, 3)
String(A_AhkPath)
throw MemoryError()
throw Error()

(*) => false
FatArrow(*) => false
FatArrow(Args*) => (SubStr(args[1]))
FatArrow(Args*) => SubStr(args[1]) . SubStr(args[1])

def() {
    if (a ~= "[\/^%]  (?<path>[^\$=:\>`"`']*white) | text (?<=\G) \$ (?: (?<paren>\( (?: [^\(\)\r\n]+ | (?&paren)) \)) | (?<brace> { [^{}\r\n]+ }) | [\w\-\.:]+) \K(?&path) \K") {
        return
    }

    s := SubStr(args[1]) . SubStr(args[1])
    s := 'aaa"d"' . d . "fff'a'f`'`"\n`n" . a
}

Show22()
AutoTrim "Off"
AutoTrim "On"
On Off False True 
f.v22
power.stop
#SingleInstance off 
#Include <data> 

send "+{Delete}"	; full name in { }
send "^+D"			; just 1 letter
send "^+Del"		; only 1st would be interpreted as key
send "CapsLock"		; not a key!
send 'text Delete and some {CapsLock 2}' so Delete		; some text and keys in { }
send "+s some {Delete} and some {CapsLock 12}"			; mod+key and some text					

; special characters are interpreted literally
send "{Raw}#f ^!d s{o}me {CapsLock}"					
send "{Text} {Caps} {Delete} Winand some CapsLock" 

; just strings
send "& $ * ~ "
Tooltip "+s some {Delete} and some {CapsLock 12}"
MsgBox "+s some {Delete} and some {CapsLock 12}"

; Перенезначение сочетаний клавиш в приложениях с помощью #Hotif.

#Requires Autohotkey v2.0
#Include <reload>   
#Include <jetbrainsGroup>   

GroupAdd("jetbrains", "ahk_exe notepad++.exe")

try TraySetIcon "C:\Users\ToYu\Pictures\icons\clay_square\iHash.png"
KeyHistory(false)
CoordMode('Mouse', 'Screen')


    +!XButton1::{
        path := WinGetProcessPath("A")
        name := WinGetProcessName("A")
        WinTitle   := "ahk_exe " name
        WaitTimout := 10 
        
        processQuery := 
        (Join`s
           "select processId, commandLine 
            from Win32_Process 
            where CommandLine like '%" name "%'"
        )
        
        for p in ComObjGet("winmgmts:").ExecQuery(processQuery) {
            if !InStr(p.commandLine, path)
                continue
                
            WinClose(WinTitle)
            WinWaitNotActive(WinTitle, , WaitTimout)
            Run(p.commandLine)
            
            if WinWaitActive(WinTitle, , WaitTimout) {
                WinActivate(WinTitle) 
            } 
        }
                
    }

    #^r::{
        SendInput('#r')
        if !KeyWait('Enter', 'DT7')
            return
        
        winId := 0
        loop {
            loop 4 {
                try {
                    ControlClick('Edit3', 'A')  
                } catch {
                    Sleep(500)
                }
            }
            
            if !winId {
                winId := WinExist('A')
                WinSetTitle('$', winId)
            } else if !WinActive(winId) {
                return
            }
            
            if !KeyWait('Enter', 'DT15')
                return
                
            if !WinWaitActive('ahk_class #32770', , 2, '$') {
                WinHide(winId)
                return
            } else {
                SendInput('{Enter}')
            }
        }
    }
```

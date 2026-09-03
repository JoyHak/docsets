```ahk
variable
%deref%
Fn(A_AhkPath, %deref%())
Function(MsgBox(%deref%()), [1, 2, 3])
a.Method(a.%deref%, MsgBox(), [1, 2, 3])
%a[1].a%
a.__PrivateMethod()
a.__Item[0x1].a
a.__item.a
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

class Version extends Any {
__New() {
}
}

FatArrow() => false
FatArrow(Args*) => (SubStr(args[1]))
FatArrow(Args?) => SubStr(args[1]) . SubStr(args[1])

def(arg, args?) {
    if (a ~= "[\/^%]  (?<path>[^=:\$\>`"`']*white) | text (?<=\G) \$ (?: (?<paren>\( (?: [^{}%\(\)]+ | (?&paren)) \)))") {
    }
    r := 'm)\b\1\2$0[:=\\]\w+
    (?#comment)(*PRUNE)(*F)(?R)(?=:)(?!%^&[^*])(?=[$%])
    (?<!%^&[^*])'

    s := SubStr() . SubStr()
    s := SubStr() 'str' a "str" . SubStr()
    s := "str" SubStr()
    s := 'aaa"d"' . d . "fff'a'f`'`"\n`n" . a
    
    return unset
}

fn := () => false
fn := (*) => (false, "True", SubStr())

processQuery := 
(comment
   "select processId, commandLine  ; comment
    from Win32_Process`; 
    where CommandLine like '%" name "%'"
)

#SingleInstance off 
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
                } catch TargetError as Ex {
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

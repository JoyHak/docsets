```ahk
;@Ahk2Exe-SetVersion 2.0.21
;@Ahk2Exe-SetDescription %A_PriorLine~.*"(.*)"~$1%
;@Ahk2Exe-SetMainIcon .ico
;@Ahk2Exe-SetCopyright Rafaello
#Warn Unreachable, Off

;@region Hotkeys, hotstrings
; static (load-time)
::h::Hello
:*:acheiv::achiev for A_this
::achievment::achievement.
:*:adquir::acquir
:*:ftw::Free the whales
::GN::Gui.__New()    ; create
::GT::ToolTip("GC")  ; builtin
::GT::Arr[0].Get()  ; statement
::btw::{
    MsgBox("You typed btw.")
}

#HotIf WinActive("Untitled - Notepad") || GetKeyState("AppsKey", "P")
!q::SendEvent('^t')
!g::Arr[0].Get()
AppsKey::ToolTip("Press < or > to cycle through windows.")
AppsKey Up::ToolTip()
~AppsKey & <::Send("!+{Esc}")
~AppsKey & >::Gui.__New()

; Disable
*<#RCtrl::return
*<#AppsKey::return

; Remaps
^XButton1::^z
Numpad0 & Numpad1::return


; Press AppsKey and Alt in any order, then slash (/).
#HotIf GetKeyState("AppsKey", "P")
    Alt & /::MsgBox("Hotkey activated.")

; If the keys are swapped, Alt must be pressed first (use one at a time):
#HotIf GetKeyState("Alt", "P")
    AppsKey & /::MsgBox("Hotkey activated.")

#HotIf GetKeyState("[") && GetKeyState("]")
    \::MsgBox()

^+e::
    editor_open_folder(*) {
        path := WinGetTitle("A")
        if RegExMatch(path, "file://.+", &path)
            return
        if RegExMatch(path, "m)^\*?\K(.*)\\[^\\]+(?= [-*] )$", &path)
            if (FileExist(path[0]) && A_ThisHotkey = "^+e")
                Run("explorer.exe /select,`"" . path[0] . "`"")
            else
                Run("explorer.exe `"" path[1] "`"")
    }

; This example also demonstrates one way to implement case conformity in a script.
:C:BTW::  ; Typed in all-caps.
:C:Btw::  ; Typed with only the first letter upper-case.
: :btw::  ; Typed in any other combination.
    case_conform_btw(*) {
        hs := A_ThisHotkey  ; For convenience and in case we're interrupted.
        if (hs == ":C:BTW")
            try Send("BY THE WAY")
        else if (hs == ":C:Btw")
            try Send("By the way")
        else
            try Send("by the way")
    }

#HotIf WinActive("ahk_class Notepad", )
    ::btw::This replacement text will appear only in Notepad.
#HotIf
    ::btw::This replacement text appears in windows other than Notepad.

#HotString EndChars -()[]{}:;'"/\,.?!`n `t
Hotstring("EndChars", "-()[]{}:;")

; TODO: fix hotstring functions
::btw::MsgBox("You typed `"``btw```".")
:*:]d::
    MyFunction(FirstParameter, Second := "", &Third := "", Fourth := "") {
        ; This hotstring replaces "]d" with the current date and time via the commands below.
        return "a value"
    }

; dynamic (run-time)
Hotkey("^WheelUp", (*) => 0, "On")
Hotkey("*<#RCtrl", , "Off")
KeyWait("^+s")
GetKeyState('^sc003')
HotString(':*:acheiv::achiev.')
HotString('::btw', , 'Off')
;@endregion

Add(X, Y, Z := 0)  => X + Y + Z
LogToFile(TextToLog) => FileAppend(TextToLog "`n", "l.log")

FatArrow() => false
FatArrow(Args*) => (SubStr(args[1]))
FatArrow(Args?) => SubStr(args[1]) . SubStr(args[1])

fn := (_) => false
fn := (*) => (false, "True", SubStr())
u := unset

; storage modifiers
SetDefaults() {
    global MyGlobal := 33
    local x, y := 0, z
    static count := 0
    
    static dummy := {Color: "Yellow", Taste: "Delicious", Price: 3}
}

/**
 * @param {Integer} Num Unsigned value
 * @returns {Integer}
 * @throws {ValueError|CustomClass}
 */
GetValue(num) {
    switch num {
    case 1:
        SetDefaults()
        break label
    case 2:
        break label
    default:
        throw ValueError(1, 'num', num)
    }
    
    label:
    throw CustomClass(1, 'num', num)
}

label:
popcount() => DllCall("BitSet\popcount", "Ptr", this.B.Ptr, "Ptr", this.B.Size, "cdecl")
goto label

DllCall(
    "WriteProcessMemory", 
    "Ptr", hProcess, 
    "Ptr", lpBaseAddress, 
    "Ptr", lpBuffer, 
    "UInt", nSize, 
    "UInt*", &lpBytesWritten := 0
)

hProcess := DllCall(
    "OpenProcess" 
    , "UInt", PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ 
    , "Int", false 
    , "UInt", WinGetPID("ahk_id " hwnd) 
    , "Ptr"
)

NumPut("UInt", 0x0002, lvFindInfo, 0)               ; LVFI_STRING flag
NumPut("Int",  column, lvFindInfo, A_PtrSize * 3)   ; lParam for column search

DllCall("RtlZeroMemory",
    "Ptr", this.B.Ptr + CurSize,
    "Ptr", ReqSize - CurSize, 
    "thiscall Ptr")
}

Byte := NumGet(this.B, Value >>> 3, "UChar")
if (!(Byte & (1 << (Value & 0x07)))) {
    NumPut("UChar",
            Byte | (1 << (Value & 0x07)),
            this.B,
            Value >>> 3)
}
    
/**
 * `RGB` wrapper. Stores invidual Red, Green, Blue bits.
 * 
 * @param {Integer} aRGB Unsigned RGB value
 * @example
 * c := Color(0xff0000)
 * c.R := 0xf | 0xd
 *
 * red  := Color(0xff0000), red.R -= 5
 * cyan := Color(0), cyan.G := 255, cyan.B := 255
 * @warn This class is designed for syntax test only!
 */ 
class Color {
    static Shift := {R: 16, G: 8, B: 0}
    static Dummy := {Color: "Yellow", Taste: "Delicious", Price: 3}
    
    __New(aRGB) {
        this.RGB := aRGB
        this.stored_RGB := 0x000000
    }
    
    static __New() {
    }

    __Delete() {            
        try {
            this.RGB.__Delete
        } catch ValueError as Ex {
            e := 0
        } catch CustomClass as Cs {
            e := 1
        } catch {
            e := -1
        }
    }
    
    __Enum(num) {
    }

    __Get(aName) {
        ; NOTE: Using this.Shift here would cause an infinite loop!
        shift := Color.Shift[aName]  ; Get the number of bits to shift.
        if (shift != "")  ; Is it a known property?
            return (this.RGB >> shift) & 0xff
        ; NOTE: Using 'return' here would break this.RGB.
    }

    __Set(aName, aValue) {
        shift := Color.Shift[aName]
        if !shift
            return ""

        aValue &= 255
        this.RGB := (aValue << shift) | (this.RGB & ~(0xff << shift))
        return aValue
    }

    ; Meta-functions can be mixed with properties:
    RGB {
        get {
            ; Return it in hex format:
            return format("0x{:06x}", this.stored_RGB)
        }
        set {
            this.stored_RGB := value
        }
    }

    __Item[value] {
        get => this.__RGB.%value%()  ; valid V2 code (dereference)
    }
    
    __Item => 0
    
    static __Item[value] {
        get => 0
    }
    
    Nul(*) => 0x000000
}

class Properties extends Func {
    Call(aTarget, aName, aParams*) {
        ; If this Properties object contains a definition for this half-property, call it.
        return this[aName].Call(aTarget, aParams*)
    }
    
    static Call(*) => Func()
}

red  := Color(0xff0000), red.R -= 5
cyan := Color(0), cyan.G := 255, cyan.B := 255

MsgBox("red: " red.R "," red.G "," red.B " = " red.RGB)
MsgBox("cyan: " cyan.R "," cyan.G "," cyan.B " = " cyan.RGB)

; This example requires the FunctionObject class in order to work.
blue := Color(0x0000ff) ; c
MsgBox(blue.R "," blue.G "," blue.B)

; Paremeters after keyword (without parentheses)
if Color = "Red" or Color = "Green"  or Color = "Blue"    ; no trailing operator = check next line
   Color = "Black" or Color = "Gray" or Color = "White"   ; no leading operator = stop parsing params
    color := 0
    return false

if Color = "White" or  ; trailing operator
   Color = "Black" or  ; trailing operator
   Color == "Cyan" {   ; Comment.
    color := 0
    return false
}

if (Color ~= "\b(red|green)\b")  ; no trailing operator = check next line
or Color = "gray"                ; leading operator
    return false
    
while Color ~= "\b(red|green)\b"  ; comment
    color := "blue"
    
if ((color >> 16) & 0xFF) 
 | (color & 0x00FF00)         ; leading operator
 | ((color & 0xFF) << 16)     ; leading operator
    Fn(Color, true)

return Color == "Red"
    || Color == "Blue" 
    Color == "Cyan"

return {
    Key: Key,
    Value: Value
}

return [
    1, 
    2
]

Return Color(0).__Item[0x0].ToString().MsgBox()
 && Fn(Color, "true")

; Params in parentheses
if (codepage != "")
    codepage := " /CP" . codepage
if (MyVar ~= '\b\1\2$0[:=\\]\w+(?#comment)(*PRUNE)(*F)(?R)(?=:)(?<!&)(?![$%])')

if MyVar ~= '\b\1\2'

; Assignment inside params without parent. checks for non-emptiness|non-zero of the new variable
if (MyVar := "Text")
 && MyVar {
    MyVar := MyVar2
 }
 
if (MyVar := "Text")
 and MyVar
    MyVar := MyVar2

if (MyVar := "a" . "b")
&& MyVar {
    MyVar := MyVar2
 }
 
MyVar := 
{
    p1: 0,
    p2: 0
}

MyVar := 
"Text"
. "Text"  
   
isRgb := 
    Color == "Green" || Color == "Blue"

isRgb := Color == "Red"
      || Color == "Green"
      || Color == "Blue"

cmd:="`"" . A_AhkPath . "`"" . codepage . " `"`%1`" `%*"
key:="AutoHotkeyScript\Shell\Open\Command"
if A_IsAdmin    ; Set for all users.
    RegWrite(cmd, "REG_SZ", "HKCR\" key)
else            ; Set for current user only.
    RegWrite(cmd, "REG_SZ", "HKCU\Software\Classes\" key)

; The characters ^+!# represent the modifier keys Ctrl, Shift, Alt and Win. 
; They affect only the very next key. 
; To send the corresponding modifier key on its own, enclose the key name in braces.
Send("This text has been typed{!}")
Send("{a 2}") 
Send("{a}a{b}b{c}")
Send("^s")                     ; Both of these send CTRL+S
Send("{Ctrl down}s{Ctrl up}")  ; Both of these send CTRL+S
Send("+{Delete}text")	       ; key name must be in { }, everything else is text
SendEvent("^+D")			   ; just 1 letter
SendEvent("^+Del")		       ; only 1st would be interpreted as key
SendInput("CapsLock")		   ; not a key!
SendInput('Delete {Delete 2}')			
'{CapsLock}'
; special characters would be interpreted literally
Send("{Raw}#f ^!d s{o}me {CapsLock}`n")
Send("{Text}{Caps}{Delete}CapsLock`%")
Send("{Blind#^}{Caps}{Delete} CapsLock`%")

Send("$ * ~")    ; hooks are treated literally here
SendText("^{Delete 2}")
SendPlay("^{Delete 2}")

; concatenation
Send("{" . MyVar . " 2}")
Send(
    "{Left}{" 
    . Format(
        "A {}{}", 
        condition ? "DownTemp" : "DownR", 
        Integer("2")
    ) 
    . "}{Right}"
)

; multiline text
Send(
    (LTrim0 Join$
    "{!}A line of text.
    {Enter 2}e
    a{tab}"
    )
)

Send("
(
{!}A line of text.
    {Enter 2}e
    a{tab}
)")

; EXAMPLE #1 - inside a quoted/literal string:
Var := "
(
A line of text.
By default, the hard carriage return (Enter) between the previous line and this one will be stored.
    This line is indented with a tab; by default, that tab will also be stored.  ; literal string
Additionally, "quote marks" are automatically escaped when appropriate.
)"

; EXAMPLE #2 - outside a quoted/literal string:
Var :=
(Join`s`n LTrim0 Comment
"Same as above, except that quote marks are not automatically escaped.  ; comment
Specify variables as follows: " Var "
A line of text."
)

; EXAMPLE #1 - inside a quoted/literal string:
FileAppend('
(
A line of text.
By default, the hard carriage return (Enter) between the previous line and this one will be stored.
	This line is indented with a tab; by default, that tab will also be stored.
)', A_Desktop '\My File.txt')

MsgBox "
(com
A line of text.`r`nBy default, the "quote marks" are automatically escaped  ; comment
)"

; EXAMPLE #2 - outside a quoted/literal string:
FileAppend(
(
"Same as above, except that quote marks are not automatically escaped.
Specify variables as follows: " Var "
A line of text."
), A_Desktop "\My File.txt")

; EXAMPLE #4:
FormatStr := "
(
Another way of using variables with a continuation section.
Input value 1: {1}
Input value 2: {2}
)"

Format("{1:x}{2}", 0x13, 0x14)

; Assign multiline string
section := 
(Join`r`n LTrim0
   "select processId, commandLine  ; comment
    from Win32_Process`; 
    where CommandLine like '%" cmd "%'"
)

s .= Format("{2}, {1}!`r`n", "World", "Hello")
s .= Format('|{:-10}|`r`n|{:10}|`r`n", "Left", "Right')
s .= Format("{1:#x} {2:X} 0x{3:x}`r`n", 3735928559, 195948557, 0)
s .= Format('{1:0.3f} {1:.10f}', 4 * ATan(1))
s .= Format('{{} {} {}}', 4 * ATan(1))

Send(A_Hour)
SubStr(37 * 12, 1, 2)
SubStr(A_Hour - 12, 2)
SubStr("I'm scripting, awesome!", 16)

if (MyVar = 5) {
    MsgBox("MyVar equals " MyVar "!!")
    ExitApp()
}

MsgBox(IsSet)       ; operator, cannot be passed as callback
MsgBox(IsSetRef)    ; built-in function

IsVar := IsSet(Var)
IsVarRef := IsSetRef(&Var)
var := unset
MsgBox(var?)

MyVar := MyVar2
MyVar := MyVar2 . " some text " . MyVar . "."
MyVar := SubStr("I'm scripting, awesome!", 16)
MyVar := "Text"
MyVar := MyVar2
MyVar := 6 + 8 / 3 * 2 - Sqrt(9)
MyVar := "The value of 5 + " MyVar2 " is: " 5 + MyVar2
if (Var1 != Var2)
    Var1 := Var2 + 100
if (MyVar !== MyVar2)   ; case sensitive string compare
    Var1 := Var2 + 200
    
; Some examples showing when to use percents and when not:
Var := "Text"  ; Assign some text to a variable (legacy).
Var2 := Var  ; Assign a variable to another (legacy).
Var3 := Var  ; Assign a variable to another (expression).
Var4 .= Var  ; Append a variable to the end of another (expression).
Var5 += Var  ; Add the value of a variable to another (expression).
Var5 -= Var  ; Subtract the value of a variable from another (expression).
Var6 := SubStr(Var, 2, 2)  ; Variable inside a function. This is always an expression.
Var7 := Var . " Text"  ; Assigns a variable to another with some extra text (legacy).
Var8 := Var " Text"  ; Assigns a variable to another with some extra text (expression).
MsgBox(Var)  ; Variable inside a command.
Var := StrSplit(Var,"x")  ; Variable inside a command that uses InputVar and OutputVar.
if (n = 6) 
if (Var is MyClass or Var is SubClass.Control)
if (Var is Class)   ; technically valid
if (Number(6) = 6) 
if (Var[1] < Var[2])

states := ["true", "on", "false", "off"]
MyArray := ["one", "two", "three", 17]
MyObject := {Color: "Yellow", Taste: "Delicious", Price: 3}
Banana := Map("Color", "Yellow", "Taste", "Delicious", "Price", 3)
Banana["Taste"] := "Weird"
Value := Banana["Color"]
MyObject.NewKey := "Shiny"
MyArray.Push(Var, Var2, MyArray*)
RemovedValue := MyArray.Delete(1)
NumberOfRemovedKeys := MyArray.Delete(2, 4)
arr := [{}]  ; Creates an array containing an object.
arr.RemoveAt(1)  ; Removes and frees the second object.
x := {}, y := {}             ; Create two objects.
x.child := y, y.parent := x  ; Create a circular reference.
y.parent := ""
x := "", y := ""
Banana.__Item["Color"]
RemovedValue := MyArray.RemoveAt(1)
NumberOfRemovedKeys := MyArray.RemoveAt(1, 3)
MyArray.Pop()
MyArray.__Private()
MyArray.__Field
Method%Var%()

Array.prototype
Class.prototype  ; an object, not a keyword
v := Class()     ; instance of Class.prototype
(fn)(Class)      ; retrieve function and call
(MsgBox.Call)("hi")

({}.method)()    ; retrieve method implementation
{}.method()      ; call a method on empty object
({}.__Call)()
(MsgBox.Call)()
(Object.Prototype.DefineProp)()
"".DefineProp("Length", {call: StrLen})

Sleep(1)
MsgBox(1 + 1)  ; Shows "2"
MsgBox("1+1")  ; Shows "1+1"
MsgBox(A_AhkVersion)
MsgBox("Hello " A_UserName ".")

Var := [1, 2]
Low := High := 1
if (Var[1] = Var[2])
if (Var[1] = Var[2])
if (Var[1] >= Low and Var[1] <= High)
if (Var[1] >= Low && Var[1] <= High)

Format("{:L}{:U}{:T}", Var[1], Var[2], Low)

; for-loop only supports variables followed by expression
for a, b, c in [1, 2]
for a, b in Arr.Slice(1, 2).Transform(a => a > 2)
for a, b in StrSplit(
    "1 , 2", 
    ',', 
    A_Space, 2
) {
    MyVar := a
}

; Keyword after `loop` must be literal, comma is optional
Loop Reg "HKEY_LOCAL_MACHINE", "KVR"
loop reg, "HKEY_LOCAL_MACHINE", "KVR" {
    if A_LoopRegType = "key"
        value := ""
}

repeat:
loop read, "Export.txt" {
    loop parse A_LoopReadLine, A_Tab {
        MsgBox "Field number " A_Index " is " A_LoopField "."
        continue repeat
    }
}

;@Ahk2Exe-IgnoreBegin
loop files, SourcePattern {
    copy_it := false
    if !FileExist(Dest "\" A_LoopFileName)  ; Always copy if target file doesn't yet exist.
        copy_it := true
}
;@Ahk2Exe-IgnoreEnd

loop parse, A_Clipboard, "`n", "`r" {
}

; count can be an expression
loop 12
loop MyArray.length
loop Min(MyArray.Length, 2)

/*@Ahk2Exe-Keep 
    ; in .exe only
    Array.prototype
    Class.prototype
    v := Class()
    (fn)(Class)
*/
```

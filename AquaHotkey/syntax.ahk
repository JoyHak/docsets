```ahk
#Warn Unreachable, Off
::ftw::Free the whales ; hotstring label abbreviation
::btw::{  ; hotstring label action
    global
    MsgBox("You typed btw.")
    Run("notepad.exe")  ; Run Notepad when you press CTRL+N.
    MsgBox("Wow!")
    MsgBox("There are")
    Run("notepad.exe")
    WinActivate("Untitled - Notepad")
    Send("7 lines{!}{Enter}")
    SendInput("inside the CTRL{+}J hotkey.")
}

Numpad0 & Numpad1::return

#HotIf WinActive("Untitled - Notepad", )
!q::SendEvent('^t')

; Any window
#HotIf
!q::SendEvent('^t')

; Press Win+↑ to maximize the active window
#Up::WinMaximize("A")

:*:acheiv::achiev
::achievment::achievement
::acquaintence::acquaintance
:*:adquir::acquir
::aquisition::acquisition
:*:agravat::aggravat
:*:allign::align
::ameria::America
:*:ftw::Free the whales ; Hotstring modifiers

*#up::MouseMove(0, -10, 0, "R")  ; Win+UpArrow hotkey => Move cursor upward
*#Down::MouseMove(0, 10, 0, "R")  ; Win+DownArrow => Move cursor downward
*#Left::MouseMove(-10, 0, 0, "R")  ; Win+LeftArrow => Move cursor to the left
*#Right::MouseMove(10, 0, 0, "R")  ; Win+RightArrow => Move cursor to the right

*<#RCtrl::return
*<#AppsKey::return

<^>!m::MsgBox("You pressed AltGr+m.")
<^<!m::MsgBox("You pressed LeftControl+LeftAlt+m.")

AppsKey::ToolTip("Press < or > to cycle through windows.")
AppsKey Up::ToolTip
~AppsKey & <::Send("!+{Esc}")
~AppsKey & >::Send("!{Esc}")

; Press AppsKey and Alt in any order, then slash (/).
#HotIf GetKeyState("AppsKey", "P")
    Alt & /::MsgBox("Hotkey activated.")

; If the keys are swapped, Alt must be pressed first (use one at a time):
#HotIf GetKeyState("Alt", "P")
    AppsKey & /::MsgBox("Hotkey activated.")

#HotIf GetKeyState("[") && GetKeyState("]")
    \::MsgBox()

; Ctrl+Shift+O to open containing folder in Explorer.
; Ctrl+Shift+E to open folder with current file selected.
; Supports SciTE and Notepad++.
^+o::
^+e::
    editor_open_folder(*) {
        path := WinGetTitle("A")
        if RegExMatch(path, "x)\*?\K(.*)\\[^\\]+(?= [-*] )", &path)
            if (FileExist((path&&path[0])) && A_ThisHotkey = "^+e")
                Run("explorer.exe /select,`"" (path&&path[0]) "`"")
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
            Send("BY THE WAY")
        else if (hs == ":C:Btw")
            Send("By the way")
        else
            Send("by the way")
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

Add(X, Y, Z := 0) {
    return X + Y + Z
}

Join(sep, params*) {
    for index,param in params
        str .= param . sep
        
    return SubStr(str, 1, -StrLen(sep))
}

MsgBox(Join("`n", "one", "two", "three"))

LogToFile(TextToLog) {
    FileAppend(TextToLog "`n", "l.log")
}

SetDefaults() {
    global
    MyGlobal := 33
    local x, y := 0, z
}

GetFromStaticArray(WhichItemNumber) {
    static FirstCallToUs := true
    if FirstCallToUs {
        FirstCallToUs := false
        Loop 10 {
            StaticArray%A_Index% := "Value #" . A_Index
        }
    }
    
    return StaticArray%WhichItemNumber%
}

class baseObject {
    static foo := "bar"
}
thing := {}
thing.foo := "bar"
thing.test := thing_test
thing.test()

thing_test(this) {
    MsgBox(this.foo)
}

class Color {
    __New(aRGB) {
        this.RGB := aRGB
        this.stored_RGB := 0x000000
    }

    __Delete() {
        MsgBox("Delete Color.")
    }

    static Shift := {R:16, G:8, B:0}

    __Get(aName) {
        ; NOTE: Using this.Shift here would cause an infinite loop!
        shift := Color.Shift[aName]  ; Get the number of bits to shift.
        if (shift != "")  ; Is it a known property?
            return (this.RGB >> shift) & 0xff
        ; NOTE: Using 'return' here would break this.RGB.
    }

    __Set(aName, aValue) {
        if ((shift := Color.Shift[aName]) != "") {
            aValue &= 255  ; Truncate it to the proper range.

            ; Calculate and store the new RGB value.
            this.RGB := (aValue << shift) | (this.RGB & ~(0xff << shift))

            ; 'Return' must be used to indicate a new key-value pair should not be created.
            ; This also defines what will be stored in the 'x' in 'x := clr[name] := val':
            return aValue
        }
        ; NOTE: Using 'return' here would break this.stored_RGB and this.RGB.
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

    class __RGB {
        R() => ((this.RGB >> 16) & 255)
        G() => ((this.RGB >> 8) & 255)
        B() => (this.RGB & 255)
    }

    __Item[value] {
        get => this.__RGB.%value%()  ; valid V2 code (dereference)
    }
}

class Properties extends Func {
    Call(aTarget, aName, aParams*) {
        ; If this Properties object contains a definition for this half-property, call it.
        return this[aName].Call(aTarget, aParams*)
    }
}

red  := Color(0xff0000), red.R -= 5
cyan := Color(0), cyan.G := 255, cyan.B := 255

MsgBox("red: " red.R "," red.G "," red.B " = " red.RGB)
MsgBox("cyan: " cyan.R "," cyan.G "," cyan.B " = " cyan.RGB)

; This example requires the FunctionObject class in order to work.
blue := Color(0x0000ff)
MsgBox(blue.R "," blue.G "," blue.B)

if (Color = "Red" or Color = "Green"  or Color = "Blue"   ; Comment.
    or Color = "Black" or Color = "Gray" or Color = "White")   ; Comment.

if (codepage != "")
    codepage := " /CP" . codepage
cmd:="`"" . A_AhkPath . "`"" . codepage . " `"`%1`" `%*"
key:="AutoHotkeyScript\Shell\Open\Command"
if A_IsAdmin    ; Set for all users.
    RegWrite(cmd, "REG_SZ", "HKCR\" key)
else            ; Set for current user only.
    RegWrite(cmd, "REG_SZ", "HKCU\Software\Classes\" key)

Send("This text has been typed{!}")
Send("{a}")       ; WRONG
Send("{a}{b}{c}") ; WRONG
Send("{abc}")     ; WRONG
Send("abc")       ; CORRECT
Send("^s")                     ; Both of these send CTRL+S
Send("{Ctrl down}s{Ctrl up}")  ; Both of these send CTRL+S
Send("{Ctrl down}c{Ctrl up}")
Send("{b down}{b up}")
Send("{Tab down}{Tab up}")
Send("{Up down}")  ; Press down the up-arrow key.
Sleep(1000)      ; Keep it down for one second.
Send("{Up up}")    ; Release the up-arrow key.

Send(
(LTrim
"Line 1
Line 2
Apples are a fruit."
))

section := 
(Join`r`n LTrim0
   "select processId, commandLine  ; comment
    from Win32_Process`; 
    where CommandLine like '%" cmd "%'"
)

Send(A_Hour)
SubStr(37 * 12, 1, 2)
SubStr(A_Hour - 12, 2)
SubStr(A_AhkPath, (InStr(A_AhkPath, "AutoHotkey"))<1 ? (InStr(A_AhkPath, "AutoHotkey"))-1 : (InStr(A_AhkPath, "AutoHotkey")))
SubStr("I'm scripting, awesome!", 16)

if (MyVar = 5) {
    MsgBox("MyVar equals " MyVar "!!")
    ExitApp()
}

if (MyVar ~= '\b\1\2$0[:=\\]\w+(?#comment)(*PRUNE)(*F)(?R)(?=:)(?<!&)(?![$%])')
RegExMatch(MyVar, 'x)(?<paren>[^\(\)\r\n]+)\G(?&paren)')
MyVar := "Text"
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
if (Number = 6)  ; Whenever an IF has parentheses, it'll be an expression. So no percent signs.
if (Var != Number)  ; Whenever an IF has parentheses, it'll be an expression. So no percent signs.
if (Number = 6)  ; Without parentheses, the IF is legacy. However, only variables on the 'right side' need percent signs.
if (Var[1] < Var[2])  ; Without parentheses, the IF is legacy. However, only variables on the 'right side' need percent signs.

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
arr[1] := {}  ; Creates a second object, implicitly freeing the first object. ;  V1toV2: Invalid Index errors?, try 'arr.Push(<val>)'
arr.RemoveAt(1)  ; Removes and frees the second object.
x := {}, y := {}             ; Create two objects.
x.child := y, y.parent := x  ; Create a circular reference.
y.parent := ""
x := "", y := ""
Banana.__Item("Color")
RemovedValue := MyArray.RemoveAt(1)
NumberOfRemovedKeys := MyArray.RemoveAt(1, 3)
MyArray.Pop()
%Var%()

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

WatchPOV() {
    global
    POV := GetKeyState("JoyPOV")  ; Get position of the POV control.
    KeyToHoldDownPrev := KeyToHoldDown  ; Prev now holds the key that was down before (if any).

    ; Some joysticks might have a smooth/continous POV rather than one in fixed increments.
    ; To support them all, use a range:
    if (POV < 0)   ; No angle to report
        KeyToHoldDown := ""
    else if (POV > 31500)               ; 315 to 360 degrees: Forward
        KeyToHoldDown := "Up"
    else if (POV >= 0 && POV <= 4500)      ; 0 to 45 degrees: Forward
        KeyToHoldDown := "Up"
    else if (POV >= 4501 && POV <= 13500)  ; 45 to 135 degrees: Right
        KeyToHoldDown := "Right"
    else if (POV >= 13501 && POV <= 22500) ; 135 to 225 degrees: Down
        KeyToHoldDown := "Down"
    else                                ; 225 to 315 degrees: Left
        KeyToHoldDown := "Left"

    if (KeyToHoldDown = KeyToHoldDownPrev)  ; The correct key is already down (or no key is needed).
        return  ; Do nothing.

    ; Otherwise, release the previous key and press down the new key:
    SetKeyDelay(-1)  ; Avoid delays between keystrokes.
    if KeyToHoldDownPrev   ; There is a previous key to release.
        Send("{" KeyToHoldDownPrev " up}")  ; Release it.
    if KeyToHoldDown   ; There is a key to press down.
        Send("{" KeyToHoldDown " down}")  ; Press it down.

}

Dummy() {
    global
    ; Get the text currently selected. The clipboard is used instead of
    ; "ControlGet Selected" because it works in a greater variety of editors
    ; (namely word processors).  Save the current clipboard contents to be
    ; restored later. Although this handles only plain text, it seems better
    ; than nothing:
    ; V1toV2: Removed AutoTrim Off  ; Retain any leading and trailing whitespace on the clipboard.
    ClipboardOld := ClipboardAll()
    A_Clipboard := ""  ; Must start off blank for detection to work.
    Send("^c")
    if !ClipWait(1)  ; timed out.
        return
        
    ; Replace CRLF and/or LF with `n for use in a "send-raw" hotstring:
    ; The same is done for any other characters that might otherwise
    ; be a problem in raw mode:
    s := StrReplace(A_Clipboard, "`, ```, All",,,, 1)  ; Do this replacement first to avoid interfering with the others below.
    s := StrReplace(Hotstring, "`r`n", "``r")  ; Using `r works better than `n in MS Word, etc.
    s := StrReplace(Hotstring, "`n", "``r")
    s := StrReplace(Hotstring, A_Tab, "``t")
    s := StrReplace(Hotstring, "`;", "```;")
    A_Clipboard := ClipboardOld  ; Restore previous contents of clipboard.
    ; This will move the InputBox's caret to a more friendly position:
    
        
    if InStr(Hotstring, ":R`:::") {
        MsgBox("You didn't provide an abbreviation. The hotstring has not been added.")
        return
    }
    ; Otherwise, add the hotstring and reload the script:
    FileAppend("`n" Hotstring, A_ScriptFullPath)  ; Put a `n at the beginning in case file lacks a blank line at its end.
    Reload()
}
```

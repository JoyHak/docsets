```ahk
#Requires AutoHotkey v2.1-alpha.30
#Include <AquaHotkey/AquaHotkey>

class ListViewColoring extends AquaHotkey {
class Gui {
class ListView {
__New() {
    ; Set LVS_EX_DOUBLEBUFFER style to avoid drawing issues.
    this.Opt('+LV0x010000')
    this.CUSTOMDRAW := -12
    
    this.BackColor   := SendMessage(0x1025, 0, 0, this)  ; LVM_GETTEXTBKCOLOR
    this.TextColor   := SendMessage(0x1023, 0, 0, this)  ; LVM_GETTEXTCOLOR

    this.RowsCount := this.GetCount()
    this.ColsCount := this.GetCount("col")
    
    this.Showcolors()
    this.DefineProp("__Delete", { Call: __Delete })
    this.__initialized := true
    
    __Delete() {
        this.Hidecolors()
        if WinExist(this.Hwnd)
           WinRedraw(this.Hwnd)
    }
}

Field[Row, Column := 1] => Gui.ListView.Field(this, Row, Column)

class Field {
    __New(ListView, Row, Column := 1) {        
        if !ListView.HasOwnProp('__initialized') {
            ; GUI controls constructor is not called explicitly
            ListView.__New()
        }
        
        if (row > ListView.RowsCount)
           throw ValueError("Row exceeds the maximum number of rows",, Row)
           
        if (Column > ListView.ColsCount)
           throw ValueError("Column exceeds the maximum number of columns",, Column)
           
        this.DefineProp("ListView", { Get: (_) => ListView })
        this.DefineProp("Row",      { Get: (_) => Row      })
        this.DefineProp("Column",   { Get: (_) => Column   })
    }

    BackColor {
        set => this.SetColor(value)
        get => this.ListView.Colors[this.Row][this.Column]["Back"]
    }

    TextColor {
        set => this.SetColor( , value)
        get => this.ListView.Colors[this.Row][this.Column]["Text"]
    }
    
    SelBackColor {
        set => this.SetColor(value, , this.ListView.SelColors)
        get => this.ListView.SelColors[this.Row][this.Column]["Back"]
    }

    SelTextColor {
        set => this.SetColor( , value, this.ListView.SelColors)
        get => this.ListView.SelColors[this.Row][this.Column]["Text"]
    }
    
    SetColor(back?, text?, colorsMap := this.ListView.Colors) {
        row := this.Row
        col := this.Column
        
        if (colorsMap.Has(row)) {
            if (colorsMap[row].Has(col)) {
                colorsMap[row].Delete(col) 
            } else {
                colorsMap.Delete(row)
            }  
        } 
        
        if (!colorsMap.Has(row)) {
            colorsMap[row] := Map()
            colorsMap[row].default := Map(
                "Back", this.ListView.BackColor,
                "Text", this.ListView.TextColor
            )
        
            colorsMap[row].capacity := Max(this.ListView.ColsCount, col)
        }
  
        colorsMap[row][col] := Map(
            "Back", this.ListView.BGR(back?) ?? this.ListView.BackColor,
            "Text", this.ListView.BGR(text?) ?? this.ListView.TextColor
        )

        return 0
    }
}

SelColors {
    get {
        defaultColor := Map(
            "Back", this.BackColor,
            "Text", this.TextColor
        )
        defaultColor.default := defaultColor
    
        Rows := Map()
        Rows.capacity := this.rowsCount
        Rows.default := defaultColor
        
        this.DefineProp("SelColors", { Get: (_) => Rows })

        return Rows
    }
}

Colors {
    get {
        defaultColor := Map(
            "Back", this.BackColor,
            "Text", this.TextColor
        )
        defaultColor.default := defaultColor
        
        Rows := Map()
        Rows.capacity := this.rowsCount
        Rows.default := defaultColor
        
        this.DefineProp("Colors", { Get: (_) => Rows })

        return Rows        
    }
}

Showcolors() {
    if this.HasOwnProp("onNotifyFunc")
        return false

    this.onNotifyFunc := ObjBindMethod(this, "NM_CUSTOMDRAW")
    this.OnNotify(this.CUSTOMDRAW, this.onNotifyFunc)
    WinRedraw(this.hwnd)
  
    return true
}

Hidecolors() {
    if !this.HasOwnProp("onNotifyFunc")
        return false
        
    this.OnNotify(this.CUSTOMDRAW, this.onNotifyFunc, 0)
    this.DeleteProp("onNotifyFunc")
    WinRedraw(this.hwnd)
    
    return true
}

NM_CUSTOMDRAW(LV, lParam) {
    ; structs offsets
    static SIZE_NMHDR        := A_PtrSize * 3                      ; Size of NMHDR structure
    static SIZE_NCD          := SIZE_NMHDR + 16 + (A_PtrSize * 5)  ; Size of NMCUSTOMDRAW structure
    static OFFSET_ITEM       := SIZE_NMHDR + 16 + (A_PtrSize * 2)  ; Offset of dwItemSpec (NMCUSTOMDRAW)
    static OFFSET_ITEM_STATE := OFFSET_ITEM + A_PtrSize            ; Offset of uItemState (NMCUSTOMDRAW)
                                                                
    static OFFSET_TEXT_CLR   := SIZE_NCD                           ; Offset of clrText    (NMLVCUSTOMDRAW)
    static OFFSET_BACK_CLR   := OFFSET_TEXT_CLR + 4                ; Offset of clrTextBk  (NMLVCUSTOMDRAW)
    static OFFSET_SUBITEM    := OFFSET_BACK_CLR + 4                ; Offset of iSubItem   (NMLVCUSTOMDRAW)
    
    ; current draw stage
    static CDDS_SUBITEMPREPAINT   := 0x030001
    static CDDS_ITEMPREPAINT      := 0x010001
    static CDDS_PREPAINT          := 0x000001
    
    ; returns
    static CDRF_NOTIFYITEMDRAW    := 0x20
    static CDRF_NOTIFYSUBITEMDRAW := 0x020
    static CDRF_NEWFONT           := 0x02

    if (!LV.Hwnd || (NumGet(lParam, 'UPtr') != LV.Hwnd)) {
        return
    }

    Critical(-1)
    DrawStage := NumGet(lParam + SIZE_NMHDR, 'UInt')
    
    ; rows and columns are 1-based
    Row  := NumGet(lParam + OFFSET_ITEM,   'UPtr') + 1
    Col  := NumGet(lParam + OFFSET_SUBITEM, 'Int') + 1
    Item := Row - 1   ; item is 0-based
    
    switch DrawStage {
    case CDDS_SUBITEMPREPAINT:   
        MsgBox('Colorize individual cells')
        ; Colorize individual cells
        ; Set the colors
        NumPut('UInt', LV.Colors[row][col]["Back"], lParam + OFFSET_BACK_CLR)
        NumPut('UInt', LV.Colors[row][col]["Text"], lParam + OFFSET_TEXT_CLR)
        
        if (col <= LV.Colors[row].count)
            return CDRF_NOTIFYSUBITEMDRAW
        
        return 0
    
    case CDDS_ITEMPREPAINT:
        ; Colorize entire row
        static LVM_GETITEMSTATE := 0x102C
        static LVIS_SELECTED    := 0x0002

        if (LV.SelColors.Has(row) 
         && SendMessage(LVM_GETITEMSTATE, item, LVIS_SELECTED, LV.Hwnd)) {
            ; Set selected row color
            
            ; Remove the CDIS_SELECTED and CDIS_FOCUS from uItemState
            static CDIS_SELECTED := 0x0001
            static CDIS_FOCUS    := 0x0010
            flag  := CDIS_SELECTED | CDIS_FOCUS
            
            state := NumGet(lParam + OFFSET_ITEM_STATE, 'UInt')
            NumPut('UInt', state & ~flag, lParam + OFFSET_ITEM_STATE)
            
            ; Set the colors
            NumPut('UInt', LV.SelColors[row][col]["Back"], lParam + OFFSET_BACK_CLR)
            NumPut('UInt', LV.SelColors[row][col]["Text"], lParam + OFFSET_TEXT_CLR)
            
            return CDRF_NEWFONT
        }
        
        try {
        NumPut('UInt', LV.Colors[row][col]["Back"], lParam + OFFSET_BACK_CLR)
        NumPut('UInt', LV.Colors[row][col]["Text"], lParam + OFFSET_TEXT_CLR)
        } catch as ex {
        MsgBox(Format('{}: {} {}`n[{}, {}] {}', ex.what, ex.message, ex.extra, row, col, LV.Colors[row].ToString()), A_ScriptName, 'Iconx')
        }
        return 0
    
    case CDDS_PREPAINT:
        return CDRF_NOTIFYITEMDRAW
        
    default:
        return 0
    }
}

BGR(color?) {
    if (!IsSet(color)  || color = 0)
        return color?
        
    return ((color >> 16) & 0xFF) | (color & 0x00FF00) | ((color & 0xFF) << 16)
}

}
}
}

#Include <AquaHotkey/src/Base/ToString>

G := Gui()
G.SetFont('q5 s11', 'Maple Mono NF CN')
LV := G.AddListView('w800 h300', ['path', 'state', 'date'])
LV.Add(, 'C:\Program Files\AutoHotkey\v2\AutoHotkey64_UIA.exe', 'unset', A_Now)
LV.Add(, 'C:\Program Files\AutoHotkey\v2\AutoHotkey32_UIA.exe', 'unset', A_Now)
LV.Add(, 'C:\Program Files\AutoHotkey\v2\AutoHotkey.exe',       'unset', A_Now)
LV.Add(, 'C:\Program Files\AutoHotkey\v2\AutoHotkey.chm',       'unset', A_Now)
LV.Add(, 'C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe',     'unset', A_Now)
LV.Add(, 'C:\Program Files\AutoHotkey\v2\AutoHotkey32.exe',     'unset', A_Now)
LV.ModifyCol()

LV.Field[1].BackColor    := 0x81e881
LV.Field[1, 2].BackColor := 0x70a5eb
; LV.Field[1, 3].BackColor := 0xe13936
; LV.Field[2].SelBackColor := 0x34e434
; LV.Field[2].SelTextColor := 0

G.Show("autosize")

; Map { 1: Map { 2: red } }
```

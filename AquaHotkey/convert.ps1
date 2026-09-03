Split-Path -Parent $PSCommandPath | Set-Location
pandoc.exe nested.ahk `
    --output syntax.html `
    --from gfm --to html5 `
    --standalone `
    --syntax-definition syntax.xml `
    --css style.css `
    --wrap none
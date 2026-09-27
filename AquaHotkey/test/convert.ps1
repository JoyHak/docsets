Split-Path -Parent $PSCommandPath | Set-Location
pandoc.exe syntax.ahk `
    --output syntax.html `
    --from gfm --to html5 `
    --standalone `
    --syntax-definition ../ahk.xml `
    --css ../style.css `
    --wrap none
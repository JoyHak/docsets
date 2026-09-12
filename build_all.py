from subprocess import run
from pathlib import Path

for script in (
  Path(__file__)
    .parent
    .rglob('*_docset.py')
):
    run(['python', script], cwd=script.parent)

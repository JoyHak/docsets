Your personal reference library, searchable in an instant and available without a connection. Requires [Zeal](https://github.com/zealdocs/zeal) offline documentation browser. [See more docsets here](https://github.com/Kapeli/Dash-User-Contributions).

![](Images/demo.avif)
![](Images/syntax2.png)

### How to use

[Download `.tgz` archives](https://github.com/JoyHak/docsets/releases) (docsets). Exctract them in `%LocalAppData%\Zeal\docsets`. After installing [Zeal](https://github.com/zealdocs/zeal) you'll see your offline documentation on the left pane.

Open `File -> Docset Library`, select the docsets you want, and click the `Download` button.

#### Query and filter docsets

Limit the search scope by prefixing your query with a docset name and a colon:

`ahk:hotkey`

To search multiple docsets, separate them with a comma:

`ahk,aqua:string`

#### Command line

You can also start Zeal with a query from the command line:

`zeal python:pprint`

#### Create your own docsets

Follow the instructions in the [Dash docset generation guide](https://kapeli.com/docsets). Each docset is generated with specific  `*_docset.py` scripts (e.g. [autohotkey_docset](AutoHotkey/autohotkey_docset.py)). You can read them for inspiration. Run [build_all.py](build_all.py) to build all docsets using all builder scripts inside this repository.

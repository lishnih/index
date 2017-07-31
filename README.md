# index

### Installation

```sh
$ python -m easy_install <package.egg>
```
- or
```sh
$ py -3 -m easy_install <package.egg>
```

### After installation

- Now you can run the package from a python environment:
```sh
from index import main
main.main()
```
- or cli mode
```sh
from index import export
export.main(files)
```
```sh
from index import export
export.main(files, "Example list (proceed_default)")
```

Use *tksettings.py* for import setting from plugins
'*proceed_default*', '*proceed_default2*'
(Click 'Import from module' and choose files:
'*proceed_default/presets_default.py*' and
'*proceed_default2/presets_default.py*').

License
----
- MIT

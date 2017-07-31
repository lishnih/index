*************
index
*************

**Installation**

::

  $ python -m easy_install <package.egg>
  $ py -3 -m easy_install <package.egg>

**After installation**

Now you can run the package from a python environment:

::

  from index import main
  main.main()

or cli mode

::

  from index import export
  export.main(files)

::

  from index import export
  export.main(files, "Example list (proceed_default)")

Use *tksettings.py* for import setting from plugins
'*proceed_default*', '*proceed_default2*'
(Click 'Import from module' and choose files:
'*proceed_default/presets_default.py*' and
'*proceed_default2/presets_default.py*').

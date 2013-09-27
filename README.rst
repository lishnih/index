===========
index
===========

INSTALLATION
------------
::

   sudo easy_install index

HOW TO USE
----------

::

  from index import main
  main.main()

or cli

::

  from index import export
  export.main(files)

  from index import export
  export.main(files, "Example list (proceed_default)")

Use *tksettings.py* for import setting from plugins
'*proceed_default*', '*proceed_default2*'
(Click 'Import from module' and choose files:
'*proceed_default/presets_default.py*' and
'*proceed_default2/presets_default.py*').

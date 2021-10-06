```python
# Instantiate an extension of Environment with custom functions
# such as "jcompile" and "jtest".
e = JEnvironment(...)

# The following hack allows to avoid the Import("*") call and the exports
# parameter of the SConscript() call in SConscript files.
SCons.Script._SConscript.GlobalDict.update(
    {
        "e": e,
        "jcompile": e.jcompile,
        "jtest": e.jtest,
    }
)
```

## Use external files with scons, e.g. a linker script

In some cases, you need to give tools additional files per command line, e.g. a linker script to a linker. The easiest way would be to manipulate the SConscript environment variables, like: 

```python
env = Environment()
# force scons to use '/usr/bin/ld' as linker (not gcc)
env['LINK'] = '/usr/bin/ld'
# pass it a linker script per commandline
env['LINKFLAGS']+=' -T linkerscript.lds '
```
However, the disadvantages of this are 

1. SCons doesn't know what you're doing 
1. You need to give a filename relative to the SConstruct directory (i.e. `src/subtree1/linkerscript.lds`) 
1. SCons doesn't add the file to the dependencies (you could do this manually with `Depends(program, filename)`) 
1. It's (of course) unportable (ok, with the linkerscripts example that doesn't make sense, since linkerscripts mostly are unportable, but there maybe more examples, where portability makes sense) 
A solution may be to write a [custom Builder](CustomBuilders). 

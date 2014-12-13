
Program() 

Tells SCons to build an executable given a list of sources. A very simple example is 
```python
#!python 
## Beginning of script
sources = [ "foo.c", "bar.c" ];
Program( 'my_program', sources );
```
On Unix the resulting program will be 'my_program', on Windows the resulting program will be 'my_program.exe'. 

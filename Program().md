
Program() 

Tells SCons to build an executable given a list of sources. A very simple example is 

```python 
## Beginning of script
sources = ["foo.c", "bar.c"]
Program('my_program', sources)
```

On Unix the resulting filename will be `my_program`, on Windows the resulting program will be `my_program.exe`. If this file needs to be referred to later, save the return from calling `Program`, it will be a node which includes the correct computed name - this saves having to write operating-system conditional code for target filenames.

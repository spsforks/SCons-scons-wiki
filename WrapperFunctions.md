**How to write a scons wrapper function ?**


**WARNING: as of SCons 0.98, the API provides the [AddMethod](http://scons.org/doc/production/HTML/scons-user.html#chap-add-method) function (more portable and API-safe).**


If you have a sequence of SCons operations that's not well-captured by a Builder, or you just want to wrap up some SCons functions into a neat callable package, you probably want to make it look like a regular SCons environment method.  Here's how to do that:

Let's say you have this (just for example):


```python
#!python
sources = ["foo.c", "bar.c", "main.c"]
env = Environment()
BuildDir("build", ".", duplicate = 0)
build_sources = ["build/" + filename for filename in sources]
prog = env.Program("build/program", build_sources)
Default(prog)
```

and you want to wrap it up so you can do that kind of thing in several places.  Write a normal python function making sure an Environment is its first arg:

```python
#!python
def BuildProgramInDir(env, program, sources):
   BuildDir("build", ".", duplicate=0)
   build_sources = ["build/" + filename for filename in sources]
   prog = env.Program("build/"+program, build_sources)
   Default(prog)
```

then to make it callable as an Environment method, do this (_pre-0.98; otherwise use AddMethod)_:

```python
#!python
from SCons.Script.SConscript import SConsEnvironment # just do this once
SConsEnvironment.BuildProgramInDir = BuildProgramInDir
```

then you can call it as usual:

```python
#!python
env=Environment()
sources = ["foo.c", "bar.c", "main.c"]
env.BuildProgramInDir('program', sources)
```

There are many more useful things you can do with this, from simple renaming of standard methods to complex pathname manipulations to automatically building and installing in one command. Have fun!

Here's another wrapper example that handles targets, sources, and overrides in the same way that ordinary SCons builders do. In this example, I want to define a wrapper that will automatically add a certain library when building my test programs.


```python
#!python
from SCons.Script.SConscript import SConsEnvironment
# Define _null (used to detect missing target arg in wrapper functions)
class _Null:
    pass
_null = _Null
def MyTestProgram( env, target=None, source=_null, **kw ):
    '''Build a test program, adding utest library to link automatically.'''
    # Reassign args if no target specified
    if source is _null:
        source = target
        target = None
   # Add utest to the list of libraries
    if 'LIBS' in kw:
        libs = kw.pop( 'LIBS' )
    else:
        libs = []
    kw['LIBS'] = [ 'utest' ] + libs
    # Use ordinary Program builder to build the program
    program = env.Program( target, source, **kw )
    # Must build the utest library first
    env.Depends( program, env['LIBPREFIX'] + 'utest' + env['LIBSUFFIX'] )
    return program
# Add wrapper to environment
SConsEnvironment.MyTestProgram = MyTestProgram
env = Environment()
env.Library( 'utest', 'usub1.c' )
# Specify just the source
env.MyTestProgram( 'test1.c' )
# Specify both target and source
env.MyTestProgram( 'renamed_test2', 'test2.c' )
# Specify just source with an override for CCFLAGS
env.MyTestProgram( 'test3.c', CCFLAGS='/nologo /O1' )
```


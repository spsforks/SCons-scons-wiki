**Table of Contents**

[TOC]

If you're familiar with `make` utility, **SCons** is a replacement for it. As the `make` utility looks for a **Makefile**, SCons looks for a **SConstruct** file by default. SConstruct file is a Python script. _Note that you do not have to know Python or `make` for basic operation with this build tool._

See [SconsProcessOverview](SconsProcessOverview) for a high level view of SCons processing.

## SConstruct and Environment

**SCons** main file is the `SConstruct` file. When calling the `scons` script, it will automatically search for this file in the current directory.

All SCons API are available for usage from SConstruct, including the **Environment** class.

You must first instantiate this class (this is not strictly required, but you'll need it sooner or later, so best do it right away):

```python
#!python
env = Environment()
```

This sets up a basic environment. Afterwards, you can set up build targets.

```python
env.Program(target='bar', source=['foo.c'])
```

This will make a program 'bar' from source file 'foo.c'.

For more complex programs you must set up a more specialized environment. For example, setting up the flags the compiler will use, include directories, etc.

To do that you can specify named parameters such as CCFLAGS for C files or CPPFLAGS for the C++ Preprocessor. More of these can be seen below in this article and also in the [Configuration File Reference](http://www.scons.org/doc/production/HTML/scons-man.html#configuration_file_reference) section of the [man page](http://www.scons.org/doc/production/HTML/scons-man.html).

```python
#!python

# directly when constructing your Environment
env = Environment(CCFLAGS='-O3')

# ... or appending it later
env.Append(CCFLAGS='-O3')
```

Some parameters require specific lists, such as the source list. Reading the Configuration File Reference should be very helpful.


## Specifying A Default Target

An important note is the Default command. It tells scons what to build by default. It will not build anything unless you specify a target otherwise.

```python
t = env.Program(target='bar', source=['foo.c'])
Default(t)
```

You can call Default many times to add to the default target list.

**Tip:**
You can pass the target name to Default(), but Steven Knight (author of SCons) recommends that you use the return value from your target as the default value instead of specifying the name. He explains it best: "The only stylistic suggestion I'll make is that if you use the object returned by env.Program as the input to Default(), then you'll be more portable, since you won't have to worry about whether the generated program will have a .exe suffix or not."


## Some Common tasks

A few common tasks are shown below. (_Note that, although these examples mostly use 'Append',  you can also specify the same information by using the same flags when calling e.g. Program()_)

Add flags from a config
```python
env.ParseConfig('pkg-config --cflags glib-2.0')
```

Add header search path
```python
env.Append(CPPPATH = ['/usr/local/include/'])
```

Add compile-time flags
```python
env.Append(CCFLAGS = ['-g','-O3'])
```

Add define
```python
env.Append(CPPDEFINES=['BIG_ENDIAN'])
```

Add define with value (e.g. -DRELEASE_BUILD=1)
```python
env.Append(CPPDEFINES={'RELEASE_BUILD' : '1'})
```

Add library search path
```python
env.Append(LIBPATH = ['/usr/local/lib/'])
```

Add libraries to link against
```python
env.Append(LIBS = ['SDL_image','GL'])
```

Link time flags
```python
env.Append(LINKFLAGS = ['-Wl,--rpath,/usr/local/lib/'])
```

Building a more complex program that the example outlined above from several source files can be done the following way:
```python
sources = [ 'main.cpp', 'utils.cpp', 'gui.cpp' ]
env.Program(target = 'a.out', source = sources)
```

## SConscript and variant dir

Most of the time you will want to do hierarchical builds, giving the responsability of building a particular module/library/subprogram to a subscript rather than stuffing everything in to the SConstruct file.
In SCons this kind of script is called a SConscript.

In order to keep the build clean, each SConscript will usually produce its build targets in a different *variant directory*.
By doing this, sources and produced targets for a given configuration are separated from other configurations.

A typical example is building the same targets in release and debug modes:

```python
SConscript('SConscript', variant_dir='build_release', duplicate=0, exports={'MODE':'release'})
SConscript('SConscript', variant_dir='build_debug',   duplicate=0, exports={'MODE':'debug'})
```


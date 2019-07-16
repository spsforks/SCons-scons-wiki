If you are familiar with the `make` utility, **SCons** has similar aims: build a software or documentation project based on a description of the project you provide. As the `make` utility looks for a **Makefile**, SCons looks for a **SConstruct** file by default. The language used to tell SCons about your project is Python, extended by a set of interfaces (API) specific to SCons. _Note that you do not have to know Python or `make` for basic operation with this build tool._

See [SconsProcessOverview](SconsProcessOverview) for a high level view of SCons processing.

## SConstruct and Environment

The main build configuration script for **SCons** is the `SConstruct` file. When the `scons` script is called, it will automatically search for this file in the current directory (actually, several alternate names are also searched for and will be used if found `Sconstruct`, `sconstruct`, `SConstruct.py`, `Sconstruct.py`, `sconstruct.py`).

The full SCons API is available for usage from SConstruct, including the **Environment** class. The Environment class describes a **Construction Environment** which controls a build; a build configuration may have several of these if there are different instructions for different parts of the build. Typically a build configuration instantiates this class very early, although it's certainly not required to do so at the very top. 

```python
env = Environment()
```
This sets up a basic environment. Now, you can set up build targets.

```python
env.Program(target='bar', source=['foo.c'])
```
This tells SCons that `bar` is made from source file `foo.c`. SCons has rules for lots of common build tasks so you don't have to describe the actual commands to use. The Program builder figures out that this is a C language build and the the appropriate Action will invoke the appropriate C compiler to build it. Behind the scenes, SCons will also work out if there are other dependencies - for example if `foo.c` includes header files, and maybe those header files include other header files, those are all added to the dependency graph, and SCons can detect when `bar` needs to be rebuilt if any of those dependencies go out of date. This is a big improvement over older build systems that could not detect if a rebuild was needed due to a dependency unless you explicitly called out the dependency.

For more complex programs you must set up a more specialized environment. For example, setting up the flags the compiler will use, additional directories to search for include files, etc.

To do that you can specify named parameters such as `CCFLAGS` for C files or `CPPFLAGS` for the C++ Preprocessor. More of these can be seen below in this article and also in the [Configuration File Reference](http://www.scons.org/doc/production/HTML/scons-man.html#configuration_file_reference) section of the [man page](http://www.scons.org/doc/production/HTML/scons-man.html).

```python
# directly when constructing your Environment
env = Environment(CCFLAGS='-O3')

# ... or appending it later
env.Append(CCFLAGS='-O3')
```

Some parameters require specific lists, such as the source list. Reading the [Configuration File Reference](http://www.scons.org/doc/production/HTML/scons-man.html#configuration_file_reference) should be very helpful.

## Specifying A Default Target

An important note is the **Default** command. It tells scons what to build by default. Scons always builds the targets it is given on the command line, and any targets that are necessary to be able to build the specifid targets. Default helps set up the list to build if no targets are given on the command line.  If Default is not used, scons selects all the targets for building, which may be too much in a larger project.

```python
t = env.Program(target='bar', source=['foo.c'])
Default(t)
```

You can call Default many times to build up the default target list. If it later turns out you want to build everything in spite of having a default list, you can give the current directory as an argument to scons, as in:

```python
scons .
```

**Tip:**
You can pass the target name to Default(), but Steven Knight (author of SCons) recommends that you use the return value from your target as the default value instead of specifying the name. He explains it best: "The only stylistic suggestion I'll make is that if you use the object returned by `env.Program` as the input to `Default()`, then you'll be more portable, since you won't have to worry about whether the generated program will have a `.exe` suffix or not."


## Some Common tasks

A few common tasks are shown below. (_Note that, although these examples mostly use 'Append',  you can also specify the same information by using the same flags when calling e.g. Program()_). 


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

Add flags from a config (the `ParseConfig` method sorts the result of running an external command into the appropriate buckets - effectively it does an `Append` to `CPPDEFINES`, `CCFLAGS`, `LINKFLAGS`, etc. as necessary (see [ParseFlags in the manpage](https://scons.org/doc/3.0.5/HTML/scons-man.html#f-ParseFlags) for details):

```python
env.ParseConfig('pkg-config --cflags glib-2.0')
```

Building a more complex program that the example outlined above from several source files can be done the following way:
```python
sources = [ 'main.cpp', 'utils.cpp', 'gui.cpp' ]
env.Program(target = 'a.out', source = sources)
```

## Extending the configuration: SConscript

As soon as the project extends beyond "extremely simple", you will probably want to set up hierarchical builds, giving the responsability of describing a particular module/library/subprogram to a subsidiary script rather than stuffing everything in to the SConstruct file. These scripts are by default named `SConscript` (the same variation of names as show for `SConstruct` above also work here), and are invoked by a call to the `SConscript` method. A simple case might be to put the code for a library in a lib subdirectory, and test code in a test subdirectory.

```python
SConscript('lib/SConscript')
SConscript('src/SConscript')
```

##  Supporting mutiple builds: Variant directory

Many projects need to support building in several different ways from the same sources.  A common case is a "debug" build with support for examining objects with debuggers, etc. and a "release" build that is stripped and optimized. SCons has the capability of supporting this through an instruction that tells it to use a *variant directory*. A variant directory is a build-specific location where the targets are placed, while the sources continue to come from the common location.

Here is an example building the same targets in release and debug modes; in addition to setting the distinct variant directories, in this example a flag named `MODE` is passed to the SConscript so it can determine which build it is doing, and set up the environment for that build appropriately.

```python
SConscript('SConscript', variant_dir='build_release', duplicate=0, exports={'MODE':'release'})
SConscript('SConscript', variant_dir='build_debug',   duplicate=0, exports={'MODE':'debug'})
```


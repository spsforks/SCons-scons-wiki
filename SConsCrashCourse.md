**Table of Contents**

[TOC]

If you're familiar with `make` utility, **SCons** is a replacement for it. As the `make` utility looks for a **Makefile**, SCons looks for a **SConstruct** file by default. SConstruct file is a Python script. _Note that you do not have to know Python or `make` for basic operation with this build tool._ 

See [SconsProcessOverview](SconsProcessOverview) for a high level view of SCons processing. 

When running scons it will automatically make all its API available for usage from SConstruct, including **Environment** class. You must first instantiate this class (this is not strictly required, but you'll need it sooner or later, so best do it right away) : 


```python
#!python
env = Environment()
```
This sets up a basic environment. Afterwards, you can set up targets. 


```python
#!python
env.Program(target='bar', source=['foo.c'])
```
This will make a program 'bar' from 'foo.c'. 

For more complex programs you must set up a more specialized environment. For example, setting up the flags the compiler will use, include directories, etc. 

To do that you can specify named parameters such as CCFLAGS for C files or CPPFLAGS for the C++ Preprocessor. More of these can be seen below in this article and also in the [Configuration File Reference](http://www.scons.org/doc/HTML/scons-man.html#lbAF) section of the [man page](http://www.scons.org/doc/HTML/scons-man.html). 


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
#!python
t = env.Program(target='bar', source=['foo.c'])
Default(t)
```

<div>
[[!img http://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Im-jabber.svg/48px-Im-jabber.svg.png] ******Tip****** 

You can pass the target name to Default(), but Steven Knight (author of SCons) recommends that you use the return value from your target as the default value instead of specifying the name. He explains it best: "The only stylistic suggestion I'll make is that if you use the object returned by env.Program as the input to Default(), then you'll be more portable, since you won't have to worry about whether the generated program will have a .exe suffix or not." 
</div>
You can call Default many times to add to the default target list. 


## Some Common tasks

A few common tasks are shown below. (_Note that, although these examples mostly use 'Append',  you can also specify the same information by using the same flags when calling e.g. Program()_) 

Add flags from a config 
```python
#!python
env.ParseConfig( 'pkg-config --cflags glib-2.0' )
```
Add header search path 
```python
#!python
env.Append(CPPPATH = ['/usr/local/include/'])
```
Add compile-time flags 
```python
#!python
env.Append(CCFLAGS = ['-g','-O3'])
```
Add define 
```python
#!python
env.Append(CPPDEFINES=['BIG_ENDIAN'])
```
Add define with value (e.g. -DRELEASE_BUILD=1) 
```python
#!python
env.Append(CPPDEFINES={'RELEASE_BUILD' : '1'})
```
Add library search path 
```python
#!python
env.Append(LIBPATH = ['/usr/local/lib/'])
```
Add libraries to link against 
```python
#!python
env.Append(LIBS = ['SDL_image','GL'])
```
Link time flags 
```python
#!python
env.Append(LINKFLAGS = ['-Wl,--rpath,/usr/local/lib/'])
```
Building a more complex program that the example outlined above can be done the following way : 
```python
#!python
sources = Split("""
main.cpp
utils.cpp
gui.cpp
""")
object_list = env.Object(source = sources)
env.Program( target = 'a.out', source = object_list )
```

## SConscript and build dir

To avoid struggle, make sure you create at least two scripts - SConstruct and SConscript. This will allow you to build into a separate folder from your source files, and eventually this will allow you to harness more of the power of scons. Example: `SConscript('SConscript', build_dir='.build', duplicate=0) ` And then you put all the usual stuff from the examples inside SConscript instead of SConstruct. I was hammering at this for an hour trying to do it all in one file, but the build_dir functionality just wouldn't cooperate until I did this, now I'm in heaven. Now that you've done it this way, you can pass some values into your SConscript and call it multiple times: 


```python
#!python
SConscript('SConscript', build_dir='.build_release', duplicate=0, exports={'MODE':'release'})
SConscript('SConscript', build_dir='.build_debug', duplicate=0, exports={'MODE':'debug'})
```
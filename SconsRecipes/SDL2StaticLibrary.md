
This is a quick tutorial about how to build [SDL 2](http://www.libsdl.org) as a static library on Linux. 

The static library will be used to create a basic program which opens a window, nothing fancy, but it’s a good proof of concept to check everything works as expected. 

A detailed explanation and an archive containing all the files is available on my [blog](http://blog.davidecoppola.com/2014/03/13/building-sdl-2-with-scons-on-linux/). 


## The project Hierarchy

For this simple project I decided to have the following hierarchy: 


```txt
my_scons_project/
|
+---- bin/
|
+---- build/
|
+---- SConstruct
|
+---- src/
      +---- game/
      |     +---- main.cpp
      |     |---- SConscript
      |
      +---- libs/
            +---- SDL2/
                  +---- SConscript
```

## The SConstruct

This is the main SCons script in the project’s root: 


```python
#!python 
# 3 build modes
vars = Variables()
vars.Add(EnumVariable('mode', 'Building mode', 'debug', allowed_values=('debug', 'profile', 'release')))

env = Environment(variables = vars)
Help(vars.GenerateHelpText(env))

# basic flags according to build mode
if env['mode'] == 'debug':
    env.Append(CCFLAGS = ['-Wall', '-g', '-O0', '-DDEBUG'])
elif env['mode'] == 'release':
    env.Append(CCFLAGS = ['-Wall', '-O3', '-DNDEBUG'])
    env.Append(LINKFLAGS = ['-s'])
elif env['mode'] == 'profile':
    env.Append(CCFLAGS = ['-Wall', '-pg', '-O0', '-DNDEBUG'])

env.Append(CCFLAGS = ['-DLINUX'])

# LIBS
SConscript('src/libs/SDL2/SConscript', exports = 'env', variant_dir = 'build/' + env['mode'], src_dir = 'src', duplicate = 0)

# GAME
SConscript('src/game/SConscript', exports = 'env', variant_dir = 'build/' + env['mode'], src_dir = 'src', duplicate = 0)
```
It allows to specify a “mode” parameter which controls the building mode (debug, profile, release). 


## The 2 SConscript

This is the SConscript in_ src/game/_ : 


```python
#!python 
Import('env')

print '[I] building game (' + env['mode'] + ')'

# create a local environment cloning the imported one
localEnv = env.Clone();

# sources
sources = Split(""" main.cpp """)

# flags
localEnv.Append(CCFLAGS = ['-D_REENTRANT'])
localEnv.Append(LINKFLAGS=['-Wl,--no-undefined'])

# libraries
localEnv.Append(LIBS = ['SDL2', 'pthread', 'm', 'dl', 'ts', 'pthread', 'rt'])

# paths
localEnv.Append(CPPPATH=['#/src/libs/SDL2/include'])
localEnv.Append(LIBPATH = ['../libs/SDL2'])

# build an executable
localEnv.Program('#/bin/%s/game/my_game' % localEnv['mode'], sources)
```
And this is the one in _src/libs/SDL2/_ : 


```python
#!python 
Import('env')

print '[I] building SDL2 (' + env['mode'] + ')'

# create a local environment cloning the imported one
localEnv = env.Clone();

# sources
sources = Split(""" src/SDL.c
                    ......ALL THE SDL FILES HERE......
                    src/core/linux/SDL_evdev.c """)

# flags
localEnv.Append(CPPPATH=['include', '/usr/include/dbus-1.0', '/usr/lib/x86_64-linux-gnu/dbus-1.0/include'])

localEnv.Append(CCFLAGS = ['-DUSING_GENERATED_CONFIG_H', '-mmmx', '-m3dnow', '-msse', '-msse2', '-fvisibility=hidden', '-D_REENTRANT', '-DHAVE_LINUX_VERSION_H', '-fPIC', '-DPIC'])

# build a static library
localEnv.StaticLibrary(target = 'SDL2', source = sources)
```

## Building the project

Building the project is pretty straightforward, go to the root directory and type: 


```txt
scons -j8
```
This will start the build in debug mode (which is default) using 8 threads (you can change the value to any number you want). 

If you wanted to build the project in a different mode you can type: 


```txt
scons -j8 mode=release
```
As you may imagine, this will build the project in release mode. 


      * Author: JohnA 
      * OS: Win2K 
      * Tools: Mingw32, gcc 
This is the shortest SConstruct for creating an executable 
```txt
#need glob to get all the source files
import glob
import os

#create an environment that uses mingw tools
#FIXME: clobbers env['TOOLS']
env = Environment(ENV=os.environ, tools=['mingw'])

#the target will be myprogram.exe (in win32)
#the source files will be every file in the 
#current directory that matches "*.cpp"
env.Program(target='myprogram', source = glob.glob('*.cpp'))
```
_errata: don't need the .exe in the target name_ 

_errata: don't need to Split() the glob_ 

_errata: don't forget to set the ENV argument in the call to Environment(); import os also_ 

_errata: don't set tools= in the Environment(), use Tool('mingw')(env) to avoid clobbering env['TOOLS']_ 

The page had this code instead: 
```txt
#create an environment that uses mingw tools
env = Environment(ENV=os.environ)
#Prefer MinGW over other compilers
Tool('mingw')(env)
```
I couldn't get this to work. As of version 2.3.0, It would pass /nologo (an MSVC flag) to g++, causing the build to fail. 


This SConstruct file can be used as a simple template to build a SDL application in Windows. Uses MinWG and will need to be customized slightly to work with other compilers like Visual Studio's compiler. 

This example includes a windows resource which links the executable to a .ico file and it uses the -mwindows flag so no annoying dialog window will appear when the application is started. 


```python
#!python 
# SCons SConstruct file to build a typical SDL application on Windows with a windows icon using mingw

env = Environment(ENV=os.environ)
Tool('mingw')(env)

build_filename = 'appname'  # Will automatically add .exe extension
sources = [Glob('src/*.cpp'), env.RES('appname.rc')]  #Add window resource to include .ico file
libraries = ['mingw32', 'SDLmain', 'SDL', 'SDL_mixer', 'SDL_image', 'SDL_ttf']
library_paths = ['/MinGW/lib']

env.MergeFlags('-mwindows')  # Parse the -mwindows flag to remove the annoying console window
env.Program(target = build_filename, source = sources, LIBS = libraries, LIBPATH = library_paths)
```
**appname.rc:** 
```txt
A ICON MOVEABLE PURE LOADONCALL DISCARDABLE "appname.ico"
```
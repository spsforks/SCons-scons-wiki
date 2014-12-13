
      * Author: JohnA 
      * OS: Win2K 
      * Tools: msvc 
_Note: these are my first SCONS trys, there are probably better ways of doing them_ 

---

 This is the shortest SConstruct for creating an executable. This is even simpler than [SconstructShortMingwWin32](SconstructShortMingwWin32) 
```txt
#need glob to get source files
import glob

#create an environment
env = Environment()

#target us myprogram.exe
#source is a list of source files
env.Program(target='myprogram', source = glob.glob('*.cpp'))
```
_errata: do not need Split() around glob, i.e. source can be a list_ 

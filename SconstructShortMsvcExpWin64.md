
      * Author: JohnA, HeBD 
      * OS: [WinVista64](WinVista64) 
      * Tools: msvc express 
_Note: these are my first SCONS trys, there are probably better ways of doing them_ 

---

 This is the shortest SConstruct for creating an executable. This is even simpler than [SconstructShortMingwWin32](SconstructShortMingwWin32) 
```txt
#need glob to get source files
import glob

#Create an environment with x86 target as msvc does not support x64 and target defalts to host(x64).
#This fixes the following error:
#  'cl' is not recognized as an internal or external command,
#  operable program or batch file.
env = Environment(TARGET_ARCH="x86")

#Target is myprogram.exe
#Source is a list of source files.
env.Program(target='myprogram', source = glob.glob('*.cpp'))
```
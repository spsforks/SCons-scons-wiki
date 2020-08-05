
This shows how to have multiple sub-projects driven from a single sconstruct. 

It assumes a directory structure: 


```txt
...\Sconstruct                ; main sconstruct file
...\herprogram\sconscript     ; sconscript for sub-project
              \src files      ; the source files for the sub-project
...\hisprogram\sconscript
              \src files
...\myprogram\sconscript
             \src files

...\debug\herprogram          ; the debug build directory for sub-project
...\debug\hisprogram
...\debug\myprogram
...\release\herprogram        ; the release build directory for sub-project
...\release\hisprogram
...\release\myprogram
```
The command line looks like this: 


```txt
scons myprogram                ; build project 'myprogram' in release mode
scons hisprogram               ; build project 'hisprogram' in release mode

scons herprogram               ; build project 'herprogram' in release mode
scons mode=debug herprogram    ; build project 'herprogram' in debug mode
scons mode=release herprogram  ; build project 'herprogram' in release mode
```
SConstruct: 


```python
# get the mode flag from the command line
# default to 'release' if the user didn't specify
mymode = ARGUMENTS.get("mode", "release")  # holds current mode

# check if the user has been naughty: only 'debug' or 'release' allowed
if not (mymode in ["debug", "release"]):
    print("Error: expected 'debug' or 'release', found: " + mymode)
    Exit(1)

# tell the user what we're doing
print("**** Compiling in " + mymode + " mode...")

debugcflags = [
    "-W1",
    "-GX",
    "-EHsc",
    "-D_DEBUG",
    "/MDd",
]  # extra compile flags for debug
releasecflags = ["-O2", "-EHsc", "-DNDEBUG", "/MD"]  # extra compile flags for release

env = Environment()

# make sure the sconscripts can get to the variables
Export("env", "mymode", "debugcflags", "releasecflags")

# put all .sconsign files in one place
env.SConsignFile()

# specify the sconscript for myprogram
project = "myprogram"
SConscript(project + "/sconscript", exports=["project"])

# specify the sconscript for hisprogram
project = "hisprogram"
SConscript(project + "/sconscript", exports=["project"])

# specify the sconscript for herprogram
project = "herprogram"
SConscript(project + "/sconscript", exports=["project"])
```

SConscript: 

```python
import glob

# get all the build variables we need
Import("env", "project", "mymode", "debugcflags", "releasecflags")
localenv = env.Copy()

buildroot = "../" + mymode  # holds the root of the build directory tree
builddir = buildroot + "/" + project  # holds the build directory for this project
targetpath = (
    builddir + "/" + project
)  # holds the path to the executable in the build directory

# append the user's additional compile flags
# assume debugcflags and releasecflags are defined
if mymode == "debug":
    localenv.Append(CCFLAGS=debugcflags)
else:
    localenv.Append(CCFLAGS=releasecflags)

# specify the build directory
localenv.BuildDir(builddir, ".", duplicate=0)

srclst = map(lambda x: builddir + "/" + x, glob.glob("*.cpp"))
localenv.Program(targetpath, source=srclst)
```

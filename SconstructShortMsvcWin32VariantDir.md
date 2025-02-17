It you want your build directory in another directory tree, try this: 

```python
import glob

env = Environment()

# variable to hold the build directory (relative)
mybuilddir = "../debug/myprogram"

# set up an alternate build directory
VariantDir("#" + mybuilddir, "#.", duplicate=0)

# target is myprogram.exe (win32) in the current directory
# lambda translates source file names relative to build directory
env.Program(
    "myprogram", source=map(lambda x: "#" + mybuilddir + "/" + x, glob.glob("*.cpp"))
)
```
this assumes that your dir tree looks like this 


```txt
    ...\Debug
             \myprogram
             \hisprogram
             \herprogram
    ...\myprogram
    ...\hisprogram
    ...\herprogram
```
_Note that you can use absolute path names for mybuilddir_ 

_errata: don't need Split() for source files_ 



---

 In the above situations, the target file 'myprogram.exe' is placed in the currect directory. If you want the target file to also be put into the build directory, try this: 
```python
import glob

env = Environment()

# variable to hold the build directory (relative)
mybuilddir = "../debug/myprogram"

# set up an alternate build directory
VariantDir("#" + mybuilddir, "#.", duplicate=0)

# target is myprogram.exe (win32) in the build directory
# lambda translates source file names relative to build directory
env.Program(
    mybuilddir + "/myprogram",
    source=map(lambda x: "#" + mybuilddir + "/" + x, glob.glob("*.cpp")),
)
```

---

 Assuming that the project name is the same as the executable name is the same as the build directory name... 
```python
import glob

# project name is the root name for the executable and build directory
project = "myproject"

# buildroot is where all project build directories reside
buildroot = "../debug"

# -------
# From here on will be common to all projects

# holds the project build directory
builddir = buildroot + "/" + project
# holds the path to the target file in the project build directory
targetpath = builddir + "/" + project

env = Environment()

# define the build directory for scons
VariantDir("#" + builddir, "#.", duplicate=0)

env.Program(
    targetpath, source=map(lambda x: "#" + builddir + "/" + x, glob.glob("*.cpp"))
)
```
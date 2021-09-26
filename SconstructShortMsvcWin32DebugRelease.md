This lets you choose debug or release from the command line: 

```python
import glob

# get the mode flag from the command line
# default to 'release' if the user didn't specify
mymode = ARGUMENTS.get("mode", "release")  # holds current mode

# check if the user has been naughty: only 'debug' or 'release' allowed
if not (mymode in ["debug", "release"]):
    print "Error: expected 'debug' or 'release', found: " + mymode
    Exit(1)

# tell the user what we're doing
print "**** Compiling in " + mymode + " mode..."

project = "myprogram"  # holds the project name
buildroot = "../" + mymode  # holds the root of the build directory tree
debugcflags = [
    "-W1",
    "-GX",
    "-EHsc",
    "-D_DEBUG",
    "/MDd",
]  # extra compile flags for debug
releasecflags = ["-O2", "-EHsc", "-DNDEBUG", "/MD"]  # extra compile flags for release

# -------
# From here on will be common to all projects

builddir = buildroot + "/" + project  # holds the build directory for this project
targetpath = (
    builddir + "/" + project
)  # holds the path to the executable in the build directory

env = Environment()

# append the user's additional compile flags
# assume debugcflags and releasecflags are defined
if mymode == "debug":
    env.Append(CCFLAGS=debugcflags)
else:
    env.Append(CCFLAGS=releasecflags)

# specify the build directory
VariantDir("#" + builddir, "#.", duplicate=0)

env.Program(
    targetpath, source=map(lambda x: "#" + builddir + "/" + x, glob.glob("*.cpp"))
)
```

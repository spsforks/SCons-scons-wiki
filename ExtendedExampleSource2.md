Here's the current Sconstruct: 

```python
import os
import fnmatch

##-------------------------------------------------
# Use:
#   scons projectx [mode=debug]
#        - defaults to mode=release
##-------------------------------------------------

##-------------------------------------------------
# -- Function definitions here
def DoSrc(tgt, mode):
    variant = os.path.join("/projects", mode, tgt)
    SConscript("src/" + tgt + "/sconscript", variant_dir=variant)


def DoFrozen(tgt, mode):
    variant = os.path.join("/projects", mode, tgt)
    SConscript("frozen/" + tgt + "/sconscript", variant_dir=variant)


class Dev(Environment):
    def DevGetSourceFiles(self, patterns=None):
        files = []

        if patterns is None:
            patterns = [
                "*" + self["CXXFILESUFFIX"],
                "*" + self["CFILESUFFIX"],
                "*" + self["QT_UISUFFIX"],
            ]
        for file in os.listdir(self.Dir(".").srcnode().abspath):
            for pattern in patterns:
                if fnmatch.fnmatchcase(file, pattern):
                    files.append(file)
        return files


##-------------------------------------------------
# --
# prevent accidental building of everything;
# - to build everything use 'scons.py .'
Default(None)

##-------------------------------------------------
# - check compilation mode: 'debug' or 'release' only
mode = ARGUMENTS.get("mode", "release")
if not (mode in ["debug", "release"]):
    print "Error: expected 'debug' or 'release', found: " + mode
    Exit(1)

print "**** Compiling in " + mode + " mode..."

env = Environment()
dev = Dev()
Export("env", "dev")
env.PrependENVPath("PATH", "E:/tools/mingw/bin")

DoSrc("pso", mode)
DoSrc("cppwiki", mode)
DoSrc("smanager", mode)
DoFrozen("jmirror", mode)
DoFrozen("classesinc", mode)
```
Here's a typical sconscript (they're all very similar): 

```python
Import('env', 'dev')
project = 'classesinc'

localenv = env.Clone()
localenv.Tool('msvc')
tgt = localenv.Program(project, dev.DevGetSourceFiles(['*.c']))
env.Alias(project, tgt)
```

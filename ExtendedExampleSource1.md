Here's the current Sconstruct: 

```python
import os

def DoSrc(tgt, mode):
    variant = os.path.join("/projects", mode, tgt)
    SConscript("src/" + tgt + "/sconscript", variant_dir=variant)

def DoFrozen(tgt, mode):
    variant = os.path.join("/projects", mode, tgt)
    SConscript("frozen/" + tgt + "/sconscript", variant_dir=variant)

mode = "release"
if ARGUMENTS.has_key("mode"):
    mode = ARGUMENTS["mode"]
print "**** Compiling in " + mode + " mode..."

env = Environment()
Export("env")
env.PrependENVPath("PATH", "E:/tools/mingw/bin")

DoSrc("pso", mode)
DoSrc("cppwiki", mode)
DoSrc("smanager", mode)
DoFrozen("jmirror", mode)
```
Note: `DoSrc` and `DoFrozen` are identical except for the root directory. Should probably be refactored into one function 

Here's a typical sconscript (they're all very similar): 

```python
import glob
Import('env')
project = 'cppwiki'

localenv = env.Clone()
localenv.Tool('msvc')
tgt = localenv.Program(project, glob.glob('*.cpp'))
env.Alias(project, tgt)
```

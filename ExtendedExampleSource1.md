Here's the current Sconstruct: 

```python
import SCons.Script
import os
def DoSrc(tgt, mode):
    build_dir = os.path.join('/projects', mode, tgt)
    SConscript('src/' + tgt + '/sconscript', build_dir= build_dir)

def DoFrozen(tgt, mode):
    build_dir = os.path.join('/projects', mode, tgt)
    SConscript('frozen/' + tgt + '/sconscript', build_dir= build_dir)

mode = 'release'
if ARGUMENTS.has_key('mode'):
   mode = ARGUMENTS['mode']
print '**** Compiling in ' + mode + ' mode...'

env = Environment()
Export('env')
env.PrependENVPath('PATH', 'E:/tools/mingw/bin')

DoSrc('pso', mode)
DoSrc('cppwiki', mode)
DoSrc('smanager', mode)
DoFrozen('jmirror', mode)
```
Note: `DoSrc` and `DoFrozen` are identical except for the root directory. Should probably be refactored into one function 

Here's a typical sconscript (they're all very similar): 

```python
import glob
Import('env')
project = 'cppwiki'

localenv = env.Copy()
localenv.Tool('msvc')
tgt = localenv.Program(project, glob.glob('*.cpp'))
env.Alias(project, tgt)
```
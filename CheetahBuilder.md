# SCons Tool for Cheetah

Provides a SCons tool that allows SConstruct scripts to build files from [Cheetah templates](http://www.cheetahtemplate.org).


### Builders

```python
#!python

import SCons.Builder
import pickle

def makeCheetahCommand(target, source, env, for_signature):
    base = 'export PYTHONPATH="${TARGET.dir}" &&'
    base += 'cheetah fill --stdout --nobackup '
    sourceAndTarget = '$SOURCE >> $TARGET'

    if 'PICKLE' in env:
        env.Depends(target, env['PICKLE'])
        return base + '--pickle $PICKLE ' + sourceAndTarget
    else:
        return base + sourceAndTarget

cheetahBldr = SCons.Builder.Builder(
    generator = makeCheetahCommand,
    src_suffix = '.tmpl',
    single_source = True,
)


def pickle_function(target, source, env):
    for i in range(len(target)):
        print(target[i])
        pickle.dump(source[i].read(), open(str(target[i]), 'wb'))
    return None

pickleBldr = SCons.Builder.Builder(
    action = pickle_function,
    suffix = '.pkl'
)


def generate(env):
    env['BUILDERS']['Cheetah'] = cheetahBldr
    env['BUILDERS']['Pickle'] = pickleBldr


def exists(env):
    return env.Detect('cheetah')

```


### Example

```python
#!python

pickle = env.Pickle('vars.pkl', Value({'var1':1, 'var2':2}))
env.Cheetah('output.txt', 'input.tmpl', PICKLE=pickle)
```


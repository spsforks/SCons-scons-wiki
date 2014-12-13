
This is a builder to help when you need to take a file and replace certain variables in it.  (See also [SubstInFileBuilder](SubstInFileBuilder) for another approach which may do better handling changes in the variable values.) 

For example, when creating pkg-config files, autoconf will take a package.pc.in file and create package.pc from it, replacing things such as @libdir@ with the actual value. 

We can do much better :-) 

scanreplace.py: 
```python
#!python 
from string import Template

def replace_action(target, source, env):
    open(str(target[0]), 'w').write(Template(open(str(source[0]), 'r').read()).safe_substitute(env))
    return 0

def replace_string(target, source, env):
    return "building '%s' from '%s'" % (str(target[0]), str(source[0]))

def generate(env, **kw):
    action = env.Action(replace_action, replace_string)
    env['BUILDERS']['ScanReplace'] = env.Builder(action=action, src_suffix='.in', single_source=True)

def exists(env):
    return 1
```
To use this, place scanreplace.py into your tools directory (see the manpage for more details) and then do this: 


```python
#!python 
env = Environment(tools=['default', 'scanreplace'], toolpath=['tools'])
env['prefix'] = '/usr/local'
env.ScanReplace('myprogram.pc.in')
```
This will create myprogram.pc from myprogram.pc.in, replacing variables along the way. 

Variables will be found in the environment, so in the previous example, any occurence of '$prefix' or '${prefix}' in myprogram.pc.in would be replaced with '/usr/local'. 

Have fun! 

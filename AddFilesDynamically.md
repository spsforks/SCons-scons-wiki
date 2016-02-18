The function presented here is useful if: 

* You've got one environment used to create many targets (too many to start messing with). 
* The environment is configured differently for different platforms/compilers/etc. 
* Some platforms/compilers/etc. need an additional source file to be compiled in order to work properly. This can be, for example, a replacement for a library that is not available on a certain platform. 
This function wraps a given emitter with another emitter that adds another file to the source nodes. 

Replaceable emitters (as of SCons 0.96.90): 

* `PROGEMITTER` - emitter for Program builder 
* `SHLIBEMITTER` - emitter for [SharedLibrary](SharedLibrary) builder 
* `LIBEMITTER` - emitter for Library builder 

## The Function


```python
#!python
def add_file_to_emitter(env, emitter_name, file):
  try:
    original_emitter = env[emitter_name]
    if type(original_emitter) == list:
      original_emitter = original_emitter[0]
  except KeyError:
    original_emitter = None
  def emitter(target, source, env):
    if original_emitter:
      target, source = original_emitter(target, source, env)
    return target, source + [file]
  env[emitter_name] = emitter
```

## Example Usage

In this example, the environment is searched for a library called _somelib_. If this library is not found, add_file_to_emitter is called to add _somelibreplacement.c_ to every program built using the environment. 


```python
#!python
env = Environment()
conf = env.Configure()
if not conf.CheckLib('somelib'):
  add_file_to_emitter(env, 'PROGEMITTER', File('somelibreplacement.c'))
conf.Finish()
```
* -- [AmirSzekely](AmirSzekely) 

## Changing the Emitter for StaticObject

If you want to change where a builder finds its C/C++ source files, you want to change the emitter for the [StaticObject](StaticObject) builder, aka Object. Unfortunately, there is no OBJEMITTER currently defined, but another way to do it is shown below. 
```python
#!python
# Assuming the BUILD_DIR is set to the location of the generated files
# and some other generated files are in OTHER_BUILD_DIR
def my_emitter(target, source, env):
    ''' Tell SCons about the locations of some generated files. This could
        be any emitter you want'''
    if os.path.exists(source[0].path):
        # The source file was generated in the local build directory
        return (target, source)
    altSrcName = source[0].abspath.replace(env['BUILD_DIR'] + os.sep, '')
    if os.path.exists(altSrcName):
        # The source file is in the source directory
        return (target, altSrcName)
    # Assume that the source file is in the other generated files build directory
    altSrcName = "%s/%s%s" % (File('#'), env['OTHER_BUILD_DIR'],
                  source[0].path.replace(env['OTHER_BUILD_DIR'], ''))
    return (target, altSrcName)
# This is the part where we override the emitter for the Object builder
from SCons.Tool import createObjBuilders
# Get the underlying builder objects
static_obj, shared_obj = createObjBuilders(env)
# Now SCons can find .cpp files in different locations
static_obj.add_emitter('.cpp', my_emitter)
```
* -- [MattDoar](WikiUsers/MattDoar) 

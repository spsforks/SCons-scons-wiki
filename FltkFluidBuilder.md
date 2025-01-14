
The FltkFluidBuilder creates C++ source and header files from Fluid's .fl files. Fluid is the graphical GUI editor of the GUI toolkit [FLTK](http://fltk.org). Simply add the .fl files to the list of sources to be compiled. 


```python
#!python 
sources = Split("""main.cpp UserInterface.fl""")
```
The builder will create two files: `fluid_UserInterface.h` and `fluid_UserInterface.cxx` and adds them to the list of sources to be built. 

Here's the builder and emitter + registration: 


```python
#!python 
import os
import Scons.Util

# emitter to add the generated .h file to the dependencies
def fluidEmitter(target, source, env):
  adjustixes = SCons.Util.adjustixes
  file = SCons.Util.splitext(str(source[0].name))[0]
  file = os.path.join(str(target[0].get_dir()), file)
  target.append(adjustixes(file, "fluid_", ".h"))
  return target, source

fluidBuilder = Builder(action = "cd ${SOURCE.dir} && " + 
                                "fluid -o fluid_${SOURCE.filebase}.cxx " + 
                                "-h fluid_${SOURCE.filebase}.h -c ${SOURCE.name} ",
                        emitter = fluidEmitter,
                        src_suffix = '.fl',
                        suffix = '.cxx',
                        prefix = 'fluid_')

# register builder
env.Append( BUILDERS = { 'Fluid': fluidBuilder } )

# add builder to the builders for shared and static objects, 
# so we can use all sources in one list
shared, static = SCons.Tool.createObjBuilders(env)
shared.src_builder.append('Fluid')
static.src_builder.append('Fluid')
```
-- [hirsch](hirsch) 2006-08-11 10:54:26 

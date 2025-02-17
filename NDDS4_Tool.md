NDDS 4 (also known as RTI DDS) is the Network Data Distribution Service, a commercial implementation of the OMG Data Distribution Service (DDS) standard.  DDS is a real-time publish-subscribe middleware which one could consider a peer of CORBA. 

This was developed on the Linux platform, and has not been tested on any other platform. 

Here's the python source for the tool (ndds4.py): 
```python
#!python
"""SCons.Tool.ndds
Tool-specific initialization for NDDS

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

import os
import re

import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Scanner.IDL
import SCons.Tool
import SCons.Util

class ToolNddsWarning(SCons.Warnings.SConsWarning):
   pass

class NddsHomeNotFound(ToolNddsWarning):
   pass

def emitNddsType(target, source, env):
   """Produce a list of files created by nddsgen"""
   base, ext = SCons.Util.splitext(str(source[0].abspath) )
      
   filenames = [base, base + 'Support', base + 'Plugin']
   
   dot_cxx = map(lambda f: f + '.cxx', filenames)
   dot_h = map(lambda f: f + '.h', filenames)
   
   #Don't forget to clean up the generated headers
   env.Clean(dot_cxx, dot_h)
   
   return dot_cxx, source

scanNddsIDL = SCons.Scanner.IDL.IDLScan()

actNddsGen = SCons.Action.Action('nddsgen -replace $SOURCE -d $TARGET.dir -I$SOURCE.dir')

buildNddsType = SCons.Builder.Builder(action = actNddsGen,
                                      emitter = emitNddsType,
                                      source_scanner = scanNddsIDL,
                                      src_suffix='.idl')

def _detect(env):
   """Not really safe, but fast method to detect NDDSHOME"""

   NDDSHOME = env['ENV'].get('NDDSHOME',None)
   if NDDSHOME!=None : return NDDSHOME

   NDDSHOME = os.environ.get('NDDSHOME',None)
   if NDDSHOME!=None : return NDDSHOME

   nddsgen = env.WhereIs('nddsgen')
   if nddsgen:
      SCons.Warnings.warn(
         NddsHomeNotFound,
         "NDDSHOME variable is not defined, using nddsgen executable as a hint (NDDSHOME=%s)" % NDDSHOME)
      return os.path.dirname(os.path.dirname(nddsgen))

   SCons.Warnings.warn(
      NddsHomeNotFound,
      "Could not detect ndds, using empty NDDSHOME")
   return None

def generate(env):
   """Add Builder and Scanner for ndds to the Environment."""

   
   
   try:
      NDDSHOME = _detect(env)

      NDDSARCH = os.listdir(os.path.join(NDDSHOME, 'lib') )[0]
   except:
      print("Error looking for NDDSHOME and/or libraries")

   print("Loading ndds4 tool...")

   #Set up NDDS environment      
   env.AppendUnique(CPPPATH = [os.path.join(NDDSHOME,'include')] )
   env.AppendUnique(CPPPATH = [os.path.join(NDDSHOME,'include', 'ndds')] )
   
   env.AppendUnique(CPPDEFINES = ['RTI_UNIX'] )

   #TODO: Options for static vs. dynamic and debug vs. optimized?
   env.AppendUnique(LIBS = SCons.Util.Split("""
                                               nddscppzd
                                               nddsczd
                                               nddscorezd
                                               pthread                    
                                            """) )

   env.Append(LIBPATH = os.path.join(NDDSHOME, 'lib', NDDSARCH) )


   
   #Add the scanner and builder to the environment
   env.Append(SCANNERS = [scanNddsIDL])
   env.Append(BUILDERS = {'NddsType' : buildNddsType})
   
   #Add them to the object builders
   static_obj, shared_obj = SCons.Tool.createObjBuilders(env)
   
   static_obj.src_builder.append('NddsType')
   shared_obj.src_builder.append('NddsType')
   
def exists(env):
   return _detect(env)
```
The tool must be loaded into your environment like so: 
```python
#!python
env.Tool('ndds4', ['path_to_ndds4.py_file'])
```
See the section on Tool objects in the SCons User Guide for more details. 

The following python source demonstrates several ways you may use the tool: 
```python
#!python
#Precondition: Environment 'env' must have the ndds4 tool loaded.

#(1) Run nddsgen on the idl file specified (generates source and header files)
env.NddsType('Foo.idl')

# (2) Run nddsgen on Foo.idl, then compile the resulting source files (Foo.cxx, FooSupport.cxx, FooPlugin.cxx)
env.StaticObject('Foo.idl')

# (3) Run nddsgen on Foo.idl, compile the source files and roll them into a static library
env.StaticLibrary('Foo.idl')

# (4) Run nddsgen on Foo.idl, compile the source files and link them into an executable
env.Program(['main.cpp', 'Foo.idl'])
```

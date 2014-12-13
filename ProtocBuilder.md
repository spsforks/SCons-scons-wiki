

## Generating Protocol Buffers files with SCons

_**Repositories under version control are the place for code rather than wiki pages, so a [Mercurial repository](https://bitbucket.org/russel/scons_protobuf) has been created on [BitBucket](https://bitbucket.org/) and the code from this page copied into it. The repository is where all evolution of this tool should happen. See also the [ToolsIndex](http://scons.org/wiki/ToolsIndex) page which has more on the tool strategy.**_ 

This builder will allow you to generate Google Protocol Buffers .pb.cc, .pb.h, and _pb2.py files using SCons from a .proto source file. 

It doesn't currently support Java, but that should be easy to add. 

Put this builder/tool file somewhere (next to the SConstruct file or in the Environment's 'toolpath', and call it 'protoc.py'. 


```python
#!python 
"""
protoc.py: Protoc Builder for SCons

This Builder invokes protoc to generate C++ and Python
from a .proto file.

NOTE: Java is not currently supported."""

__author__ = "Scott Stafford"

import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Node.FS
import SCons.Util

from SCons.Script import File, Dir

import os.path

protocs = 'protoc'

ProtocAction = SCons.Action.Action('$PROTOCCOM', '$PROTOCCOMSTR')
def ProtocEmitter(target, source, env):
    dirOfCallingSConscript = Dir('.').srcnode()
    env.Prepend(PROTOCPROTOPATH = dirOfCallingSConscript.path)

    source_with_corrected_path = []
    for src in source:
        commonprefix = os.path.commonprefix([dirOfCallingSConscript.path, src.srcnode().path])
        if len(commonprefix)>0:
            source_with_corrected_path.append( src.srcnode().path[len(commonprefix + os.sep):] )
        else:
            source_with_corrected_path.append( src.srcnode().path )

    source = source_with_corrected_path

    for src in source:
        modulename = os.path.splitext(src)[0]

        if env['PROTOCOUTDIR']:
            base = os.path.join(env['PROTOCOUTDIR'] , modulename)
            target.extend( [ base + '.pb.cc', base + '.pb.h' ] )

        if env['PROTOCPYTHONOUTDIR']:
            base = os.path.join(env['PROTOCPYTHONOUTDIR'] , modulename)
            target.append( base + '_pb2.py' )

    try:
        target.append(env['PROTOCFDSOUT'])
    except KeyError:
        pass

    #~ print "PROTOC SOURCE:", [str(s) for s in source]
    #~ print "PROTOC TARGET:", [str(s) for s in target]

    return target, source

ProtocBuilder = SCons.Builder.Builder(action = ProtocAction,
                                   emitter = ProtocEmitter,
                                   srcsuffix = '$PROTOCSRCSUFFIX')

def generate(env):
    """Add Builders and construction variables for protoc to an Environment."""
    try:
        bld = env['BUILDERS']['Protoc']
    except KeyError:
        bld = ProtocBuilder
        env['BUILDERS']['Protoc'] = bld

    env['PROTOC']        = env.Detect(protocs) or 'protoc'
    env['PROTOCFLAGS']   = SCons.Util.CLVar('')
    env['PROTOCPROTOPATH'] = SCons.Util.CLVar('')
    env['PROTOCCOM']     = '$PROTOC ${["-I%s"%x for x in PROTOCPROTOPATH]} $PROTOCFLAGS --cpp_out=$PROTOCCPPOUTFLAGS$PROTOCOUTDIR ${PROTOCPYTHONOUTDIR and ("--python_out="+PROTOCPYTHONOUTDIR) or ""} ${PROTOCFDSOUT and ("-o"+PROTOCFDSOUT) or ""} ${SOURCES}'
    env['PROTOCOUTDIR'] = '${SOURCE.dir}'
    env['PROTOCPYTHONOUTDIR'] = "python"
    env['PROTOCSRCSUFFIX']  = '.proto'

def exists(env):
    return env.Detect(protocs)
```
Now you should have an env.Protoc() builder that takes .proto as source and emits generated protobuf source. 

Here is a sample SConstruct I used (some MSVC/Windows-specific stuff, but the Protoc builder is OS-agnostic.)  Note that you must make sure the protoc executable is available in your PATH or it won't be able to execute it. 


```python
#!python 
import os

env = Environment(
    ENV = {'PATH' : os.environ['PATH']},
    CPPPATH = ['C:\wc\protobuf-trunk\src' ],
    CPPFLAGS = ['/EHsc', '/MDd'],
    tools=['default', 'protoc']
    )

proto_files = env.Protoc(
    [],
    "config.proto",
    PROTOCPROTOPATH=['.',r'C:\wc\protobuf-trunk\src',],
    PROTOCPYTHONOUTDIR='python', # set to None to not generate python
    PROTOCOUTDIR = 'build', # defaults to same directory as .proto
    # PROTOCCPPOUTFLAGS = "dllexport_decl=PROTOCONFIG_EXPORT:", too
)

env.Program('test', ['test.cpp', proto_files[0]],
    LIBPATH=[r'C:\wc\protobuf-trunk\vsprojects\Debug'],
    LIBS=['libprotobuf.lib'],
    )
```
-- [ScottStafford](ScottStafford) 

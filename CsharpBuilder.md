

# SCons and C#

It would be great to roll this into a generic CLI builder that can take sources from any supported CLI language and compile them to EXE or DLL. 

Russel Winder has contributed a SCons C# tool based on the code from this page to the sconscontrib repo.  See  
[https://github.com/SCons/scons-contrib/tree/master/sconscontrib/SCons/Tool/csharp](https://github.com/SCons/scons-contrib/tree/master/sconscontrib/SCons/Tool/csharp)


## Mono

Here is a simple mcs builder.  It takes one or more C# files and creates and EXE or a DLL from them.  The user variables that effect the build are:  

* CSC: the name of the compiler (in this case mcs) 
* CSCFLAGS: extra compiler flags 
* CILLIBS: libraries to link against 
* CILLIBPATH: library paths 

### Example Usage


```python
#!python 
env.Tool('mcs', toolpath = [''])
env.CLILibrary('Foo.dll', 'Foo.dll')
env.CLIProgram('Bar.exe', 'Bar.exe')
```

### Builder


```python
#!python 
import os.path
import SCons.Builder
import SCons.Node.FS
import SCons.Util

csccom = "$CSC $CSCFLAGS -out:${TARGET.abspath} $SOURCES"
csclibcom = "$CSC -t:library $CSCLIBFLAGS $_CSCLIBPATH $_CSCLIBS -out:${TARGET.abspath} $SOURCES"


McsBuilder = SCons.Builder.Builder(action = '$CSCCOM',
                                   source_factory = SCons.Node.FS.default_fs.Entry,
                                   suffix = '.exe')

McsLibBuilder = SCons.Builder.Builder(action = '$CSCLIBCOM',
                                   source_factory = SCons.Node.FS.default_fs.Entry,
                                   suffix = '.dll')

def generate(env):
    env['BUILDERS']['CLIProgram'] = McsBuilder
    env['BUILDERS']['CLILibrary'] = McsLibBuilder

    env['CSC']        = 'mcs'
    env['_CSCLIBS']    = "${_stripixes('-r:', CILLIBS, '', '-r', '', __env__)}"
    env['_CSCLIBPATH'] = "${_stripixes('-lib:', CILLIBPATH, '', '-r', '', __env__)}"
    env['CSCFLAGS']   = SCons.Util.CLVar('')
    env['CSCCOM']     = SCons.Action.Action(csccom)
    env['CSCLIBCOM']  = SCons.Action.Action(csclibcom)

def exists(env):
    return internal_zip or env.Detect('mcs')

```

## Microsoft C# compiler


### Example Usage (Library)


```python
#!python 
refpaths = []

refs = Split("""
  System
  System.Data
  System.Xml
  """)

sources = Split("""
  DataHelper.cs
  Keyfile.snk
        """)

r = env.CLIRefs(refpaths, refs)

prog = env.CLILibrary('MyAssembly.Common', sources, ASSEMBLYREFS=r)
# use the following call to allow programs built after this library to find it
# without having to add to the refpaths (see next example)
env.AddToRefPaths(prog)
```

### Example Usage (Program)


```python
#!python 
refpaths = Split("""
  #/thirdparty/EncryptionLib
  """)

# note we don't have to add MyAssembly.Common's location to refpaths
# it will be stored with the call to AddToRefPaths() in the above example
refs = Split("""
  MyAssembly.Common
  System
  System.Data
  """)

sources = Split("""
  Main.cs
  gui/App.cs
  gui/MyForm.cs
  Keyfile.snk
  """)

resx = Split("""
  gui/App.resx
  gui/MyForm.AddServerModelForm.resx
  """)
sources.append([env.CLIRES(r, NAMESPACE='MyCompany') for r in resx])

r = env.CLIRefs(refpaths, refs)
prog = env.CLIProgram('myapp', sources, ASSEMBLYREFS=r, WINEXE=1)
```

### A Small, Complete Example


```python
#!python 
import os

env_vars = {}
for ev in ['PATH', 'LIB', 'SYSTEMROOT', 'PYTHONPATH']:
  env_vars[ev] = os.environ[ev]

env = Environment(
  platform='win32',
  tools=['mscs', 'msvs'],
  toolpath = ['.'],
  ENV=env_vars,
  MSVS_IGNORE_IDE_PATHS=1
  )

mod = env.CLIModule('mymod', 'MyMod.cs')

refs = ['System', 'System.Reflection', 'System.Runtime.CompilerServices', 'System.Runtime.InteropServices']
pathrefs = env.CLIRefs(refs)

mod2 = env.CLIModule('common', 'AsmInfo.cs', ASSEMBLYREFS=pathrefs) #, NETMODULES=mod)

# Note that CLILink actually uses the VS 2005 C++ linker, since it can handle linking .netmodules
asm = env.CLILink('Common', [mod, mod2])
env.AddToRefPaths(asm)

# WINEXE=1 needed if this is a windows app, rather than a console app
prog = env.CLIProgram('MyApp', 'MyApp.cs', ASSEMBLYREFS=asm, VERSION="1.0.1.0")

# Resolve location of Common assembly, this was registered with AddToRefPaths, above.
# added_paths included simply to show how to add assembly paths to the lookup besides
# the ones in the PATH environment variable.  Leave this argument out if there are none.
added_paths = ['#/path']
rr = env.CLIRefs(['Common'], added_paths)

# VERSION can also be passed by tuple, rather than string.
# "asm" variable could have been passed directly into ASSEMBLYREFS if we wanted.
asm2 = env.CLILibrary('MyAsm', 'MyClass.cs', ASSEMBLYREFS=rr, VERSION=(1,0,1,0))

# Create a publisher policy to redirect anything with major minor 
# version of assembly to the MyAsm assembly above.
policy = env.PublisherPolicy(asm2)
```

### Builder


```python
#!python 
import os.path
import SCons.Builder
import SCons.Node.FS
import SCons.Util
from SCons.Node.Python import Value

# needed for adding methods to environment
from SCons.Script.SConscript import SConsEnvironment

# parses env['VERSION'] for major, minor, build, and revision
def parseVersion(env):
  if type(env['VERSION']) is tuple or type(env['VERSION']) is list:
    major, minor, build, revision = env['VERSION']
  elif type(env['VERSION']) is str:
    major, minor, build, revision = env['VERSION'].split('.')
    major = int(major)
    minor = int(minor)
    build = int(build)
    revision = int(revision)
  return (major, minor, build, revision)

def getVersionAsmDirective(major, minor, build, revision):
  return '[assembly: AssemblyVersion("%d.%d.%d.%d")]' % (major, minor, build, revision)

def generateVersionId(env, target, source):
  out = open(target[0].path, 'w')
  out.write('using System;using System.Reflection;using System.Runtime.CompilerServices;using System.Runtime.InteropServices;\n')
  out.write(source[0].get_contents())
  out.close()

# used so that we can capture the return value of an executed command
def subprocess(cmdline):
  import subprocess
  startupinfo = subprocess.STARTUPINFO()
  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
  proc = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, startupinfo=startupinfo, shell=False)
  data, err = proc.communicate()
  return proc.wait(), data, err

# this method assumes that source list corresponds to [0]=version, [1]=assembly base name, [2]=assembly file node
def generatePublisherPolicyConfig(env, target, source):
  # call strong name tool against compiled assembly and parse output for public token
  outputFolder = os.path.split(target[0].tpath)[0]
  pubpolicy = os.path.join(outputFolder, source[2].name)
  rv, data, err = subprocess('sn -T ' + pubpolicy)
  import re
  tok_re = re.compile(r"([a-z0-9]{16})[\r\n ]{0,3}$")
  match = tok_re.search(data)
  tok = match.group(1)
    
  # calculate version range to redirect from
  version = source[0].value
  oldVersionStartRange = '%s.%s.0.0' % (version[0], version[1])
  newVersion = '%s.%s.%s.%s' % (version[0], version[1], version[2], version[3])    
  build = int(version[2])
  rev = int(version[3])

  # on build 0 and rev 0 or 1, no range is needed. otherwise calculate range    
  if build == 0 and (rev == 0 or rev == 1):
    oldVersionRange = oldVersionStartRange
  else:
    if rev - 1 < 0:
      endRevisionRange = '99'
      endBuildRange = str(build-1)
    else:
      endRevisionRange = str(rev - 1)
      endBuildRange = str(build)  
    oldVersionEndRange = '%s.%s.%s.%s' % (version[0], version[1], endBuildRange, endRevisionRange)
    oldVersionRange = '%s-%s' % (oldVersionStartRange, oldVersionEndRange)
  
  # write .net config xml out to file
  out = open(target[0].path, 'w')
  out.write('''\
<configuration><runtime><assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
  <dependentAssembly>
    <assemblyIdentity name="%s" publicKeyToken="%s"/>
    <bindingRedirect oldVersion="%s" newVersion="%s"/>
  </dependentAssembly>
</assemblyBinding></runtime></configuration>
''' % (source[1].value, tok, oldVersionRange, newVersion))
  out.close()

# search for key file
def getKeyFile(node, sources):
  for file in node.children():
    if file.name.endswith('.snk'):
      sources.append(file)
      return
  
  # if not found look in included netmodules (first found is used)
  for file in node.children():
    if file.name.endswith('.netmodule'):
      for file2 in file.children():
        if file2.name.endswith('.snk'):
          sources.append(file2)
          return

# creates the publisher policy dll, mapping the major.minor.0.0 calls to the 
# major, minor, build, and revision passed in through the dictionary VERSION key
def PublisherPolicy(env, target, **kw):
  sources = []
  # get version and generate .config file
  version = parseVersion(kw)
  asm = os.path.splitext(target[0].name)[0]
  configName = 'policy.%d.%d.%s.%s' % (version[0], version[1], asm, 'config')
  targ = 'policy.%d.%d.%s' % (version[0], version[1], target[0].name)
  config = env.Command(configName, [Value(version), Value(asm), target[0]], generatePublisherPolicyConfig)
  sources.append(config[0])
  
  # find .snk key
  getKeyFile(target[0], sources)

  return env.CLIAsmLink(targ, sources, **kw)

def CLIRefs(env, refs, paths = [], **kw):
  listRefs = []
  normpaths = [env.Dir(p).abspath for p in paths]
  normpaths += env['CLIREFPATHS']
  
  for ref in refs:
    if not ref.endswith(env['SHLIBSUFFIX']):
      ref += env['SHLIBSUFFIX']
    if not ref.startswith(env['SHLIBPREFIX']):
      ref = env['SHLIBPREFIX'] + ref
    pathref = detectRef(ref, normpaths, env)
    if pathref:
      listRefs.append(pathref)
  
  return listRefs

def CLIMods(env, refs, paths = [], **kw):
  listMods = []
  normpaths = [env.Dir(p).abspath for p in paths]
  normpaths += env['CLIMODPATHS']

  for ref in refs:
    if not ref.endswith(env['CLIMODSUFFIX']):
      ref += env['CLIMODSUFFIX']
    pathref = detectRef(ref, normpaths, env)
    if pathref:
      listMods.append(pathref)
  
  return listMods

# look for existance of file (ref) at one of the paths
def detectRef(ref, paths, env):  
  for path in paths:
    if path.endswith(ref):
      return path
    pathref = os.path.join(path, ref)
    if os.path.isfile(pathref):
      return pathref

  return ''

# the file name is included in path reference because otherwise checks for that output file
# by CLIRefs/CLIMods would fail until after it has been built.  Since SCons makes a pass
# before building anything, that file won't be there.  Only after the second pass will it be built
def AddToRefPaths(env, files, **kw):
  ref = env.FindIxes(files, 'SHLIBPREFIX', 'SHLIBSUFFIX').abspath
  env['CLIREFPATHS'] = [ref] + env['CLIREFPATHS']
  return 0

def AddToModPaths(env, files, **kw):
  mod = env.FindIxes(files, 'CLIMODPREFIX', 'CLIMODSUFFIX').abspath
  env['CLIMODPATHS'] = [mod] + env['CLIMODPATHS']
  return 0

def cscFlags(target, source, env, for_signature):
  listCmd = []
  if 'WINEXE' in env:
    if env['WINEXE'] == 1:
      listCmd.append('-t:winexe')
  return listCmd

def cscSources(target, source, env, for_signature):
  listCmd = []
  
  for s in source:
    if str(s).endswith('.cs'):  # do this first since most will be source files
      listCmd.append(s)
    elif str(s).endswith('.resources'):
      listCmd.append('-resource:%s' % s.get_string(for_signature))
    elif str(s).endswith('.snk'):
      listCmd.append('-keyfile:%s' % s.get_string(for_signature))
    else:
      # just treat this as a generic unidentified source file
      listCmd.append(s)

  return listCmd

def cscRefs(target, source, env, for_signature):
  listCmd = []
  
  if 'ASSEMBLYREFS' in env:
    refs = SCons.Util.flatten(env['ASSEMBLYREFS'])
    for ref in refs:          
      if SCons.Util.is_String(ref):
        listCmd.append('-reference:%s' % ref)
      else:
        listCmd.append('-reference:%s' % ref.abspath)
        
  return listCmd

def cscMods(target, source, env, for_signature):
  listCmd = []
  
  if 'NETMODULES' in env:
    mods = SCons.Util.flatten(env['NETMODULES'])
    for mod in mods:
      listCmd.append('-addmodule:%s' % mod)
      
  return listCmd     

# TODO: this currently does not allow sources to be embedded (-embed flag)
def alLinkSources(target, source, env, for_signature):
  listCmd = []
  
  for s in source:
    if str(s).endswith('.snk'):
      listCmd.append('-keyfile:%s' % s.get_string(for_signature))
    else:
      # just treat this as a generic unidentified source file
      listCmd.append('-link:%s' % s.get_string(for_signature))

  if 'VERSION' in env:
    version = parseVersion(env)
    listCmd.append('-version:%d.%d.%d.%d' % version)
    
  return listCmd

def add_version(target, source, env):
  if 'VERSION' in env:
    if SCons.Util.is_String(target[0]):
      versionfile = target[0] + '_VersionInfo.cs'
    else:
      versionfile = target[0].name + '_VersionInfo.cs'
    source.append(env.Command(versionfile, [Value(getVersionAsmDirective(*parseVersion(env)))], generateVersionId))
  return (target, source)

MsCliBuilder = SCons.Builder.Builder(action = '$CSCCOM',
                                   source_factory = SCons.Node.FS.default_fs.Entry,
                                   emitter = add_version,
                                   suffix = '.exe')

# this check is needed because .NET assemblies like to have '.' in the name.
# scons interprets that as an extension and doesn't append the suffix as a result
def lib_emitter(target, source, env):
  newtargets = []
  for tnode in target:
    t = tnode.name
    if not t.endswith(env['SHLIBSUFFIX']):
      t += env['SHLIBSUFFIX']
    newtargets.append(t)
    
  return (newtargets, source)

def add_depends(target, source, env):
  """Add dependency information before the build order is established"""
    
  if 'NETMODULES' in env:
    mods = SCons.Util.flatten(env['NETMODULES'])
    for mod in mods:
      # add as dependency if it is something we build
      dir = env.File(mod).dir.srcdir
      if dir is not None and dir is not type(None):
        for t in target:
          env.Depends(t, mod)

  if 'ASSEMBLYREFS' in env:
    refs = SCons.Util.flatten(env['ASSEMBLYREFS'])
    for ref in refs:            
      # add as dependency if it is something we build
      dir = env.File(ref).dir.srcdir
      if dir is not None and dir is not type(None):
        for t in target:
          env.Depends(t, ref)

  return (target, source)

MsCliLibBuilder = SCons.Builder.Builder(action = '$CSCLIBCOM',
                                   source_factory = SCons.Node.FS.default_fs.Entry,
                                   emitter = [lib_emitter, add_version, add_depends],
                                   suffix = '$SHLIBSUFFIX')

MsCliModBuilder = SCons.Builder.Builder(action = '$CSCMODCOM',
                                   source_factory = SCons.Node.FS.default_fs.Entry,
                                   emitter = [add_version, add_depends],
                                   suffix = '$CLIMODSUFFIX')

def module_deps(target, source, env):
  for s in source:
    dir = s.dir.srcdir
    if dir is not None and dir is not type(None):
      for t in target:
        env.Depends(t,s)
  return (target, source)

MsCliLinkBuilder = SCons.Builder.Builder(action = '$CLILINKCOM',
                                   source_factory = SCons.Node.FS.default_fs.Entry,
                                   emitter = [lib_emitter, add_version, module_deps], # don't know the best way yet to get module dependencies added
                                   suffix = '.dll') #'$SHLIBSUFFIX')

# This probably needs some more work... it hasn't been used since 
# finding the abilities of the VS 2005 C++ linker for .NET.
MsCliAsmLinkBuilder = SCons.Builder.Builder(action = '$CLIASMLINKCOM',
                                   source_factory = SCons.Node.FS.default_fs.Entry,
                                   suffix = '.dll')

typelib_prefix = 'Interop.'

def typelib_emitter(target, source, env):
  newtargets = []
  for tnode in target:
    t = tnode.name
    if not t.startswith(typelib_prefix):
      t = typelib_prefix + t
    newtargets.append(t)
    
  return (newtargets, source)

def tlbimpFlags(target, source, env, for_signature):
  listCmd = []
  
  basename = os.path.splitext(target[0].name)[0]  
  # strip off typelib_prefix (such as 'Interop.') so it isn't in the namespace
  if basename.startswith(typelib_prefix):
    basename = basename[len(typelib_prefix):]
  listCmd.append('-namespace:%s' % basename)

  listCmd.append('-out:%s' % target[0].tpath)

  for s in source:
    if str(s).endswith('.snk'):
      listCmd.append('-keyfile:%s' % s.get_string(for_signature))

  return listCmd     

MsCliTypeLibBuilder = SCons.Builder.Builder(action = '$TYPELIBIMPCOM',
                                    source_factory = SCons.Node.FS.default_fs.Entry,
                                    emitter = [typelib_emitter, add_depends],
                                    suffix = '.dll')

res_action = SCons.Action.Action('$CLIRCCOM', '$CLIRCCOMSTR')

# prepend NAMESPACE if provided
def res_emitter(target, source, env):
  if 'NAMESPACE' in env:
    newtargets = []
    for t in target:
      tname = t.name
      
      # this is a cheesy way to get rid of '.aspx' in .resx file names
      idx = tname.find('.aspx.')
      if idx >= 0:
        tname = tname[:idx] + tname[idx+5:]

      newtargets.append('%s.%s' % (env['NAMESPACE'], tname))
    return (newtargets, source)
  else:
    return (targets, source)

res_builder = SCons.Builder.Builder(action=res_action,
                                   emitter=res_emitter,
                                   src_suffix='.resx',
                                   suffix='.resources',
                                   src_builder=[],
                                   source_scanner=SCons.Tool.SourceFileScanner)

SCons.Tool.SourceFileScanner.add_scanner('.resx', SCons.Defaults.CScan)

def generate(env):
  envpaths = env['ENV']['PATH']
  env['CLIREFPATHS']  = envpaths.split(os.pathsep)
  env['CLIMODPATHS']  = []
  env['ASSEMBLYREFS'] = []
  env['NETMODULES']   = []

  env['BUILDERS']['CLIProgram'] = MsCliBuilder
  env['BUILDERS']['CLIAssembly'] = MsCliLibBuilder
  env['BUILDERS']['CLILibrary'] = MsCliLibBuilder
  env['BUILDERS']['CLIModule']  = MsCliModBuilder
  env['BUILDERS']['CLILink']    = MsCliLinkBuilder
  env['BUILDERS']['CLIAsmLink'] = MsCliAsmLinkBuilder
  env['BUILDERS']['CLITypeLib'] = MsCliTypeLibBuilder
  
  env['CSC']          = 'csc'
  env['_CSCLIBS']     = "${_stripixes('-r:', CILLIBS, '', '-r', '', __env__)}"
  env['_CSCLIBPATH']  = "${_stripixes('-lib:', CILLIBPATH, '', '-r', '', __env__)}"
  env['CSCFLAGS']     = SCons.Util.CLVar('-nologo -noconfig')
  env['_CSCFLAGS']    = cscFlags
  env['_CSC_SOURCES'] = cscSources
  env['_CSC_REFS']    = cscRefs
  env['_CSC_MODS']    = cscMods
  env['CSCCOM']       = SCons.Action.Action('$CSC $CSCFLAGS $_CSCFLAGS -out:${TARGET.abspath} $_CSC_REFS $_CSC_MODS $_CSC_SOURCES', '$CSCCOMSTR')
  env['CSCLIBCOM']    = SCons.Action.Action('$CSC -t:library $CSCFLAGS $_CSCFLAGS $_CSCLIBPATH $_CSCLIBS -out:${TARGET.abspath} $_CSC_REFS $_CSC_MODS $_CSC_SOURCES', '$CSCLIBCOMSTR')
  env['CSCMODCOM']    = SCons.Action.Action('$CSC -t:module $CSCFLAGS $_CSCFLAGS -out:${TARGET.abspath} $_CSC_REFS $_CSC_MODS $_CSC_SOURCES', '$CSCMODCOMSTR')
  env['CLIMODPREFIX'] = ''
  env['CLIMODSUFFIX'] = '.netmodule'
  env['CSSUFFIX']     = '.cs'

  # this lets us link .netmodules together into a single assembly
  env['CLILINK']      = 'link'
  env['CLILINKFLAGS'] = SCons.Util.CLVar('-nologo -ltcg -dll -noentry')
  env['CLILINKCOM']   = SCons.Action.Action('$CLILINK $CLILINKFLAGS -out:${TARGET.abspath} $SOURCES', '$CLILINKCOMSTR')

  env['CLIASMLINK']   = 'al'
  env['CLIASMLINKFLAGS'] = SCons.Util.CLVar('')
  env['_ASMLINK_SOURCES'] = alLinkSources
  env['CLIASMLINKCOM'] = SCons.Action.Action('$CLIASMLINK $CLIASMLINKFLAGS -out:${TARGET.abspath} $_ASMLINK_SOURCES', '$CLIASMLINKCOMSTR')

  env['CLIRC']        = 'resgen'
  env['CLIRCFLAGS']   = ''
  env['CLIRCCOM']     = '$CLIRC $CLIRCFLAGS $SOURCES $TARGETS'
  env['BUILDERS']['CLIRES'] = res_builder

  env['TYPELIBIMP']       = 'tlbimp'
  env['TYPELIBIMPFLAGS'] = SCons.Util.CLVar('-sysarray')
  env['_TYPELIBIMPFLAGS'] = tlbimpFlags
  env['TYPELIBIMPCOM']    = SCons.Action.Action('$TYPELIBIMP $SOURCES $TYPELIBIMPFLAGS $_TYPELIBIMPFLAGS', '$TYPELIBIMPCOMSTR')

  SConsEnvironment.CLIRefs = CLIRefs
  SConsEnvironment.CLIMods = CLIMods
  SConsEnvironment.AddToRefPaths = AddToRefPaths
  SConsEnvironment.AddToModPaths = AddToModPaths
  SConsEnvironment.PublisherPolicy = PublisherPolicy
  
def exists(env):
  return env.Detect('csc')
```
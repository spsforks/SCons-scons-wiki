
This is a bit rough but this builder is for generating Corba client and server stubs using the Orbix 6.0 idl compiler from iona. 

Note originally we had one builder that generated all 4 output files in one hit, and we directly used that in the SConscripts.  We realised tihs is a hard way to do it as after using the builder we then would filter out the header files and pass the C++ files to a Object builder. 

The untested shown approach below is to use a wrapper builder that around the real builder, the wrapper does the filtering  for us.  It is important that the real builder still outputs all the files including the headers so that scons can match the headers against dependencies from #include statements. 

This approach could actaully be taken even further, and one [CorbaIdl](CorbaIdl)() builder could generate all the suported language mappings, ie c++, java, c, python etc.  The user would simply use the appropriate wrapper depending on the files they needed. 

Apologies in advanve for any typos, this is manual reentry of relevant bits from a big printout, and I do not have the tool here to test.  Used with scons 0.95 


```python
#!python

import SCons.Scanner.IDL

idlCmd = '/blah/bin/idl $_CPPINCFLAGS -base:-Oh${TARGET.dir}:-Oc${TARGET.dir} -poa:-i:-Oh${TARGET.dir}:-Oc${TARGET.dir} $SOURCES'

def idl_emitter(target, source, env):
  "Produce list of files created by idl compiler"
  base,ext = SCons.Util.splitext(str(source[0]))
  hh = base + '.hh'
  Shh = base + 'S.hh'
  Ccxx = base + 'C.cxx'
  Scxx = base + 'S.cxx'
  t = [hh, Shh, Ccxx, Scxx]
  return (t, source)

bld = Builder(
  action=idlCmd,
  src_suffix = '.idl',
  emitter = idl_emitter,
  source_scanner = SCons.Scanner.IDL.IDLScan(),
  suffix = '.hh')

def CorbaCpp(env, sources):
  'Trigger idl Builder, but only return the Cpp source files'
  out = env.CorbaIdl(sources)
  cpp=[]
  for i in out :
    if str(i)[-4:] == '.cxx' :
      cpp.append(i)

  Object(cpp)
  return cpp

env.Append(BUILDERS={'CorbaIdl':bld})
env.Append(BUILDERS={'CorbaCpp':CorbaCpp})

# setup orbix environmet for idl command
# it seems to expect some things I didn't!
env.AppendENVPath('LD_LIBRARY_PATH', 'blah')
env.Append(LIBPATH='blah')
env['ENV']['IT_LICENSE_FILE'] = 'blah'
env['ENV']['IT_CONFIG_DOMAINS_DIR'] = 'blah'
env['ENV']['IT_DOMAIN_NAME'] = 'blah'
env['ENV']['IT_PRODUCT_SHLIB_DIR'] = 'blah'
env['ENV']['IT_PRODUCT_DIR'] = 'blah'
env['ENV']['IT_PRODUCT_VER'] = 'blah'

# setup to find libraries
env.Append(LIBPATH='blah')

# link programs with these libraries for orbix
corbaLibs=Split('it_poa it_art it_ifc it_naming')

# we do NOT use CCPATH for orbix headers as they are full of warnings.
# This also avoids scons checksumming the headers anyway, which is faster.
env.Append(CCFLAGS='-isystemblah')



# use like so
tmp = env.CorbaCpp('thingy.idl')
Library('thingy', tmp)


```
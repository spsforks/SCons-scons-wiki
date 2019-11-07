This is rough builder for Corba-using applications using Tao. It is based on the other builder [CorbaBuilder](CorbaBuilder), but this one works without any modifications and allows you to build client and server applications separately. With minor modifications, this also works for Orbacus from IONA.

```python
import SCons.Scanner.IDL

def idl2many_emitter(target, source, env):
  new_t = []
  fls = source[0]
  flt = target[0]
  if str(fls).endswith('.idl'):
    # you might need to adapt these to your suffixes and generation (e.g. if you don't generate S_T files)
    for suf in [ 'C.h', 'C.cpp', 'C.inl', 'S.h', 'S.cpp', 'S.inl', 'S_T.h', 'S_T.cpp', 'S_T.inl' ]:
        new_t.append( str(flt) + suf)
  return (new_t, source)

# you might also use this generator instead of the action below (in this concrete case, it is for Orbacus)
#def idl2many_generator(source, target, env, for_signature):
#  env['INCPREFIX'] = '-I'
#  return "$IDL $IDLFLAGS --output-dir ${TARGET.dir} $_CPPINCFLAGS ${SOURCE}"

idl2many_bld = Builder(
  action="$IDL $IDLFLAGS $_CPPINCFLAGS ${SOURCE} -o ${TARGET.dir}",
  src_suffix = '.idl',
  emitter = idl2many_emitter,
  source_scanner = SCons.Scanner.IDL.IDLScan(),
  single_source = 1
)

def idl2cppC_bld(env, target, source):
  idl_res = env.CorbaIdl(source)
  cpp = []
  for fl in idl_res:
    if str(fl).endswith('C.cpp'):
      cpp.append(env.Object(fl))
  return cpp

def idl2cppS_bld(env, target, source):
  idl_res = env.CorbaIdl(source)
  cpp = []
  for fl in idl_res:
    if str(fl).endswith('C.cpp') or str(fl).endswith('S.cpp'):
      cpp.append(env.Object(fl))
  return cpp

Import('env')

env.Append(
  IDL = 'tao_idl',
  IDLFLAGS = '',
)

env.Append(BUILDERS={
    'CorbaIdl' : idl2many_bld,
    'CorbaBuildC' : idl2cppC_bld,
    'CorbaBuildS' : idl2cppS_bld,
})

cli_corba = env.CorbaBuildC('hellworld.idl')
srv_corba = env.CorbaBuildS('hellworld.idl')

env.Program(
  target = 'client',
  source = [ 'client.cc', cli_corba, ],
  CPPPATH = [ '.' ],
  LIBS = [
    'TAO_CosLifeCycle', 'TAO_PortableServer', 'TAO_CosNaming'
  ],
)

env.Program(
  target = 'server',
  source = [ 'server.cc', srv_corba, ],
  CPPPATH = [ '.' ],
  LIBS = [
    'TAO_CosLifeCycle', 'TAO_PortableServer', 'TAO_CosNaming',
    'TAO_Utils', 'TAO_PI', 'TAO_CodecFactory'
  ],
)

```
-- Teftin, --platon42 
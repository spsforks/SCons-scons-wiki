

# Building Pyrex extensions for Python using SCons

This recipe is based on the example for building boost.python extensions from page [PythonExtensions](PythonExtensions). Pyrex builder was peeked from [http://pyinsci.blogspot.com/2007/01/building-pyrex-with-scons.html](http://pyinsci.blogspot.com/2007/01/building-pyrex-with-scons.html) 

I've combined info from both pages and now I have SConstruct to build my Pyrex extensions under OS Windows with MSVC 2003 compiler. This works fine for me on Python 2.5/2.4 with SCons v.1.1. 

I've tried to make my Sconstruct.pyrex more or less smart and decided to reuse typical setup.py for creating scons targets. To achieve this one need to slightly change setup.py: 

1) SConstruct.pyrex tries to get extension list to build by invoking function get_extensions() from setup.py. This function should return list of extensions to build. 

2) Because setup.py is imported by SConstruct.pyrex one need to guard main setup() function from execution, to achieve this one need to make it conditional, e.g.: 
```txt
if __name__ == '__main__':
        setup(...)
```
3) To reduce probability of user errors it's better to use get_extensions() in your setup.py, i.e. 
```txt
if __name__ == '__main__':
     setup(
       name = 'Demos',
       ext_modules=get_extensions(),
       cmdclass = {'build_ext': build_ext}
     )
```
Changing setup.py in this way one ends up with fully workable `python setup.py build_ext` command and in the same time one can use SConstruct.pyrex for building extensions. 

I've attached my SConstruct.pyrex and modified primes.pyx example from standard Pyrex sources tarball (the only thing I've changed is setup.py). You can build it either with 
```txt
python setup.py build_ext -i
```
or 
```txt
scons -f SConstruct.pyrex
```
I've tried to write SConstruct.pyrex in cross-platform way, but I suspect it should be adjusted to use with mingw or gcc (@Linux). 

SConstruct.pyrex: 
```python
#!python

import distutils.sysconfig
import os
import re
import sys


def TOOL_DISTUTILS(env):
    """Add stuff needed to build Python/Pyrex extensions [with MSVC]."""
    (cc, opt, so_ext) = distutils.sysconfig.get_config_vars('CC', 'OPT', 'SO')
    if cc:
        env['CC'] = cc
    env.AppendUnique(CPPPATH=[distutils.sysconfig.get_python_inc()])
    if os.name == 'nt':     # OS Windows
        if sys.version_info[:2] in ((2,4), (2,5)):
            # this flags suitable for Python 2.4/2.5 + MSVC 2003 compiler
            cppflags = Split("/Ox /MD /W3 /GX /DNDEBUG")
        else:
            raise Exception("Unsupported Python version.")
    env.AppendUnique(CPPFLAGS=cppflags)
    if opt:
        env.AppendUnique(CPPFLAGS=opt)
    env.AppendUnique(LIBPATH=[distutils.sysconfig.PREFIX+"/libs"])
    env['SHLIBPREFIX'] = ""   # gets rid of lib prefix
    env['SHLIBSUFFIX'] = so_ext


env = Environment(tools=['default', TOOL_DISTUTILS])

# adding Pyrex builder
if os.name == 'nt':
    pyrex_executable = '"%s" "%s"' % (sys.executable,
        os.path.join(sys.prefix, 'Scripts', 'pyrexc.py'))
else:
    pyrex_executable = 'pyrexc'
pyxbld = Builder(action='%s -o $TARGET $SOURCE' % pyrex_executable)
env.Append(BUILDERS={'Pyrex': pyxbld})


# build extension(s)
import setup
for e in setup.get_extensions():
    envx = env.Clone()
    # adjust compiler flags/options
    if e.define_macros:
        envx.AppendUnique(CPPDEFINES=dict(e.define_macros))
    if e.libraries:
        envx.AppendUnique(LIBS=e.libraries)
    if e.include_dirs:
        envx.AppendUnique(CPPPATH=e.include_dirs)
    # looking for common src dir prefix
    sources = e.sources[:]
    variant_dir = None
    src_dir = None
    for s in sources:
        parts = re.split(r'[\\/]', s, 1)
        if len(parts) != 2 or parts[0] == '':
            break
        else:
            prefix = parts[0]
            if src_dir is None:
                src_dir = prefix
            elif prefix != src_dir:
                break
    else:
        # src_dir found
        if src_dir:
            variant_dir = os.path.join('build',
                'temp.%s-%d.%d' % (sys.platform, sys.version_info[0], sys.version_info[1]))
            envx.VariantDir(os.path.join(variant_dir, src_dir),
                src_dir,
                duplicate=0)
            sources = [os.path.join(variant_dir, s) for s in sources]
    # check if we build pyrex extension
    for ix, s in enumerate(sources):
        if s.endswith('.pyx'):
            cfile = s[:-4]+'.c'
            sources[ix] = cfile
            envx.Pyrex(cfile, s)
    # and schedule it for building
    envx.SharedLibrary(e.name.replace('.', os.sep), sources)
```
Example of setup.py: 
```python
#!python
from distutils.core import setup
#from distutils.extension import Extension
from Pyrex.Distutils.extension import Extension
from Pyrex.Distutils import build_ext


def get_extensions():
    return [
        Extension("primes",       ["primes.pyx"]),
#        Extension("spam",         ["spam.pyx"]),
#        Extension("numeric_demo", ["numeric_demo.pyx"]),
        ]


if __name__ == '__main__':
    setup(
      name = 'Demos',
      ext_modules=get_extensions(),
      cmdclass = {'build_ext': build_ext}
    )
```
primes.pyx source file: 
```python
#!python
def primes(int kmax):
    cdef int n, k, i
    cdef int p[1000]
    result = []
    if kmax > 1000:
        kmax = 1000
    k = 0
    n = 2
    while k < kmax:
        i = 0
        while i < k and n % p[i] <> 0:
            i = i + 1
        if i == k:
            p[k] = n
            k = k + 1
            result.append(n)
        n = n + 1
    return result
```
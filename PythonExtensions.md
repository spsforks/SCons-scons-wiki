

# Building Python Extensions with SCons

Python provides the distutils tools to build Python extension modules. 

This first example is very simple for a beginner new to SWIG and SCons,  the sources are from the ["SWIG tutorial"](http://www.swig.org/tutorial.html): 


```python
#!python
import distutils.sysconfig
env = Environment(SWIGFLAGS=['-python'],
                  CPPPATH=[distutils.sysconfig.get_python_inc()],
                  SHLIBPREFIX="")
env.SharedLibrary('_example.so', ['example.c', 'example.i'])
```
This example shows a way of using the distutils package build extension modules with SCons. 


```python
#!python
Import("tool_prefix")
import distutils.sysconfig, os
vars = distutils.sysconfig.get_config_vars('CC', 'CXX', 'OPT', 'BASECFLAGS', 'CCSHARED', 'LDSHARED', 'SO')
for i in range(len(vars)):
    if vars[i] is None:
        vars[i] = ""
(cc, cxx, opt, basecflags, ccshared, ldshared, so_ext) = vars
lib = SharedLibrary("dparser_swigc",
                    ["pydparser.c", "make_tables.c", "dparser_wrap.c"],
                    LIBS=['mkdparse', 'dparse'],
                    LIBPATH=["../"],
                    CC=cc,
                    SHLINK=ldshared,
                    SHLINKFLAGS=[],
                    SHLIBPREFIX="",
                    SHLIBSUFFIX=so_ext,
                    CPPPATH=[distutils.sysconfig.get_python_inc()],
                    CPPDEFINES={"SWIG_GLOBAL":None},
                    CPPFLAGS=basecflags + " " + opt)
if type(lib) == type([]): lib = lib[0]
dp1 = Install(os.path.join(tool_prefix, "lib"), "dparser.py")
dp2 = Install(os.path.join(tool_prefix, "lib"), lib)
Depends(dp1, dp2)
```
The following is a boost.python example to compile the Hello.cpp example. Needs to be expanded to other platforms and compilers. This example creates a compile environment to set the parameters. 


```python
#!python
# Example build for Boost.python example hello
# Tested on Windows VC7 (VC6.0 possible see below?) with Python 2.3
# must put debug multi-threaded  boost_python.dll and .lib in current directory.
# Currently compiles a debug version
# following line gave me an error
#Import("tool_prefix")
import distutils.sysconfig, os
# XXX: these should just set the defaults and let user override them with an Environment var
boost_prefix=r"D:\usr\boost_1_33_1"
boost_libdir=boost_prefix + "/libs/..../shared-linkable-true/"
def TOOL_BOOST_DISTUTILS(env):
    """Add stuff needed to build Python extensions with boost.  """
    vars = distutils.sysconfig.get_config_vars('CC', 'CXX', 'OPT', 'BASECFLAGS', 'CCSHARED', 'LDSHARED', 'SO')
    for i in range(len(vars)):
        if vars[i] is None:
            vars[i] = ""
    (cc, cxx, opt, basecflags, ccshared, ldshared, so_ext) = vars
    #For some reason all but so_ext are zero
    #print 'cc',cc, 'cxx',cxx, 'opt',opt
    #print 'basecflags',basecflags, 'ccshared',ccshared,
    #print 'ldshared',ldshared, 'so_ext',so_ext
    #print distutils.sysconfig.get_python_inc()
    env.AppendUnique(CPPPATH=[distutils.sysconfig.get_python_inc(),boost_prefix])
    env.AppendUnique(CXXFLAGS=Split("/Zm800 -nologo /EHsc /DBOOST_PYTHON_DYNAMIC_LIB /Z7 /Od /Ob0 /EHsc /GR /MDd /Op  /wd4675 /Zc:forScope /Zc:wchar_t"))
    # Use the following for VC6.0
    #env.AppendUnique(CXXFLAGS=Split("/Zm800 /nologo /DBOOST_PYTHON_DYNAMIC_LIB /Z7 /Od /Ob0 /EHsc /GR /MDd"))
    env.AppendUnique(LIBPATH=[boost_libdir, distutils.sysconfig.PREFIX+"/libs"])
    env.AppendUnique(LIBS="boost_python")
    env['SHLIBPREFIX']=""   #gets rid of lib prefix
    env['SHLIBSUFFIX']=so_ext
Default('.')
env=Environment(tools=['default', TOOL_BOOST_DISTUTILS])
hello = env.SharedLibrary(target='hello', source=['hello.cpp',])
#TODO add install line
```
[AlexanderBelchenko](AlexanderBelchenko) have created recipe to build Pyrex extensions for Python based on the last example. See [PyrexPythonExtensions](PyrexPythonExtensions) page for details.  

Julien Boeuf noted that if you try to run the scons example on a Mac, it won't work because what you need on the Mac is a 'bundle' and not a dylib. The way to do it is to add the appropriate flags to your environment. It is also a good idea to do a universal build for both powerpc and x86 architectures. Then Greg Noel pointed out that Gary Oberbrunner has added a "[LoadableModule](LoadableModule)" that captures the essence of a bundle in a platform-neutral way.  You can use that together with the FRAMEWORKSFLAGS to get a much simpler invocation. 

For the record, here's a fragment from a SConscript of Noel's that builds a SWIG library on Mac, Linux, Solaris, and other Unix-like platforms; it could be simplified a bit to remove the options for his specific configuration.  It also doesn't include the rule to build sample.i from the *.h files; I leave that as an exercise for the reader. 


```txt
# SWIG library for Python
## FIXME: produces sample.py as a side-effect which is not cleaned
Alias('swig', env.LoadableModule('sample', 'sample.i',
     SWIGFLAGS = '-c++ -python -shadow -Wall'.split(),
     CPPPATH = ['.', os.path.join(sys.prefix, 'include',
         'python%d.%d'%(sys.version_info[0],sys.version_info[1]))],
     CCFLAGS = '-O', LIBS = lib, OBJPREFIX = 'tmp/',
     LDMODULEPREFIX='_', LDMODULESUFFIX = '.so',
     FRAMEWORKSFLAGS = '-flat_namespace -undefined suppress',
     )
)
```
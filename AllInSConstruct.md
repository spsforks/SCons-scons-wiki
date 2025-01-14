

## INTRO

This aims to be a complete, usable, and fairly non-trivial SCons example for C/C++. 

I set out with the goal of making a simple to use SCons-based build set up that would automatically build Release and Debug variants into separate directories. Additionally I sometimes like to have my build consolidate all the libs, executables, and/or headers into given directories after building. For instance creating, a `source_tree/Lib` dir and a `source_tree/Include` directory for the libs and public header files for utility library projects. 

And when you build multiple variations of a lib, some Debug some Release, you often want to give them different names, like 'foo.lib' vs 'foo_dbg.lib' (or 'libfoo.a' vs 'libfoo_dbg.a'). The scripts below handle all that, while providing a few other niceties. 

This is still a work in progress, but already it does a lot of things I find useful. 

Naturally, you want your SConscript files to be as simple as possible and basically have them 'include' all your standard rules for building. I considered doing that via the Python `execfile()` function, and storing the default rules in a separate file at the build root, but in the end it seemed like I might as well just `Export`/`Import` a build object with all the smarts in methods. Then the global build object can just be defined in the main SConstruct. Originally I thought it would be good to put all the source and target data etc into a big dictionary structure in the SConscript files and pass that to my processing methods, but upon consideration it became clear that what I was really accomplishing with all that was decorating, or 'wrapping', the default `Program()` and `Library()` builder methods. The [WrapperFunctions](WrapperFunctions) Wiki page describes exactly how to do this in a much more straightforward way. Part of the benefit of a wrappers approach is that to the SConscript writer, the syntax looks pretty much like the basic SConscript examples in the SCons User's Guide. 

So basically the result is that the SConscript just calls some things that look pretty similar to `Program()` and `Library()` calls (specifically, I've named them `dProgram()` and `dLibrary()`), but all the extra things happen that I described above. For example:

```python
Import('env')
env.dLibrary(target='foo',source='foo.c *.cpp',CPPPATH=['#Include'])
```
Complete examples of the SConstruct files are included below. 


## OVERVIEW

So what's good about it: 

   * The SConscripts are relatively simple 
         1. Easy to write initially 
         1. Easier to edit by non-SCons experts 
   * All the logic is in the SConstruct, so only need to modify SConstruct to change whole build behavior. 
   * Variant build products are put in separate sub-directories (build/Debug, build/Release) 
         1. Using the convention of `debug=1` to specify a debug build 
         1. Just two variants right now, `Debug` and `Release` 
   * Each sub-SConscript can define multiple libs and exes to build and install, and also specify headers to install. 
         1. Build products and sources are described using same syntax as the built-in builders, like `Program()` 
         1. New functions include `dProgram()`,`dLibrary()`,`dSubdirs()`, and `dHeaders()`. The latter installs headers. 
   * Lists of source files can include glob patterns 
         1. Glob patterns search the _source_ dir not the _build_ dir. The latter is SCons' not-very-useful default. 
         1. Glob patterns relative to the root using the '#' character (e.g. `#subdir/*.cpp`) also work properly. 
   * Optional install step for libs apps and headers. 
         1. Not a system install, but copying elsewhere in the build tree 
         1. E.g., allows copying all libs to a #lib directory 
         1. E.g., allows copying all exes to a #bin directory 
         1. E.g., allows copying all include files to a #include directory 
   * Optional decoration of lib names based on build variant. E.g. tack on a `'_dbg'` to the end of library names in the debug variant. 
What needs work: 

   * The mechanism for linking with external libraries. ([ParseConfig](ParseConfig)?) 
   * Proper settings of compiler flags for more compilers. 
   * External specification of site-specific info like standard include dirs. 
   * Overall better separation of config data and instructions in the SConstruct file. (Currently there are many things you have to delve into the guts of the SConstruct to change, like the names of the install directories for libs, programs, and headers.) 
Other possible negatives: 

   * Too C/C++ specific. 
   * Recent Python required (I use a fair number of list comprehensions. And being pretty new to Python, I may be using other 'new' Python stuff without realizing it, because it's all new to me.) 

## THE CODE

Here are the files. 

An example SConscript for a dir with some libraries: 

```python
Import('env')
env.dLibrary(target='viewer',
             libsrc = '''
               viewer.cpp
               #camera/camdisplay.cpp
               #math/mat16fv.cpp
               #timer/stopwatch.cpp
             ''',
             CPPPATH = Split('#camera #math #math_objs #timer')
             )
env.dHeaders('*.hpp #camera/*.hpp trackball.h')
```
There's only one lib there, but you can of course make multiple dLibrary calls. Also note that not all the sources for this lib are located in the directory with this SConscript. That's fine. The `dHeaders` call is used to install the headers listed in the '#Include' directory of the tree. Note that it can take a single string that include a combination of globs, build relative globs, and non-globs. Any non-list argument is automatically `Split()` and anything that looks like a glob is globbed on (and globbed properly, in the source directory, not in the build directory as is the default SCons behavior) 

An example SConscript for a dir with several binaries: 

```python
Import('env')
 
for appname in Split('''
    test_basic
    test_basic_oo
    test_keymouse
    test_menu
'''):
    env.dProgram(target=appname, source=[appname + '.cpp'],
                 CPPPATH=Split('#viewer #camera #math'),
                 LIBPATH=['#lib'],
                 LIBS=['viewer'])
```
The above example uses a loop, but you could certainly also just write each one, one-by-one, if you're afraid of Python and find that more intuitive. 

Finally, the top-level Root SConscript just calls subdirs: 

```python
Import('env')
 
env.dSubdirs('subdir1 subdir2 librarysrc tests')
```
And now the main SConstruct file: 

```python
# The goal here is to be able to build libs and programs using just
# the list of sources.
# I wish to 'wrap' or 'decorate' the base scons behavior in
# a few ways:
# * default variant builds ('Debug'/'Release')
# * automatic build dirs (which are variant-sensitive)
# - with work-arounds to make *everything* go in the build dir
# * automatic no-fuss globs (that *also* work properly for build dirs)
# * default platform-specific build env vars (also variant-sensitive)
# (i.e. some extra compiler specific CCFLAGS and such)
# * automatic 'installation' of libs, program, and headers into specific
# directories (e.g. '#lib', '#bin', and '#include')
import sys
 
############################################
# Site-specific setup
 
# Hmm... this should go somewhere else. SCustomize??
# This is my own site-specific win32 setup...
if sys.platform == 'win32':
    stdinc = [r'c:\usr\include']
    stdlibinc = [r'c:\usr\lib']
else:
    stdinc = []
    stdlibinc = []
 
############################################
# Generic boiler plate
#-------------------------------------------
import os
import os.path
 
opts = Options('SCustomize')
opts.Add('debug', 'Build with debugging symbols', 0)
opts.Add('CC', 'Set C compiler')
 
env = Environment(options=opts)
Help(opts.GenerateHelpText(env))
 
debug = env.get('debug',0)
build_base = 'build'
 
if debug:
    env.Append(CPPDEFINES = ['DEBUG', '_DEBUG'])
    variant = 'Debug'
else:
    env.Append(CPPDEFINES = ['NDEBUG'])
    variant = 'Release'
 
############################################
# PLATFORM SPECIFIC CONFIGS
############################################
#-------------- win32 MSVC -----------------
if env['CC'] == 'cl':
    def freeMSVCHack(env, vclibs):
        # SCons automatically finds full versions of msvc via the registry, so
        # if it can't find 'cl', it may be because we're trying to use the
        # free version
        def isMicrosoftSDKDir(dir):
            return os.path.exists(os.path.join(dir, 'Include', 'Windows.h')) and os.path.exists(os.path.join(dir, 'Lib', 'WinMM.lib'))
 
        def findMicrosoftSDK():
            import SCons.Platform.win32
            import SCons.Util
            import re
            if not SCons.Util.can_read_reg:
                return None
            HLM = SCons.Util.HKEY_LOCAL_MACHINE
            K = r'Software\Microsoft\.NETFramework\AssemblyFolders\PSDK Assemblies'
            try:
                k = SCons.Util.RegOpenKeyEx(HLM, K)
                p = SCons.Util.RegQueryValueEx(k,'')[0]
                # this should have \include at the end, so chop that off
                p = re.sub(r'(?i)\\+Include\\*$','',p)
                if isMicrosoftSDKDir(p): return p
            except SCons.Util.RegError:
                pass
 
            K = r'SOFTWARE\Microsoft\MicrosoftSDK\InstalledSDKs'
            try:
                k = SCons.Util.RegOpenKeyEx(HLM, K)
                i=0
                while 1:
                    p = SCons.Util.RegEnumKey(k,i)
                    i+=1
                    subk = SCons.Util.RegOpenKeyEx(k, p)
                    try:
                        p = SCons.Util.RegQueryValueEx(subk,'Install Dir')[0]
                        # trim trailing backslashes
                        p = re.sub(r'\\*$','',p)
                        if isMicrosoftSDKDir(p): return p
                    except SCons.Util.RegError:
                        pass
            except SCons.Util.RegError:
                pass
 
            return None
 
        # End of local defs. Actual freeMSVCHack begins here
        if not env['MSVS'].get('VCINSTALLDIR'):
            if os.environ.get('VCToolkitInstallDir'):
                vcdir=os.environ['VCToolkitInstallDir']
                env.PrependENVPath('INCLUDE', os.path.join(vcdir, 'Include'))
                env.PrependENVPath('LIB', os.path.join(vcdir, 'Lib'))
                env.PrependENVPath('PATH', os.path.join(vcdir, 'Bin'))
                env['MSVS']['VERSION'] = '7.1'
                env['MSVS']['VERSIONS'] = ['7.1']
            if not env['MSVS'].get('PLATFORMSDKDIR'):
                sdkdir = findMicrosoftSDK()
                if sdkdir:
                    env.PrependENVPath('INCLUDE', os.path.join(sdkdir, 'Include'))
                    env.PrependENVPath('LIB', os.path.join(sdkdir, 'Lib'))
                    env.PrependENVPath('PATH', os.path.join(sdkdir, 'Bin'))
                    env['MSVS']['PLATFORMSDKDIR']=sdkdir
            # FREE MSVC7 only allows
            # /ML(libc) /MT(libcmt) or /MLd(libcd)
            # Full IDE versions also have
            # /MD(msvcrtd) /MTd(libcmtd) and /MDd(msvcrtd)
            # So if you want to debug with the freever, the only option is
            # the single-threaded lib, /MLd
            vclibs['Debug']='/MLd'
            vclibs['Release']='/MT'
 
    # MSVC SETUP
    # MDd is for multithreaded debug dll CRT (msvcrtd)
    # MD is for multithreaded dll CRT (msvcrt)
    # These are just my preferences
    vclibs = {'Debug':'/MDd','Release':'/MD'}
    freeMSVCHack(env, vclibs)
 
    env.Append(CCFLAGS=[vclibs[variant]])
    if debug:
        env.Append(CCFLAGS=Split('/Zi /Fd${TARGET}.pdb'))
        env.Append(LINKFLAGS = ['/DEBUG'])
        # env.Clean('.', '${TARGET}.pdb')
        # Need to clean .pdbs somehow! The above line doesn't work!
    else:
        env.Append(CCFLAGS=Split('/Og /Ot /Ob1 /Op /G6'))
 
    env.Append(CCFLAGS=Split('/EHsc /J /W3 /Gd'))
    env.Append(CPPDEFINES=Split('WIN32 _WINDOWS'))
 
#-------------- gcc-like (default) ---------
else: # generic posix-like
    if debug:
        env.Append(CPPFLAGS = ['-g'])
    else:
        env.Append(CPPFLAGS = ['-O3'])
#-------------------------------------------
 
 
# Put all the little .sconsign files into one big file.
# (Does this slow down parallel builds?)
# Need to create the build dir before we put the signatures db in there
fullbuildpath = Dir(build_base).abspath
if not os.path.exists(fullbuildpath): os.makedirs(fullbuildpath)
import dbhash
env.SConsignFile(os.path.join(build_base, 'sconsignatures'), dbhash)
 
 
# Make a singleton global object for keeping track of all the extra data
# and methods that are being added
class Globals:
    def __init__(self):
        self.env = env
        self.stdinc = stdinc
        self.stdlibinc = stdlibinc
        self.variant = variant
        self.build_base = os.path.join(build_base, variant)
        self.libname_decorators = { 'Debug' : '_dbg' }
        self.appname_decorators = { 'Debug' : '_dbg' }
        self.incinstdir = '#include'
        self.libinstdir = '#lib'
        self.appinstdir = '#bin'
        self.objcache = {}
 
    def Glob(self, pat):
        ## GLOB IN THE REAL SOURCE DIRECTORY (NOT BUILD DIR)
        import glob
        prevdir = os.getcwd();
        if pat[0] != '#':
            os.chdir(self.env.Dir('.').srcnode().abspath)
            ret = glob.glob(pat)
        else:
            pat = pat[1:]
            base = os.path.dirname(pat)
            searchdir = self.env.Dir('#').srcnode().abspath
            os.chdir(searchdir)
            ret = ['#'+x for x in glob.glob(pat)]
        os.chdir(prevdir)
        return ret
 
    def GlobExpand(self, list):
        ## look for pattern-like things and glob on those
        ret = []
        for item in list:
            if item.find('*') or item.find('?') or item.find('['):
                ret += self.Glob(item)
            else:
                ret += [item]
        return ret
 
    def IsALocalLib(self, lib):
        # This is rather heuristic determining if a lib is local or not
        return lib.find('/') or lib.find(os.sep) or lib[0]=='#'
 
    def MyHeaderMethod(self, env, source, **dict):
        if type(source)==type(''): source = Split(source)
        source = self.GlobExpand(source)
        nodes = []
        if hasattr(self,'incinstdir') and self.incinstdir:
            for i in source:
                nodes.append( env.Install(self.incinstdir, i) )
        return nodes
 
    def MyLibraryMethod(self, env, **dict):
        relincs = dict.get('CPPPATH',[])
        dict['CPPPATH'] = ['.'] + relincs + self.stdinc
 
        # These shenanigans are necessary to get SCons to build non-local
        # sources in the VariantDir instead of their own local directories
        target = dict.pop('target')
        source = dict.pop('source')
        if type(source)==type(''): source = Split(source)
        allsrc = []
        for x in source:
            objbase = os.path.basename(x)
            if self.objcache.get(objbase):
                #print 'Reusing node', objbase
                #NOTE: We should check that defines etc are all the same!!
                allsrc += self.objcache[objbase]
            else:
                onode = env.SharedObject(
                    os.path.splitext(objbase)[0], x,
                    **dict)
                allsrc += onode
                self.objcache[objbase]=onode
 
        targpath = '#' + os.path.join(self.build_dir, target)
        # decorate libname with e.g. '_dbg'
        if hasattr(self,'libname_decorators'):
            targpath += self.libname_decorators.get(self.variant,'')
 
        dict['source'] = allsrc
        dict['target'] = targpath
        node = env.Library(**dict)
        if hasattr(self,'libinstdir') and self.libinstdir:
            env.Install(self.libinstdir, node)
        return node
 
    def MyProgramMethod(self, env, **dict):
        # Enhance CPPPATH,LIBPATH
        dict['CPPPATH'] = ['.'] + dict.get('CPPPATH',[]) + self.stdinc
        dict['LIBPATH'] = dict.get('LIBPATH',[]) + self.stdlibinc
 
        # These shenanigans are necessary to get SCons to build non-local
        # sources in the VariantDir instead of their own local directories
        target = dict.pop('target')
        source = dict.pop('source',[])
        if type(source)==type(''): source = Split(source)
        allsrc = []
        for x in source:
            objbase = os.path.basename(x)
            if self.objcache.get(objbase):
                print 'Reusing node', objbase
                allsrc += self.objcache[objbase]
            else:
                onode = self.env.SharedObject(
                    os.path.splitext(objbase)[0], x,
                    **dict)
                allsrc += onode
                self.objcache[objbase]=onode
 
        targpath = '#' + os.path.join(self.build_dir, target)
        # decorate app name with e.g. '_dbg'
        if hasattr(self,'appname_decorators'):
            deco = self.appname_decorators.get(self.variant,'')
            targpath += deco
        # decorate local lib names with e.g. '_dbg'
        if hasattr(self,'libname_decorators'):
            deco = self.libname_decorators.get(self.variant,'')
            # decorate source lib names with e.g. '_dbg'
            LIBS = []
            for l in dict.pop('LIBS',[]):
                if self.IsALocalLib(l):
                    #print "Decorating lib", l, '->', l+deco
                    LIBS += [l+deco]
                else:
                    LIBS += [l]
 
        dict['target']=targpath
        dict['source']=allsrc
        dict['LIBS']=LIBS
        node = env.Program(**dict)
 
        if hasattr(self,'appinstdir') and self.appinstdir:
            self.env.Install(self.appinstdir, node)
 
        return node
 
    def MySubdirsMethod(self, env, subdirs, **dict):
        # Build sub-directories
        if type(subdirs)==type(''): subdirs=Split(subdirs)
        for d in subdirs:
            savedir = self.build_dir
            self.build_dir = os.path.join(self.build_dir, d)
            env.SConscript(os.path.join(d, 'SConscript'),
                           exports=['G','env'])
            self.build_dir = savedir
 
 
G = Globals()
 
# Wrap the methods of G into method objects, and then add them
# as methods to Environment.
# See http://www.scons.org/cgi-bin/wiki/WrapperFunctions
def MyLibraryMethod(env, **dict):
    G.MyLibraryMethod(env, **dict)
def MyHeaderMethod(env, source, **dict):
    G.MyHeaderMethod(env, source, **dict)
def MyProgramMethod(env, **dict):
    G.MyProgramMethod(env, **dict)
def MySubdirsMethod(env, subdirs, **dict):
    G.MySubdirsMethod(env, subdirs, **dict)
from SCons.Script.SConscript import SConsEnvironment # just do this once
SConsEnvironment.dLibrary = MyLibraryMethod
SConsEnvironment.dProgram = MyProgramMethod
SConsEnvironment.dHeaders = MyHeaderMethod
SConsEnvironment.dSubdirs = MySubdirsMethod
 
G.build_dir = G.build_base
 
# Call the SConscript in the top-level directory
env.SConscript('SConscript', variant_dir=G.build_dir, exports=['env','G'])
```
Note that a big chunk of that code has to do with trying to find out if the free VC++ toolkit is installed. SCons doesn't currently (ver 0.96.90) detect this even if it is the only compiler available. I just happened to be using the free toolkit while I waited for my actual copy of Visual Studio to arrive, when I started playing with SCons. Consequently I spent a lot of my first day or so with SCons struggling to figure out why on earth the simplest compile with VC required so much code to get the environment right. Well since I struggled through it, I'm including the results of that struggle here in the form of the `freeMSVCHack()` function above. Hopefully something similar will be built into future releases of SCons. 

That's it for now. This is still a work in progress as of 2/18/05, JST. I'll keep updating this page as I make progress. Feedback from the experts is much appreciated. 

One last thing, why did I name all my functions like `dProgram` or `dLibrary`? What's with the `d`? 

The answer is just I wanted to use names similar to the existing builders I was wrapping, and `d` seemed like a decent prefix. Maybe it stands for `different` or `decorated` or `decent`. Or maybe `dorky` :-) 

Bill Baxter 


## ACKNOWLEDGEMENTS

Thanks to Steven Knight, Dobes Vandermeer, Gary Oberbrunner and the other folks on the SCons users mailing list for helpful suggestions, pointers, and advice. And of course a big thanks to Steven Knight and the other developers of SCons. 

If you are interested in a basic tutorial for compiling FORTRAN using SCons, [try this page](llarsen/FortranTutorial). Here is a simple setup for a multiple directory Fortran 90 project, along with some tips on using scons with Fortran. Fortran 90 is a little more complicated to compile than C, in the sense that compiling a single source file can lead to one or more module files, in addition to an object file. Other source files can depend on these module files. To make things worse, there is no standard naming scheme for module files, or standard flags for stipulating where module files should end up. 


# The SConstruct File

The example project has a simple directory layout: 

   * subdir1/ 
   * subdir2/ 
   * build/ 
The source is kept in the directories subdir1 and subdir2. The build directory is used to store object and module files. 

The SConstruct file creates variables for the list of source directories, and then builds up a module search path for the compiler: 


```python
#!python
#
# Paths
#
subdirs = ['subdir1', 'subdir2']
modpath = map(lambda d: os.path.join('#/build',d), subdirs)
```
For each source directory, a corresponding build directory is created under build. The modpath variable is assigned to a list of these build directories. The module files will be kept along with the object files in build directories, and need to be in the module search path used by the compiler. 

The module path is passed to the scons environment as follows: 


```python
#!python
#
# Environment
#
env = Environment(
    F90PATH = modpath,
    FORTRAN = 'g95',
    FORTRANMODDIRPREFIX = '-fmod=',
    FORTRANMODDIR = '${TARGET.dir}',
    LINK = 'g95')
```
The modpath list is passed to the environment via F90PATH. In this example, the g95 compiler has been used, but other compilers work equally well. 

The FORTRANMODDIRPREFIX should be set to the command option of the fortran compiler that stipulates where module files should be moved after a source file has been compiled. G95 uses -fmod for this, but every compiler has a different option, and some have no option at all (more on that below). 

The FORTRANMODDIR is set to ${TARGET.dir}. This gets substituted with the directory of the target file, namely the build directory. The net result is that the module files resulting from a compilation will end up together with the emitted object file. 

LINK has also been set to g95. Most Fortran compilers require you to link with particular Fortran libraries, and the easiest way to achieve this is not to use ld for linking, but the Fortran compiler itself, which automatically links in the libraries. 

Calling the SConscript files in the source subdirectories is pretty much the same as for any other programming language. Here is how it is done in the example: 


```python
#!python
#
# Build dependency tree
#
allobjs = []
for sd in subdirs:
    buildDir = os.path.join('build',sd)
    consFile = os.path.join(buildDir,'SConscript')
    env.BuildDir(buildDir, sd)
    allobjs = allobjs + env.SConscript( consFile, exports = ['env','Glob'])
```
There is one important discrepency between Fortran 90 and other languages: the SConscript file typically returns a list of not only object files, but also module files. If you blindly pass this list to a Program method, as you would for a C program, for example, you will get a link error because the linker does not know what to do with the module files. To avoid this, you need to 'weed out' the module files before passing the list to the Program method, like so: 


```python
#!python
#
# Remove any mod files. These should not be passed to the linker.
#
objs = filter(lambda o: str(o)[-4:] != '.mod', allobjs)

...

#
# Build program
#
env.Program('test.x', ['main.f90'] + objs )
```
As eluded to above, some compilers (eg. MIPS f90 on Irix) don't have a flag to stipulate the directory that module files should be moved to when a source file is compiled. The module files get put in the current working directory, which would be the root directory of your project. The problem is that scons expects module files to be stored in the build directories. If you rerun scons, it will not find the module files, and will rebuild all sources in any way connected to the modules. To avoid this, you really do need to move the module files to the appropriate build directories. 

One way to do this is to add a post action for each object file target returned by the SConscripts: 


```python
#!python
#
# Add an action to move any module files
#
def moveModFiles(target=None, source=None, env=None):
    import glob, os, os.path
    targetdir = target[0].dir
    for t in target:
        if t.name[-4:] == '.mod':
            os.rename(t.name,os.path.join(str(targetdir),t.name))

env.AddPostAction(objs, moveModFiles)
```
The moveModFiles function simply looks for any module files passed in target, which is a list of the object and module files corresponding to the source file passed, and moves them to the build directory. 

Below is the full SConstruct file for the example. Note that this variant does not use the -fmod flag of g95, but uses a post action to move module files to the build directory. This is purely for demonstration purposes; if you were really using g95, you would be better to use the -fmod flag. 


```python
#!python
#!/usr/bin/env python
import os, os.path, sys, fnmatch

#
# Functions
#
def Glob(match):
    """Similar to glob.glob, except globs SCons nodes, and thus sees
    generated files and files from build directories.  Basically, it sees
    anything SCons knows about.  A key subtlety is that since this function
    operates on generated nodes as well as source nodes on the filesystem,
    it needs to be called after builders that generate files you want to
    include."""
    def fn_filter(node):
        fn = str(node)
        return fnmatch.fnmatch(os.path.basename(fn), match)

    here = Dir('.')

    children = here.all_children()
    nodes = map(File, filter(fn_filter, children))
    node_srcs = [n.srcnode() for n in nodes]

    src = here.srcnode()
    if src is not here:
        src_children = map(File, filter(fn_filter, src.all_children()))
        for s in src_children:
            if s not in node_srcs:
                nodes.append(File(os.path.basename(str(s))))

    return nodes

#
# Paths
#
subdirs = ['subdir1', 'subdir2']
modpath = map(lambda d: os.path.join('#/build',d), subdirs)

#
# Environment
#
env = Environment(
    F90PATH = modpath,
    FORTRAN='g95',
    LINK = 'g95')

#
# Build dependency tree
#
allobjs = []
for sd in subdirs:
    buildDir = os.path.join('build',sd)
    consFile = os.path.join(buildDir,'SConscript')
    env.BuildDir(buildDir, sd)
    allobjs = allobjs + env.SConscript( consFile, exports = ['env','Glob'])

#
# Remove any mod files. These should not be passed to the linker.
#
objs = filter(lambda o: str(o)[-4:] != '.mod', allobjs)


#
# Add an action to move any module files
#
def moveModFiles(target=None, source=None, env=None):
    import glob, os, os.path
    targetdir = target[0].dir
    for t in target:
        if t.name[-4:] == '.mod':
            os.rename(t.name,os.path.join(str(targetdir),t.name))

env.AddPostAction(objs, moveModFiles)

#
# Build program
#
env.Program('test.x', ['main.f90'] + objs )
```

# The SConscript File

The SConscript file for this example is very simple. Here it is: 


```python
#!python
#!/usr/bin/env python

Import('env','Glob')

sources = Glob('*.f90') + Glob('*.f')
objs = env.Object(sources)

Return('objs')
```
What you'll notice is that it uses a function Glob, which is imported from the SConstruct script. This Glob function is taken from the page [BuildDirGlob](BuildDirGlob); it allows you to do a glob for source files from within the corresponding build directory. In this case it is used to get a list of all files with the extension .f90 or .f. 

A list of Objects are made in the usual way, and returned. Note that these Objects include the module files, in addition to the real object files. 


# Other Problems

Fortran is a case-insensitive language, so the case used in module names is irrelevant. Most compilers create module files with lowercase names, such as somemodule.mod, but others use uppercase (ie SOMEMODULE.mod). At this point, scons assumes module files will be in lowercase. Hopefully options will be added in the future to allow for either, but in the meantime there is a simple workaround if you are stuck with a compiler using uppercase: ensure that both module file variants are created. 

You can do this with a post action that copies the module file created by the compiler, and uses the lowercase naming scheme for the new copy. Here is a variation on the moveModFiles function given earlier that creates the two module file variants: 


```python
#!python
def MoveModFiles(target=None, source=None, env=None):
    """
    Moves mod files to build directory. Also creates upper/lower-case versions.
    This is needed on SGI, for example.
    """
    import os, os.path, shutil
    targetdir = target[0].dir
    for t in target:
        namebase, nameext = os.path.splitext(t.name)
        modfilename = namebase.upper() + nameext
        lowermodfilename = namebase.lower() + nameext
        if modfilename[-4:] == '.mod':
            builddirupperpath = os.path.join(str(targetdir),modfilename)
            builddirlowerpath = os.path.join(str(targetdir),lowermodfilename)
            os.rename(modfilename, builddirupperpath)
            shutil.copy(builddirupperpath, builddirlowerpath)

...

env.AddPostAction(objs, MoveModFiles)
```
As you can see, it is simply a question of duplicating the uppercase file, and using the lowercase naming scheme for the duplicate. Note that you can't just move the uppercase file, because the compiler will expect it to exist. In effect, the uppercase file is for the compiler, and the lowercase file is for scons. 

* -- [DrewMcCormack](DrewMcCormack) 
Options specific to Intel FORTRAN compiler: 

```
#!python
FORTRANMODDIRPREFIX = '-module ', 
```
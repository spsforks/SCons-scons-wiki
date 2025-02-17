
Line 3: Imports the env from the parent script 

Line 5&7: Sets up the C compiler to look in both the current directory and the include directory underneath the main directory in which SCons was started. Note the "#" in the "#include". This is important. That include directory contains a "config.h" file that almost all the C code references and it is not copied over to the build/etc/etc hierarchy. 

Line 9: Gambit Scheme input files (sources) Line 12: Extra input source files.  This is here because these files have extra dependencies. 

Line 16&17: Converts the Gambit Scheme input files into C output files (targets) via the [GambitCompiler](GambitCompiler) Builder defined in the top-level SConstruct. ie. _gsi.scm becomes _gsi.c. Note that I am saving the targets here for later reference. 

Line 23,23,25,26,27: Lots of dependencies.  Make the targets dependent upon libgambc. As the comment says, only the gsc executable is, strictly speaking, dependent upon libgambc. However, the easiest way to pick up the dependencies from lots of the source files to the lib files is to make the targets depend on the whole library. Yes, it's a bit of a hack which forces libgambc to build first. 

Line 29: Gambit requires some extra link information to produce a stand-alone executable. This uses the [GambitLinker](GambitLinker) Builder that was defined in the top-level SConstruct to produce that file. It demonstrates multiple sources compiling into one target. 

Line 31: Invoke the normal SCons Program Builder to produce an executable and remember it 

Line 33: Not used yet, but I send the reference to the executable back up to the SConstruct for later use, if required. 


```python
#!python
# -*-python-*-

Import(["env", "libgambc"])

cpppath = [".", "#include", "#lib"]

env.Replace(CPPPATH=cpppath)

gambitSourceFiles = ["_back.scm", "_env.scm", "_front.scm", "_gvm.scm", "_host.scm",
                     "_parms.scm", "_prims.scm", "_ptree1.scm", "_ptree2.scm", "_source.scm",
                     "_t-c-1.scm", "_t-c-2.scm", "_utils.scm"]
gambitGenericDependentSourceFiles = ["_t-c-3.scm", "_gsc.scm"]


# This "GenericDependent" contortion is because source files can't have dependencies
gambitTargetFiles = env.GambitCompiler(gambitSourceFiles)
gambitGenericDependentTargetFiles = env.GambitCompiler(gambitGenericDependentSourceFiles)


# The target files are not strictly dependent upon the entire
# libgambc but on some of the files generated during its build
env.Depends(gambitTargetFiles, libgambc)
env.Depends(gambitGenericDependentTargetFiles, libgambc)

env.Depends(gambitTargetFiles, ["fixnum.scm", "_envadt.scm", "_gvmadt.scm", "_ptreeadt.scm", "_sourceadt.scm"])
env.Depends(gambitGenericDependentTargetFiles, ["fixnum.scm", "_envadt.scm", "_gvmadt.scm", "_ptreeadt.scm", "_sourceadt.scm"])
env.Depends(gambitGenericDependentTargetFiles, ["generic.scm"])

gscLinkerFile = env.GambitLinker([gambitTargetFiles, gambitGenericDependentTargetFiles])

gsc = env.Program("gsc", [gambitTargetFiles, gambitGenericDependentTargetFiles,
                          gscLinkerFile, libgambc])
Return("gsc")
```
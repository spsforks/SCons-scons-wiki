
Line 3: Imports the env from the parent script 

Line 5&7: Sets up the C compiler to look in both the current directory and the include directory underneath the main directory in which SCons was started. Note the "#" in the "#include". This is important. That include directory contains a "config.h" file that almost all the C code references and it is not copied over to the build/etc/etc hierarchy. 

Line 9: Gambit Scheme input files (sources) 

Line 11: Converts the Gambit Scheme input files into C output files (targets) via the [GambitCompiler](GambitCompiler) Builder defined in the top-level SConstruct. ie. _gsi.scm becomes _gsi.c. Note that I am saving the targets here for later reference. 

Line 15: Make the targets dependent upon libgambc.  As the comment says, only the gsi executable is, strictly speaking, dependent upon libgambc.  However, the easiest way to pick up the dependencies from _gsi.scm to the lib files is to make the _gsi target depend on the whole library.  Yes, it's a bit of a hack which forces libgambc to build first. 

Line 17: Gambit requires some extra link information to produce a stand-alone executable.  This uses the [GambitLinker](GambitLinker) Builder that was defined in the top-level SConstruct to produce that file.  A better example of this is in the gsc SConscript which demonstrates the multiple sources compiling into one target.  Here I only have one source. 

Line 18: Invoke the normal SCons Program Builder to produce an executable and remember it 

Line 19: Not used yet, but I send the reference to the executable back up to the SConstruct for later use, if required. 


```python
#!python
# -*-python-*-

Import(["env", "libgambc"])

cpppath = [".", "#include"]

env.Replace(CPPPATH=cpppath)

gambitSourceFiles = ["_gsi.scm"]

gambitTargetFiles = env.GambitCompiler(gambitSourceFiles)

# The target files are not strictly dependent upon the entire
# libgambc but on some of the files generated during its build
env.Depends(gambitTargetFiles, libgambc)

gsiLinkerFile = env.GambitLinker([gambitTargetFiles])
gsi = env.Program("gsi", [gambitTargetFiles, gsiLinkerFile, libgambc])
Return("gsi")
```
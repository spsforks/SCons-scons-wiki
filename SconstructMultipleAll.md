
Same as [SconstructMultiple](SconstructMultiple) with an 'all' Alias used. 

Now the command line also allows: 
```txt
scons mode=release all  ; build all subprojects
scons mode=debug all
```
The Sconstruct does not change from [SconstructMultiple](SconstructMultiple). The Sconscript changes slightly (the last 2 lines): 
```python
#!python
import glob

Import('env', 'project', 'mymode', 'debugcflags', 'releasecflags')
localenv = env.Copy()

buildroot = '../' + mymode  #holds the root of the build directory tree
builddir = buildroot + '/' + project   #holds the build directory for this project
targetpath = builddir + '/' + project  #holds the path to the executable in the build directory

#append the user's additional compile flags
#assume debugcflags and releasecflags are defined
if mymode == 'debug':
   localenv.Append(CCFLAGS=debugcflags)
else:
   localenv.Append(CCFLAGS=releasecflags)

#specify the build directory
localenv.BuildDir(builddir, ".", duplicate=0)

srclst = map(lambda x: builddir + '/' + x, glob.glob('*.cpp'))
pgm = localenv.Program(targetpath, source=srclst)
env.Alias('all', pgm)
```
The difference is that the Node from Program() is saved in variable 'pgm' and is used in an Alias(). The Alias() in the three sconscripts name the same alias name (i.e. 'all'). When the alias name is used on the command line, scons builds everything associated with it. 

Note a couple of things: 

* the exact same alias name 'all' is used in all three sconscripts. 
* that 'env' is used for the Alias() not 'localenv' 
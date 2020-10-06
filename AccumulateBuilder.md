## Description of Problem

Many a time it is necessary to create a ZIP file or tarball for distribution of sources, binaries, and documentation.  The ZIP file or tarball also must be properly rooted. 

Unfortunately, SCons does not have a built-in capability to do this easily, but instead exposes an interface which makes this relatively easy. 

One could use standard Python tools (e.g., `shutil.copy`) to copy the necessary files and directories and then the `zipfile` module then using the builders that come with SCons, but not only could you create something that isn't properly rooted but you also lose SCon's dependency tracking, cleaning, etc. 

See also [DistTarBuilder](DistTarBuilder) for another solution to this problem (with ability to handle file extension lists and excluded directory lists, but without the dependency tracking stuff) 


## Solution

The solution is two-step: 

* "Collect" files and directories to a destination. 
* Use one of SCon's built-in builders to tar/zip (e.g., `env.Tar`, `env.Zip`) the destination, or use a new Builder to properly "root" the tar/zip file. 
The builder to collect the files and directories is called "Accumulate", and the code for which is as follows. 


```python
##
## AccumulatorAction.py
##

import myShutil # for better copytree()
import os
import shutil

def accumulatorFunction(target, source, env):
  """Function called when builder is called"""
  destDir = str(target[0])
  if not os.path.exists(destDir):
      os.makedirs(destDir)
  for s in source:
      s = str(s)
      if os.path.isdir(s):
          myShutil.copytree(s, destDir, symlinks = False)
      else:
          shutil.copy2(s, destDir) 
```
The above code requires a better `copytree()` because `shutil.copytree()` is very limiting.  What is needed is the equivalent of `cp -R`, which the following module provides. 


```python
##
## myShutil.py
##

import os.path
import shutil

def copytree(src, dest, symlinks=False):
    """My own copyTree which does not fail if the directory exists.
    
    Recursively copy a directory tree using copy2().

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied.
    
    Behavior is meant to be identical to GNU 'cp -R'.    
    """

    def copyItems(src, dest, symlinks=False):
        """Function that does all the work.
        
        It is necessary to handle the two 'cp' cases:
        - destination does exist
        - destination does not exist
        
        See 'cp -R' documentation for more details
        """
        for item in os.listdir(src):
            srcPath = os.path.join(src, item)
            if os.path.isdir(srcPath):
                srcBasename = os.path.basename(srcPath)
                destDirPath = os.path.join(dest, srcBasename)
                if not os.path.exists(destDirPath):
                    os.makedirs(destDirPath)
                copyItems(srcPath, destDirPath)
            elif os.path.islink(item) and symlinks:
                linkto = os.readlink(item)
                os.symlink(linkto, dest)
            else:
                shutil.copy2(srcPath, dest)

    # case 'cp -R src/ dest/' where dest/ already exists
    if os.path.exists(dest):
        destPath = os.path.join(dest, os.path.basename(src))
        if not os.path.exists(destPath):
            os.makedirs(destPath)
    # case 'cp -R src/ dest/' where dest/ does not exist
    else:
        os.makedirs(dest)
        destPath = dest
    # actually copy the files
    copyItems(src, destPath)
```
Using `env.Zip` is not very useful for creating properly rooted ZIP files, but the following builder is: 


```python
##
## Zipper.py
##
import distutils.archive_util

def zipperFunction(target, source, env):
    """Function to use as an action which creates a ZIP file from the arguments"""
    targetName = str(target[0])
    sourceDir = str(source[0])
    distutils.archive_util.make_archive(targetName, "zip", sourceDir)
```
To actually create the builders, use the following example: 


```python
##
## SConstruct
##
env = Environment()

# add builder to accumulate files
accuBuilder = env.Builder(
    action=AccumulatorAction.accumulatorFunction,
    source_factory=SCons.Node.FS.default_fs.Entry,
    target_factory=SCons.Node.FS.default_fs.Entry,
    multi=1,
)
env["BUILDERS"]["Accumulate"] = accuBuilder

# add builder to zip files
zipBuilder = env.Builder(
    action=Zipper.zipperFunction,
    source_factory=SCons.Node.FS.default_fs.Entry,
    target_factory=SCons.Node.FS.default_fs.Entry,
    multi=0,
)
env["BUILDERS"]["Zipper"] = zipBuilder
```
And you are done!  Quite the hassle, but I think the result is worthwhile (IMHO).  See the following code example for yourself: 


```python
##
## SConstruct
##
env.Accumulate("distDir/src", "main.cpp")
env.Accumulate("distDir/images", "something.png")

Export("env")
SConscript("inner/SConscript")

env.Zipper("package", "distDir")
```

```python
##
## inner/SConscript
##
Import('env')

env.Accumulate('#/distDir', 'include')
```
Scons output will be as follows: 


```console
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
accumulatorFunction(["distDir/images"], ["something.png"])
accumulatorFunction(["distDir/src"], ["main.cpp"])
accumulatorFunction(["distDir"], ["inner/include"])
zipperFunction(["package"], ["distDir"])
scons: done building targets.
```
And your ZIP file will be properly rooted: 


```txt
Archive:  package.zip
  Length     Date   Time    Name
 --------    ----   ----    ----
       59  05-09-05 08:15   src/main.cpp
        7  05-09-05 08:15   images/something.png
        0  05-09-05 08:15   include/app/app.h
        0  05-09-05 08:15   include/app/db/db.h
        0  05-09-05 08:15   include/more/sun.h
        0  05-09-05 08:15   include/more/build/moon.h
        0  05-09-05 08:15   include/tool/something.h
 --------                   -------
       66                   7 files
```

## TODO

All this can be improved by: 

* adding some kind of "filter" option (e.g., only Accumulate '.h' files). 
* fixing cleaning because 'scons -c' does actually clean the destination directory. 
* removing unnecessary rebuilds because running 'scons' again will recopy/re-zip everything. 

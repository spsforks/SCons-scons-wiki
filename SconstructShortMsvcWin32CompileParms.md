


---

 If you want to add additional compile flags, try this: 
```txt
import glob

#assumes project name is the build directory name is the executable name...

project = 'myprogram'      #holds project name
buildroot = '../debug'     #holds root of the build directory tree
cflags = ['-W1', '-GX']    #some additional compile flags

#-------
#From here on will be common to all projects

builddir = buildroot + '/' + project   #holds build directory name
targetpath = builddir + '/' + project  #holds path to executable in the build directory

env = Environment()

#if cflags is defined, don't anything, otherwise append 
#the user's compile flags to the current compile flags
try: cflags
except NameError: pass
else: env.Append(CCFLAGS=cflags)

#set up the build directory
BuildDir('#' + builddir, "#.", duplicate=0)

env.Program(targetpath, source=map(lambda x: '#' + builddir + '/' + x, glob.glob('*.cpp')))
```
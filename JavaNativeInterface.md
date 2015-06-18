
# Building Java Native Interfaces

Although _SCons_ supports the creation of Java Native Interface (JNI) header files _via_ JavaH(), building and linking _C_ or _C++_ JNI libraries is another matter. _SCons_ does not report _where_ the JNI include files or libraries are stored. We need that information to point to the header files and/or libraries needed by JNI.  The following example shows how to build JNI libraries on multiple platforms using Sun's Java Development Kit (JDK). 

The python code `ConfigureJNI.py` below first searches for a shell environment variable `JAVA_HOME`. If `JAVA_HOME` is not found, it then searches for the java compiler and uses this information to set `JAVA_HOME`. From the java home directory, the build environment's `CPPPATH` and `LIBPATH` are set appropriately. Additional `CCFLAGS`, `SHLINKFLAGS`, and `SHLIBSUFFIX` variables are updated in the build environment to allow cygwin or OS X (darwin) to properly build and link a shared library  suitable for JNI. 


##### file: ConfigureJNI.py


```
#!python 
import os
import sys

def walkDirs(path):
    """helper function to get a list of all subdirectories"""
    def addDirs(pathlist, dirname, names):
        """internal function to pass to os.path.walk"""
        for n in names:
            f = os.path.join(dirname, n)
            if os.path.isdir(f):
                pathlist.append(f)
    pathlist = [path]
    os.path.walk(path, addDirs, pathlist)
    return pathlist

def ConfigureJNI(env):
    """Configure the given environment for compiling Java Native Interface
       c or c++ language files."""

    if not env.get('JAVAC'):
        print "The Java compiler must be installed and in the current path."
        return 0

    # first look for a shell variable called JAVA_HOME
    java_base = os.environ.get('JAVA_HOME')
    if not java_base:
        if sys.platform == 'darwin':
            # Apple's OS X has its own special java base directory
            java_base = '/System/Library/Frameworks/JavaVM.framework'
        else:
            # Search for the java compiler
            print "JAVA_HOME environment variable is not set. Searching for java... ",
            jcdir = os.path.dirname(env.WhereIs('javac'))
            if not jcdir:
                print "not found."
                return 0
            # assuming the compiler found is in some directory like
            # /usr/jdkX.X/bin/javac, java's home directory is /usr/jdkX.X
            java_base = os.path.join(jcdir, "..")
            print "found."

    if sys.platform == 'cygwin':
        # Cygwin and Sun Java have different ideas of how path names
        # are defined. Use cygpath to convert the windows path to
        # a cygwin path. i.e. C:\jdkX.X to /cygdrive/c/jdkX.X
        java_base = os.popen("cygpath -up '"+java_base+"'").read().replace( \
                 '\n', '')

    if sys.platform == 'darwin':
        # Apple does not use Sun's naming convention
        java_headers = [os.path.join(java_base, 'Headers')]
        java_libs = [os.path.join(java_base, 'Libraries')]
    else:
        # windows and linux
        java_headers = [os.path.join(java_base, 'include')]
        java_libs = [os.path.join(java_base, 'lib')]
        # Sun's windows and linux JDKs keep system-specific header
        # files in a sub-directory of include
        if java_base == '/usr' or java_base == '/usr/local':
            # too many possible subdirectories. Just use defaults
            java_headers.append(os.path.join(java_headers[0], 'win32'))
            java_headers.append(os.path.join(java_headers[0], 'linux'))
            java_headers.append(os.path.join(java_headers[0], 'solaris'))
        else:
            # add all subdirs of 'include'. The system specific headers
            # should be in there somewhere
            java_headers = walkDirs(java_headers[0])

    # add Java's include and lib directory to the environment
    env.Append(CPPPATH = java_headers)
    env.Append(LIBPATH = java_libs)

    # add any special platform-specific compilation or linking flags
    if sys.platform == 'darwin':
        env.Append(SHLINKFLAGS = '-dynamiclib -framework JavaVM')
        env['SHLIBSUFFIX'] = '.jnilib'
    elif sys.platform == 'cygwin':
        env.Append(CCFLAGS = '-mno-cygwin')
        env.Append(SHLINKFLAGS = '-mno-cygwin -Wl,--kill-at')

    # Add extra potentially useful environment variables
    env['JAVA_HOME'] = java_base
    env['JNI_CPPPATH'] = java_headers
    env['JNI_LIBPATH'] = java_libs
    return 1
```

## Example

The following example illustrates a very simple java native interface function. The java class `jsrc/HelloWorld.java` below attempts to load a shared library named `HelloWorldImp` (`HelloWorldImp.dll` on windows or cygwin, `libHelloWorldImp.jnilib` on OS X, `libHelloWorldImp.so` on linux). The java `main` function calls a native function named `displayHelloWorld()`. 

The code for `displayHelloWorld()` is included in the file `csrc/HelloWorldImp.cpp` below. `displayHelloWorld()` prints the all too familiar message on stdout. 


##### file: jsrc/HelloWorld.java


```txt
class HelloWorld {
    public native void displayHelloWorld();

    static {
        System.loadLibrary("HelloWorldImp");
    }

    public static void main(String[] args) {
        new HelloWorld().displayHelloWorld();
    }
}
```

##### file: csrc/HelloWorldImp.cpp


```txt
#include <stdio.h>
#include <jni.h>
#include "HelloWorld.h"

JNIEXPORT void JNICALL
Java_HelloWorld_displayHelloWorld(JNIEnv *env, jobject obj)
{
    printf("Hello world!\n");
    return;
}
```
The _S``Cons_ build files below are used to build this simple example. Since java classes are platform independent, they are compiled into the subdirectory "classes". 

C++ classes are platform _dependent_ so they are compiled and linked into the subdirectory "lib-_platform_" such as "lib-win32", "lib-cygwin", "lib-linux", "lib-darwin", etc. 

`SConstruct` sets up the build environment and `SConscript` build the java and native code. 


##### file: SConstruct


```python
#!python 
import os
import sys
from ConfigureJNI import ConfigureJNI

if sys.platform == 'win32':
    # MS Visual C++ is found from the registery, not the PATH
    env = Environment()
else:
    # we need the path to find java
    env = Environment(ENV = {'PATH' : os.environ['PATH']})

if not ConfigureJNI(env):
    print "Java Native Interface is required... Exiting"
    Exit(0)

SConscript('SConscript', exports = 'env')
```

##### file: SConscript


```python
#!python 
import os
import sys
Import('env')

def PrependDir(dir, filelist):
    return [os.path.join(dir,x) for x in filelist]

# compile java classes into platform independent 'classes' directory
jni_classes = env.Java('classes', 'jsrc')
jni_headers = env.JavaH('csrc', jni_classes)

# compile native classes into platform dependent 'lib-XXX' directory
# NOTE: javah dependencies do not appear to work if SConscript was called
# with a build_dir argument, so we take care of the build_dir here
native_dir = 'lib-' + sys.platform
native_src = PrependDir(native_dir, env.Split("""HelloWorldImp.cpp"""))
env.BuildDir(native_dir, 'csrc', duplicate=0)
env.SharedLibrary(native_dir+'/HelloWorldImp', native_src)
```

### Building

Create a directory and place the five files listed here in the following directory structure: 
```txt
ConfigureJNI.py
SConstruct
SConscript
jsrc/HelloWorld.java
csrc/HelloWorldImp.cpp
```
Then run _scons_: 


```txt
C:\Devel\jni> scons
```

### Testing

When testing this example, remember that Java must be able to find the shared library. 

**On windows**, the library must be in the current directory or somewhere in the `PATH`. To test this example on windows, build it with scons, change to the directory containing the DLL and run the java class 
```txt
C:\Devel\jni> cd lib-win32

C:\Devel\jni\lib-win32> java -cp ..\classes HelloWorld
Hello World!
```
**On linux**, Java searches `LD_LIBRARY_PATH` for shared libraries. However, the `LD_LIBRARY_PATH` rarely contains the current directory, so it must be added. To test this example on linux, first update `LD_LIBRARY_PATH`, then change to the directory containing the shared library and run the java class. 
```txt
[user@localhost ~/jni]$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.

[user@localhost ~/jni]$ cd lib-linux

[user@localhost ~/jni/lib-linux]$ java -cp ../classes HelloWorld
Hello World!
```
**On OS X**, Java searches the current directory or `/Library/Java/Extension` for shared libraries. Note that shared JNI libraries on OS X need to have the extension `.jnilib`. This is taken care of by `ConfigureJNI()` above. 
```txt
[user@localhost ~/jni]% cd lib-darwin

[user@localhost ~/jni/lib-darwin]% java -cp ../classes HelloWorld
Hello World!
```

## Remarks

The goal of this example is to encourage cross-platform building of Java Native Interface files. Ideally, most or all of the platform-dependent setup should be taken care of in `ConfigureJNI.py`, rather than in `SConstruct` or `SConscript`. 

I have tested the above example on windows, cygwin, linux, and OS X 10.2. 

   * -- Jeff Kuhn <[jeffrey.kuhn@yale.edu](mailto:jeffrey.kuhn@yale.edu)> 
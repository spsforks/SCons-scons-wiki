

# Description

Using a combination of RPATH and $ORIGIN features on modern linkers, you can specify relative paths to directories in which to search for libraries.  This is very useful for projects which distribute their own libraries, such as Firefox and KDE.  It keeps /etc/ld.so.conf clean and makes the software relocatable anywhere. 

This page specifically discusses: 

* common practices in Windows and Linux vis a vi shared libraries. 
* using RPATH and $ORIGIN effectively using SCons. 

# Shared libraries in Windows and Linux

In the Windows world, it is common practice to include the necessary DLLs in the same directory as the program because the DLL loader will search in the executable's path.  The directory structure of the software thus ends up looking like this: 


```txt
Program\
Program\program.exe
Program\program.dll
```
In the Linux world, the dynamic loader does not search in the executable's directory, so the common practice is to install libraries into one of the system paths specified in /etc/ld.so.conf.  Thusly, the directory structure commonly looks as such: 


```txt
/usr/bin/program
/usr/lib/libprogram.so
```
Standard locations for libraries allow the linkers to easily find shared libraries available on your system. 


# The Problem

The problem that commonly arises in the Linux world is that of a large number of locations for libraries.  The SuSE Linux 9.2 Professional /etc/ld.so.conf lists fifteen (15) directories: 


```txt
/usr/X11R6/lib/Xaw95
/usr/X11R6/lib/Xaw3d
/usr/X11R6/lib
/usr/i486-linux/lib
/usr/i486-linux-libc5/lib=libc5
/usr/i486-linux-libc6/lib=libc6
/usr/i486-linuxaout/lib
/usr/i386-suse-linux/lib
/usr/local/lib
/usr/openwin/lib
/opt/kde/lib
/opt/kde2/lib
/opt/kde3/lib
/opt/gnome/lib
/opt/gnome2/lib
```
KDE will be taken as an example.  In SuSE Linux Professional 9.2, the KDE binaries go into /opt/kde3/bin, while the libraries go into /opt/kde3/lib. 

In order for the binaries in /opt/kde3/bin to correctly load, /opt/kde3/lib was added to the dynamic loader's runtime search paths via /etc/ld.so.conf. 

But here lies the problem: will every 3rd party vendor who releases a Linux application which has its own shared libraries create a new directory and add it to /etc/ld.so.conf?  What about un-installation?  There is a better way. 


# Using RPATH

The RPATH is described as scons as the following: 



---

 A list of paths to search for shared libraries when running programs. Currently only used in the GNU linker (gnulink) and IRIX linker (sgilink). Ignored on platforms and toolchains that don't support it. Note that the paths added to RPATH are not transformed by scons in any way: if you want an absolute path, you must make it absolute yourself. 

---

 

**NOTE:** The Sun linker also supports such functionality, but only SCons versions >= 0.97 support it.   

Please note that this is the _runtime_ search path, not the link time.  (The GNU linker uses the '-L' option for compile-time search paths, and '--rpath' for runtime search paths.) 


# The Solution

The solution is to use a little-known feature available in the Sun, GNU, and Irix linkers. 

The $ORIGIN symbol is resolved--at runtime--to the location of the binary, and, as stated before, the RPATH specifies runtime search locations for libraries.  These two parts together create the best solution. 

With a directory structure as follows... 
```txt
/opt/newApp/bin/app
/opt/newApp/lib/libapp.so
```
...it is best to specify a relative path for the binary to search for based on its location.  It would be nice if you could tell the 'app' binary to search '../lib/', would it not?  You can! 


```python
#!python
import os
env = Environment()
env.Append( LINKFLAGS = Split('-z origin') )
env.Append( RPATH = env.Literal(os.path.join('\\$$ORIGIN', os.pardir, 'lib')))
```
If you also add the following line: 


```python
#!python
env.Program('main', 'main.cpp')
```
...scons will output the following on a Linux/gcc system: 


```txt
g++ -c -o main.o main.cpp
g++ -Wl,--rpath=\$ORIGIN/../lib -z origin -o main main.o
```
The Sun toolchain will output the following: 


```txt
CC -c -o main.o main.cpp
CC -R\$ORIGIN/../lib -z origin -o main main.o
```
The allows you to put the program's directory tree anywhere--e.g., /opt, /usr/local--and it will still work without ever touching /etc/ld.so.conf! 

This is the proper and best solution for projects such as KDE, Mozilla, and Firefox that have their own libraries. 


# More information

See the appropriate documentation for your toolchain.  Linux users can view the man pages for gcc and ld. 

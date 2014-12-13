

# SCons's Interaction With Cygwin

There are two versions of SCons that work on Windows: the native version of SCons and the Cygwin version of SCons. (Maybe there's an MSys version too? Maybe even Interix? Let's ignore those possibilities. The principles in this document could presumably be expanded in much the same way to include those as well.) Actually the terms "native SCons" and "Cygwin SCons" are a simplification because it's the "Cygwin-ness" of Python that really matters, but we'll come back to that. 

The issues that arise with running SCons on Windows, and the interaction with Cygwin, fall into two main categories: 

1. How do I runs SCons (and what version is being run)? 
1. How does SCons start processes? 
These two points are addressed below. However, there are some guiding principles: 

* None of this matters if you use only native stuff with native SCons (e.g. you're a Windows-only dev.), or you use only Cygwin stuff with Cygwin SCons (e.g. you're a Unix dev. who thinks it'd be cool to have a Windows build, but want to pretend that Windows is Unix so you don't have to do anything instead of porting to MSVC) 
* I suspect the main problem people face is starting native Python from a Cygwin shell, but starting Cygwin SCons from a native shell (cmd.exe or [PowerShell](PowerShell)) will not work out of the box either 
* SCons's behavior differs between native and Cygwin SCons, and this behavior changes based on the version of SCons (really: the version of Python) and not the shell it is run from; e.g. running native SCons from a Cygwin shell won't magically make it act like Cygwin SCons 
Let's start off with the basics: 


# What version of SCons am I installing?

As far as I know, there are three ways to install SCons on Windows: 

1. The Windows installer from scons.org (requires you to have a native Python installation already) 
1. From the Cygwin package manager (will probably automatically install Cygwin Python as a prerequisite if you don't have it) 
1. From source, by running python setup.py install in the source distribution from scons.org (requires a version of Python installed already) 
The first two options give you the version you expect. The third option will give you the version that is associated with the Python installation being run. If python gives you Cygwin Python, then #3 will give you Cygwin SCons; if python gives you native Python, then #3 will give you native SCons. 

(Of course, you could also run something like `c:\weird-path\python27\python setup.py install` in which case substitute `c:\weird-path\python27\python` in this discussion.) 

If you don't know whether `python setup.py install` will give you native or Cygwin Python, you can do one of a few things. First, you can use `which python`/`where python`/`whence python` as appropriate and look at whether it tells you something in the Cygwin directory or not. More foolproof is to run python, then `import platform`, then look at `platform.system()`. Cygwin Python will show you a name that includes "Cygwin", and native Python will give you "Windows". Here is what I see on my system: 

Native Python: 
```txt
Python 2.7.3 (default, Apr 10 2012, 23:24:47) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import platform
>>> platform.system()
'Windows'
```
Cygwin Python: 
```txt
Python 2.7.3 (default, Dec 18 2012, 13:50:09) [GCC 4.5.3] on cygwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import platform
>>> platform.system()
'CYGWIN_NT-6.2-WOW64'
```

# What version of SCons am I running?

You could use `where`/`which`/`whence scons` (as appropriate), but more foolproof is probably to make an `SConstruct` file containing just 
```txt
import platform
print(platform.system())
```
and run `scons` and see what it says. As above, it will either tell you Windows if you're running native SCons or something that has "cygwin" in it if you're running Cygwin SCons (like the above). 


# How can I run native SCons from a Cygwin shell, or vice versa?

By default, neither of the things in the question will work if you just run `scons` in the "wrong" shell. If you try to run native SCons from a Cygwin shell, you'll get a `bash: scons: command not found` error (or something similar). If you try to run Cygwin SCons from a native shell, you'll get the Windows equivalent `'scons' is not recognized as an internal or external command, operable program or batch file.` 

The reason this happens is as follows. For native SCons, the command `scons` itself is actually a batch script (which then starts Python), and Cygwin shells don't look at `.bat` files when looking for executables. For Cygwin SCons, the command `scons` is the Python script that the native `scons.bat` starts, but the native interpreter doesn't recognize it as executable because it doesn't have an executable extension. 

To run native SCons from a Cygwin shell, there are two options: 

1. Run `scons.bat` instead of just `scons`. If you just want to do this occasionally, this works out of the box. 
1. Make a wrapper script called `scons` containing 
         * ```txt
#!/usr/bin/bash
exec scons.bat "$@"
    
```
and put it in your `$PATH` somewhere. 

To run Cygwin SCons from a native shell, create a file called `scons.cmd` (or `scons.bat`) in your `%PATH%`, containing the following: 
```txt
@bash -c "%*"
```
```Note:``` this script (`scons.cmd`/`scons.bat`) may not properly handle arguments that need quoting. Not sure what the deal would be with that. Also, this assumes that the Cygwin tools are in your `%PATH%`, otherwise you'll have to provide the full path to bash. 


# What really determines what version of SCons is run?

I don't think I've ever seen anything in this section matter in practice, so keep that in mind. But for completeness and in case anything really weird ever happens to someone, it's actually the version of Python that the `scons` script invokes that determines how it behaves. 

For instance, suppose I have the following `SConstruct`, which outputs the platform as described above along with the value of `env['CC']` for an environment, which will be MSVC for native SCons and GCC for Cygwin SCons (see below.) 
```txt
import platform
print platform.system()
env = Environment()
print env['CC']
```
If I run native SCons normally, it confirms it's native and is behaving like native SCons: 
```txt
I:\scons-test>scons -Q
Windows
cl
```
Behind the scenes, that's actually running the Python program `scons.py` with the version of Python it was installed with. We can also do that directly, and see the same thing: 
```txt
I:\scons-test>c:\Python27\python.exe c:\python27\Scripts\scons.py  -Q
Windows
cl
```
But if I start the _same_ installation of SCons (in `c:\python27`) with Cygwin Python, it changes its behavior: 
```txt
I:\ scons-test>c:\ cygwin\bin\python2.7.exe  c:\python27\Scripts\scons.py  -Q
CYGWIN_NT-6.2-WOW64
gcc
```
and now it's acting like Cygwin SCons. The Python interpreter determines SCons's behavior. 

Similarly, I can run the version of SCons installed by Cygwin with native Python and get the native behavior: 
```txt
$ /cygdrive/c/Python27/python 'c:\cygwin\bin\scons' -Q
Windows
cl
```

# How does SCons change behavior between native and Cygwin?

There are three(?) ways in which SCons's behavior changes: 

1. The set of tools that are loaded by default 
1. The paths SCons recognizes 
1. How SCons launches processes via the shell 
The next sections discuss each of these more. 


## How does the "Cygwin-ness" of SCons impact what tools are used?

The main behavior difference is in defaults only. By default, native SCons builds C and C++ programs using MSVC, while Cygwin SCons builds C and C++ programs using GCC. (Perhaps other tools are different too?) 

Because much of the toolchain is abstracted by SCons, you may not notice a difference here, and something that works under native SCons may work under Cygwin SCons or vice versa. For example, the flags that control the name of the output file as well as the extension of output files (e.g. `.so` versus `.dll`) are abstracted. However, if you explicitly set `CFLAGS`/`CXXFLAGS`/`CCFLAGS`/`LINKFLAGS`/etc. yourself (e.g. to add optimization flags or debugging information), you have to make sure you do the correct thing for each of the compiler choices. 

[insert example of explicitly loading the opposite set of tools from the SCons version (in both directions)] 


## How does the "Cygwin-ness" of SCons impact how it recognizes paths?

Because Cygwin Python goes through the Cygwin abstraction layer, it recognizes Cygwin-style paths. For instance, you can set `env['CC'] = '/usr/bin/g++-4.4'` or something if you have a specific version of GCC you want to use, and that will be a valid path. 

Under native SCons, that is not true, and `/usr/bin/g++-4.4` will nearly-certainly give an error about not being able to find that path. (I guess it might work if `usr/` was in the root of the current drive.) You can still tell native SCons to run Cygwin executables, you just have to use the Windows path, e.g. `'c:/cygwin/bin/g++-4.4'`. 

In reverse however, it suspect will work (untested currently): Cygwin SCons will cope OK with being given Windows paths. 


## How does the "Cygwin-ness" of SCons impact how SCons launches processes?

One potential hangup comes from the fact that native SCons launches programs via the native shell (`cmd.exe`) and Cygwin SCons launches programs via Bash. Because the syntax of the shells differ, you may not be able to use every shell feature you want if it will be run from the other shell. 

For example, someone wrote the SCons mailing list asking why a Command builder call was failing when the command to be executed contained a semicolon. The reason it was failing was because the native shell does not recognize semicolons as separators, and just passes them as part of the command line to the program being started. 

There are two things that have to change in order to change the shell that is used: 

1. `env['SHELL']` controls what shell is run (so on Linux you could set it to `/usr/bin/zsh` or something if you wanted). It is just a string that points to the location of the shell. 
1. `env['SPAWN']` is a function that controls how the shell is invoked. A call to GCC in Cygwin SCons would be invoked somewhat like `sh -c "gcc ..."` while a call to MSVC in native SCons would be invoked somewhat like `cmd /C "cl ..."`. (I'm showing those commands after the expansion of `env['SHELL']`.) Merely changing `env['SHELL']` will not fix the improper use of `-c` or `/C` to specify that it should run a command. 
To use a Cygwin shell (this was actually tested for Msys, but the same should be true for Cygwin) from native SCons, you'll need to do something like the following: 
```txt
from SCons.Platform.win32 import exec_spawn
env["SHELL"]="C:/cygwin/bin/sh.exe"
env["SPAWN"] = (lambda sh, esc, cmd, args, env_param:
                exec_spawn([sh, '-c', ' '.join(args)], env_param))
```
[add example the other way?] 

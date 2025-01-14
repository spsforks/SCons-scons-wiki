
Some software libraries built with MinGW on Windows can be easily built though MSys.  MSys provides a small shell environment making it possible to execute the configure scripts and then build the libraries using the produced makefiles.  Most of these libraries install pkg-config files, which works just fine as is with SCons and the pkg-config.exe program, but some libraries use custom shell scripts which need to be executed under the MSys shell.  Once executed, the results can be parsed with [ParseConfig](ParseConfig). 

One way to get such scripts to be used with SCons is to have SCons somehow detect if it is an executable (pkgconfig.exe) or a shell script, and if it is a shell script then execute it directly with 'sh.exe'  This would also require a way to tell SCons where sh.exe is.  The disadvantage is it requires substantial changes to the SCons configuration files. 

I've made a small batch script which makes it where the following will work on Linux based systems as well as Windows MinGW, with little or not changes to the SCons configuration files. 


```txt
env.ParseConfig('wx-config --cxxflags --libs')
```
On Unix-like environments, wx-config can be executed just fine.  One Windows, however, wx-config is a shell script that needs to be executed with the MSys shell.  In order for the above to work, a simple batch script is made with the same name as the desired shell script, with a .cmd extension. 


```txt
@c:\tools\msys\bin\sh.exe -c "result=`. \"%~d0%~p0%~n0\" %*`;retval=$?;if test \"x$result\" != \"x\"; then cmd //c echo $result; fi;exit $retval"
```
If you need to use c:\libs\wx\wx-config, then just create a file called c:\libs\wx\wx-config.cmd and put that line in the file.  Here is how it works: 

1. cmd.exe replaces %~d0%~p0%~n0, which translates c:\path\wx-config.cmd to c:\path\wx-config 
1. cmd.exe executes sh.exe passing the specified string. 
1. sh.exe executes it (c:\path\wx-config), and stores the output in result. 
1. It stores the return value in retval. 
1. If the script did produce something, it echoes it out, else it does not echo so it doesn't produce 'ECHO is on'.  Using cmd.exe causes sh.exe to convert the arguments from any MSys-style paths to windows style-paths, /c/msys/local/lib to c:/msys/local/lib, that can be used by the mingw compiler. 
1. It then exits with the retval return value and cmd.exe exits with the same return value. 
This can be used for any shell script, just name the file the same as the shell script being executed.  It also can be directly invoked from the command line outside of SCons.  The advantage of this script is no changes are needed to most SCons configuration files.  As long as 'wx-config.cmd' is in the PATH when attempting to execute [ParseConfig](ParseConfig)('wx-config --cxxflags --libs'), it will execute the .cmd file 

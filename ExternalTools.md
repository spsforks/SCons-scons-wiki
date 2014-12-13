
There are lots of tools you might want to have SCons launch instead of an editor. These frequently require certain types of environment variable inheritance, and SCons, by default does none of that. For example, let's say you want to use the most excellent tool ccache ([http://ccache.samba.org/](http://ccache.samba.org/) with your SConscript. You already know that you have to replace the tool with another, so you setup an environment like: 

`env = Environment( CXX = 'ccache g++' )` 

and invoke SCons, and see: 


```txt
% scons
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
ccache g++ -c -o foo.o foo.cxx
ccache: failed to create (null)/.ccache (No such file or directory)
scons: *** [foo.o] Error 1
scons: building terminated because of errors.
```
Drat! So what's going on? Well, turns out that ccache relies on putting temp files in your HOME directory. Arguably, this is a bug with the way ccache handles the getenv() system call, but that's another story. The scoop is that, alas, the environment is not inherited by SCons. So, how does one get the environment into SCons? Very simply: 


```txt
import os
env = Environment(ENV = os.environ)
```
ah, much better: 


```txt
% scons
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
ccache g++ -c -o foo.o foo.cxx
ccache g++ -o foo foo.o
scons: done building targets.
```
/!\ A better way of updating the ENV settings of the Environment is shown in [ImportingEnvironmentSettings](ImportingEnvironmentSettings). 

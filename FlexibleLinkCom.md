Goal: to have a more flexible `LINKCOM`, so that we can put options in any order. Right now, we are force to have `LINKFLAGS` `LIBPATH` `LIBS`. In particular, if we want to put linkflags between libs, this is not possible right now wo rewrwiting link actions. 

None of below is meant as a prototype: this is just to show the basic concept. 


```python
#!python 
import SCons                                                                              
from SCons.Defaults import _stripixes, _concat                                            
                                                                                          
# This dict of func is just a (really) poor-man replacement for  scons                    
# interpolation. In real life, of course, the scons scheme should be used.                
def interpolate_lib(libs, env):                                                           
    return _stripixes(env['LIBLINKPREFIX'], libs,                                         
                      env['LIBLINKSUFFIX'], env['LIBPREFIXES'],                           
                      env['LIBSUFFIXES'], env)                                            
                                                                                          
def interpolate_libpath(libpaths, env):                                                   
    return _concat(env['LIBDIRPREFIX'], libpaths, env['LIBDIRSUFFIX'], env,               
                      env['RDirs'], None, None)                                           
                                                                                          
_INTERPOLATE = {'LIBS' : interpolate_lib,                                                 
        'LIBPATH': interpolate_libpath,                                                   
        'LINKFLAGS': lambda x, y: x}                                                      
                                                                                          
class Framework:                                                                          
    _keys = {'LIBPATH': None, 'LIBS': None, 'LINKFLAGS': None}                            
    def __init__(self):                                                                   
        self._data = []                                                                   
                                                                                          
    def append(self, key, value):                                                         
        # XXX: handling non valid construction variables ?                                
        assert key in self._keys                                                          
                                                                                          
        # XXX: of course, this should be handled correctly too                            
        assert SCons.Util.is_List(value)                                                  
                                                                                          
        self._data.append((key, value))                                                   
                                                                                          
    def subst(self, env):                                                                 
        intp = []                                                                         
        # XXX: I should see how scons interpolation works                                 
        for item in self._data:                                                           
            key = item[0]                                                                 
            val = item[1]                                                                 
            intp.extend(_INTERPOLATE[key](val, env))                                      
                                                                                          
        return ' '.join(intp)                                                             
                                                                                          
class Bstatic:                                                                            
    def __init__(self, lib):                                                              
        f = Framework()                                                                   
                                                                                          
        # XXX: This is tool specific (e.g. gnu ld here)                                   
        # Maybe this could be handled at the tool level, be defining pre/post             
        # flag ? But does this catpure all way of doing it (MS platforms ?) ?             
        f.append('LINKFLAGS', ['-Wl,-Bstatic'])                                           
        f.append('LIBS', lib)                                                             
        f.append('LINKFLAGS', ['-Wl,-Bshared'])                                           
                                                                                          
        self._f = f                                                                       
                                                                                          
    def subst(self, env):                                                                 
        return self._f.subst(env)                                                         
~                                             
```
Which would be used in : 


```python
#!python 
from framework import interpolate_lib, interpolate_libpath, Framework, Bstatic

env = Environment()

# Simple example with libpath + lib (not useful here, but anyway)
f1 = Framework()

f1.append('LIBPATH', ['/opt/bar'])
f1.append('LIBS', ['bar'])

print f1.subst(env)

# Simple example to wrap a lib to link statically
f2 = Bstatic(["foo"])

print f2.subst(env)

# Simple example to add two libraries: this way, of foo in present in /opt/bar
# and /opt/foo, foo in /opt/foo will be picked up first
f3 = Framework()
f3.append('LIBPATH', ['/opt/foo'])
f3.append('LIBS', ['foo'])
f3.append('LIBPATH', ['/opt/bar'])
f3.append('LIBS', ['bar'])

print f3.subst(env)

# More complicated example
f4 = Framework()
f4.append('LIBPATH', ['/opt/foo'])
f4.append('LINKFLAGS', ['-Wl,--rpath-link=/opt/foo'])
f4.append('LIBS', ['foo'])
f4.append('LIBPATH', ['/opt/bar'])
f4.append('LINKFLAGS', ['-Wl,--rpath-link=/opt/bar'])
f4.append('LIBS', ['bar'])
f4.append('LINKFLAGS', ['-xlic_lib=foobar'])

print f4.subst(env)
```
Which would print: 


```txt
-L/opt/bar -lbar
-Wl,-Bstatic -lfoo -Wl,-Bshared
-L/opt/foo -lfoo -L/opt/bar -lbar
-L/opt/foo -Wl,--rpath-link=/opt/foo -lfoo -L/opt/bar -Wl,--rpath-link=/opt/bar -lbar -xlic_lib=foobar
```
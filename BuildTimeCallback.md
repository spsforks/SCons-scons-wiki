
This is a more generalized form of the technique described on the [DynamicSourceGenerator](DynamicSourceGenerator) page from where I got the idea.  I too had source being generated which is why I read that page, but I also used the same idea for other reasons. 

For example: In my case have many (>3000) source files in ~100 libraries and even more headers.  Users are used to just dropping a new file into a folder and having it built into the library - so we have to glob the folders to find all the .cpp files.   This glob can take a long time, and if I've only changed 1 .cpp file in 1 library then I only want to rebuild and link that one library - I don't really want scons to have glob all the files and check them all.  Couple this with the fact that we do have generated source that we need to add in as well.. so even if we did the glob at "reading sconscript" time we have to wait to get the full list later on. 

End result is I need to call scons at build time to do stuff.  Scons has something called [ActionFactory](ActionFactory).  These are objects that create Actions that call a function but can also remember the parameters to call them with.  Things like Mkdir use this.  Here I create my own [ActionFactory](ActionFactory) which can then be used to create an Action that can be passed to a builder. 

This is a heavily cutdown version of what I have to demonstrate this point. 

My Sconscript files set up a list of libraries each of which has a directory of source (actually it can be more than one, but I've simplified): 


```python
class MyLib:

    allLibs = {}
    
    def __init__(self, name, folder):
        MyLib.allLibs[name] = self
        self.name = name
        self.folder = folder

foolib = MyLib("foo", "foosrc")
barlib = MyLib("bar", "barsrc")
```
Now for each library we want to set up a dummy or phony target that when "built" does the globbing and tells scons about the real files.  For this we use the afore mentioned trick that Scons uses to turn a function and parameters into an Action, which we can then use in a Command - an [ActionFactory](ActionFactory). 


```python
from SCons.Script import *

# These are "callbacks" that we set up as actions that Scons can call at build time.
def libcallback(libname):
    # Do something clever
    pass

LibCallback = SCons.Action.ActionFactory(libcallback, lambda name: 'Doing "%s"' % name)
```
So a call to [LibCallBack](LibCallBack) now creates a Action object that "remembers" the parameter it was called with, and when invoked will call my libcallback function with that parameter.  This means I can now add a method to [MyLib](MyLib) class to do the following: 


```python
    def doInitial(self):
        """ This sets up a dummy target to do the lib globbing etc. at build time """

        self.myinitdummy = env.Command(
            "dummy" + self.name + "_libinit", [], LibCallback(self.name)
        )

        env.Alias(self.name, self.myinitdummy)
```
The Command line is telling scons about a target of "dummy_libfoo_libinit" which is a file that will never exist so scons will always attempt to build it.  It has no source files (just an empty list) and to "build" it scons will call libcallback with self.name. 

I'll explain the Alias at the end. 

So now we need to do the something clever in the callback (well.. actually it's not that clever).  All we do is lookup the library with the name, and then make a call to that object 


```python
def libcallback(libname)
    if libname not in MyLib.allLibs:
        raise Exception("The library %s is not defined" % libname)
    
    MyLib.allLibs[libname].doPreCompile()
```
Now we just need to add the doPreCompile to [MyLib](MyLib): 


```python
    def doPreCompile(self):
        files = glob.glob(os.path.join( self.folder, "*.cxx"))
        
        mydll = env.SharedLibrary(self.name, files, CPPPATH = self.folder)
        env.Depends(self.name, mydll)
```
The last thing is then do the initial calls: 


```python
foolib.doInitial()
barlib.doInitial()
```

The Alias from before, with the above Depends now mean that we can invoke scons like 
```console
scons foo 
```
and it will only glob and consider files in foosrc! 

Of course there downsides in that you can't tell scons to compile a single object file - but we are writing things to get round that. And you can't do a `scons -c`.
However the purpose was to show how you can call something at build time. 

Complete code in context: 
```python
import os
import glob
from SCons.Script import *

env = Environment()


class MyLib:

    allLibs = {}

    def __init__(self, name, folder):
        MyLib.allLibs[name] = self
        self.name = name
        self.folder = folder

    def doInitial(self):
        """ This sets up a dummy target to do the lib globbing etc. at build time """

        self.myinitdummy = env.Command(
            "dummy" + self.name + "_libinit", [], LibCallback(self.name)
        )

        env.Alias(self.name, self.myinitdummy)

    def doPreCompile(self):
        files = glob.glob(os.path.join(self.folder, "*.cxx"))

        mydll = env.SharedLibrary(self.name, files, CPPPATH=self.folder)
        env.Depends(self.name, mydll)

# These are "callbacks" that we set up as actions that Scons can call at build time.
def libcallback(libname):
    if libname not in MyLib.allLibs:
        raise Exception("MyLib: The library %s is not defined" % libname)

    MyLib.allLibs[libname].doPreCompile()

LibCallback = SCons.Action.ActionFactory(libcallback, lambda name: 'Doing "%s"' % name)

foolib = MyLib("foo", "foosrc")
barlib = MyLib("bar", "barsrc")

foolib.doInitial()
barlib.doInitial()
```

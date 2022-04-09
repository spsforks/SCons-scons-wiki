

# Memory Reduction War Stories


## Episode 2: Breaking Reference Cycles

Garbage occurs if objects refer too each other in a circular fashion. Such reference cycles cannot be freed automatically and must be collected by the garbage collector. While it is sometimes hard to avoid creating reference cycles, preventing such cycles saves garbage collection time and limits the lifetime of objects. 

Anyway, is that a problem in SCons? Let's see how much garbage is produced building a simple "Hello World program". 

SConstruct: 
```python
env = Environment()
SConscript('src/SConscript', exports='env')
```
src/SConscript: 
```python
Import('env')
env.Program('hello.c', CPPPATH='.')
```
The garbage can be measured with the garbage debug flag which turns off the garbage collector and prints the garbage that would have been collected. To reduce the noise, the output can be redirected to a file which can be used to build reference graphs to illustrate the cycles graphically. 


```console
> $SCONS --debug=garbage --garbage=leak.txt
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gcc -o src/hello.o -c -Isrc src/hello.c
gcc -o src/hello src/hello.o
scons: done building targets.
Garbage reference graph saved to: leak.txt
Garbage:      893 collected objects (   403 in cycles):    562.06 KB
```
If graphviz is installed, a PDF can be generated with the following commands: 


```console
dot -o leak.dot leak.txt
dot leak.dot -Tps -o leak.eps
epstopdf leak.eps
```
What can be seen are a number of small cycles involving only three or four objects and a few very big cycles.  


## Patch 1: Don't refer to your own stack frame

The big cycles are connected by a hierarchy of interconnected _frame_ objects. After some digging through the SCons source code I found a number of spots where stack-frames are extracted to deal with exceptions or get access to variables stored in the frame of one of the calling functions. The culprit is a local reference to the own stack-frame which creates a cycle: The local variables are stored in the frame. If the frame is referred by one of the variables a cycle has been created. 

Once the problem was found, it was quite easy to fix. As information is searched in one of the prior frames, one can start with the parent frame to prevent the cycle creation. The attached patch solves this problem: [leak_frame.patch](leak_frame.patch) 

Another clean build with the patched version reveals the effect: 


```txt
Garbage:      564 collected objects (   185 in cycles):    255.60 KB
```

## Patch 2: Weak Methods and Weak Proxies

The remaining cycles all involve bound methods as depicted.  

[[/WikiUsers/LudwigHaehne/ReferenceCycles/methodcycle.png]]

The pattern in the code looks like the following: 


```python
class Foo:
  def __init__(self, variant):
    if variant == 'Alice':
      self.method = self.alice
    elif variant == 'Bob':
      self.method = self.bob
  def alice(self):
    pass
  def bob(self):
    pass
```
What can be done is to use [weak methods](http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81253) to refer to the bound methods. This is safe because the method is referenced by the instance it is attached to. If the method refers back (with im_self) a cycle is created. However, the cycle can be avoided if the method only holds a weak reference to the object: [leak_weakmethod.patch](/WikiUsers/LudwigHaehne/ReferenceCycles/leak_weakmethod.patch)

Compiling again we are told that building our hello world example, no garbage is produced at all! 
```txt
Garbage:        0 collected objects (     0 in cycles):      0     B
```
There is one problem with this approach, though. Calling a weak method is slower than calling a bound method: 


```python
import weakref

class WeakMethod(object):
    __slots__ = ('f', 'c')
    def __init__( self , f ) :
        self.f = f.im_func
        self.c = weakref.ref( f.im_self )
    def __call__( self , *arg ) :
        try:
            return self.f(self.c(), *arg)
        except AttributeError:
            raise TypeError, 'Method called on dead object'

class A:
    def __init__(self, variant):
        if variant:
            self.h = self.f
        else:
            self.h = self.g
    def f(self):
        pass
    def g(self):
        pass

class B:
    def __init__(self, variant):
        if variant:
            self.h = WeakMethod(self.f)
        else:
            self.h = WeakMethod(self.g)
    def f(self):
        pass
    def g(self):
        pass


import timeit
t = timeit.Timer('a.h()', 'from __main__ import A \na = A(1)')
print "%.3f usec/call" % (1000000 * t.timeit(1000000) / 1000000)
t = timeit.Timer('a.h()', 'from __main__ import B \na = B(1)')
print "%.3f usec/call" % (1000000 * t.timeit(1000000) / 1000000)
```

```txt
0.378 usec/call (Bound Method invocation)
1.429 usec/call (Weak Method invocation)
```
For real-life use cases, the difference is small but measurable. An up-to-date check of Ardour takes around 43s without and 46s with the weak method patch applied. 

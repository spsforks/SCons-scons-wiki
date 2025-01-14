
# Memory Reduction Techniques

This page describes techniques for reducing the memory footprint of a SCons build. The first part addresses SCons users while the second part discusses techniques that can be applied to reduce the memory consumption in SCons itself. 


## User Guide

SCons implements some debugging facilities that can help to track down memory problems. If those are not sufficient, check out the [SCons Heapmonitor branch](WikiUsers/LudwigHaehne/HeapMonitor). 


```console
scons --debug=memory --debug=count
```
If you got the impression that SCons allocates too much memory to build your project you should first make sure it is really SCons and not a build tool that is used. The easiest way is to run an up-to-date check of your project after a full build was performed. If you still think that SCons takes up too much memory run SCons with the above mentioned debug flags. 

The Node and Executor objects in the `--debug=count` output should correspond to the number of files (or other Node types). There is not much you can do about it. If you see a high number of Environment objects, try to reduce those in your SConscript files. 


### Environment Objects

Environment objects have a high memory footprint. Try to reuse existing environments if you can. Also note that you can override flags when invoking the builder: 


```python 
env.Program('fastfoo.c', CFLAGS='-O3')
```

## Developer Guide


### Limit Lifetime

If you can formulate invariants stating that when reaching a specific condition an object is not needed anymore, delete it. 


### Caching

Caching is commonly employed to speed up access to values which are used more then once. Therefore, there is always a trade-off between memory consumption and runtime performance. SCons used `_memo` dictionaries attached to each object which uses caching. These dictionaries allocate a considerable share of memory. It should always be asked if caching a specific object actually speeds up the build enough to sacrifice the additional memory used by the slot in the cache.  


### Lazy initialization

Empty sequences, dictionaries and sets consume memory. If such an attribute is only needed for a small subset of the instances of a class, lazy initialization can be used. The `ignore` and `depends` attributes of Node objects would be a classic example. Instead of: 


```python 
def __init__(self):
  self.rarely_used = {}
def append(self, k, v):
  self.rarely_used[k] = v
```
The `rarely_used` dictionary can be assigned to an object only if it's used: 


```python 
def __init__(self):
  pass
def append(self, k, v):
  try:
    self.rarely_used[k] = v
  except AttributeError:
    self.rarely_used = {k: v}
```
If the `append` method is not called for most of the existing objects, the alternative above might be used. However, every attempt to access the object must then be protected to not raise an `AttributeError`. 


 Pros  |  Cons
:--|:--
 Does not require special language features  |  Reduces readability of the code 

### __slots__

New-styles classes with slots might be used for helper classes which contain a fixed set of attributes. Some memory overhead can be avoided by using slots because it doesn't create a `__dict__` for the object. 


```python 
class Color(object):
  __slots__ = ('red', 'green', 'blue')
```

 Pros  |  Cons
:--|:---
 Few code changes needed, faster instantiation  |  Requires Python 2.2; pickling must be done manually; does not work with morphing classes 



### Reuse strings with intern

String objects are not reused in general. Assigning the same string to another string actually makes a copy. This can be avoided by using the [built-in function intern()](http://docs.python.org/lib/non-essential-built-in-funcs.html). Using `intern()` applies the Fly-weight pattern: It's most useful when a huge number of instances share a small number of unique attributes. For example, in a huge address database for a specific state, the `city` attribute might be interned as it will most likely be reused by a large number of other address instances: 


```python 
class Citizen:
  def __init__(self, name, address, city):
    self.name = name
    self.address = address
    self.city = intern(city)
```

In SCons, intern strings could be used for filenames, suffixes, any string that has a good chance of being reused. 


 Pros  |  Cons
:---|:----
 Few code changes needed  |  interned strings are immortal in Python 2.2 and before 



### Singleton pattern

Don't create a unique object if a singleton can be used instead. 

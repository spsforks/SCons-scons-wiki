

# Memory Reduction War Stories


## Episode 1 - Lazy Attribute Initialization

As I'm trying to find ways to reduce SCons memory consumption, I'll illustrate how the [HeapMonitor](HeapMonitor) facility can be used by example. 


## Find the problem

Let's take a non-trivial project like Ardour and build it: 


```txt
cd ardour-2.4.1
$SCONS --debug=memory
```
The _debug=memory_ output shows the following footprint: 


```txt
Snapshot Label                     Virtual Total ( Measurable)   Tracked Total
before reading SConscript files:         9.90 MB (    0     B)         0     B
after reading SConscript files:         32.82 MB (    0     B)         0     B
before building targets:                32.82 MB (    0     B)         0     B
after building targets:                 60.26 MB (    0     B)         0     B
```
Although the memory consumption is not critical, there's certainly room for improvement. To get an idea of the distribution, run it under the observation of the Heapmonitor (redirect the Heapmonitor noise to a file that can be analyzed later): 


```txt
$SCONS --debug=heapmonitor --debug=memory > hm.log
```
The first thing to note is that the virtual memory footprint increased just by passing _debug=heapmonitor_. The Heapmonitor keeps a lot of meta-data for all the tracked objects: 


```txt
Snapshot Label                     Virtual Total ( Measurable)   Tracked Total
before reading SConscript files:         9.90 MB (    0     B)         0     B
after reading SConscript files:         49.17 MB (   14.21 MB)        13.04 MB
before building targets:                52.06 MB (   14.36 MB)        13.04 MB
after building targets:                 93.45 MB (   30.12 MB)        28.57 MB
```
The measurable size in brackets depicts the amount of memory asizeof (the integrated sizing facility) is aware of. The heapmonitor-inflicted overhead is discounted. _Tracked total_ is the summed size of all tracked objects at that instant. 

**TODO** Give a better explaination of the difference between VIRTUAL TOTAL and MEASURABLE. 

Beneath the memory is apportioned to the tracked classes.  


```txt
after building targets:                  active     24.90 MB      average   pct
  Action.CommandAction                      844    209.94 KB    254     B    0%
  Action.CommandGeneratorAction             207    176.08 KB    871     B    0%
  Action.FunctionAction                      39     30.31 KB    795     B    0%
  Action.LazyAction                         310    170.05 KB    561     B    0%
  Action.ListAction                         125     26.51 KB    217     B    0%
  Builder.BuilderBase                       795      1.04 MB      1.33 KB    4%
  Builder.CompositeBuilder                  207     30.80 KB    152     B    0%
  Builder.OverrideWarner                      0      1.85 KB      0     B    0%
  Environment.Base                           41      1.65 MB     41.09 KB    6%
  Environment.OverrideEnvironment           153     12.19 KB     81     B    0%
  Executor.Executor                        1348    953.17 KB    724     B    3%
  Executor.Null                            2135      1.63 MB    800     B    6%
  Node.FS.Base                             2238     15.35 MB      7.02 KB   61% <<<
  Node.FS.Dir                               141      1.01 MB      7.30 KB    4%
  Node.FS.File                             1393      6.99 MB      5.14 KB   28% <<<
  Node.Node                                  43    115.27 KB      2.68 KB    0%
  SConsign.DB                                69    492.80 KB      7.14 KB    1%
```
As reported, almost 90% of the (measurable) footprint is due to different Node objects. Moreover, 5-7KB per Node seems rather large. So what is taking up the space in the Node objects? 

Let's generate detailed statistics for Node.FS.Base. Edit the _SConstruct_ and change the default class tracking parameters: 


```txt
import SCons.Heapmonitor
SCons.Heapmonitor.track_class(SCons.Node.FS.Base, resolution_level=2)
```
Now rebuild: 


```txt
$SCONS --debug=heapmonitor --debug=memory > hm-node.fs.base-2.log
```
A couple of coffee-sips later, the heapmonitor produced quite a logging soup to wade through. Looking for Node.FS.Base you'll only find that it's gone. Instead, the formerly _Node.FS.Base_ instances go by the name of _SCons.Node.FS.Base_. That's because the name was chosen implicitly when registering the class. Let's pick two random examples with an average size and look at the referents. 


```txt
SCons.Node.FS.Entry              0x09e75d8c gtk2_ardour/mixer_strip.h

  [...]
  00:01:13.23                       6.82 KB
    __dict__                                          6.80 KB      99% [1]
      [V] includes: [('<', 'vector', '>'), ('<'...    1.94 KB      28% [2]
      [V] _memo: {'get_build_env': Null(), 'get...    1.65 KB      24% [2]
      [V] binfo: <SCons.Node.FS.FileBuildInfo i...  464     B       6% [2]
      [V] prerequisites: []                         192     B       2% [2]
      [V] attributes: <SCons.Node.Attrs instanc...  152     B       2% [2]
      [V] ignore_set: set([])                       136     B       1% [2] <<<<
      [V] depends_set: set([])                      136     B       1% [2] <<<<
      [V] waiting_s_e: set([])                      136     B       1% [2]
      [V] sources_set: set([])                      136     B       1% [2]
      [V] waiting_parents: set([])                  136     B       1% [2]
      [V] implicit_set: set([])                     136     B       1% [2]
      [V] scanner_paths: {}                         128     B       1% [2]
      [V] abspath: '/home/ludwig/Projects/gsoc/...  104     B       1% [2]
      [V] labspath: '/home/ludwig/Projects/gsoc...  104     B       1% [2]
      [V] path_elements: [<SCons.Node.FS.RootDi...   88     B       1% [2]
      [V] path: 'gtk2_ardour/mixer_strip.h'          56     B       0% [2]
      [V] tpath: 'gtk2_ardour/mixer_strip.h'         56     B       0% [2]
      [V] sources: []                                40     B       0% [2]
      [V] depends: []                                40     B       0% [2] <<<<
      [V] side_effects: []                           40     B       0% [2]
      [V] implicit: []                               40     B       0% [2]
      [V] ignore: []                                 40     B       0% [2] <<<<
      [V] suffix: '.h'                               32     B       0% [2]
```

```txt
SCons.Node.FS.Entry              0x09389dcc libs/glibmm2/glibmm/stringutils.os
  [...]
  00:01:13.23                       6.78 KB
    __dict__                                          6.76 KB      99% [1]
      [V] _memo: {'get_build_env': <SCons.Scrip...    2.44 KB      35% [2]
      [V] implicit_set: set([<SCons.Node.FS.Fil...  712     B      10% [2]
      [V] binfo: <SCons.Node.FS.FileBuildInfo i...  384     B       5% [2]
      [V] implicit: [<SCons.Node.FS.File instan...  328     B       4% [2]
      [V] prerequisites: []                         192     B       2% [2]
      [V] _proxy: <SCons.Node.FS.EntryProxy ins...  152     B       2% [2]
      [V] ninfo: <SCons.Node.FS.FileNodeInfo in...  152     B       2% [2]
      [V] attributes: <SCons.Node.Attrs instanc...  152     B       2% [2]
      [V] sources_set: set([<SCons.Node.FS.File...  144     B       2% [2]
      [V] ignore_set: set([])                       136     B       1% [2] <<<<
      [V] depends_set: set([])                      136     B       1% [2] <<<<
      [V] waiting_s_e: set([])                      136     B       1% [2]
      [V] waiting_parents: set([])                  136     B       1% [2]
      [V] scanner_paths: {}                         128     B       1% [2]
      [V] abspath: '/home/ludwig/Projects/gsoc/...  112     B       1% [2]
      [V] labspath: '/home/ludwig/Projects/gsoc...  112     B       1% [2]
      [V] path_elements: [<SCons.Node.FS.RootDi...   96     B       1% [2]
      [V] path: 'libs/glibmm2/glibmm/stringutil...   64     B       0% [2]
      [V] tpath: 'libs/glibmm2/glibmm/stringuti...   64     B       0% [2]
      [V] sources: [<SCons.Node.FS.File instanc...   40     B       0% [2]
      [V] depends: []                                40     B       0% [2] <<<<
      [V] side_effects: []                           40     B       0% [2]
      [V] ignore: []                                 40     B       0% [2] <<<<
      [V] suffix: '.os'                              32     B       0% [2]
```
You may have guessed by the marked refs, that I was looking for fields that are not used for most Nodes but take up space in each of them. AFAICT, ignore and depends are only used if explicitly announced with Ignore() or Depends() in the SConscript files. The latter are not used for the vast majority of Nodes. 


## Fix the problem


### Dumb the problem down

The first idea I came up with was to override getattr: 


```python
class LazyBuddy:
  lazyattr = {
    'a': 0,
    'b': []
  }
  def __getattr__(self, name):
    try:
      return LazyBuddy.lazyattr[name]
    except KeyError:
      raise AttributeError, name
```
This seemed to work great: 


```txt
>>> o = LazyBuddy()
>>> o.a
0
>>> for x in o.b: print 'Nooo'

>>> o.a = 13
>>> o.a
13
```
However, extending a list by calling a method to change the internal state is obviously not handled: 


```txt
>>> o.b.append(42)
>>> o.b
[]
```

### A conservative approach

An easier method would be to just not initialize the attribute until it is actually needed. As a downside, this approach introduces catching [AttributeErrors](AttributeErrors) or calling hasattr explicitly when the attribute is referenced. 


### Being Smarter

To fix the problem with the above approach, a proxy object could be used that creates an actual list or set instance if it is actually needed (e.g. append is called on the proxy). The code could look like that: 


```python
class LazyAttr(object):

    __slots__ = ('obj', 'attr', 'cls')

    def __init__(self, obj, attr, cls):
        self.obj = obj
        self.attr = attr
        self.cls = cls

    def __getattr__(self, name):
        """
        An operation was requested that our lazy proxy can't handle.
        Create a real class instance for the container object and delegate the
        call.
        """
        setattr(self.obj, self.attr, self.cls())
        return getattr(getattr(self.obj, self.attr), name)

    def __contains__(a, b):
        return 0

    def __len__(self):
        return 0

    def __radd__(self, other):
        return other

    def __iter__(self):
        return self

    def next(self):
        raise StopIteration

class Node:

    ...

    lazyattrs = {
        'ignore'       : list,
        'depends'      : list,
        'depends_set'  : set,
        'ignore_set'   : set,
        'side_effects' : list
    }

    def __getattr__(self, name):
        if name in Node.lazyattrs:
            return LazyAttr(self, name, Node.lazyattrs[name])
        else:
            raise AttributeError, name
```

## Quantify (and revert) the fix

                                 |  Original  |  Conservative patch  |  Smart patch 
 ---                             | ---        | ---                  | ---
 after reading SConscript files  |  32.82 MB  |  31.78 MB  |  31.52 MB 
 after building targets          |  60.26 MB  |  59.29 MB  |  59.22 MB 
 Total build time                |  43.83 s   |  43.76 s   |  74.84 s 

The amount of memory saved is about 1MB or 1-2%, depending on the nature of the project. The "smart" patch seems to be nice and elegant, but really hits performance. Furthermore, it is hard to get it really right with all the magic methods involved. 

The conservative patch does not seem to affect the runtime performance. However, it reduces the readability of the code and actually changes the API (ignore, depends, ... are "public" members of the Node object). 


## So what?

Lazy attribute initialization does not gain much and obfuscates the code. In so far the endeavour has been rather fruitless. At least it serves as an example of how to use the Heapmonitor and interpret the data. 



# Heapmonitor Documentation


# Introduction

The Heapmonitor is a facility delivering insight into the memory distribution of SCons. It provides facilities to size individual objects and can track all objects of certain classes. The Heapmonitor is developed in a dedicated SCons Subversion branch as part of a [Google Summer of Code project](GSoC2008/LudwigHaehne).  
[[!table header="no" class="mointable" data="""
 **The Heapmonitor and the associated facilities described herein are not part of the official SCons distribution.** 
"""]]

[[!toc 2]] 


# Usage

The Heapmonitor can be activated by passing the associated debug flag. The gathered data will be shown after the build is complete: 


```txt
scons-hm --debug=heapmonitor
```
In this operation mode, Heapmonitor will track a set of pre-configured SCons classes. Per-instance statistics will be printed to the standard output after SCons has finished building the targets. 


```txt
scons-hm --debug=heapmonitor --debug=memory
```
When used in conjunction with `--debug=memory`, snapshots of all tracked objects will be taken at four pre-defined instants. 


# Basic Functionality


## Instance Tracking

The purpose of instance tracking is to observe the size and lifetime of an object of interest. Creation and destruction timestamps are recorded and the size of the object is sampled when taking a snapshot. 

To track the size of an individual object: 


```python
#!python 
import SCons.Heapmonitor
env = Environment()
SCons.Heapmonitor.track_object(env)
```

## Class Tracking

Most of the time, it's cumbersome to manually track individual instances. All instances of a class can automatically be tracked with `track_class`: 


```python
#!python 
SCons.Heapmonitor.track_class(SCons.Action.CommandAction)
```
All instances of `CommandAction` (or a class that inherits from `CommandAction`) created hereafter are tracked.  


## Tracked Object Snapshot

Tracking alone will not reveal the size of an object. The idea of the Heapmonitor is to sample the sizes of all tracked objects at configurable instants in time. The `create_snapshot` function computes the size of all tracked objects: 


```python
#!python 
SCons.Heapmonitor.create_snapshot('Before juggling with tracked objects')
...
SCons.Heapmonitor.create_snapshot('Juggling aftermath')
```
 

With this information, the distribution of the allocated memory can be apportioned to tracked classes and instances. 


# Advanced Functionality


## Per-referent Sizing

It may not be enough to know the total memory consumption of an object. Detailed per-referent statistics can be gathered recursively up to a given resolution level. Resolution level 1 means that all direct referents of an object will be sized. Level 2 also include the referents of the direct referents, and so forth. Note that the member variables of an instance are typically stored in a dictionary and are therefore second order referents. 


```python
#!python 
SCons.Heapmonitor.track_object(obj, resolution_level=2)
```
The resolution level can be changed if the object is already tracked: 


```python
#!python 
SCons.Heapmonitor.track_change(env, resolution_level=2)
```
The new setting will become effective for the next snapshot. This can help to raise the level of detail for a specific instance of a tracked class without logging all the class' instances with a high verbosity level. Nevertheless, the resolution level can also be set for all instances of a class: 


```python
#!python 
SCons.Heapmonitor.track_class(SCons.Node.FS.Base, resolution_level=1)
```[[!table header="no" class="mointable" data="""
 Please note the per-referent sizing is very memory and computationally intensive. The recorded meta-data must be stored for each referent of a tracked object which might easily quadruplicate the memory footprint of the build. Handle with care and don't use too high resolution levels, especially if set via `track_class`. 
"""]]


## Instantiation traces

Sometimes it is not trivial to observe where an object was instantiated. The Heapmonitor can remember the instantiation stack trace for later evaluation.  


```python
#!python 
SCons.Heapmonitor.track_class(SCons.Node.FS.Base, trace=1)
```
This only works with tracked classes, and **not** with individual objects. 


## Background Monitoring

The Heapmonitor can be configured to take periodic snapshots automatically. The following example will take 10 snapshots a second (approximately) until SCons has exited or the periodic snapshots are stopped with `stop_periodic_snapshots`. Background monitoring also works if `--debug=heapmonitor` is not passed on the command line. In this mode, SCons will only record the total virtual memory associated with it. This can be useful in combination with background monitoring to detect memory usage which is transient or not associated with any tracked object. 


```python
#!python 
SCons.Heapmonitor.start_periodic_snapshots(interval=0.1)
```[[!table header="no" class="mointable" data="""
 Take care if you use automatic snapshots with `--debug=heapmonitor`. The sizing of individual objects might be inconsistent when memory is allocated or freed while the snapshot is being taken. It's safe to use `--debug=memory` alone, though. 
"""]]


## Off-line Analysis

The more data is gathered by the Heapmonitor the more noise is produced on the console. The acquired Heapmonitor log data can also be saved to a file for off-line analysis: 


```txt
scons-hm --debug=heapmonitor --debug=memory --heapprofile=heap.dat
```
The MemStats class of the Heapmonitor provides means to evaluate the collected data. The API is inspired by the [Stats class](http://docs.python.org/lib/profile-stats.html) of the Python profiler. It is possible to sort the data based on user preferences, filter by class and limit the output noise to a manageable magnitude.  

The following example reads the dumped data and prints the ten largest Node objects to the standard output: 


```python
#!python 
from SCons.Heapmonitor import MemStats

stats = MemStats()
stats.load('heap.dat')
stats.sort_stats('size').print_stats(limit=10, filter='Node')
```

### HTML Statistics

The Heapmonitor data can also be emitted in HTML format together with a number of charts (needs python-matplotlib). HTML statistics can be emitted directly, by specifying a file with the extension _.html_ file as the profiling output: 


```txt
scons-hm --debug=heapmonitor --debug=memory --heapprofile=heap.html
```
However, you can also read in the file generated with `--heapprofile`: 


```python
#!python 
from SCons.Heapmonitor import HtmlStats

stats = HtmlStats('heap.dat')
stats.create_html('heap.html')
```

## Tracking Garbage

Garbage occurs if objects refer too each other in a circular fashion. Such reference cycles cannot be freed automatically and must be collected by the garbage collector. While it is sometimes hard to avoid creating reference cycles, preventing such cycles saves garbage collection time and limits the lifetime of objects. 

The Heapmonitor provides special flags to analyze reference cycles. If `--debug=garbage` is passed to SCons, the garbage collector is turned off and the garbage objects are printed: 


```txt
scons-hm --debug=garbage
```
Reference cycles can be visualized with [graphviz](http://www.graphviz.org). A graphviz input file is generated when the `--garbage=`_file_ flag is passed: 


```txt
scons-hm --debug=garbage --garbage=leakgraph.txt
```
The graph file can be turned into a PDF with the following commands (Linux): 


```txt
dot -o leakgraph.dot leakgraph.txt
dot leakgraph.dot -Tps -o leakgraph.eps
epstopdf leakgraph.eps
```

# Limitations and Corner Cases


## Inheritance

Class tracking allows to observe multiple classes that might have an inheritance relationship. An object is only tracked once. Thus, the tracking parameters of the most specialized tracked class control the actual tracking of an instance. 


## Morphing objects

SCons instates the pattern of changing an instance' class at runtime, for example to morph abstract Node objects into File or Directory nodes. The pattern looks like the following in the code: 


```txt
obj.__class__ = OtherClass
```
If the instance which is morphed is already tracked, the instance will continue to be tracked by the Heapmonitor. If the target class is tracked but the instance is not, the instance will only be tracked if the constructor of the target class is called as part of the morphing process. The object will not be re-registered to the new class in the tracked object index. However, the new class is stored in the representation of the object as soon as the object is sized. 


## Shared Data

Data shared between multiple tracked object won't lead to overestimations. Shared data will be assigned to the first (evaluated) tracked object it is referenced from, but is only counted once. Tracked objects are evaluated in the order they were announced to the Heapmonitor. This should make the assignment deterministic from one run to the next, but has two known problems. If the Heapmonitor is used concurrently from multiple threads, the announcement order will likely change and may lead to random assignment of shared data to different objects. Shared data might also be assigned to different objects during its lifetime, see the following example: 


```python
#!python 
class A():
  pass

a = A()
Heapmonitor.track_object(a)
b = A()
Heapmonitor.track_object(b)
b.content = range(100000)
Heapmonitor.create_snapshot('#1')
a.notmine = b.content
Heapmonitor.create_snapshot('#2')
```
In the snapshot #1, _b_s size will include the size of the large list. Then the list is shared with _a_. The snapshot #2 will assign the list's footprint to _a_ because it was registered before _b_. 

If a tracked object _A_ is referenced from another tracked object _B_, _A_s size is not added to _B_s size, regardless of the order in which they are sized. 


## Accuracy

Heapmonitor uses [asizeof](http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/546530) to gather size informations. Asizeof makes assumptions about the memory footprint of the various data types. As it is implemented in pure Python, there is no way to know how the actual Python implementation allocates data and lays it out in memory. Thus, the size numbers are not really accurate and there will always be a divergence between the virtual size of the SCons process as reported by the OS and the sizes asizeof estimates. 

Most recent C/Python versions contain a [facility to report accurate size informations](http://bugs.python.org/issue2898) of Python objects. If available, asizeof uses it to improve the accuracy. 


# Download SCons/Heapmonitor Edition

There are two possibilities to get your hands on the Heapmonitor facility. Either grab one of the packages below or fetch the sources with Subversion. 


## Packages

An installation package is available for your convenience. Choose one of the packages below that suits your platform. 

* [scons-hm-08-0.98.5.tar.gz](scons-hm-08-0.98.5.tar.gz) 
* [scons-hm-08-0.98.5.win32.exe](scons-hm-08-0.98.5.win32.exe) 

### Installation

Once it has been downloaded, it can be installed with the following commands (Linux): 


```txt
$ tar xzf scons-hm-08-0.98.5.tar.gz
$ cd scons-hm-08-0.98.5
$ python setup.py install --prefix=/usr/local --record=install.log
```
This configuration can be safely used without interfering with any already installed SCons version. If you would like to invoke the newly installed branch version, run: 


```txt
$ scons-hm
```
To uninstall, use the record-file created on installation: 


```txt
$ xargs -a install.log rm -f
```

## Development Branch

Check out the development branch with Subversion: 


```txt
svn co http://scons.tigris.org/svn/scons/branches/heapmonitor --username guest
cd heapmonitor
```
Set up runtime environment (Unix): 


```txt
export SCONS_DIR=$PWD/src
export SCONS_LIB_DIR=$SCONS_DIR/engine
export SCONS="python $SCONS_DIR/script/scons.py"
```
Use the development version to build SCons projects: 


```txt
cd /home/user/myproject
$SCONS
```
To get access to the SCons modules outside of SConscripts, for example to import the MemStats class, use this code in your Python scripts: 


```python
#!python 
if 'SCONS_LIB_DIR' in os.environ:
    sys.path.insert(1, os.environ['SCONS_LIB_DIR'])
```

# Tutorials

* [Lazy initialization](LudwigHaehne/LazyInitialization) introduces the basic features of the Heapmonitor 
* [Breaking Reference Cycles](LudwigHaehne/ReferenceCycles) demonstrates how to use the Garbage tracking facility 
* [Block-wise MD5 hashing](LudwigHaehne/ChunkHashing) shows how background monitoring can help detecting transient memory usage 
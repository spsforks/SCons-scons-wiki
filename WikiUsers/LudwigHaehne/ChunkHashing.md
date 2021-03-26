

# Memory Reduction War Stories


## Episode 3: Block-wise MD5 hashing

The MD5 signature generation as it is now reads the whole file into memory and performs the computation on the whole memory block. This is sane for the average source file but not an option for very large files as was pointed out in a number of mailing list posts and bug reports (e.g. [#1646](/SCons/scons/issues/1646), [#1459](/SCons/scons/issues/1646)). 

The memory allocation for signature computation is transient and therefore hard to detect without taking further measures. One has to create a snapshot between fetching the file contents and computing the hash to even notice the memory consumption.  

With some crafted examples like the one below, the memory consumption is observable using external tools like Valgrind/Massif or the Heapmonitor background monitoring facility. 


```python
import os

def get_stat(target, source, env):
    stat = os.stat(source[0].abspath)
    dest = open(target[0].abspath,'w')
    dest.write(str(stat))
    dest.close()

env = Environment()
env.Command('test.big', 'SConstruct', 'dd if=/dev/zero of=test.big seek=900 bs=1M count=0 2>/dev/null')
env.AlwaysBuild('test.big')
env.Command('test.stat', 'test.big', Action(get_stat))
```

### Valgrind/Massif

[Valgrind/Massif](http://valgrind.org/docs/manual/ms-manual.html) used to output informative post-script graphs which were superseded by plain-text output in version 3.3. To make sense of the output, `ms_print` or [msplot](http://www.aaltjegron.nl/msplot/) can be used. Here is an example illustrating `ms_print` for the purpose of extracting memory usage over time. 


```txt
$ valgrind --tool=massif --max-snapshots=30 scons
==15263== Massif, a heap profiler.
==15263== Copyright (C) 2003-2007, and GNU GPL'd, by Nicholas Nethercote
==15263== Using LibVEX rev 1804, a library for dynamic binary translation.
==15263== Copyright (C) 2004-2007, and GNU GPL'd, by OpenWorks LLP.
==15263== Using valgrind-3.3.0-Debian, a dynamic binary instrumentation framework.
==15263== Copyright (C) 2000-2007, and GNU GPL'd, by Julian Seward et al.
==15263== For more details, rerun with: -v
==15263== 
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
dd if=/dev/zero of=test.big seek=900 bs=1M count=0 2>/dev/null
scons: done building targets.
==15263== 

$ ms_print massif.out.15263 | egrep "^ +[0-9,n]"
  n        time(i)         total(B)   useful-heap(B) extra-heap(B)    stacks(B)
  0              0                0                0             0            0
  1     55,822,584        1,797,656        1,788,496         9,160            0
  2     99,907,620        2,691,912        2,678,468        13,444            0
  3    132,124,622        4,595,696        4,581,271        14,425            0
  4    173,337,665        3,045,728        3,029,974        15,754            0
  5    200,090,613        3,126,232        3,109,351        16,881            0
  6    253,459,339        4,132,480        4,109,313        23,167            0
  7    290,156,633        4,139,344        4,116,997        22,347            0
  8    323,160,296        4,944,008        4,918,075        25,933            0
  9    346,719,604        4,993,544        4,962,728        30,816            0
 10    381,837,304        5,112,760        5,079,251        33,509            0
 11    410,636,700        5,179,392        5,143,599        35,793            0
 12    449,771,682      949,033,176      948,993,309        39,867            0 
 13  8,957,989,286      949,033,024      948,993,148        39,876            0
 14  8,973,517,468        5,052,232        5,016,678        35,554            0
```
As the output reveals, SCons uses more than 900MB of memory building this test case. 


### Background Monitoring

The same can be achieved by letting the Heapmonitor create periodic snapshots in the background. The following lines have to be added to the SConstruct to activate background monitoring: 


```python
import SCons.Heapmonitor
SCons.Heapmonitor.start_periodic_snapshots(interval=0.5)
```

```txt
$ scons -Q --debug=memory
dd if=/dev/zero of=test.big seek=900 bs=1M count=0 2>/dev/null
Snapshot Label                     Virtual Total ( Measurable)   Tracked Total
before reading SConscript files:         9.93 MB (    0     B)         0     B
00:00:00.08                             17.94 MB (    0     B)         0     B
after reading SConscript files:         18.68 MB (    0     B)         0     B
before building targets:                18.68 MB (    0     B)         0     B
00:00:00.58                            918.82 MB (    0     B)         0     B
00:00:01.08                            918.82 MB (    0     B)         0     B
00:00:01.58                            918.82 MB (    0     B)         0     B
00:00:02.08                            918.82 MB (    0     B)         0     B
00:00:05.85                             18.82 MB (    0     B)         0     B
after building targets:                 18.82 MB (    0     B)         0     B
```
It becomes even clearer that the memory consumption rises exactly 900MB at some point in time - corresponding to the size of the file for which the signature is computed. 


## Patches

A patch was proposed by Tasci ([#1646](/SCons/scons/issues/1646)) solving that issue by using a generator to read the file chunk-by-chunk. As this would not be backwards compatible, I tried to change the patch to conform to the current requirements. 

The idea is to not use `get_contents` of Node.FS.File for signature generation of large files, but a function returning an open file object. A specialized MD5 signature function receives the file object and computes the signature for the file block-by-block. The block-size is configurable with the `--md5-chunksize=N` flag. 

Here is the result of the test above with the patch applied: 


```txt
$ scons -Q --debug=memory
dd if=/dev/zero of=test.big seek=900 bs=1M count=0 2>/dev/null
Snapshot Label                     Virtual Total ( Measurable)   Tracked Total
before reading SConscript files:         9.96 MB (    0     B)         0     B
00:00:00.02                             17.97 MB (    0     B)         0     B
after reading SConscript files:         18.70 MB (    0     B)         0     B
before building targets:                18.70 MB (    0     B)         0     B
00:00:00.52                             19.02 MB (    0     B)         0     B
00:00:01.02                             19.02 MB (    0     B)         0     B
00:00:01.52                             19.02 MB (    0     B)         0     B
00:00:02.02                             19.02 MB (    0     B)         0     B
00:00:02.52                             19.02 MB (    0     B)         0     B
00:00:03.02                             19.02 MB (    0     B)         0     B
00:00:03.52                             19.02 MB (    0     B)         0     B
00:00:04.02                             19.02 MB (    0     B)         0     B
00:00:04.52                             19.02 MB (    0     B)         0     B
after building targets:                 19.01 MB (    0     B)         0     B
```

## Content Caching

The patch is laid out in a way to allow caching the content of files. This is not done currently but might be integrated at a later time, if it ever deems beneficial. Content caching could be implemented in `get_contents`. There's only one (known) case that would benefit: The contents of a file which is scanned for implicit dependencies could be cached and reused for the MD5 signature computation. The cached contents could be removed after computing the hash. 

A prototype implementation of content caching did not lead to a measurable speedup. Therefore, it's questionable if it's worth the additional memory consumption. Furthermore, some operating systems already perform caching of file contents. 


## Benchmark
[[!table header="no" class="mointable" data="""
                            |  Bigfile-Test Case  |  Ardour       |  Synthetic Project 
 Unpatched                  |  6.0s               |  44.1s        |  8.3s              
 Generator Patch            |  5.0s               |  44.2s        |  8.3s              
 Backward-compatible Patch  |  5.0s               |  44.1s        |  8.3s              
"""]]

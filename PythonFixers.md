
[[!toc 2]] 
# Fixers Available in 2to3

By [GregNoel](GregNoel) 

As part of changing the floor Python version we support to 2.2, we should update our language use to the most modern possible.  It's worth doing, since many of the new language features are faster than the equivalent older features.  I believe we can automate a great deal of this processing. 

Python 3.0 will retire many idioms from older versions of Python, so it provides a program called `2to3` that converts obsolete idioms.  It does this by applying a selectable set of "fixers" to code files.  Since some of the new idioms actually became available as far back as Python 2.0, the program can be used to update usage for a floor of Python 2.2 by a suitable selection of fixers. 


## Aside: Strategy for Python 3.0

Since it seems to be a recurring source of confusion, let's take a quick aside to describe the strategy for dealing with Python 3.0. 

Supporting two code bases, one for 2.x and one for 3.x, is fraught with peril.  There are just too many opportunities for unintentional incompatibilities, either by only updating one code base or by accidentally making different changes. 

Instead, the strategy is to create a code base that works on 2.x and can be mechanically translated to work on 3.x.  We will maintain the 2.x code base, so all changes will be automatically made to the 3.x code base.  This strategy will require some care to make it work, but it is the simplest way to approach the problem. 

Many of the fixers do a good job, but punt on complex translations.  As a result, they need to be manually tweaked.  To deal with this problem, we will try to apply fixers as soon as possible; in other words, this strategy works best if the language we are using is as "modern" as possible.  We will use forward-compatibility routines in the `compat` module to support features that aren't yet available in the base Python version. 

Conversely, for those changes which can't be fully automated, we will try to provide backward-compatibility routines in 3.x.  Some of these may be difficult, as the Python language itself is different, so the exact code required may need to be a compromise to match what we can support in both cases. 

The actual packaging for distribution will probably contain a copy of both code bases.  There are several options that can be employed to provide the end-user with the correct package: the installer could identify the system Python in use and install the correct code base, a front-end shim could detect whether the Python version is 2.x or 3.x and choose the correct version to use, or other ingenous solutions. 

So the major point of this exercise is to identify which fixers can be applied immediately, with or without `compat` support, and which fixers must be reserved for the mechanical upgrade to 3.0.  If the only fixers for the automated step are basically cosmetic, we will be in good shape.  If they will require manual tweaking, life will become more interesting. 


## Table of Fixers

The table below contains the 47 fixers available in Python 3.0.  The **Floor** column is the important one; it says which fixers may be safely applied with the specified floor.  The column can also specify "compat" which means the fixer is safe if the `compat` module provides forward compatibility or the column can specify "unused" which means it's a feature not used in SCons.  As our base Python version moves up, we can apply more of the fixers. 

**CAVEAT:** _I am mostly concerned about fixers for a floor of Python 2.2, so this table is incomplete.  I'd like help completing the missing entries (or even confirming the entries that are present).  If you have knowledge about when fixers are safe to apply or can work on figuring it out empirically, please [contact me](GregNoel)._ 
[[!table header="no" class="mointable" data="""
 **Fixer**[1]  |  **Floor**  |  **Description** 
 `apply`[*](PythonFixers)  |  2.2  |  `apply(fn, arg, kw)` ==> `(fn)(*arg, **kw)` 
 `basestring`[*](PythonFixers)  |  unused  |  `basestring` ==> `str` 
 `buffer`[2][*](PythonFixers)  |  compat?  |  `buffer(...)` ==> `memoryview(...)` 
 `callable`[*](PythonFixers)  |  2.6  |  `callable(obj)` ==> `hasattr(obj, '__call__')` 
 `dict`[*](PythonFixers)  |  2.2  |  for ? in keys, items, values:  
`    dict.?()` ==> `list(dict.?())`  
`    dict.iter?()` ==> `iter(dict.?())` 
 `except` <span style="display:none">[*](PythonFixers)</span>  |  2.6  |  `except e, t` ==> `except e as t` 
 `exec`[*](PythonFixers)  |  3.0  |  `exec code in ns1, ns2` ==> `exec(code, ns1, ns2)` 
 `execfile`[*](PythonFixers)  |  [[!bug 2326]]  |  `execfile(name, *args)` ==> `exec(open(name).read(), *args)` 
 `filter`[*](PythonFixers)  |  2.2  |  `filter(F, X)` ==> `list(filter(F, X))` 
 `funcattrs` <span style="display:none">[*](PythonFixers)</span>  |  2.6  |  for ? in closure doc globals name defaults code dict  
`    f.func_?` ==> `f.__?__` 
 `future`[*](PythonFixers)  |  3.0  |  remove `from __future__ import foo` 
 `getcwdu` <span style="display:none">[*](PythonFixers)</span>  |  unused  |  `os.getcwdu()` ==> `os.getcwd()` 
 `has_key`[*](PythonFixers)  |  2.2  |  `d.has_key(k)` ==> `k in d` 
 `idioms`[2][*](PythonFixers)  |  compat  |  some `type(x) op Type` comparisons into `isinstance()` calls  
some `list.sort()` into `sorted(list)`  
`while 1:` ==> `while True:` 
 `import`[*](PythonFixers)  |  2.5[3]  |  using `'.'` for local directory imports 

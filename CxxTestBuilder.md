
# Description

The builder for running unit tests created with the [CxxTest](http://cxxtest.com) framework. This is the official builder for CxxTest (see below). 

I'm pleased to say that this builder has now been included in the new and improved version of CxxTest that is currently in git. The source code here is not updated every time I fix a bug, mainly because I forget. So, the most up-to-date version can always be found here: [https://github.com/CxxTest/cxxtest/tree/master/build_tools/SCons](https://github.com/CxxTest/cxxtest/tree/master/build_tools/SCons).

Get it there while it's hot. 


# Installation

Get the code from `build_tools/SCons` in your CxxTest distribution. 

Copy this code into a `cxxtest.py` somewhere in your toolpath (usually to `#/site_scons/site_tools/cxxtest.py`). 


# Documentation

An expanded (and maintained) version of the documentation for this builder is located in the builder file. Please consult that version to solve any problems, or email me. It should be very easy to use. 


# Usage

In short, it can be used in the same way the `Program()` builder can be used. You can even specify other flags on call etc. 


## Example


```python
# vanilla include (the 'cxxtest' would be 'CxxTest' if the file was called CxxTest.py!)
env = Environment(tools = ['default', 'cxxtest'])

# if you have to specify some options: (others can be found in the comment block of the generate function in the code or above)
env = Environment(tools = ['default', ('cxxtest', {'CXXTEST':'#/cxxtestgen.py', 'CXXTEST_CPPPATH':'#/libs/cxxtest/'})])

# or you can use this syntax:
env = Environment(tools = ['default','cxxtest'], CXXTEST='#/path/to/cxxtestgen.py')

# if you don't want to have an extra scons_site directory
env = Environment(toolpath=['cxxtest/build_tools/SCons'], tools = ['default','cxxtest'])

env.CxxTest('test_quaternion', source = 'Quaternion.t.h')      # the quaternion test
env.CxxTest('test_utility', ['utility.t.h', '../utility.cpp']) # utility functions test
env.CxxTest('test_timer', ['Timer.t.h'])                       # timer class test

# generate the source for multile files and then call the runner (--root/--part functionality)
env.CxxTest('test_multi', ['TestSuite1.t.h', 'TestSuite2.t.h', 'test_utility_functions.cpp'], CXXFLAGS='-Wall -W -Wextra')

```

# Authors

The 1st version was written by Gašper Ažman, and then completely rewritten again to produce the code as it largely is today. 

Diego Nieto Cid kindly provided the windows interpreter finding fixes. Many thanks! 

Some fixes and additions (and code cleanup) were initiated and implemented by J. Darby Mitchell. It is because of him that I started working on getting this builder to try to work out of the box. 

Globbing support problems reported by Edmundo Lopez, who also provided a patch. As a result, the sourcecode was streamlined in order to fix the problems the patch uncovered. 

The current maintainer is Gašper Ažman (gasper dot azman at gmail dot com). 


# Quality control

All problems reported have their own unit-test that fails if run by a builder without the fix. This means regressions shoud not crop up. If you have a problem with a version of this script that you did not have before, check the changelog - the behaviour might have changed. If that is not the case, please write to me. 


# The code

Get it here: [https://github.com/CxxTest/cxxtest/tree/master/build_tools/SCons](https://github.com/CxxTest/cxxtest/tree/master/build_tools/SCons).
if you are using CxxTest, it should already be in the `build_tools/SCons directory`. Use that one, the latest one might not be backwards-compatible with your local version. 

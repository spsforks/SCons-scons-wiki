

# CheckPython, CheckPythonHeaders and CheckPythonModule (Autoconf Functionality)

The `CheckPython`, `CheckPythonHeaders` and `CheckPythonModule` methods are not yet a part of SCons. The current code is viewable [here](http://scons.tigris.org/source/browse/scons/branches/py-builder/). Adding `CheckPython`, `CheckPythonModule` and `CheckPythonHeaders` methods became a part of [my Google Summer of Code project](http://www.scons.org/wiki/GSoC2008/MatiGruca). 

This functionality is also available for download in installation packages for [Python Binary Builder](http://www.scons.org/wiki/GSoC2008/MatiGruca/InstallPython). 

The [original patch](http://scons.tigris.org/issues/show_bug.cgi?id=1344) was submitted by [Gustavo Carneiro](http://live.gnome.org/GustavoCarneiro). 

Multi-Platform Configuration is described in [SCons User Guide](http://www.scons.org/doc/0.98.5/HTML/scons-user/c3036.html). 


## CheckPython method

`CheckPython(minver)` method checks if a python interpreter is found matching a given minimum version. 

`minver` should be a tuple, eg. to check for `python >= 2.4.2` pass `(2,4,2)` as `minver`. 

If detection is successful, `env['PYTHON']` is defined to point to the python that matches the minimum version constraint.  In addition, `PYTHON_VERSION` is defined as `'MAJOR.MINOR'` (eg. '2.4') of the actual python version found.  Finally, `pythondir` and `pyexecdir` are defined, and point to the site-packages directories (architecture independent and architecture dependent respectively) appropriate for this python version. 


## CheckPythonHeaders method

`CheckPythonHeaders` method checks for headers necessary to compile python extensions. If successful, `CPPPATH` is augmented with paths for python headers. 

This test requires that `CheckPython` was previously executed and successful. 


## CheckPythonModule method

`CheckPythonModule(modulename)` method checks for the existence of module 'modulename'. 

This test requires that [CheckPython](CheckPython) was previously executed and successful. 


## Example

Sample `SConstruct` file: 


```python
#!python 
env = Environment()
conf = Configure(env)
# We need python 2.2.2 or higher
if conf.CheckPython((2,2,2)):
    if conf.CheckPythonHeaders():
        print 'Found Python header files in:', env['CPPPATH']
    else:
        print 'Python header files not found'
        Exit(1)
    if not conf.CheckPythonModule('mechanize'):
        print "Module 'mechanize' not found"
        Exit(1)
else:
    print 'Python 2.2.2 or higher must be installed'
    Exit(1)
conf.Finish()
```
Let's now run `SCons`: 
```txt
$ scons
scons: Reading SConscript files ...
Checking for Python >= 2.2.2...(cached) yes
Checking for C header file Python.h... yes
Found Python header files in: ['/usr/include/python2.5']
Checking for python module mechanize...(cached) no
Module 'mechanize' not found
```
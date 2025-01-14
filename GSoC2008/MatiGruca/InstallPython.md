

# Python Binary Builder (InstallPython method)

The `InstallPython` method is not yet a part of SCons. The current code is viewable [here](http://scons.tigris.org/source/browse/scons/branches/py-builder/). Creating Python Binary Builder is a part of [my Google Summer of Code project](http://www.scons.org/wiki/GSoC2008/MatiGruca). 

An installation package is also available for download: 

* [scons-pybuilder-01-0.98.5.tar.gz](scons-pybuilder-01-0.98.5.tar.gz) 
* [scons-pybuilder-01-0.98.5.win32.exe](scons-pybuilder-01-0.98.5.win32.exe) 
`InstallPython` method provides a possibility to install Python source files along with its binary versions (`.pyc` or `.pyo` files) in chosen directory for public use. 

`InstallPython` takes target (destination) directory as its first argument and a list of source files/directories as a second argument. 

A simple example of `SConstruct` file: 


```txt
env = Environment()
hello = File('hello.py')
env.InstallPython('/usr/local/bin/', hello)
env.Alias('install', '/usr/local/bin/')
```
`SCons` invoked with `-Q install` parameter will compile `hello.py` file into `hello.pyc` and copy both files into `/usr/local/bin/` directory. 

Sample output: 


```txt
$ scons -Q install
Install file: "hello.py" as "/usr/local/bin/hello.py"
Install file: "hello.pyc" as "/usr/local/bin/hello.pyc"
```
`InstallPython` method can also compile Python source files into optimized binary files (`.pyo` suffix) instead of ordinary binaries (`.pyc` files). To achieve this change the call to `Environment()`: 


```txt
env = Environment(TARGETSUFFIX = 'PYO')
hello = File('hello.py')
env.InstallPython('/usr/local/bin/', hello)
env.Alias('install', '/usr/local/bin/')
```
Sample output: 


```txt
$ scons -Q install
Install file: "hello.py" as "/usr/local/bin/hello.py"
Install file: "hello.pyo" as "/usr/local/bin/hello.pyo"
```
`InstallPython` method accepts both files and directories as its source arguments: 


```txt
env = Environment()
pyfiles = Dir('pyfiles/')
env.InstallPython('/usr/local/bin/', pyfiles)
env.Alias('install', '/usr/local/bin')
```
Running `scons -Q install` will copy all the `.py` files from `pyfiles` directory into `/usr/local/lib/pyfiles` directory along with corresponding `.pyc` files. 

Sample output: 


```txt
$ scons -Q install
Install file: "pyfiles/hello.py" as "/usr/local/bin/pyfiles/hello.py"
Install file: "pyfiles/hello.pyc" as "/usr/local/bin/pyfiles/hello.pyc"
Install file: "pyfiles/hello2.py" as "/usr/local/bin/pyfiles/hello2.py"
Install file: "pyfiles/hello2.pyc" as "/usr/local/bin/pyfiles/hello2.pyc"
```
Mixing files and directories is also possible: 


```txt
env = Environment()
hello = File('hello.py')
pyfiles = Dir('pyfiles/')
env.InstallPython('/usr/local/bin/', [hello, pyfiles])
env.Alias('install', '/usr/local/bin')
```
Sample output: 


```txt
$ scons -Q install
Install file: "hello.py" as "/usr/local/bin/hello.py"
Install file: "hello.pyc" as "/usr/local/bin/hello.pyc"
Install file: "pyfiles/hello.py" as "/usr/local/bin/pyfiles/hello.py"
Install file: "pyfiles/hello.pyc" as "/usr/local/bin/pyfiles/hello.pyc"
Install file: "pyfiles/hello2.py" as "/usr/local/bin/pyfiles/hello2.py"
Install file: "pyfiles/hello2.pyc" as "/usr/local/bin/pyfiles/hello2.pyc"
```
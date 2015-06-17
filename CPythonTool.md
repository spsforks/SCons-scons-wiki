# CPython, a binary builder for Python installs

This first version of a Python Binary Builder is based on the work of [Mati Gruca's Google Summer of Code 2008 project](http://www.scons.org/wiki/GSoC2008/MatiGruca) ([last SVN branch](http://scons.tigris.org/source/browse/scons/branches/py-builder/)). 

The `InstallPython` method creates `.pyc` or `.pyo` files for `.py` source files and adds them to the list of targets along with the source files. They are later copied to the destination (target) directory. 

The `InstallPython` Builder takes a target (destination) directory as its first argument and a list of source files/directories as a second argument. It returns the list of target files to copy to the target directory. 


# Download

This builder is developed as an external tool, meaning it is currently not a part of the SCons core sources in all standard distributions. For getting your own copy, please visit the [ToolsIndex](ToolsIndex) and follow the link to its current mainline...or issue the given "branch command" directly. 


# Examples

A simple example of an `SConstruct` file: 


```txt
env = Environment()
hello = File('hello.py')
env.InstallPython('/usr/local/bin/', hello)
env.Alias('install', '/usr/local/bin/')
```
`SCons` invoked with the `-Q install` parameter will compile the `hello.py` file into `hello.pyc`, and copy both files into `/usr/local/bin/` directory. 

Sample output: 


```txt
$ scons -Q install
Install file: "hello.py" as "/usr/local/bin/hello.py"
Install file: "hello.pyc" as "/usr/local/bin/hello.pyc"
```
`InstallPython` can also compile Python source files into optimized binary files (`.pyo` suffix) instead of ordinary binaries (`.pyc` files). To achieve this, change the call to `Environment()` and set the `CPYTHON_PYC` variable to '`0`' (zero): 


```txt
env = Environment(CPYTHON_PYC=0)
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
The `InstallPython` method accepts both, files and directories, as its source arguments: 


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

# Documentation

The current user and reference manuals are available as PDF 

[manual.pdf](manual.pdf) [reference.pdf](reference.pdf) 

and HTML versions 

[manual.html](manual.html) [reference.html](reference.html) 

As a Python application, SCons 1.x/2.x and previous versions use standard means for installation and packaging of Python modules.  More specifically - `distutils`.  While this works good for Unix systems, it is not that convenient on Windows.  See [SConsInstaller](SConsInstaller) for background. 

There are three possible ways of SCons installation: 

* SCons is installed globally and it just works when you type `scons`; 
* SCons is installed locally and works when you specify a full or relative path to `scons`; 
* SCons is not installed, but copied into the project source tree and executed from there. 

### Windows Details

SCons can be installed and used through several ways on Windows: 

1. **From source** - download source distributive, unpack and run `python setup.py install`   
  
 This installs modules into `Python\scons-<version>` dir, creates `scons.bat` and `scons-2.0.1.bat` scripts in `Python\` directory, and places actual command line scripts `scons`, `sconsign` and `scons-time` that are executed by .bat files into `Python\Scripts` directory (along with their versioned copies).   
  
 As a result, SCons is **not importable** from Python shell. This was made to allow multiple SCons versions to coexist side-by-side in single Python installation long before [virtualenv](http://pypi.python.org/pypi/virtualenv) was born. 
1. **Using distutils installer** - usually named `scons-<version>.win32.exe` it can be downloaded from SCons site   
  
 Installer allows to uninstall SCons from Windows control panel, but file layout is different. Modules are placed into `Python\Lib\site-packages\scons-<version>` and are not importable as in source installation. .bat files and script files are all located in `Python\Scripts`. 
1. **Using setuptools easy_install** - as of 15 April 2011 this way still doesn't work on Windows.   
  
 With `python -m easy_install scons` the latest version (currently alpha) is downloaded from PyPI web site.   
  
 Main problem that due to misplaced directories, SCons scripts can not find SCons modules (which are not importable). Next alpha after 15 Apr 2011 will include fix to allow executing SCons with scripts from `Python\Scripts` directory, and maybe with .bat files. File layout is different for this case also. 
1. **Using distutils MSI installer** - attempt to build this installer currently fails on `FILEaixc++.py`, which seem to be an invalid filename for MSI. 
1. **Copy scons manually** - ... 
1. **Run from checkout** - useful for development and sending patches. ... 

### Unix Details

---
**NOTE**

_As of 4.0, SCons works only with Python 3, and Jython is Python 2 only, with no current indication that a 3.x version is in the works.  To attempt the below, use a checkout of SCons that is prior to the 4.0 release._

---

# SCons on Jython

Getting Jython source code: 


```txt
$ svn co
```
To update run: 


```txt
$ cd jython
$ svn up
```
To compile a development version: 

run ant  inside of the jython directory 

The following settings will have to be made within: 


```txt
dist/bin/jython
JAVA_HOME      Java installation directory
JYTHON_HOME    Jython installation directory
JYTHON_OPTS    Default Jython command line arguments
```
You can set an alias in your shell for the jython command and point it to dist/bin/jython 

Installing setuptools 


```txt
$ wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c9.tar.gz#md5=3864c01d9c719c8924c455714492295e
$ tar xzvf setuptools-0.6c9.tar.gz
$ cd setuptools-0.6c9
$ jython setup.py build
$ jython setup.py install
```
Installing qmtest 


```txt
$ svn co svn://source.codesourcery.com/qmtest/trunk qmtest
$ cd qmtest
$ jython setup.py build
$ jython setup.py install
```
Installing SCons using the Jython branch 


```txt
$ svn co  scons-jython
$ cd scons-jython
$ jython bootstrap.py build/scons
$ export SCONS_LIB_DIR=`pwd`/src/engine
$ jython src/script/scons.py build/scons

$ cd build/scons
$ jython setup.py install

Optional:
$ jython setup.py install --standard-lib
Installs SCons libraries into the Python std lib

```
-incompatabilities fixed in the Jython port 

-the porting progress and changes to SCons 

-how to use SCons on Jython 

-information about the setup of a buildbot for SCons on Jython 

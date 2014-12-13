

# Introduction

This page is currently under construction. 


# Stories

This section will outline some ways in which I see a system for building Python packages being used. I'll use [NumPy](http://www.scipy.org/) for some of the examples, since this is a good example of a project with a large body of C and Fortran code. The NumPy developers had to write [lots of extra code](http://projects.scipy.org/scipy/numpy/browser/trunk/numpy/distutils) to get their package to build across many platforms with many configurations. 


## New User

1. The user goes to the [NumPy download page](http://www.scipy.org/Download). 
1. The user chooses the binary package (.rpm, .dmg, .egg, .exe) of the latest release for his platform and CPU type. 
1. The user installs the binary package. 
1. `import numpy` works. 

## Bug Reporter

1. The user finds a bug in NumPy and reports it to the developers. 
1. The bug is fixed in SVN. 
1. The user is asked to verify the bugfix. 
1. The user checks out the latest revision from SVN. 
1. `python setup.py installl` 
1. `import numpy` works and the user verifies the bugfix. 
In this case, the user isn't interested in building the package with optimized libraries or a specific compiler. He simply wants to build it using whatever tools are available on his system. For some packages, he might have to install some third party libraries in default locations prior to building. 


## Experienced User

1. The user has purchased the [Intel Matrix Kernel Library](http://www.intel.com/cd/software/products/asmo-na/eng/perflib/mkl/266858.htm) for Windows or downloaded the free version for Linux. 
1. The user checks out the latest revision of NumPy from SVN. 
1. `python setup.py build --with-mkl install` 
1. The user uses his optimized version of NumPy. 
In this case, recompiling NumPy with MKL was anticipated by the developers and they were able to add useful default library paths and other details to the setup script. 


# Existing Tools


## setuptools

* Automatically find/download/install/upgrade dependencies at build time using the [EasyInstall](http://peak.telecommunity.com/DevCenter/EasyInstall) tool 
* Create [Python Eggs](http://peak.telecommunity.com/DevCenter/PythonEggs) 
* Project deployment in development mode 
* [setuptools now in Python 2.5 trunk](http://mail.python.org/pipermail/distutils-sig/2006-April/006240.html) 

# Links

* [Building and Distributing Packages with setuptools](http://peak.telecommunity.com/DevCenter/setuptools) 
* [Python Packaging with Setuptools](http://ianbicking.org/docs/setuptools-presentation/) 

# Things to think about

Which Python versions will be supported? SCons supports many old versions, but setuptools only supports 2.3 and 2.4. I think that support for 2.3 and 2.4 might be enough. Other projects such as NumPy [only support 2.3 and 2.4](http://thread.gmane.org/gmane.comp.python.numeric.general/5042/focus=5042). 


# Comments

Feel free to add comments in this section. 

   * While distutils is a good example to look for inspiration, I think this task should not exclusively focus on packaging Python modules, but be useful for packaging software in general. Thus it is important to capture requirements not only from python conventions but other packaging conventions such as the relevant   sections from the  [GNU Coding Standard](http://www.gnu.org/prep/standards/html_node/Managing-Releases.html#Managing-Releases). On a design-related note, I believe it would be best to work on a layered approach, where the lower layer provides 'builders' that hook up common packaging tools (rpm, deb, wininst, tar), and a layer that is largely orthogonal to SCons, and thus can be provided on top of it, which encapsulates the actual workflow. Users will thus be able to wire the low-level builders up manually, without necessarily following any standard (install prefixes, etc.), while typical users will use the high level layer, which works out-of-the-box on all platforms, but doesn't provide flexibility advanced users may desire. --[StefanSeefeld](StefanSeefeld) 

## Random Code


```python
#!python 
import distutils.sysconfig
self['PYEXTPREFIX'] = ''
self['PYEXTSUFFIX'] = distutils.sysconfig.get_config_vars('SO')
def PythonExtensionBuilder(*args, **kw):
    kw.setdefault('SHLIBPREFIX', '$PYEXTPREFIX')
    kw.setdefault('SHLIBSUFFIX', '$PYEXTSUFFIX')
    # ...[0] returns only the dynamic library
    return self['BUILDERS']['SharedLibrary'](*args, **kw)[0]
self['BUILDERS']['PythonExtension'] = PythonExtensionBuilder 
```
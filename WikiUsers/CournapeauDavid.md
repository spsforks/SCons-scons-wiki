

## Cournapeau David

I am a French PhD student at Kyoto University, in speech processing. I use scons for most of my own software projects. 


### Using bzr with scons svn repository

See here: [UsingBzr](UsingBzr) 


### Contribution to scons


#### Better autoconf-like capabilities

Scons is one obvious candidate to replace autotools. Unfortunately, for projects which care about portability, scons is really behind autotools to get capabilities of the platform. I am adding more code to scons to handle those: [CheckTypeSize](CheckTypeSize) to check the size of a C/C++ type, [CheckDeclaration](CheckDeclaration) to check whether a pre-processor symbol is defined, and Define, to define new declarations (useful for custom checks). I intend to add more tests in the [AutoconfRecipes](AutoconfRecipes) list. 


#### Python Extension Support

It would be nice to build python extensions with scons, without the need to use distutils. I am working on this in the pyext branch: 

[http://scons.tigris.org/source/browse/scons/branches/pyext/](http://scons.tigris.org/source/browse/scons/branches/pyext/) 


#### Fortran support

For numscons, I needed a better fortran support. I have cleaned up and updated the fortran support of scons (is in scons since 0.98.0. 


#### More flexible link commands

It is sometimes necessary to control link in a really fine grained manner, because many options are order dependant (think -Bstatic/-Bshared, linked libraries, etc...). Currently, scons makes it difficult to control this without rewriting LINKCOM. I started working on it, and the ideas can be found there in [FlexibleLinkCom](FlexibleLinkCom) 


#### numscons

I am working on integrating scons within distutils, to circumvent distutils deficiencies when building C/Fortran/C++ code, the project is called numscons, and is intended to replace the current build system for numpy and scipy. numscons developement happens on launchapd: 

[https://code.launchpad.net/numpy.scons.support](https://code.launchpad.net/numpy.scons.support) 



---

 [CategoryHomepage](CategoryHomepage) 

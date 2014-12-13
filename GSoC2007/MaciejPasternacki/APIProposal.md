

# API Proposal

This page is intended for proposed API to be discussed and edited.  Final, polished and agreed upon form belongs to [APIReference](GSoC2007/MaciekPasternacki/APIReference) page.  Fragments moved to reference are deleted from proposal. 


## Core API (framework)


### High-level API

All high-level API functions can either be called as project object's methods, or from top-level.  When called from top-level, they refer to primary project, which is first one defined in SConstruct.  Calling any of those without calling Project first will raise an exception. 

Exact set of templates will be determined by analyzing model programs.  Here are few examples of how would they look like 


```python
#!python 
Bin(name, *sources, **kwargs)
=> proj.AutoInstall(Program(name, sources or None, **kwargs))
=> proj.AutoInstall(Script(name, sources or None, **kwargs))
# depending on source file names (*.in will mean script sources).

SBin(name, *sources, **kwargs)
# same as Bin(name, *sources, **kwargs), but with install_dir="sbin"


Data(name, *sources, **kwargs)
=> proj.AutoInstall(SubstInFile(name, *sources, **kwargs))
=> proj.AutoInstall(name) # if sources list is empty

Config(name, *sources, **kwargs)
# same as Data(name, *sources, **kwargs), but with
install_dir="sysconf", machine_dependent=True
```

### Texinfo

Meta-builder combining Info, PostScript, PDF, DVI, HTML builders in one call. 

`Texinfo([target,] source, [default=...])` Compile Texinfo documentation to various formats.  By default, all targets are generated, but all except Info are not built by default. 

List of generated rules can be adjusted by setting targets explicitly; in this case, all targets will be built by default.  List of targets that are build by default can be adjusted by `default` keyword argument, which, if given, should be a list of extensions (example: `Texinfo('manual.texi', default=['info', 'ps','dvi']))`). 


## Additional Builders and top-level functions


### Texinfo

Builders and modifications to get Texinfo  (see [http://www.gnu.org/software/texinfo/texinfo.html](http://www.gnu.org/software/texinfo/texinfo.html)) support: 


#### PDF, PostScript, DVI

Modify to accept `*.texi` sources and use `texi2dvi` command. 

Or maybe separate Texi2DVI builder? 


### Libtool

Not sure if it will be actually needed, or if SharedLibrary() can be used instead (possibly wrapped version, to support building static libraries on systems not supporting shared ones). 

TODO: check also libltdl, libtool/libltdl interaction (is there any actual?), behaviour of libltdl on platforms not supporting dynamic libraries and/or dlopen() equivalent. 


### Glob

Possibly convenience builder to easily alias a group of files with a glob expression. 

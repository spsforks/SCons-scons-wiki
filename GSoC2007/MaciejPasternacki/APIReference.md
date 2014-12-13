

# API Reference

This is reference of the API for automatic build tree generation modeled on Automake project.   Aim of the project is to bring Automake's functionality to SCons.  This page is meant to be exact reference of API, while [API proposal](MaciejPasternacki/APIProposal) is aimed for discussion and exploration of possible API.  This functionality is implemented in `project` SCons Tool. 


# Contents

[[!toc 3]] 


# Operation

Central concept to Automake compatibility functions is a **Project**.  Project is a single package of software built with SCons.  Project is uniquely distinguished by its **name**.  In further sections, _`name`_ will mean a specific project name.  By **user** we will refer to SConstruct author.  **End user** will be person that builds software by running SCons. 

Project deployment is composed of few steps: 


## Distribution

Project distribution is collection of files needed to successfully build, install and test project.  List of files to distribute is mostly created automatically from sources of Nodes that project consists of.  It is also possible to explicitly mark files for distribution. 

Files `INSTALL`, `NEWS`, `README`, `AUTHORS`, `ChangeLog`, `THANKS`, `HACKING`, and `COPYING` at top source directory are automatically distributed if found.  So is `SConstruct` file and all `SConscript` files read. 


## Build

This is stage that SCons already focuses on.  This is actually building software package (usually compiling programs or libraries). 


## Test

Some files can be declared as unit tests for project.  Testing is conducted by building project and all additional files required for testing (test nodes and their dependencies).  After that, all files designated by nodes declared as tests are run in sequence, possibly using some interpreter. 


## Installation

Files that are part of built project are installed into system directories.  There is a standard location for many of commonly used types of files, and these locations form a hierarchy.  This hierarchy is the same as used by Autotools, most of which is required by GNU standards: 
[[!table header="no" class="mointable" data="""
 **prefix**                  |  `"/usr/local"`                         
 **dataroot**                |  `"${DIR.prefix}/share"`                
 **data**                    |  `"${DIR.dataroot}"`                    
 **pkgdata**<sup>1</sup>              |  `"${DIR.data}/${NAME}"`                
 **doc**                     |  `"${DIR.dataroot}/doc/${NAME}"`        
 **html = dvi = ps = pdf**   |  `"${DIR.doc}"`                         
 **info**                    |  `"${DIR.dataroot}/info"`               
 **lisp**                    |  `"${DIR.dataroot}/emacs/site-lisp"`    
 **locale**                  |  `"${DIR.dataroot}/locale"`             
 **man**                     |  `"${DIR.dataroot}/man"`                
 **man**_**X**_<sup>4</sup>       |  `"${DIR.man}/manX"`                    
 **sysconf**                 |  `"${DIR.prefix}/etc"`                  
 **sharedstate**<sup>3</sup>          |  `"${DIR.prefix}/com"`                  
 **pkgsharedstate**<sup>2</sup>       |  `"${DIR.sharedstate}/${NAME}"`         
 **localstate**              |  `"${DIR.prefix}/var"`                  
 **pkglocalstate**<sup>2</sup>        |  `"${DIR.localstate}/${NAME}"`          
 **include**                 |  `"${DIR.prefix}/include"`              
 **pkginclude**<sup>1</sup>           |  `"${DIR.include}/${NAME}"`             
 **exec_prefix**             |  `"${DIR.prefix}"`                      
 **bin**                     |  `"${DIR.exec_prefix}/bin"`             
 **sbin**                    |  `"${DIR.exec_prefix}/sbin"`            
 **libexec**                 |  `"${DIR.exec_prefix}/libexec"`         
 **pkglibexec**<sup>2</sup>           |  `"${DIR.libexec}/${NAME}"`             
 **lib**                     |  `"${DIR.exec_prefix}/lib"`             
 **pkglib**<sup>1</sup>               |  `"${DIR.exec_prefix}/lib/${NAME}"`     
 **oldinclude**              |  `"/usr/include"`                       
 **pkgoldinclude**<sup>2</sup>        |  `"${DIR.oldinclude}/${NAME}"`          
"""]]

<sup>1</sup> Not required by standard, Automake extension <sup>2</sup> Not required by standard, SCons extension <sup>3</sup> Most distros set `sharedstate` directory to `/var/lib` <sup>4</sup> _X_=1,...,9,l,n 

`exec_prefix` and directories derived from it by default are architecture-specific; all other directories are architecture-independent.  Individual installed files can also be explicitly marked as architecture-specific or architecture-independent. 


## Cleaning

Cleaning up build directory after building, to various degrees. 

_Exact semantic is not agreed upon yet._ 


## Distribution check

It is a test for all functions above, checks if distribution is complete and functional.  Distribution check: 

* creates distribution 
* unpacks it in separate directory 
* builds it and runs unit tests 
* installs it in separate sandbox directory 
* uninstalls and checks if there's anything left 
* cleans up after build and checks if there's anything left 
* finally, makes distribution from unpacked distribution and compares distributions 

# End-user API


## Targets

Primary entry points for end-user are **alias targets** defined automatically for each Project.  There are two flavours: per-project targets, that are specific to single project, and global targets, which refer to all projects at once. 


### Per-project targets


#### Distribution

`dist-`_`name`_ alias creates all configured distribution archives for a project.  Specific distribution file names (e.g. _`name`_`-`_`version`_`.tar.gz`) are also available and supported targets. 


#### Build

`all-`_`name`_ target will build all files required for installation of project.  After `all-`_`name`_, installation targets will not need to build or rebuild anything &ndash; they will only copy built files to installation directories. 

`.` or no target will build everything in current directory, including files not required for installation (e.g. helper scripts for testing).  And, of course, naming specific targets still works. 


#### Testing

Alias `check-`_`name`_ will build program, all files needed to conduct tests, and run unit tests. 


#### Installation

* `install-data-`_`name`_ installs architecture-independent files 
* `install-exec-`_`name`_ installs architecture-specific files 
* `install-`_`name`_ installs all files by depending on two targets above, and possibly runs some initialization 
If files needed for installation are not already built (e.g. by running target `all-`_`name`_ earlier), they are rebuilt. 


#### Cleaning

_Exact interface not decided yet._ 


#### Distribution check

`distcheck`-_`name`_ conducts distribution check. 


### Global targets

Targets `dist`, `all`, `check`, `install`, `install-data`, `install-exec` that perform proper actions for all projects defined in SConstruct. 


## Parameters


### Installation directories

For each directory in installation directory hierarchy, an command-line option `--dir_name` is added, by which user can override default value.  Example: `$ scons --dir_prefix=`pwd`/Inst install`. 


### Customized compilation

For customization of build, including optional functionality or dependency, user can declare Autotools-compatible `--with-foo`, `--without-foo`, `--enable-foo` and `--disable-foo` command-line options.  They are, like in Autotools' `./configure` scripts, switches to turn desired functionality on or off, and, when functionality is on, `--with` and `--enable` switches accept optional argument that can be used to e.g. specify library path for optional library that cannot be found automatically. 


# Python API

This is the main API which will be used by user (i.e. SConstruct author). 


## Project

Project object represents a single project (self-contained set of sources with description of build and installation process) built with SCons, and holds information related to project's deployment.  Project object is created with `Project` environment method: 


```python
#!python 
proj = env.Project([name[, version[, bugreport=None]]], [[**keywords]])
```
Parameters `name` and `version` are obligatory and should contain package's name and version as strings (empty version string is explicitly allowed).  `bugreport` should contain contact information for end user to report bugs to; this will usually by author's name and e-mail. 

When `version` is left out, `Project` returns already defined Project object or raises an exception if no Project of that name was defined.  Without `name`, `Project` returns first Project defined in SConstruct. 

To provide alternative way of referring to already defined projects, newly created Projects are added to parent Environment's construction variable `PROJECTS`.  First element of this list is saved in construction variable `PROJECT`.  It is thus possible to expand it in strings substituted by Environment, e.g. `env.Command('version.txt', env.Value(env['PROJECT']['VERSION']), 'echo ${PROJECT["VERSION"]} > $TARGET')`. 

Reserved keywords for `Project` factory function are: 

* `header` &ndash; should contain a Header object, a header file name, or tuple (file name, language) to be fed to `Header` constructor.  This will be the default header file with project description, and will also be used in Configure contexts spawned from Project object; 
* `TEST_COMMAND`, `TEST_ARGS`, `TEST_ENVIRONMENT` &ndash; specify default values for `Test` method keyword arguments `command`, `args` and `environment`; 
* `DIST_TYPE` &ndash; package type (as for `Package` Builder) for source distribution; 
* `DIRECTORIES` &ndash; dictionary of additional or overriden from defualt installation directories. 
Standard informational (optional) keywords for project description are: 

* `SHORTNAME` &ndash; shorter version of name for naming files, if applicable 
* `author` 
* `summary` 
* `description` 
* `url` 
* `license` 
Other data related to project can be specified. 

Nodes (files) that are in some way part of the project need to be **attached** to a project object.  There are four main entry points for attaching files (whenever nodes are mentioned, this is node or file name that names the node): 


### proj.Distribute(*node)

Add Nodes to distribution.  Files passed to this method will be included in project's source distribution, along with their sources if they are built. 

Function returns list of nodes it received. 


### proj.Attach(*node)

**Attach** target to distribution &ndash; make Project object know about the target, and distribute its sources. 

Function returns list of nodes it received. 


### proj.Test(nodes, sources=[], distribute_sources=True, environment={}, command='', args=None)

Build Nodes when testing package and add them to test list.  Attaches `nodes` (a file node or sequence of file nodes) to a project &ndash; their sources are distributed by default.  `sources` argument denotes files that are needed to run tests and are saved as test's dependencies. 

Function returns list of nodes it received. 

`command` argument specifies command used to run tests.  This command is run and receives test file as first argument.  If left empty, test files themselves will be run (as programs or scripts).  Return code of test is checked after running, non-zero means failed test.  Code of 77 will be ignored, which allows failing of non-portable tests in environment where they don't make sense. 

`args` is a list or string of further command-line arguments to the test. 

In effect, full command used to run test is `command test args...`, where both `command` and `args` may be empty, and `test` is a full path to test file. 

`environment` argument is a dictionary of environment variables exported to tests. 


#### User-defined tests

Automatic tests and unit tests can be coupled with custom tests defined by user in SConstruct.  This can be done by adding Nodes (usually, Command Nodes) to appropriate `check` target. 


### proj.AutoInstall(*node, install=None, base=True, executable=None, arch_dependent=None, machine_specific=None, writable=None)

Pass nodes to `proj.Attach()`, add them to `all` alias and to relevant installation alias. 

Function returns list of nodes it received. 

`install` parameter specifies installation directory.  This can be either full absolute path, or name of a predefined installation directory.  When passing full path to `install`, non-None boolean value (`True`, `False`, `0`, `1`) has to be passed to `arch_dependent` for SCons to know whether to put file in `install-exec` or `install-data` phase. 

When `base` is true, node will be installed right in directory specified by `install`.  When it is false, installed target directory will be its full subpath from SConscript within installation directory (e.g. `AutoInstall('tutorial/tutorial.html', install='doc', base=False')` will install `tutorial.html` as `${DIR.doc}/tutorial/tutorial.html`).  When it is a string, this string specifies subdirectory relative to installation directory (e.g. `AutoInstall('tutorial.html', install='doc', base='tutorial')` will install `tutorial.html` in the same place). 

Actual, used values for `AutoInstall` keyword arguments are specified by few levels of default values: 

* Global default keyword arguments: `install=None, base=True, executable=False, arch_dependent=False, machine_specific=False, writable=False` 
* Project's parent Environment construction variable `autoinstall_keywords` (dictionary) 
* Project's own construction variable `autoinstall_keywords` 
* Builder instance's parameter `autoinstall_keywords` 
* Node's OverrideEnvironment's construction variable `autoinstall_keywords` (so that hints can be specified in Builder calls) 
* Actual keyword arguments given to `AutoInstall` 
Defaults coded in standard Builders are: 
[[!table header="no" class="mointable" data="""
 **Program**                         |  install=bin, executable=True, arch_dependent=True                                            
 **Object**                          |  install=pkglib, arch_dependent=True                                                          
 **SharedObject**                   |  install=pkglib, arch_dependent=True, executable=True                                         
 **Library, StaticLibrary**         |  install=lib, arch_dependent=True                                                             
 **SharedLibrary**                  |  install=lib, arch_dependent=True, executable=True                                            
 **LoadableModule**                 |  install=pkglib, arch_dependent=True, executable=True                                         
 **DVI, PDF, PostScript**           |  install=doc                                                                                  
"""]]

`install`, if neither given explicitly, nor determined by Node type, will be determined with following heuristic: 

* if `writable` and either `machine_specific`, or `arch_dependent`, are true, `install='pkglocalstate'` 
* otherwise, if `writable` is true, `install='pkgsharedstate'` 
* otherwise, if `machine_specific` is true, `install='sysconf'` 
* otherwise, if `arch_dependent` is true, `install='pkglib'` 
* otherwise, `install='pkgdata'`. 

#### Manual file handling

Unix manual files are automatically handled in special way: 

* Files installed to `man` directory should have extension that matches a valid manual section (i.e. start with a digit (1-9) or letter (l, n by default) denoting manual section), so that they will be installed in appropriate manual section, not in root manual dir; 
* Files installed to specific manual section (e.g. `install="man3"`), if they do not have an extension already matching this section, will be installed with extension changed to match section. 
Installing files directly to `man` directory is prohibited (if user actually needs it, she can define new directory in hierarchy that expands to `"${DIR.man}"`); non-default manual sections should be declared with API described below. 


#### Installation directory hierarchy

Installation directory hierarchy is kept as attributes of object `proj['DIR']`. 

`proj['DIR'].DefineDirectory(name, directory, arch_dependent=False, help=None)` Define new installation directory in hierarchy and define appropriate `--dir_name` command-line option. 

* `name` &ndash; name of new directory variable (e.g. standard directories' names would be `'prefix'`, `'bin'` etc.); 
* `directory` &ndash; default value of variable.  It should start either with `${DIR.prefix`, `${DIR.exec_prefix`, or variable that starts with one of those. 
* `arch_dependent` &ndash; a boolean that decides if directory is architecture-dependent (i.e. if it should be installed with `install-exec` or `install-data`); 
* `help` &ndash; override default help text for directory variable. 
`proj['DIR'].AddManSection(section)` &ndash; define new manual section.  If it is needed to use section that is not already defined with automatic manual file handling, new section should be declared with this method to make SCons recognize it as valid section. 


### Wrapped methods

Project objects wrap some Environment and global methods to make them cooperate with Project: 

`proj.Alias()` &ndash; calls parent environment's `Alias` method, adding a dash and project name to alias name. 

`proj.Configure()` &ndash; creates Configure context from Project's parent environment, passing it Project's associated Header object to write results of configuration tests (unless user specifies otherwise). 

`proj.Header()` &ndash; when given no arguments, returns Header object associated with Project; otherwise, sets or changes Header associated with Project.  Can be given already created Header object as well as file name. 

`proj.Substitute()` &ndash; default dictionary for Substitute builder when invoked as Project method is dictionary of Environment, updated by dictionary of Project. 


# New or modified Builders and functions


## Header

This is new, separate functionality that can be used without rest of code described in this project, by using `header` Tool. 

Generator of header file for various languages.  Header file consists of comments, constant (or variable in language that does not support constants) definitions, and (possibly but unlikely) fragments of verbatim text.  It is a mean of setting up the program being built by SCons (by e.g. passing it what libraries are available, what is the name and version of the project, or installation directory paths). 

This is a new infrastructure for doing what Configure context does in a limited way.  Configure context is now able to use new Header infrastructure as well as old `config_h` code; this is described in detail in section on changes to existing SCons mechanism. 

`Header(name[, lang[, dict]], [[**keywords]])` function will return an object representing header file named `name`.  Optional `lang` argument is a string specifying header file's language; by default, language is inferred from file name's extension and, if no language matches the extension, C is used.  Further invocations of `Header()` with the same `name` argument will return the same object.  Dictionary `dict` or keyword arguments can be used to supply initial values (or, if header already exists, to supply new values). 

Header objects expose following methods: 


### Low-level methods

`header.Verbatim(text[, position])`  Inserts `text` literally into header file.  `text` may be a string, a callable (result of call with no arguments is inserted), or other value which is coerced to a string.  Optional parameter `position` may be `"top"` or `"bottom"`, which means inserting text at top or bottom of the file.  Returns inserted text as a string. 

Default position for text is in header file's body.  Specifying `"top"` will insert text at beginning of file, before body and all earlier `"top"` insertions.  Similarly, specifying `"bottom"` will insert text at end of file, after body and all earlier `"bottom"` insertions.  Body goes between all `"top"` and `"bottom"` insertions. 

`header.Comment(text[, position], [[noinsert=False, nofill=False]])` Inserts `text` as comment into header, coerced to a string as in `header.Verbatim()`.  Text is reflowed, wrapped and formatted as a comment using conventions for the language associated with file, and inserted into file by calling `header.Verbatim()` method.  Returns formatted comment as a string.  Optional keyword argument `noinsert` will suppress calling `header.Verbatim()` when set to true value.  Optional keyword argument `nofill` will suppress reflow and wrap of original text when set to true value. 

`header.Definition(name, value[, position], [[noinsert=False, comment=None, verbatim=False]])` Checks &ldquo;name&rdquo; for validity as file's language identifier and raises exception if it is invalid.  Otherwise it defines identifier named `name` to value `value`.  Definition text in header's language as a string is returned.  Optional keyword argument `comment` defines comment inserted before the definition.  Optional keyword argument `noinsert` suppresses actual insertion of the definition when set to true value.  Optional keyword argument `verbatim` suppresses any interpretation of `value` when set to true value; `value` is then coerced to string and inserted verbatim into header file. 

When `verbatim` is not set to true, `value` argument is interpreted according to its type: 

* `None` inserts &ldquo;undefined&rdquo; value appropriate to header file's language (`#undef` in C, `undef` in Perl, `None` in Python, etc.) 
* Integer and longint values are inserted as target language's integers (no range checking) 
* Float and double values are inserted as target language's floating point numbers (no range checking) 
* Strings and Unicode strings are inserted as target language's strings 
* Files and file-like objects have their contents inserted at parse time 
* Callables are called without arguments and returned value is inserted according to the same rules 
* Other values are coerced to a string and inserted as target language's string. 

### High-level interface

API described above is low-level and should not be necessary often.  Main, high-level API consists of **templates** and **dictionary access** to header object.  Header objects act as dictionaries of values, where keys are variable names, and values associated with them are their definitions, interpreted as in `header.Define()`.  Contrary to `header.Define()` definitions, which are fixed once called, dictionary assignments can be changed or deleted &ndash; dictionary keys and values at build time are effective. 

Definitions of all dictionary keys and their associated values are inserted in alphabetical order at end of header body. 

`header.Template(name, comment[, value], [[nodef=False]])`  Establishes template for definition `name` to be defined by dictionary access.  Template consists of variable name, comment describing variable that will be inserted before proper definition, and usually an initial value, defaulting to None.  Passing `nodef=True` suppresses initial definition. 


## Substitute

Builder to process `.in` template files to produce target files by substituting keys (by default marked `@KEY@`) to associated values.  Unrecognized keys occuring in file will result in error, empty key (`@@` with default settings) will expand to key marker (single `@` in default settings).  Based on [GaryOberbrunner](GaryOberbrunner)'s [SubstInFileBuilder](SubstInFileBuilder). 

Substituted keys and values are controlled by environment variable `SUBST_KEYS`: 

* if it is not set (default) or expands to false value, simply all construction variables of underlying Environment are expanded; 
* if it is a list or set, it contains explicit list of construction variables that are expanded by this builder; 
* if it is a dictionary, its keys will be substituted to their values: Environment expansion of strings (or, if value is callable, of call result); 
* if it is a callable, it will be called with Environment and substituted keys as arguments, and returned value will be substituted. 
If construction variable `SUBST_IGNORE_UNKNOWN` is set to true value, unknown keys are ignored and left as they are; if set to false or unset, error is signalled on unknown keys. 

Environment variable `SUBST_MARKER` (by default, `'@'`) contain string which will delimit key to be substituted (i.e. by default, `@KEY@` will be expanded to `KEY` variable value).  This is also result of expansion of empty variable.  Alternatively, user can set separately `SUBST_PREFIX` and `SUBST_SUFFIX` to different values; this will not change result of expanding empty key. 

Two more variables control Substitute's behaviour, but there usually should be no need to change them; these are `SUBST_KEY_REGEXP` (`'[a-zA-Z0-9_]+'` by default), which is a regular expression that should match key names, and `SUBST_REGEXP` which is a regular expression, which: 

1. matches whole key with delimiters to be substituted; 
1. its first parenthesized group matches only the key. 
Its default value is `'${re_quote(SUBST_PREFIX)}(|$SUBST_KEY_REGEXP)${re_quote(SUBST_SUFFIX)}'`. 


## Makeinfo

New builder, named `Makeinfo`, located in `makeinfo` Tool, processes Texinfo files by `makeinfo` command to produce various formats of documentation (Info &ndash; default, HTML, XML, plain text). 

Construction variables that affect this builder: 

* `MAKEINFO` (default `'makeinfo'`) &ndash; command used to run makeinfo; 
* `MAKEINFOFLAGS` (default empty) &ndash; additional flags to pass to makeinfo (e.g. `'--html'` to produce HTML output); 
* `TEXINFOPATH` (default empty) &ndash; include path for makeinfo; expanded internally into `_MAKEINFOINCFLAGS` list of switches; 
* `MAKEINFOCOM` (default `'$MAKEINFO $_MAKEINFOINCFLAGS $MAKEINFOFLAGS ${SOURCE}'`) &ndash; complete command used to invoke makeinfo. 

## WithArgument, EnableArgument

These Environment methods, defined in Tool `with`, declare command-line arguments for conditional compilation. 

`env.WithArgument(name, help='', default=None, opts=('with','without'), metavar=-1)` Adds a _with/without_ argument pair.  Defines two command-line options, `--with-name` with optional string value, and `--without-name` switch that takes no value.  Value specified by end user is stored in option `"with_name"`, and it is: 

* `default` keyword argument value (`None` by default) if end user specified neither of switches, 
* `False` if end user specified `--without` switch, 
* `True` if end user specified `--with` switch without value, 
* value given by user to `--with` argument, as string, if user specified `--with` switch with value. 
Help string displayed by the switches is specified by `help` keyword argument, and help text metavariable (see optparse documentation for details) can be specified by `metavar` keyword argument (default is uppercased `name`). 

Optionally, names for switches and option name other than `with`/`without` can be specified in `opts` keyword argument as two-tuple of strings. 

`env.EnableArgument(*args, **kwargs)` Convenience wrapper for `WithArgument` that is identical in use, but by default defines `--enable-name`/`--disable-name` option pair whose value is stored in `"enable_name"` option. 


# Changes to existing SCons mechanism


## Configure contexts

Configure contexts are now able to write `config.h` files to Header objects.  Old `config_h=...` interface is still supported; additional parameter `header=` to constructor of Configure context was added.  In this parameter, user can supply either header object, or target header file name. 

In order to achieve compatibility with Autotools, Configure context now adds `HAVE_CONFIG_H` to `CPPDEFINES` construction variable (effectively adding `-DHAVE_CONFIG_H` to C compiler/preprocessor flags) when configuration header is written in any form (i.e. via `config_h` or `header` parameter). 


### LIBOBJS support

Support for Autotools &ldquo;LIBOBJS&rdquo; functionality (see [http://www.gnu.org/software/autoconf/manual/html_node/Generic-Functions.html](http://www.gnu.org/software/autoconf/manual/html_node/Generic-Functions.html)) was added to Configure context. 

`conf.CheckFunc` method takes additional keyword parameter `add_libobj`.  Its value defaults to False, which means standard behaviour.  Otherwise, library object will be used if function is not found.  If `add_libobj` value is a string or a Node, it will denote the library object's source file.  If it is `True` or `1`, it means that library object's source file name is name of function plus suffix of tested language.  Library object itself is the result of running `Object` builder on library object source file. 

* On Configure context initialization, `ALL_LIBOBJS` and `LIBOBJS` construction variables are set to empty lists; 
* List of all library objects is saved in `ALL_LIBOBJS` construction variable.  This is list of all potentially needed library objects and it is later used by Project to find source files to distribute; 
* If `CheckFunc` does not find tested function, library object is added to `LIBOBJS` construction variable; 
* On Configure context finalization (`conf.Finish()`), contents of `LIBOBJS` variable is added to `LIBS` variable in order to actually link with needed library objects. 

### Missing tools support

Tools that can be considered “maintainer tools” and can be missing on average end user machine, target files for those builders (which are usually source files later on) can be distributed.  When such Tool is missing, pseudo-builders are generated to generate correct dependency tree and detect pre-existing target file, provide warning about missing Tool when target file is considered out of date, and signal an error if target file is missing. 

Support for missing tools is currently built into _lex_ and _yacc_ Tools. 

Tools that need missing support should, besides of `exists` and `generate`, define third function: `missing`, which should accept the same arguments as `generate`, and set up everything so that existing targets are always treated as up-to-date.  If `missing` is defined, `exists` is wrapped by `SCons.Tool.Tool` class: it always returns true value, but if original `exists` returns false, `missing` is called instead of `generate`. 

To make writing `missing` function easier, helper class `SCons.Tool.Missing` is provided.  Its constructor takes obligatory `name` argument, which should be name of the Tool, and optional keyword argument `emitter` which should be an emitter used to create dependencies between Nodes.  Attributes `action` and `emitter` of initialized `Missing` provide wrapped no-op Action and emitter outputting proper messages. 

Example `missing` function, using `SCons.Tool.Missing` class, can be found in _lex_ and _yacc_ Tools. 


### FindSourceFiles

Added new `callback` keyword argument to `FindSourceFiles` Environment method.  User can specify function that will be called for each node in traversed hierarchy with two arguments: visited node and list of results to which node can be appended. 


# Changes to this file


```txt
$Log: APIReference.txt,v $
Revision 1.45  2007/08/27 21:48:46  japhy
- shortname -> SHORTNAME

Revision 1.44  2007/08/27 21:47:26  japhy
- Document SUBST_IGNORE_UNKNOWN

Revision 1.43  2007/08/26 13:17:10  japhy
- Document callback argument to FindSourceFiles.

Revision 1.42  2007/08/25 23:35:53  japhy
- Document Missing tools support.

Revision 1.41  2007/08/25 19:39:40  japhy
- Typo.

Revision 1.40  2007/08/25 19:37:10  japhy
- Document WithArgument and EnableArgument methods.

Revision 1.39  2007/08/20 18:10:37  japhy
- Document default AutoInstall arguments for SharedObject.

Revision 1.38  2007/08/19 16:39:57  japhy
- Cut out Config and Script builder -- they belong to high-level API.

Revision 1.37  2007/08/19 16:25:08  japhy
- Minor edits.

Revision 1.36  2007/08/19 16:08:13  japhy
- Document automatic handling of Unix manual files.

Revision 1.35  2007/08/18 14:38:57  japhy
- Document distcheck

Revision 1.34  2007/08/18 14:14:47  japhy
- Document PROJECT construction variable

Revision 1.33  2007/08/18 12:25:58  japhy
Bulk edit:
- Mention that Project API is defined in "project" Tool
- Specify that Project function is now an Environment method
- Document PROJECTS construction variable
- Cut out distributing directories
- Document that distributed files' sources are also distributed
- Document Test method's sources keyword argument
- Document Alias wrapper
- Multiple minor edits

Revision 1.32  2007/08/18 11:16:40  japhy
- Edit header for `Python API'; add main header and title.

Revision 1.31  2007/08/18 11:13:19  japhy
- Re-edit user-defined tests.

Revision 1.30  2007/08/18 11:08:44  japhy
- Drop `test' target from list of global new targets.

Revision 1.29  2007/08/18 11:07:43  japhy
- Drop install-init alias from reference.

Revision 1.28  2007/08/18 11:06:33  japhy
- Edit.

Revision 1.27  2007/08/17 06:11:08  japhy
- Document command-line options for installation directories and
  current proj['DIR'].DefineDirectory() API.

Revision 1.26  2007/08/17 05:49:18  japhy
- Document important Project variables.

Revision 1.25  2007/08/16 20:06:53  japhy
- Document LIBOBJS support.

Revision 1.24  2007/08/16 19:46:31  japhy
- Describe header-related changes to Configure context API.

Revision 1.23  2007/08/16 19:41:15  japhy
- Delete TODO part, format (add/remove empty lines).

Revision 1.22  2007/08/16 19:37:13  japhy
- Document Makeinfo builder.

Revision 1.21  2007/08/15 21:19:41  japhy
- Typo fix.

Revision 1.20  2007/08/15 21:11:00  japhy
- Document wrapped Project.Substitute builder

Revision 1.19  2007/08/10 20:16:21  japhy
- Document sources argument for proj.Test().

Revision 1.18  2007/08/02 00:58:58  japhy
- Move Substitute builder to API Reference page.

Revision 1.17  2007/07/09 00:55:21  japhy
- Define directories at proj['DIR'], not at proj itself.

Revision 1.16  2007/07/09 00:35:33  japhy
- Rename left `platform-dependent' mentions to `architecture-specific'

Revision 1.15  2007/07/08 23:44:34  japhy
- Document wrapped methods.

Revision 1.14  2007/07/08 23:41:36  japhy
- Add shortening parameter to Project factory.

Revision 1.13  2007/07/08 23:12:48  japhy
- Document Project() factory method arguments.

Revision 1.12  2007/07/08 15:32:57  japhy
- Document dict and keyword arguments to
  SCons.Environment.Base.Header() factory

Revision 1.11  2007/07/08 15:25:06  japhy
- Add Header API description

Revision 1.10  2007/07/07 15:41:47  japhy
- Describe default keyword arguments to Project.AutoInstall()

Revision 1.9  2007/07/05 16:44:36  japhy
- Changed Project.Build method to Attach, and update its semantics to
  make it only attach targets to project, and leave adding to `all'
  target to AutoInstall.

Revision 1.8  2007/06/30 21:47:46  japhy
- Add table of contents.

Revision 1.7  2007/06/30 21:44:32  japhy
- Add RCS log.

```
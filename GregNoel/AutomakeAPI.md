

# Possible Automake API

_This was hacked together in only a couple of hours, so it's more "stream of consciousness" than "carefully thought out" and there are bound to be inconsistencies.  For example, I see I used "package," "distribute," "install," and "deploy" somewhat randomly, sometimes meaning the same thing, sometimes meaning something different (there needs to be an agreement as to the exact nomenclature)._ 


## Project name and version

The basis of the Automake-like support (and future Autoconf-like support?) is the `Project()` function.  It has several forms, each with different semantics. 

`     proj = Project()` 

This form returns the current project or `None` if there isn't a current project. 

`     proj = Project(name)` 

This form returns the project with the given _name_, which must already exist.  The project is set as the current project for this SConscript. 

`     proj = Project(name, version[, contact[, *options]][, **keywords)]` 

This form returns a <ins>new</ins> Project with the specified _name_ and _version_.  A Project with the given _name_ must not already exist.  The project is set as the current project for this SConscript.  If _version_ is (explicitly) `None`, the project won't generate a distribution or packaging of its own, although it can be composed into a higher-level Project.  If _name_ is `None` then the _version_ must also be `None` and the result is an anonymous project with no name of its own.  For example:  
 `     prev = Project()`  
 `     me = Project('libme', '0.1', ...)`  
 `     me.Distribute('LesenSieMich')`  
 `     me.Distribute('LisezMoi')`  
 `     proj = Project(None, None, subset_of = [prev, me], ...)`  
 `     sources = 'common.c subs.c'`  
 `     proj.Lib('me', static_library = sources)`  
 `     proj.Lib('me', shared_library = sources)` 

The files '`LesenSieMich`' and '`LisezMoi`' will appear in a new project named '`libme-0.1`', while the libraries '`libme.a`' and `libme.so` (as well as any other files added to `proj`) will appear in both the original project and '`libme-0.1`'. 

A SConscript inherits the current project of its invoking SConscript.  If invoked SConscript changes the project, the original project is restored when invoked SConscript is complete.  _Future: there should be some way of preventing an invoked SConscript from creating a distribution to allow for the case where a project incorporates another project but does not expose it externally._ 

The _contact_ may be `None` to indicate that there is no contact information.  If the contact contains an @-sign, it is assumed to be a mailing address, typically for bug reports.  If the contact begins with '`http:`' or '`https:`', it is assumed to be a web address for the project.  Otherwise, the contact is assumed to be the author's name. 

The _options_ are zero or more strings of space-separated options.  The _keywords_ are discussed further below; they either provide specialized options or are used as defaults for the construction environment used to build any commands.  For example:  
 `     Project('demo', '0.1', 'demo-bugs@demo.org')`  
 `     Project('demo', '0.1', 'http://bugs.demo.org')`  
 `     Project('demo', '0.1', None, 'dist-tar package-rpm', 'package-zip')`  
 `     Project('demo', '0.1', CCFLAGS = '-O2')`  
 `     Project('demo', '0.1', 'Joe Programmer', 'package-tz', CCFLAGS = '-O2')` 

(_half-baked_) A project acts as a _namespace_ for information about the project.  Names placed in a local project are automatically forwarded to any containing project(s).  Name lookup is forwarded to containing projects in order.  In this way, information from one part of a project can be made available and used in another part of a project.  _TODO:  These semantics are insufficient as stated and need to be fleshed out._ 


### Project options

The _options_ are modeled after [automake's options](http://www.gnu.org/software/automake/manual/html_mono/automake.html#Options); they control the behavior of various features.  Here are some possible options, listed to give an idea of what can be done: 
dist-bzip2
: 
Create a `dist-bzip2` target to provide a source distribution in bzip2-compressed TAR archive and add it to the `dist` target. 


dist-shar
: 
Create a `dist-shar` target to provide a source distribution in SHAR archive and add it to the `dist` target. 


dist-zip
: 
Create a `dist-zip` target to provide a source distribution in ZIP archive and add it to the `dist` target. 


dist-tz
: 
Create a `dist-tz` target to provide a source distribution in GZIP-compressed TAR archive and add it to the `dist` target. 


check-news
: 
Cause '`scons dist`' to fail unless the current version number appears in the first few lines of the NEWS file. 


no-install-info
: 
Info pages will not be built or installed by default. However, `info` and `install-info` targets will still be available. 


no-install-XXX
: 
 For **XXX** in `man`, `html`, _others to be defined_, are similar to `no-install-info` for the specific type of documentation. 


package-rpm
: 
Create a `package-rpm` target to provide a binary package in RPM format and add it to the `package` target. 


package-deb
: 
Create a `package-deb` target to provide a binary package in Debian format and add it to the `package` target. 


package-XXX
: 
Create a `package-XXX` target to provide a binary package in XXX format and add it to the `package` target.  _(other formats to be defined.)_ 


topdir-objects
: 
Generated objects are placed in the top-level build directory. For instance, if the source file is `subdir/file.cxx`, then the output file would be `file.o`. 




### Project keywords

Any keyword not used for project information is assumed to be a construction variable for building objects within this project. 
dist = DIR
: 
The root directory of the distribution tree.  Files will be copied into the distribution directory with their pathname relative to this root.  The default is ‘`#dist/$name-$version`’.  Thus, if `subdir/file.c` is distributed by a project, it will be copied to `#dist/$name-$version/subdir/file.c` for distribution. 


subset_of = DEPLOY_LIST
: 
This project is a subset of other project(s); the distributed files and installed files will be placed in both this project and the enclosing project(s).  The DEPLOY_LIST must be either the name of an existing project or a list of names of existing projects.  If this option is present, the `consists_of` option cannot be present. 


consists_of = DEPLOY_LIST
: 
This project consists of other project(s) in addition to the individual files added to the files specified for this project.  The DEPLOY_LIST must be either the name of an existing project or a list of names of existing projects.  If this options is present, the `subset_of` option cannot be present.  _I think it's possible to create any reasonable relationship between project names with just_ `subset_of`_, so maybe this option isn't needed._ 




### Project targets (still only partially-baked)

A Project will generate aliases for a number of operations, for the most part corresponding to the stages of the development of a product: 

* **Build:** The `all-`_name_ alias builds everything in the _name_ project; the `all` alias consists of the `all-`_name_ aliases for every project in the build. 
* **Test** _TODO: the 'test-name' and 'test' targets ..._ 
* **Install:** A number of targets are generated to install the projects in the build. _TODO: the --install parameter; _installcheck_; Maciej's install-init twist?_ 
   * Each project will have an `install-exec-`_name_ target that installs the platform-dependent files and an `install-data-`_name_ target that installs the platform-independent files.  They both depend on the `all-`_name_ alias. 
   * An `install-`_name_ alias will contain the `install-exec-`_name_ and `install-data-`_name_ targets. 
   * An `install-exec` alias will contain the `install-exec-`_name_ targets for all projects; similarly, an `install-data` alias will contain all the `install-data-`_name_ targets.  They depend on the `all` alias. 
   * An `install` alias will contain the `install-exec` and `install-data` aliases. 
* **Check** _TODO: the various 'check' targets_ 
   * _check:_ really ought to be _test_ 
   * _distcheck:_ creates a distribution file, unpacks in in a temporary location, tries to do a build (in a separate build_dir), runs the test suite, _distcleancheck_, _distuninstallcheck_, and finally make another distribution file. 
   * _distcleancheck:_ _distclean_s the build directory and verifies that everything has been removed. 
   * _distuninstallcheck:_ Installs in a scratch DESTDIR, uninstalls, and verifies that the DESTDIR is empty. 
   * _installcheck:_ Post-install verifications, maybe part of install process? 
* **Distribute:**  For each selected distribution format within a project, there will be a target generated (_e.g._, _name_`-`_version_`-src.tz` for a compressed TAR format) and an alias (_e.g._, `dist-`_name_`-tz`) to generate it.  Each such `dist-`_name_`-`_FORMAT_ alias is included in a `dist-`_name_ alias, which is in turn included in a `dist` alias. 
* **Package:**  For each selected packaging format within a project, there will be a target generated (_e.g._, _name_`-`_version_`.zip` for a ZIP format) and an alias (_e.g._, `package-`_name_`-zip`) to generate it.  Each such `package-`_name_`-`_FORMAT_ alias is included in a `package-`_name_ alias, which is in turn included in a `package` alias. 
* **Clean:** _TODO: Semantics TBD._ 
* **Miscellaneous:** _TODO: other targets not covered above_ 

## SubProject (half-baked)

`     [proj.]SubProject(*options, **keywords)` 

A subproject is an anonymous project within the scope of a larger project. 

The intent is to capture the idea of per-Makefile defaults in Automake.  Each Makefile.am can specify its own AUTOMAKE_OPTIONS and AM_ variables that are in effect for only that file.  A project already has the semantics that it can specify options and construction variables for objects generated from it, so a `SubProject()` declaration is a simplified way of providing this functionality.  Each SConscript would have a `SubProject()` declaration that would provide the defaults for itself (and any SConscripts that it may invoke). 

It's equivalent to `Project(None, None, None, *options, subset_of=proj, **keywords)` and, in fact, the implementation may be exactly that.  However, if `subset_of` is put off for future implementation, there will need to be a way to access this functionality, and `SubProject()` would be the vehicle of choice. 


## Project header files

`     hdr = [proj.]Header()` 

Returns the first header file generated for this project, or `None` if there isn't one. 

`     hdr = [proj.]Header(name[, *options])` 

Returns an object representing a header file with the given name.  If the header already exists, the existing object is returned; otherwise a new object is returned with the specified options applied.  If options are present and there's an existing object, the options must be compatible with those already applied to the object. 

A header file is implemented as a sequence of _keys_.  The first time a given header key is used, it is added to the end of the list of keys to be emitted; subsequent references to the key reuse the same entry.  A key has an optional text part and an optional definition part (at least one must be present).  When a key is expanded, any text part is first written and then any definition is converted in a language-specific way so that the key's value is available to whichever program includes it. 


### Header options

Header options include the language and any other characteristics ... 
C, C++, sh, python, perl, others TBD
: The configuration file will be generated with the quoting and comment conventions of the respective language.  If no language is specified, the default is 'C'. 

no-define
: 
Prevent the `PACKAGE` and `VERSION` variables from being automatically `Define()`d in this header. 




### Header methods

These methods should not be considered as inclusive; there are some other me 

`     hdr.Top(text)`  
 `     hdr.Bottom(text)` 

The _text_ is added at the top or bottom of the header file.  The text is not reflowed or wrapped; it is assumed that the content is valid for the file in question. 

`     hdr.Verbatim(key, text)` 

The _text_ is added to the text (if any) associated with _key_.  The text is not reflowed or wrapped; it is assumed that the content is valid for the file in question. 

`     hdr.Comment(key, text)` 

The _text_ is reflowed and wrapped as a comment using the conventions for the language associated with the file.  The converted text is added to the text (if any) associated with _key_ (using Verbatim() above). 

`     hdr.Template(key, comment)` 

The _comment_ is reflowed and wrapped using Comment() above and the value of _key_ is set to `None`. 

`     hdr.Define(key, value[, comment])` 

If a _comment_ is present, it is reflowed and wrapped using Comment() above and the value of _key_ is set to _value_.  The value can be `None` to cause the key to be undefined in languages that support that concept, or it can be a string or an int which are translated into the appropriate form of language-specific declaration.  _Future: how about a float value?_ 

_Future: a way of inserting file contents into the header._ 



---

 _Stuff below this line is still being rewritten._ 


## Primitive operation

The underlying action to virtually all of the Automake functionality is implemented in this function: 

`     deploy = [project.]DeployDir(directory, *files, sources=None,`  
 `                              install=True, owner='bin', group='bin',`  
 `                              executable=False, platform_specific=False,`  
 `                              distribute=False, substitute=False, **overrides)` 

This function encapsulates all of the operations to distribute the sources, install the files, deploy the files into a deployment directory for packaging, and construct all the Aliases and Action chains as needed.  It uses the current project information (from the SConscript or Environment) to determine where to stage the files.  It returns a deployment object that can be modified by further methods. 

This function is not normally used directly; it's called by one of the wrapper functions.  However, if user needs to specify a non-standard installation directory, the function may be called by a user wrapper. 

(Internally, deployment objects are chained together and not expanded until the end of parsing.  The information is validated when it is added, so any errors should be generated at that time.  Question: does this mean that the overrides should be removed, or does this mechanism just offer a different flavor for convenience?) 


### Parameters

The _directory_ is where the files should be installed, relative to the deployment root. 

The _files_ are a (list of) File node(s) that are to be deployed.  If _files_ is false, no files are deployed. 

If there are _sources_ (a list of filenames and File nodes), presumably the sources for the files being deployed), they are distributed.  If _dist_ is true, the _files_ are distributed as well. 

If _executable_ is true, mode 755 is used, otherwise mode 644 is used (I could be convinced that 555 and 444 are better defaults).  If _platform_specific_ is true, the installation action(s) is(are) linked into an `install-exec` action, otherwise they are linked into an `install-data` action.  If _substitute_ is true, SubstInFile is used to copy the file, otherwise the file is simply copied.  Files installed into the system apply the mode, _owner_, and _group_ directly; files in the deployment area(s) are tagged with the mode, _owner_, and _group_ for the edification of the packager. 

_There may be other parameters yet to be determined._ 


### Deployment objects

The function returns a deployment object that may be modified by various methods TBD... `AddSources()`? `AddFlags()`? `AddLib()`? `AddLoad()`? `Dependencies()`? `ShortName()`? Override a specific construction variable?  Specify (or replace) the choice of a Tool? 


## Wrappers for standard directories

There are a bunch of wrapper functions.  These are the normal way that a user would invoke the functionality.  A package name must be defined in the scope where the wrapper is called. 


### Bin and SBin

`     deploy = [env.]Bin(prog, program=None, script=None, **overrides)`  
 `     deploy = [env.]SBin(prog, program=None, script=None, **overrides)` 

Creates an executable file and installs it in the binary (or system binary) location. 

If program is specified, it's a list of sources to be compiled into the program.  If script is specified, it must be a single file which is built with the SubstInFile builder.  If neither is specified, _prog_ is assumed to be a pre-existing script.  (If both are specified, it's an error.) 

If the executable file is not named '`prog`' (_e.g._, it might be '`prog.exe`'), an alias is created so that '`scons prog`' will build the program. 

The program is deployed into the executable directory (`$EPREFIX/bin` for `Bin()` or `$EPREFIX/sbin` for `SBin()`) using the `DeployDir` function. 


### Data and PkgData

_Other wrapper functions are similar.  Each creates one or more types of file from the inputs and then calls `DeployDir` to do the rest of the processing._ 

_(Variant: data-centric wrappers like `Data()` can specify more than one file to be installed.  I don't know if this convenience outweighs the inconsistency.)_ 

`     deploy = [env.]Data(files=None, subst=None, **overrides)`  
 `     deploy = [env.]PkgData(files=None, subst=None, **overrides)` 

These deploy a list of data files into $DATA (which is normally $PREFIX/share) and $DATA/$name, respectively. 


### Dist

`     deploy = [env.]Dist(files=None, subst=None, **overrides)` 

This method specifies files that are part of the distribution but are not installed or packaged. 


### Doc

`     deploy = [env.]Doc(files=None, subst=None, **overrides)` 

This installs a list of documentation files into $DATA/doc/$name. 

_This installation location is inconsistent: other functions that have the package name appended have a name beginning with 'Pkg' (so this function should be PkgDoc).  We appear to be stuck with it._ 


### Include, PkgInclude, and OldInclude

`     deploy = [env.]Include(headers=None, subst=None, **overrides)`  
 `     deploy = [env.]PkgInclude(headers=None, subst=None, **overrides)`  
 `     deploy = [env.]OldInclude(headers=None, subst=None, **overrides)` 

These install a list of header files into $PREFIX/include, $PREFIX/include/$name, and /usr/include, respectively. 


### Info

`     deploy = [env.]Info(infos=None, subst=None, **overrides)` 

Compiles `.texi` files into `.info` files and deploys them into $DATA/info. 


### Lib and PkgLib

`     deploy = [env.]Lib(lib, library=None, shared_library=None,`  
 `                             libtool=None, **overrides)`  
 `     deploy = [env.]PkgLib(lib, library=None, shared_library=None,`  
 `                                libtool=None, **overrides)` 

Compiles the sources for the type of library requested, binds appropriately, and installs in $EPREFIX/lib or $EPREFIX/lib/$name, respectively. 


### LibExec (and PkgLibExec?)

`     deploy = [env.]LibExec(lib, program=None, script=None, **overrides)`  
 `     deploy = [env.]PkgLibExec(lib, program=None, script=None, **overrides)` 

Installs in $EPREFIX/libexec or $EPREFIX/libexec/$name, respectively. 


### LocalState and SharedState

What kind of files are installed in $PREFIX/var and $PREFIX/com? 


### Man

`     deploy = [env.]Man(mans=None, subst=None, **overrides)` 

This installs a list of (compressed?) man pages in `$DATA/man/man`_x_, where 'x' is the same as the suffix of the file being installed. 


### SysConf

`     deploy = [env.]SysConf(files=None, subst=None, **overrides)` 

This installs a list of files into $PREFIX/etc.  (I believe there's a special case: if $PREFIX is /usr, system configuration files go in /etc.) 

Both `files` and `subst` can be present.  The difference is that `subst` files are run through the SubstInFile builder as they are being installed and any suffix of '`.in`' is removed. 


## Other Stuff

TeXinfo ==> {info,dvi,ps,pdf,html} builders (with `@include(version.texi)` support) 


## TODO

Executable: PROGRAMS, SCRIPTS  
 Libraries: LIBRARIES, LTLIBRARIES  
 Data: DATA, HEADERS  
 Documentation: MANS, TEXINFOS  
 Other: LISP, PYTHON, JAVA (where do these go?)  
 To find: dvi, ps, pdf, html (created by TEXINFOS, go in pkgdatadir/docdir?) 

dist, packaging, check, and test wrappers (more generally, generated stuff not done by default) 

-hook and -local extensions 

TAGS 

AM_ global variable settings 

nobase_ to not strip directories off install name (more generally, insert directories between install directory and file) 

$srcdir, $workdir, $builddir paths?  (may not be necessary?) 


## Examples

All of these examples assume that `Project('demo', '0.1')` is in effect. 


### Simple Program

Build a program and install it in the binary directory: 

`     bin_PROGRAMS = hello`  
 `     hello_SOURCES = main.c` 

becomes 

`     Bin('hello', program = 'main.c')` 


### Simple Library

Build a library and install it in the library directory: 

`     lib_LIBRARIES = sample`  
 `     sample_SOURCES = sample.c` 

becomes 

`     Lib('sample', library = 'sample.c')` 


### Two programs from the same source

Build two programs that share the same source file, but use a different preprocessor value when compiled. 

`     bin_PROGRAMS = true false`  
 `     true_SOURCES = main.c`  
 `     true_CPPFLAGS = -Dreturn=0`  
 `     false_SOURCES = main.c`  
 `     false_CPPFLAGS = -Dreturn=1` 

becomes 

`     Bin('true', program = 'main.c', ADD_FLAGS = '-Dreturn=0')`  
 `     Bin('false', program = 'main.c', ADD_FLAGS = '-Dreturn=1')` 


### Configuration file

Put a file in the configuration directory: 

`     sysconf_DATA = dhcp.conf`  
 `     dhcp_conf_SOURCES = dhcp.conf.in` 

becomes 

`     SysConf('dhcp.conf', subst = 'dhcp.conf.in')` 

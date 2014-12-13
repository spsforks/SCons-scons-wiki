

# SConfiscation Paradigm

****SConfiscate: _verb [trans.]_, to convert a (usually foreign) project to use the SCons build system.  
 SConfiscation: _noun_, the process of SConfiscating a project. **** 

OK, so I made up the word.  It follows in the footsteps of the GNU Autotools people, who speak of "confiscating" a project, meaning that they convert it to their tool chain, that is, make it use `automake` and `autoconf` as a precurser to `make`. 

The usual problem is that the maintainers of the project are often reluctant to allow checkins of a new build system until it has been proven.  Moreover, some source-code control systems object to foreign files within their tree, so it can be difficult to debug a build system within a live tree that's constantly being updated.  This paradigm allows the build system to be isolated from the source (and possibly even distributed independently until the package maintainers see the light and convert). 

The SConfisication paradigm uses both `Repository`() and `VariantDir`(), so it's an example of how the two functions have complimentary usages.  Here's the `SConstruct` I use as a starting point: 

`    src = Dir('path').Dir('to').Dir('repository')`  
 `    bld = Dir('build')`  
 `    dbx = bld.File('.sconsign')` 

`    Repository(src)`  
 `    config = SConscript('SConfigure', variant_dir=bld, duplicate=0)`  
 `    SConscript('SConscript', variant_dir=bld, duplicate=0, exports='config')`  
 `    SConsignFile(dbx.path)` 

The first three lines are the variable information; they are different for every project.  The strange-looking `Dir()...` sequence is so that the path is platform-independent; there are other was to gain this platform independence, but this technique is simple and straightforward and doesn't require importing Python modules to concatenate the path elements. 

The last four lines are pretty much canned and rarely change.  I prefer the actual work to be done by two external files: a `SConfigure` script that is responsible determining the system variability and a `SConscript` script that creates the build.  They communicate through a `config` object that contains any necessary configuration. 

The last line of the `SConstruct` places the build database within the build tree, so that all knowledge of the build can be eliminated by removing the build directory (_e.g._, to force a rebuild from scratch).  If this is not wanted, the `SConsignFile`() and the setting of `dbx` is unnecessary. 

For smaller projects, the first `SConscript()` call, the `SConfigure` script, and the `config` object is not needed and can be left out.  If the system is extremely small, the external `SConscript` file can be replaced by a `VariantDir`() and build declarations within the `SConstruct`: 

`    VariantDir(bld, '.', duplicate=0)`  
 `    Program(bld.File('prog'), [bld.File('prog1.c'), bld.File('prog2.c')])` 

However, if the project is this small, it's very unusual that this much machinery is needed. 

There are dozens of variants of this paradigm.  Here are some examples. 


### Example: Revising an existing SCons-based build system

When revamping a build system that already uses SCons, this same pattern can be used to overlay the existing SConscripts with the new ones, and existing ones that don't need to change can still be used in place: 

`    src = Dir('path').Dir('to').Dir('current')`  
 `    bld = Dir('build')`  
 `    dbx = bld.File('.sconsign')` 

_This is a hint: as this page is being composed, the current build system for SCons itself is in sad shape.  It was written using a prehistoric version of SCons, before most of the modern conveniences were implemented, and it's a complicated mass of spaghetti.  Some serious cleanup is needed, probably pretty much creating a new build system from scratch._ 


### Example: Build system in a subdirectory

Some projects support multiple build systems and want the sources for each build system to be kept in a separate subdirectory of the main directory.  This paradigm can be easily adapted to do that: 

`    src = Dir('..').Dir('code')`  
 `    bld = Dir('..').Dir('build')`  
 `    dbx = bld.File('.sconsign')` 

This example builds from the '`code`' subdirectory of the main directory and places the output in the '`build`' subdirectory of the main directory. 

In fact, if the requirement is to exactly replace a build system that builds in the same tree as the source code, it can do that, as well: 

`    src = Dir('..').Dir('code')`  
 `    bld = src`  
 `    dbx = File('.sconsign')` 

In this latter case, we keep the build database in the SCons subdirectory to avoid creating additional artifacts in the source area. 

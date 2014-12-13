
****Third draft, with more examples and details.  This description now includes the entire future scope of what the `IAPAT` will do, even though only two aspects are currently explored.**** 

****Note that this content is maintained elsewhere, so please don't change this page directly.  Instead, if you have comments, or find things wrong or inconsistent, let me know and I'll fix it as quickly as possible.  If it's something trivial (like a typo), contact me via the the email information in my [wiki home page](GregNoel).  If it's more significant, write me in the scons-dev mailing list, or create a section in the [discussion page](PlatformToolConfig/Discussion). Thanks!**** 


# Introduction and Overview

This page introduces the `InformationAboutPlatformAndTools` (`IAPAT`) class.  It is the focus of all of the discussion below.  The intent is that users will be naturally encouraged to use a new paradigm for their development:   
`     iapat = InformationAboutPlatformAndTools()`   
`     ... modify iapat for their build`   
`     env = iapat.Environment()`   
The existing `Environment()` function will be redefined in terms of a default `IAPAT`; that is, it's the rough equivalent of this code:   
`     def Environment(*args, **kw):`   
`          iapat = DefaultInformationAboutPlatformAndTools()`   
`          return iapat.Environment(*args, **kw)` 

Information collected in the `IAPAT` is used to set up a derived `Environment`.  The `IAPAT` can be reused so that the same collected information can be used in more than one `Environment`.  Thus, to set up a configuration for the entire build, one only need initialize the default `IAPAT` suitably. 

A side-effect is that the SCons `Environment` is no longer the focus for configuration and becomes much cheaper to construct.  The user is naturally guided into using one or two `IAPAT`s for configuration and then reusing them for more than one `Environment` to get detailed control over their build steps. 

The name `InformationAboutPlatformAndTools` is deliberately chosen to be as unusable as possible, so that it'll have to be changed before implementing it.  Inventing good names is not one of my skills; I'll leave that to others who have a better imagination than I do. 

There's a quick overview just after the table of contents. [[!toc 2]] 


### Platform Configuration

xxx???  Should there be a section reflecting how the existing platform configuration is now contained in an `IAPAT` rather than an `Environment`?  Includes use of default `IAPAT`... 

If an `IAPAT` has no platform argument, the `--build` host is used to specify the platform type.  If not given for the default `IAPAT`, the `--build` host is used.  As a result, if the user does nothing special, all one has to do is give the `--build` option on the command line and the build will be cross-compiled.  (Perhaps the `--target` option will be used; [see this section](PlatformToolConfig).) 

In general, the user will  XXXXXXXX 


### Cross-Compilation

For [cross-compilation](PlatformToolConfig), the intent is that everything Just Works.  Note that as a result of the platform configuration, the default is that all the targets are cross-compiled.  If users creats an `IAPAT` (_i.e._, uses something other than the default `IAPAT`), they will have to be aware that the xxx 

To enable [cross-compilation](PlatformToolConfig), all a user has to do is use the `IAPAT` paradigm.  The intent is that everything else Just Works. 

Methods are provided to interrogate the GNU cpu-vendor-kernel-os information as well as the SCons platform ID:   
`     if iapat['PLATFORM'] == 'darwin': iapat['FRAMEWORKS'] = 'Cocoa'`   
`     if iapat['PLATFORM_CPU'] == 'sparc': iapat['CCFLAGS'] += '-mv8'` 

Based on the platform type, the `IAPAT` setup also determines the prefix and suffix for things like program names, library names, and the like.   
`    prog_name = iapat['PROGPREFIX'] + 'prog' + iapat['PROGSUFFIX']`   
`    if prog_name != 'prog': Alias('prog', progname)` 

The `IAPAT` also contains the shell environment that will be used by any commands run (both the configuration commands below and Environments derived from the `IAPAT`), so this is now the place to fiddle with those values:   
`     iapat['ENV']['PATH'] += os.path.join(sys.environ['HOME'], 'bin')`   
`     iapat.vars.ENV.PATH += '/usr/X11/bin' # maybe`   
`     iapat['ENV']['JAVA_HOME'] = os.environ['JAVA_HOME']` 


### Per-invocation Overrides

Simply put, [per-invocation overrides](PlatformToolConfig) are options and variables found on the command line.  The twist is that a build can save selected options in one or more files and use them as defaults later. 

Restore the specified options and variables from save file:   
`     opts = iapat.OptionFile('saved_args', '--opt', 'CCFLAGS', 'LIBS')`   
`     opts.AddOptions('CC', 'CFLAGS')`   
`     opts.AddOptions('CXX', 'CXXFLAGS')` 

Allow `--type` and `--opt` on the command line:   
`     iapat.EnumOption('type', 'Type of build', 'debug', 'production,build,profile')`   
`     iapat.IntOption('opt', 'Set optimization level', 0, dest='optimize')` 

Allow `--enable-framework` and `--disable-framework` on the command line:   
`     iapat.FeatureOption('framework', 'use of OS X frameworks', True)` 

Allow `--with-threads` and `--without-threads` on the command line:   
`     iapat.PackageOption('threads', 'thread support', True, '/usr/share/threads')` 

Allow `DESTDIR=PATH` on the command line:   
`     iapat.PathVariable('DESTDIR', 'Staging location', 'stage')` 

Allow `CCFLAGS=` on the command line as a SCons list-like variable:   
`     iapat.CLVar('CCFLAGS', 'Common C/C++ options', '-pedantic')`   
`     # add optimization level (from command-line --opt above)`   
`     iapat['CCFLAGS'] += '-O%d' % GetOption('optimize')` 









Set an arbitrary variable that will be copied to derived Environments:   
`     iapat['FOO'] = 'bar'` 

Example usage:   
`     $ scons -opt=2 --type=profile --without-threads DESTDIR=/tmp/stage CCFLAGS='-Wall'` 


### Toolchains

[Toolchains](PlatformToolConfig) are the way a user identifies the commands that are needed for the build. A _toolchain_ is one or more _tool_s that should be used together.  Any toolchains used in the build must be declared.  Toolchains may be specified abstractly (`'CC'` asks for an available C toolchain based on the platform defaults) or concretely (`'CC-intel'` specifies the Intel C compiler toolchain). 

xxx work on these examples   
`    iapat.Toolchain('CC', 'CXX')`   
`    ftn = iapat.Toolchain.OneOf('F90', 'F95', 'F77', 'FC')`   
`    my_tools = iapat.Toolchain.All('TeX', ftn)`   
`    iapat.Toolchain.SetDefault(my_tools)` 


### Per-platform Configuration

[Per-platform configuration](PlatformToolConfig) allows features of the `IAPAT`'s platform to be probed.  Multiple header files can be created and they can be created for different language conventions.  Variables declared in a header are placed (with their values) in the header when it is generated:   
`    hdr = iapat.Header('config.h')`   
`    hdr.Comment('/* GENERATED FILE: do not edit */')`   
`    hdr.Comment(disclaimer)`   
`    hdr.Declare('PREFIX', 'Path prefix to installed location', '/usr/share')`   
`    hdr.vars.PREFIX = GetOption(['prefix'])`   
`    hdr.Declare('HAVE_LIBM', 'Can use functions in math library')`   
`    hdr.vars.HAVE_LIBM = iapat.CheckHeader('math.h')`   
`    hdr.Declare('HAVE_ZLIB', 'Include support for zlib compression')` 

Configuration nodes can be created and placed in a DAG.  Evaluating the node as a 'bool' or a 'str' causes the commands to be run and the appropriate result returned:   
`    if iapat.TryCommand(c_cmd_line, test_prog): ...`   
`    action = iapat.CheckHeader('zlib.h')`   
`    node = iapat.MakeNode('check.hdr.zlib', None, action)`   
`    action = iapat.CheckFunc('zlib', 'zlib.h')`   
`    node = iapat.MakeNode('check.hdrfunc.zlib', node, action)`   
`    hdr.vars.HAVE_ZLIB = node` 

<a name="cross"></a> 
# Cross-compilation

xxx we're discussing the `IAPAT` itself 


## Requirements

Here are a set of goals for what the new scheme must achieve.  It's in the form of a checklist, with items checked off that I belive are taken care of in this design.  This list is roughly in in order by importance. 

* (./) Simple and intuitive, _i.e._, SCons-like. 
* (./) Process --build, --host, --target on command line 
* (./) Do cross-compilation 
* (mostly) Be interrogatable for what was determined 
* Retain configuration across invocations 
* (probably) Adequate performance 

## Synopsis

The idea is that the user can create an InformationAboutPlatformAndTools (IAPAT) instance for each platform that is of interest, seeding it with suitable information.  This establishes a number of "interesting" values about the platform.  Tools are then configured for this platform by running a method and giving it the name of the toolchain wanted. 

The simplest case is when no paramters are specified.  If the command line has a `--host` option, that argument is used, otherwise the default is to set up for the local machine:   
`    iapat = InformatonAboutPlatformAndTools()` 

If one argument is specified, it is either a single value or hyphen-separated values.  The single value can either be one of the SCons platform IDs (or values we choose to add later) or a special form that refers to the command line; the hyphen-separated values are split and proceed as if they had been specified as multiple arguments:   
`    iapat = InformatonAboutPlatformAndTools('--target')`   
`    iapat = InformatonAboutPlatformAndTools('darwin')`   
`    iapat = InformatonAboutPlatformAndTools('posix')`   
`    iapat = InformatonAboutPlatformAndTools('win32')`   
`    iapat = InformatonAboutPlatformAndTools('cray-unicos')`   
`    iapat = InformatonAboutPlatformAndTools('580-amdahl-sysv')`   
`    iapat = InformatonAboutPlatformAndTools('x86-suse-linux-gnu')` 

If there are two arguments, the first is a CPU designation and the second is a shorthand of either the vendor or the operating system.   
`    iapat = InformatonAboutPlatformAndTools('sparc', 'sun')`   
`    iapat = InformatonAboutPlatformAndTools('pyramid', 'bsd')`   
`    iapat = InformatonAboutPlatformAndTools('ppc', 'ibm')`   
`    iapat = InformatonAboutPlatformAndTools('ppc', 'osx')`   
`    iapat = InformatonAboutPlatformAndTools('x86', 'osx')`   
`    iapat = InformatonAboutPlatformAndTools('x86', 'pc')` 

If there are three arguments, they are the CPU designation, the vendor, and the operating system:   
`    iapat = InformatonAboutPlatformAndTools('ppc', 'apple', 'osx')`   
`    iapat = InformatonAboutPlatformAndTools('amd64', 'redhat', 'linux')`   
`    iapat = InformatonAboutPlatformAndTools('x86', 'pc', 'windows')` 

If there are four arguments, they are the CPU designation, the vendor, the kernel, and the OS:   
`    iapat = InformatonAboutPlatformAndTools('x86', 'debian', 'linux', 'gnu')`   
`    iapat = InformatonAboutPlatformAndTools('ppc', 'apple', 'darwin', 'osx')` 

In all cases, the arguments are processed to produce five canonicalized values: the platform, the CPU, the vendor, the kernel, and the OS.  If a value cannot be determined, a reasonable default is used.  Note that little attempt is made to validate that the pieces fit together properly, so it's quite possible that a bogus specification will lead to an illegal combination. 

In addition to the canonicalized values, an `IAPAT` has variables that help when setting up a cross-build.  For example, `CROSSPREFIX` is empty for a normal compile but is set with the standard GNU prefix for a cross-build, so it's simple to locate the appropriate program:   
`    erlang = iapat.WhereIs('${CROSSPREFIX}erlc')`   
The Erlang compiler is `'erlc'` in a normal build or `'powerpc-apple-darwin9-erlc'` for a cross-compile to OS X on PPC. 


## Background: GNU Autotools

There's a tension between the SCons platform configuration and the GNU autotools platform configuration.  The former has a small set of key identifiers (`aix`, `posix`, `os2`, `win32`, ...) that completely categorizes the tool selection.  The later uses a canonical string of either three or four values (`cpu-vendor-os` or `cpu-vendor-kernel-os`) that allows great descriptivness and flexibility.  (For historical reasons, this canonical string is called a _triple_.)  This proposal tries to keep the small set of standard identifiers while allowing much of the flexibility of triples when it is needed. 


### Autotools Model

The GNU autotools model is concerned with with running cross-compilers, so it defines three types of machines: the _build_ machine, the _host_ machine, and the _target_ machine: 

* The build machine is where where the build will take place, normally the current machine.  If the build triple is not given, it is assumed to be the current machine and the triple values are guessed. 
* The host machine and OS where the built program will run.  By default, it is the same as the build machine.  If the host machine is specified, it means that the the current build is a cross-compile, producing a program that will run on the host. 
* The target machine is what the built program will generate output for.  By default, it is the same as the host machine, so that the built program will produce output for the machine it runs on.  If it's different, the built program is itself a cross-compiler. 
If the build triple isn't given, GNU uses a shell script called `config.guess` to determine it, which goes through a complex series of gyrations (including probes of the filesystem and even the occasional compile) to determine the canonical name of the current machine.  It's infected by the GNU virus so I haven't looked at it, but it's supposed to be a nightmare of complexity that's grown hoary rings over the years. 

GNU also uses a shell script called `config.sub` to canonicalize a triple and provide aliases for common architectures.  (For example, a CPU of `'ppc'` is canonicalized into `'powerpc'`; `'ppc'` is called an _alias_.)  This means that anything analyzing the triple doesn't need to know that, for example, `'amd64'` is really a CPU type of `'x86_64'`.  It's also infected by the GNU virus and is also supposed to be complex. 

<a name="#autocompat"></a> === Compatibility Constraints and Related Issues=== 

By far the most common complaint of people using the GNU system is that just specifying the target machine (the `--target` option to `configure`) is that their programs aren't cross-compiled.  It's not intuitive that one has to specify the <ins>`--host`</ins> option to get a cross-compile of the program being built.  Therefore, I believe we need to break with this model, either by coining a new word for the output of the built cross-compiler or by defaulting things such that just specifying the target machine will cross-compile the build.  I don't have any immediate suggestions for either case, but [see the discussion](PlatformToolConfig/Discussion) about it.. 

SCons doesn't have to deal with the possibility of a separate build host (GNU `configure` may need to generate configure scripts for use on another system), so we probably don't need to distinguish between some platforms that `config.guess` considers important.  Moreover, we have more information available from the Python run-time, so we probably won't need to go to the extremes `config.guess` does to determine the build host's identity. 

We should try to be as compatible with the GNU triples as possible, but because of the GNU virus, anyone implementing the SCons code can't look at the `config.guess` and `config.sub` shell scripts.  We will have to use the [clean room design](http://en.wikipedia.org/wiki/Clean_room_design) paradigm to implement our code, with complete documentation of the communication between the "clean" and "dirty" sides. 


## Canonicalization

SCons will have to implement canonicalization, although it won't have to implement the full range that `config.sub` does.  The complete set of aliases recognized by `config.sub` includes hundreds, perhaps thousands, of aliases for obsolete machines and vendors.  I don't propose that we implement all aliases (we won't be concerned with a DEC PDP-11, for example), since the effort to completely reverse-engineer `config.sub` would be a herculean task (and we won't even think about the issues with the license).  We should implement a subset, but the choice of subset belongs in the separate specification. 

There are five general types of autoconf alias: 

* simple name: 'decstation' for `mips-dec-ultrix4.2` 
* cpu-company: 'ppc-ibm' for `powerpc-ibm-aix` 
* cpu-os: 'ppc-linux' for `powerpc-unknown-linux-gnu` 
* vendor-os: 'amiga-os' for `m6``8k-cbm-amigaos` 
* kernel-os: ??? the documentation says this, but I can't find any examples 
The `IAPAT` initializer will canonicalize its parameters in a way similar to `config.sub`.  The proposal is that `IAPAT` will allow zero through four non-keyword arguments, interpreted as described here (assuming the GNU conventions for now): 

* Zero arguments: equivalent to an argument of `'--host'` 
* One argument: a string from one of these possible ranges: 
   * `'--build'`, `'--host'`, or `'--target'` interpreted by the GNU convention above 
   * A SCons platform identifier (defaulted appropriately) 
   * maybe some autoconf aliases if they're popular 
   * name-name: proceed as if it were two arguments. 
   * cpu-vendor-os: proceed as if it were three arguments 
   * cpu-vendor-kernel-os: proceed as if it were four arguments 
* Two arguments: A GNU alias identifying a configuration 
* Three arguments: A GNU (cpu,vendor,os) triple identifying a configuration 
* Four arguments: A GNU (cpu,vendor,kernel,os) quadruple identifying a configuration 
In all cases, the result is expanded into a SCons platform ID (for backward compatibility), a CPU, a vendor, a kernel, and an OS, all canonicalized.  The specification for this process is convoluted enough that it deserves a specification page of its own, but I believe it can be done, and probably do a better job than `config.sub` does. 

The results are made available to the environment (((under discussion: as environment variables named `PLATFORM`, `PLATFORM_CPU`, `PLATFORM_VENDOR`, `PLATFORM_KERNEL`, and `PLATFORM_OS`???))).  In addition to these values, the initialization will determine these platform-specific values: 

* The default tools: see below. 
* The default shell PATH 
* Prefix/suffix for programs 
* Prefix/suffix for binaries 
* Prefix/suffix for static libraries 
* Prefix/suffix for shared libraries 
* Prefix/suffix for loadable libraries 
* (other prefixes/suffixes???) 
* Cross-compiler prefix (or empty if not cross-compiling) 

## Default IAPAT

The default `IAPAT` is accessed via a `DefaultInformationAboutPlatformAndTools()` factory function that implements the "singleton" pattern.  The default `IAPAT` may be used in much the same way that a `IAPAT` created by a user:   
`    iapat = DefaultInformationAboutPlatformAndTools('--target')`   
`    iapat.Toolchain('LEX', 'YACC', 'CC')`   
`    DefaultInformationAboutPlatformAndTools().Toolchain('PDF')`   
`    DefaultInformationAboutPlatformAndTools(toolchains = 'Jar')`   
`    DefaultInformationAboutPlatformAndTools(FOO = 'BAR')` 

There are some additional rules on the default `IAPAT` (((enforced by the factory function?  by making the default `IAPAT` a derived class?))): 

* Platform-configuration parameter(s) can only be used on the first call. 
* The default platform-configuration parameter is `'--build'` rather than `'--host'`. 
* (((others???))) 

## Backward Compatibility

Backward compatibility is provided by the default `IAPAT`.  It configures the local machine, provides the expected variables, and the correct per-platform toolchains.  xxx 

<a name="options"></a> 
# Per-invocation variations

xxx *Option() methods, command-line construction variables, and saved argument files 

<a name="tools"></a> 
# Toolchains

xxx ttt 
## Requirements

* (mostly) Be backward compatible 
* Adequate performance 
* (./) Determine if the tool is present 
* (./) Select one tool if multiple are present 
* (./) Do cross-compilation 
* Optionally retain configuration across invocations 
* Tool configuration from "external" information 
* (./) General compatibility with autoconf 
* (./) Select the default tools (if not overridden) 
* (./) Autodetect tools if no manual selection 
* (./) Command-line overrides of CC, CFLAGS, et.al.? 
* (partial) Be able to change the set of default tools 
* (partial) Extensible to new tools 
* Be interrogatable for what was selected 

## Synopsis

ttt 


## ttt

<a name="config"></a> 
# Per-machine configuration

xxx configure contexts 



---

 


# Previous draft still being mined for content

The overall objective is to allow a SCons users more control over the tools they configure.  It's intimately tied up with configuration of the platform, since many of the decisions about the right tool are predicated on which platform is selected. 

This description starts with a series of overall requirements, then discusses first platform configuration and then tool configuration.  The description continues with a discussion of the flow within a typical SCons Tool, since it differs slightly from the existing technique.  The description ends with a section on backward compatibility. 

(_Comment: As I was writing this page, I found myself flipping back and forth as to whether a Tool module configured a tool (that is, a single command) or a toolchain (that is, a series of commands).  The current Tool modules actually implement toolchains (e.g., the gcc.py module provides the environment variables for the compiler, the linker, the static archiver, the shared archiver, and the bundle archiver).  This isn't good modularization, which suggests that there should be a higher-level module explicitly for toolchains that can invoke one or more tool modules as building blocks.  That isn't in this proposal (should it be?), but it's something that should be kept in mind for the future._) 


### Overall requirements

This is a set of goals that new scheme must achieve to be viable.  It's a checklist, with the things I think are taken care of checked off.  Some goals are stronger requirements than others.  Consider them the holy grail, always sought after, never achieved: 

* (mostly) Be backward compatible 
* Adequate performance 
* (./) Determine if the tool is present 
* (./) Select one tool if multiple are present 
* (./) Do cross-compilation 
* Optionally retain configuration across invocations 
* Tool configuration from "external" information 
* (./) Some compatibility with autoconf 
* (./) Select the default tools (if not overridden) 
* (./) Autodetect tools if no manual selection 
* (./) Process --build, --host, --target on command line 
* (./) Command-line overrides of CC, CFLAGS, et.al.? 
* (partial) Be able to change the set of default tools 
* (partial) Extensible to new tools 
* Be interrogatable for what was selected 

### General flow

I'm going to invent unusable names below, mostly so they'll have to be changed before implementing them.  Inventing good names is not one of my skills; I'll leave that to others who have a better imagination than I do. 

Moreover, I don't claim a new class is the best way to implement this enhancement; it's likely that it can all be combined in an existing class (configure context comes to mind...). 

An InformationAboutPlatformAndTools instance is passed to the Environment constructor, which uses the configured platform and tools for its operations.  (If no tools are configured when the instance is passed to the Environment, a default set of tools is configured at that time.) 


### Platform configuration

The SCons scheme is adequate for limited cases of cross-compiling (a win32 program on mingw, for example) but is inadequate for more complicated cases (a Sparc SunOS program on a PPC Mac).  A scheme that will be simple for the simple cases yet flexible enough for the complex cases is not easy to do.  The complete description is complicated enough to require a separate specification to get all the details right, but I believe that it can be done. 

We also postulate that the InformationAboutPlatformAndTools initializer will canonicalize input values (similar to `config.sub`, but not as extensive), so a CPU of `ppc` is converted to `powerpc`, for example.  It takes zero, one, three, or four arguments: 

The InformationAboutPlatformAndTools initializer converts the input value(s) into a set of output values.  It's probable that not all of them should be calculated every time; some of them would be calculated on demand.  _Comment: the idea is that this would make it easier for configuration routines to generate their definitions, but it's just as logical that the calculation could be done in the configure routine that needs them.  It's an interesting trade-off._ 

The selection above is intended to be a bit controversial.  Almost certainly there are other things that should be present.  Discussion is welcome. 


### Tool configuration

Once the InformationAboutPlatformAndTools instance has been initialized with the platform information, tools can be configured. 

Again, there's a tension between the GNU tool configuration, which is based on the name of the command, and the SCons tool configuration, which is based on the name of a module that sets up the information (environment variables) for the tool.  The former is easier for a user to understand, but it requires that the knowledge of all possible command names be hard-wired into the configure macros; the latter requires that a list of module names be consulted when specifying the tool selection order.  Each scheme has its strengths and weaknesses. 

We propose a flow in the next section below that combines the two methods.  I'd like to say that it combines the strengths, but others will probably suggest that it compounds the weaknesses.  It requires that the Tool modules be extended (additional entry points will be required), but I'm pretty sure it won't affect backward compatibility. 

This is a very concrete description, far more detailed than a model or specification usually is.  Although I think it would work, I'm not wed to it, so feel free to suggest alternatives. 

Tool configuration is achieved by processing a list of tool IDs.  (A _tool ID_ is a string identifying what processing should be done.)  Processing is done by (recursively) mapping the tool IDs through a dictionary to produce (usually) module names.  The mapping is via a dictionary that maps a tool ID to a list of strings that are to be processed further. 

When examining a tool ID, it may be one of four things: 

* A tool list in the dictionary of tools.  A list may return one of three states: exists, non-existent, or error.  If a list returns error, calling lists also return the error.  A tool list may be one of four(?) types: 
      * An **optional** tool list; it's OK if an ID in the list does not exist.  _(Comment: Optional lists probably can only be usefully used in optional lists.  Anybody disagree?  If so, it may be possible to optimize this case.)_  The list returns success even if elements are non-existent. 
      * A **toolchain** where all of the IDs in the list must exist or the entire list is treated as non-existent. 
      * An **alternative** list of tools where the first ID that exists is selected; if none exists, returns non-existent. 
      * An **singleton** list of IDs where the first one that exists is selected; if none exists, it's an error. 
* A **two-tuple**, where the second element is a dict containing keyword arguments and the first element is either a callable or a module name (see below).  The keyword arguments are saved so they can be passed to the callable or to the module's generate() method. 
* A **callable** function or class, that is, something that can be called. 
* A **module** name (a string containing the name of a Python file in the toolpath); the detect() method of the module is asked if the tool exists. 
Callables and modules are not evaluated when they are encountered; they are accumulated in a list.  Only if the top-level list expansion exists is the list evaluated. 


### Default Tools

In addition to the dictionary of tool IDs (which we will assume is called `p.tool`, where `p` is an instantiated `IAPAT`), there is a list of default tools that are configured if nothing is configured specifically.  (If one tool is configured, all of them must be.)  We will assume this list is called `p.tools` although it could just as well be `p.tool['default']` by convention. 

Here's a simple example of part of what would be set up for IRIX:   
`      p.tools = ['any', 'STDtoolchain', ... ]`   
`      p.tool['STDtoolchain'] = ['any', 'SGItoolchain', 'GNUtoolchain']`   
`      p.tool['SGItoolchain'] = ['all', 'sgicc', 'sgic++', 'FC', 'sgilink']`   
`      p.tool['GNUtoolchain'] = ['all', 'gcc', 'g++', 'FC', 'gnulink']`   
`      p.tool['FC'] = ['any', 'f95', 'f90', 'f77', 'g77', 'fortran']`   
`      ...`   
The default set of tools can be adjusted, including replacing them whole cloth, by changing `p.tools`.  New tools are created just by adding an entry in `p.tool`.  The order of tool selection can be modified by changing `p.tool['CC']`, for example.  Normally, a missing toolchain is ignored, but it can be made mandatory by setting the first element of the list to `'one'`:   
`      p.tool['FC'][0] = 'one'`   
to require a FORTRAN compiler to be present, for example.   
(_Comment: this is still not fully baked and may change as it is worked out more carefully._) 


### Command Variables

The _command variable_ is the environment variable that specifies the command on the command line.  Here is a set of potential command variable names, based on the tools supported by GNU.  Autoconf has been around a while, so it's probably pretty comprehensive in this regard.  (And I probably missed some!)  (TODO: Support for other configure macros that set the command variable as a side-effect of selecting a particular mode for a tool.) 

* Compilers 
   * Assembler: AS (system assembler) 
   * C: CPP (C preprocessor), CC (C compiler) 
         * TODO: STDC (standard C enforced), C89 ('89 standard enforced), C99 ('99 standard enforced), GCCTraditional (GNU C with --traditional flag) 
         * TODO: CC_C_O (-c and -o, may not be needed), CppWerror (???) 
   * C++: CXXCPP (C++ preprocessor), CXX (C++ compiler) 
         * TODO: !Cxx_C_O (-c and -o, may not be needed) 
   * Object C: OBJCPP (object C preprocessor), OBJC (object C compiler) 
   * Erlang: ERL (erlang interpreter), ERLC (erlang compiler) 
   * Fortran: FC (FORTRAN), F77 (FORTRAN 77) 
   * Java: JAVAC (java compiler), (others? jar, javah, etc.) 
   * Linker: ??? LINK may be compiler-specific? 
   * Lisp: LISP (lisp) 
   * Perl: PERL (perl) 
   * Python: PYTHON (python, could be internal?) 
* Utilities 
   * Ar: AR (static library archiver) 
   * Awk: AWK (may not be needed) 
   * Grep: GREP (probably not needed), EGREP (ditto), FGREP (ditto) 
   * Install: INSTALL (install, may not be needed) 
   * Lex/yacc: LEX (lex/flex), YACC (yacc/bison) 
   * Ranlib: RANLIB (ranlib) 
   * Sed: SED (sed, may not be needed) 
   * TeX: ??? (TeX, LaTeX, ...) 
   * TODO: ProgMkdirP (pave path, probably not needed), ProgLnS (symlink, probably not needed) [[!table header="no" class="mointable" data="""
For comparison, this table shows command variables and the existing SCons Tools that set them up:||
AS | 386asm as gas masm nasm
CC | aixcc bcc32 cc gcc hpcc icc icl intelc* mingw* msvc* mwcc* sgicc suncc
CXX | aixc++ c++ g++ hpc++ sgic++ sunc++
DC | dmd
FORTRAN | aixf77 cvf f77 f90 f95 fortran g77 ifl ifort
LINK | aixlink gnulink hplink ilink ilink32 link linkloc mslink mwld sgilink sunlink
AR | ar mslib sgiar sunar tlib
* Sets up both CC and CXX.||
||
In addition, each of these Tools sets up a command variable that is the upper case of its name:||
Java | jar javac javah
TeX | dvipdf dvips gs latex pdflatex pdftex tex
parse | lex yacc
macros | m4
GUI | qt
FFI | swig
package | tar zip
??? | midl msvs rmic rpcgen
"""]]

The configured platform and set of tools is passed to an Environment when it is instantiated.  The values set up by the platform and tools are copied (??? maybe there's a more efficient scheme ???) into the Environment instance, and off we go. 


### Typical Tool Processing

_(See note above about not yet knowing which of these subsections I like best.)_ 


#### Processing III

The essence of the merged flow between SCons and GNU is handled when the Tool module is processed.  It's more complex than this sketch covers, but let's focus on the differences and worry about the other details later.  Moreover, this short outline doesn't distinguish between what's done by the code in the Tool module and what's handled by the infrastructure.  Here's a review of the things that Tool processing must resolve: 

* Choose the appropriate module if the command variable is set. 
* Determine if a tool is present. 
* Deal with cross-compilation 
* Set up the tool environment variables. 
* Set up the Builder method(s) for the tool. 
* Have reasonable performance. 
* Be backward compatible 
* ??? more? 
Optimization: I can imagine that the higher-level `IAPAT` logic may end up considering a given Tool several times before settling on the Tools to configure.  It's likely that caching the results of the tool's cogitations may be a significant speedup.  There are other things that should be cached as well: the GNU C Tool runs the compiler to determine the version and there's no need to do that more than once (per full path name of the compiler).  And the probe for executables is likely to be repeated in different `IAPAT`s, so that could be cached. 

exists/generate v. detect/apply 

Currently, the Tool module is probed when it is encountered to see if the tool exists.  That testing needs to be extended to detect if the command variable is present and if the command name is one recognized by the module. 

The command variable may be a space-separated list (think of `LEX='lex flex'`).  In this case, the command names must be tried in succession and the first match chosen.  We'll need a convention to deal with spaces in a command name; maybe it should be cracked with shlex(). 

(((TODO: It's not immediately obvious what to do if the command name is recognized but the command doesn't exist, or if multiple modules recognize the tool name.  This is the least-baked portion of this proposal; there will need to be a lot of detail resolved before it can be implemented.))) 

Not all tools are cross-compilers, so only some tools will need to do anything about it.  At the risk of oversimplifying, Tools that support cross-compiling need to apply the appropriate cross-compile prefix (and suffix?) to their command name(s) when detecting if the tool exists and when constructing command lines.  Otherwise, there's little the Tool modules themselves need to do to support cross-compiling (most of the pain is elsewhere). 

Tool setup is in two stages.  The first stage is when the tool is configured into the `IAPAT`.  The second stage is when the `IAPAT` is applied to an Environment.  The first stage is only done once, while the second stage may take place any number of times.  The idea is to make the second stage as fast as possible, so the trade-off will be to get as much as possible done during the first stage. 

During the first stage, variables are set in the `IAPAT`.  (Note that the override variables for an `IAPAT` are distinct from the environment variables, so the Tool module will always be able to set the environment variables intelligently.)  Probably iapat['BUILDERS'] should be filled in, but there may be no need to set up the Builder methods.  There doesn't appear to be much else done by Tool modules; anything else should be considered on a case-by-case basis. 

During the second stage, environment variables are copied to the new Environment and Builders are set up.  There may be other tool-specific initialization behavior that will have to be considered on a case-by-case basis.  (The strategy I would recommend would be that Tool modules could nominate a function to be run during phase two.) 

In general, a Tool module sets up one or more command variables.  Unlike the current semantics, where the last Tool configured is the winner and sets up its construction variables, the new semantics should be that the first Tool configured for a given command variable should be the winner.  Probably the easiest way to do this is for the `IAPAT` to keep a list of configured command variables and for each Tool to check the list to see if it should configure a given variable. 

If there's no override for the command variable (or if it's empty), the processing is very similar to the existing SCons machinery.  The `exists()` method of the module is probed to see if the tool should be configured; these methods would have to be enhanced to detect if the command variable has already been configured.  If it hasn't been, the method should determine the command name by checking to see if it exists in the PATH and return the name.  (This is what most of them already return; it's not much of a leap to require it in all cases.) [Note: cross-compile] [Note: return value] 

If the command variable is overridden, it's a space-separated list of command names.  (This usage is not common, but autoconf supports it for things like `LEX='lex flex'`.)  In this case, the `exists()` method must check each name in the list against the names it recognizes.  If it recognizes a name, it should return that name.  [Note: cross-compile] [Note: return value] 

[cross-compile]: Tools that support cross-compiling must deal with the cross-compiling prefix and suffix.  When generating names, they must add the prefix and suffix to the name they use; when recognizing names, they must strip the prefix and suffix (if it exists) before checking to see if it's a name they know. 

[return value]: A possible alternative is that the `exists()` method return a bound function (or wrapper of some kind) that will generate the environment variables for the specified command name, but this is an implementation detail of the API that should be worked out later. 

xxxxxxxxxxxxxxxxxx TODO: got to here 

If the command variable is overridden, it's a space-separated list of command names (not common, but think of `LEX='lex flex'`).  Each name in the list is tried in turn to see if it exists in the PATH using the module's `cross_compile_prefix` member to know if the prefix should be applied.  (Since I anticipate that this scan will be employed heavily, the result should be cached.)  If none of the names are found, the method returns failure. 

If a valid command is found, the module is asked if it recognizes the root name.  If it doesn't, the method returns failure.  Otherwise, an object is returned wrapping the object that will cause that command name to be generated when requested. 

This requires five changes to each Tool module: 

* A `command_variable` member variable giving the name of the (primary) command variable being configured. 
* A `cross_compile_prefix` member variable set to either `True` or `False` that specifies if a prefix should be added to the name if cross-compiling. 
* A `recognize()` method that returns `True` if the root of the command name is one that the module knows how to handle. 
* The `exists()` method may need to be modified to return the command name and to use the cross-compile prefix if necessary. 
* The `generate()` method may need to be modified to apply overrides present in its input keywords. 
In these examples, we're going to assume a Tool module named `'xxx'` whose `command_variable` is `'XXX'` and which sets up a context variable named `XXXFLAGS`: 

* `ApplyModule('xxx', XXXFLAGS = '-yyy')` configures the `XXX` command variable and sets the XXXFLAGS context variable to '-yyy'. 
* `ApplyAlternates('xxx', 'fail', XXXFLAGS = '-yyy')` is the same as the previous one except that an error will be thrown if the tool isn't found. 
* `ApplyAlternates('my_xxx', 'xxx', XXXFLAGS = '-zzz')` tries to configure the `XXX` command variable first with module `'my_xxx'` and then with module `'xxx'` if the first fails; the XXXFLAGS environment variable is set to '-zzz'. 
* `ApplyModule('xxx', XXX = 'my-xxx xxx')` configures the `XXX` command variable, trying for a command named 'my-xxx' and then 'xxx'.  XXXFLAGS is initialized to the default.  The interesting thing about this example is that the prefix of `'my-'` will be stripped off the command name when asking the modules if they recognize the command name. 
* `ApplyModule('xxx', **ARGUMENTS)` configures `XXX` and `XXXFLAGS` using overrides from the command line.  A module only checks for keywords that it knows, so excess keywords are ignored. 

#### Processing II

The essence of the merged flow between SCons and GNU configure is in the `ApplyModule` method.  (The flow for the other `Apply`* methods is more complex than suggested above as well, but let's focus on `ApplyModule` here and worry about the others later.) 

The command variable that this module sets up is defined by the `command_variable` member of the module; it is set when the module is initialized.  To avoid setting up the command multiple times, the command variable is checked to see if it's already in the context.  If it is, we just return success. 

If there's no override for the command variable (or if it is empty), it's very similar to the existing SCons scheme.  The `exists()` method in the module is probed to find the tool's command name if it exists (this is what most of them already return; it's not much of a leap to require it in all cases).  If the command doesn't exist, failure is returned; otherwise, a wrapper around the module is returned that will generate context variables for the specified command name. 

If the command variable is overridden, it's a space-separated list of command names (not common, but think of `LEX='lex flex'`).  Each name in the list is tried in turn to see if it exists in the PATH using the module's `cross_compile_prefix` member to know if the prefix should be applied.  (Since I anticipate that this scan will be employed heavily, the result should be cached.)  If none of the names are found, the method returns failure. 

If a valid command is found, the module is asked if it recognizes the root name.  If it doesn't, the method returns failure.  Otherwise, an object is returned wrapping the object that will cause that command name to be generated when requested. 

This requires five changes to each Tool module: 

* A `command_variable` member variable giving the name of the (primary) command variable being configured. 
* A `cross_compile_prefix` member variable set to either `True` or `False` that specifies if a prefix should be added to the name if cross-compiling. 
* A `recognize()` method that returns `True` if the root of the command name is one that the module knows how to handle. 
* The `exists()` method may need to be modified to return the command name and to use the cross-compile prefix if necessary. 
* The `generate()` method may need to be modified to apply overrides present in its input keywords. 
In these examples, we're going to assume a Tool module named `'xxx'` whose `command_variable` is `'XXX'` and which sets up a context variable named `XXXFLAGS`: 

* `ApplyModule('xxx', XXXFLAGS = '-yyy')` configures the `XXX` command variable and sets the XXXFLAGS context variable to '-yyy'. 
* `ApplyAlternates('xxx', 'fail', XXXFLAGS = '-yyy')` is the same as the previous one except that an error will be thrown if the tool isn't found. 
* `ApplyAlternates('my_xxx', 'xxx', XXXFLAGS = '-zzz')` tries to configure the `XXX` command variable first with module `'my_xxx'` and then with module `'xxx'` if the first fails; the XXXFLAGS environment variable is set to '-zzz'. 
* `ApplyModule('xxx', XXX = 'my-xxx xxx')` configures the `XXX` command variable, trying for a command named 'my-xxx' and then 'xxx'.  XXXFLAGS is initialized to the default.  The interesting thing about this example is that the prefix of `'my-'` will be stripped off the command name when asking the modules if they recognize the command name. 
* `ApplyModule('xxx', **ARGUMENTS)` configures `XXX` and `XXXFLAGS` using overrides from the command line.  A module only checks for keywords that it knows, so excess keywords are ignored. 

#### Original processing

In this section, we're going to consider configuring a tool named `'xxx'` whose command variable is `'XXX'` and which sets up an environment variable named `XXXFLAGS` to contain its command-line flags.  Not all of the logic described here would go in a tool module; some of it would be contained in the higher-level logic described above. 

Let's look at what a tool module must do: 

* If the tool has already been configured, don't do it again. 
* Make no changes until told to do so. 
* If the tool name is overridden by the user, it must respect that. 
* xxx to be finished 
Let's consider what has to be done to configure the `'xxx'` tool. 

If the _command variable_ (`XXX` in our example) is present as a keyword, it contains a space-separated list of names (think of `LEX='lex flex'`).  (If a list is given, that should work, too.)  This list overrides the normal list otherwise used. 

If the command name is not overridden, then each module is tried in turn.  The module knows the command name(s) that should be tried.  Each name is tried in turn, and if one is found, the module is used to configure the tool. 

If the command name has been overridden, each name is checked to see if it is in the PATH.  If it is, each module is polled to see if it recognizes the name.  If a match is found, that module is used to configure the tool, otherwise a generic configuration is used. 

If the tool compiles to binary code, the cross-compile prefix is prepended to the name when searching the PATH and setting the command variable.  (The GNU convention is that cross-compilers have a prefix similar to the canonical name in front of the command name.) 

If the tool cannot be configured, an exception is raised.  (??? or return an error? ???) 

Examples: 

* `ConfigureSeriesOfToolchains('XXX', XXXFLAGS = '-yyy')` configures `xxx` using the default set of modules for the toolchain and sets the XXXFLAGS environment variable to '-yyy'. 
* `ConfigureToolFromListOfModules('my_xxx', 'xxx', XXXFLAGS = '-zzz')` tries to configure `xxx` first with module `'my_xxx'` and will use module `'xxx'` if it fails; the XXXFLAGS environment variable is set to '-zzz'. 
* `ConfigureSeriesOfToolchains('XXX', XXX = 'my-xxx xxx')` configures `xxx` trying for a command named 'my-xxx' and then 'xxx' using the default set of modules.  XXXFLAGS is initialized to the default.  The interesting thing about this example is that the prefix of `'my-'` will be stripped off the command name when asking the modules if they recognize the command name. 
* `ConfigureSeriesOfToolchains('C', 'CXX', **ARGUMENTS)` configures the C and C++ compilers using overrides from the command line.  A module only checks for keywords that it knows, so excess keywords are ignored. 

### Extensibility

The default toolchains can be changed by assigning a new list of toolchain names to the appropriate member in the platform configuration information. 

The default modules to examine for a toolchain can be changed by assigning a new list of module names to the appropriate index for that toolchain in the platform configuration information. 

The set of known toolchains can be extended by adding a list of module names to a new entry of the index of toolchains. 


### Backward compatibility

This proposal moves SCons much more toward the set of GNU canonical names.  Although the `--build` command-line option would default to the current SCons platform identifier, this has the risk of causing some subtle backward incompatibilities. 

If no InformationAboutPlatformAndTools instance is passed to the Environment constructor, a default is used.  This is somewhat different from way an Environment is currently instantiated, so it has the risk of causing some subtle backward incompatibilities. 

* The InformationAboutPlatformAndTools instance is initialized from the `platform=`_id_ keyword option if one is present, otherwise it is is initialized with `'--host'` so as to enable cross-compilation if specified on the command line. 
* If present, the `toolpath` keyword option affects the search path for modules.  I would make this a keyword option to the initializer to aid backward compatibility. 
* If the `tools` option is present, it short-circuits the default list of toolchains and causes the specified modules to be used instead.  I would make this a keyword option to the initializer to aid backward compatibility. 
* Initializer parameters cannot be mixed; if an `information_about_stuff=`_instance_ keyword parameter is used when instantiating an Environment, the `platform`, `toolpath`, and `tools` (and possibly `options` as well) keyword parameters cannot be present. 
* Generated InformationAboutPlatformAndTools instances are cached and reused if the same platform-tool-toolpath (PATH may have to be included as well) combination is repeated. 
For compatiblity with GNU autoconf, the default set of toolchains is configured with `**ARGUMENTS` for the keywords, so command-line overrides will be will be used during toolchain setup.  A SConscript that already uses an environment variable defined by a tool will perform differently. 

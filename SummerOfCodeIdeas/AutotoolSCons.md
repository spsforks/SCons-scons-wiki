

# Adding Autotools Features to SCons

GNU Autotools is a [series of programs](GregNoel/AutotoolSteps) to support portable applications.  Using it can be intellectually challenging, since changes to an input file may require several steps to be rerun.  Moreover, the implementation as interdependent programs means that communication between steps requires the creation of lots of little control files. 

We can do better. 

SCons already has configuration contexts.  Although not ideal, they are the mechanism that will be used during the 1.x releases.  Replacing configuration contexts, or otherwise breaking backward compatibility, is not an option until at least the 2.0 release. 

This page outlines a scheme of how Autotools-like functionality could work within the current SCons model, using configuration contexts, while still being flexible enough to adapt to a different scheme in the future.  It's not perfect and there are some warts, but a smoother implementation will probably require some backward incompatibilities, so complete support is probably a 2.0 feature. 

This is just the thinnest of outlines and a lot of detail needs to be added.  On the other hand, it's possible to hack out some pieces and implement them separately; the idea is that this would provide the skeleton upon which individual organs could be hung. 

This page goes through the functionality roughly in the same order as the features are present in the Autotools steps, not in the order in which it should be implemented, since the working of the earlier actions often depends on how the later actions are implemented. 


## Generate/update needed configuration

In the beginning, the user needs to generate the actions that do the configuration.  Since this phase involves user interaction, we will treat it as a separate program called `autoscons`, a horrible name that should be changed, and we will assume that the configuration information it is maintaining is in the `SConfigure` file (a Python script that is imported via an `SConscript()` function). 

There are several operations that could be part of `autoscons` which are considered below.  The could be implemented in discrete programs as `autotools` does, although a single program responsible for all user interaction seems simpler. 

We will assume that `autoscons` does its thing and produces its recommendations in the `SConfigure.scan` file, although it's possible in the long run that a GUI version could be created that updated the `SConfigure` file directly. 

The `autoscons` program should be built as an extensible framework around _experts_.  Each expert is responsible for collecting information about a specific area and then providing the necessary configuration tests. 

Initially, if the `SConfigure` already exists, `autoscons` reads the file to extract the tests already done.  I imagine that this information would be embedded in stereotyped comments or the like, but the idea is that the experts would be primed with information about what's already there. 

Then `autoscons` would walk the source tree looking for source files (identified by experts) and then scan each source file in the context of experts for that type of source.  Each expert looks for a particular portability issue and collects information about it. 

Experts would be able to: 

* Consult with one another: one expert may identify headers used, another expert may identify guards around header inclusion; the combination would lead to a header test that set the guard if it was (or was not) present. 
* Require that some other bit of knowledge is present when it performs its test, so that tests will be done in the correct order. 
* Specify what happens if its test results were ignored; the default would be to fail if not used. 
There would also be a set of _expert sinks_ that would consume the expert's information and perform some action.  They act as experts (at least to other experts), but don't produce any information that must be consumed. 

The `autoscons` program then prepares a set of recommendations and proposes them to the user in the `SConfigure.scan` file.  The user can then edit this, rename it to `SConfigure`, and repeat the process as needed. 


### Guessing tests

This section corresponds roughly to the `autoscan/ifnames` step. 

Experts would be needed to identify the type of each source file (and hence, the processor needed to build it).  The suffix should be the primary source, of course, but if the file is not otherwise recognized, one can imagine that the initial part of the file could be checked to see if it was recognizable. 

Information collected would include this data: 

* processors used (`cc`, `cpp`, `awk`, `sed`, `yacc`, `swig`, _et.al._) 
* preprocessor tokens 
* included files 
* libraries needed 
* various structures and typedefs 
* problematical library functions 
* other things I can't imagine 
Expert sinks would be available to achieve common results: 

* Add (or modify) something in the environment.  This would include adding defines to the command line. 
* Automatically provide specialized files.  I can imagine a program that includes `"sc_dirent.h"` and have the file automatically generated. 
* Other uses I can't imagine 

### Compiler characteristics

There are at least a dozen standard `autoconf` macros that determine various information about the C, C++, and FORTRAN compilers.  These need to be added to SCons. 

If an `autoscons` expert detects that one of these compilers is used, the expert should propose to perform these tests (defaulted to off) and allow the user to choose which ones are wanted. 


### Internationalization

This section corresponds roughly to the `autopoint` step. 

From the way that `autopoint` is documented, one can deduce that the way to access `gettext` varies with different releases.  There's no obvious documentation about how it changes, so it will require some research to find out. 

Once that is done, it will be possible to figure out what the `autoscons` expert in internationalization should recommend. 


### Exposing the configuration

This section corresponds roughly to the `autoheader` step. 

This is mostly done by expert sinks that perform different actions: 

* "Take this set of defines and put them in that header file" 
* "Put that set of defines on the command line" 
* "Snarf any defines not otherwise sunk and put them in config.h" 
* "Turn this (set of?) results into C++ traits in that file" 
In addition, the sink for a specific file should be able to modify its output based on additional information.  Look at the `AH_`* macros for inspiration. 


## Simplified build syntax

Like it or hate it, the Automake syntax is a well-understood way of specifying build steps.  It's easy to imagine an SCons version that acts like this: 


```python
#!python 
env.Automake("""
        bin_PROGRAMS = hello
        hello_SOURCES = hello.c version.c getopt.c getopt1.c
""")
```
This would generate all the actions necessary to build, install, package, and distribute the the program; the actions would be attached to an appropriate alias.  (It should probably also make the `all` alias the default.) 

Note that the SCons variant of the `automake` syntax would be simpler, since it doesn't need to statically specify everything.  For example, the header files needn't be declared in the SOURCES, since they can be picked up by Scons' dependency scanners. 

There's a licensing issue here: can `automake` be reimplemented under a different license?  I believe `automake` uses the GNU virus, while the SCons license is more liberal.  Instead of transliterating the Perl source, it may be necessary to do it in a clean-room environment, working from the language spec. 


## Standard macros

There are many dozens, perhaps hundreds, of standard `automake` and `autoconf` macros available.  Of these, only a dozen or so are implemented for SCons so far.  Some of them have no meaning without the Autotools infrastructure, but most of them have functionality that would be useful in SCons.  In the long run, SCons needs to offer at least the capability of `autotools`, so work on these is important. 

The first thing that needs to be done is to collect all the `autotool` macros and categorize them.  This initial breakdown is suggested by the autoconf info page (which covers AC_* macros, not AM_* macros): 

* Initialization and output 
* Variable substitution 
* Autoheader (templates and macros) 
* (Common behavior?) 
* Alternative programs (lex, yacc, awk, [ef]grep, ...) 
* Files 
* Libraries 
* Library functions 
* Header files 
* Declarations needed 
* Structures 
* Types 
* Compilers and preprocessor (sizeof) 
* System services 
* UNIX variants 
* Cross-compilation (see section below) 
* Command-line options and help (see section below) 
* Testing (Autotest) 
* Others 
The macros need to be further subdivided into: 

* implemented 
* unneeded 
* unimplemented 
(A [preliminary list](GregNoel/StandardMacros) is available, although the categorization into subdividions is not complete; it's interesting to see how little of the `autoconf` functionality has been implemented so far, let alone the full `autotools` functionality.) 

After the macros have been triaged, the unimplemented macros should be prioritized and the top N identified (where N is between ten and 25) to provide focus for working on them.  As macros are implemented, they are removed from the priority list (and moved to the implemented column), leaving room for new additions. 

Tests should instantiate themselves as uniquely-named DAG nodes so that they can be cached for reuse.  This interacts with the next section; read on. 


## Caching configuration results

Currently, each configure test is internally given a name that is effectively an integer sequence number.  If the same test is repeated (for example, if two different configuration contexts both check for `<math.h>`) then the test is re-run. 

Instead of a sequence number, the name of a configure test should be repeatibly generated from the values of its parameters.  For `<math.h>`, it might be something like `header.check.system.math.h` so that a repeated test will find the result already cached. 

Moreover, if the test executes a standard action (such as adding a value to an environment), that action should be part of the DAG so that it can be reused conveniently.  Note that this is recursive: an action named `define.have.math.h` might refer to `header.check.system.math.h`. 

Assuming that the priority list of the previous section is set up, these modifications should be on the initial list. 

* (Future direction: note that this mechanism makes it easy for a `config.h` node be dependent upon a `define.have.math.h` node, which would cause the file to be automatically regenerated if something changed.) 

## Command-line options

When the command line is evaluated, unrecognized options beginning with a double dash are marked.  If a _defining instance_ of the option (see "Help text" below for a definition) is encountered during processing, the mark is removed.  At the end of reading the input, any marked options cause an error message to be generated. 

* _(Note that how the error message is presented is critical to acceptance; rather than "Unrecognized option" with the implication that it should have been noticed immediately, it should say something like "Option never defined during processing; check the spelling.")_ 
Double-dash command line options can have internal dashes.  The dashes are converted into underscores before placing them in the construction environment.  Thus, `--enable-foo` becomes an value named `enable_foo` in the construction environment and the `--exec-prefix` could be accessed in a generated command as `$exec_prefix`.  (See also the section below on untangling various features for more on this.)  (Question: should the dashes be converted to underscores prior to matching, so `--exec_prefix` would also be recognized?  A `configure` script does this inconsistently; some options are recognized, and some are not.) 

The set of known command-line options should be extended to include these; they are the options supported by `configure` (plus `--fakeroot` to support RPM and Debian build notions). 
[[!table header="no" class="mointable" data="""
--prefix=PREFIX  | install architecture-independent files in PREFIX [/usr/local] 
--exec-prefix=EPREFIX  | install architecture-dependent files in EPREFIX [PREFIX] 
--bindir=DIR  | user executables [EPREFIX/bin] 
--sbindir=DIR  | system admin executables [EPREFIX/sbin] 
--libexecdir=DIR  | program executables [EPREFIX/libexec] 
--datadir=DIR  | read-only architecture-independent data [PREFIX/share] 
--sysconfdir=DIR  | read-only single-machine data [PREFIX/etc] 
--sharedstatedir=DIR  | modifiable architecture-independent data [PREFIX/com] 
--localstatedir=DIR  | modifiable single-machine data [PREFIX/var] 
--libdir=DIR  | object code libraries [EPREFIX/lib] 
--includedir=DIR  | C header files [PREFIX/include] 
--oldincludedir=DIR  | C header files for non-gcc [/usr/include] 
--infodir=DIR  | info documentation [PREFIX/info] 
--mandir=DIR  | man documentation [PREFIX/man] 
--fakeroot=DIR  | place the install tree relative to DIR [empty] 
--build=BUILD  | configure for building on BUILD [guessed] (unneeded?) 
--host=HOST  | cross-compile to build programs to run on HOST [BUILD] 
--target=TARGET  | programs should produce output for TARGET [HOST] 
--program-prefix=PREFIX  | prepend PREFIX to installed program names 
--program-suffix=SUFFIX  | append SUFFIX to installed program names 
--program-transform-name=PROGRAM  | run sed PROGRAM on installed program names 
"""]]

Only the last one is problematical.  It's a rarely-used feature, and maybe some other mechanism could be used. 


### Enable/Disable options

If a command-line option is encountered that begins `'--disable-'` then it is treated as if it were an enable with the value `'no'`.  That is, `--disable-foo` is turned into `--enable-foo=no` and any value is ignored. 

For each such option, SCons knows three things: 

* the state: 'yes' or 'no' 
* the default: e.g., '/usr/local/bin' 
* the current value: e.g., '$HOME/bin' 
If the option is not present on the command line, the _state_ value is chosen; otherwise, if the command-line option has  a value, that is chosen; otherwise, `'yes'` is chosen.  If this value is `'yes'`, then the _default_ is selected.  (The _default_ is set to `'yes'` if not set to something else.)  The result is that `--enable-foo` without a parameter can be set to something reasonable without special programming.  A possible prototype: 
EnableOption(key, [help, initial, default])
: 
Return a tuple of arguments to set up an enable/disable option that will use a name of `enable_`_key_, have a state of _state_, have a default value of _default_, and display the specified _help_ text.  The _initial_ parameter must be either **yes** or **no**; if it is not present, it is set to **no**.  The option will treat the values **y**, **yes**, **t**, **true**, **1**, **on** and **all** as **yes**, and the values **n**, **no**, **f**, **false**, **0**, **off** and **none** as **no**.  If the _default_ value is not given, it is set to **yes**. 




### With/Without options

The processing of the with/without options is the same as the processing for the enable/disable options, except that `--without-foo` is converted to `--with-foo=no`. 


### Other user-defined options

Most other user options are specified with the `Add()` function; it recognizes that the option begins with a double-dash and does the right thing. 

One other option type is recognized: 
FlagOption(key, [help, default])
: 
Return a tuple of arguments to set up an option whose value is None if the option is not present, the _default_ if the option is present without a value, and the value if there is one.  The option will use the specified name _key_ and display the specified _help_ text.  It's only useful with a double-dash option.  For example: 




```python
#!python 
opts.FlagOption('--opt', 'Optimize', '-O')
```

### Cross-compilation

If the `--host` or `--target` command-line option is present, SCons enters cross-compilation mode.  (There is no `--build` option, as SCons always builds on the system where it is currently running.) 

TODO: what it does; replace config.guess and config.sub (I've never written a configure script that did cross-compiling, so my knowledge of what autoconf does is small.  Can anyone help?) 


### Help text

When a command-line option is declared with help text, that is called a _defining instance_ for that option.  There must be at least one defining instance of any option on the command line or it is an error. 

Unfortunately, help text is declared in an Option object.  An Option object is intended as a place to accumulate environment overrides when initializing an environment, so if different objects declare overlapping sets of parameters, help text may be declared multiple times.  Since the help text for a given Option object is added to the global help message as a group, there's no way to coordinate help text for an individual parameter. 

So there should be a way of accumulating the help text on a per-option basis.  If there are multiple defining instances, the text is merged with some smarts (i.e., duplicate texts are combined). 

See the next section. 


## Untangling parameters, help, options, and configure

Command-line parameters are global.  That's pretty obvious, but it means that information about them needs to be global as well.  A parameter value may be consumed many times (with different interpretations), but parameter information should be manipulated on a global basis. 

In particular, help text should be accumulated globally.  If there are multiple definitions of a parameter, the help text should be accumulated intelligently, by merging duplicate copies.  The help subsystem should do its best to organize and lay out the options (the `configure` help display is a good model), but there also should be ways to influence its behavior (accumulate some of the options into a separate subsection, for example).  The default version should be reasonably intelligent, so there's not a lot of temptation to replace it. 

The Option object wants to provide values to an environment, but it's limited in the things it can initialize (for reasons obvious later, the list of tools comes to mind). 

A Configure context accumulates values to modify an environment, but these values have to be exported individually to each construction environment using them. 

Moreover, an Environment object is basically a huge number of operations built around manipulating a construction environment (which is really the only thing needed when constructing a command to be executed). 

Looking at this, the unifying thread among these objects is that they  want to manipulate construction variables.  Maybe the thing to do is expose construction variables in an object that allows them to be inexpensively composed.  This object would then either be a base class (IsA) or a member variable (HasA) of the Configure context, the Option object, and the Environment object (and maybe more; I can believe that the help generator could substitute values into the output it was displaying). 

For the sake of discussion, I'll call this class a Namespace and hope somebody picks a better name if it gets implemented.  It's basically a [SubstitutionEnvironment](SubstitutionEnvironment) with the dross pulled out and some functionality added.  For example, if a value lookup fails in the local Namespace, it should check for the value in a list of alternative Namespaces. 

Configure objects no longer need an Environment to construct commands; all they really need is the Namespace.  (There would be some fiddling to create and manipulate nodes that would have to come from someplace, but that can be worked out.)  If a Configure context configures a tool, it marks that in the Namespace, which would cause any Environment initializing from it to skip its own configuration and use the provided information. 

The Environment constructor is modified so that the 'options=' parameter can take a list of Namespaces, which is used to initialize the source list in its Namespace; no copying is needed to include them.  The same Configure context or Option object can be used in multiple Environments without having to copy the values multiple times. 

There's a lot of detail missing here (distinguishing between 'update' access and 'readonly' access is one), but I hope this sketch is enough to show how it would work. 


## Cheap environment modifications

A common paradigm is for a configure test to make some incremental changes to an environment and run a test in that environment.  After the test, the environment may need to be restored.  This can be error-prone, so a simple way to do this would be a boon. 

TODO: Maybe a function of the configure context?  Maybe related to previous section? 


## Re-architecture Tools

Currently, SCons uses a set of Python modules called _Tools_ to configure an environment.  These tools pre-date the introduction of the configure context, so they use a hard-wired internal `exists()` method to decide if a given utility is installed on the local system. 

The idea here is that if some tool is configured, the Tool should use the configuration information instead of some built-in logic.  The problem is that tools are currently set up when the environment is created, while the configure context isn't set up until later.  Since backward compatibility is an issue, some clever thinking and a lot of design work will be needed to merge the two mechanisms. 

One possible strategy would be to pass a configuration context to the Environment() constructor, but this begs the question of how to pick out the configured variables.  Another possibility would be for a configuration context to modify an option object; the option object could then be passed to the Environment constructor.  But all of this is awkward; there's got to be a cleaner way. 

This issue needs to be thrashed out and a choice made for an API moving forward. 

---

 
### Fix Bugs

As with all projects, bugs and requests for enhancements and new features accumulate. Many of them only involve a couple of weeks worth of effort, but the primary developers are busy enough that there's just not enough time to get to them. Dealing with a few small bugs, a couple of medium enhancements, or a single large new feature (and including tests and documentation) is a tremendous way for inexperienced programmers to get their feet wet, gain experience, and sharpen your Python skills. 

The idea here is to choose a reasonable set of bugs to tackle: not too hard and not too easy. You can get advice from the mailing list as to the difficulty of various bugs, but judging how long it will take to do a task is one of the skills that young programmers must develop. 

The issues database contains the [list of defects](http://scons.tigris.org/issues/buglist.cgi?Submit+query=Submit+query&issue_type=DEFECT&component=scons&subcomponent=scons&issue_status=NEW&issue_status=STARTED&issue_status=REOPENED&target_milestone=-unspecified-&order='Importance') that would be the starting place to look for bugs to fix. It also contains the [requests for enhancement and new features](http://scons.tigris.org/issues/buglist.cgi?Submit+query=Submit+query&issue_type=ENHANCEMENT&issue_type=FEATURE&component=scons&subcomponent=scons&issue_status=NEW&issue_status=STARTED&issue_status=REOPENED&target_milestone=-unspecified-&order='Importance') that can also be mined for potential ideas. 

Mentor(s): [StevenKnight](StevenKnight), [GaryOberbrunner](GaryOberbrunner), others 



---

 
### Simpler Interface for "Simple" Builds

The attraction of systems like [CMake](http://www.cmake.org/HTML/Documentation.html) and [GNU automake](http://sources.redhat.com/automake/automake.html) is that they provide a very simple interface (parseable as a Python script) that handles a wide number of typical builds.  The idea is to design and implement an interface that is as simple as CMake and `automake` for the kinds of tasks they handle, while still allowing the full power of SCons for the tasks that they don't handle well. 

A prior project has provided a great deal of the `automake` functionality for SCons.  Although it is useful, the interface is not simple.  One approach to this task would be to take that implementation and extend it with a very simple interface. 

This task requires skills in language synthesis and language design, plus the ability to conceal unnecessary complexity behind a simple façade.  The interface should "just work" for a wide range of common tasks, keeping the implementation details out of sight. 

Mentor(s): [GregNoel](GregNoel), possibly [StevenKnight](StevenKnight) 



---

 
### New Builders


#### SubstInFile() Builder

This is a builder that takes a file containing a template and fills it in using a dictionary of names and values. There's a starting implementation in [SubstInFileBuilder](SubstInFileBuilder). This project would turn that into the be-all end-all of template builders. Here's some ideas for how it could be better: 

* Currently it just does simple value substitution; it could do full Python expression substitution (although that may be overkill?). 
* It could take prefix/suffix arguments so template variables could look like %FOO% or $(FOO) or whatever people want. Handling parens like this means maybe handling nested parens in the expressions. Even should allow for no prefix/suffix. 
* It should be able to take a construction environment as the dictionary, so construction variables get expanded. This shouldn't be the default because it's a little unsafe (you never know what stuff might appear in an Environment in the future and break your build). 
* There could be a better interface for passing the substitution dict than just overriding SUBST_DICT; apply some creativity here! A Value node or something possibly? 
It also needs a test suite and documentation. There's some documentation in this wiki at [DeveloperGuide/TestingMethodology](DeveloperGuide/TestingMethodology). 

This is a reasonably-sized project, and well-contained so it should be very easy to integrate the result into the release with minimal disruption. It shouldn't take more than two or three weeks: a week for preparation (exploring ideas, specification, writing some tests), a week for implementation and testing, and a week for documentation and fixing bugs. 

Mentor(s): [GaryOberbrunner](GaryOberbrunner) 


#### Python Binary Builder

Surprisingly, SCons can't compile a Python source into a Python binary.  A builder that did this would be a useful addition.  This isn't enough of a project for a full summer's worth of work, but it could be combined with other small projects to fill up the summer. 

Mentor(s): probably [StevenKnight](StevenKnight), possibly [GregNoel](GregNoel) 


#### Other Builders

When converting a legacy build system, portions of it may well be written in another scripting language.  Instead of being forced to rewrite the scripts into Python, it would be simpler to continue to use them as they are.  Builders for Sed, Awk, Python, Perl, Lua, Ruby, and others would be a useful addition; see also Groovy under the [Java](GSoC2008) heading below. 

These are a bit different from other builders, in that not only do they have the typical target and sources, but they also have a script that must be executed.  This will probably require modifications to the core builder logic to deal with this. 

These are small projects, not enough individually to fill up a summer of coding, but they could be combined with other small projects. 

Mentor(s): probably [StevenKnight](StevenKnight), possibly [GregNoel](GregNoel) 



---

 
### Internationalization with Gettext

The `gettext` set of library functions allows a program to deal with internationalization (i18n) and localization (l10n) issues.  The entire suite contains functions to use a translation catalog to convert a string in one language into another and handle the various numeric and date formats.  Providing this support to programs being built would be very useful. 

GNU uses the `autopoint` command to determine the `getttext` infrastructure.  SCons will need a similar configuration step to determine exactly what it needs to do. 

SCons will need a builder for the `msgfmt` program, which compiles the catalogs into binary format, and possibly for other programs as well. 

This project will need someone who understands i18n, l10n, and the `gettext` model. 

Mentor(s): [GregNoel](GregNoel), [StevenKnight](StevenKnight) 



---

 
### Internationalization of SCons

SCons itself needs to be internationalized.  There's a Python `gettext` module to do the heavy lifting, but locating and marking all the strings that need to be translated, plus setting up the infrastructure to provide translations, is a lot of patient, detailed grunt work. 



---

 
### LIBOBJ Support

GNU `autoconf` can replace missing or broken library functions with versions that are locally compiled and included in a program.  It provides support for `alloca`, `error_if_line`, `getloadavg`, `lstat`, `malloc`, `memcmp`, `mktime`, `obstack`, `realloc`, `strtod`, `strnlen`, `fnmatch`, `fileblocks`, and probably others. 

It would not be a stretch to extend this facility to generating header files for specific circumstances; `dirent.h` comes to mind. 

SCons should have such a facility.  It's far more than a summer project to provide a framework and all the functions, not to mention the configure tests that determine if the replacement is needed, but establishing the framework and a few of the configure tests and corresponding functions should be well within scope. 

Mentor(s): [GregNoel](GregNoel), possibly [StevenKnight](StevenKnight) 



---

 
### Revamped Option Handling

SCons has three completely-independent mechanisms for providing variations in a build: 

* An Optik parser for command-line flags. This is a fine system, but it's not extensible to allow flags to be declared after the initial parse. 
* A home-grown parser for dealing with variable assignments on the command line and in files. It isn't bad and probably is a reasonable basis for expansion. 
* A `configure` subsystem that extracts information from the machine and operating system. It currently has only a few actions implemented, and its integration with other components isn't as smooth as one would like. 
All of them have in common that they convert external information into an internal form, so that user code (or even system code) can make decisions based on it. All of them have ways to validate the external information, change the shape of the external information into a more palatable internal form, make decisions based upon the values, and usually have the effect (or sometimes side-effect) of changing the values of variables in the construction environment. The first two also have in common that they want to provide help text to the user upon request. 

The idea here is to integrate the three mechanisms, or, at worst, integrate the first two and provide a foundation for the third. Ideally, it should be fully backward-compatible with the existing `Options()` functionality. 

There's been some discussion on the mailing list about this, and a (partial) specification is available. However, there are still a few points for which no consensus emerged; these would need to be resolved. The most likely way to tackle it would be to translate the single-character flags into their token equivalents as a special case so that all the later processing only has to deal with tokens. 

Mentor(s): Probably [GregNoel](GregNoel) 



---

 
### Smarter Treatment of Intermediate Targets

[bug #583](/SCons/scons/issues/583) is about implementing something similar to the .INTERMEDIATE and .SECONDARY special targets in GNU `make` (see the description in the [manual](http://www.gnu.org/software/make/manual/make.html#Chained-Rules)). A SECONDARY target is only built if it is needed by a downstream target that's being rebuilt. An INTERMEDIATE target is a SECONDARY that is automatically deleted once all downstream targets using it are successfully built. 

This idea will need four things to be implemented: 

* The Intermediate() and Secondary() functions to mark Nodes appropriately. 
* The logic to delete an intermediate target when the need for it is done. 
* The logic to figure out if a target is up-to-date even if intermediate or secondary targets are missing. 
* The logic to rebuild missing intermediate targets if a downstream target needs them. 
Mentor(s): [GregNoel](GregNoel) 



---

 
### Don't Rebuild if Only "Comments" Differ

If only the comments in a file change, there's no need to rebuild anything that depends on it. This can easily be accomplished by stripping out comments (and other extraneous content) when calculating the signature. [bug #193](/SCons/scons/issues/193) discusses this, including some tips for implementation, although the approach suggested there may not be adequate in all cases. 

The complication here is that the source for one tool could be comments for another.  For example, the C compiler and the Oxygen documentation system operate on the same files, but they have different ideas about what the significant content is.  Changing the documentation should not trigger the C compiler and changing the code should not trigger the documentation system. 

Since this change would cause almost all targets to be rebuilt the first time the new release of SCons is run, this change should be packaged with other updates that do the same. The [BigSignatureRefactoring](BigSignatureRefactoring) page appears to be the meeting place for coordinating this. 

Mentor(s): Probably [StevenKnight](StevenKnight) 



---

 
### Library and Application Versioning




SCons has no direct support for versioned libraries and applications, that is, packages that may have multiple versions installed at the same time.  SCons supports neither installing a versioned package nor choosing between multiple packages for a particular build. 

In the former case, the need is for a cross-platform "link" (or "symlink"?) action, with generic chaining so that `libfoo.so` can be symlinked to `libfoo.so.1`, which is linked to `libfoo.so.1.2`, which is linked to `libfoo.so.1.2.3` (the actual installed library).  Similarly, an application might be installed as `prog2.3` and needs a symlink to `prog`.  In addition, when cleaning (`'scons -c'`), it needs to remove the link only if it refers to the correct object (_i.e._, it should not remove a link created by a later installation).  See [bug #1947](/SCons/scons/issues/1947) for other aspects of this task. 

In the latter case, the need is to be able to choose a version of a library or application that's not the default (either an older guaranteed-stable version or a newer maybe-not-stable version).  How this is done varies between systems; the design of the feature should hide that level of detail.  Robert Lupton of Princeton has an Python implementation for selecting applications that works in his environment (it also can specify version dependencies to automate much of the selection), but it's not clear if it's sufficiently general-purpose. 

Doing both aspects of this for a single summer is probably too much, unless there's some existing technology that can be leveraged. 

Mentor(s): [StevenKnight](StevenKnight), [GregNoel](GregNoel), Robert Lupton (rhl at astro princeton edu), others 



---

 
### Reduce Memory Footprint

It's known that some applications have an enormous memory footprint when running SCons.  There's little visibility into why this would happen in some cases but not others.  Knowing what affects the memory footprint would enable both developers and users better control of the size of their run. 

There seem to be few tools that give insight into the footprint of a Python application.  SCons needs a framework that allows various sorts of statistics to be accumulated and displayed.  There are a number of pieces of information that would be useful (in no particular order): 

* The average size of each type of object, the number of times it is allocated, and the high-water mark of allocations. 
* The amount of memory allocated over time during the run, possibly annotated by how many of each type of object is in use. 
* The amount of memory spent on compiled Python code. 
* Objects freed by garbage collection (as opposed to a refcount dropping to zero). 
* Leaked (not collectible) objects. 
It may not be possible to gather all of these statistics currently, but if we can make a suitable case, it might be possible to influence future Python development to include features to make it possible. 

It would also be very useful to develop a set of guidelines that identifies what users can do to minimize their memory footprint. 

Existing tools that we're aware of in this space are [PySizer](http://pysizer.8325.org/) (which hasn't been updated since 2005), the Heapy toolset from [Guppy-PE](http://guppy-pe.sourceforge.net/) (which hasn't been updated since 2006), and [this recipe](http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/546530) by Jean Brouwers. 

Mentor(s): [GregNoel](GregNoel), [StevenKnight](StevenKnight) 



---

 
### Performance Improvements

SCons would get much wider adoption if its performance were improved.  The subsections below describe different techniques.  In general, the techniques can be divided into two major styles: top-down, by eliminating the need to execute entire phases, and bottom-up, by speeding up individual functions that contribute too much to the runtime. 


#### Large-scale Optimizations

There have been proposals to optimize SCons' performance by eliminating the need to reparse the SConscripts every time.  Other proposals have approached the issue by identifying only those SConscripts that contribute to the current rebuild and only reparse those. 

This section describes some large-scale changes that are intended to eliminate entire phases of SCons' operation in some circumstances. 

* One idea is a daemon that monitors filesystem changes.  SCons could query this daemon to learn what files have changed since the last build.  The daemon might also keep the SCons environment in memory to make "startup" instantaneous.  On Windows, the daemon could easily be implemented using public APIs (`FindFirstChangeNotification`, `ReadDirectoryChangesW`).  On some U<small>NIX</small>-like systems, there is the `fam` utility to monitor changes to files (there is a bit of prior art several years back when someone prototyped something like this on IRIX, but it never became widespread). 
* Another idea is to cache the DAG itself, in addition to the dependencies.  When SCons is started, it would check to see if any of its inputs (which would include files such as SConscripts, option files, imports, and so forth, as well as command-line options) have changed from the last run.  If not, it would reuse the cached DAG instead of running the SConstruct to rebuild the DAG from scratch. 
Mentor(s):  probably [StevenKnight](StevenKnight) 


#### "Fast Unsafe" Build Mode

Normally, SCons emphasizes correct builds over everything else, including speed.  For larger projects with multiple hierarchal directories, it would be a boon to have an 'instant build' option that would just build the changed files in a leaf directory, sort of as a syntax check before building and linking everything that depends on the changed files in other directories.  This would ease the pain on large projects where only a small part of it at a time is being modified and a quick compile check would suffice. 

The idea is to trade a guaranteed correct build for a fast development cycle when correctness is not desired.  This feature would be intended for savvy users, and it would be up to them to diagnose any problems that result from missing dependencies. 

The feature could require modifications to SConscripts to take advantage of it.  It could also impose restrictions on the information provided by calling SConscripts (perhaps so that the imports could be cached) so that only the local SConscript needs to be evaluated.  Additional restrictions and caveats are also possible.  And when a full build is done, the affected files may be rebuilt, even if it is not strictly necessary. 

[bug 1939](/SCons/scons/issues/1939) is one possible way to implement this project.  Other ways are possible.  A good proposal should consider alternatives. 

Mentor(s): Josh Leavitt <Josh dot Leavitt at hill af mil>, [GregNoel](GregNoel), [StevenKnight](StevenKnight) 


#### Benchmarks

One important aspect of performance is to be able to document the changes in performance.  The SCons project has started developing some benchmarks where the performance of routines believed to be critical can be tested and documented.  The task here would be to build some more of these benchmarks. 

There are two complimentary approaches in use: "micro" benchmarks that profile an actual SCons run that exercises one particular feature, and "nano" benchmarks that do side-by-side comparisons of internal functions.  Microbenchmarks are used to identify code that seems to be more expensive than one would expect.  Nanobenchmarks explore possible alternative implementations of code highlighted by microbenchmarks. 

Any project to work on performance should describe how the project plans to measure the performance.  It's not enough to just say, "I'll use the Python profiler," the idea is to discuss <ins>_how_</ins> you'd use it, what pieces you think you'll measure, how you plan to set reasonable performance targets and track progress against them, _etc_.  Development of any necessary tools, subsystems, or other infrastructure for measuring performance is fine, but should ideally aim for tools that are generally re-usable and useful in the future, not one-offs just for the project. 

Mentor(s): [GregNoel](GregNoel) or [StevenKnight](StevenKnight) 



---

 
### Integrate Code Coverage into Testing

_Code coverage_ is a form of testing that determines how much of the code has been executed during testing.  [Wikipedia](http://www.wikipedia.org/) lists five types of [code coverage](http://en.wikipedia.org/wiki/Code_coverage): 

* Function coverage - Has each function in the program been executed? 
* Statement coverage - Has each line of the source code been executed? 
* Condition coverage - Has each evaluation point (such as a true/false decision) been executed? 
* Path coverage - Has every possible route through a given part of the code been executed? 
* Entry/exit coverage - Has every possible call and return of the function been executed? 
There are at least three packages that do code coverage for Python: [trace2html](http://pypi.python.org/pypi/trace2html), [Coverage](http://nedbatchelder.com/code/modules/coverage.html), and [figleaf](http://darcs.idyll.org/~t/projects/figleaf/doc/).  A Google search would probably turn up others. 

The idea here is to add code coverage as a testing option.  The project would be to evaluate the various tools available, pick one (or synthesize one), and integrate it into the standard testing procedures.  It should be possible to visualize the output easily so that areas of untested code can be quickly identified.  And the process should be well documented. 

Mentor(s): [GregNoel](GregNoel) or [StevenKnight](StevenKnight) 



---

 
### Distributed Compilation

A model for being able to parallelize software builds by distributing work across a network of homogeneous machines would benefit many large projects.  One possible approach would be to try to integrate (and generalize) some functionality like `distcc`, perhaps similar to the way that SCons has already integrated some `ccache`-like functionality.  Another more ambitious approach would be to try to make use of existing grid computing systems.  Since the scope of this project is only a summer's worth of coding, there probably won't be enough time to solve this big a problem completely, so a better idea is to try to carve out a manageable first step in your proposal. 

(Note: [Incredibuild](http://www.xoreax.com/) recently added support for distributed SCons builds, which would meet the needs of some users.  However, it is a closed-source commercial product, so it is not an option for most open source software projects.) 

Mentor(s):  probably [StevenKnight](StevenKnight) 



---

 <a name="java"></a> 
### Better Java Support

SCons' Java support gets dinged by Java programmers for being relatively limited.  Revising the Java support to be better is important to the acceptance of SCons in the Java community.  There are a number of different pieces that could be carved out as well: 


#### Revamp approach to Java

SCons' approach to Java is to build entire subdirectories of `'.java'` files into one or more `'.jar'` files.  This is inadequate when only partial rebuilds are needed.  The Java support could use some refactoring (even redesign) by someone who's familiar with the needs of large-scale Java projects, and has an itch to try to use the underlying flexibility of SCons to do better than what's out there. 

Mentor(s): ???  Possibly [StevenKnight](StevenKnight) 


#### More Ant-like Behavior?

`Ant` is obviously the standard for Java compilation.  As a general dependency tool, it leaves something to be desired, largely because so much of the nitty-gritty Java dependency management is actually in `javac`, not `Ant`.  Nevertheless, Java programmers are familiar with the `Ant` model, and to the extent that we can find SCons-like ways to adopt parts of it, it would help make SCons more attractive (especially to Java programmers who are part of multi-language software projects). 

Mentor(s): ???  Possibly [StevenKnight](StevenKnight) 


#### Port to Jython

Making SCons run under Jython, thereby allowing it to run under the Java VM, might also help make it more attractive to the Java community.  Since SCons is all Python, it's actually not far from being able to do this, but there's a serious barrier with respective to Java's complete lack of a notion of a current directory and being able to `chdir()`.  Working around that might involve some serious refactoring to completely eradicate `chdir()` calls from the SCons source. 

Mentor(s): ???  Possibly [StevenKnight](StevenKnight) 


#### Groovy

Add a `Groovy()` builder that works with the `Java()` builder so that Groovy programs can be compiled and intermixed with Java. 

A simple builder for Groovy is a small project that could combined with other small projects to fill up a summer.  Integrating Groovy with Java is at least a medium-sized project. 

Mentor(s): Russel Winder <russel dot winder at concertan com>, possibly [StevenKnight](StevenKnight) 



---

 
### Improved Target-File Caching

The SCons `CacheDir()` function provides a framework for sharing built targets between developers, but it's relatively primitive.  A project to tackle one or more potential improvements to it would be extremely welcome.  Possible objectives include: 

* Administrative tools for managing the cache directory, including aging/clean up of old targets, limiting the size of cache, etc.  All subject to configuration options, of course. 
* Some mechanism for locking write access to target files when multiple clients try to create the same target—or better, some distribution of locking logic so clients can detect that some other client is in the progress of building a target file that will end up in the cache when finished. 
* Measure the efficiency and scalability of caching and address any issues so that it can handle thousands of source files in a tree and tens of thousands of targets. 
Mentor(s):  probably [StevenKnight](StevenKnight) 

















---

 
### Dynamically Determine Documentation Toolchains










A problem with many open source projects is that in the documentation area, developers don't know how to produce documentation that will be of use to many different users, so they end up producing plaintext documentation or documentation that only really flies on one platform (as in the case of SCons manpage), or they produce a PDF and hope that that will be OK with everyone.  If SCons were able to provide a convenient path from some of the popular documentation 'source' formats (L<small>a</small>T<small>e</small>X, TextInfo, DocBook, HTML) all the way through to platform-specific help files, this would help to improve access to what documentation developers create. 

The challenge is to integrate a decent suite of documentation tools so that platform-specific help files can be built and installed. On Windows there is the HtmlHelp compiler that can produce `.CHM` files from HTML files plus some index files. On GNOME and KDE there is the freedesktop.org [ScrollKeeper](http://scrollkeeper.sourceforge.net/) system, which allows HTML and DocBook XML to be served up via a centralised help browser. There are probably similar things on Mac, Solaris, and so on. 

The idea here is to create the mechanism that will determine the correct "native" documentation format based upon the deployment platform and then find a toolchain from the starting format to the deployment format.  The toolchain could be as short as zero commands if the deployment format is the same as the source format, or it could be one command that converts directly from the source format to the destination format, or it could be a series of conversions.  It's possible that the toolchain could vary based upon the commands available on the build machine.  Moreover, there could be more than one documentation format required if the same package could be deployed on different platforms. 

Mentor(s): possibly [JohnPye](JohnPye) 



---

 
### Batched Builders

Some builders are significantly faster if they compile more than one program at a time.  Other builders can optimize better if they can see more than one file at a time.  What these builders have in common is that they want to be passed all the out-of-date source files in the same step. 

[bug #1086](/SCons/scons/issues/1086) offers further discussion of the issues and and [bug #1381](/SCons/scons/issues/1381) has a patch that partially implements this concept.  The patch is several years old and is unlikely to work in its current state, but it should provide a good starting point. 

Finishing the development, creating regression tests, and writing the documentation is unlikely to be a full summer's worth of work, but it could easily be combined with other smaller tasks to fill out the time. 

Mentor(s): [StevenKnight](StevenKnight) 



---

 
### Better Windows Installation

The current SCons self-extracting Windows installer is generated by the Python `distutils` package. It has some limitations: 

* Because `distutils` is geared towards installing Python modules, it installs SCons as a script within the current Python installation, not as a standalone utility that happens to use Python 
* Related: it doesn't support multiple side-by-side installations of SCons (different versions) 
* It does not add SCons to the Windows Menu 
* It provides no "uninstall" action for SCons 
* It provides no Windows-style help (`.chm`) 
A project to re-write SCons' Windows installation so it behaves more like a "real application" would help spread SCons more widely and benefit a lot of users. 

One likely approach would involve writing a full [WiX](http://wix.sourceforge.net/) installer and by trying to crib best practices from other projects that already use it. (WiX itself is open source and available from SourceForge.) 

Also see the next item for a possible related project. 

Mentor(s): possibly [StevenKnight](StevenKnight) 



---

 
### Standalone Executable

There are still sites that don't have Python installed.  And sometimes an application can only be run with a particular version of Python.  Adding packaging logic so SCons can be shipped as a self-contained unit would help lower the barrier to entry for those sites. 

For Windows, the most likely approach would involve using [py2exe](http://www.py2exe.org/).  A more generic approach might involve using [PyInstaller](http://pyinstaller.python-hosting.com/), which reportedly covers Windows, Linux and Irix.  Coming up with a `.dmg` for Mac OS X would be good, too—perhaps this could involve helping a project like PyInstaller add that support...? 

A possible project to mine for ideas (and code?) is the [Chandler project](http://chandlerproject.org/) at the [Open Source Applications Foundation](http://www.osafoundation.org/), who apparently package Python in their distributions for systems that don't have it. 

Also see the previous item for a possible related project. 

Mentor(s): possibly [StevenKnight](StevenKnight) 



---

 
### Continuous Documentation


Keeping the public documentation in sync with the source is a continual problem in all open-source projects.  The idea here is to regenerate the PyDoc/JavaDoc/whatever, convert it into the wiki markup, and automatically inject it into the wiki.  Conversely, any edits to those pages would be turned into deltas that could be posted as patches or just folded back into the source.  This would keep the documentation up-to-date both on the web and in the source, and allow individuals without code commit privileges to participate by providing small edits to incomplete or incorrect documentation. 

Moreover, the injected documentation should be readily integrated into a higher-level framework so that the wiki can be organized by the way that makes sense to describe the concepts rather than the way it makes sense to code the program. 

The synchronization could be triggered every time the code is checked in, or on a timer, or manually.  The deltas between what is in the source and what is in the wiki would need to be retained (and reapplied) until they are resolved.  Some scheme would be needed to deal with conflicts between competing changes (probably the source should win, but alternatives exist that a proposal should explore). 

SCons uses Python, SVN, and a MoinMoin wiki, but the framework should not be limited to those choices, but should be adaptable to deal with different programing languages, repository types, and wiki markups. 

Mentor(s): [GregWilson](GregWilson) 



---

 
### Python Software Foundation

SCons will accept proposals for non-SCons projects, as long as we believe that the work will directly benefit us as well a wider community. 

One source of ideas is the [Python Software Foundation](http://www.python.org/psf/) (PSF), an umbrella organization whose mission is to promote, protect, and advance the Python programming language, and to support and facilitate the growth of the international community of Python programmers.  It holds the intellectual property rights to recent versions of Python and ensures that Python distributions are made available to the public free of charge. 

PSF is also a participant in the Summer of Code and has [their own ideas page](http://wiki.python.org/moin/SummerOfCode).  Feel free to pick a topic from their site that has direct applicability to SCons and float a proposal with us. 










---

 
### Another idea

info 


#### Idea subhead one

info 


#### Idea subhead two

info 

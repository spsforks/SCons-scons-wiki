

# GSOC 2014 Ideas Page


## Change SCons code to be runnable on Python 2.7 and Python 3.3 and later

The current source code of SCons is based on Python 2.4 as floor version. To support the goal of SCons running on Python 3 as well as Python 2, the floor version of Python has now been raised to 2.7. Also a branch has been taken in the Mercurial repository to support the work of creating a single SCons source that works with both Python 2 and Python 3. However, this is currently at a very early stage of work. 

The work of the project is envisaged to be: 

Become familiar with SCons as a build framework. Become familiar with the SCons source code structure. Become familiar with the SCons test system – SCons has a Buildbot-based continuous integration (CI) system, buildbot.scons.org. Integrate tox (for checking Python 2 and Python 3 compliance) into the CI system. Amend the SCons code, adding new tests as appropriate, so that all tests pass with both Python 2 and Python 3. Amend as needed, the documentation ([UserGuide](UserGuide)). During the work, redundant code (needed to support Python 2.4, 2.5 and 2.6) will be found and deleted – to the cheers of everyone. Also it is very likely that possible code refactorings will be discovered. Small refactors will just be made, large ones will need some discussion first, in case of overlap with other ongoing work.  

It is assumed that the person undertaking this project is reasonably proficient with Python before starting the project, is able (or willing to learn) to use Mercurial. 

Keywords: _Python_, _programming_, _code parsing_, _code rewrite_, _testing framework_, _continuous integration_, _CI_ 


## Get SCons to work better/at all on cygwin

Currently SCons doesn’t work that well in a cygwin environment. This mainly has to do with the use of posix paths inside the cygwin environment and with it’s tools, but not with tools which are normal win32 applications.   So this would require the student to handle translating paths and recognizing which tools require which paths. 

Keywords: _Python_, _cygwin_, _win32 environment knowledge_. 


## Change code to use more modern constructs (slots, generators/iterators)

SCons recently moved to a floor of Python 2.7; many modern python idioms are now available to us to increase performance, readability and maintainability as well as reducing memory usage. Keywords: _Python_, _software engineering skills_ 


## Improve packaging (get it into pypy and make it work with python setup.py and also in virtualenvs)

* Work on improving the way that SCons is packaged to enable easier distribution, and development. 
Keywords: _Python_, _setuptools_, _virtualenv_, _win32 installers_. 


## Migrate some functionality from Parts project (http://parts.tigris.org/)

The Parts project currently sits on top of SCons and provides some macro functionality as well as some patches to internals which improve upon SCons’s baseline. 

The Parts project creator has expressed interest for some time to migrate some (or all) of this logic into the core of SCons. 

Possible items that can be migrated: 

1. Move over parts.api.output code to allow an API independent of the python print logic to deal with messages of different types ( such as messages, warnings, verbose, tracing). so the text can be routed to log files, and colorized on the screen 
1. Move the code to allow python to correctly open files on windows, so that symlinks and hardlinks can be correctly supported. With this move over the Part CCopy and CCopyAs builder and --ccopy logic 
1. Given above or as a stretch goal, add the Part [SymbolicFileNode](SymbolicFileNode) object and api to allow SCons to deal with Symlinks as first class objects 
1. Move over the Version and [VersionRange](VersionRange) object. 
1. Move over the Namespace and bindable logic and objects 
1. Move over the [SystemPlatform](SystemPlatform) logic and api. This support the idea of stuff like win32-x86, or android-arm so the system can better support the idea of host system and target system for cross build, etc.. 
Keyword: _Python_ 


## Refactor the Node object

The Node is the central core object in SCons.  It represents a node in the dependency graph; a file, directory, alias, or abstract dependency or target node.  Over the years it has grown large and unwieldy and needs to be refactored.  This is a significant project, but not out of the realm of a summer student. 

This project has several goals: 

   * Reduce memory usage 
   * Improve performance 
   * Improve code readability and maintainability 
   * Lay the groundwork for future work 
The work itself takes several phases: 

   * Understand all the members and uses of the current Node object 
   * Design an improved refactoring 
   * Review with the dev team 
   * Implement the refactoring in stages 
   * Update tests 
Keyword: _Python_ 

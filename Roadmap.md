# The Roadmap

The goal of this page is to provide an overview of current goals and their status similar to the [roadmap page](http://dungeonhack.sourceforge.net/Roadmap) from [DungeonHack](DungeonHack). 

Task status description: 

* **open**: no one has claimed this task yet or the task has not been started
* **wip**: work-in-progress; someone has claimed/started this task
* **done**: task is finished

Additional tasks can be found on our [issue tracker](https://github.com/SCons/scons/issues). 

## SCons itself
Task | Status | Assigned to |  Target version
:----|:-------|------------:|:---------------
Performance Work| wip | bdbaddog | 3.1
Integrating stubprocess.py wrapper for speedup  |  wip  |  gary, dirk  |  3.x
[Revamp of Tools subsystem](RevampToolsSubsystem)  |  wip  |  gary  |
Recursive Glob (ant-like)  |  wip  |  dirk  |
Java support, partial redesign and adding functionality, e.g. for inner classes ([JavaStrategy](JavaStrategy) and [JavaSupport](JavaSupport))  |  open  |  jannijtmans,russel?  |
TNG, refactor task scheduling  |  open  |    |
[PluginArchitecture](PluginArchitecture), what's this?  |  open  |   |


## Web stuff
Task | Status | Assigned to |  Target version
:----|:-------|------------:|:---------------
Rewrite/restructure "About SCons"/"Getting started" sections  |  open   | member


## Done

Task | Status | Assigned to |  Target version
:----|:-------|------------:|:---------------
Migrate to [GitHub](http://github.com)  |  done  | bdbaddog | 3.x  |
Migrate current issues database from Tigris to GitHub  |  done |  bdbaddog  |  3.0.1
[Python 3 compatibility](Python3Compatibility) (including full Unicode support)  |  wip  |  bdbaddog  |  3.0
Switch trunk development to Mercurial ([DVCSMigration](DVCSMigration))  |  done (2017-04-14) | member
Redesign website | Done | Bill
[Issue 2264: cross-language scanner support](https://bitbucket.org/scons/scons/pull-requests/244/issue-2264-cross-language-scanner-support/diff)  | done | William Blevins | 2.5
Switch Node class to using slots  |  done  |  dirk  |  2.4 
Rewrite of [doc toolchain](DeveloperGuide/Documentation/Discussion)  |  done (2013-05-04, rev 0c9c8aff8f46)  |  dirk
New design for SCons docs (book/article)  |  done (2013-05-04, rev 0c9c8aff8f46)  |  dirk
[MoinMoin upgrade](WikiUpgrade) for further tweaking  |  done  |  techtonik

See also [SConsFutureProjects](SConsFutureProjects) for ideas considered for implementation.
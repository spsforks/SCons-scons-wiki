The goal of this page is to provide an overview of current goals and their status similar to the [roadmap page](http://dungeonhack.sourceforge.net/Roadmap) from [DungeonHack](DungeonHack).  You can login and subscribe to this page to monitor current development. 

Task status description: 

   * **open**: no one has claimed this task yet or the task has not been started 
   * **wip**: work-in-progress; someone has claimed/started this task 
   * **done**: task is finished

Additional tasks can be found on our [issue tracker](http://scons.tigris.org/project_issues.html). 

## SCons itself
Task | Status | Assigned to |  Target version
:----|:-------|------------:|:---------------
Switch Node class to using slots  |  wip  |  dirk  |  2.4 
Integrating stubprocess.py wrapper for speedup  |  wip  |  gary, dirk  |  2.4 
[Revamp of Tools subsystem](RevampToolsSubsystem)  |  wip  |  gary  |  
GSoC 2013, collecting ideas/mentors and apply  |  open  |   |  
Wrapup of all other old GSoC projects, including new structure for Wiki pages  |  open  |   |  
[Python 3 compatibility](Python3Compatibility) (including full Unicode support)  |  wip  |  gary  |  
[GitHub](GitHub) clone to get additional buildbot at [https://travis-ci.org/](https://travis-ci.org/)  |  open  |   |  
Migrate current issues database from Tigris to [GoogleCode](GoogleCode) ([HostingSites](DVCSMigration/HostingSites))  |  [open](https://bitbucket.org/techtonik/dataliberation/src/default/issues/tigris/)  |  techtonik  |  
[SConsInstaller](SConsInstaller), wrapup of GSoC 2009 by Lukas Erlinghagen |  open  |   |  
Recursive Glob (ant-like)  |  wip  |  dirk  |  
Java support, partial redesign and adding functionality, e.g. for inner classes ([JavaStrategy](JavaStrategy) and [JavaSupport](JavaSupport))  |  open  |  jannijtmans,russel?  |  
[ApproximatePercentageThatMightGoBackwards](ApproximatePercentageThatMightGoBackwards), what's this?  |  open  |    |  
TNG, refactor task scheduling  |  open  |    |  
[PluginArchitecture](PluginArchitecture), what's this?  |  open  |   |  


## Web stuff
Rewrite/restructure "About SCons"/"Getting started" sections  |  open  
:-------------------------------------------------------------|:-----
[MoinMoin](MoinMoin) Roadmap plugin for this page  |  open


## Done
Switch trunk development to Mercurial ([DVCSMigration](DVCSMigration))  |  done (2011-11-21) | member
:-----------------------------------------------------------------------|-------------------:|:------
Rewrite of [doc toolchain](DeveloperGuide/Documentation/Discussion)  |  done (2013-05-04, rev 0c9c8aff8f46)  |  dirk 
New design for SCons docs (book/article)  |  done (2013-05-04, rev 0c9c8aff8f46)  |  dirk 
[MoinMoin upgrade](WikiUpgrade) for further tweaking  |  done  |  techtonik 

See also [SConsFutureProjects](SConsFutureProjects) for ideas considered for implementation. 
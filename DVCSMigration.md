On November 21th, 2011 SCons codebase officially migrated from SVN to Mercurial. 

[https://bitbucket.org/scons](https://bitbucket.org/scons) 

# SCons DVCS Migration

The release team decided on 3 August 2010 to go ahead and migrate SCons development to [Mercurial](http://mercurial.selenic.com/).  The goal is to make the transition shortly after 2.1 is released, which by the current [Roadmap](http://scons.tigris.org/roadmap.html) is scheduled for October 2010. 

This page and its sub-pages are to record opinions and discussion, as well as final decisions, leading up to the transition.  Open-ended discussion and exploratory questions should be carried out on the [dev@scons.tigris.org](mailto:dev@scons.tigris.org) mailing list.  Record things here if they represent some conclusion or other fact that affects the transition, or if they represent a significant dissenting opinion that should be recorded for posterity (e.g. to record an alternate solution if some aspect hits a snag). 


## Decision Criteria

Underlying assumption:  at this point picking a reasonable direction and going with it will be more productive than continuing to dither while trying to decide on the "best" solution.  With that in mind: 

Mercurial won out over [Git](http://git-scm.com/) because Windows support is still not a first-class citizen in the Git world.  Although `msysgit` reportedly works well enough for "normal" use, it apparently still has problems with some workflows.  Also, Mercurial is written and extensible in python, as is SCons. 

Mercurial won out over [Bazaar](http://bazaar.canonical.com/en/) because two of the SCons development team have experience with it, and none have experience with Bazaar.  Given that other key factors (multi-platform support, Python extensibility) were roughly equivalent and Bazaar didn't seem to have a "killer feature" that made it clearly superior for our likely purposes, the shallower learning curve of prior exposure gives Mercurial the nod as a reasonable choice. 


## Workflow

We are planning to use the same branching model as Mercurial themselves, with main development on the trunk and long-lived branches for releases.  Mercurial's documentation for this is at  [http://mercurial.selenic.com/wiki/StandardBranching](http://mercurial.selenic.com/wiki/StandardBranching). 

Users will be able to clone the repository and submit pull requests for patches. 


## Planning

Transition planning (enumerating specific tasks) is being discussed at the [DVCSMigration/TaskList](DVCSMigration/TaskList) sub-page. 


## Site Hosting

We have decided to host SCons at bitbucket, at [https://bitbucket.org/scons](https://bitbucket.org/scons).  Both bitbucket and Google Code seemed good enough, and some people already had repos at bitbucket. 

The decision about where to host development is documented at the [DVCSMigration/HostingSites](DVCSMigration/HostingSites) sub-page. 

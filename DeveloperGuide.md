# SCons Developer Guide

This is the SCons Developer Guide.  Start here to [learn how to contribute to SCons](DeveloperGuide/Introduction) and understand how it works under the hood.

* [Introduction](DeveloperGuide/Introduction)
* Getting the source
    * git clone [https://github.com/SConsProject/scons.git](https://github.com/SConsProject/scons.git)
    * [Source tree organization](SourceWalkThrough) 
* Hacking on the source
    * META: do you really need to?
        * [Writing builders](ToolsForFools), wrappers, and subclassing (don't need to change source)
        * Using scons_dir for extensions
    * [Running from the source tree](https://github.com/SConsProject/scons)
    * [DebuggingScons](DebuggingScons)
* Contributing
    * [Mailing lists](http://www.scons.org/lists.html) (hammering out an idea before jumping in)
    * [Easy issues to fix](DeveloperGuide/EasyIssuesToFix) from our Tigris bug tracker
    * [Documentation](DeveloperGuide/Documentation)
    * [Writing and debugging tests](DeveloperGuide/TestingMethodology)
    * [git workflows](DeveloperGuide/GitWorkflows), explains how to work with git to submit your patches
    * [Accepting pull requests](DeveloperGuide/AcceptingPullRequests), howto for the SCons admin
    * [SconsBuildRequirements](SconsBuildRequirements), which packages you need for a full build
    * [Packaging](ReleaseHOWTO/SimplifiedReleaseProcedure)
* [Architecture](DeveloperGuide/ArchitectureOverview)
    * [Installation](DeveloperGuide/Installation) (the way SCons is meant to be found)
    * [Nodes](DeveloperGuide/Nodes) (Dir, File, Value, ...)
    * [Signatures](DeveloperGuide/Signatures)
    * Determining configuration
    * Environments and what they encapsulate
    * Tools
    * Building blocks for scripting (Commands, Actions, Builders, Emitters, ...)
    * [Scanners](Scanners)
    * Parsing the SConscripts
    * Node management (building the DAG)
    * [TaskMaster](DeveloperGuide/TaskMaster)
        * Running the DAG
        * Scanning for implicit dependencies
        * Dealing with signatures
    * [Statistics](DeveloperGuide/Statistics) (for debugging and performance measurement)
* [Overview of Modules and Classes](DeveloperGuide/Classes)
* Improvement ideas
    * [SummerOfCodeIdeas](SummerOfCodeIdeas)

Other resources:

* The [man page](http://www.scons.org/doc/HTML/scons-man.html), especially the [Extending SCons](http://www.scons.org/doc/HTML/scons-man.html#lbAO) section.
* Be sure to check out the [developer guidelines](http://scons.org/guidelines.html)
* [JavaSupport](JavaSupport)
* [LatexSupport](LatexSupport) (and TeX)
* [VisualizeDependencies](VisualizeDependencies) - display of large source graphs (DOT format) with yEd
* [WhySconsIsNotSlow](WhySconsIsNotSlow) - runtime and speedup analysis


---

**This is a work in progress.**

Items to add:

* More information on .sconsign file.


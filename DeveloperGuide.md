# SCons Developer Guide

This is the SCons Developer Guide.  Start here to [learn how to contribute to SCons](DeveloperGuide/Introduction) and understand how it works under the hood.

* [Introduction](DeveloperGuide/Introduction)
* Getting the source
    * git clone [https://github.com/SCons/scons.git](https://github.com/SCons/scons.git)
    * [Source tree organization](SourceWalkThrough) 
* Hacking on the source
    * META: do you really need to?
        * [Writing builders](ToolsForFools), wrappers, and subclassing (don't need to change source)
        * Using scons_dir for extensions
    * [Running from the source tree](https://github.com/SCons/scons/wiki/Running-SCons-from-your-git-sandbox)
    * [DebuggingScons](DebuggingScons)
* Contributing
    * [Mailing lists](http://www.scons.org/lists.html) (hammering out an idea before jumping in)
    * [Documentation](Documentation)
    * [Writing and debugging tests](TestingMethodology)
    * [git workflows](GitWorkflows), explains how to work with git to submit your patches
    * [SconsBuildRequirements](SconsBuildRequirements), which packages you need for a full build
    * [Packaging](ReleaseHOWTO/SimplifiedReleaseProcedure)
* [Architecture](ArchitectureOverview)
    * [Installation](Installation) (the way SCons is meant to be found)
    * [Nodes](Nodes) (Dir, File, Value, ...)
    * [Signatures](Signatures)
    * Determining configuration
    * Environments and what they encapsulate
    * Tools
    * Building blocks for scripting (Commands, Actions, Builders, Emitters, ...)
    * [Scanners](Scanners)
    * Parsing the SConscripts
    * Node management (building the DAG)
    * [TaskMaster](TaskMaster)
        * Running the DAG
        * Scanning for implicit dependencies
        * Dealing with signatures
    * [Statistics](Statistics) (for debugging and performance measurement)
* [Overview of Modules and Classes](Classes)
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


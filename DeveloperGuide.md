

# SCons Developer Guide

This is the SCons Developer Guide.  Start here to [learn how to contribute to SCons](DeveloperGuide/Introduction) and understand how it works under the hood. 

* [Introduction](DeveloperGuide/Introduction) 
* Getting the source 
   * hg clone [https://bitbucket.org/scons/scons](https://bitbucket.org/scons/scons) 
   * [Source tree organization](DeveloperGuide/SourceWalkThrough) 
* Hacking on the source 
   * META: do you really need to? 
      * [Writing builders](ToolsForFools), wrappers, and subclassing (don't need to change source) 
      * Using scons_dir for extensions 
   * [Running from the source tree](https://bitbucket.org/scons/scons) 
   * [DebuggingScons](DebuggingScons) 
* Contributing 
   * [Mailing lists](http://www.scons.org/lists.php) (hammering out an idea before jumping in) 
   * [Easy issues to fix](DeveloperGuide/EasyIssuesToFix) from our Tigris bug tracker 
   * [Documentation](DeveloperGuide/Documentation) 
   * [Writing and debugging tests](DeveloperGuide/TestingMethodology) 
   * [Mercurial workflows](SconsMercurialWorkflows), explains how to submit your patches 
   * [Accepting pull requests](DeveloperGuide/AcceptingPullRequests), howto for the SCons admin 
   * [SconsBuildRequirements](SconsBuildRequirements), which packages you need for a full build 
   * [Packaging](DeveloperGuide/SconsPackaging) 
* [Architecture](DeveloperGuide/ArchitectureOverview) 
   * [Installation](DeveloperGuide/Installation) (the way SCons is meant to be found) 
   * [Initialization](DeveloperGuide/Initialization) (processing the command line and option files) 
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
* Be sure to check out the [developer guidelines](http://www.scons.org/guidelines.php) 
* "Use the source, Luke" 
* [JavaSupport](JavaSupport) 
* [LatexSupport](LatexSupport) (and TeX) 
* [VisualizeDependencies](VisualizeDependencies) - display of large source graphs (DOT format) with yEd 
* [WhySconsIsNotSlow](WhySconsIsNotSlow) - runtime and speedup analysis 


---

 This is a work in progress.  Click on the "Edit(Text)" link below, and let's start discussing what needs to go in this guide. 

* Known topic with no place to live yet: .sconsign.  The architecture section is organized more-or-less in time order and this topic doesn't fit that particularly well.  [JGN 19 Jan 2007] 
* I put in links for sections that I thought were pretty solid, but there are a number of areas where the topics are still flexible.  Someone with more knowledge of the internals should clarify those aspects. [JGN 19 Jan 2007] 
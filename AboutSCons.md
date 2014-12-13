
SCons is a build system (build tool, make tool or software construction tool) written in pure Python. SCons uses Python scripts as "configuration files" for software builds. Based on the design that won the Software Carpentry build tool competition, SCons solves a number of problems associated with build automation, especially with the classic and ubiquitous Make itself. 

In contrast to command automation tools like Fabric, where you specify a name of an action to execute, in build systems like SCons you specify the name of a target (usually a file or directory) that needs to be built. You can have abstract targets (Value nodes) and aliases for doing ordinary automation tasks, but the base principle is that you specify what you need built, and SCons figures out what needs to be done.  It builds a complete dependency graph (what nodes depend on other nodes and what commands each node needs) and then executes the minimal set of commands to bring the desired targets up to date. 

If you're familiar with Linux, then you might be interested to know that in its evolution SCons will not only serve as a replacement to make, but for whole GNU Build System. This GNU Build System (GBS) is also known as the set of Autotools (autoconf, automake, autoheader, etc...) 

Distinctive features of SCons include: 

* modular design, lending itself to embedding in other applications 
* pure Python makes it possible to distribute tool along with project sources 
* a [GlobalView](GlobalView) of all dependencies in the source tree 
* an improved model for [ParallelBuilds](ParallelBuilds) (-j) 
* automatic scanning of files for dependencies 
* use of MD5 signatures for deciding whether a file is up-to-date 
* use of MD5 signatures instead of traditional file timestamps available as an option 
* use of Python functions or objects to build target files 
* easy user extensibility 
[SconsVsOtherBuildTools](SconsVsOtherBuildTools) 

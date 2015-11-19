**This is the place to share tips, examples, and short scripts.**

The SCons [ManPage](http://www.scons.org/doc/HTML/scons-man.html) also contains a number of quick examples. 

See the [Examples](http://www.scons.org/doc/HTML/scons-man.html#lbBB) section towards the bottom of the page. 

**Table of Contents**

[TOC]

---

## Scons : Extending and getting info

* [SconsVersion](SconsVersion): how to retrieve the version of scons from your script 
* [WrapperFunctions](WrapperFunctions): you want to wrap up a bit of SCons and python as a new Environment method without modifying scons itself 
* An [ExportImportShortcutHack](ExportImportShortcutHack). 

## Command-Line Arguments and Help

* [ArgumentQuoting](ArgumentQuoting) in actions 
* [UsingCommandLineArguments](UsingCommandLineArguments): Using ARGUMENTS 
* [AutomaticHelpFromAliases](AutomaticHelpFromAliases): technique for injecting helper functions into environment and wrapping Alias() to get Help() automatically 

## Configuration

* [SconsAutoconf](SconsAutoconf): How to add autoconf functionality to your scons builds. 
* [Autoconf recipes](AutoconfRecipes): a few autoconf macro implementations. 
* [GenerateConfig](GenerateConfig): generating a config.h file 
* [SavingVariablesToAFile](SavingVariablesToAFile) - saving the value of some variables to a file and loading them back 
* [UpdateOnlySomeVariables](UpdateOnlySomeVariables) - Update some variables in an environment without overwriting changes to others. 

## Targets

* [GetTargets](GetTargets): you want to look at the targets the user entered 
* [PhonyTargets](PhonyTargets): A close approximation of a target that is always built 
* [DependsAndAliases](DependsAndAliases): How to ensure Alias() work correctly with Depends() 

### Install & Uninstall Targets

* [InstallTargets](InstallTargets): writing install and uninstall targets 
* [InstallationPrefix](InstallationPrefix) 
* [PlatformIndependedInstallationTool](PlatformIndependedInstallationTool) 

### Clean Targets

* [CustomCleanActions](CustomCleanActions): Having an Action run when scons is in clean mode 

## Tree Problems

* [NonDeterministicDependencies](NonDeterministicDependencies) How to incorperate builders which can produce an unknown number of results 

## Source Files

* [BuildDirGlob](BuildDirGlob) lets you glob for source files from a build directory. 
* [ExternalFiles](ExternalFiles): how to use other source files not recognized by scons (e.g. linker scripts) 
* [UsingCvs](UsingCvs): how to download source files from a CVS server 
* [WgetSourceCode](WgetSourceCode): How to use sourcecode() methods to 'wget' files 
* [DynamicSourceGenerator](DynamicSourceGenerator): how to use a source generator that puts out many source files, by having scons add targets dynamically. 
* [FindTargetSources](FindTargetSources): Find sources and headers for a target when generating MSVSProject. 
* [AddFilesDynamically](AddFilesDynamically) to every build per-environment 
* [MFObject](MFObject): Compile multiple source files with a single invocation of the compiler 
* [ExplicitlyCallCppScanner](ExplicitlyCallCppScanner): How to explicitly call the C/CPP scanner on a source file in your SConstruct/SConscript. 

## Building and Linking

* [UsingOrigin](UsingOrigin): using $ORIGIN to specify runtime search path for libraries 
* [UsingPkgConfig](UsingPkgConfig): many libraries these days come with .pc files, such as GTK+, but how do you use them? 
* [SharedLibrarySignatureOverride](SharedLibrarySignatureOverride): avoid relinking every program when a shared library is rebuilt. 
* [BuildTimeCallback](BuildTimeCallback): How to have a function called at build time 
* [RightNow](RightNow): Build one or more targets during the SConscript reading phase, then continue reading SConscripts 

### Build Dirs

* [UsingBuildDir](UsingBuildDir) 
* [UnderstandingBuildDir](UnderstandingBuildDir) 

### Build logs

* [BuildLog](BuildLog): How to write SCons output to a file as well as the screen. 
* [ColorBuildMessages](ColorBuildMessages): Replace the raw build commands printed to the screen with colored messages 
* [ColorGcc](ColorGcc): using the [colorgcc](http://www.mindspring.com/~jamoyers/software/) wrapper to colorize the output of compilers with warning / error messages matching the gcc output format. 
* [HidingCommandLinesInOutput](HidingCommandLinesInOutput): how to hide all or part of the printed command lines for prettier build logs. 

## Environment

* [ImportingEnvironmentSettings](ImportingEnvironmentSettings) from your process environment. 
* [EnvValue](EnvValue): A value node which substitutes variables from the environment 
* Using [ExternalTools](ExternalTools) from within SCons frequently requires certain types of environment variable inheritance. 

## Testing

* [ValgrindMemChecker](ValgrindMemChecker): Automatic running of valgrind on executables 
* [UnitTests](UnitTests): Running unit tests with an Alias or Command 

## Multiple Projects

* [SconstructMultiple](SconstructMultiple): multiple projects, build dir, debug/release 
* [SconstructMultipleAll](SconstructMultipleAll): build all, multiple projects, build dir, debug/release 
* [SconstructMultipleRefactored](SconstructMultipleRefactored): clean up redundancy in [SconstructMultiple](SconstructMultiple) 


---

 


## Increasing performance and large builds

* The [GoFastButton](GoFastButton): options you can use to make SCons faster by sacrificing build accuracy 
* [ModularExample](ModularExample): A modular way to support multiple systems and build multiple setups at a time. 
* [SimultaneousVariantBuilds](SimultaneousVariantBuilds): How to make build different variants (e.g. debug/release, target/host) at the same time. 
* [PreventBuildingOfEverything](PreventBuildingOfEverything): you have a big hierarchical tree of projects... 
* [ProxyDependencies](ProxyDependencies): A simple way to avoid inefficiencies when you have commands that consume lots of input files and produce lots of output files. 
* [TargetDrivenBuilderCreation](TargetDrivenBuilderCreation): Avoid scanning large source trees on startup by only queuing up dependencies on demand for things scons actually needs to build. 
* [LimitCacheSizeWithProgress](LimitCacheSizeWithProgress): Prevent the cache directory to grow indefinitely. 
* [SerialiseForSharedResources](SerialiseForSharedResources) : Tell scons to run particular tasks in series, while letting others run in parallel. 


---

 


## Misc

* [DumpEnv](DumpEnv): Dump the contents of the construction environment 
* [JavaNativeInterface](JavaNativeInterface): how to build java native interface (JNI) libraries 
* [MultipleDirectoryFortranBuild](MultipleDirectoryFortranBuild): how to setup a multiple-directory Fortran 90 project 
* [SconsLatexThesisSkeleton](SconsLatexThesisSkeleton): A more elaborate way to build LaTeX documents with SCons, including automatic file format conversion 
* [StaticallyLink](StaticallyLink): Statically link g++ libraries 
* [CudaTool](CudaTool) - tool for NVidia's CUDA 
* [Building Debian packages](http://quentinsf.com/writings/debscons/) 
* Quite a bunch of SCons techniques, including the use of SConf, can be seen in the [http://madman.sf.net](http://madman.sf.net) madman build scripts. 

## Full-blown Examples

* [AdvancedBuildExample](AdvancedBuildExample): This document describes how the [Bombyx](http://bombyx.sourceforge.net/) project is doing its builds. This configuration is interesting in that it builds for each target platform in a different directory, and has a very structured build. 
* [ExtendedExample](ExtendedExample) A log of John Arrizza's quest to convert an Ant-based build system to SCons. 
* [AllInSConstruct](AllInSConstruct) Bill Baxter's attempt at a SCons-based build system. 
* [RpmHonchoTemp](RpmHonchoTemp): [JeffPitman](JeffPitman)'s adventure in coercing SCons to manage an RPM repository. 
* [BasicSimpleProject](BasicSimpleProject): Andrew Lentvorski's venture to build Gambit with SCons on his way to cross-compiling 
* [SimpleProject_1](SimpleProject_1): A simple project with libraries and profile information 
* [MavenIdeasWithSCons](MavenIdeasWithSCons): An approach of using some maven ideas and best practices with SCons. 
* [SDLWindowsApp](SDLWindowsApp): A typical SDL application on Windows (including icon and no annoying dialog pop-up) 

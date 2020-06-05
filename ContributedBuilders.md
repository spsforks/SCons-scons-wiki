Here is a list of community-contributed Builders:

* Also see [ToolsIndex](ToolsIndex), a list of external SCons Tools that are developed as packages and managed via a distributed version control system such as Bazaar, Mercurial, Git, and so on.

# Builders

* [AccumulateBuilder](AccumulateBuilder): builder which "collects" files and/or directories for easy tarring/zipping for distribution 
* [AntlrBuilder](AntlrBuilder): Builder for antlr to create targets that Scons can use 
* [ArchiveBuilder](ArchiveBuilder): Builder to make archive (tar.gz, tar.bz2 or zip) in a simple way 
* [BuildNumberProcessing](BuildNumberProcessing): you have a build number or version number that needs to be included in the link 
* [CheetahBuilder](CheetahBuilder): compiles and fills Cheetah templates 
* [CombineBuilder](CombineBuilder): Small Builder to include several c/c++ source files into one file 
* [CorbaBuilder](CorbaBuilder): Builder for orbix corba idl generated C++ files. 
* [CorbaTaoBuilder](CorbaTaoBuilder): Builder for tao corba idl generated C++ files. 
* [CsharpBuilder](CsharpBuilder): a builder to support C# using Mono, mcs, etc. 
* [CxxTestBuilder](CxxTestBuilder): Integrate [CxxTest](CxxTest) unit testing framework into scons, together with a 'scons check' target. (make check clone from autotools) 
* [DistTarBuilder](DistTarBuilder): builds a tar file with an internal directory structure 
* [Download- & UnpackBuilder](DownloadUnpack) - two correspondent builders, that can download and unpack a file (eg tar.gz / tar.bz2), usefull for installing libraries to a project 
* [DoxygenBuilder](DoxygenBuilder): generates doxygen docs automatically scanning for dependencies 
* [EiffelStudioTool](EiffelStudioTool): Builder tool for the Eiffel programming language ([EiffelStudio](http://dev.eiffel.com)). 
* [EnvValue](EnvValue): A value node which substitutes variables from the environment 
* [GchBuilder](GchBuilder): Builder for gcc's precompiled headers 
* [GhcBuilder](GhcBuilder): Builder for the [Haskell](http://www.haskell.org/) programming language. 
* [InstallFiles](InstallFiles) - Recursively scan the source for files to install according to glob and exclude patterns 
* [LyxBuilder](LyxBuilder): Convert .lyx files to .tex. And teach PDF to understand .lyx files. 
* [MsvcIncrementalLinking](MsvcIncrementalLinking) - Replaces the Program and [SharedLibrary](SharedLibrary) builders to support Microsoft Visual C++ incremental linking. 
* [NasmBuilder](NasmBuilder): how to compile nasm source files 
* [NsisBuilder](NsisBuilder): see [NsisSconsTool](NsisSconsTool) 
* [ProtocBuilder](ProtocBuilder) - Generates Protocol Buffers target files from .proto source. 
* [PyrexPythonExtensions](PyrexPythonExtensions): how to build pyrex python extension modules using SCons 
* [PythonExtensions](PythonExtensions): how to build python extension modules using SCons Swig & Boost 
* [PyuicBuilder](PyuicBuilder) - Generates [PyQt](PyQt) Python files from [QtDesigner](QtDesigner) .ui source. 
* [ReplacementBuilder](ReplacementBuilder): for when you need to take a *.in file and replace some variables in it, such as pkg-config .pc files or DBus .service files 
* [ReStructuredTextBuilder](ReStructuredTextBuilder): produces HTML or LaTeX output from reStructuredText input 
* [RpcBuilder](RpcBuilder): how to compile RPC protocol sources 
* [RunningConfigureAndMake](RunningConfigureAndMake): how to use SCons to run configure and make, as part of migrating from Makefiles 
* [SconsDotNet](SconsDotNet) - using SCons to build [CoctaThorpe](CoctaThorpe) and [VbDotNet](VbDotNet) 
* [StaticPicLibrary](StaticPicLibrary) - a builder like [StaticLibrary](StaticLibrary) but aiming to place position independant code (pic) in the library built 
* [SwigBuilder](SwigBuilder): extra stuff about building SWIG beyond what's currently built-in. 
* [UicImageEmbedder](UicImageEmbedder): builder which generates an image collection by embedding image files into a c++ sourcefile 
* [UsingCodeGenerators](UsingCodeGenerators): how to build an application and then use that application to generate other files 
* [UsingCompilerBuilt](UsingCompilerBuilt) asks about building a compiler/tool which is then used to build the application. 
* [SubstInFileBuilder](SubstInFileBuilder): provides TOOL_SUBST, which substitutes values from a dictionary into a file.  Can be used for autotools-like configure substitution or other purposes. 
* [SubstInFileBuilder2](SubstInFileBuilder2): provides a slightly different implementation of [SubstInFile](SubstInFile) that substitutes values from the environment into a file. 
* [GenericSubstBuilder](GenericSubstBuilder): Provides a powerful generic substitution mechanism and two helpers for regular files and headers. 

# Tools for specific libraries

* [CheckBoostVersion](CheckBoostVersion): Boost does not provide pkg-config file so we need to check its version by other means 
* [Qt4Tool](Qt4Tool): David García Garzón has been working on a Qt4 tool with much success 
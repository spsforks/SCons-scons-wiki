Here is a list of community-contributed Builders:

* Also see [ToolsIndex](ToolsIndex), a list of external SCons Tools that are developed as packages and managed via a distributed version control system such as Bazaar, Mercurial, Git, and so on.

# Builders

* [AccumulateBuilder](AccumulateBuilder) - Collect files and/or directories for easy tarring/zipping for distribution
* [AntlrBuilder](AntlrBuilder) - Use [ANTLR](https://www.antlr.org/) to create targets that SCons can use
* [ArchiveBuilder](ArchiveBuilder) - Create archives (`.tar.gz`, `.tar.bz2`, `.zip`) in a simple way
* [BuildNumberProcessing](BuildNumberProcessing) - Add a build number or version number to the linked output
* [CheetahBuilder](CheetahBuilder) - Compile and fill [Cheetah templates](https://cheetahtemplate.org/)
* [CombineBuilder](CombineBuilder) - Combine several C / C++ source files into one file
* [CorbaBuilder](CorbaBuilder) - Generate C++ from [Orbix CORBA](https://www.microfocus.com/en-us/products/orbix/overview) IDL files
* [CorbaTaoBuilder](CorbaTaoBuilder) - Generate C++ from [Tao CORBA](https://objectcomputing.com/products/tao) IDL files
* [CsharpBuilder](CsharpBuilder) - Build C# using Mono, mcs, etc.
* [CxxTestBuilder](CxxTestBuilder) - Integrate [CxxTest](CxxTest) unit testing framework into SCons, together with a 'scons check' target. (make check clone from autotools)
* [DistTarBuilder](DistTarBuilder) - Build a `.tar` file with an internal directory structure
* [DownloadUnpackBuilder](DownloadUnpack) - Two related Builders, that can download and unpack a file (`.tar.gz` / `.tar.bz2`), useful for installing libraries to a project
* [DoxygenBuilder](DoxygenBuilder) - Generate [Doxygen](https://www.doxygen.nl/index.html) documentation automatically
* [EiffelStudioTool](EiffelStudioTool) - Build and use the Eiffel programming language, see: [EiffelStudio](http://dev.eiffel.com).
* [EnvValue](EnvValue) - A value Node which substitutes variables from the Environment
* [GchBuilder](GchBuilder) - Build and use `gcc` precompiled headers
* [GhcBuilder](GhcBuilder) - Build and use the [Haskell](http://www.haskell.org/) programming language.
* [InstallFiles](InstallFiles) - Recursively scan the source for files to install according to glob and exclude patterns
* [LyxBuilder](LyxBuilder) - Convert `.lyx` files to `.tex` and teach [PDF()](https://scons.org/doc/production/HTML/scons-user.html#b-PDF) to understand `.lyx` files
* [MsvcIncrementalLinking](MsvcIncrementalLinking) - Replaces the [Program](https://scons.org/doc/production/HTML/scons-user.html#b-Program) and [SharedLibrary](SharedLibrary) builders to support Microsoft Visual C++ incremental linking.
* [NasmBuilder](NasmBuilder) - Compile [NASM](https://nasm.us/) assembly source files
* [NsisBuilder](NsisBuilder) - See: [NsisSconsTool](NsisSconsTool)
* [ProtocBuilder](ProtocBuilder) - Compile Protocol Buffers `.proto` source files
* [PyrexPythonExtensions](PyrexPythonExtensions) - Build [Pyrex](https://wiki.python.org/moin/Pyrex) Python extensions
* [PythonExtensions](PythonExtensions) - Build Python extensions using [SWIG](http://swig.org/) and [Boost](https://www.boost.org/)
* [PyuicBuilder](PyuicBuilder) - Generate [PyQt](PyQt) Python files from [QtDesigner](QtDesigner) `.ui` sources
* [ReplacementBuilder](ReplacementBuilder) - Interpolate variables into `*.in` files, e.g. `pkg-config .pc` files or DBus `.service` files
* [ReStructuredTextBuilder](ReStructuredTextBuilder) - Use reStructuredText to produce HTML or LaTeX output
* [RpcBuilder](RpcBuilder) - Compile RPC protocol source files
* [RunningConfigureAndMake](RunningConfigureAndMake) - Run `configure` and `make`, as part of migrating from `Makefiles`
* [SconsDotNet](SconsDotNet) - Build [CoctaThorpe](CoctaThorpe) and [VbDotNet](VbDotNet) projects
* [StaticPicLibrary](StaticPicLibrary) - Build static libraries using Position-Independant Code (PIC), instead of [StaticLibrary](StaticLibrary)'s method
* [SwigBuilder](SwigBuilder) - Build SWIG wrappers with extra options
* [UicImageEmbedder](UicImageEmbedder) - Embed image file collection into a C++ source file
* [UsingCodeGenerators](UsingCodeGenerators) - Build an application and then use that application to generate other files
* [UsingCompilerBuilt](UsingCompilerBuilt) - Build a compiler / tool which is then used to build the application
* [SubstInFileBuilder](SubstInFileBuilder) - Provide `TOOL_SUBST`, which substitutes values from a dictionary into a file.  Can be used for autotools-like configure substitution or other purposes
* [SubstInFileBuilder2](SubstInFileBuilder2) - Provide a slightly different implementation of [SubstInFile](SubstInFile) that substitutes values from the environment into a file
* [GenericSubstBuilder](GenericSubstBuilder) - Provide a powerful generic substitution mechanism and two helpers for regular files and headers

# Tools For Specific Libraries

* [CheckBoostVersion](CheckBoostVersion) - [Boost](https://www.boost.org/) does not provide a `pkg-config` file, so we need to check its version by other means
* [Qt4Tool](Qt4Tool) - David García Garzón has been working on a Qt4 tool with much success
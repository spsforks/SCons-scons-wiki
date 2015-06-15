**Table of Contents**

[TOC]

SCons processes the commands in the [SConstruct](SConstruct) in order as they appear. These commands build a [DependencyTree](DependencyTree). The dependency tree contains [NodeObjects](NodeObjects) that correspond to some sort of object to be built. Which Nodes to build in the dependency tree is determined by the command line arguments given by the user. 

We now have a family of trees (a forest) that represent the topmost files to build. All of the files that are out of date are built. This process recurses to ensure all subsequent Nodes are built as needed. 

The following is pseudo code for the overall process that SCons follows: 

# Pseudo Code

```
Read SConstruct as a Python script:
# Default Environment object is created.
# Tools do their checks and modify the Environment object.
# Regular Python code is executed as usual.
# SConscript() calls cause referenced SConscript files to be
#   read/executed immediately.
# Methods of Environment object are used to update the dependency
#   tree and manipulate SCons state.

# After the file is read, we have:
#    a global dependency tree of the entire system,
#    consisting of a tree of Node objects. A Node is usually a
#    filesystem object, but can be an Alias or a Value node.
#    Each Node contains:
#         - a pointer to the corresponding Environment object
#         - a command to execute to build that node,
#         - a list of dependencies.
# Note the dependency tree may not be complete at this point;
#    for example, source files which are generated as part of the build
#    will be scanned for more dependencies before building the targets that depend on them.

command line arguments are "expanded" into a list of Nodes that we want built
      # if the argument is a file, then a single file is built
      # if the argument is a directory, then everything within that directory is built
      # if an argument is an Alias, then everything the Alias names is built
      # There are also default targets; ones specified with Default() and -u/-U and if nothing else, '.'.

if there is nothing to build, we're done

foreach Node:
      recursively build all of its dependencies
      check source dependencies for the Node
          # check the .sconsign file
          # use MD5 or signature method
      if out of date, or MD5 mismatch
           build the target using its associated command(s) and Environment
           # The commands in the Node do the actual work in the build phase,
           # normally by expanding an Env variable and passing it to a shell.
```

# Categories of Commands

The commands you can use in the SConstruct or SConscript files can be categorized in by their intent: 

* Node Commands  
* Admin/Bookkeeping Commands
* Actions

A complete reference of commands in on the [Man page](http://www.scons.org/doc/HTML/scons-man.html). 

# Node Commands

These commands are used to create Nodes. They all return a Node or a list of Nodes. 

Nodes are created by: 

* building a target 
* naming an existing target 
* specifying a pseudo target 
* composition of other existing targets 

These commands actually build stuff. They can affect files and directories on the file-system. Note they only define how to build, but don't actually do anything (i.e. on the filesystem) at the time they are called. The actual building is only done if the target is part of the final target Node list (see the process above). 

**File system** | **Description**
---------------:|:---------------
[Dir()](Dir()) |  a node representing a directory
[Dir()](Dir()) |  a node representing a directory
[File()](File()) | a node representing a file
**Pseudo targets** | **Description**
[Alias()](Alias()) | creates one or more phony targets that expand to one or more other targets
[Value()](Value()) | creates a node based on a string. If the string changes then the Value node is "out of date"
**Common build objects** | **Description**
[Program()](Program()) | build an executable from one or more object files, or C, C++, D or Fortran source files
[StaticLibrary()](StaticLibrary()) | builds a library file; .a in POSIX or .lib in Win32
[StaticObject()](StaticObject()) or [Object()](Object()) | builds an object file; .o in POSIX or .obj in Win32
[SharedLibrary()](SharedLibrary()) | builds a shared library; a .so on Posix, a .dll in Win32
**Win32 specific** | **Description**
[MSVSProject()](MSVSProject()) | generates MS Visual Studio project (.vcproj and .sln) files
[RES()](RES()) | build an MS Visual C++ resource .res file from a .rc file
[TypeLibrary()](TypeLibrary()) | builds Win32 type library .tlb from an input .idl file
**Java specific** | **Description**
[Java()](Java()) |  builds a java class file
[JavaH()](JavaH()) |  builds a C header and source file for building Java native methods
[RMIC()](RMIC()) | builds stub and skeleton files for remote objects from Java .class files
**Lex/Yacc specific** | **Description**
[CFile()](CFile()) | builds a C source file given a lex or yacc input file
[CXXFile()](CXXFile()) | builds a C++ source file given a lex or yacc input file
**Moc specific** | **Description**
[M4()](M4()) |  builds an output file from an M4 input file
[Moc()](Moc()) | builds an output file from an moc input file
[Uic()](Uic()) | builds a header, an implemenation and a moc file from a .ui file
**Documentation specific** | **Description**
[DVI()](DVI()) |  builds a .dvi file
[PDF()](PDF()) | builds a .pdf file from a .dvi, .tex, .ltx or .latex input file
[PostScript()](PostScript()) |  builds a .ps from a .dvi, .tex, .ltx or .latex input file
**Archive specific** | **Description**
[Tar()](Tar()) | builds a tar archive from files and/or directories
[Zip()](Zip()) | builds a zip file from files and/or directories
**Install** | **Description**
[Install()](Install()) | installs one or more files in a destination directory
[InstallAs()](InstallAs()) |  installs one or more files as specific file names
**CM tools** | **Description**
[SourceCode()](SourceCode()) | Arrange for non-existent source files to be fetched from a source code management system using the specified builder.
[BitKeeper()](BitKeeper()) | A factory function that returns a Builder object to be used to fetch source files using [BitKeeper](BitKeeper).
[CVS()](CVS()) | A factory function that returns a Builder object to be used to fetch source files from the specified CVS repository.
[Perforce()](Perforce()) | A factory function that returns a Builder object to be used to fetch source files from the Perforce source code management system.
[RCS()](RCS()) |  A factory function that returns a Builder object to be used to fetch source files from RCS.
[SCCS()](SCCS()) | A factory function that returns a Builder object to be used to fetch source files from SCCS.

# Admin/Bookkeeping Commands

These commands are for "admin" or bookkeeping purposes. They provide the "glue" between the various bits of the build system. Or from another perspective, they allow the entire build system to be decomposed into separate but coordinated parts. 

**Environment** | **Description**
---------------:|:---------------
[Environment()](Environment()) | Creates a new scons environment
[Copy()](Copy()) | Return a separate copy of a construction environment.
[Append()](Append()) | Appends the specified keyword arguments to the end of construction variables in the environment.
[AppendUnique()](AppendUnique()) | Appends the specified keyword arguments to the end of construction variables in the environment.
[Prepend()](Prepend()) | Prepends the specified keyword arguments to the beginning of construction variables in the environment.
[PrependUnique()](PrependUnique()) | Prepends the specified keyword arguments to the beginning of construction variables in the environment.
[Platform()](Platform()) | Returns a callable object that can be used to initialize a construction environment using the platform keyword of the Environment() method
[Tool()](Tool()) | Returns a callable object that can be used to initialize a construction environment using the tools keyword of the Environment() method. 
**Command-line and invocation** | **Description**
[Default()](Default()) | specifies one or more targets to build if not targets are specified on the command line
[Help()](Help()) | indicates what to display when -h is used on the command line
[Return()](Return()) | what to return when scons exits
[Exit()](Exit()) | exit from scons
[GetLaunchDir()](GetLaunchDir()) | Returns the absolute path name of the directory from which scons was initially invoked.
[GetOption()](GetOption()) | This function provides a way to query a select subset of the scons command line options from a SConscript file.
[SetOption()](SetOption()) | This function provides a way to set a select subset of the scons command line options from a SConscript file. 
**Run time environment** | **Description**
[SConsignFile()](SConsignFile()) | store the scons db in the given file
[EnsurePythonVersion()](EnsurePythonVersion()) | Ensure that the Python version is at least x.y
[EnsureSConsVersion()](EnsureSConsVersion()) | Ensure that the SCons version is at least x.y
[AppendENVPath()](AppendENVPath()) | Appends new path elements to the given path in the specified external environment (ENV by default)
[PrependENVPath()](PrependENVPath()) | Prepends new path elements to the given path in the specified external environment (ENV by default)
[GetBuildPath()](GetBuildPath()) | Returns the scons path name (or names) for the specified file (or files)
[SourceSignatures()](SourceSignatures()) | This function tells SCons what type of signature to use for source files: MD5 or timestamp.
[TargetSignatures()](TargetSignatures()) | This function tells SCons what type of signatures to use for target files: build or content. 
**Decomposition** | **Description**
[SConscript()](SConscript()) | reads another scons file
[Export()](Export()) | makes variables available to sconscript files
[Import()](Import()) | pulls in the values of exported variables
[BuildDir()](BuildDir()) | indicates that the build directory for a target
[SConscriptChdir()](SConscriptChdir()) | Enable/Disable changing working directory when in an SConscript file 
**Caching functions** | **Description**
[CacheDir()](CacheDir()) | Specifies that scons will maintain a cache of derived files in cache_dir
[Local()](Local()) | The specified targets will have copies made in the local tree, even if an already up-to-date copy exists in a repository.
[Repository()](Repository()) | Specifies that directory is a repository to be searched for files.
**Utility functions** | **Description**
[Dictionary()](Dictionary()) | Returns a dictionary object containing copies of all of the construction variables in the environment.
[FindFile()](FindFile()) | Search for file in the path specified by dirs. file may be a list of file names or a single file name.
[WhereIs()](WhereIs()) | Searches for the specified executable program, returning the full path name to the program if it is found, and returning None if not.
[Flatten()](Flatten()) | Takes a sequence (that is, a Python list or tuple) that may contain nested sequences and returns a flattened list containing all of the individual elements in any sequence.
[Split()](Split()) | Returns a list of file names or other objects.
[Literal()](Literal()) | The specified string will be preserved as-is and not have construction variables expanded

# Action Commands

These commands are used to perform actions, to specify when an action occurs, to prevent an action from occuring, affect the dependency tree, etc. 

**Dependency tree functions** | **Description**
---------------:|:---------------
[Depends()](Depends()) | Specifies an explicit dependency; the target file(s) will be rebuilt whenever the dependency file(s) has changed. 
[Clean()](Clean()) | This specifies a list of files or directories which should be removed whenever the targets are specified with the -c command line option. 
[AlwaysBuild()](AlwaysBuild()) | Marks each given target so that it is always assumed to be out of date, and will always be rebuilt if needed. 
[Ignore()](Ignore()) | The specified dependency file(s) will be ignored when deciding if the target file(s) need to be rebuilt. 
[Precious()](Precious()) | Marks each given target as precious so it is not deleted before it is rebuilt. Normally scons deletes a target before building it. 
[SideEffect()](SideEffect()) | Declares side_effect as a side effect of building target. 
**Generic command objects** | **Description**
[Scanner()](Scanner()) | Creates a Scanner object for the specified function. You can use the Scanner function to define objects to scan new file types for implicit dependencies. 
[Builder()](Builder()) | Creates a Builder object for the specified action. In general, you should only need to add a new Builder object when you want to build a new type of file or other external target. 
[Action()](Action()) | Creates an Action object for the specified action. These are similar in concept to "tasks" in the Ant build tool, although the implementation is slightly different. These functions do not actually perform the specified action at the time the function is called, but instead return an Action object that can be executed at the appropriate time. 
[Execute()](Execute()) | Executes an Action object immediately (at the time the command is read)
[AddPostAction()](AddPostAction()) | Arranges for the specified action to be performed after the specified target has been built. 
[AddPreAction()](AddPreAction()) | Arranges for the specified action to be performed before the specified target is built. 
**Actions** | **Description**
[Chmod()](Chmod()) | Returns an Action object that changes the permissions on the specified dest file or directory to the specified mode. 
[Copy()](Copy()) | Returns an Action object that will copy the src source file or directory to the dest destination file or directory.
[Delete()](Delete()) | Returns an Action that deletes the specified entry, which may be a file or a directory tree.
[Mkdir()](Mkdir()) | Returns an Action that creates the specified directory dir 
[Move()](Move()) | Returns an Action that moves the specified src file or directory to the specified dest file or directory. 
[Touch()](Touch()) | Returns an Action that updates the modification time on the specified file 
** Uncategorized** | **Description**
[Configure()](Configure()) | Creates a Configure object for integrated functionality similar to GNU autoconf 
[ParseConfig()](ParseConfig()) | Calls the specified function to modify the environment as specified by the output of command. 

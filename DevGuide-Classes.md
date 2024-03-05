

# Overview of SCons Modules and Classes

This is essentially a brain dump of key facts about the various classes that make up the SCons internals.  There's been talk that some of this information more properly belongs in some of the other Architecture sections.  If so, cool--feel free to edit or move this stuff around as makes sense.

There are TODO sections here that list various architectural ideas that have been hanging around in the ether (or SK's head) for a while.  Some of them are small, some are big.  If you want to dive in on something architectural, feel free to tackle one of these.  It would be a good idea to discuss it first on the scons-dev mailing list, just to make sure that no one else is already duplicating the effort, and that the idea still makes sense.  (Architectural directions may have changed over time.)

PLEASE feel free to ask clarifying questions, either on scons-dev, or by editing your question into the wiki.  Also feel free to add your own clarifications (it's a wiki, after all).

[Added by JGN 2007/02/05] This is effectively a first draft of a Module Overview, except that it focuses on classes rather than collection of classes.  I'm leaving it with this name for the time being, but eventually it should grow sub-pages for each module.  I've also added an clearly-incorrect initial guess of the classes that should be under each topic.  I just took the classes that occur at the top level (_i.e._, classes where the `class` declaration has no indentation), so optional classes, or classes whose contents are generated dynamically are not represented.  It also includes internal classes that should not be part of the API.


## Action

An `Action` is an object that actually controls the creation of one or more targets in the real world (on disk) from zero or more sources.  There are two main flavors: `CommandAction`, which builds targets by executing a command, `FunctionAction`, which builds targets by executing a Python function.  There is a `ListAction` container that can encapsulate a list of other `Actions` and allow other objects (primarily `Executor`) to treat them as a more-or-less atomic list.

* `Action`
   * `ActionBase`
   * `ActionCaller`
   * `ActionFactory`
   * `CommandAction(_ActionAction)`
   * `CommandGeneratorAction(ActionBase)`
   * `FunctionAction(_ActionAction)`
   * `LazyAction(CommandGeneratorAction, CommandAction)`
   * `ListAction(ActionBase)`
   * `_ActionAction(ActionBase)`
   * `_Null`
* TODO
   * Explore getting rid of a separate `ListAction` class, or rather have everything be a `ListAction`, with single actions just being `ListAction` objects with one entry.  This would make `ListAction` different from `CommandAction`+`FunctionAction`, but might allow us to simplify the APIs because `ListAction` would be the only "public" interface.

## Builder

A `Builder` is probably the most visible object to the `SConscript` writer, being the thing that gets called to describe that you want a given set of targets built from a given set of sources.  A `Builder` used to be responsible for actually executing the underlying `Action` objects when the time came to walk the dependency graph and really build the file, but that proved to be a problem because a `Builder` may typically be called many times (to build many programs or object files), and each of those may be called through a different construction environment or with different overrides.  Now all a `Builder` call really does is translate its arguments into `Nodes` and set up an `Executor` object, which is the thing that actually holds the necessary associations so we can calculate once and only once the information necessary to decide whether a target (or list of targets) needs to be rebuilt.

* `Builder`
  * `BuilderBase`
  * `CallableSelector(SCons.Util.Selector)`
  * `CompositeBuilder(SCons.Util.Proxy)`
  * `DictCmdGenerator(SCons.Util.Selector)`
  * `DictEmitter(SCons.Util.Selector)`
  * `EmitterProxy`
  * `ListEmitter(UserList.UserList)`
  * `OverrideWarner(UserDict.UserDict)`
  * `_Null`

## Defaults

* `Defaults`
  * `NullCmdGenerator`
  * `Variable_Method_Caller`

## Configuration (SConf.py)

* `Configuration (SConf.py)`
  * `CheckContext`
  * `ConfigureCacheError(SConfError)`
  * `ConfigureDryRunError(SConfError)`
  * `SConf`
  * `SConfBuildInfo(SCons.Node.FS.FileBuildInfo)`
  * `SConfBuildTask(SCons.Taskmaster.Task)`
  * `SConfError(SCons.Errors.UserError)`
  * `SConfWarning(SCons.Warnings.SConsWarning)`
  * `Streamer`

## Environment

There are two main construction environment classes, `Environment.Base` and `Environment.SubstitutionEnvironment`.  Confusingly enough, `SubstitutionEnvironment` is actually the base class.  We started out with just the `Environment.Base` class, and it contained a lot of stuff.  However, we publicized the idea that you could just subclass `Environment.Base` and re-assign to it in order to get your own customized construction environment, and people started using it.  But because it was the one base class, it started getting a lot of stuff jammed into it.  At some point, we decided it would be good to have a *really* minimal base class that behaved like a construction environment (in particular, had the necessary methods for our variable substitution), but wasn't populated with the `Builder`s and method calls that had already become attached to the `Environment.Base` class.  Consequently, the methods in `SubstitutionEnvironment` ended up getting factored out.  At some point, it would probably be nice to swap names, but we have the backwards compatibility issues to consider.

* TODO
  * Rename `SubstitutionEnvironment` to `Base` and `Base` to ???  (figure out backwards compatibility issues...)
  * Investigate turning this back into a subclass of `UserDict`.  A comment there says we don't make it a `UserDict` for performance reasons, but those reasons may no longer be valid, or we might be able to get the benefits of the standard `UserDict` by overriding one or two methods that exhibit performance issues.
* `Environment`
  * `Environment.py`
    * `Base(SubstitutionEnvironment)`
    * `BuilderDict(UserDict)`
    * `BuilderWrapper`
    * `OverrideEnvironment(Base)`
    * `SubstitutionEnvironment`
    * `_Null`
  * `Subst.py`
    * `CmdStringHolder(UserString.UserString)`
    * `Literal`
    * `NLWrapper`
    * `SpecialAttrWrapper`
    * `Target_or_Source`
    * `Targets_or_Sources(UserList.UserList)`

## Exceptions

(((Probably should be discussed in the module that throws them)))

* `Exceptions`
  * `Errors/BuildError(Exception)`
  * `Errors/ExplicitExit(Exception)`
  * `Errors/InternalError(Exception)`
  * `Errors/StopError(Exception)`
  * `Errors/TaskmasterException(Exception)`
  * `Errors/UserError(Exception)`
  * `Warnings/CacheWriteErrorWarning(Warning)`
  * `Warnings/CorruptSConsignWarning(Warning)`
  * `Warnings/DependencyWarning(Warning)`
  * `Warnings/DeprecatedWarning(Warning)`
  * `Warnings/DuplicateEnvironmentWarning(Warning)`
  * `Warnings/MisleadingKeywordsWarning(Warning)`
  * `Warnings/MissingSConscriptWarning(Warning)`
  * `Warnings/NoMD5ModuleWarning(Warning)`
  * `Warnings/NoMetaclassSupportWarning(Warning)`
  * `Warnings/NoParallelSupportWarning(Warning)`
  * `Warnings/ReservedVariableWarning(Warning)`
  * `Warnings/Warning(SCons.Errors.UserError)`

## Executor

This is the object that really controls execution of an `Action` object (or list of `Action` objects) to build a list of targets.  `AddPreAction()` and `AddPostAction()` are handled here.  Once upon a time, `Action` execution was handled more-or-less directly by the `Builder`s themselves.  The problem with that was a `Builder` will get called multiple times to build multiple targets, through different construction environments and with different construction-variable overrides.  When that information was spread out in the other objects, and you had a list of target files, we had to assemble the information repeatedly and re-calculate it for each target in the list.  An `Executor` allows us to calculate the `Action` signature once, and to apply an up-to-date status of all of the targets built when the `Executor` is invoked.

* `Executor`
  * `Executor`
  * `Null(_Executor)`

## Job (see Taskmaster)


## Memoization

* `Memoizer`
  * `A`
  * `CountDict(Counter)`
  * `CountValue(Counter)`
  * `Counter`
  * `M`
  * `Memoizer`
* TODO
  * Get rid of `Memoizer` class, looks like it's left over

## Node

This is the big, hairy center of things.  The whole `Node` class structure has gotten unwieldy as we've shoved more things into it over time and it would be really, really good to refactor it to make it easier to work with.  (Maybe this XXX TEXT MISSING

The basic idea behind the `Node` class hierarchy is to separate the dependency management methods and attributes from the methods and attributes that represent the real-world thing that the `Node` represents (the file, directory, Python value...).  The way in which we did this, though, was to make the dependency management layer the base class (`Node.Node`) and then derive subclasses for the `Nodes` that represent real-world things (`Node.FS.File`, `Node.FS.Dir`, `Node.Python.Value`, _etc._).

* `Nodes`
  * `Node/`
    * `BuildInfoBase`
    * `Node`
    * `NodeInfoBase`
    * `Walker`
    * `Alias/Alias(SCons.Node.Node)`
    * `Alias/AliasBuildInfo(SCons.Node.BuildInfoBase)`
    * `Alias/AliasNameSpace(UserDict.UserDict)`
    * `Alias/AliasNodeInfo(SCons.Node.NodeInfoBase)`
    * `FS/Base(SCons.Node.Node)`
    * `FS/BuildInfo(FileBuildInfo)`
    * `FS/Dir(Base)`
    * `FS/DirBuildInfo(SCons.Node.BuildInfoBase)`
    * `FS/DirNodeInfo(SCons.Node.NodeInfoBase)`
    * `FS/DiskChecker`
    * `FS/Entry(Base)`
    * `FS/EntryProxy(SCons.Util.Proxy)`
    * `FS/FS(LocalFS)`
    * `FS/File(Base)`
    * `FS/FileBuildInfo(SCons.Node.BuildInfoBase)`
    * `FS/FileFinder`
    * `FS/FileNodeInfo(SCons.Node.NodeInfoBase)`
    * `FS/LocalFS`
    * `FS/NodeInfo(FileNodeInfo)`
    * `FS/RootDir(Dir)`
    * `FS/_Null`
    * `Python/Value(SCons.Node.Node)`
    * `Python/ValueBuildInfo(SCons.Node.BuildInfoBase)`
    * `Python/ValueNodeInfo(SCons.Node.NodeInfoBase)`
  * `Sig/`
    * `Calculator`
    * (((clearly missing some)))
* TODO
  * Explore refactoring the `Node` class hierarchy to use delegation instead of inheritance for the relationship between the dependency-management parts of a `Node` and the real-world parts of a `Node`.

## Options

* `Optik`
  * `BadOptionError(OptikError)`
  * `OptikError(Exception)`
  * `Option`
  * `OptionConflictError(OptionError)`
  * `OptionError(OptikError)`
  * `OptionParser`
  * `OptionValueError(OptikError)`
  * `Values`
* `Options`
  * `Options`
  * `_ListOption(UserList.UserList)`
  * `_PathOptionClass`

## PathList

This is a newer class to encapsulate lists of directory `Nodes`.  Its purpose in life is to try to cache lookups of different path lists of directories (the things like `$CPPPATH`, `$LIBPATH`, etc.) so that we can avoid searching for directories (turning strings into `Nodes`) for different construction environments that use the same values while still delaying evaluation of the construction variables.  We don't try to do a perfect job of detecting duplicates, we just want to be good enough to save cycles.

* `PathList`
  * `PathListCache`
  * `_PathList`

## Platform

* `Platform`
  * `PlatformSpec`
  * `TempFileMunge`

## SConsign

* `SConsign`
  * `SConsign.py`
    * `Base`
    * `DB(Base)`
    * `Dir(Base)`
    * `DirFile(Dir)`
  * `dblite.py`
    * `dblite`

## Scanner

* TODO
      * Explore really separating the two parts of what we mean by "scanning:"  the part that opens the file and looks for `#include` lines, and the part that searches directory lists (`PathList` objects) for existing or to-be-built dependency files.
* `Scanner`
  * `Scanner.py`
    * `Base`
    * `Classic(Current)`
    * `ClassicCPP(Classic)`
    * `Current(Base)`
    * `D(SCons.Scanner.Classic)`
    * `F90Scanner(SCons.Scanner.Classic)`
    * `FindPathDirs`
    * `LaTeX(SCons.Scanner.Classic)`
    * `Selector(Base)`
    * `_Null`
  * `cpp.py`
    * `DumbPreProcessor(PreProcessor)`
    * `FunctionEvaluator`
    * `PreProcessor`

## Script

* `Script`
  * `TargetList(UserList.UserList)`
  * `Main/BuildTask(SCons.Taskmaster.Task)`
  * `Main/CleanTask(SCons.Taskmaster.Task)`
  * `Main/CountStats(Stats)`
  * `Main/MemStats(Stats)`
  * `Main/OptParser(OptionParser)`
  * `Main/QuestionTask(SCons.Taskmaster.Task)`
  * `Main/SConscriptSettableOptions`
  * `Main/Stats`
  * `Main/TreePrinter`
  * `SConscript/DefaultEnvironmentCall`
  * `SConscript/Frame`
  * `SConscript/SConsEnvironment(SCons.Environment.Base)`

## Taskmaster

There are two parts, one is the `Taskmaster` class itself.  It's only responsible for walking the dependency graph and deciding when a given `Node` is ready to be evaluated (for whether it's up-to-date or must be rebuilt).  A `Node` is ready for evaluation when all of its children (if any) are up-to-date.  As part of determining a `Node's` current list of children, the `Node` and its source files may be scanned for implicit dependencies.

The second part is the `Task` class, which handles a `Node` after the `Taskmaster` has decided it's ready for evaluation.  It controls whether or not the must be checked or whether the `Node` should always be "built."  The `Task` class is intended to be sub-classed by the wrapping interface to provide custom behavior, such as whether or not a message should be printed if a target is up-to-date, how exceptions should be handled, _etc_.

* `Taskmaster`
  * `Taskmaster.py`
    * `Stats`
    * `Task`
    * `Taskmaster`
  * `Job.py`
    * `Jobs`
    * `Parallel`
    * `Serial`

## Tool

* `Tool`
  * `Tool`
  * `fortran/VariableListGenerator`
  * `intelc/IntelCError(SCons.Errors.InternalError)`
  * `intelc/MissingDirError(IntelCError)`
  * `intelc/MissingRegistryError(IntelCError)`
  * `intelc/NoRegistryModuleError(IntelCError)`
  * `linkloc/LinklocGenerator`
  * `msvs/Config`
  * `msvs/_DSPGenerator`
  * `msvs/_DSWGenerator`
  * `msvs/_GenerateV6DSP(_DSPGenerator)`
  * `msvs/_GenerateV6DSW(_DSWGenerator)`
  * `msvs/_GenerateV7DSP(_DSPGenerator)`
  * `msvs/_GenerateV7DSW(_DSWGenerator)`
  * `mwcc/MWVersion`
  * `qt/GeneratedMocFileNotIncluded(ToolQtWarning)`
  * `qt/QtdirNotFound(ToolQtWarning)`
  * `qt/ToolQtWarning(SCons.Warnings.SConsWarning)`
  * `qt/_Automoc`

## Utility

* `Utility`
  * `Util.py`
    * `CLVar(UserList)`
    * `CallableComposite(UserList)`
    * `DisplayEngine`
    * `LogicalLines`
    * `NodeList(UserList)`
    * `OrderedDict(UserDict)`
    * `Proxy`
    * `Selector(OrderedDict)`
  * `compat/`
    * `_UserString/UserString`
    * `_subprocess/Popen(object)`
    * (((clearly some missing)))

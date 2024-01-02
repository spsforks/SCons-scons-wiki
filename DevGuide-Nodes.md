# SCons Nodes


## Types of Nodes

The overriding principle here is that stuff related to managing dependencies goes in the `Node.Node` base class, and stuff about the actual real-world object that the Node represents goes in a specific subclass for the type of object (`File`, `Dir`, Python `Value`, _etc._). 

In retrospect, inheritance may not have been the right choice here.  Over time, a _lot_ of stuff has gotten shoved into these classes, and they really need some surgery to split them up into more manageable chunks. 


### Node.Node Class

`Node.Node` is the base class for all derived Nodes.  As mentioned, it contains the stuff related to dependency management.  The intent is to (try to) abstract dependency management well enough that you can have any Node depend on any other Node, regardless of what kind of real-world objects they represent.  To the extent that you can, in fact, have a file depend on a Python value, we succeeded.  To the extent that this part of the code is unwieldy or slow, well, it can stand improvement. 


### Node.FS.Base Class

`Node.FS.Base` is derived from `Node.Node` and is the base class for Nodes that represent things in the file system.  This contains common methods that we want available regardless of whether the underlying filesystem entry is a `Dir` or a `File` (or if we don't yet know which it will be). 


### Node.FS.Entry Nodes

`Node.FS.Entry` is derived from Node.FS.Base and is a generic Node that will be either a `Dir` _or_ a `File`, but we don't yet know what it will become.  This mainly allows Builder calls to be declarative with respect to the type of the Node they handle.  This trivial example shows how it works:  
 `    env.Command('outdir', 'infile', 'cp $SOURCE $TARGET')`  
 `    env.Dir('outdir')` 

If we didn't delay disambiguation, then the `env.Command()` call would have to make some assumption at the time it's called, or people would be required to disambiguate explicitly when calling it, which would be a pain.  (Individual Builders can, of course, specify that they only deal with `File`s, or `Dir`s, in which case the underlying Builder call will check the types and issue errors if there's a mismatch.) 

There aren't that many methods specific to the `Entry` class, and they're mostly concerned with calling the disambiguation logic when appropriate and morphing the `Entry` into a `Dir` or `File`, as appropriate. 


### Node.FS.Dir Nodes

`Node.FS.Dir` is derived from `Node.FS.Base` and represents an actual on-disk directory.  SCons treats the contents of the directory as implicit dependencies, specifically using scanner objects to populate the implicit dependency list.  The upshot is that all of the entries within a directory must be up-to-date for the directory itself to be considered up-to-date.  There are two directory scanners available.  The default directory scanner only "scans for" the in-memory Nodes within the `entries` list (that is, the things SCons already knows about from other Builder calls and the like).  The second scanner, which is available in the SConscript namespace as `DirScanner`, can be attached as a `source_scanner` for any target that depends on a directory, and actually adds implicit dependencies for all entries in the on-disk directory. 

`Dir` nodes do not have build information stored in the `.sconsign` file between runs. 


### Node.FS.File Nodes

`Node.FS.File` is derived from `Node.FS.Base` and represents an on-disk file.  It is the backbone of what happens. 

(((TODO))) 


### Node.Alias Nodes

`Node.Alias` is derived from `Node.Node` and (((TODO))) 


### Node.Value Nodes

`Node.Value` (often called a _Python value_) is derived from `Node.Node` and (((TODO))) 


## Setting up a Node

(((e.g., implemented in `Node.Node` layer, primarily for building the DAG))) 


### Locating the Node

(((The Node's _name_ (a text string) may be used to locate the node by ...))) 


### Sources

Sources are the names that `"$SOURCES"` expands into.  They are usually set by the Builder.  (((TODO))) 

(((sources are added by calling `Node.add_source(source)`, where `source` is either a Node or a list of Nodes; the (read-only) list of unique sources is `Node.sources`. ...))) 


### Dependencies

Explicit dependencies are other requirements that must be done before this Node can be built.  (((TODO))) 

(((explicit dependencies are added by calling `Node.add_dependency(depend)`, where `depend` is either a Node or a list of Nodes; the (read-only) list of unique sources is `Node.depends`.  ...))) 


### Ignored

Ignored dependencies are a list of the Nodes that are ignored when examining dependencies of this Node.  Used in two places, to prune the nodes returned by `Node.Node.children()`, and by `Node.Node.gen_binfo()` to keep ignored dependencies out of the signature calculation. 

(((ignored dependencies are added by calling `Node.add_ignore(depend)`, where `depend` is either a Node or a list of Nodes; the (read-only) list of unique sources is `Node.ignore`.  ...))) 


### Side-effects

The side-effects list contains Nodes that are updated when this Node is run.  It is used by the `Taskmaster` to prevent multiple tasks from updating a side-effect at the same time. 

(((unlike other node actions, side-effects are directly inserted into a Node by `Environment.SideEffect(side_effect, target)`, where both `side_effect` and `target` are a name, a Node, or a list of either.  The (read-only) list of side-effects is `Node.side_effects`.  ...))) 


### Builders

Builders are (((TODO))) (((ref to page discussing builders))) 

(((builders are set up by ...))) 


### Scanners

Scanners are used to determine implicit dependencies.  There are two different types of scanners.  (((TODO)))  (((ref to page discussing scanners))) 

**Source scanners** are scanner objects run on the source(s) of a target that do the whole shebang of opening a source file to look for `#include` lines and then searching the FS nodes (and maybe on disk) to find the actual FS Nodes that those `#include` imply are dependencies, based on the value of (_e.g._) `$CPPPATH` that is being used to build the target in question. 

(((source scanners are set up by ...))) 

**Target scanners** are scanner objects run on the target(s) of a build; they have been attached to a node because certain things have to be sought whenever it's built.  The canonical example here is search `$LIBPATH` for the libraries specified in the `$LIBS` variable.  We don't have to open up a file and look for `#include` lines, but we do have to search the FS Nodes (and maybe on disk) for the libraries that the executable depends on. 

(((target scanners are set up by ...))) 


### Executors

Executors are (((TODO)))  (((ref to page discussing executors))) 

(((executors are set up by Builder calls.  ...)))  _(((Yes, Builders would call `set_executor()` to set it, and everyone else can call `get_executor()` to retrieve it, but who calls `executor_cleanup()` or `reset_executor()`?  Are they only for internal use?)))_ 


### Fetching Dependencies

Even though the sources, explicit dependencies, and implicit dependencies are stored in separate lists, they're typically not referenced separately by outside code.  Read-only access to these lists should be safe; that wasn't a specific design criteria, but if they're not, it should be fixed. 

The main dependency-fetching methods are: 

* `Node.all_children(scan = 1)`: the union of the sources, explicit dependencies, and implicit dependencies, used when a caller needs to know about all of them. 
* `Node.children(scan = 1)`: the list returned by `Node.all_children()` minus any ignored dependencies. 
Both of these methods will, by default, cause a scan for the implicit dependencies of the Node to be invoked, if necessary.  This made for convenient coding once upon a time, because callers could just use the above methods without having to worry about whether a Node had been scanned or not, but this is probably a bad idea.  Scanning is potentially expensive enought that it should really happen in a controlled and explicit manner, not as a side effect of querying a Node for information. 


## Node Signatures

(Note:  The elusive [BigSignatureRefactoring](BigSignatureRefactoring) is/was supposed to have cleaned up some of this mess by changing how we handle all of these signatures, pretty significantly, but that's been on the back burner a long time now and the code base has diverged a good bit.) 


### NodeInfo Objects

An object derived from `NodeInfoBase` stores the individual signature information for a specific Node.  Unfortunately, this whole area is pretty messy right now.  We've been trying to keep the base class "dependency layer" separate from the "real-world" layer of the subclasses, but `NodeInfo` objects are one place where the line gets blurry with the result of a fair amount of back-and-forth calls between the methods of these layers. 

In a nutshell, the signature information for a Node can consist of up to the following parts: 

* **build signature**:  Fetch this with `get_bsig()`.  This is supposed to be subclass-independent, so it comes from some complicated logic in the `Node.Node.gen_binfo()` method. 
* **content signature**: Fetch this with `get_csig()`.  There's a base class `Node.Node.get_csig()`, but there's also a subclass-specific `Node.FS.File.get_csig()` method because the File logic is more complicated, involving looking at timestamps and cached values. 
* **timestamp**:  Fetch this with `Node.FS.Base.get_timestamp()`, which generates it if necessary.  It gets stored in a `FileNodeInfo` object by that object's `update()` method. 
* **size**:  Fetch this with `Node.FS.Base.getsize()`, which generates it if necessary.  It gets stored in a `FileNodeInfo` object by that object's `update()` method. 

### BuildInfo Objects

Each target file has a Node-specific subclass of a `BuildInfoBase` object stored in the `.sconsign` file.  In the same way that real-world-object-specific Nodes are subclasses of the base `Node.Node` class, each `Node.Node` subclass should have a corresponding `BuildInfoBase` subclass that's specific to its type of real-world object.  The `BuildInfo` object contains a `NodeInfo` object for each dependency.  It records "The last time this target was built, these particular {sources, explicit dependencies, implicit dependencies} had exactly _these_ characteristics." 

The `BuildInfoBase` class itself controls information that is supposed to be independent of any specific real-world subclass.  This includes: 

* **explicit sources**:  list of `NodeInfo` objects for the sources used to last build this target (i.e., stuff that came from the Builder call for this target). 
* **explicit dependencies**:  list of `NodeInfo` objects for the explicit dependencies when this target was last built (that is, stuff that came from `env.Depends()` calls for this target. 
* **implicit dependencies**:  list of `NodeInfoB` objects for the implicit dependencies the last time the target was built (that is, the stuff found when scanning this target and its sources). 
* **actions**: signature info for the `Action` object(s) used to last build this target. 
Even if a real-world Node subclass doesn't have any subclass-specific dependency processing, it still gets its own `NodeInfoBase` subclass so that the type of the object when stored in the `.sconsign` file will match the type of the underlying Node last time. So if a given on-disk entry was a Dir last time and the configuration changes and it's a File this time, we won't mistakenly try to match the `DirBuildInfo` from the `.sconsign` file with the `FileBuildInfo` this run. 

Ignored dependencies are taken out of the above lists of sources, explicit dependencies, and implicit dependencies.  They don't get stored in the `.sconsign` file at all. 


## Stuff that belongs elsewhere

Walking the dependency tree is the responsibility of the Taskmaster and should be moved there. Scanning for implicit dependencies could easily be supervised by by the Executor and should be moved there. 

**(((SK:  If I understand correctly, Greg's idea here is to treat the Node class as a smart cache.  It would still do the scans and cache the results, but instead of updating the dependencies directly and doing tree-walks, it would report the result to a higher level which would make the decisions about what to do with them.  The Taskmaster is what walks the DAG, so it would ask the Executor to have the Node scanned and find the dependencies, then it would manage things without getting intertwined with the Node or Executor internals.)))** 


### Walking the Dependency Tree

(((TODO))) 


### Scanning for Implicit Dependencies

This is another area where things have gotten more complicated than is good. 

Before we begin, keep in mind that there are really two key stages to what SCons (currently) calls "scanning".  A scan is done by a _subject_ Node (either a source or a target) at the request of the Executor controlling the build. 

* Opening up a file and searching the contents for (_e.g._) `#include` lines; the result is a set of "raw" include names.  _(((??? the result of the scan is cached [? by the subject Node] so the scan is only done once for each distinct scanner. ???)))_ 
* Looking through SCons' in-memory FS Nodes, and maybe on disk, to convert the "raw" include names into the exact path to a file on which the target implicitly depends.  _(((??? this is done for the target's Environment and search list; the result of the scan is cached [? by the subject Node] so the scan is only done once for each distinct build environment. ???)))_ 
**(((SK:  hmm... that's the intent, but it looks like we actually do both of these for each (env,scanner,path) triple... to the extent that a scanner hypothetically could vary its output per path, that needs to be allowed for, but that might mean that we actually ARE opening up files multiple times... let me dig into this...)))** _(((JGN:  I suspect that the env and the path are redundant, so only one or the other should be used.  I don't know if an override environment would create a different key, but I suspect that it would, so the cache key should be the path.)))_ 

Here's an overview of what happens.  Scanning goes through the following layers, with the following purposes: 

* `Node.Node`:  In the target Node, use cached implicit dependencies from the `.sconsign` file if so configured. 
* `Executor`: aggregate lists of target files being built from lists of source files, so we don't have an NxM calling tree from calling each source file once for each target. 
* `Node.Node`: In the target Node, handle re-invocation of a scanner object on nodes found for its `#include` lines. 
* `Node.FS.File`: In the source Node, actually call the scanner object. 
Here are the details: 

* Something decides that a Node needs to be scanned for implicit dependencies and calls the target's `Node.scan()`.  (This is currently most often a side effect of calling `Node.all_children()` or `Node.children()`, although it can also come from `Node.gen_binfo()`, which does its own independent reaching into the different source+dependency lists.) 
* `Node.scan()` will, if the `--implicit-cache` option is in force, short-circuit all the rest of this stuff and just use the list implicit dependencies from the `.sconsign` file. 
* Otherwise, `Node.scan()` will end up calling `Executor.scan_sources()` to use the appropriate source scanner on the sources of this build and `Executor.scan_targets()` to use the appropriate target scanner on the targets of this build.  Both of them call the underlying...
    * `Executor.scan()` method, which contains common logic to (_e.g._) look for the right scanner for the different file suffixes.  For each Node involved, the executor calls... 
        * `Node.get_implicit_deps()`, which exists so that (in theory) the underlying scanner object can just open and search for `#include` lines in a single file, and `Node.get_implicit_deps()` can handle re-invoking the appropriate scanner on the files found for the `#include` lines.  (In retrospect, this was probably an architectural mistake; it would probably be cleaner to just let the scanner itself handle all of that re-invocation, much like a C preprocessor itself would.)  For each TEXT MISSING. 
            * `Node.FS.File.get_found_includes()`, which actually handles invocation of a scanner object on this particular type of Node.
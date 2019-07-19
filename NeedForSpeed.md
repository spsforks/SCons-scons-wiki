# The Need For Speed
## How Can We Make SCons Faster

<!-- TOC -->
<a name="contents">

 - [Introduction](#introduction)
 - [Python code usage](#python-code-usage)
 - [Start up time](#start-up-time)
 - [Improved DAG traversal](#improved-dag-traversal)
 - [Serial DAG traversal](#serial-dag-traversal)
 - [The Dependency Graph is the Python Object Graph](#the-dependency-graph-is-the-python-object-graph)
 - [CacheDir](#cachedir)
 - [SConsign generation](#sconsign-generation)
 - [Configure check performance:](#configure-check-performance)
 - [Variable Substitution](#variable-substitution)
 - [Process Spawning](#process-spawning)
 - [Environment Creation](#environment-creation)
 - [General Thoughts from Jason Kenny](#general-thoughts-from-jason-kenny)
<!-- /TOC -->

### Introduction

Performance is one of the major challenges facing SCons. When compared with other current options, particularly Ninja, in many cases performance can lag significantly. That said other options by and large lack the extensibility and many features of SCons.

Performance is always a tricky subject. It is oft said that premature optimization is the root of all evil (Knuth) but as SCons approaches 20 years old it's hard to say optimization based on observed problem areas is premature.  Of course a great deal of optimization has already been done on SCons code paths, so there isn't a lot of low-hanging fruit to pick. Performance is also relative:  SCons mainly asks other tools to do the real work, and in many cases, particularly small builds, the time SCons takes to figure out what it needs to do is dwarfed by the time spent once SCons calls out to the operating system to get `gcc` or `cl.exe` to actually compile a file. So it is important to measure on meaningful workloads.

Performance issues can be roughly divided into:
 * The code is doing too much work.  For example, recomputing internal things that could have been saved from a previous build, repeating operations many times, not reusing build artefacts that might have been available, etc. Roughly speaking, "caching" and "memoizing". SCons does a lot of that already.
 * The code is doing work is has to, but slowly. This might include small language inefficiencies, too much recursion or otherwise deeply nested execution contexts, etc.  Certianly, running a scanner over all the dependencies in a project with thousands of files takes some time. Profiling the code helps identify these areas.
 * The build configuration is suboptimal, causing scons to work inefficiently. This case is out of the control of the scons developers and won't be considered here, but should not be discounted when someone complains their build is too slow. It would be cool if a tool could detect poor sconscript style, but that's a non-trivial task.

Bill Deegan (SCons project co-manager) and Andrew Morrow (MongoDB) have been working together to understand some of the issues that lead to poor SCons performance in a real world (and fairly modestly sized) C++ codebase. The remaining sections capture some of the findings.

### Python code usage

There are many places in the codebase where while the code is correct, performance based on cpython’s implementation can be improved by minor changes.

* Examples
    * Using for loops and hashes to uniquify a list. Simple change in Node class yielded approximately 15% speedup for null build.
    * Using `if x.find(‘some character’) >= 0` instead of `if ‘some character’ in x` (timeit benchmark shows a 10x speed difference).
    * Whether EAFP or LBYL is better depends on the "hit" percentage: if a `try/except` takes the exception most times, then it probably costs more than doing a check up front, and vice versa. Don't even bother unless it's a piece of code that is called an awful lot.
    * SCons has its own memoization code, or rather it has a framework for measuring whether the memoization is working effectively. Again, if hit percentage is low and the saved computation isn't all the expensive, memoization may not pay off. Note: `functools.lru_cache` could be an effective alternative to homegrown memoization, but it's Py3-only.
    * Namespace lookups: it may be worth saving multilevel lookups (`SCons.Util.to_str` is going to be slower than `to_str`) if the reference happens in a loop where the line is executed frequently.
* Method to address
    * Profile the code looking for hotspots first with cprofile, then with line_profiler to examine the hotspot functions. Then look for best implementations of code. (Use timeit if useful to compare implementations. There are examples of such in the [benchmark directory](https://github.com/SCons/scons/tree/master/bench).

Special note on threading: Python is kind of famous for not getting as much speedup from threading as one might expect from capable machines with lots of cores.  This is because the Global Interpreter Lock (GIL) allows only one thread to be running Python code at a time.  However, the way SCons uses threading is not much affected by this - the threads are used in the Jobs module, and are used to spawn the external commands that drive the build - so from the point of view of Python, each running threat is "waiting for I/O" and not spending time blocked by the GIL.

[back to contents](#contents)

### Start up time

* A null incremental build is going to be the worst case for a build up to date, as we have to make sure all items are in a good state. Time to start building on diff should be a lot faster. SCons spends a lot of time having to read everything on second passes. We can use our cache much better to store states on what builds what, etc to avoid even having to read a file. If the file did not change we already know the node/builder tree it will provide. We already know the actions. We can start building items as soon as a MD5/time stamp check fails most of the time. Globs can store information about what it read and processed and only need to go off when we notice a directory timestamp. Avoiding processing build files and loading known state is much faster than processing the python code. My work (Jason Kenny) in Parts has shown this. The trick is knowing when you might have to load a file again to make sure custom logic get processed correctly.

* In the case of Parts it would be great to load file concurrently and in parallel. I think I have a way to go this concurrently which I have not done yet. The main issue is the node FS object tree is a sync point for being parallel.

[back to contents](#contents)

### Improved DAG traversal

One issue is that the DAG for doing builds is based on nodes. There is a bit of logic to deal with handing side effects and build actions that have multiple outputs. Greg Noel had made a push for something called TNG taskmaster. I understand now the main fix he was going for is to tweak SCons to navigate a builder DAG instead of Node DAG, the node DAG is great to get the main organization but after that it is generally trivial to make a DAG based on builder at the same time, Traversing this is much faster, we require less “special” logic and will be easier to parallelize.

* One big improvement this provides is that we only need to test if the sources or targets are out of date if the dependent builders are all up to date. If one of the is out of date, we just build, This vs we check each node and see if the build action has been done which requires extra scans and work in the current logic.
* Given a builder is out of data you just mark all parents out of date. We only care about builders in a set that we don’t know are out of date yet. Simple tweaks on how we go through the tree can mean we only need to touch a few nodes.

[back to contents](#contents)

### Serial DAG traversal

SCons walks the DAG to find out of date targets in a serial fashion. Once it finds them, it farms the work out to other threads, but the DAG walk remains serial. Given the proliferation of multicore machines since SCons’ initial implementation, a parallel walk of the DAG would yield significant speedup. Likely this would require implementation using the multiprocessing python library (instead of threads), since the GIL would block real parallelism otherwise. Packages like Boost where there are many header files can cause large increases in the size of the DAG, exacerbating this issue. There are two serious consequences of the slow DAG walk:

* Incremental rebuilds in large projects. Typical developer workflow is to edit a file, rebuild, test. In our modestly sized codebase, we see the incremental time to do an ‘all’ rebuild for a one file change can reach well over a minute. This time is completely dominated by the serial dependency walk.

* Inability to saturate distributed build clusters. In a distcc/icecream build, the serial DAG walk is slow enough that not enough jobs can be farmed out in parallel to saturate even a modest (400 cpu) build cluster. In our example, using ninja to drive a distributed full build results in an approximately 15x speedup, but SCons can only achieve a 2x speedup.

    * Method to address:
        * Investigate changing tree walk to generator
        * Investigate implementing tree walk using multiprocessing library

[back to contents](#contents)

### The Dependency Graph is the Python Object Graph

The target dependency DAG is modeled via python Node Object to Node Object linkages (e.g. a list of child nodes held in a node). As a result, the only way to determine up-to-date-ness is by deeply nested method calls that repeatedly traverse the Python object graph. An attempt is made to mitigate this by memoizing state at the leaves (e.g. to cache the result of stat calls), but this still results in a large number of python function invocations for even the simplest state checks, where a result is already known. Similarly, the lack of global visibility precludes using externally provided change information to bypass scans.
* See above re generator
* Investigate modeling state separately from the python Node graph via some sort of centralized scoreboarding mechanism, it seems likely that both the function call overhead could be eliminated and that local knowledge could be propagated globally more effectively.

[back to contents](#contents)

### CacheDir 

There are some issues listed below. End-to-end caching functionality of SCons, including generated files, object files, shared libraries, whole executables, etc., is one of its great strengths, but its performance has much room for improvement. 

* Existing bug(s) when combining CacheDir with MD5-Timestamp devalues CacheDir.
    * ~~https://github.com/SCons/scons/issues/2980~~

* Performance issues:
    * CacheDir re-creates signature data when extracting nodes from the Cache, even though it could have recorded the signature when entering the objects into the cache.

* Method to address
    * Store signatures for items in cachedir and then use them directly when copying items from Cache.
    * Fix the CacheDir / MD5-Timestamp integration bug

[back to contents](#contents)

### SConsign generation

The generation of the SConsign file is monolithic, not incremental. This means that if only one object file changed, the entire database needs to be re-written. It also appears that the mechanism used to serialize it is itself slow. Moving to a faster serialization model would be good, but even better would be to move to a faster serialization model that also admitted incremental updates to single items.
* (JK) I think this is a bigger deal for larger builds. I have found in Parts, as I store more data I would try to break up the items into different files. This helps, but in the end, at some point a pickle or JSON dump takes times. It also takes time to load them as in cases for builds I have had, loading 700mb files takes even the best systems a moment to do. This is a big waste when I only need to get a little bit of data. Likewise, the storing of the data could and should be happening as we build items. As noted we don’t have a good way to store a single item without storing all the file. If the file is large 100MB to GBs this can take time, as in many seconds, which in the end annoy users. I would say with what I do have working well in Parts that the data storage, retrieval is the big time suck. Addressing this would have the largest impact me.

* Method to address:
    * Replace sconsign with something faster than the current implementation, which is based on Pickle.
    * And/or Improve sconsign with something which can incrementally only write that which has changed.

[back to contents](#contents)

### Configure check performance

Even cached Configure checks seems slow, and for a complex configured build this can add significant startup cost. Improvements here would be useful.
* (JK) For me so far I try to avoid this feature as much as I can. However, it does have it uses. I feel from using automake at the moment SCons version is faster, but lacks some common features. The main issue I have seen is that a user can make complex logic that can run slow. For a project I am working on porting from automake, the item for me is if there is a better way to say this in SCons. At the moment it is a lot of code that is easy to break. I would like a better way to express this. I feel this could help address maintainability issues with configure logic as well as avoiding certain speed issues to better use Scons logic to check if we need to

* Method to address:
    * Code inspection, look for improvements
    * Profile

[back to contents](#contents)

### Variable Substitution

Currently variable substitution, which is largely used to create the command lines run by SCons, uses an appreciable percentage (approximately 18% for a null incremental build) of SCons’ CPU runtime. By and large much of this evaluation is duplicate (and thus avoidable work). For the moderate sized build discussed above there are approximately 100k calls to evaluation substitutions. There are only 413 unique strings to be evaluated. Consider that the CXXCOM variable is expanded 2412 times for this build. The only variables which are guaranteed unique are the SOURCES and TARGETS, all others could be evaluated once and cached.

* (JK) I abuse this in Parts to share data in a lazy fashion between components. It has been a sore point for me, given reason stated below. We have done some work to address the items by reusing states better. I can say there are some issues with the current code that causes memory bloat and wasted time. I don’t want to dwell on this, but will say that this is the second biggest item in my mind that would have a big impact to overall time to the user. I know I want to change the load logic in Parts to avoid using the substitution engine as much as possible.

* Prior work on this item:
    * [Previous Discussion](SubstQuoteEscapeCache/Discussion)
* Working doc on current and areas for improvement:
    * [New Approach](SubstQuoteEscapeCache/SubstImprovement2017)
* Method to address:
    * Consider pre-evaluating Environment() variables where reasonable. This could use some sort of copy-on-write between cloned Environments. This pre-evaluation would skip known target specific variables (TARGET,SOURCES,CHANGED_SOURCES, and a few others), so minimally the per command line substitution should be faster.

[back to contents](#contents)

### Process Spawning

* (JK) I add this as We had submitted a sub process fix for POSIX systems. The code effect larger builds more than smaller builds because of forking behavior. I don’t believe it been added to SCons as of yet.
* (JK) As a side design note, If we did make a multiprocessing setup for SCons, This might be less of an issue, as the “process” workers only need information about a build to run on. Changing of nodes state would have to be synced with the main process via messages as there would be no fast efficient way to share the whole tree across all the process.
* (JK) Another thought is we might want to look at some nested parallel strategies to make a task like setup that might allow us to use the TBB python library to avoid the GIL issue. However, given my time on SCons/Parts I think the change of a taskmaster to go over a builder DAG will have the biggest effect

[back to contents](#contents)

### Environment Creation

* (JK) It easy to define lots of different environment in a large build. How you do this is can be subtitle and have a huge effect on build time. Ideally, you always want to clone the “default” environment you have or pass values into builders, not the environment. I feel that it better for SCons to define a more Default environment and all environment created are clones. I would also push to have all Clone be a copy of write environment. There are still cases in which the user needs a “clean” environment, however, in my experience, the common case of all the environments I have made in Parts are only small copy on write clones from a common base. I think we should have more copy on write higher up the stack. At the moment the class that does copy on write are used in builders, not in the Clones.

[back to contents](#contents)

### General Thoughts from Jason Kenny
       
1. The big value SCons tends to have for me is the ability to create reproducible environments to do a build. One that is not broken because of different shells the user might be running in. This ability to duplicate exactly on a dumb shell is a huge win. The use of SConsign to help store tool state is an item I want to improve on in the Parts toolchain improvements. I think for SCons this is a win as well. More so for people using SCons to cross build. There is a time to start up we can avoid by some smarter logic on using what we know about tools. Honestly, tools don’t get added or removed as often as we change build files or source files.
1. Given the common case for most devs would be to build changes in the source, It seems to me using our cache better to speed this up would have a big effect. We can detect changes in inputs that would cause us load build files. Most of the time the user added/removed code that has no effect on the actions we would call in the end. Even with changes to imports/include we don’t need to load build files we already processed. The Scanner can deal with that for us.
1. Being smarter about how we store data could help us reduce what we keep in memory for a non-interactive build. This can help large builds as having to load a 2-3GB tree takes resources we would rather use on other items. I think we have options to store information and possible use of generators to reduce memory overhead and improve build speeds.
1. Given multiprocessing thinking, the main issue is that we have a large data tree. Sharing this tree across processes will be slow. We need to avoid this as much as we can. Using processes to do work that can be independent as possible and pass state to the main thread about node state which has the main data structure will work much better. This should have a positive effect on builder based on Python code as they can build independently. In all cases of builders, we have to address that I have seen builder that try to set state in the environment or globally. These states have to shared or avoided in some way. I not suggesting how to solve this.. but this will be a design issue to address.
1. Last item is that no matter how good SCons is.. people will want to be able to generate build files for a different system. The current logic for Visual studio, for example, tries to make a makefile project to run SCons. The users really want to make a MSBuild project. We should do that. Likewise, we should be better at working with other build system projects. Having good middleware to allow building or working with an automake or CMake project will help adoption. CMake is doing well because it is a build generator, same with Meson. You want to cover your bases with your users. Systems like these make it easy to do so.
1. Try Intel's VTune for Python for profiling. It was very useful working on Parts.

[back to contents](#contents)
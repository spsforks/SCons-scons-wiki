Performance is one of the major challenges facing SCons. When compared with other current options, particularly Ninja, in many cases performance can lag significantly. That said other options by and large lack the extensibility and many features of SCons.

Bill Deegan (SCons project co-manager) and Andrew Morrow (MongoDB) have been working together to understand some of the issues that lead to poor SCons performance in a real world (and fairly modestly sized) C++ codebase. Here is a summary of some of our findings:

* Python code usage: There are many places in the codebase where while the code is correct, performance based on cpython’s implementation can be improved by minor changes.
    * Examples
        * Using for loops and hashes to uniquify a list. Simple change in Node class yielded approximately 15% speedup for null build
        * Using if x.find(‘some character’) >=0 instead of is ‘some character’ in x (timeit benchmark shows a 10x speed difference)
    * Method to address
        * Profile the code looking for hotspots with cprofile and line_profiler. Then look for best implementations of code. (Use timeit if useful to compare implementations. There are examples of such in the bench dir (see: <https://bitbucket.org/scons/scons/src/68a8afebafbefcf88217e9e778c1845db4f81823/bench/?at=default> )

* Serial DAG traversal: SCons walks the DAG to find out of date targets in a serial fashion. Once it finds them, it farms the work out to other threads, but the DAG walk remains serial. Given the proliferation of multicore machines since SCons’ initial implementation, a parallel walk of the DAG would yield significant speedup. Likely this would require implementation using the multiprocessing python library (instead of threads), since the GIL would block real parallelism otherwise. Packages like Boost where there are many header files can cause large increases in the size of the DAG, exacerbating this issue. There are two serious consequences of the slow DAG walk:

    * Incremental rebuilds in large projects. Typical developer workflow is to edit a file, rebuild, test. In our modestly sized codebase, we see the incremental time to do an ‘all’ rebuild for a one file change can reach well over a minute. This time is completely dominated by the serial dependency walk.

    * Inability to saturate distributed build clusters. In a distcc/icecream build, the serial DAG walk is slow enough that not enough jobs can be farmed out in parallel to saturate even a modest (400 cpu) build cluster. In our example, using ninja to drive a distributed full build results in an approximately 15x speedup, but SCons can only achieve a 2x speedup.

        * Method to address:
            * Investigate changing tree walk to generator
            * Investigate implementing tree walk using multiprocessing library

* The dependency graph is the python object graph: The target dependency DAG is modeled via python Node Object to Node Object linkages (e.g. a list of child nodes held in a node). As a result, the only way to determine up-to-date-ness is by deeply nested method calls that repeatedly traverse the Python object graph. An attempt is made to mitigate this by memoizing state at the leaves (e.g. to cache the result of stat calls), but this still results in a large number of python function invocations for even the simplest state checks, where a result is already known. Similarly, the lack of global visibility precludes using externally provided change information to bypass scans.
    * See above re generator
    * Investigate modeling state separately from the python Node graph via some sort of centralized scoreboarding mechanism, it seems likely that both the function call overhead could be eliminated and that local knowledge could be propagated globally more effectively.

* CacheDir: There are some issues listed below. End-to-end caching functionality of SCons, including generated files, object files, shared libraries, whole executables, etc., is one of its great strengths, but its performance has much room for improvement. 
    * Existing bug(s) when combining CacheDir with MD5-Timestamp devalues CacheDir.
        * Bug: <http://scons.tigris.org/issues/show_bug.cgi?id=2980>

    * Performance issues:

        * CacheDir re-creates signature data when extracting nodes from the Cache, even though it could have recorded the signature when entering the objects into the cache.

    * Method to address

        * Store signatures for items in cachedir and then use them directly when copying items from Cache.

        * Fix the CacheDir / MD5-Timestamp integration bug

* SConsign generation: The generation of the SConsign file is monolithic, not incremental. This means that if only one object file changed, the entire database needs to be re-written. It also appears that the mechanism used to serialize it is itself slow. Moving to a faster serialization model would be good, but even better would be to move to a faster serialization model that also admitted incremental updates to single items.
    * Method to address:
        * Replace sconsign with something faster than the current implementation, which is based on Pickle.
        * And/or Improve sconsign with something which can incrementally only write that which has changed.

* Configure check performance: Even cached Configure checks seems slow, and for a complexly configured build this can add significant startup cost. Improvements here would be useful.
    * Method to address:
        * Code inspection, look for improvements
        * Profile

* Variable Substitution: Currently variable substitution, which is largely used to create the command lines run by SCons, uses an appreciable percentage (approximately 18% for a null incremental build) of SCons’ CPU runtime. By and large much of this evaluation is duplicate (and thus avoidable work). For the moderate sized build discussed above there are approximately 100k calls to evaluation substitutions. There are only 413 unique strings to be evaluated. Consider that the CXXCOM variable is expanded 2412 times for this build. The only variables which are guaranteed unique are the SOURCES and TARGETS, all others could be evaluated once and cached.

    * Prior work on this item:
        * [Previous Discussion](SubstQuoteEscapeCache/Discussion)
    * Working doc on current and areas for improvement:
        * [New Approach](SubstQuoteEscapeCache/SubstImprovement2017)
    * Method to address:
        * Consider pre-evaluating Environment() variables where reasonable. This could use some sort of copy-on-write between cloned Environments. This pre-evaluation would skip known target specific variables (TARGET,SOURCES,CHANGED_SOURCES, and a few others), so minimally the per command line substitution should be faster.
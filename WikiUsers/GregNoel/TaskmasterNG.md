

# Taskmaster (Next Generation) Design

This is a mix of how it works now, how it should work, and how I'd rewrite it. It's a very preliminary draft; consider it about an 0.1 version. 

## Contents

* [General](#general)
* [Schedule Executors not Nodes](#schedule-executors-not-nodes)
* [Transverse Graph](#transverse-graph)
* [Extensions to Functionality](#extensions-to-functionality)
* [Backward Incompatibilities](#backward-incompatibilities)
* [Jobs](#jobs)
* [Tasks](#tasks)
* [Scheduling Pipeline](#scheduling-pipeline)

To add: 

* Caching negatives to enable implicit dependencies 
* Copying sources for duplicate=1. 
* Creating output directories (may be more than one, viz. dup=0 and TeX .aux) 

## General

In effect, the Taskmaster and the job dispatcher are _coroutines_ acting together to accomplish their task.  If Python had a simple way to do closures, the two could indeed be implemented as coroutines, but Python doesn't, so they aren't.  (Yes, there's the `yield` command, which gets Python a long way down the path to coroutines, but it's not available on all our supported platforms.) 

To implement coroutines sequentially, the choice has to be made as to which flow is the driver and which is the driven.  The driver code runs sequentially, so the code is simpler.  The driven code is more complex, since it has to retain state so that it can restart where it was stopped. 

The basic difference between the old Taskmaster and this design is that the Taskmaster drives the job dispatching rather than the reverse.  The obvious rationale is that the state required to save and restart the job dispatching is <ins>much</ins> smaller than the state required for the Taskmaster: all of the state for job dispatching can be encapsulated in a simple API that controls a queue of pending tasks.  Via the API, the Taskmaster pushes as many jobs as it can into the queue and then asks for run results.  A run result can lead to further jobs being eligible to run, which are pushed onto the queue; when there are no jobs left to be run, the build is complete.  (One special case: in serial mode, a single job at a time is placed in the queue at a time and the results are immediately requested, since the execution order could be counterintuitive otherwise.) 

There's some state shared between TaskmasterNG and the job dispatcher, such as a flag that's set if the run is being aborted.  It's not always obvious where this state should live; it may come down to case-by-case determinations. 


## Schedule Executors not Nodes

Nodes accumulate upstream dependencies and form the _dependency graph_.  This dependency graph forms a [DAG](http://en.wikipedia.org/wiki/Directed_acyclic_graph).  To determine which actions must be performed before others, the transverse graph[*] must be calculated, which also forms a DAG. 

[*] The _transverse_ of a graph is the same graph with the direction of the arcs reversed. 

Instead of creating the transverse graph in the Nodes (as is currently done), TaskmasterNG calculates the transverse dual[*] of the dependency graph in the Executors, creating a _scheduling graph_.  In its current state, it does this by creating a wrapper for each new Executor it encounters.  This is slower, but allows testing using an actual Executor.  Eventually, the logic in the wrapper should be put in a Taskmaster-owned base class for Executor, which would not only be faster but also consume less memory. 

[*] A _dual_ of a graph is another graph that is logically equivalent, that is the dual can be calculated from the original and the original can be calculated from the dual.  In this case, the arcs of the original graph are replaced by nodes and the nodes are replaced by arcs.  The duality isn't exact, since an Executor in the scheduling graph replaces more than one arc of the dependency graph (the arcs connecting one set of sources to their respective targets). 

The Executor wrapper also uses actual Nodes.  As part of TaskmasterNG, a great deal of the dependency logic that operates on Nodes is being moved to the Executor.  That is, instead of accumulating dependencies in a Nodes, they are accumulated in the Node's Executor.  The existing API can be retained by functions that forward scheduling-related requests to the Executor.  The current implementation of TaskmasterNG simulates this by copying the sources from a sibling set of target nodes into the wrapper before proceeding. 

(In fact, one can argue that the dependency logic should be factored into multiple base classes, one to create the downstream dependencies, one to handle creating the upstream transverse links, and maybe some others.  This design hasn't proceeded far enough to identify those items yet.) 


## Transverse Graph

The fundamental operation of the Taskmaster is creating the transverse ("downstream") graph that will control the build sequence.  It is created from the dependency ("upstream") graph created by Builders and the like.  TaskmasterNG has a "visit once" design policy for upstream scans; in other words, there's no rescanning, even when adding implicit dependencies.  This is substantially faster than the old Taskmaster, which has to continually rescan to find dependencies added during the build. 

The strategy for this policy is based on the observation that implicit dependencies only add arcs to the DAG, they don't add nodes.  At any point in time, a node has either already been visited (and hence has been placed in the scheduling pipeline, see below) or it hasn't; if it's been visited, it could have already been completed (leaf or built or failed or ...).  When an upstream Executor is examined, if it has already been completed there's nothing more to do; otherwise, the transverse link is added so the downstream Executor will be notified and the upstream Executor is placed in the scheduling pipeline if it has never been visited before. 

It can be demonstrated that this algorithm is stable and conservative.  The Nodes are already created by the parse phase and evaluating Nodes is linear in the number of arcs traversed, so generating the transverse graph to run the build is optimal (at least in that sense).  Since arcs are only evaluated in the master thread, there are no race conditions to worry about, nor is there any need to rescan. 


## Extensions to Functionality

This design strategy makes it easy to add some extensions to SCons' functionality. 


### Before/after sequencing

There have been some cases where what a user wanted to completely execute one sequence of steps before executing some other sequence.  One example of this is to build all of a project before installing any of it.  For example, Make can do this by executing `make` as a build action (SCons cannot do this since updates by the subprocess are not propagated back). 

With this design, all it takes is a pipeline stage that delays the "after" processing until the "before" processing has been completed successfully. 


### Secondary/intermediate targets

In GNU Make, a _secondary_ target is not automatically rebuilt if it is missing, an _intermediate_ target is a secondary target that is automatically deleted after its last use, and a _precious_ target is one that is not deleted if an interrupt occurs while building it.  The relationships between them are, ah, interesting to explain (see the [manual for GNU `make`](http://www.gnu.org/software/make/manual/make.html#Chained-Rules)). 

This design allows a Node may be specified as one of three flavors: primary, secondary, and intermediate.  I don't see how this could be applied to non-filesystem targets, but I don't see any reason to forbid it, either; when the text below mentions "files" assume the Node could be any of the valid types. 

* **Primary**: This file must be built.  This flavor is the default.  Leaf sources are automatically primary.  Root targets are automatically primary.  Probably sources of a primary alias will automatically be primary. 
* **Secondary**: If a cached signature is present, there's no check for the existence of the file.  Otherwise, they are treated as primaries. 
* **Intermediate**: Treated as secondaries, but as they are found, they are collected.  At the end of a successful run, they are deleted.  Failure to delete an intermediate is ignored. 
Four things will need to be implemented: 

   * The Primary(), Secondary, and Intermediate() functions to mark Nodes appropriately. 
   * The logic to figure out if a target is up-to-date even if intermediate or secondary targets are missing. 
   * The logic to rebuild missing intermediate targets if a downstream target needs them. 
   * The logic to delete an intermediate target when the need for it is done. 
Using an explicit pipeline, it is much more straightforward to add the secondary and intermediate target flavors.  A stage is inserted just before the build stage to check for missing sources.  If there are any, the build stage of the missing source is scheduled (which may cause its missing targets to be scheduled), then wait for all the targets to be completed. 

[issue #583](/scons/scons/issues/583)


### Adding Nodes at build time

Adding Nodes at build time is something we don't do now, but people have wanted.  The canonical example is processing a file to get a list of sources.  If the file is built, it cannot be processed at build time, so people have wanted some way to create a list at build time and potentially add Nodes to the graph that will cause the listed files to be built. 

The design of the API to allow this is a separate design, but the scheduling pipeline can be easily extended to add the necessary processing steps.  I can see a number of methods for adding this functionality; possibly more than one will be implemented. 

Note that the strategy adopted by TaskmasterNG implies restrictions on any Nodes and their corresponding Executors created at build time.  Forests of Nodes can be created, but except for the root(s) of the tree(s), none of the Nodes can have dependencies outside the created forest; the root(s) of the tree(s) can have at most one dependency, and that only to an Executor that has not yet been (completely) evaluated.  (These Nodes and Executors can be added in any thread as long as the upstream link is evaluated in the master.)  Any other scenario could lead to dependencies being added too late to have any effect. 


### What-if

xxx 


### Load Average

xxx 


## Backward Incompatibilities

xxx 


### Meaning of --jobs=1

The exact meaning of the `--jobs=`**N** command line option is changed by this implementation. 

The current meaning for `--jobs=0` and `--jobs=1` is effectively identical: tasks are serialized in a very predictable order.  The meaning for **N** larger than one is that **N** threads may be working at one time (the master thread can only run when at least one worker thread is suspended).  (As this is written, there's a pending change to push anticipatory work onto the worker's queue which will mean that the master thread can be running at the same tima as the **N** worker threads.) 

This implementation always allows up to **N**+1 threads to run at a time.  For `--jobs=0` the meaning is unchanged: either the master process or a single subprocess is running.  For `--jobs=`**N** for **N** greater than one, the meaning is effectively unchanged: **N** worker processes can be running in parallel.  The real change of meaning is for `--jobs=1`. 

In this implementation, `--jobs=1` is treated as a _parallel_ execution.  Although only one job step will be run at a time, the master process can (and will) run in parallel to queue up other work to be done.  The result is that the order of execution is not the same as the expected simple treewalk. 

Because of this visible difference, this implementation changes the default from `--jobs=1` to `--jobs=0`.  Since this change makes no functional difference to the current Taskmaster, it can be made well before fielding TaskmasterNG if desired (_i.e._, at any major release prior to when TaskmasterNG is scheduled to be implemented). 


### Implicit dependencies on by default

The use of cached implicit dependencies is on by default.  ``Negative caching`` is used to make it reliable.  xxx 


## Jobs

xxx 


## Tasks

(((Probable oversimplification: The caller of the Taskmaster passes in a set of decisions (a function in some object).  In the current Taskmaster, this is done by passing in a subclass of Task.  The exact mechanism for TaskmasterNG is not yet decided; maybe optional arguments?  Since the type of `Job` is one of the options, maybe the caller creates it and passes it in?  This is very rough and almost certain to change.))) 

The Taskmaster can operate in a number of different _modes_. xxx Possible taskmaster modes: 

* **build** run commands that are out of date 
* **clean** remove built files 
* **query** determine if targets are out of date 
* **dryrun** show what would be done, but don't run anything 
* **config** run configuration commands 
* **touch** bring targets up-to-date 
* **???** other modes not yet identified 
For each mode, there are a number of decisions made by the Taskmaster that may be influenced by the mode. xxx Possible functions: 

* **treewalk** ??? run function for each Executor; mode could be built out of separate, much simpler implementation, not requiring pipeline or other complexity 
* **job** the type of job scheduler to use: 
      * _serial_ run at most one external job at a time 
      * _parallel_ evaluate `--jobs=N` for number of jobs 
      * _special_ Python function run internally 
* **outofdate** evaluate build for out-of-date 
* **print** print command before executing 
* **???** other functions not yet identified

 **function**  |  **build**  |  **clean**  |  **query**  |  **dryrun**  |  **config**  |  **touch**  |  **mode** 
 ------------- | ----------- | ----------- | ----------- | ------------ | ------------ | ----------- | ---------
 treewalk  |  no  |  yes  |  yes  |  yes  |  no  |  yes  |  mode 
 job  |  parallel  |  special  |  special  |  special  |  serial  |  special  |  mode 
 parallel  |  yes  |  no  |  no  |  no  |  no  |  no  |  mode 
 outofdate  |  yes  |  always  |  yes  |  special  |  yes  |  yes  |  mode 
 print  |  yes  |  special  |  no  |  yes  |  no  |  yes  |  mode 
 fn  |  build  |  clean  |  query  |  dryrun  |  config  |  touch  |  mode 
 fn  |  build  |  clean  |  query  |  dryrun  |  config  |  touch  |  mode 


## Scheduling Pipeline

The meat of TaskmasterNG is the pipeline.  It is seeded by the top-level targets (whether from the command line, Default(), or default).  It operates on Executors; whenever a Node is indicated, assume it's translated into its corresponding Executor. 

_This description is light on error logic (as is the code).  Where it is described, it's in italics to indicate that it's not part of the pipeline itself._ 

The pipeline consists of a number of stages.  A pipeline stage can be delayed by specifying a set of upstream Executors that must be completed before it can continue.  An Executor is initially placed in the **before/after** stage. 

Unlike a typical pipeline, an Executor does not pass through every stage; in fact, the stages form a DAG linked by decisions made during a stage's processing.  The logic in a stage determines which stage should be executed next. 

Dispatching a stage involves calling a function to execute the stage.  If the stage can be delayed, it specifies the Executors that must be completed and establishes a callback function where flow will be resumed.  (Of course, if the Executors are all already completed, the callback is executed immediately.)  When an Executor completes, any waiting Executors are notified. 

As a convention, if the stage name is `NAME()`, the callback function is `do_NAME()`.  As a rule, a stage has at most one callback, but it's possible that a future stage could have multiple callbacks during its flow.  It's possible for a callback to be repeated if it nominates additional predecessors, as happens when an implicit dependency has its own implicit dependencies. 

_If the build is being aborted, instead of dispatching the callback, the _**completed**_ stage is forced to clean up the run queue._ 

(((Stuff in triple parenthesis has not been implemented yet.))) 


### Visiting an Executor

There are two primitive operations that underlie the pipeline staging.  One is _visiting_ an Executor and the other is _waiting on_ an Executor.  Visiting an Executor may cause it to wait on other Executors and waiting on an Executor requires that it first be visited. 

To wait on a set of upstream Executors, each Executor is visited.  The first time an Executor is visited, its pipeline is started.  If the pipeline isn't completed when returning from the visit, the downstream Executor is added to the "notify list" of the upstream Executor.  When the upstream Executor completes, it notifies any downstream Executors, which can proceed with their own pipeline. 

Taskmaster activity is started by waiting on the Executors of the top-level targets.  It does this by using a dummy Executor that depends on the top-level targets and runs a fake pipeline stage to wait on them.  When that pipeline stage completes, the Taskmaster checks for dependency loops, cleans up, and reports its status back. 

The Taskmaster can be run more than once in a given program invocation.  The two major examples of this are evaluating configure tests and interactive mode.  Each time the Taskmaster is called, it needs to recalculate the scheduling graph in the Executors.  The problem is knowing whether an Executor is being visited for the first time for this Taskmaster run. 

Resetting all the Executors before a run can be expensive if only a few are going to be used, so TaskmasterNG only initializes the Executors used in a run.  In the draft implementation, it uses a wrapper object containing the scheduling state and discards all the wrappers at the end of a run.  In an implementation that keeps the scheduling state in the Executor itself, it would keep a _visit ID_ that is incremented each time the Taskmaster is called.  When visiting an Executor, the visit ID is compared against the ID saved in the Executor.  If the IDs don't match, this is a new visit and the Executor's scheduling state is initialized. 


### (((Before/after stage)))

This stage does no processing on an Executor, not even dependency evaluations, until a prior step has been completed.  Even if there are upstream dependencies that could otherwise be executed, this causes them to be delayed until some other activity has been completed.  In other words, it forces steps to be run sequentially. 

_Psuedocode_ 

Wait on Executors in the `before` list. 

Flow always proceeds to the **check sources** stage. 


### Check sources stage

This stage worries about explicit upstream dependencies.  Explicit upstream dependencies are things like the sources, the command, and any dependencies added by the user, less any explicitly-ignored dependencies.  This stage evaluates the explicit dependencies and determines which flow should be chosen to evaluate the implicit dependencies.  The tactic is that if the explicit dependencies are causing a (re)build, the implicit dependencies may have changed, so we go directly to to the stage to (re)calculate them.  Otherwise, we assume (for now) that the cached implicit dependencies are OK and we go to a stage that will determine what do do with them. 

_Psuedocode_ 

If there are no upstream dependencies, this target is a leaf, so all we have to do is arrange to have the signature (re)calculated if it's subsequently needed.  (((If this a build directory with `duplicates=1` and the source has changed, this is a good place to update from the original.)))  (((TODO: this needs some research, but I believe that there's a 100% chance that at least the `os.stat()` results will be required for the signature, so in addition to clearing the signature cache, it might optimize things a bit to get those values now.))) 

Otherwise, if any of the explicit upstream sources are poisoned, the build is poisoned so that this build and any downstream builds will be suppressed (a failed build "poisons" its targets recursively; this supports the `-k` command-line option).  Even thought this build will not happen, we need to process any built implicit dependencies, so we proceed to the **stored deps** stage. 

If any of the sources (((are primaries and))) do not exist, plan to rescan and proceed to the **full scan** stage. (((If the order of the sources has changed, plan to build and proceed to the **full scan** stage.))) If any of the other explicit dependencies has changed, plan to build and proceed to the **full scan** stage. 

If a user-provided dependency has changed, track this fact. 

Otherwise, proceed to the **stored deps** stage to process the stored implicit dependencies. 


### Stored deps stage

This stage is concerned with implicit dependencies.  If implicit dependencies have never been calculated, or we aren't storing them (`--implicit-cache`), or we don't trust them (`--implict-deps-changed`), we need to calculate them from scratch, so we go do a full scan.  Otherwise, the cached dependencies are examined; if any are out-of-date, a rebuild will be needed so we indicate that a rebuild is needed and go do a full scan done in case the set of implicit dependencies has changed. 

_Psuedocode_ 

If there are no stored implicit dependencies, proceed to the **full scan** stage. If we aren't using implicit dependencies, proceed to the **full scan** stage. If we don't trust implicit dependencies, proceed to the **full scan** stage. 

If any implicit dependency is poisoned, poison this build.  If the build is poisoned, proceed to the **completed** stage. 

If any implicit dependency has changed, plan to build and proceed to the **full scan** stage. 

If a user-provided dependency has changed, proceed to the **schedule** stage. 

Otherwise, the build is up-to-date and there's nothing to do, so proceed to the **completed** stage. 


### Full scan stage

This stage is concerned with scanning for implicit dependencies.  Since an implicit dependency may itself have implicit dependencies, this stage iterates through successive rounds of scans until all dependencies have been determined.  If this stage finds no out-of-date implicit dependencies (and if no prior stage found a reason to plan a build), there's nothing to do; otherwise, a build is scheduled. 

_Psuedocode_ 

This stage consists of setup logic and a callback that is executed repeatedly until all implicit dependencies have been scanned. 

XXX 


### Schedule stage

This stage is responsible for seeing that the job is run.  It will queue a job if there are already too many jobs running.  (((It will also suppress job execution if the load average is too high.))) 

(((This stage maintains a queue of jobs separate from the queue used to feed the worker threads primarily to have control when some sort of error condition occurs (such as a failed job).  Having a job queued that can be immediately dispatched is much faster than the current Taskmaster, but there's still a delay before the worker thread can start a new task.  There are difficulties in having the job dispatching make decisions about when to quench the job queue and complications with locking for side effects, but integrating the two queues would allow the maximum possible number of jobs to be running whenever possible.))) 

_Psuedocode_ 

xxx 


### Start stage

This stage is responsible for coordinating side effects and for passing available jobs to be run. 

_Psuedocode_ 

xxx 


### Wait stage

This pseudo-stage is responsible for waiting for a job to finish.  It is called when the Taskmaster cannot find any other tasks to queue up.  It waits for the first job to complete and resumes the corresponding pipeline. 

xxx if waiting and no jobs outstanding, there's a dependency loop 

_Psuedocode_ 

Any side-effect locks are released and flow proceeds to the **completed** stage. 

xxx 


### Completed stage

This stage deals with an Executor whose processing is completed.  It releases any downstream dependencies to continue down their pipeline. 

_Psuedocode_ 

xxx 

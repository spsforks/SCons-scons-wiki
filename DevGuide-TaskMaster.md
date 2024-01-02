
# SCons Taskmaster

The Taskmaster is responsible for taking the directed acyclic graph (DAG) created during the parse phase, evaluating it, and arranging for the execution of any commands needed to bring the project up to date.  As part of its processing, it scans source files for implicit dependencies and adds them to the DAG.  To determine if something needs to be built or rebuilt, it compares the signatures of the antecedents; if they have changed from the last run, the Taskmaster runs a command and then generates new signatures. 


## Processing

The Taskmaster is called from the Jobs module.  The Jobs module pulls a batch of tasks (a subclass of Task wraps a runnable Node) and runs the batch to completion.  The Jobs module repeats this process until the Taskmaster tells it that there are no more runnable tasks.  If the Jobs module is in _parallel_ mode, the batch size is set by the **-j** parameter on the command line.  If the number of jobs is one (the default) or if the Python implementation does not support parallel execution, the Jobs module operates in _serial_ mode and the batch size is one. 

When the Taskmaster is instantiated, it is given the specific class to use to wrap the runnable nodes.  This class is normally a subclass of the Task class (also defined in the Taskmaster module) and contains the logic to process a node.  Subclasses are used to cause the Taskmaster to operate in different modes; the subclass provides the behavior that is specific to the mode.  Different subclasses are used for a standard build (BuildTask), for cleaning targets (CleanTask), for determining if a build is up-to-date (QuestionTask), and for configuring (SConfBuildTask). 


## Running the DAG

The classic technique for processing elements in a DAG is called a _topological sort_.  A topological sort of a DAG is a linear listing of its nodes such that each node comes before any other node that depends on it.  For greater detail about topological sorting, look at the [Wikipedia entry for topological sort](http://en.wikipedia.org/wiki/Topological_sort).  There are two classic algorithms: if the graph is pre-built, a _recursive descent_ (also called _graph coloring_) approach may be used; if only the relationship information is available (pairs of nodes where one must precede the other), a _traversal tree_ approach can be used, which evaluates a _work queue_ of nodes whose predecessors have been evaluated (each evaluation potentially releases additional nodes into the work queue). 

For the recursive descent approach, each node is visited exactly once, so the run time is linear in the number of nodes (_i.e._, _O_(**n**)).  For the traversal tree approach, each relationship link must be used to build the traversal tree and then each node is visited exactly once, so the run time is linear in the number of nodes plus the number of dependencies (_i.e._, _O_(**n**+**d**)). 

In general, the parse phase creates a larger DAG than is used by any specific build.  Because of this, and because of the need to handle generated header files and scanned implicit dependencies, the SCons Taskmaster does not use a topological sort directly.  Instead of sorting all of the Nodes in the DAG, the Taskmaster starts walking the DAG at a given Node (one of the targets specified on the command line) and looks for child Nodes (sources or dependencies, implicit or explicit) that are ready to be built.  In essence, it's a recursive-descent sort that stops when it finds the first unevaluated Node. 

The Taskmaster keeps a list of _candidates_ (analogous to the "work queue" of a traversal-tree topological sort), the Nodes that the Taskmaster is ready to examine either because each was an explicitly-specified top-level target, or because they're somewhere down the walk of the tree from those top-level targets--that is, children (or children of children of children...) of a target that SCons has been requested to make sure is up-to-date (either because it needs to be built or because it already was up-to-date).  This optimization so that the full recursive descent does not need to be done means that often only a small subset of the full DAG needs to be visited on each call. 

The Taskmaster only puts Nodes back on the candidates list after the children for which it is waiting complete their builds.  Putting a Node back on the candidate list will cause it (and/or its sources) to be re-scanned, if necessary.  This is how implicit dependencies within generated header files get detected, because generated files can get re-scanned as necessary.  (For efficiency, source files that haven't changed--been built--since the last time they were scanned can just return their previous results, but that's an optimization handled within the Node layer itself.) 

The Taskmaster is only concerned with the _order_ in which Nodes are evaluated.  It does not itself look at any signature information to decide whether a Node being evaluated is up to date or needs to be rebuilt; that is delegated to the Task class, once the Taskmaster has decided that all of its dependencies have been satisfied. 

If a build fails and the **-k** flag causes evaluations to continue, the Node is marked as _poisoned_.  When a subsequent Node is evaluated and finds an antecedent that is poisoned, that Node is also marked poisoned and the execution of its command is skipped. 

Before a Node is selected for execution, it is checked to see if any of its side-effects conflict with the side-effects of any Tasks currently being built.  If there are any conflicts, the Node's execution is delayed until all side-effects are cleared. 

The Taskmaster algorithm only runs in one thread and is not itself parallelized.  That means child detection and reference counts do not need to be thread-safe.  What _is_ parallelized (that is, handled by separate threads when the **-j** option is used) is the evaluation of whether the Node is up-to-date and the execution of its build, if necessary. 

It's worth noting that the Jobs module calls the Taskmaster once for each node to be processed (_i.e._, it's _O_(**n**)) and the Taskmaster has an amortized performance of _O_(**n**) each time it's called.  Thus, the overall time is _O_(**n**^2).  It takes a pathological DAG to achieve the worst-case performance, but it occasionally happens in practice. 


## Scanning for implicit dependencies

Running scanners; adding to the graph when a scanner reports a dependency. 


## (Future?) Extending the graph based on the result of executing a command

The restrictions imposed so that this can work. 


## Dealing with signatures

Signature types, calculating signatures, comparing signatures. 

---

 
# Taskmaster Module


## The Taskmaster class

Here are the steps performed by the Taskmaster to select the next job to run: 

* When the Jobs module requests another task to perform, the Taskmaster pulls a candidate Node off the list. 
* If the Node's state indicate is has already been handled, the Node is simply skipped for this walk.  This can happen if the Node was already visited by the DAG walk for another target, or just because it's a dependency of multiple targets and it ended up on the candidate list multiple times during a parallel build. 
* The Node's list of child Nodes is generated.  This causes relevant files to be scanned for implicit dependencies. 
* If the Node has a child that's already failed a build (or had one of its children fail), the Node is marked as having failed (which propagates the failure condition up the DAG) and skipped.  This can happen if a Node is a dependency for an earlier top-level target. 
* If any child Nodes are currently pending process, it means we've detected a dependency cycle.  The cycle is identified and printed, and an exception is raised. 
* If one or more of the Node's children are derived targets (that is, may need building) that have not _started_ their builds, several things happen: 
      * All of the unstarted children are added to the candidates list. 
      * The Node under consideration is removed from the list and marked with a counter of how many of its children must finish their unstarted builds. 
      * Each of the unstarted children has this parent Node added to a list of "waiting parents" who will have their reference counts decremented when they finish their builds. 
      * When each unstarted child finishes its build, all of its "waiting parents" have their reference counts decremented, and Nodes whose "waiting parent" counts drop to zero are put back on the candidates list to be re-evaluated. 
* If one or more of the Node's children are derived targets (that is, may need building) that have not _finished_ their builds, several things happen: 
      * All of the unfinished children are added to the candidates list. 
      * The Node under consideration is removed from the list and marked with a counter of how many of its children must finish their unfinished builds. 
      * Each of the unstarted children has this parent Node added to a list of "waiting parents" who will have their reference counts decremented when they finish their builds. 
      * When each unstarted child finishes its build, all of its "waiting parents" have their reference counts decremented, and Nodes whose "waiting parent" counts drop to zero are put back on the candidates list to be re-evaluated. 
* If the Node has one or more side-effect Nodes that are currently being built, several things happen: 
      * The Node is removed from the candidate list. 
      * Each of the side-effects has this Node added to a list of "waiting side effects." 
* With none of the above conditions satisfied, the Node is accepted as the next Node that is ready to be evaluated for building.  The Node is wrapped in a Task class that shepherds it through that process. 

## The Task class

(((TODO: Tasks and their entry points.))) 


## The Stats class

(((TODO: Statistics accumulated by the Taskmaster))) 



---

 
# Jobs Module


## The Jobs class

(((redirects to either Serial or Parallel))) 


## The Serial class

(((does synchronous execution))) 


## The Parallel class

(((does parallel execution))) 



---

 
# Script Module (partial)

(((entry points for SCons))) 


## Initialization

(((setup))) 


## Main Sub-Module

(((contains definitions of three subclasses of Task))) 

(((instantiates Jobs and Taskmaster; runs them))) 


## SConscript Sub-Module

(((API support for SConscripts))) 



---

 

This is a work in progress.  Click on the "Edit(Text)" link below, and let's start discussing what needs to go in this section. 

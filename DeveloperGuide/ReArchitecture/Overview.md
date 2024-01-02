This is the main entry page for working out a redesigned architecture suitable for SCons' feature set, but designed with performance in mind. 

Methodology:  Things that have been more-or-less decided upon, or are an initial draft for discussion with no competing counter-proposal, go in the pages in the **Settled** section.  Undecided issues go in the topic's discussion page (follow the link in the navigation bar).  To start a discussion about an item, add a section to the topic's discussion page and link to the discussion section from its location in the appropriate **Settled** page. 


## Settled

[Goals](Goals) - The requirements spec (where we use the term "Goals" because these won't all be hard-and-fast). 

[UseCases](UseCases) - The use cases we believe cover 90% of what users want and for which we will optimize performance. 

[Design](Design) - The design itself.  This should ideally not refer to existing SCons design or implementation.  (In practice, I'm sure it'll be hard to not have some leakage.) 

[Implementation](Implementation) - How the current SCons implementation can be made to fit the new architecture. 


## Terminology
| What | Definition |
|------|------------|
| DAG  |  [Directed Acyclic Graph](http://en.wikipedia.org/wiki/Directed_acyclic_graph).  In this architecture, one DAG records the dependency relationship between Entities and the transverse dual DAG is calculated from it to determine the build order. 
| Dependency graph  |  The graph of dependencies between individual Entities.  The graph forms a DAG. 
| Dual  |  In graph theory, a graph calculated from an initial graph by transforming its nodes to arcs and arcs to nodes.[1] 
| Entity  |  Technically, the node (junction connected by arcs) of the dependency graph.  Entities represent files, directories, Python values, _etc._ 
| Schedule graph  |  The graph of (((successors?))) between schedule items, giving the legal build order.  The graph forms a DAG. 
| Schedule items  |  Technically, the node (junction connected by arcs) of the schedule graph.  We currently anticipate these items will be implemented in the `Executor` objects (or a wrapping class). 
| Transverse  |  In graph theory, a graph calculated from an initial graph by reversing the direction of its arcs. 


[1] (((SK:  Greg, I'm trying to educate myself about the graph theory, and this doesn't look like the correct definition of "dual".  On the face of it, you can't just transform nodes to arcs, because arcs by definition have two endpoints and a node in the original graph with multiple arcs can't suddenly become a an arc in the dual that points to more than two nodes.  The definition I see for "dual" transforms each _plane region_ in the original graph into a node in the dual.  Please clarify.)))  


## TODO

Things that still need to be added: 

* External inputs (information collected from "outside" SConscripts): 
     * Configuration and configure tests (including Python `sys` and `os` modules) 
     * Variables and option files (including shell variables?) 
     * Command-line flags and overrides 
* Variable substitution and quoting 
* Backward compatibility (i.e., `compat`) 
* CacheDir 
     * Resolving races in parallel builds 
     * Multiple architectures in the same cache 
     * Caches on shared filesystems 
           * Simultaneous builds on same machine 
           * Simultaneous builds on different machines 
     * Better support for remote builds 
     * General topic of races? 
* I don't have a good categorization for this topic: 
     * Named projects with versioning 
     * Automated install targets 
     * Installing via staging areas 
     * Packaging source distributions 
     * Packaging binary distributions 
     * Generally, think automake and autoconf 
* Testing (i.e., running users' tests to validate their products) 
* I18n (builders and whatnot to support translations and the like) 
* I18n (dealing with internationalized files, filesystems, text, ...) 
* Special run modes: 
     * Clean (-c) "levels" of cleaning? 
     * Query (-q) 
     * Help (-h -H) 
* Reducing global clutter by grouping related names into a class (Action.Copy)
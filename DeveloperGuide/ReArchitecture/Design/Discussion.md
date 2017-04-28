Discussions about unresolved issues for the Design page. 

This should, ideally, not reference the current SCons design and/or implementation.  For that, go to [Implementation](Implementation). 

[TOC]


# File System entities

(((JGN: Should we mention here that this is probably an ABC for the entities in this section?  Or is this the forwarding class that provides morphability by referring to one of the entity types in this section?)))   
(((SK:  ABC?  What's that?  I was just viewing this as the encapsulating header for this section of the document, not as a separate class...)))   
(((JGN: ABC === Abstract Base Class.  You already said the previous heading was an ABC, so it makes sense.  That's how it's implemented now: this heading would be equivalent to the `Base` class in FS.py.  My question is whether you want that same hierarchy in the re-architecture or if it would make sense for this class to be a referrer class that "defers to a separate, real `File` or `Directory` object" (_i.e._, it refers to one of the four object types that are the subheads for this section, which are implemented via a different base class).)))   
(((SK:  Okay, I see what you're getting at.  I wasn't thinking of an ABC here, at least partly to cut down on the proliferation of classes.  The current `File.Base` class seems pretty useless as a separate class right now.  This is probably because I didn't really implement it as an ABC (for example, with `NotImplementedError` exceptions for methods that must be provided by the concrete subclasses).  I was just trying to be "object oriented..."  I could see benefit here to intentionally defining an ABC, but when you get down to it, is there really that much similarity between the two main concrete subclasses 
(`File` and `Dir) that there's significant benefit to a common ABC?  I don't know.)))   
(((JGN: Er, you're still missing the question, which I guess should now be a trinary: Pick one: Is it a referral class (taking over the role of `Entry`, so `Entry` becomes a referred class)?  Should it be a base class, with common filesystem-oriented things?  Or should it not exist at all?  You've focused on the last two, to the exclusion of the first, which is really why I posed the question in the first place.)))   
(((SK:  My suggestion is:  No "File System entity" class.  What we've labelled "Entry Stem Cell" below is a referral class.  A "Entry" holds ambiguous entries, and after disambiguation, it can refer to either a File or Dir object.)))   
(((JGN: OK, I'll not fight it.  I just thought it might make more sense for a "Filesystem Entity" class that was optimized as a forwarding class that initially pointed to an "Entry" object until it was disambiguated, after which it pointed to a File or Dir (or Symlink or ...).)))   
(((SK:  Well, that's just my current suggestion.  I'm not completely sure either way.  I see the advantage to what you're suggesting -- have each class do one thing well, instead of the "Entry" object needing to know how to forward requests *and* disambiguate.  But it also seemed like it might be cleaner to have fewer classes, too...))) 


# Schedule arcs

(((SK:  "...labeled with _an_ Entity...?"  Really?  Singular?  Given that any arc really represents M*N dependencies that get updated by that build, what's the advantage of labeling it with an arbitrary `Entity` from that set?)))   
(((JGN: Yes.  Yes.  And yes. ;-) Abstractly  (conceptually) the nodes are replaced by arcs and the arcs replaced by nodes, so the M*N arcs between entities that represent a build are replaced by M*N nodes with arcs labeled with a (singular) entity.  Practically (actuality), the M*N nodes are collapsed into a single node with M+N arcs.  Does that explain it better?  If so, do you want to rewrite it to make it clear?)))   
(((SK:  No, it doesn't make it clear.  I'm not disagreeing with the idea of replacing M*N nodes / arcs with a single nodes that accomplish the same work much more efficiently.  I'm confused as to why you then _label_ this with one arbitrary Entity from the set that's updated.  I'd find that labelling confusing.  I'd wonder, "Hey, wait a minute, I only see a label for `file1.obj` in this graph, but what happened to `file[2-N].obj` that are updated by the same compilation?  Based on my current understanding of what you're getting at, in other words, I'd find it less confusing to leave the arch _unlabelled_ instead of labelling it arbitrarily.  What's the advantage (or necessity) of labelling it?)))   
(((JGN: OK, what we have here is a failure to communicate.  Let me try again.  If the simple dual were taken, each arc would be labeled with a single `Entity`.  But we don't do that; we collapse the M*N nodes representing a build into a schedule item, which causes arcs to be duplicated.  The 2*M*N (M*N arcs on both the source and target side) are then combined with other arcs that have the same label, yielding M+N arcs, each with a single label.  No arbitrary labeling involved.  Are we there yet?)))   
(((SK:  Sorry, I know I'm thick about this stuff, but I'm still not getting it.  You're going to have to dumb it down for me, so avoid slinging the fancy math lingo like "simple dual" unless you're going to take the time to educate me about it.  Let me explain my current understanding of what you're suggesting in really concrete terms, and you can tell me where I've gotten it wrong.  We're building three output files (a.out, b.out and c.out) from three input files (x.in, y.in and z.in).  All three outputs depend on (e.g. concatenate) all three inputs.  So there are 3x3 edges in the dependency graph, but their build step is collapsed into a single Node in the schedule graph.  Say that some of [abc].out are used in other build steps so there are scheduling steps that depend on them being up to date.  What I *think* I hear you saying is that any arcs "emanating" from that Node will be labelled with one of [abc].out, but I have no idea which one.  Or why the labelling is necessary.)))   
(((JGN: (later re-edit: I'm making it three nodes crossing to four nodes, since with three of everything, it quickly becomes confusing.)  OK, we start with seven Files (three on the top and four on the bottom) and twelve arcs.  We create the dual by changing the nodes to arcs and the arcs to nodes.  This gives us twelve nodes linked by, hmmm, I see the problem you're having with the analysis.  The hidden assumption is that the fan-in and fan-out are (approximately) the same for the original nodes above and below the MxN crossover.  That is the three "top" nodes each have a fan-in of four and the four bottom nodes have a fan-out of three.  When the three top nodes are converted to arcs, they each connect to four former arcs that are now nodes (and similarly for the bottom nodes, with four and three), so you get twelve arcs entering the collapsed node and twelve arcs leaving it.  Three quadruples of the entering nodes are redundant, with the same label, so they are merged and you get a node with three arcs entering it, each labeled with a single entity (and similarly with the arcs leaving).  So you get an input arc labeled with the single entity x.in, an input arc labeled with the single entity y.in, an input arc labeled with the single entity z.in, an output arc labeled with the single entity a.out, an output arc labeled with the single entity b.out, an output arc labeled with the single entity c.out, and an output arc labeled with the single entity d.out.  All entities label an arc, all arcs are labeled with a single entity.  Why is the labeling necessary?  Now I wish I hadn't mentioned it, but at the time, I thought I was giving an intuitive insight to make things clearer.))) 


# Is a schedule graph a dual?

(((SK:  [GregNoel](GregNoel) suggests that the schedule graph should be a dual of the dependency graph.  The definitions of dual I find suggest that a dual is actually a mapping of enclosed plane regions of a graph to Nodes in the dual graph, with arcs in the dual graph that correspond to arcs in the original graph that border two plane regions.  Greg, either "dual" isn't the correct term for what you have in mind, or I have the incorrect definition of "dual", or you have some more sophisticated transformation in mind that we need to define more specifically.  Please clarify.)))   
(((JGN: Huh.  I threw away my forty-year-old college textbooks when I moved (after all, what use would I have for them?), but I still have some of my class notes (some were lost in a roof leak), including my first semester of graph theory.  My instructor was a brilliant teacher who had the bad habit of using a different notation than the textbook and covering about three times what was in the official syllabus, so even if I had the textbook I may not have been able to find the relevant chapter.  However, on one page I find (translated from my shorthand, badly needed when taking notes in his classes), "Dual (equivalent) exchange nodes, arcs; split and merge" surrounded by calculations about digraphs.  It's nowhere near the notes about planar graphs (which is all Wikipedia covers) and just as far from the topic of DAGs.  There are some calculations about merging and splitting nodes and arcs as part of the process (which I was doing) and a lemma that duals G* and G** of a graph G may not be the same (which I hadn't remembered, I thought duals were topologically equivalent), ah, I see, the splitting and merging can cause them to be different (but there's some sort of a family equivalence? I'm not understanding all this).  Given that graph theory was his field, it's possible that these were research results that didn't stand the test of time and duals are now only defined on planar graphs, but it also could be that Wikipedia, _et.al._, are simply covering the highlights, not the whole topic.  It's clear that a DAG need not be planar, so that definition of dual cannot be applied here.  My notes reflect what I remember about duals, but there doesn't seem to be any description of what I remember in today's references, at least under that name.  So I don't know where to go from here.))) 

<a name="builders_return_executors"></a> 
# Returning Executors from Builders


## Greg Noel's proposal

Several trains of thought have made me ponder what a builder should return.  Somehow, a list of Nodes just never has sat well with me. 

The idea is that a Builder should return an Executor.  The Executor is revamped so that it's derived from a `list` and the items exposed via that list are the targets of the build.  In other words,  
 `     pgm = Program('prog', srcs)`  
 `     cmd = pgm[0]`  
 still has the same result.  There are probably a few gotchas having to do with adding lists that will have to be resolved, but it should be almost completely backward compatible.  (Yes, that's another way of saying it's not completely backward compatible (I can think of a couple of weird examples), but they're going to be pretty rare, and I'm pretty sure we can cause an error in those cases so there will be no silent change of semantics.) 

So what do we get? 

Well, you could say,  
 `    lib = SharedLibrary('mylib', [])`  
 `    lib.AddSources('foo.c', 'bar.y')`  
 `    lib.AddSources('src/*.cpp')`  
 `    lib.MergeFlags('-Dcpp -O2 -framework Python')`  
 

Emitters are then functions that operate on an Executor.  They can use an internal entry point to add a direct predecessor or use `AddSources()` as above if there might be multiple steps.  Adding additional targets would be done via an internal API; I'm not sure if it should have a public exposure. 

I think this also takes us a big step closer to being able to add steps at build time.  I'm still puzzling through the implications, but I'm pretty sure we can mark an Executor once it enters the build pipeline.  If we can do that, then we can allow modifications to Executors any time before they are committed to execution.  And if we can generalize the `AddSources()` functionality so that it can be easily extended with other types, we can do [Gary's dynamic generators](DynamicSourceGenerator) as well as [George Foot's amazing dynamic builder creator](TargetDrivenBuilderCreation) while still being very "SCons-like". 


## Greg Noel

A problem: What to return from `Object('foo.c bar.c'.split())`?  When it was just a list of nodes, it was simple, but if we're going to return an object, it must somehow be a composite object containing (or referring to) both build steps.  Something to figure out. 

<a name="emit-v-scan"></a> 
# Emitters v. Scanners

SCons currently divides processing between an emitter (run at parse time to identify secondary sources and targets) and scanners (run at build time to identify additional upstream dependencies).  The SCons design did not anticipate that an emitter might need to examine the file in order to make these determinations. 


## Greg Noel's proposal

Executive summary: Emitters generate guesses as to what a build will use as sources and targets.  Scanners can modify those choices if they are incorrect.  Emitters are not allowed to open the source; scanners are invoked after the source is up-to-date. 


### Emitters

Emitters are a function of an Executor object and a Node object.  The results are applied to the Executor object. 

(Note that a given Node object can be used with more than one Executor object and a given Executor object can use more than one Node object, so neither is a good place to cache information about the other.  Should SCons provide a way to cache any such information?) 

We introduce an unenforceable convention that emitters do not look at the source file.  (We could semi-enforce it by not allowing File.read() during parse time, but users could still open() the file.) If the emitter can't determine the exact set of modified sources[1] and targets, it is given some guidelines and other help, discussed below. 

[1] Is there ever a case where an emitter actually adds additional sources?  If there is, I argue that the case is rare enough that the emitter can make specific provisions to do it. 

An emitter is free to look for information in other ways; a Java emitter might Glob() in the output directory to see what files already exist that could have been created for the given source file and nominate those as additional outputs (which would have to be repaired latter by a scanner). 


### Scanners

The term "scanner" is used with at least four distinct meanings: 

* Source scanner: Examine a source file to determine what other files are implicitly needed for a build. 
* Target scanner: Examine the environment to determine what other files are implicitly needed for a build. 
* Batch scanner: Examine a source file to determine what other sources must be explicit members of the same build. 
* Build scanner: Examine a file to determine what targets it will generate. 
(The first two are standard nomenclature; I made up the last two.) 

Scanners are a function of an Executor object and (optionally) a Node object.  The results are applied to the Executor object. 


### Dependencies

Upstream dependencies are easy: when in doubt, don't emit it and add it during scanning.  We have plenty of machinery to deal with this sort of thing.  (Examples: implicit dependencies, batch clusters.) 

Downstream dependencies are harder.  In general, it's better to specify too many targets rather than too few; if the scanner then detects that the target is not generated, we can remove it (and poison the file so no downstream builders will try to use it).  (Examples: FORTRAN .mod files, SWIG director files.)  Worst case, we run the command and see which files were not generated. 

The only real pain is adding a target that wasn't predicted in advance (more generally, can't be known until the source is up-to-date), and then only if the target was used by another build.  Until the build is run, you wouldn't know that the dependency existed, so there would have to be some other way to force the sequencing in those cases. 


### Emitter help

The only way I can see out of this is to give the emitter something to emit that can be used to tie things together later.  That effectively converts it into something that we can already handle, although the devil will be in the details. 

The "something" would have to have these attributes: 

* It could be passed around the same as a Node, used as a source, whatever. 
* It would represent a list of Nodes to be filled in by the upstream builder.  The list could be empty. 
* It would match a wildcard pattern; any node that matched the pattern would be inherit its dependency. 
Only the last one is potentially expensive: when the pattern was created, it would have to be matched against any names (but only in one directory, so the search would be limited) and any node subsequently created in that directory would have to be matched against the pattern. 

xxx is this sufficient?  should a proxy for fill-in be distinct from a proxy for wildcard matching? 


### ProxyNode

Let's call it a `ProxyNode` object for the sake of discussion. 

So where does a `ProxyNode` fit?  I don't think it makes sense for it to stand in for values or aliases, so maybe it can be derived from `Node.Entry`.  Could it stand in for directories, symlinks, or mixtures?  If not, it could be derived from `Node.File`. 

xxx 


### Doodles


```txt
        def sources_from_file(executor, node):
                ### 'node' is None for target scanner
                srcs = File('prog.srcs')
                srcs = [s.strip() for s in srcs.readlines()]
                executor.AddSources(srcs)

        pgm = Program('prog', [])
        pgm.Requires('prog.srcs')
        pgm.TargetScanner(sources_from_file)
```

### Comments

JGN: Still a draft; please ask questions to help me make it better.  There's an xxx where I know more is needed; suggestions welcome. 


## Greg Noel

Also see [[!bug 810]] which discusses emitters and overrides for them.  The solution to that will require both something like the proposal above plus some flavor of the kind of thing done by [DynamicSourceGenerator](DynamicSourceGenerator) (which is very interesting but also very unSCons-like).
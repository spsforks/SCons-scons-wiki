A page for the actual Rearchitecture design.

This should, ideally, not reference the current SCons design and/or implementation.  For that, go to [Implementation](Rearchitecture-Implementation).

*Note: this is part of a historical planning exercise that was not developed. The ideas would ceratainly be considered in any future rearchitecting project.


<!-- TOC -->
<a name="contents">

  - [Classes](#classes)
    - [Entities](#entities)
      - [File System entities](#file-system-entities)
        - [Entry Stem Cell](#entry-stem-cell)
        - [File](#file)
        - [Directory](#directory)
        - [Symlink (not yet)](#symlink-not-yet)
      - [Python Value](#python-value)
      - [Alias](#alias)
    - [Schedule graph](#schedule-graph)
      - [Schedule items](#schedule-items)
      - [Schedule arcs](#schedule-arcs)
    - [Environment](#environment)
    - [Context](#context)
    - [Some categorization to combine these classes](#some-categorization-to-combine-these-classes)
      - [Action](#action)
      - [Tool](#tool)
      - [Builder](#builder)
      - [Executor](#executor)
  - [Not Classes](#not-classes)
    - [Emitters](#emitters)
    - [Scanners](#scanners)
  - [Discussion](#discussion)
  - [File System entities](#file-system-entities)
  - [Schedule arcs](#schedule arcs)
  - [Is a schedule graph a dual?](#is-a-schedule-graph-a-dual)
  - [Returning Executors from Builders](#returning-executors-from-builders)
    - [Greg Noel Builder Return Proposal](#greg-noel-builder-return-proposal)
  - [Emitters v. Scanners](#emitters-v-scanners)
    - [Greg Noel Emitter Scanner Proposal](#greg-noel-emitter-scanner-proposal)
      - [Emitters](#emitters)
      - [Scanners](#scanners)
      - [Dependencies](#dependencies)
      - [Emitter help](#emitter-help)
      - [ProxyNode](#proxynode)
      - [Doodles](#doodles)
      - [Comments](#comments)
<!-- /TOC -->

# Classes

## Entities

This is the encapsulating concept for all of the "things" that can get built or from which we can build other things: files, directories, Python values, Aliases, _etc_.  `Entity` itself probably ends up as an abstract base class with concrete subclasses.

`Entity` objects are responsible for remembering their own (upstream) dependencies, probably by referring to an associated `Executor` that collects the common information for a group of objects that are built at the same time.  (((JGN: Downstream dependencies ("targets" of an entity) are calculated elsewhere; refer to that here?)))

(((JGN: XXX add list of `Entity` attributes: `contents()`, `str()`, `.path`, `.abspath`, ...)))


### File System entities

[Discussion](#filesystem-entities)


#### Entry Stem Cell

Protean file system `Entity` that morphs into a specific type.

(((SK: This should _not_ be implemented as it is currently, by actually changing the `__class__` attribute.  It should be some kind of container that defers to a separate, real `File` or `Directory` object after disambiguation.)))


#### File

A class for representing SCons' notion of an on-disk file.

This (or perhaps an underlying class that gets wrapped by this) should support many of the same methods that a Python `file` object does:  `read()`, `readlines()`, etc., so that a user can just `.read()` from the SCons `Entity` to get the contents, and not have to know about our methods like `.get_contents()`.


#### Directory

A class for representing SCons' notion of an on-disk directory.

Should support two different types of "content" (with different names, as soon as someone coins them):

   1.  A checksum of the (sorted) list of names within the directory (to determine if a name has been added or deleted within the directory).
   1.  A checksum of the _contents_ of the files + subdirectories within the directory (to determine if the directory hierarchy should be re-copied because anything in it changed).
(((SK:  Discussion:  I'm not sure where use of this distinction ends up living yet.  My two use cases are:  1) make an object file depend on the `$CPPPATH` directories in the first form, so we can figure out that we have to re-scan for .h file dependencies if someone added/deleted a file; 2) the current use case of copy-over-a-directory-hierarchy if something in it changed.))) (((JGN: I like the concept; it could avoid the `os.stat()` call on the files if the directory is unchanged and the `os.stat()` and `readdir()` on the directory would normally be amortized over multiple uses.  (It's a bit more complex that the scheme I had in mind, but it could be much more efficient.)  Maybe it deserves a mention under Performance>Caching above.  The names in the directory should be cached, so a not-exists check needn't do an `os.stat()`.  If the "contents" are calculated, I'd expect the "content" to be available as a side-effect.)))


#### Symlink (not yet)


### Python Value

A class for wrapping an in-memory value in SCons.


### Alias

DISCUSSION (i.e., not-thought-through observations):

`Alias` Nodes have turned into a kind-of catch-all for a number of current behaviors:

* "Expand" to other targets, especially for names the user will type on the command line (e.g. "scons install" -- the original, canonical use case).
* Arbitrary "virtual node" in the dependency graph for simplifying large `NxM` dependency meshes by collecting "intermediate results" in a single node.  (((JGN: These should now be collected in the Executor, making this usage unneeded.)))
* Hang arbitrary actions in the DAG to be executed after a set of (dependent) targets have been built.  (((JGN: Never seen this.  Does it work?  We know that `AddPostAction` on one doesn't work; if aliases executed actions at all, I'd expect that case to be OK.)))
As well as wish-list items:

* Be able to use an `Alias` as a source to a builder call, and have it "transparently" expand to the sources of the Alias, so you can use an Alias as a short-hand to refer to an arbitrary collection of `.c` files (e.g.) the same way it can be used on the command line to refer to an arbitrary collection of targets.  (((JGN: maybe there's a synergy here with [TargetDrivenBuilderCreation](TargetDrivenBuilderCreation), as new Builders may need to be created dynamically.)))
* ((()))
Are these distinct enough concepts that there should be separate types of Nodes for them?  On the one hand, collecting all this functionality in one Class may burden it with too much generality.  On the other hand, separate classes might just get too confusing ("No, you used a `TargetAlias` there, you really need to use a `SourceAlias`..."  Bleh.).

Currently, I think I lean towards keeping all this "virtual node" functionality in a single class.  The current `Alias` class hasn't gotten unweildy so far.  (I could see renaming it `Phony` or `Virtual` or something, though, if that would be more understandable.)

WILD IDEA:  Is it possible that `Alias` should basically be `Entity`, except as a concrete, not abstract, base class?  That is, is the set of functionality we ultimately expect from an Alias (be able to depend on other targets, be able to have other targets depend on you, be able to have an action executed when you're "updated") sufficiently general that it really defines the minimal set of what we expect from an `Entity`?  So could other `Entity` objects like `File` and `Directory` be implemented as subclasses of `Alias`, like Python new-style classes all inherit from `object`?   Hmmm...  Gotta think on this more to figure out how half-baked it is...
(((JGN: There ought to be a base class that does this, yes, but I'm not so sure it's `Alias`.  Doesn't `Node` have all this functionality now?  What is there in `Alias` that should be moved?)))
(((SK:  Leaning against this now.  Inheritance is a source of more problems for us than it solves.)))
(((JGN: Yeah, but see the comment under "Builders" about an Alias-specific subclass of Executor.)))


## Schedule graph

The schedule graph is the transverse dual of the dependency graph: the schedule graph can be calculated from the dependency graph and the dependency graph can be calculated from the schedule graph.

[Discussion](#is-a-schedule-graph-a-dual)


### Schedule items

(((We should probably call these "schedule items" (or something similar) as the architecture really manipulates two DAGs.)))

These are either the `Executor` objects themselves, or one-to-one with `Executor` objects.


### Schedule arcs

Q:  Do these need to be distinct objects, or are they implied from connections between the schedule items?

A:  (((JGN))) Hmmm...  Actually, in TNG, the schedule items refer to `Entity` objects (for the labels, if you will) but have a direct link to the downstream schedule items they preceed.  Maybe it's simpler to say that the `Entity` objects maintain the upstream (dependency) links while the schedule items maintain the downstream (transverse) links.  To the `Entity` objects, the schedule item is the label to apply to their upstream arc, while to the schedule items, the `Entity` objects are the labels to apply to their downstream arc.  Clear as mud, eh?  See if the paragraph below catches the meaning.

Conceptually, an arc in the schedule graph is labeled with an `Entity` from the dependency graph.  In reality, a given schedule arc represents the M*N arcs from the set of M sources that produce a common set of N targets.

[Discussion](#schedule-arcs)


## Environment

The dictionary(?) of settings that govern the build of a particular flavor of target.  The implementation should be optimized for lightweight access and expansion of values.

It would be good to be able to re-use an existing implementation with defined semantics like the (now-)standard Python `string.Template` class, or Ka-Ping Yee's `Itpl` class, or even whatever waf ended up implementing as appropriate for solving build problems.

Current problem areas for performance include:

* Repeated expansion of the same variables (e.g. expanding the same $CXXCOM command line for every object file)
* Recursive expansion of variables
* Evaluation of arbitrary Python expressions
* Evaluation of callables
* Deferred evaluation of virtually everything (which causes much repeated evaluation)
My half-thought-through suggestion is to change the semantics in one crucial, but I think acceptable way:  get rid of deferred evaluation entirely.
(((JGN: Maybe; I don't have any strong feelings one way or the other.  I'd like to see what Ken _et.al._ come up with first; maybe something as simple as caching everything that doesn't have `$SOURCE` or `$TARGET` in  it would be enough, _i.e._, expand CCCOM every time but cache everything it uses.)))

At the time a `Builder` is called (or whatever replaces Builders), whatever values are necessary from the environment are expanded and nailed down.  Once per `Executor`.

My guess is we could prepare for this by announcing this change in the current code base.  My guess is that very few people are intentionally _relying_ on this behavior.  In fact, I've run into several people who thought the expansion was already happening at Builder-call time and were surprised that a later setting in the same environment would affect previous `Builder` calls.  Anyone who's consciously relying on this behavior is, I submit, actually complicating their build needlessly.

Drawback:  this makes for (more) order dependency in the SCons configuration, but we're not pure about that anyway, and I think it would be acceptable.


## Context

This would be the pieces of "environment-like stuff" necessary for actually executing a build action.  Right now the (old SCons) Environment is the only thing available, which contributes to all the expensive, repeated, deferred evaluation of its values for every `Executor` signature calculation.

That said, I'm not 100% sure what would end up here if the actual environment variables like `$CC` are expanded when the Builder is called.

(Note:  I borrowed this term from what little I understand after a quick glance at the waf architecture.  I don't think I'm using it the same way waf does, though.)

(((JGN: I use the term "context" for the class with no name, probably a [SubstitutionEnvironment](SubstitutionEnvironment) or something derived from it, that carries around the nascent Environment initialization from Configure, Variables, _etc_.)))


## Some categorization to combine these classes

An Action is an object that represents some sort of activity.  A Tool sets up Builders and provides them with Tool-specific Actions and other information to make them work.  A Builder creates an Executor to apply an Action on a set of Entities. xxx


### Action

xxx


### Tool

xxx (((Maybe belongs in its own second-level head?)))


### Builder

[Discussion](#should-builders-return-executors)

Eliminate emitters by subclassing?  That is, a Program() is really just a subclass of File with some additional methods and logic specific to what a Program Node needs?

(((SK:  I'm leaning against this now.  Poorly-thought-out inheritance is a big contributing factor to our current tangled mess, and I don't see any reason to think that would change this time around.)))
(((JGN: Ah, I think I begin to understand what you were thinking.  Yes, a builder-specific subclass of Node doesn't sing, but I'm wondering about a builder-specific subclass of Executor, or the general question of subclassing Executor to provide specific semantics (an Alias subclass, hmmm).  From the 10,000-meter perspective, a builder creates and inserts an Executor; I could see a subclass inserting special-case logic into the evaluation flow, maybe indeed subsuming emitters.  There's always been that case of an emitter wanting to look at a built file that's not created yet.  Hmmm...)))


### Executor

Discussion](#should-builders-return-executors)

One-to-one with DAGNodes?  Maybe the same?
(((JGN: Yes, modulo leaves of the dependency graph, which do not always have unique `Executor` objects.)))
(((SK:  Say more about leaves (source files) not having unique `Executor` objects.  Do you mean that they need to show up in the dependency graph (because they have to get evaluated) but because they don't actually build, all the sources can re-use the same Singleton `Executor` object?)))
(((JGN: This was more of an observation as to how null `Executor` objects are used now, an implementation choice also made by TNG.  To get a true transverse dual for the schedule graph, there would need to be a unique `Executor` object for each Entity, but I don't think that's absolutely needed (and certainly not desired).  It's possible that we could get rid of the null `Executor` entirely, as there are (should be?) only a few places that depend on it, but I suspect it would be simpler to keep it.)))
(((SK:  Hmm, it feels cleaner to me to not have a null Executor if there's really nothing to be built.  On the other hand, that also smacks of the first generations of the current Taskmaster, where we thought not having it visit source nodes was an optimization.  It turned out to be cleaner architecturally to have it visit source nodes in order, because otherwise we had all sorts of evaluate-the-contents stuff hidden inside various other methods.  So I guess some kind of null Executor makes sense.)))
(((JGN: Good point about the stuff hidden all around.  I agree.)))

An `Executor` represents the execution of an action to bring a set of target `Entity` objects up to date with respect to a set of source `Entity` objects.
(((JGN: I think the `Executor` should accumulate the sources and sibling targets (currently accumulated in Nodes), turning the current MxN situation into an M+N.  This makes the dependency graph and the schedule graph more like spaghetti, but by careful abstraction we can make it almost transparent (it will have impact on things like deciders).)))


# Not Classes

xxx


## Emitters

[Discussion](#emitters-v-scanners-discussion)

xxx


## Scanners

[Discussion](#emitters-v-scanners-discussion)

xxx

# Discussion

Discussions about unresolved issues for the Design page.
*Note: after GitHub migration, a separate page no longer works well, so moved to end of main page.*

This should, ideally, not reference the current SCons design and/or implementation.  For that, go to [Implementation](Implementation).

# File System entities

(((JGN: Should we mention here that this is probably an ABC for the entities in this section?  Or is this the forwarding class that provides morphability by referring to one of the entity types in this section?)))
(((SK:  ABC?  What's that?  I was just viewing this as the encapsulating header for this section of the document, not as a separate class...)))
(((JGN: ABC === Abstract Base Class.  You already said the previous heading was an ABC, so it makes sense.  That's how it's implemented now: this heading would be equivalent to the `Base` class in FS.py.  My question is whether you want that same hierarchy in the re-architecture or if it would make sense for this class to be a referrer class that "defers to a separate, real `File` or `Directory` object" (_i.e._, it refers to one of the four object types that are the subheads for this section, which are implemented via a different base class).)))
(((SK:  Okay, I see what you're getting at.  I wasn't thinking of an ABC here, at least partly to cut down on the proliferation of classes.  The current `File.Base` class seems pretty useless as a separate class right now.  This is probably because I didn't really implement it as an ABC (for example, with `NotImplementedError` exceptions for methods that must be provided by the concrete subclasses).  I was just trying to be "object oriented..."  I could see benefit here to intentionally defining an ABC, but when you get down to it, is there really that much similarity between the two main concrete subclasses
(`File` and `Dir`) that there's significant benefit to a common ABC?  I don't know.)))
(((JGN: Er, you're still missing the question, which I guess should now be a trinary: Pick one: Is it a referral class (taking over the role of `Entry`, so `Entry` becomes a referred class)?  Should it be a base class, with common filesystem-oriented things?  Or should it not exist at all?  You've focused on the last two, to the exclusion of the first, which is really why I posed the question in the first place.)))
(((SK:  My suggestion is:  No "File System entity" class.  What we've labelled "Entry Stem Cell" below is a referral class.  A "Entry" holds ambiguous entries, and after disambiguation, it can refer to either a File or Dir object.)))
(((JGN: OK, I'll not fight it.  I just thought it might make more sense for a "Filesystem Entity" class that was optimized as a forwarding class that initially pointed to an "Entry" object until it was disambiguated, after which it pointed to a File or Dir (or Symlink or ...).)))
(((SK:  Well, that's just my current suggestion.  I'm not completely sure either way.  I see the advantage to what you're suggesting -- have each class do one thing well, instead of the "Entry" object needing to know how to forward requests *and* disambiguate.  But it also seemed like it might be cleaner to have fewer classes, too...)))


# Schedule arcs

(((SK:  "...labeled with _an_ Entity...?"  Really?  Singular?  Given that any arc really represents M\*N dependencies that get updated by that build, what's the advantage of labeling it with an arbitrary `Entity` from that set?)))
(((JGN: Yes.  Yes.  And yes. ;-) Abstractly  (conceptually) the nodes are replaced by arcs and the arcs replaced by nodes, so the M\*N arcs between entities that represent a build are replaced by M\*N nodes with arcs labeled with a (singular) entity.  Practically (actuality), the M\*N nodes are collapsed into a single node with M+N arcs.  Does that explain it better?  If so, do you want to rewrite it to make it clear?)))
(((SK:  No, it doesn't make it clear.  I'm not disagreeing with the idea of replacing M\*N nodes / arcs with a single nodes that accomplish the same work much more efficiently.  I'm confused as to why you then _label_ this with one arbitrary Entity from the set that's updated.  I'd find that labelling confusing.  I'd wonder, "Hey, wait a minute, I only see a label for `file1.obj` in this graph, but what happened to `file[2-N].obj` that are updated by the same compilation?  Based on my current understanding of what you're getting at, in other words, I'd find it less confusing to leave the arch _unlabelled_ instead of labelling it arbitrarily.  What's the advantage (or necessity) of labelling it?)))
(((JGN: OK, what we have here is a failure to communicate.  Let me try again.  If the simple dual were taken, each arc would be labeled with a single `Entity`.  But we don't do that; we collapse the M\*N nodes representing a build into a schedule item, which causes arcs to be duplicated.  The 2*M\*N (M\*N arcs on both the source and target side) are then combined with other arcs that have the same label, yielding M+N arcs, each with a single label.  No arbitrary labeling involved.  Are we there yet?)))
(((SK:  Sorry, I know I'm thick about this stuff, but I'm still not getting it.  You're going to have to dumb it down for me, so avoid slinging the fancy math lingo like "simple dual" unless you're going to take the time to educate me about it.  Let me explain my current understanding of what you're suggesting in really concrete terms, and you can tell me where I've gotten it wrong.  We're building three output files (a.out, b.out and c.out) from three input files (x.in, y.in and z.in).  All three outputs depend on (e.g. concatenate) all three inputs.  So there are 3x3 edges in the dependency graph, but their build step is collapsed into a single Node in the schedule graph.  Say that some of [abc].out are used in other build steps so there are scheduling steps that depend on them being up to date.  What I *think* I hear you saying is that any arcs "emanating" from that Node will be labelled with one of [abc].out, but I have no idea which one.  Or why the labelling is necessary.)))
(((JGN: (later re-edit: I'm making it three nodes crossing to four nodes, since with three of everything, it quickly becomes confusing.)  OK, we start with seven Files (three on the top and four on the bottom) and twelve arcs.  We create the dual by changing the nodes to arcs and the arcs to nodes.  This gives us twelve nodes linked by, hmmm, I see the problem you're having with the analysis.  The hidden assumption is that the fan-in and fan-out are (approximately) the same for the original nodes above and below the MxN crossover.  That is the three "top" nodes each have a fan-in of four and the four bottom nodes have a fan-out of three.  When the three top nodes are converted to arcs, they each connect to four former arcs that are now nodes (and similarly for the bottom nodes, with four and three), so you get twelve arcs entering the collapsed node and twelve arcs leaving it.  Three quadruples of the entering nodes are redundant, with the same label, so they are merged and you get a node with three arcs entering it, each labeled with a single entity (and similarly with the arcs leaving).  So you get an input arc labeled with the single entity x.in, an input arc labeled with the single entity y.in, an input arc labeled with the single entity z.in, an output arc labeled with the single entity a.out, an output arc labeled with the single entity b.out, an output arc labeled with the single entity c.out, and an output arc labeled with the single entity d.out.  All entities label an arc, all arcs are labeled with a single entity.  Why is the labeling necessary?  Now I wish I hadn't mentioned it, but at the time, I thought I was giving an intuitive insight to make things clearer.)))


# Is a schedule graph a dual?

(((SK:  [GregNoel](GregNoel) suggests that the schedule graph should be a dual of the dependency graph.  The definitions of dual I find suggest that a dual is actually a mapping of enclosed plane regions of a graph to Nodes in the dual graph, with arcs in the dual graph that correspond to arcs in the original graph that border two plane regions.  Greg, either "dual" isn't the correct term for what you have in mind, or I have the incorrect definition of "dual", or you have some more sophisticated transformation in mind that we need to define more specifically.  Please clarify.)))
(((JGN: Huh.  I threw away my forty-year-old college textbooks when I moved (after all, what use would I have for them?), but I still have some of my class notes (some were lost in a roof leak), including my first semester of graph theory.  My instructor was a brilliant teacher who had the bad habit of using a different notation than the textbook and covering about three times what was in the official syllabus, so even if I had the textbook I may not have been able to find the relevant chapter.  However, on one page I find (translated from my shorthand, badly needed when taking notes in his classes), "Dual (equivalent) exchange nodes, arcs; split and merge" surrounded by calculations about digraphs.  It's nowhere near the notes about planar graphs (which is all Wikipedia covers) and just as far from the topic of DAGs.  There are some calculations about merging and splitting nodes and arcs as part of the process (which I was doing) and a lemma that duals G* and G** of a graph G may not be the same (which I hadn't remembered, I thought duals were topologically equivalent), ah, I see, the splitting and merging can cause them to be different (but there's some sort of a family equivalence? I'm not understanding all this).  Given that graph theory was his field, it's possible that these were research results that didn't stand the test of time and duals are now only defined on planar graphs, but it also could be that Wikipedia, _et.al._, are simply covering the highlights, not the whole topic.  It's clear that a DAG need not be planar, so that definition of dual cannot be applied here.  My notes reflect what I remember about duals, but there doesn't seem to be any description of what I remember in today's references, at least under that name.  So I don't know where to go from here.)))

<a name="builders_return_executors"></a>
# Returning Executors from Builders

## Greg Noel Builder Return Proposal

Several trains of thought have made me ponder what a builder should return.  Somehow, a list of Nodes just never has sat well with me.

The idea is that a Builder should return an Executor.  The Executor is revamped so that it's derived from a `list` and the items exposed via that list are the targets of the build.  In other words,
```py
pgm = Program('prog', srcs)
cmd = pgm[0]
```
 still has the same result.  There are probably a few gotchas having to do with adding lists that will have to be resolved, but it should be almost completely backward compatible.  (Yes, that's another way of saying it's not completely backward compatible (I can think of a couple of weird examples), but they're going to be pretty rare, and I'm pretty sure we can cause an error in those cases so there will be no silent change of semantics.)

So what do we get?

Well, you could say,
```py
 lib = SharedLibrary('mylib', [])
 lib.AddSources('foo.c', 'bar.y')
 lib.AddSources('src/*.cpp')
 lib.MergeFlags('-Dcpp -O2 -framework Python')
```


Emitters are then functions that operate on an Executor.  They can use an internal entry point to add a direct predecessor or use `AddSources()` as above if there might be multiple steps.  Adding additional targets would be done via an internal API; I'm not sure if it should have a public exposure.

I think this also takes us a big step closer to being able to add steps at build time.  I'm still puzzling through the implications, but I'm pretty sure we can mark an Executor once it enters the build pipeline.  If we can do that, then we can allow modifications to Executors any time before they are committed to execution.  And if we can generalize the `AddSources()` functionality so that it can be easily extended with other types, we can do [Gary's dynamic generators](DynamicSourceGenerator) as well as [George Foot's amazing dynamic builder creator](TargetDrivenBuilderCreation) while still being very "SCons-like".

A problem: What to return from `Object('foo.c bar.c'.split())`?  When it was just a list of nodes, it was simple, but if we're going to return an object, it must somehow be a composite object containing (or referring to) both build steps.  Something to figure out.

# Emitters v. Scanners

SCons currently divides processing between an emitter (run at parse time to identify secondary sources and targets) and scanners (run at build time to identify additional upstream dependencies).  The SCons design did not anticipate that an emitter might need to examine the file in order to make these determinations.


## Greg Noel Emitter Scanner Proposal

Executive summary: Emitters generate guesses as to what a build will use as sources and targets.  Scanners can modify those choices if they are incorrect.  Emitters are not allowed to open the source; scanners are invoked after the source is up-to-date.


### Emitters

Emitters are a function of an Executor object and a Node object.  The results are applied to the Executor object.

(Note that a given Node object can be used with more than one Executor object and a given Executor object can use more than one Node object, so neither is a good place to cache information about the other.  Should SCons provide a way to cache any such information?)

We introduce an unenforceable convention that emitters do not look at the source file.  (We could semi-enforce it by not allowing File.read() during parse time, but users could still open() the file.) If the emitter can't determine the exact set of [modified sources][1] and targets, it is given some guidelines and other help, discussed below.

[1]: Is there ever a case where an emitter actually adds additional sources?  If there is, I argue that the case is rare enough that the emitter can make specific provisions to do it.

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

GregNoel: Also see [bug 810](/SCons/scons/issues/810) which discusses emitters and overrides for them.  The solution to that will require both something like the proposal above plus some flavor of the kind of thing done by [DynamicSourceGenerator](DynamicSourceGenerator) (which is very interesting but also very unSCons-like).


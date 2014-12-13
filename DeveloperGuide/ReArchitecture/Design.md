
A page for the actual Rearchitecture design. 

This should, ideally, not reference the current SCons design and/or implementation.  For that, go to [DeveloperGuide/ReArchitecture/Implementation](DeveloperGuide/ReArchitecture/Implementation). 

[[!toc 4]] 


# Classes


## Entities

This is the encapsulating concept for all of the "things" that can get built or from which we can build other things: files, directories, Python values, Aliases, _etc_.  `Entity` itself probably ends up as an abstract base class with concrete subclasses. 

`Entity` objects are responsible for remembering their own (upstream) dependencies, probably by referring to an associated `Executor` that collects the common information for a group of objects that are built at the same time.  (((JGN: Downstream dependencies ("targets" of an entity) are calculated elsewhere; refer to that here?))) 

(((JGN: XXX add list of `Entity` attributes: contents(), str(), .path, .abspath, ...))) 


### File System entities

[/Discussion#FileSystem entities](DeveloperGuide/ReArchitecture/Design/Discussion) 


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
(((SK:  Discussion:  I'm not sure where use of this distinction ends up living yet.  My two use cases are:  1) make an object file depend on the $CPPPATH directories in the first form, so we can figure out that we have to re-scan for .h file dependencies if someone added/deleted a file; 2) the current use case of copy-over-a-directory-hierarchy if something in it changed.))) (((JGN: I like the concept; it could avoid the `os.stat()` call on the files if the directory is unchanged and the `os.stat()` and `readdir()` on the directory would normally be amortized over multiple uses.  (It's a bit more complex that the scheme I had in mind, but it could be much more efficient.)  Maybe it deserves a mention under Performance>Caching above.  The names in the directory should be cached, so a not-exists check needn't do an `os.stat()`.  If the "contents" are calculated, I'd expect the "content" to be available as a side-effect.))) 


#### Symlink (not yet)


### Python Value

A class for wrapping an in-memory value in SCons. 


### Alias

DISCUSSION (i.e., not-thought-through observations): 

`Alias` Nodes have turned into a kind-of catch-all for a number of current behaviors: 

* "Expand" to other targets, especially for names the user will type on the command line (e.g. "scons install" -- the original, canonical use case). 
* Arbitrary "virtual node" in the dependency graph for simplifying large `NxM` dependency meshes by collecting "intermediate results" in a single node.  (((JGN: These should now be collected in the Executor, making this usage unneeded.))) 
* Hang arbitrary actions in the DAG to be executed after a set of (dependent) targets have been built.  (((JGN: Never seen this.  Does it work?  We know that [AddPostAction](AddPostAction)() on one doesn't work; if aliases executed actions at all, I'd expect that case to be OK.))) 
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

[/Discussion#Is a schedule graph a dual?](DeveloperGuide/ReArchitecture/Design/Discussion) 

(See related discussion about [GregNoel](GregNoel)'s research into a new TaskmasterNG algorithm at [GregNoel/TaskmasterNG](GregNoel/TaskmasterNG).) 


### Schedule items

(((We should probably call these "schedule items" (or something similar) as the architecture really manipulates two DAGs.))) 

These are either the `Executor` objects themselves, or one-to-one with `Executor` objects. 


### Schedule arcs

Q:  Do these need to be distinct objects, or are they implied from connections between the schedule items? 

A:  (((JGN))) Hmmm...  Actually, in TNG, the schedule items refer to `Entity` objects (for the labels, if you will) but have a direct link to the downstream schedule items they preceed.  Maybe it's simpler to say that the `Entity` objects maintain the upstream (dependency) links while the schedule items maintain the downstream (transverse) links.  To the `Entity` objects, the schedule item is the label to apply to their upstream arc, while to the schedule items, the `Entity` objects are the labels to apply to their downstream arc.  Clear as mud, eh?  See if the paragraph below catches the meaning. 

Conceptually, an arc in the schedule graph is labeled with an `Entity` from the dependency graph.  In reality, a given schedule arc represents the M*N arcs from the set of M sources that produce a common set of N targets. 

[/Discussion#Schedule arcs](DeveloperGuide/ReArchitecture/Design/Discussion) 


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


## Some catagorization to combine these classes

An Action is an object that represents some sort of activity.  A Tool sets up Builders and provides them with Tool-specific Actions and other information to make them work.  A Builder creates an Executor to apply an Action on a set of Entities. xxx 


### Action

xxx 


### Tool

xxx (((Maybe belongs in its own second-level head?))) 


### Builder

[Should Builders return Executors?](DeveloperGuide/ReArchitecture/Design/Discussion) 

Eliminate emitters by subclassing?  That is, a Program() is really just a subclass of File with some additional methods and logic specific to what a Program Node needs? 

(((SK:  I'm leaning against this now.  Poorly-thought-out inheritance is a big contributing factor to our current tangled mess, and I don't see any reason to think that would change this time around.)))   
(((JGN: Ah, I think I begin to understand what you were thinking.  Yes, a builder-specific subclass of Node doesn't sing, but I'm wondering about a builder-specific subclass of Executor, or the general question of subclassing Executor to provide specific semantics (an Alias subclass, hmmm).  From the 10,000-meter perspective, a builder creates and inserts an Executor; I could see a subclass inserting special-case logic into the evaluation flow, maybe indeed subsuming emitters.  There's always been that case of an emitter wanting to look at a built file that's not created yet.  Hmmm...))) 


### Executor

[Should Builders return Executors?](DeveloperGuide/ReArchitecture/Design/Discussion) 

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

[Emitters v. Scanners discussion](DeveloperGuide/ReArchitecture/Design/Discussion) 

xxx 


## Scanners

[Emitters v. Scanners discussion](DeveloperGuide/ReArchitecture/Design/Discussion) 

xxx 

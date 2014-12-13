

# Target-Driven Builder Creation


## Concept

The core idea here is to set up a system that allows you to dynamically tell scons how to build a particular target at the point that target first enters the dependency graph, without having to explicitly tell scons in advance how to build every target.  The key is to queue up the builder on demand.  The prerequisite is some way to determine, given an arbitrary target name, how to construct the right builder for that target. 


## Why?

The main benefit here is that you don't have to tell scons in advance how to build every target (including intermediates) in your build.  Doing that explicitly for a large build is long and tedious, and doing it automatically based on scans of the source tree is slow for large source trees; either way, you end up fully populating your dependency graph even if the user only asked to build a subset of the data, via command line options. 

Other problems arise with generated files, especially when they are then processed by scanners and they may depend on arbitrary other files, which might also be generated. 

Another case is where you want to completely avoid parsing SConscript files for sub-modules of your build if that sub-module is not actually involved in the build requested by the user. 

Beyond scalability problems, I also think this method of specifying builders is more natural, and likely to result in a more robust build overall. 


## Related Pages

Some other people have wanted this kind of thing before, and have achieved it to varying degrees - in particular, somebody anonymous wrote [DynamicSourceGenerator](DynamicSourceGenerator) and later refined it into [BuildTimeCallback](BuildTimeCallback).  The ideas are good, but not being able to build specific intermediate files is not acceptable to me.  Essentially the problem is that unless you build some master top node, the builders for deeper targets won't get queued up.  In the former example, he uses an [AlwaysBuild](AlwaysBuild) rule to do the queuing, which might get around that problem, but implies once again doing a lot of work on startup that you might not actually need later on. 

Wanting to be able to build arbitrary intermediates by name is the crux of the problem here - there are a variety of workarounds if you don't care about this, but if you want to be able to build the intermediates then target-driver builder queuing is really the way to go.  Fundamentally, you need to be able to get from the string name of an intermediate to how to build it, without telling scons in advance anything about that intermediate file.  That's what it means to be target-driven. 


## Example

As a case study, suppose you have a directory tree like this: 


```txt
   src
    +-- prog1
    | foo.cpp
    | bar.cpp
    +-- prog2
    | baz.cpp
    | quux.cpp
    :
```
and you want a SConstruct that can build any program listed under "src", without needing an explicit list of the source files for that program, and without having to scan the disk for all source files in every program prior to building anything. 


## Implementation

The following SConstruct achieves this aim. 


```python
#!python 
    import glob
    import os
    
    class ProgramLookup:
        def __init__( self, env ):
            self.env = env
            self.nodes = {}
    
        def lookup( self, name, **kw ):
            if name.startswith("exe/"):
                if name in self.nodes:
                    return self.nodes[name]
    
                program_name = os.path.splitext( os.path.basename(name) )[0]
                sources = glob.glob( "src/%s/*.cpp" % program_name )
    
                node = File(name)
                self.env.Program( node, sources )
                self.nodes[name] = node
                return node
    
    env = Environment()
    env.lookup_list.append( ProgramLookup(env).lookup )
```
Then, assuming you have the directory layout above set up properly, try: 


```txt
    scons exe/prog1.exe --tree=prune
    scons exe/prog2.exe --tree=prune
```
Note that in each case scons only needed to populate the bit of the dependency tree that it's actually working on.  Of course, you can build both at once, if you like. 


## General Technique

The general technique I'm using here is to hook into the way Environments convert names into Nodes.  The key method here is "arg2nodes", in Environment.py, which offers the incoming string to a list of functions before falling back on creating a default type of Node (usually a File).  If any of the functions returns a Node (or a list of Nodes) then the default Node creation behaviour is bypassed. 

So adding a function to this lookup list allows us to jump in before the default conversion takes place and apply our own conversion, at the same time queuing up the actual builder to build the node, just in time for when SCons actually looks for it. 

The basic pattern in the code above is taken from Aliases.py. The lookup method picks up any names beginning with "exe/", ignoring anything else. Matching names get looked up in an internal dict, because scons doesn't seem to cache these lookups itself (maybe it should?). Then we disect the name, extracting the actual program name, scan its source files, and queue up a Program job to build that program from those sources. Note that we have to explicitly create a File node - we can't just use a string because otherwise we'll get recursed into again. 

There is another alternative to get around the recursion though without hard-coding the type of node.  If we initially add "None" to our dict, then when we re-enter, we return None straight away, and let scons create the node itself the second time around.  Then we fill in the blanks, providing a builder for the node SCons has just created.  This seems preferable to me, but probably doesn't make much difference and the double-entry is messier. 


## About the lookup list

The lookup list appears to be only used at present for Aliases.  The Alias system inserts a lookup function which recognizes if the incoming string is an Alias name, and, if it is, it returns the actual Node list for that Alias.  This is the guts of how Aliases work. 

As far as I can see, it serves no other purpose at the moment, but it's almost perfect for what we need here. 


## Converting a target name into a builder

You could create your dynamic builders in various ways.  In the case above, I just recognize target executable names and convert them into source directory names, then queue up a builder to build all those files - all in the lookup function. 

For production use, to me the most obvious idea is to register regexp patterns in advance, with each regexp linked to a builder factory.  This way the core lookup code doesn't know the details of how to construct builders, and build-specific code can supply those details in a nice detached manner. 

Your mileage may vary though - you might find another system works better for you. 


## Bigger builds

This is just an illustration - many things you'd want in a code build are absent here - and probably for most code builds you can get away with just scanning the whole source directory anyway. But the larger your source tree, the more time you waste scanning it every time you run scons, if you didn't really want to build the whole thing anyway. 

My interest in scons is not so much for code builds, as for building non-code data, mostly for use in games.  Game data builds tend to have much deeper dependency trees than code builds, with much more complex scanner requirements.  In many cases, the output from a job depends on its input's contents in ways that are hard to predict unless you scan its input directly. 

We also have a lot of files in our source tree - 40,000 at my last count.  Naively scanning through this tree costs us over a minute every time we run scons.  Some source files are exploded into a large number (100+) of smaller intermediate targets, which each then go through further processing individually.  Simply looping over these targets here to queue up scons builders is pretty slow on its own. 


## Missing features and complications


### Multiple targets

Builders with multiple targets will make things interesting - we really need to insert entries into self.nodes for the alternate targets too, in case we end up trying to requeue the builder, which would be bad. 


### Pluggable pattern-based lookups, and efficiency

I've implemented this now, and it feels good.  The performance also seems reasonable - there is a measurable overhead in checking patterns on every node touched by our build, but that will be negated by the benefit we get from not queuing everything on startup.  Overall I'm pleased with the current level of performance. 

In practice, we need around 200 patterns to cover the 10,000 builder instances queued in our complete build, so the numbers aren't prohibitive.  As the pattern list grows, we also have options to process it more efficiently. 


### Clean

As it stands, a plain "scons --clean" won't do very much because it doesn't know about any targets.  To get any real effect, you need to also specify a target to clean, e.g. "scons --clean exe/prog1.exe".  Then it will clean prog1.exe and anything it used to build it - whatever is in the dependency tree it gets from trying to build prog1.exe. 

To actually clean everything, if you have an "all" target you could use that.  Otherwise, the most effective way is to just delete the target directory, if you really want to clean out everything! 


## Questions

These are questions for more experienced scons users and developers. 

1. Is env.lookup_list (or Node.arg2nodes_lookups, which defines the default value for env.lookup_list) fair game for user customisation? Is it in danger of vanishing in a later release, and if so, could we make it (or something similar) part of the official API? 

2. Is this system going to fail for some reason I haven't foreseen? It seems to work as it stands, but maybe I missed something. 

3. Am I intercepting at the wrong level?  Should I be redefining the arg2nodes method itself? 

4. Could we improve the performance of arg2nodes? It calls the lookup functions again and again with the same string names - caching that up in arg2nodes would seem sensible. 

5. Or is there a better way to do this? Bear in mind the requirements - zero startup cost, no scanning of things that aren't going to be used in the current execution, and we need to be able to build a specific intermediate by name. 

Thanks in advance for any feedback on this method. Let me know if anything is unclear. I'd also be interested in hearing if anyone else finds this approach useful, e.g. for the kind of thing being solved by the [DynamicSourceGenerator](DynamicSourceGenerator) wiki page I linked to earlier. 

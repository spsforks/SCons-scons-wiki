**NOTE:**  We're trying to use this page as a forum to clarify how `VariantDir()` is intended to be used, how (and why) it may differ from the ways most people expect it to work, maybe figure out how to improve the interface so it's less counter-intuitive, etc.  **Please** add clarifying questions, post "why doesn't this work?" examples, add your own tips, etc.  Feel free to dive in and reorganize information if it helps make things clearer. - SK 

**Table of Contents**

[TOC]


# Dueling Models: SCons v. GNU | A Tutorial

[This section added by [GregNoel](GregNoel), 2007-02-18] 

_[Reply/comment by [StevenKnight](StevenKnight):  Greg, I think this section should be moved to a separate page.  All the stuff about `Repository` isn't (IMHO) essential to understanding how to use `VariantDir()`--or at least, it isn't supposed to be.  It's supposed to be completely orthogonal to use of `VariantDir()`, and to the extent that you can use `VariantDir()` completely successfully without a `Repository()` call anywhere in your tree, I assert that this is, in fact, the case.  I think discussing `Repository` here only confuses the larger group of people who just want to get a handle on the quirks of using `VariantDir()` within a single, repository-less tree.  I do think it makes sense to link to this information from this page--the discussion of the models is good--and leave the rest of this page to discuss only use of `VariantDir()`.  If you agree, feel free to move it, or let me know and I'll be glad to.]_ 

_[JGN: Not a problem.  As you may recall, I originally wrote about the different models in a message to the mailing list, and intended to transcribe it into a wiki page, but it never got high enough on my list until you brought up this page.  If you think it's a better fit on its own page, be my guest.  As you know, I'll be out of town for a week, so I won't have this high-speed connection; if you want to take care of it, that's fine with me.  It's clear that this page should refer to this section's content, since you can't make sense of `VariantDir()` without understanding it, but I'll leave that to you.  (And if this section has its own page, I could whip up a couple of examples using both `VariantDir()` and `Repository()`; I'll look into that when I get back.)  Let me know where it goes.  Tks.]_ 
Executive summary
: 
Unlike GNU, SCons deals with three directory trees: the build tree, where SCons will put the built targets; the source tree, where SCons looks for sources; and the working tree, which is where the `scons` command is issued and where SCons keeps its own control information.  One physical tree can serve more than one role; by default, all three logical trees are the same physical tree.  To separate the build tree from the working tree, you want the VariantDir() function.  To separate the source tree from the working tree, you want the Repository() function. 



Probably the greatest source of confusion with `VariantDir()` is that the SCons model for how directories are organized differs from the GNU model.  The GNU model is what most programmers with a background in `make` have been using, so they try to use `VariantDir()` as it would be used in a GNU-style build and are frustrated when it doesn't work as they expect. 


## The GNU model

In the GNU model, there are two directory trees involved: 

* **Source**.  A complete source tree, such as one checked out from SCCS, RCS, CVS, or SVN. 
* **Build**.  All the generated files: programs, libraries, binaries, _etc_. 
In this model, the source tree never contains any built file (with the sole exception of the `configure` script that came with the checked-out sources).  The user modifies files in the source tree and runs `make` in the build tree to regenerate the objects. 


## The SCons model

In the SCons model, there are three types of directory trees involved: 

* **Repository**.  Contains sources.  There can be more than one repository tree.  (It's possible to build a project and use it as a repository; SCons will automatically use the pre-built objects if possible.) 
* **Work**.  Contains the source files under development. 
* **Yield**.  Unfortunately, SCons calls this the "build" directory, even though it isn't the same thing as the GNU build directory, so we'll use the name "yield" to keep the concepts distinct. 
In this model, everything starts with the work directory, a scratch directory where modified files under development are kept.  The repositories are conceptually added _behind_ the work directory; typically, one repository tree would be the result of a checkout from a repository like Aegis, SCCS, RCS, CVS, or SVN.  The yield directory is conceptually added _before_ the work directory, so that when SCons "looks in" the yield directory it "sees" all of the files in the repositories with the work files in front. 

When SCons is invoked, it assumes it is running in the work directory.  To tell SCons to build something, you give it the _source_ name.  In general, SCons builds any generated files in the same directory as the source, so if you use a name in the yield directory, the generated files accumulate there.  At the same time, SCons accumulates its own control information in the _work_ directory, not in the yield directory, since it's the _repository_ directories where the original sources live. 

The advantage of this model is that the work directory usually contains only a few files: just the ones that are being edited, plus a few control files.  The source files stay in the repository directories and the generated files accumulate in the yield directory, so there's nothing to clutter up the work directory. 

Note that this model works best if individual files can be checked out of the repository into the work directory, since updates from elsewhere can be merged in; this works for Aegis, SCCS, RCS, and CVS, but, unfortunately, _not_ for SVN. 


## The Duel

The difficulty arises because the GNU model doesn't have an equivalent of the work directory, and it's not the same as either the source or the build directory.  Since it contains sources, the natural expectation is that it's equivalent to the source directory, but it's really closer to being the _build_ directory.  Trying to use `VariantDir()` so that the source directory remains pristine doesn't work, since SCons feels free to create files within what it presumes to be the work directory.  (The closest match is that the yield directory plus the work directory is equivalent to the build directory, but that's still not exact.) 

To get SCons to simulate a GNU-style build directory, don't use `VariantDir()` at all; instead, use `Repository()` to tell SCons where to find the sources.  Or create the build directory, and run this command in it:  
 `     scons -Y /path/to/source [options] [targets]`  
 This will create all targets relative to the work (current) directory, looking in the repository directory to find the sources.  (_Caveat_: As of 2007-02-18, the SConstruct must be manually copied to the top of the build tree for this to work; a near-future version of SCons will remember the repository location between invocations and this copy will not be needed.) 

Then, if you want to try a SCons-style yield directory and get all of the clutter out of your work directory, you can experiment with `VariantDir()`.  At that point, all of the gnashing of teeth and rending of garments in the next sections will be useful as you work it through. 


# A Brief Introduction | What And The Why

[This section added by [StevenKnight](StevenKnight)] 

`VariantDir()` is a powerful tool for enabling the separation of built files from their sources. This is useful for several reasons: 

1. You can now build different 'build types' into different directories (Release, Debug, etc) 
1. You don't clutter up your source directory with intermediate files. 


---

 

NOTE: the rest of this page is mostly about the `VariantDir()` function.  Most people instead use the variant_dir argument to SConscript, which has much more natural behavior.  There's some discussion of this below, but perhaps not enough.  I don't have time right now, but super quickly, to use variant_dir in the most common way, put this in your SConstruct: 
```python
env = Environment()
Export('env')
SConscript('SConscript', variant_dir='build')
# and more SConscript calls as desired
```
Then in SConscript: 
```python
Import('env')
Program('foo', 'foo.c')
```
will do all the right stuff, including better subdir behavior in many cases (but not all -- some of the stuff discussed on the rest of this page is still relevant and important). 



---

 


# A More In Depth Look | How

The function itself takes two arguments: the source directory, and the build directory. 

While it has a simple interface, you may initially find its use a little counter-intuitive and perhaps even confusing (don't worry, you're not alone!). One might expect SCons to take files in the specified 'source' directory, and compile them to said 'build' directory. 

`VariantDir()` instead indicates to SCons that if anyone specifies a source file *in* the build directory, to look for the source file from the source directory, copy it to said location, and compile it. 


## Woaaaah, Too Much Talk, Not Enough Examples!

Fair enough. So, the problem you may run into is this: 


```python
environment = Environment()
environment.VariantDir('build/', 'src/')
environment.Library(target="Foo", source=["src/foo.cpp"])
```
And yet it's still building the files in src/foo.cpp? The reason is because you need to specify your source=[build/foo.cpp](build/foo.cpp). I know, I know, it's stupid. 

-- Author note: I was fixing this, but I'm getting angry thinking about how stupid SCons is with this behaviour. Here's the garbage that some author wrote below. I'll make it more legible later, once I calm down my SCons rage. :P 


### Why does SCons do it this stupid way?

Here's the counter-example: 


```python
env1 = Environment()
env2 = Environment(CCFLAGS = '-g')
env1.VariantDir('build1/', 'src/')
env2.VariantDir('build2/', 'src/')

env1.Library(target="Foo", source=["build1/foo.cpp"])
env2.Library(
    target="Foo",
    source=["build2/foo.cpp"],
    CCFLAGS = '$CCFLAGS -DSPECIAL_DEBUG_FLAG'
)
```
`VariantDir()` is really designed around the supporting multiple side-by-side variants, which may be built in different ways.  The only way to guarantee that the flags you want get applied to one variant but not the other is to refer to separate "source file copies" that represent the different compilation steps. 

And because the SCons model requires that you specify lists of input _source files_ from which the target name(s) are derived (instead of specifying target files and deriving the sources using pattern rules, like Make does), you have to refer to the source files as if they live in the build directory, so that you can distinguish between the builds taking place in the `build1` and `build2` directories. 

Part of the problem is that the chosen name `VariantDir()` and the functionality are close enough to uses of "build dir" in other contexts that it easily leads people to think it works like other systems. 


## Back to the talk...

Quite apart from wondering why such a non-obvious way of specifying a built directory was devised (we'll see why shortly), there are a couple of concerns you may have about `VariantDir()`. Not least of these is likely to be that you must apparently write source file lists as if each source file is located in the build directory instead of the source directory. However, while you can do this (and it will work), it is not how `VariantDir()` was intended to be used. Instead, you should only need to specify the build directory once when calling a SConscript file stored in your source directory. Your list of source files and the call to the builder function you are using should be moved to this SConscript file, and all source files should be listed as relative to the source directory (as if that's where they should be built). Now when you build, because your SConstruct file calls the SConscript file as if it is in your build directory, and because all file names in the SConscript file are relative, the derived files are built in your build directory. 

So why does `VariantDir()` work like this? Well, we now know that you can write a SConscript file that has short relative paths, and then build the source in any location by simply specifying a build directory (as an alias for your source directory) and calling the SConscript as if it's in the build directory. What you may not immediately realise is that with this method you can create a second build simply by adding another two lines to your SConstruct file (one to create a second build directory and another to call the SConscript file again). Hence we have come to the real reason why `VariantDir()` may appear to be an unnecessarily complicated way to specifying a build directory. `VariantDir()` is primarily intended as a means of simplifying the otherwise complicated process of creating multiple build variants from the same source files. If you need to build a debug and release build of your project (or localised builds etc.) this can be very useful. But even if you don't, to use `VariantDir()` to separate the built files from your source files, you should at the very least separate the build logic into a single SConscript file, and export build configuration to it in the form of environment objects and so on. Not only does this keep things tidy, but if at some point in the future you need to build several different version of your project at the same time, it should only require some fairly trivial changes to your SConstruct file to do. 


## VariantDir() and files in other directories

Expanding on the example above, all references to files outside the current directory require special attention when using `VariantDir()`. 

For instance in the user guide section entitled [Top-Level Path Names in Subsidiary SConscript Files](https://scons.org/doc/production/HTML/scons-user/ch14s03.html)
the following example is given: 


```console
% cat ./SConstruct
SConscript('src/prog/SConscript')

% cat src/prog/SConscript
env = Environment()
env.Program('prog', ['main.c', '#lib/foo1.c', 'foo2.c'])

% scons -Q
gcc -c -o lib/foo1.o lib/foo1.c
gcc -c -o src/prog/foo2.o src/prog/foo2.c
gcc -c -o src/prog/main.o src/prog/main.c
gcc -o src/prog/prog src/prog/main.o lib/foo1.o src/prog/foo2.o
```
A naive use of variant_dir results does not produce the expected results: 


```console
% cat ./SConstruct
SConscript('src/prog/SConscript', variant_dir='build')

% scons -Q
gcc -c -o build/foo2.o build/foo2.c
gcc -c -o build/main.o build/main.c
gcc -c -o lib/foo1.o lib/foo1.c
gcc -o build/prog build/main.o lib/foo1.o build/foo2.o
```
Note that foo1.o is still bein built in the library source directory. 

The solution is to use a subsidiary SConscript file in the top level directory and refer to foo1.c relative to the build directory: 


```console
% cat ./SConstruct
SConscript('SConscript', variant_dir='build')

% cat ./SConscript
SConscript('src/prog/SConscript')

% cat src/prog/SConscript
env = Environment()
env.Program('prog', ['main.c', '#build/lib/foo1.c', 'foo2.c'])

% scons -Q
gcc -c -o build/lib/foo1.o build/lib/foo1.c
gcc -c -o build/src/prog/foo2.o build/src/prog/foo2.c
gcc -c -o build/src/prog/main.o build/src/prog/main.c
gcc -o build/src/prog/prog build/src/prog/main.o build/lib/foo1.o build/src/prog/foo2.o
```

## VariantDir() and absolute paths

Files referenced by an absolute path ignore `VariantDir()` entirely and are always built in their source directories. 


```console
% cat src/prog/SConscript
env = Environment()
env.Program('prog', ['main.c', '/usr/src/lib/foo1.c', 'foo2.c'])

% scons -Q
gcc -c -o /usr/src/lib/foo1.o /usr/src/lib/foo1.c
gcc -c -o build/main.o build/main.c
gcc -c -o lib/foo1.o lib/foo1.c
gcc -o build/prog build/main.o /usr/src/lib/foo1.o build/foo2.o
```
The solution is to use a relative directory by adding a symlink and then refering to the file via that link: 


```console
% ln -s /usr/src/lib lib2

% cat src/prog/SConscript
env = Environment()
env.Program('prog', ['main.c', '#build/lib2/foo1.c', 'foo2.c'])
```
Comment from Matt Doar: I think you may want to note that the ln command is issued while in the build directory 


## Hierarchies

(This section from Matt Doar) 

One of the things that people are used to with `make` and other languages is the idea of including files. The `SConscript` function and related `VariantDir` function correspond to this in some ways, but not in others. For instance, I often use: 


```python
env = Environment()
Export('env')

VariantDir = 'build'

# The directory structure of the project
dirs = ['son/grandson',
        'son/granddaughter',
        'daughter/grandson',
       ]

for dir in dirs:
    SConscript(
        dir + os.sep + 'SConscript',
        variant_dir = VariantDir + os.sep + dir,
        duplicate = 0
        )
```
Then in each SConscript: 
```python
Import('env')
Program('foo', 'foo.c')
```
At first glance, this looks like a series of includes in a makefile. But it is subtly different. Now I understand (many thanks) from earlier comments that `foo.c` in each subdirectory is actually viewed relative to the variant_dir that the SConscript function was called with, so that the file is first looked for in the build dir, then in its parallel source directory. 

Aside: SCons is not the only tool to use the idea of multiple build directories and have trouble with it being tricky to use. Jam and the concept of grist makes many Jamfiles hard to debug. 


# Mailing-list Question

**This question really belongs in the mailing list.  It makes a valid point about the examples not reflecting how things ought to work, but the mailing list is the place for requests like this.  I moved it to the end so that it doesn't get lost, but marv, whoever you are, you should be discussing this on the mailing list. -JGN** 

[_OK here is my problem._ I am reading in the user guide, in the section entitled "Multiple Construction Environments", that you can create a debug environment and an optimized environment. This, according to the documentation, seems to be the whole point of multiple environments: "The real advantage of construction environments is that you can create as many different construction environments as you need, each tailored to a different way to build some piece of software or other file." 

Well, the problem with the example is that it is completely unlikely given the above statement. In fact, the example does not build the same piece of software in different ways as claimed. It builds _different_ pieces of software in different ways. It builds foo.c in the first environment, and bar.c in the second environment. When you try to build foo.c in both environments, scons says "*** Two environments with different actions for the same target: foo.o" 

The user guide continues by describing this very scenario, but the solution provided is quite unsatisfying. Instead of the simple env.Program('foobar', ['foo.c', 'bar.c']) that made scons seem so attractive, we now have a long list of tedious statements where you have to provide a unique name for each object file, for each configuration. 

My use case here is quite simple: I have around 100 source files in a directory. I want to build a release version and a debug version of those files. I want the .o files placed in release/*.o and debug/*.o, respectively. And, I want to get this done without having to create more than the single SConstruct file (in particular, I don't want to have to work around the problem by breaking stuff out into as SConscript file -- one make file should be enough). [VariantDir](VariantDir) seems like it might solve the problem. The user documentation says "Use the [VariantDir](VariantDir) function to establish that target files should be built in a separate directory from the source files", which is exactly what I want. The variant_dir argument _also_ seems like was meant to solve my problem, but I have discarded that since it doesn't allow me to stay within a single SConstruct file, and it also does not allow me to keep the source files together with the SConstruct file. I have been experimenting for about an hour and have found no simple solution to this. - marv] 

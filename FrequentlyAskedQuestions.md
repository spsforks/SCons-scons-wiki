**This FAQ contains information about the SCons software construction tool.**

*The most frequently-asked frequently asked questions*

1. [Why doesn't SCons find my compiler/linker/etc.? I can execute it just fine from the command line.][1]
1. [How do I install files? The Install() method doesn't do anything. In general, how do I build anything outside my current directory?][2]

**Table of Contents**

[TOC]

# General Information

## What is SCons?

SCons is a software construction tool—that is, a superior alternative to the classic "Make" build tool that we all know and love. 

SCons is implemented as a Python script and set of modules, and SCons "configuration files" are actually executed as Python scripts. This gives SCons many powerful capabilities not found in other software build tools. 


## Where do I get SCons?

The SCons download page is [http://scons.org/download.php](http://scons.org/download.php) 

If you're interested in the [b]leading edge, you can take a look at what the developers are up to in the latest code checked in to the Mercurial (hg) tree. You can browse the tree on-line at [https://bitbucket.org/scons/scons](https://bitbucket.org/scons/scons) or follow the instructions on that page to download the sources to your own machine.  The default branch is the primary development branch. 


## What's the difference between the scons, scons-local, and scons-src packages?

We make SCons available in three distinct packages, for different purposes. 

The `scons` package is the basic one for installing SCons on your system and using it or experimenting with it. You don't need any other package if you just want to try out SCons. 

The `scons-local` package is one that you can execute standalone, out of a local directory. It's intended to be dropped in to and shipped with packages of other software that want to build with SCons, but which don't want to have to require that their users install SCons. 

The `scons-src` package is the complete source tree, including everything we use to package SCons and all of the regression tests. You might want this one if you had concerns about whether SCons was working correctly on your operating system and wanted to run the regression tests. 


## What version of Python do I need?

SCons is written to work with any Python version >= 2.4 and < 3.0. Versions 3.0 and above are not supported at this time. Extensive tests are used to ensure that SCons works on all supported versions. 

In order to install SCons from a source distribution, the Python Distutils package is required. Distutils is part of Python version 1.6 and higher. For Python 2.4, you can obtain the Distutils package from [http://python.org/sigs/distutils-sig/](http://python.org/sigs/distutils-sig/) 


## Do I need to know how to program in Python to use SCons?

No, you can use SCons very successfully even if you don't know how to program in Python. 

With SCons, you use Python functions to tell a central build engine about your input and output files. You can look at these simply as different commands that you use to specify what software (or other files) you want built. SCons takes care of the rest, including figuring out most of your dependencies. 

Of course, if you do know Python, you can use its scripting capabilities to do more sophisticated things in your build: construct lists of files, manipulate file names dynamically, handle flow control (loops and conditionals) in your build process, etc. 


## Why is SCons written for Python version 2.4?

Python 2.4 is still in widespread use on many systems, and was the version shipped by Red Hat as late as Red Hat 7.3. By writing the internal code so that it works on these systems, we're making it as easy as possible for more sites to install and work with SCons on as wide a variety of systems as possible. 

"Why don't people just upgrade their Python version?" you may ask. Yes, Python's packaging and installation make it easy for people to upgrade versions, but that's not the only barrier. 

In commercial development environments, any new operating system or language version must usually be accompanied by extensive tests to make sure that the upgrade hasn't introduced subtle problems or regressions into the code being produced. Consequently, upgrading is an expensive proposition that many sites can't undertake just because a new tool like SCons might require it. When faced with that sort of choice, it's much less risky and expensive for them to just walk away from trying the new tool. 


## Am I restricted to using Python 2.4 code in my SConscript files?

You can use any syntax supported by the version of python you are using to run SCons. SCons can be run with Python versions >= 2.4 and < 3.0. Versions 3.0 and above are not supported at this time. 


## Are there any SCons mailing lists or newsgroups? Are they archived anywhere?

There are several SCons mailing lists, and they are archived. Information about the lists and archives is available at [http://scons.org/lists.php](http://scons.org/lists.php) . 

There is no SCons newsgroup, but we also have an IRC channel at [FreeNode](FreeNode) ( [irc://irc.freenode.net/#scons](irc://irc.freenode.net/#scons) ). For a complete overview of how to best contact us, visit [http://scons.org/contact.php](http://scons.org/contact.php) . 


## Is SCons released under an Open Source license?

Yes. SCons is distributed under the MIT license, an approved Open Source license. This means you can use it, modify it, or even redistribute it without charge, so long as you maintain the license. 


## Can I help with SCons development?

Definitely. We're looking for any help possible: 

* Python programmers 
* documentation writers 
* web designers and/or administrators 
* testers (especially if you use a non-usual operating system or tool chain) 
If you have time and/or resources to contribute, contact scons-dev AT scons DOT org, the SCons developers and tell us what you're interested in doing. You may also want to check out [http://scons.org/wiki/HowToContribute](http://scons.org/wiki/HowToContribute) , for some ideas about how you can help us. 


# SCons Questions

<a name="shell_env"></a> 
[1]:
## Why doesn't SCons find my compiler/linker/etc.? I can execute it just fine from the command line.

A common problem for new users is that SCons can't seem to find a compiler, linker, or other utility that they can run just fine from the command line. This is almost always because, by default, SCons does not use the same PATH environment variable that you use from the command line, so it can't find a program that has been installed in a "non-standard" location unless you tell it how. Here is the explanation from the SCons man page: 

> SCons does not automatically propagate the external environment used to execute '`scons`' to the commands used to build target files. This is so that builds will be guaranteed repeatable regardless of the environment variables set at the time scons is invoked. This also means that if the compiler or other commands that you want to use to build your target files are not in standard system locations, SCons will not find them unless you explicitly set the PATH to include those locations. 
Fortunately, it's easy to propagate the PATH value from your external environment by initializing the ENV construction variable as follows: 

                     * `import os`  
 `env = Environment(ENV = {'PATH' : os.environ['PATH']})` 
Alternatively, you might want to propagate your entire external environment to the build commands as follows: 

                     * `import os`  
 `env = Environment(ENV = os.environ)` 
Of course, by propagating external environment variables into your build, you're running the risk that a change in the external environment will affect the build, possibly in unintended ways. The way to guarantee that the build is repeatable is to explicitly initialize the PATH 

                     * `path = ['/bin', '/usr/bin', '/path/to/other/compiler/bin']`  
 `env = Environment(ENV = {'PATH' : path})` 

### How do I get SCons to find my #include files?

If your program has #include files in various directories, SCons must somehow be told in which directories it should look for the #include files. You do this by setting the CPPPATH variable to the list of directories that contain .h files that you want to search for: 

                           * `env = Environment(CPPPATH='inc')`  
 `env.Program('foo', 'foo.c')` 
SCons will add to the compilation command line(s) the right -I options, or whatever similar options are appropriate for the C or C++ compiler you're using. This makes your SCons-based build configuration portable. 

Note specifically that you should not set the include directories directly in the CCFLAGS variable, as you might initially expect: 

                           * `env = Environment(CCFLAGS='-Iinc')    # THIS IS INCORRECT!`  
 `env.Program('foo', 'foo.c')` 
This will make the program compile correctly, but SCons will not find the dependencies in the "inc" subdirectory and the program will not be rebuilt if any of those #include files change. 

<a name="build_outside"></a>

[2]:
## How do I install files? The Install() method doesn't do anything. In general, how do I build anything outside my current directory?

By default, SCons only builds what you tell it to, and anything that these files depend on (no matter where they live). If you don't specify differently, SCons builds "." (_i.e._, all the targets in and under the current directory). If you want SCons to build/install targets outside the current directory, you have to tell it to do so somehow. There are four ways you might do this: 

1. Specify the full path name of the external target(s) on the command line.  This will build the the target(s) and anything they need. 
                     * `% scons /full/path/to/target` 
1. Specify a directory on the command line that is above the target(s) to be built.  One example of this is to specify the root directory, which tells SCons to build everything it knows about. 
                     * `% scons /` 
1. Use [Default()](SConsMethods/Default). Any argument you pass to Default() will be built when the user just runs "scons" without explicitly specifying any targets to build. So, you'd say something like: 
                     * `Default(env.Install(directory='my_install_dir', source='foo'))` 
1. Use [Alias()](SConsMethods/Alias). Alias allows you to attach a "pseudo target" to one or more files. Say you want a user to type "scons install" in order to install all your targets, just like a user might type "`make install`" for traditional make. Here is how you do that: 
                     * `Alias("install", env.Install(dir="install_dir", source="foo"))` 
Note that you can call Alias() with a target of "install" as many times as you want with different source files, and SCons will build all of them when the user types "`scons install`". 

[Charles Crain, 14 August 2003, updated by Greg Noel, 1 December 2008] 


## Why is my directory only updated the first time?

Like every other build system, SCons considers a directory used as a target as up-to-date if it exists.  The first time you built, the directory wasn't there, so SCons ran the update command.  Each time after that, the directory already existed, so SCons considered it up-to-date. 

As a workaround, make the dependency on some file within the directory that's always updated: 

                     * `env.Command('html_dir/index.html', Glob('rst/*.rst'),`  
 `            'rst2html -o $TARGET.dir $SOURCES')` 
If there isn't such a file, create one and put something in it that changes every time you build (such as the date): 

                     * `env.Command('html_dir/last_updated', Glob('rst/*.rst'),`  
 `            ['rst2html -o $TARGET.dir $SOURCES',`  
 `             'date >$TARGET'])`  
 

## I'm already using ldconfig, pkg-config, gtk-config, etc. Do I have to rewrite their logic to use SCons?

SCons provides explicit support for getting information from programs like ldconfig and pkg-config. The relevant method is `ParseConfig()`, which executes a `*-config` command, parses the returned flags, and puts them in the environment through which the [ParseConfig](ParseConfig)() method is called: 

                     * `env.ParseConfig('pkg-config --cflags --libs libxml')` 
If you need to provide some special-purpose processing, you can supply a function to process the flags and apply them to the environment in any way you want. 


## Linking on Windows gives me an error: LINK: fatal error LNK1104: cannot open file 'TEMPFILE'. How do I fix this?

The Microsoft linker requires that the environment variable TMP is set. I do the following in my SConstruct file. 

                     * `env['ENV']['TMP'] = os.environ['TMP']` 
There are potential pitfalls for copying user environment variables into the build environment, but that is well documented. If you don't want to import from your external environment, set it to some directory explicitly. 

[Rich Hoesly, 18 November 2003] 


## How do I prevent commands from being executed in parallel?

Use the [SideEffect() method](SConsMethods/SideEffect) and specify the same dummy file for each target that shouldn't be built in parallel.  Even if the file doesn't exist, SCons will prevent the simultaneous execution of commands that affect the dummy file.  See the linked method page for examples. 


# Compatibility with make


## Is SCons compatible with make?

No. The SCons input files are Python scripts, with function calls to specify what you want built, 


## Is there a Makefile-to-SCons or SCons-to-Makefile converter?

There are no current plans for a converter. The SCons architecture, however, leaves open the future possibility of wrapping a Makefile interpreter around the SCons internal build engine, to provide an alternate Make-like interface. Contact the SCons developers if this is something you're interested in helping build. 

Note that a proof-of-concept for parsing Makefiles in a scripting language exists in the Perl-based implementation for Gary Holt's Make++ tool, which has its home page at [http://makepp.sourceforge.net/](http://makepp.sourceforge.net/) 


## Does SCons support building in parallel, like make's -j option?

Yes, SCons is designed from the ground up to support a `-j` option for parallel builds. 


## Does SCons support something like VPATH in make?

Yes. SCons supports a [Repository() method](SConsMethod/Repository) and a `-Y` command-line option that provide very similar functionality to VPATH, although without some inconsistencies that make VPATH somewhat difficult to use. These features are directly modeled on (read: stolen from) the corresponding features in the Cons tool. 


# SCons History and Background


## Who wrote SCons?

SCons was written by Steven Knight and the original band of developers: Chad Austin, Charles Crain, Steve Leblanc, and Anthony Roach. 


## Is SCons the same as Cons?

No, SCons and Cons are not the same program, although their architectures are very closely related. The most obvious difference is that SCons is implemented in Python and uses Python scripts as its configuration files, while Cons is implemented in Perl and uses Perl scripts. 

SCons is essentially a re-design of the Cons architecture (by one of the principal Cons implementors) to take advantage of Python's ease of use, and to add a number of improvements and enhancements to the architecture based on several years of experience working with Cons. 

Information about the classic Cons tool is available at [http://dsmit.com/cons/](http://dsmit.com/cons/) 


## So what can SCons do that Cons can't?

Although SCons was not started to be the anti-Cons, there are a number of features designed into SCons that are not present in the Cons architecture: 

SCons is easier to extend for new file types. In Cons, these methods are hard-coded inside the script, and to create a new Builder or Scanner, you need to write some Perl for an undocumented internal interface. In SCons, there are factory methods that you call to create new Builders and Scanners. 

SCons is more modular. Cons is pretty monolithic. SCons is designed from the ground up in separate modules that can be imported or not depending on your needs. 

The SCons build engine (dependency management) is separate from the wrapper "scons" script. Consequently, you can use the build engine in any other piece of Python software. For example, you could even theoretically wrap it in another interface that would read up Makefiles (a la Gary Holt's make++ Perl script). 

SCons dependencies can be between arbitrary objects, not just files. Dependencies are actually managed in an abstract "Node" base class, and specific subclasses (can) exist for files, database fields, lines within a file, etc. So you will be able to use SCons to update a file because a certain web page changed, or a value changed in a database, for example. 

SCons has good parallel build (-j) support. Cons' recursive dependency descent makes it difficult to restructure for good parallel build support. SCons was designed from the ground up with a multithreaded tasking engine (courtesy Anthony Roach) that will keep N jobs going simultaneously, modulo waiting for dependent files to finish building. 


## Should I use Cons or SCons for my project?

Well, this is the SCons FAQ, so of course we'll recommend that you use SCons. That having been said... 

Unfortunately, Cons classic is essentially a dead project at this point. The last release many years ago (May 2001) and no one is actively working on it. This is really too bad, because Cons is still a very useful tool, and could continue to help people solve build problems if it got some more development. 

In contrast, SCons has a thriving development and user community, and we're releasing new functionality and fixes approximately once a month. SCons also has a virtual superset of Cons classic functionality, the only things really missing are some minor debugging capabilities that don't affect basic software builds. 

So at this point, probably the only reason to prefer Cons over SCons is if you're a die-hard Perl fan who really can't stomach using Python for your software build configuration scripts, and the functionality you need from Cons works well enough that you don't need new features or bug fixes, or you can get by with fixing your own bugs. If that's your situation and Cons is a better fit for you, then more power to you. Maybe you could even help get Cons kick-started again... 


## Is SCons the same as the ScCons design from the Software Carpentry competition?

Yes. Same design, same developer, same goals, essentially the same tool. 

SCons, however, is an independent project, and no longer directly associated with Software Carpentry. Hence, we dropped the middle 'c' to differentiate it slightly, and to make it a tiny bit easier to type. 

Even though SCons is being developed independently, the goal is for SCons to be a flexible enough tool that it would fit in with any future tools that the Software Carpentry project may produce. 

Note that, at last report, the Software Carpentry project renamed their tools with the prefix "qm"--the build tool being "qmbuild"--so there shouldn't be any confusion between SCons and any independent build tool that Software Carpentry may eventually produce. 

Although the information about the original Software Carpentry competition doesn't seem to be available any more, the project lives on as a source of teaching materials to teach software development skills. See [http://en.wikipedia.org/wiki/Software_Carpentry](http://en.wikipedia.org/wiki/Software_Carpentry) for details and further links. 


# Administrivia


## Current Version of This FAQ

The most recent and up-to-date version of this FAQ may always be found at [http://scons.org/wiki/FrequentlyAskedQuestions](http://scons.org/wiki/FrequentlyAskedQuestions) 

Please check to make sure your question hasn't already been answered in the latest version before submitting a new question (or an addition or correction to this FAQ). 


## Copyright

The original of this document is copyright 2001 by Steven Knight (knight at baldmt com). 

This document may be freely copied, redistributed, or modified for any purpose and without fee, provided that this copyright notice is not removed or altered. 

Individual items from this document may be excerpted and redistributed without inclusion of the copyright notice. 

If you incorporate this FAQ in any commercial, salable, or for-profit collection or product, please be courteous and send a copy to the copyright holder. 


## Feedback

Any and all feedback on this FAQ is welcome: corrections to existing answers, suggested new questions, typographical errors, better organization of questions, etc. Contact the scons-users AT scons DOT org, the user mailing list. 

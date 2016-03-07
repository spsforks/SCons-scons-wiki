_Note: this page may contain flammable opinions. This is a wiki, many have contributed to it. Please be considerate and balanced._ 

**Table of Contents**

[TOC]

# SCons

Pros: 

* Based on a full-fledged programming language, Python. This means you can make the build system do pretty much anything you can figure out how to program, if it doesn't do it already. This also means it doesn't reinvent the wheel, and uses a tried-and-proven syntax. 
* Support for many platforms, compilers, and targets built-in. 
* Has auto-configuration abilities. 
* Can be distributed with the software product, so users do not need to install it. This reduces the dependencies your users need to python, which almost everyone already has (or can easily get) 
* No need for intermediate steps like generating a makefile and then using a makefile; likewise, no need for many tools like automake, autoconf, autoreconf, make, ... scons is all-in-one, self-contained, usable with a single call, making it easier for users 

Cons: 

* Based on a general-purpose programming language, Python. This means writing even a basic build file requires you to know a bit about Python and its syntax. 
* If you want to do more complicated builds, you will quickly find yourself having to write a fair amount of Python code to achieve the functionality built into other build systems. 
* A bit low-level; even some quite common tasks require writing more code than you'd expect 
* Requires users (developers) to have a full Python installation and then to install the SCons scripts on top of that (though python is arguably very largely installed, and scons-local can be included inside your program's source code to remove the dependency on scons) 
* Very centric on the idea of having a build dir. Great pains to avoid this. 
* Can get slow on big projects 

# make

This is the standard against which all other build systems are currently compared. Make is at its core a dependency checker that can execute shell commands based on one file being older than another. Implementations of Make exist on almost every software platform, although by far the most widespread would be GNU Make. 

Most Make implementations include a set of 'default make rules' which allow very simple building of C, C++, FORTRAN, lex and yacc projects. Additionally make rules can be specified for other languages, but these tend to need to be customized from platform to platform. 

Make doesn't include dependency checking by default, although there are make rules that can do this for you fairly easily in the case of GNU Make. 

GNU Make's support for shell scripts under GNU/Linux means that GNU Makefiles can be very powerful, but use of advanced GNU Make features will usually render your makefile incompatible with other Make implementations. 


# GNU Autotools

GNU Autotools extends GNU Make with a larger library of default build rules, plus extensive dependency checking capability. It knows how to compile software (executables, shared libraries, plus documentation, etc) for a large number of targets, which is something that rapidly becomes tedious when using plain Makefiles. 

GNU Autotools have an intimidating learning curve, however; fairly detailed knowledge is required before they can be easily put to use on an existing codebase. 

GNU Autotools is the defacto standard build system for large linux programs, although other tools such as Scons are making inroads. 

GNU Autotools generate a 'configure' script which can be bundled with your source distribution, so that the person compiling your software doesn't need to have Autotools installed. This script performs requirements checking on the target system then generates Makefiles to compile the software. 


# CMake

[CMake](http://www.cmake.org) is a principal competitor to both GNU Autotools and SCons.  It is a build system _generator_, i.e. after running CMake, the user has a native Visual Studio file at his disposal, or a native Makefile, or nmake file, or whatever their preference is.  Off-the-shelf build capabilties are comprehensive and proven for large scale software development.  The implementation architecture is far more unified than GNU Autotools and it runs much faster.  CMake has its own scripting language that runs on all platforms that CMake targets.  It is Yet Another Scripting Language, which puts some people off, but it has the advantage of not introducing any additional language dependencies to a project. 

When compared to scons, CMake is : 

* Faster 
* Requires less code for common tasks 
* Arguably more stable 
* Supports outputting to projects like Code::Blocks, Xcode, etc. which scons does not 

But : 

* Uses its own language, reinventing the wheel and not providing access to the extensibility and power of a real language. 
* Arguably not as extensible as scons 
* For terminal builds, still requires the use of 'make' (which, depending on your point of view, may or may not be a disadvantage) while scons is self-contained, all-in-one 
To sum up, my very subjective opinion is that scons is a better idea, but CMake has a stronger implementation 


# Makeit

Makeit ([http://www.dscpl.com.au/projects/makeit/](http://www.dscpl.com.au/projects/makeit/)) is a wide-ranging, quick and venerable build system that was part of Graham Dumpleton's OSE. Under the hood it's little more than an aspect-oriented collection of GNU Make modules. App/lib build files are typically tiny - on the order of a half dozen to a dozen lines - and contain nothing more than a few parameter settings. Mainly tilted toward C/C++/Python development, Makeit supports very large multi-platform multi-compiler multi-target and multi-technology-path builds while hiding almost all low-level details from app and maintenance programmers. 


# Jam

Jam is a build tool with its own, primitive, built-in interpreted language. 

There are several variants of Jam out there. 

* First it was created by [folks at Perforce](http://www.perforce.com/jam/jam.html). 
* Then it was updated by [the folks behind FreeType](http://freetype.sourceforge.net/jam/). Also known as FTJam. 
* There is a version maintained by the Boost people, called [Boost Jam](http://www.boost.org/tools/build/v1/build_system.htm). Also known as BJam, it supports language extensions -- such as modules and classes -- that are required to actually put together a build system of any sophistication. See [Boost Build V2](http://boost.org/boost-build2/). 
* Now there is a new version of Jam called [KJam](http://www.oroboro.com/kjam). It's a complete rewrite of Jam with many extensions and improvements to the language. It has a distributed mode where build jobs can be spawned on a load-balanced peer network of build servers. 
Jam is similar to Make in that it is based on dependency triggered execution of commands. It comes with a very small, but extensible, set of functions ("rules") that make "building simple things simple and building complicated things manageable." That's true up to the point that you need to do some very simple things portably. Even the creation of dynamic libraries is not supported by the default ruleset. You can always extend these rules, but eventually you will run into the limits of the Jam language'e expressivity. 

Boost.Build is a system build on the Boost.Jam substrate. Like Make, it is able to deduce a sequence of build steps given just sources and a target type. Unlike Make, it knows about different types of compilers that are common on various systems, and the different steps involved in compiling for Windows vs Unix. This knowledge allows the user to describe what needs to be built in high-level terms, without concern for low-level details such as the compiler's specific flags, the way that the operating system handles dynamic libraries. The goal is to be able to write a single, simple, build description (Jamfile) that is likely to work with any compiler and/or operating system, even ones you can't personally test on. It also has built-in support for variant builds, options (e.g. include paths and threading options) associated with the _usage_ of particular libraries, and the running of test cases (including automatically setting up necessary environment variables such as LD_LIBRARY_PATH). 

The Boost Build V2 system can create multiple variant and/or compiler builds in a single build step (e.g. debug objects and release objects are compiled into separate directories). The learning curve may be steeper if you're used to directly manipulating low-level build details such as compiler flags, but you get much more of a full-featured build system right out of the box. With SCons you could achieve the same results, but you would have to build an extensive system on top of it with several more layers of abstraction. Or you can write much more complicated Sconsfiles, designed to deal with each of several supported compilers and operating systems individually. The Boost.Build team is seriously considering the use of Scons as its low-level build substrate. 

However, the support of multiple variant builds comes with a cost - the user has no control of where the built files get placed (you can supply only a prefix path). You can easily end up with an executable at your_project_dir/bin/msvc-7.1/debug/link-static/threading-single/user-interface-gui (or deeper) even if that is the only variant you are ever going to build. 

Another problem is that the built files depend only on the source files and not on the command to build them (like in scons). That means that when you alter your Jamfile you either have to find and delete the executable by yourself or rebuild the whole target. That is another problem since it does not rebuild only the target you specify but also all depending libraries (aka rebuilding the world) without the option not to. 


# qmake

Qmake is the [build system created by Trolltech](http://doc.trolltech.com/3.0/qmake.html) for their Qt toolkit. 

Pretty similar in concept to Jam. Brief build files and lots of built-in knowledge of specific compilers for building on different platforms. The main motivation, however, seems to be that Trolltech wanted their build system to automatically recognize moc and uic steps. SCons has support for these build types built in as well. 

A big difference between qmake and Jam, however, is that Jam actually builds the sources, whereas qmake is used to generate native makefiles or project files, which the user then uses to do the actual building. 

Qmake's predecessor was called [tmake](http://www.trolltech.com/download/freebies.html). 


# A-A-P

[A-A-P](http://www.a-a-p.org) is another python based build tool, written by Vim's author Bram Moolenar. 


# Ant

Ant uses XML for the format of the build file, and as such tends to be somewhat verbose (in comparison to Makefiles, for example) and a bit tedious to type. As with **make** the 'language' of the build file is declarative rather than procedural. Ant can be readily extended by writing custom 'tasks', which are simple Java classes. 

Ant has the advantage of widespread use. IDEs understand and support Ant scripts (with _at least_ Eclipse and [NetBeans](NetBeans) as examples). Custom tasks are available for quite a number of uses.   If you have a unique need, odds are you can find an existing example you can adapt that is close to what you need. Some available custom tasks are quite sophisticated, and you may not be able to find equivalents for other build tools. 

Ant is written in Java, was aimed at and is most widely used for Java development.   As a consequence Java development is throughly supported - perhaps more so than most or all other build tools. On the other hand, support for use of other languages is a bit more generic. 

Note that the use of the [Script](http://ant.apache.org/manual/OptionalTasks/script.html) task allows Ant build files to embed snippets of other languages. You can readily [install](http://ant.apache.org/manual/install.html) support for Jython, Javascript, JRuby, Netrexx, Groovy, and others. 

Compared to _make_ there are far fewer headaches in creating and maintaining cross-platform build files. If you have ever had to maintain Makefiles for different platforms (Windows and differing versions of Unix) a good share of your effort goes into handling major and minor incompatibilites between platforms. 

Although Ant itself does not come with the ability to compile C/C++ sources, the [Ant-Contrib project](http://ant-contrib.sourceforge.net) has risen to fill this void.  The [cc task](http://ant-contrib.sourceforge.net/cc.html) can "can compile various source languages and produce executables, shared libraries (aka DLL's) and static libraries. Compiler adaptors are currently available for several C/C++ compilers, FORTRAN, MIDL and Windows Resource files." 

[NAnt](http://nant.sourceforge.net) is a version of Ant focused on .NET and C#, rather than Java development. 


# Maven

By 2010, [Apache Maven](http://maven.apache.org/) has become the dominant build tool in the Java world, but it's first versions date back ten years prior. It is a build system as well as a packaging and distribution system built around a set of rather common workflows and best practices. Maven is written in Java and quite JVM centric, and has a huge ecosystem of plugins for each and everything, including development for C++ and Flex. Maven is highly configurable, but in order to reduce configuration, it is advisable to follow _The Maven Way_, which is a _Convention over Configuration_ philosophy; there is an recommended layout of the source tree and a recommended way for doing several things (although many organizations choose this layout whether they are using Maven or not). Arguably, the entrance barrier is high and the learning curve is steep. Like any advanced tool, when not handled with some diligence, it can lead into "configuration hell".  But this is mitigated by the large number of current [books](http://maven.apache.org/articles.html) documenting the use of it, and the support lists generally have very few people asking how to get started these days. 

For use with Maven, each project and each sub module defines a _Project Object Model_ (pom.xml), declaring metadata, required plug-ins and library dependencies. Plugins are attached to a build/lifecycle through the POM, which is then executed. The POM only contains declarative information and conforms to a well-known XML schema, so it can be easily parsed by IDEs and other build tools. POMs thereby form the canonical build description, regardless of the variety of IDEs used by individual developers on a team. These POMs also form the metadata that is uploaded to repositories for sharing built artifacts, and are primarily used at that level for transitive dependency resolution. 

Any procedural aspects of a build are encapsulated in Maven Plugins. **Plugin** is a Java interface with one **execute()** method that takes no parameters or return value. In addition Maven **Archetype**s can create minimal Maven projects of a requested type, and the Plugin Archetype is no different in that it can create a Plugin project with one line on the command line. For specific technologies with divergent build techniques, a Plugin can change the standard workflow to whatever is required. This allows modules with new technologies to be easily built when a Plugin already exists for it. 

Like any build environment with highly granular dependencies, Maven benefits from the availability of a fast network connection for the first build. Any plug-ins and library dependencies will be fetched online and there are mechanisms for publishing automatically back to the Net. These downloaded dependencies are placed automatically in a local repository, and if dependencies are not changed or the dependencies were already downloaded for other projects a user has developed, no downloads or net connection is required. Supporting the repository, Maven has extensive support with robust tools for version and release management. These tools integrate directly with all popular VCS/DVCS system and manage automatic source tree tagging for each release, allowing for complete reproducibility. All of this makes Maven well suited for an industrial setup or for large scale open source library / platform projects. 

Some argue that Maven is too heavyweight and complex for small projects, but outside the paradigm shift from a procedural to a declarative build description, it is really just the same question of whether to have a build system at all. Many people find that they are more comfortable without Makefiles, and for those folks, Maven will be similarly harmful for their needs. On the other hand, Maven has been extensively emulated in one degree or another by projects such as [Buildr](http://buildr.apache.org/), [Gradle](http://gradle.org) and [Ant+Ivy](http://ant.apache.org/ivy/) through their use of the Maven central repository. 

# Gradle

[Gradle](http://www.gradle.org) was originally a [Groovy](http://www.groovy-lang.org) implemented system for building Java and Groovy codes. Crucial buts have been reimplemented in Java, and a build server architecture created for speed of builds. Builds are specified in a Groovy-based build specification language, in this is it analogous to SCons and Python. Gradle is now the default build system for Android projects. Gradle has been extended to create native code builds. Initially this only covers C and C++.

# TWW tools from TWW Inc.

Cross-Platform Application Dvelopment and Management solutions are in need to deal with the computing world we created. 

For one of CPAD solutions please see [http://www.gnustep.org](http://www.gnustep.org). TWW tools is one of CPAM solutions, it use 

XML and Python to glue together the incompatiable operating systems to minimize the cost of maintaining applicatoins on different OS. 

TWW tools match create,package and manage phases of software application management. 

1. Application Creation. 
   * "sb" in sbutils take care of the following process. 
      1. Software unpack a .tar.gz, .zip, .bz2, .cpio packed source. 
      1. Software patching to the source tar ball. 
      1. Software configure to supply configuration setting to GNU's configure in autotool. 
      1. Software build with your choice of compiler. 
      1. Software install into installation 
1. Application Packaging. 
   1. package the installation directory into native PMS(package management system)format. 
   1. Include the init,post/pre install type of scripts. 
1. Application Management. 
   1. Same "pkg-inst" across supported OS platforms to install application. 
   1. pkg-inst handle package dependency. 
   1. Same "pkg-rm" to remove package including removal package dependent if needed. 
For details please see [http://www.thewrittenword.com](http://www.thewrittenword.com) or [http://en.wikibooks.org/wiki/CPAM_with_TWW](http://en.wikibooks.org/wiki/CPAM_with_TWW) 


# Rake

[Rake](http://rake.rubyforge.org) is a Ruby-based build tool. 

Overview: [http://martinfowler.com/articles/rake.html](http://martinfowler.com/articles/rake.html) 

Pros: 

* Clear syntax 
* Ruby integration (RDoc / [RubyGems](RubyGems)) 
* Core functionality is in one file - easily distributed with packages 
Cons: 

* Lacking much of SCons' target-type-specific support 
   * C/C++/Java/TeX/... 
   * gcc/icc/VS.NET/... 
   * and more 

# Makepp

[Makepp](http://makepp.sourceforge.net) is a build system implemented entirely in Perl. Although it is 'backward compatible' with make it allows you to have Perl code and functions in your makefile. As the [Makepp](http://makepp.sourceforge.net) website states: 


```txt
Makepp is a drop-in replacement for GNU make which has a number of features that allow for more reliable builds and simpler build files. It supports almost all of the syntax that GNU make supports, and can be used with makefiles produced by utilities such as automake. It is called makepp (or make++) because it was designed for building C++ programs. Also its relationship to make is supposed to be analogous to C++'s relationship to C: it is almost 100% backward compatible but adds a number of new features. In fact, it will work with input files designed for make, but there are much better ways to do things.  Some features that makepp adds to make are: greatly improved handling of builds that involve multiple makefiles (recursive make is no longer necessary); automatic scanning for include files; rebuilds triggered if build command changes; checksum-based signature methods for reliable builds; extensibility through perl (within your makefile); repositories (automatically importing files from another tree). For a more complete feature list, see the manual http://makepp.sourceforge.net/1.50/.
```
Pros: 

* In the quest for reducing boilerplate and simplifying individual Makefiles in large projects Makepp seems to be one step ahead: It will allow you to completely eliminate individual makefiles if there is a makefile higher up in the directory structure that defines all the necessary rules to build the files in the current directory (with the targets being created in the same directory) 
* Provides functions for the more obscure automatic make variables ($@, $^, $+ etc.) 
* Multiple variant builds are easily possible by having the sources in a repository and building from there in empty directories.  Alternately or additionally the build cache mechanism allows quickly reviving files that have been built identically before. 
Cons: 

* Makefile syntax 

# Waf

[Waf](http://freehackers.org/~tnagy/waf.html) is a build system written in python. It was invented because the KDE project needs a new build system. WAF is technically a fork of an older version of SCons, but it's been rewritten so extensively that, for all practical purposes, it should be considered a separate code base. 

Pros: 

* Much faster than SCons. 
* Configuration is separated from building. 
* A set of diffrent pretty output modes available by default. 
* Pythonic API, compared to SCons use of [CamelCase](CamelCase). 
* Makes use of features provided by newer versions of Python. 

Cons: 

* Not as wide platform and tool support compared to SCons. 
* Small developer team and user base. 
* No proper test suite for regression protection. 
* The API is still changing quite a bit. 
* Not backwards compatible with older versions of Python compared to SCons. 
There's some rough and incomplete documentation in the [WAF wiki](http://code.google.com/p/waf/w/list) and there's also some information in this [PDF file](http://waf.googlecode.com/svn/trunk/doc/waf.pdf). 


# KConfig

[KConfig](https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt) is a build system written in make, which is used to build the Linux kernel, and a number of other low-level tools (buildroot, uclibc, busybox). It has a snazzy configuration GUI, and is quite fast. 


# Other comparisons

[The AAP page](http://www.a-a-p.org/tools_build.html) has a list of various build tools out there. 

[dmoz.org](http://dmoz.org/Computers/Software/Build_Management/) also has a short list of build tools. In particular there is a list of [Make tools](http://dmoz.org/Computers/Software/Build_Management/Make_Tools/). 

[Make alternatives](http://freecode.com/articles/make-alternatives) A few suggestions of alternatives to make.

[Benchmarks of various C++ build tools](http://psycle.svn.sourceforge.net/viewvc/psycle/branches/bohan/wonderbuild/benchmarks/time.xml) Compares the speed of SCons, Waf, Wonderbuild, Jam, Make, the Autotools, CMake, VCBuild ... 

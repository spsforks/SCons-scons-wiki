**Table of Contents**

[TOC]

# Overview

This page arose out of a bug party discussion where it became clear that the core SCons developers didn't have the background or experience to evalutate the importance of Java issues.  The intent of this page is to encourage the Java community to provide that perspective, focusing on three elements: what SCons does well, what it does poorly, and what it doesn't do at all.  With that information, the SCons developers can have an idea of what should be kept, what should be improved, and what should be added.  It is hoped that this page will evolve into a consensus between the Java community and the SCons developers, and create an outline of the steps we need to take in the future.

# An Introductory Polemic (originally an email by Russel Winder)

Ant and Maven are the current main players in the Java build world.  Ant is the "swiss army knife" build system, Maven is the "you will do it our way" project management/build system.  Maven is great if your project fits their model.  Both use XML for specification.  For Maven this is mostly fine, again as long as your project fits the model.  For Ant it is a right royal pain in the proverbials.  An obvious evolution came out of the Groovy work (Groovy is a dynamic programming language that runs on the JVM and works symbiotically with Java), replace XML with Groovy as the specification of a build using the Ant tasks.  This is exactly what Gant is, it is a way of scripting the Ant tasks using Groovy.  Gradle was going to build a Maven replacement on top of Gant, but after some experimentation, it was decided (not unreasonably) to start from scratch, so Gant and Gradle are distinct and separate systems. 

People trying Gant as an Ant replacement are very rapidly getting the "use a dynamic programming language to specify your build" message.  Gradle may get this message into the Maven-minded -- though it has the problem of being Ivy rather than Maven based (Ivy is the new kid on the block for dependency management). 

Others have cottoned on to the "dynamic language as build specification language".  Buildr for example is a Maven replacement using Ruby and the Rake engine. 

So the days of XML are now looking numbered, which is good. 

What about SCons?  Well very, very few people in the Java community have ever heard of it.  Ant replaced Make very quickly, then Maven came along and between them they have the entire market.  Buildr has a core following, but it is Ruby -- well JRuby actually and even though there is massive push by Sun to get JRuby and Jython accepted in the community, it is an uphill struggle.  The Groovy team believe (hopefully it is not a delusion) that despite not getting the obvious public backing from Sun that JRuby and Jython have, Groovy is actually winning the dynamic language on the JVM battle.  Gant and Gradle appear to be two of the things (there are a number of others) that are helping Groovy's progress.  The context is though very Ant/Maven/Ivy based. 

Even if SCons could run on Jython, it is not clear that that would give it entry.  Obviously the build system does not need to run on the JVM to support the JVM-oriented world.  The Ruby/Rake/JRuby/Buildr situation is slightly weird as JRuby often runs Ruby code faster than the Ruby interpreter.  It is not certain this will ever be the case for Python/Jython.  The Ruby/JRuby, Python/Jython relationships are very different. 

Back to SCons.  SCons has a wonderful C/C++/Fortran/LaTeX infrastructure (caveat various issues of apparent need to rework the tools architecture).  The Java support is basically minimal.  It is clear that SCons does not currently have the necessary infrastructure to even get to the Java project build framework starting line.  It certainly doesn't have the model-oriented core à la Maven, Gradle, and Buildr, and it doesn't have quite the right infrastructure to challenge Ant or Gant.  Currently though SCons is in the "swiss army knife" camp so you have to look at Ant and Gant as the primary competition.  Which really means is it likely that people would put effort into providing the infrastructure for SCons to challenge Ant.  If it wasn't for Gant, there could be a strong rationale.  The question is can a system with a C/C ++/Fortran/LaTeX background get any traction in an area where Java and Groovy rather than Python (or Ruby, even given JRuby and Jython) are the languages of development. 

For the Java mainstream, it is the time of evolution not revolution in build technology.  I suspect Gant and Gradle fit that evolution, where SCons cannot -- at least not without a backer to fund in some way the creation of the needed infrastructure. 

The one area of real possibility though is the boundary between C/C++ and Java, JNI.  Ant and Maven have truly primitive support for C, C++ (and Fortran and LaTeX) builds.  The  C/C++/Fortran Ant task and the LaTeX Ant task are poor and have no traction.  It is probably the case that most projects that have a JNI component just call out to Make from Ant for the C/C++ build.  This could be an area where SCons could generate a USP would be building mixed C/C++/Java systems.  However,  the market for these is probably small and very specialized so the cost benefit in creating the infrastructure may not be worth it. 

Some people appear to be getting interested in Waf as an Autotools replacement.  There is an interesting parallel in the SCons/Waf relationship to the Ant/Maven one.  Waf has a model of being a direct replacement for Autotools, and it is getting better and better at doing that these days.  Where a project and context fit the Waf model, the build is simple, straightforward and does all that is needed whereas the SCons builds tend to be much more complex and things have to be programmed that arguably should not have to be. 

Issues that keep cropping up in SCons are installation support (this generally requires a lot of programming whereas Waf enforces the Autotools view and has the infrastructure to back it up), and the configuration support is stronger in Waf than SCons.  As an example, there is direct support for intltool in Waf but not in SCons which is a Very Big Deal in the Gnome arena. 

In terms of cost/benefit, I wonder if putting effort into evolving SCons to be the clear and obvious choice for C/C++/Fortran/LaTeX would be better than improving the Java support?  Would ensuring that there is no need for Waf, be a better strategy that trying to take on Ant/Maven/Gant/Gradle? 


# Follow up thoughts

SCons needs the ability to handle dependencies on jars in the Maven and Ivy repositories and to manipulate CLASSPATHS.  cf. the Maven Ant task. 

SCons needs a unit test execution capability.  TestNG, JUnit4, and JUnit3 execution tasks would be needed.  These would need to depend on creating compilation of all the source then the compilation of all the tests, including pulling dependencies from Maven and/or Ivy repositories. 

SCons needs to support construction and installation of War files (see [1704](/scons/scons/issues/1704))

SCons needs to support the handling of Cobertura and other instrumentation systems for handling code coverage. 

SCons needs to have an Ant Task so that continuous integration systems that only support Ant and Maven (which is most of them, CruiseControl, TeamCity, Bamboo) can still be used.  Buildbot just calls a command so SCons is already supported.  Hudson rather  forward lookingly created a Gant capability as well as Ant and Maven and may be amenable to adding SCons (but may have to be Jython based to avoid the need for a Python installation?). 

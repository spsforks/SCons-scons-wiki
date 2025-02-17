

# Some thoughts for a 2010 evolution of the Java Support in SCons

The current support for Java in SCons is fairly simplistic and is rooted in a pre-Groovy, pre-Scala world.  The following are some thoughts designed to start a review and refactoring (or reimplementation) of the JVM-based languages support in SCons. 

Currently the DAG built by SCons is supposed to have knowledge about every single generated file so that the engine can work out which files need transformation.   In a world where there is 1 -> 1 relationship between source file and generated file (as with C, C++, Fortran, etc.) or where there is 1 -> n relationship where the various n files can be named without actually undertaking the compilation, things are fine.  For Java, and even more extremely for languages like Groovy, it is nigh on impossible to discover the names of the n files without running the compiler -- either in reality or in emulation.  This means you have to reason in terms of the 1 -> 1 and not worry about the n-1 files that also get generated.  This works fine for forward transformation, but SCons has an issue that none of the other systems have, it treats cleaning as "unbuild" not as a target "clean".  For this it must know what got built.  However, unless there is a post-processing stage that manipulates the stored DAG after compilation, there is no way this can happen.  The idea of running the actual compiler to gain the information in order to decide whether to run the compiler is clearly not the way forward. 

The only other alternative is to have a special Java/Closure/Scala/JRuby/Jython SideEffect builder which realizes the ideas of the Ant glob "**/*.class".  This is, in effect,  what Maven, and Gradle do -- Ant and Gant require the user to specify explicitly what it means to clean so they use remove tasks explicitly. 

So SCons has to compromise here and allow for not having all build products specified in the DAG.  Relying on only considering the 1 -> 1 transformation of: 

| | | |
| --- | --- | --- |
| X.java | | |
| X.groovy | --> | X.class |
| X.scala | | |

to determine whether to compile seems good enough, the reason being that all the other generated classes will always be regenerated anyway. 

The Big Downside is clearly what happens if someone removes or damages an untracked generated file?  Well in this case the tests fail and the developer will usually do a "rebuild project" which means full clean out.  This may seem strange to C, C++, Fortran, SCons folk, but it ends up being the fastest way of solving things in a number of cases, not just in the one above, but in the case where downloaded dependent jars are out of sync. 

C, C++, Fortran, etc. have the idea of compiling against a library, but it is assumed that the library is either there (in which case transformation proceeds) or it isn't (in which case transformation stops).  The whole Autotools/Waf/SCons philosophy has been based on this.  The Java build structure introduces an extra intermediate step -- if the jar I need isn't already here can I go and get it from the Maven repository (implemented using either Maven, Ivy or something built on them as Gradle does).   This is something SCons should be able to handle in its DAG since this is the way ultimately Maven, Ivy and Gradle do things. 

Given the Object and Program builders, then Classes seems like the builder to cover Java, Groovy and Scala compilation since builder names generally indicate the target not the source.  Then we can have Jar, War, Ear.  These should be OSGi-fy from the outset so the BND tool will be a dependency that SCons will have to carry. 


# Material on this page from 2005 and 2008

* Multi-Step Java Builder patch and build example: [http://scons.tigris.org/issues/show_bug.cgi?id=1162](http://scons.tigris.org/issues/show_bug.cgi?id=1162) by [LeanidNazdrynau](LeanidNazdrynau) 
* This is another [Java-Build-Run-Code](javascript:void(0);/*1216648444670*/). Builds Java files with classpath containing any directory within the project, recursively parses the classpath directory to include all files .class and .jar files, within it. Can compile a single file or complete src directory. Runs, class files, with the same classpath principle. Easy to change and modify, by [BabarAbbas](BabarAbbas). 
This is first implementation of multi-step Java builder. It re-defines next builders: Jar, JavaH, Java, [JavaDir](JavaDir), [JavaFile](JavaFile), where 

* Jar has src_builder=Java 
* JavaH has src_builder=Java 
* Java has src_builder=[JavaFile](JavaFile)  (but I am not using it now) 
* [JavaDir](JavaDir) - build all java in directories (what current Java builder does), I just could not mixed together Java, which takes files as source and [JavaDir](JavaDir), which takes directories as source in one builder declaration. I hope this builder can be combine with Java later on. They do use the same functions in javac.py tool. 
What you can do with it: 

With Multi-step builders you can simply define build Jar file and specify .java. Or you can add swig.py builder to it and use .i as input to Jar builder, like: 

* `Jar(['Sample.i','A.java'])`
In this call swig builder will build .java from .i files and send it to Java builder, which will build .class files and send them to Jar builder, which will generate .jar file all in one call, so your Java can work similar as  C/C++ builds. 

From patch above download java build example: project.zip file. This example tested on Windows with `VariantDir` set and  `duplicate=0`. You have to have JDK and swig in your path. 

Example demostrate: 

* src/HelloApplet - build jar file from directory and pottentially sign it. 

```python
# this is regular Java build for scons
import os

Import("env")
denv = env.Clone()
classes = denv.JavaDir(target="classes", source=["com"])
# set correct path for jar
denv["JARCHDIR"] = os.path.join(denv.Dir(".").get_abspath(), "classes")
denv.Jar("HelloApplet", classes)
```
* src/server - build classes from Java directories and create .war file, which includes built class files, WEB-INF and built [HelloApplet](HelloApplet).jar 

```python
import os

Import("env")
classes = env.JavaDir(target="classes", source=["com"])
env["WARXFILES"] = ["SConscript", ".cvsignore"]
env["WARXDIRS"] = ["CVS"]
env.War(
    "scons", [classes, Dir("../WebContent"), "#/buildout/HelloApplet/HelloApplet.jar"]
)
```
* src/jni - JNI interface. Will build Shared library and Jar file, Will use swig to generate interface Java and C++ files. Deactivate build in this directory if you do not have swig installed. 

```python
Import("env")
denv = env.Clone()
denv.Append(SWIGFLAGS=["-java"])
denv.SharedLibrary("scons", ["JniWrapper.cc", "Sample.i"])
denv["JARCHDIR"] = denv.Dir(".").get_abspath()
denv.Jar(["Sample.i", "A.java"])
```
* src/javah - JNI. Will build shared library and Jar file. Will use JavaH to generate C++ header files. 

```python
Import("env")
denv = env.Clone()
denv["JARCHDIR"] = denv.Dir(".").get_abspath()
denv.Jar("myid", "MyID.java")
denv.JavaH(denv.Dir(".").get_abspath(), "MyID.java")
denv.SharedLibrary("myid", "MyID.cc")
```

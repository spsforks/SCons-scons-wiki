
**Java-Build-Run, classpath made by recursively walking through the directories.** 

The code compiles and runs java files. 

The project attached [project-java-build-run.zip](project-java-build-run.zip) consists of a few directories, src, bin, lib, tools. Three main-code files, SConstruct, run.py, config.py. The functionality of the three files is explained below. 



---

 

* SConstruct contains the build code, to invoke build, 
$ python tools/scons/scons-local-0.98.4/scons.py buildresource=src/somecompany/HiSCons.java 

this will build the HiSCons.java and put the resulting class file in bin/com/somecompany/HiSCons.class. 

The classpath consists of all the files in dirs/subdirs of lib, and files in src. 

Whole src directory is build, if you don't specify buildresource parameter or buildresource=src. 



---

 

* run.py compiles the .java file, by calling SConstruct and then run's it with classpath of lib and bin directories. To invoke run.py 
$ python run.py [--javaargs] src/com/somecompany/HiSCons.java. 

If the class file needs input parameters to run, you can specify --javaargs, and it will prompt you for parameters. 



---

 

* config.py contains configuration code for the project. you can change the configuration code according to your needs. 


---

 

* I looked over the internet for java 1.5 classpath, if I don't have to walk through directories and explicitely mention jars and class files in the lib(just mention lib and it automatically finds all the files), but it was not possible at least to me . Perhaps you can find a way. Java 1.6 allows some support in this regard, but since I was on 1.5 so.. 
The code is self explanatory, and comments are added as and when needed. It's been tested, on ubuntu, should work well on windows, except that at some points the path separator is of posix systems, e.g. src/com/somecompany/HiSCons.java instead of src\com\somecompany\HiSCons.java. 

-- Regards, Babar Abbas, [abbas.babar@gmail.com](mailto:abbas.babar@gmail.com) 

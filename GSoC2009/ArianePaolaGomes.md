

# SCons on Jython

This project introduces the support of SCons on Jython. 


### Contact Information
[[!table header="no" class="mointable" data="""
 Name  |  Ariane Paola Gomes 
 Email  |  [arianepaola@gmail.com](mailto:arianepaola@gmail.com) 
 Timezone  |  UTC -3 
 Place of Residence  |  São Paulo, SP, Brazil 
Contact  | jabber: [arianepaola@gmail.com](mailto:arianepaola@gmail.com)   
IRC: arianepaola on irc.freenode.net #scons 
"""]]


## Abstract


### Overview

This project introduces the support of SCons on Jython. SCons as an important build tool, awakes the interest in the Java community and with a port to Jython will allow it to run under the JVM and attract the Java community to use SCons as default build tool, leading to more SCons users.   
 This project will improve the usability, support and compatibility of SCons on Jython and also make SCons go the first steps on a new Python interpreter. 


### Benefits

SCons as an important Open Source, cross platform build tool will profit in many ways from this project. First of all, a step to a new Python interpreter will solve possible problems inside of SCons and make it more portable to other Python interpreters and offer the possibility to be used on more platforms and different environments.   
 Compared to Python, Java has been deployed for years in environments where Python is going to be used. A port of SCons to Jython will allow the use of SCons on the Java platform, without having to make the major switch to CPython. The new support of a great language, Python, will allow the Java developers to develop really fast build scripts, compared to ant, and highly automatize the work, by using SCons. One of the most interesting goals is that with this project SCons will have the possibility to compete with ant directly on the Java platform, using a Python interpreter written in Java: Jython. All this will be really attractive to the Java community and allow SCons to grow. 


## Detailed Description


### Analysis

The effort of this project is the port of SCons and its dependencies to Jython, which do not run at the moment on Jython.   
 The principal work of this project is to figure out the parts that are not working on Jython or are specific for this Python interpreter, fix them within SCons and/or Jython.   
 Several parts of SCons will not run by default on Jython, because they use parts of the CPython implementation, which are not yet implemented or are buggy within Jython. Jython features now the Python 2.5 library which will make it easier to port SCons. Additional code parts, especially on Jython are the usage of system operations with files and directories, which do not work properly (e.g. chdir, spawn, exec, fork, fcntl, etc.).   
 The goal is to identify those parts, fix them and provide tests for Jython or SCons to track those problems in the future.   
   
 Some of the lacking Jython parts are for example many process execution commands, like exec, spawn and fork. Those are not available in Jython, but can be replaced by using the subprocess module, which is new in Jython 2.5. This will need mostly changes in engine/SCons/Platform and also the creation of a java.py platform specification, that will be based on posix, win32, cygwin and sunos.  
 There is need to check the underlying platform of the JVM, which is possible within Jython and make the changes compatible with the major systems supporting Jython. For example Jython on a POSIX system will behave in a different way than Jython on a Windows system.   
   
 The scripts responsilbe for the build and the runtest scripts will have to be improved to work better on Jython – some of the critical parts is the introduction of usage of subprocess on Jython instead of system calls for process management and also the handling of starting a sub interpreter shell.   
   
 A lot of SCons tests rely on QMTest, which is at the moment not working on Jython. Both QMTest and other SCons tests make use of fcntl, which is not available on Jython. In addition QMTest has a small Python extension (~90 lines), written in C, to add support for saving and restoring the signal mask. This tiny code can be rewritten in Jython or as Java module for Jython.   
   
 The strongest requirement is the support for fcntl, which can be implemented using JNA (Java Native Access, [https://jna.dev.java.net/](https://jna.dev.java.net/)). The Python files would be required to return their real file descriptor via fileno(), which returns at the moment a fake file descriptor because Java does not allow access to the real file descriptor due to a private field in  java.io.[FileDescriptor](FileDescriptor).   
 It would be possible to have access to that field using the Java Reflection API, which will allow to modify the behavior of Jython running in the JVM. The JRuby project, an implementation of the Ruby language in Java, has example code.   
   
 A minor issue is the different usage and need of the "<ins>builtin</ins>" module on Jython in some parts of the SCons code. At the moment "runtest.py -a" returns many failures due to the lack of fcntl, but also some additional failures on Jython, which are:  
 -the Platform() function due to the lack of a Java platform implementation and the proper calls for posix, windows – fails in several tests   
  
 -scons_subst, scons_subst_list due to syntax errors on Jython   
  
 -current_file attribute due to assertion errors on Jython About 95% or more of the tests are not running at the moment (issues explained above).   
   
 The installer will need improvements and checks for the Jython interpreter and to deal with specific Jython installation locations and the proper setting of file permissions, which is failing right now. 


### Backward Compatibility

The great backward compatibility of SCons with older Python versions will not be changed at all and will continue to work properly. The biggest change will be the introduction of a Java platform for SCons (in engine/SCons/Platform), which will itself deal with the real underlying platform (e.g. posix, windows, cygwin, sun os).   
   
 There is need to change some parts of the installer, bootstrap and the runtest script. Those changes will not affect SCons on Python and will be improvements for Jython and can be handled by checking explicitly for the Java platform.   
   
 Jython brings since its 2.5 version better Python compatibility and also support for the Python standard library and the major work will be done on getting SCons working on Jython 2.5. In the future there would be the possibility to see if there is interest for Jython 2.2 support in the community. This may include the shipping of the Python subprocess module with SCons for compatibility reasons.   
   
 Some parts of the new code, like the usage of the subprocess module are of interest for the whole SCons code. There is the possibility to extend and improve the current available implementation of "SCons.Action._subproc" and reuse this code for the java platform implementation. 


### Special Techniques

There will be a different approach for Jython compared to CPython, because of the uniqueness of Jython as a bridge between two languages, namely Java and Python.   
 Python extension modules can be written in 3 different languages: plain Java, plain Python and Jython, compared to CPython in C or Python.   
  
 One of the strangest things is that Jython uses the Java virtual machine as platform, but still will need to check for the real underlying platform and deal with different platforms for SCons platform compatibility.   
  
 The success of the whole project and the progress will be measured a lot with the tests included with SCons, which will identify exactly a malfunction, help to make progress and check all of the corner cases on Jython. 


### References

Many platform specific issues in Jython have already been resolved within JRuby. The JRuby implementation can be use in many cases to treat the platform and system specific issues within Jython and provide a good Java source code references.   
  
 SCons provides a big amount of tests that can be used as an example for writing new tests for Jython.   
  
 SCons already provides an initial implementation of a subprocess wrapper in its code, which can be extended.   
  
 SCons provides many examples on platform differences (e.g. posix, win32, cygwin, sunos) that can be used as a sole base for the Java platform implementation. 


### Plan

The initial goal is to implement a SCons.Platform.java and deal with all corner cases of the real underlying platforms. All the system calls like exec, spawn, fork will be replaced with the counter parts in the subprocess module for Jython.   
  
 There is need to change and improve bootstrap, runtest and also the installer scripts in the beginning to treat Jython specialties.   
  
 It is possible to test this functionality on the different platforms already in the beginning by letting the CPython interpreter run the tests. The subprocess module within Jython is from the Python 2.5 standard library and there will not be any compatibility issues.   
  
 In the longer term, the usage of the subprocess module will be improved by extending "SCons.Action._subproc" and use it as a base for the Java platform implementation.   
  
 The fcntl module will be needed in the first place to be able to run all of the tests on Jython. There will be a short term solution by replacing the usage of fcntl.  
 After the fcntl implementation, it will be possible to rely completely on the Jython interpreter for testing all of the code changes directly by running tests.   
  
 The fcntl implementation can be written in Java by using JNA and also accessing Java internals via the Java Reflection API (see for more details the Analysis section).   
  
 SCons uses QMTest, which also uses fcntl and it will be easy to implement the tiny C extension module in Java for Jython and also run the SCons tests using QMTest. This will introduce Jython support for QMTest.   
 At this stage it will be really easy to run all tests for SCons and start fixing bugs within Jython or SCons for the failing tests and improve much more the Jython compatibility.   
  
 There are some failures in the tests that can be worked on already in the beginning of the project.   
  
 To help testing the Jython support for SCons, there will be a buildbot setup with the configuration information published in the Wiki. The setup can be adopted by the SCons buildbot.   
  
 For helping users to tests the progress of the Jython port, there will be a distribution of SCons published via the Wiki and refered in the mailing list.   
  
 To show progress and also have additional work to do if the Summer of Code will run short, there are additional tasks included in the Secondary tasks section below. During the project, I will contribute with a documentation to the SCons wiki and also introduce and discuss the new functionality to the community and make several calls for testing on the SCons mailing list. 


#### Testing

One of the main goals of the project is to get the tests running properly on Jython. Testing has a high importance in the whole project phase. On the one hand there is SCons based testing and on the other hand the testing by the community. The tests within SCons will ensure the proper work on Jython and the compatibility with other parts of the SCons source code.   
  
 In a continuous development progress the Jython support will be ensured by fixing failing tests one by one, examine this code using different version of CPython and Jython and assure that there are no changes that influence the stability of SCons.   
  
 The community based testing will be used for getting feedback and see the functionality of Jython support for SCons in the wild. There will be several call for testing announcements on the mailing list to ensure a good code quality, but the community will be always able to check out code from a repository and see the cutting edge of code.   
  
 SCons relies for testing on QMTest and unittest. Those tests can be automized and made available online using buildbot. One of the goals of the project is to add QMTest support to Jython and make a buildbot setup for SCons running on Jython. 


#### Documentation

All changes and incompatibilities fixed in the Jython port will be documented in the Wiki for future development. This information could be used for adding additional Python interpreters, e.g. IronPython.   
 The Wiki will include documenation pages about:  
 -incompatabilities fixed in the Jython port   
  
 -the porting progress and changes to SCons   
  
 -how to use SCons on Jython   
  
 -information about the setup of a buildbot for SCons on Jython 


### Secondary Tasks

This tasks can be worked on if the Summer of Code project runs shorts or if some of the above implementations will take longer than expected. The listed tasks are of my interest and will help to improve SCons and also additional progress during this Summer of Code project.   
  
 -Documentation in the Wiki pages (e.g. differences between CPython and Jython when running SCons)   
  
 -Better Windows installation: Create a Windows executable installer using the NSIS installer system ([http://nsis.sourceforge.net](http://nsis.sourceforge.net/)). NSIS is supported on Linux, it is possible to build the installer on Linux and include the scripting process directly in the bootstrap script / the additional SCons scripts.  
  
 The installer will feature multiple side-by-side installations of SCons, adding SCons to the Windows menu and the registry, providing an uninstall option and install Windows style (.chm) help files.   
  
 With NSIS it will be possible to handle many Windows corner cases and support even Windows 95 – Windows 7, handle the user restrictions and additional administrator settings.   
  
 It will be possible to easily bundle the SCons installer with a current Python version and use them together not depending on the current Python install on the system.   
  
 -The Windows installer could also feature providing SCons as an executable archive using py2exe or PyInstaller.   
  
 -Provide a SCons jar for Jython / package SCons and Jython in a jar for usage from Java   
  
 -Adding better Java support to SCons.   
  
   
 There are several Java relate tickets in the tracker. Some of the most important ones are listed below.  
 Those bugs include mainly Java and Windows issues and are of my interest:  
  
 **Java:**   
 5 and 6 as well as 1.5 and 1.6 should be valid Java versions in Java builder - [http://scons.tigris.org/issues/show_bug.cgi?id=2088](http://scons.tigris.org/issues/show_bug.cgi?id=2088)   
 chdir flags renders Java paths incorrect - [http://scons.tigris.org/issues/show_bug.cgi?id=1202](http://scons.tigris.org/issues/show_bug.cgi?id=1202)   
 add Builder for Java WAR files - [http://scons.tigris.org/issues/show_bug.cgi?id=1704](http://scons.tigris.org/issues/show_bug.cgi?id=1704)   
 Find javac and jar using the JAVA_HOME - [http://scons.tigris.org/issues/show_bug.cgi?id=1714](http://scons.tigris.org/issues/show_bug.cgi?id=1714)   
 Java Builder issue wrong class name in dependency tree - [http://scons.tigris.org/issues/show_bug.cgi?id=1766](http://scons.tigris.org/issues/show_bug.cgi?id=1766)   
  
 **Windows:**   
 [win] Add SCons to App Paths - [http://scons.tigris.org/issues/show_bug.cgi?id=1883](http://scons.tigris.org/issues/show_bug.cgi?id=1883)   
 Long command lines & multi-threaded builds on Windows system - [http://scons.tigris.org/issues/show_bug.cgi?id=947](http://scons.tigris.org/issues/show_bug.cgi?id=947)   
 Scons can not compile with MSVC under Cygwin - [http://scons.tigris.org/issues/show_bug.cgi?id=2266](http://scons.tigris.org/issues/show_bug.cgi?id=2266)   
 NSIS has tool configuration for mingw cross-compiler (and "mstoolkit") - [http://scons.tigris.org/issues/show_bug.cgi?id=2283](http://scons.tigris.org/issues/show_bug.cgi?id=2283)   
 Bug when installing a dll using Mingw - [http://scons.tigris.org/issues/show_bug.cgi?id=1116](http://scons.tigris.org/issues/show_bug.cgi?id=1116)   
 win32 installer dies when no write to main python directory - [http://scons.tigris.org/issues/show_bug.cgi?id=1413](http://scons.tigris.org/issues/show_bug.cgi?id=1413)   
 get_native_path() bugged with Cygwin - [http://scons.tigris.org/issues/show_bug.cgi?id=2302](http://scons.tigris.org/issues/show_bug.cgi?id=2302)   
 Installer fails (with registry privileges problem?) - [http://scons.tigris.org/issues/show_bug.cgi?id=1490](http://scons.tigris.org/issues/show_bug.cgi?id=1490) RES builder does not work with Cygwin - [http://scons.tigris.org/issues/show_bug.cgi?id=2077](http://scons.tigris.org/issues/show_bug.cgi?id=2077)   
 SCons fails on Windows when mingw tool is activated twice over env.Tool('mingw') - [http://scons.tigris.org/issues/show_bug.cgi?id=2101](http://scons.tigris.org/issues/show_bug.cgi?id=2101)   
 mingw tool: disable .def file target emitting - [http://scons.tigris.org/issues/show_bug.cgi?id=2296](http://scons.tigris.org/issues/show_bug.cgi?id=2296)   
  
 **Features / Broken:** schema definition, xslt for scons-test XML output - [http://scons.tigris.org/issues/show_bug.cgi?id=914](http://scons.tigris.org/issues/show_bug.cgi?id=914)   
 [ListAction](ListAction) doesn't handle Unicode strings - [http://scons.tigris.org/issues/show_bug.cgi?id=1098](http://scons.tigris.org/issues/show_bug.cgi?id=1098)   
 SCons child processes are hanging immediately after forking - [http://scons.tigris.org/issues/show_bug.cgi?id=2050](http://scons.tigris.org/issues/show_bug.cgi?id=2050)   
 SUN C compiler - [http://scons.tigris.org/issues/show_bug.cgi?id=1468](http://scons.tigris.org/issues/show_bug.cgi?id=1468)   
 Please allow an optional name extension on SConstruct and SConscript files - [http://scons.tigris.org/issues/show_bug.cgi?id=2262](http://scons.tigris.org/issues/show_bug.cgi?id=2262)   
 Compat: importing 'pickle' should select faster version is available - [http://scons.tigris.org/issues/show_bug.cgi?id=2331](http://scons.tigris.org/issues/show_bug.cgi?id=2331)   
 Compat: forward compatibility for 'winreg' module - [http://scons.tigris.org/issues/show_bug.cgi?id=2335](http://scons.tigris.org/issues/show_bug.cgi?id=2335)   
 scons won't run when installed using easy_install - [http://scons.tigris.org/issues/show_bug.cgi?id=2051](http://scons.tigris.org/issues/show_bug.cgi?id=2051)   
 unicode paths break SCons - [http://scons.tigris.org/issues/show_bug.cgi?id=589](http://scons.tigris.org/issues/show_bug.cgi?id=589)   
 scons -h should print new options - [http://scons.tigris.org/issues/show_bug.cgi?id=2356](http://scons.tigris.org/issues/show_bug.cgi?id=2356)   
 Scons install fails partially on Solaris (no tar czf) - [http://scons.tigris.org/issues/show_bug.cgi?id=1351](http://scons.tigris.org/issues/show_bug.cgi?id=1351)   
  
 


## Scope of Work


### Deliverables

-Full Jython support for SCons as a project result -Implementation of Scons.Platform.java with the support for posix, windows, cygwin, sunos   
  
 -Implementation / completion of the subprocess wrapper in SCons.Action._subproc   
  
 -Implementation of all Jython related tests for SCons   
  
 -Documentation in the Wiki: Incompatabilities fixed in the Jython port   
  
 -Documenation in the Wiki: Porting progress and changes to SCons   
  
 -Documenation in the Wiki: How to use SCons on Jython   
  
 -Documenation in the Wiki: Setting up a buildbot for SCons on Jython   
  
 -Documenation in the Wiki: Porting SCons to a new interpreter (as a resource for the future, e.g. [IronPython](IronPython), [PyPy](PyPy))   
  
 -Configuration files of a buildbot with SCons on Jython   
  
 -Implementation of tests for the Java platform   
  
 -Improvements to the installer, bootstrap and runtest   
  
 -Replacement of the system calls for Jython by using the subprocess module (this code can be reused later on, e.g. when SCons will use CPython 2.5 as the default)   
  
 -Workaround / improvements for language specific features, that are not available on Jython (system calls, signal, fcntl, etc.)   
  
 -Implementation of fcntl on Jython   
  
 -Complete integration of Jython support in the SCons code base with all needed tests   
  
 -Replacement of chdir() calls within SCons   
  
 -Successful execution of all tests on Jython and CPython   
  
 -Integration of jar creation in the installer / making SCons, Jython easier to use for Java developer   
  
 -Completion Jython and CPython compatibility without breaking any existing SCons code   
  
 -Work on additional tasks, like creating a Windows installer and improving Java support and fixing bugs, listed in the bug tracker 


### Schedule

Summer of Code consists of 12 weeks, which can be split up in 4 parts, two parts for each first and second half of Summer of Code. Writing weekly status reports and hold IRC meetings with the mentor and the community to verify the progress  and identify possible problems in the plan are really important. 

**Community bonding period, **April 20 - May 23 (5 weeks) 

-Communication with the mentor, mentoring organization and the SCons community 

-discussion of implementation ideas, working out difficulties, e.g. fcntl in Jython implementation 

-get a better knowledge of the SCons code internals and the development process 

-create Wiki / documentation pages and announce them as future resource for the community 

* -use the time for studies, e.g.: Java JNA, Java Reflection API to implement the missing fcntl 
-start with improvements in the code generation / installation, improve the setup scripts and the bootstrap for Jython 

-look at some of the additional tasks, fix bugs in the SCons bug tracker to become more comfortable with the SCons development process 

* **FIRST PART OF SUMMER OF CODE ** 
******Part A:    23 may - 14 June (3 weeks)** 

-implementation of SCons.Platform.java for posix, windows, cygwin, sunos / add tests 

-adding subprocess calls for Jython in several SCons parts / add tests 

-fixing bugs in the tests that are running right now 

-start to work on fcntl support to Jython, find a work around in the beginning to get the tests running 

-work on getting test engine to run without fcntl **** 

**Part B:    14 june - 5 July (3 weeks)   
** 

* -add support for qmtest: includes rewriting a small module in Java, depends on fcntl 
-after fcntl and qmtest are working, create a plan of the failing tests and add priorities for fixing those tests 

-finish tests for Jython specific changes (e.g. SCons.Platform.java) 

-improving installer, add possibility to package SCons in a jar 

-work on the failing tests, add fixes to Jython / SCons, write additional tests, double check with CPython**** 

**Midterm evaluation (6 July - 12th July)** **** 

**SECOND PART OF SUMMER OF CODE** **** 

**Part C: 6 july - 26 july (3 weeks)** 

-getting all outstanding problems resolved in the Jython port 

-run major tests with the community to test Jython compatibility 

* -improving Wiki pages, introducing SCons on Jython usage to the community 
-work on additional tasks, e.g. improving Java support for SCons / fixing Java related bugs 

-getting at least 95% of the tests passing successfully by the end of this time frame **** 

**Part D: 26 july - 16 august (3 weeks)** 

-integrating improvements suggested by the community, bugs found during testing 

-work on the Windows installer 

-work on fixing additional bugs, integrating new features into SCons 

-time window on working on any difficulties that did occur during the Jython port 

– some of the failing tests could be really hard to fix. **** 

**August 10: Suggested 'pencils down' date. Take a week to scrub code, write tests, improve  documentation, etc.  
** 

******Final evaluation (August 17 - August 24)** 

**Beginning of September code submission to Google** 

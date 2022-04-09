

# Add Memory Introspection Facility

The goal of this work is to develop a facility that assists users and developers in reducing memory consumption of software builds. Its usage will be demonstrated by boiling down the memory footprint in real-life scenarios. 


### Contact Information

 Name  |  Ludwig Hähne 
 :--- | ---
 Email  |  wkx gmx li 
 Place of Residence  |  Dresden, Germany 
 Timezone  |  CEST +0200 


## Abstract


### Overview

SCons is a significant contender in the realm of software build systems. A major drawback in practice is SCons' large memory footprint in comparison to classic build tools like Make. As projects grow in size, the build system has to store an increasing amount of bookkeeping information. Empiric studies indicate that the memory demand grows in a linear fashion with the number of nodes in the dependency graph. In the case of SCons the memory footprint for a build of a large project might even exceed the amount of physical memory, resulting in bad build performance. 

Memory profiling mechanisms are made available to identify how the memory is distributed among the different subsystems of SCons. The introspection facility will take advantage of asizeof which can easily be integrated into SCons and adapted to its specific requirements. Based on this information, different ways to reduce the overall memory demand are examined. Where possible, the API definition will be coordinated with other memory profiling efforts in the Python community. 


### Benefits

I hope this contribution will add more transparency to SCons, help to identify and eliminate resource dissipators early in the development process. As memory introspection appears to be one of the blind spots in the Python API, other Python projects could also benefit from the introspection measures, as an exemplification of how to approach memory consumption problems. Furthermore, part of this work might be reused in a standardized Python memory profiling facility. 

With a reduced memory footprint, it would be more feasible to build large software projects with SCons. 


## Detailed Description


### Analysis

I'd first like to illustrate the problem with a figure: 

[[/GSoC2008/LudwigHaehne/benchmark.png]]

This is the result of a scalability test where I compared the applicability of Make and SCons for large projects using synthetically generated projects. 

As can be seen the memory footprint scales almost linearly in all variants but recursive Make. As recursive Make has its own problems with regards to missing dependencies and runtime performance it should not be taken as a reference. However, the big margin between (non-recursive) Make and SCons indicate that there is actually room for improvement. 

To achieve an effective reduction of memory consumption better inspection features are a precondition. There are a small number of tools available (most notably Heapy, PySizer, and asizeof) whose fitness for introspection need to be checked. Ideally, the chosen tool can be bundled with SCons and no additional utility needs to be installed on the user's system. The observable information need to be summarized into a clipped and precise presentation of the problem.  

With this tool at hand it should be possible to identify the relevant parts for optimization attempts. 


### Compatibility

It is intended that the modifications I implement shall be transparent to SCons users. The only exception is to annotate existing debug output with size informations. This will allow to integrate my work into the mainline product without the risk to break backward compatibility. However, if a change leads to a significant reduction of memory consumption but has negative impacts on runtime performance an additional flag would make sense to let the user decide what is more important for the task at hand. 

The instrumentation code is to be used as a debugging facility. Therefore compatibility issues should not arise because the code is only executed in debug mode. I will need to exploit features introduced in more recent versions of Python, so a fallback path for older supported versions will be made available. 

The more invasive approaches which have an impact on resource consumption need to be thoroughly tested on various real-life test scenarios. 


### Techniques

I plan to first prepare, integrate, and document the instrumentation code which will be used to measure the memory usage. Once in place, a suite of synthetic and real-life projects is assembled on which performance and memory tests are run. I will use the therewith gathered information to deduce candidates for optimization. After a change was made in order to reduce memory consumption the test-suite is rerun to quantify the effect and avoid regression problems. Furthermore, changes which trade runtime performance in for memory reduction can be detected this way. 

The Python [weak reference facility](http://docs.python.org/lib/module-weakref.html) can be utilized to track an object's lifetime in an unintrusive way. 


### References

* [Heapy: A Memory Profiler and Debugger for Python](http://guppy-pe.sourceforge.net/heapy-thesis.pdf) 
* [PySizer - a memory profiler for Python](http://pysizer.8325.org/) 
* [Recipe: Size of Python objects by Jean Brouwers](http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/546530) 

### Plan

As a first step, measures to introspect memory usage per object/type are implemented into SCons in order to give developers and users a more detailed picture of the problem. [asizeof](http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/546530) appears to be a solid foundation which can be adapted to our needs and even packaged with SCons. This mechanism enables SCons to collect memory information recursively about the various types of objects. 

* Why _asizeof_? 
Neither Heapy nor PySizer are included in Python and both rely on C extension modules. A framework based on one of the two would require the user to manually install it alongside SCons. Moreover, Heapy does not seem to work on 64 bit platforms. In contrast to the before-mentioned candidates, asizeof is implemented in pure Python. This makes it possible to distribute it with SCons and is believed to be more portable. However, I intend to verify the output of asizeof with PySizer or Heapy. 

Another interesting property which shall be monitored is the lifetime of different types of objects. SCons already has a scheme to log certain types of instances with instrumentation code in the constructors. The end of lifetime can be monitored by installing a callback with the help of the weak reference library. One can get a clue about allocation and deallocation patterns by evaluating the obtained information. A memory monitor facility, in the following referred to as heap monitor, is implemented to sample periodically the allocated memory of a set of tracked objects and its referents. These snapshots can be matched with the output of [Valgrind/Massif](http://valgrind.org/docs/manual/ms-manual.html) to verify the validity of the data. 

A second step is to identify and seal memory leaks. The Python garbage collector has debugging facilities of its own that detect and report reference cycles. The heap monitor is extended to trace back orphaned objects to objects tracked by the monitor. [Heapy](http://guppy-pe.sourceforge.net/#Heapy) provides additional facilities which can be used to track leaked objects more easily. I will document the way external tools like Heapy or [PySizer](http://pysizer.8325.org/) can be used most effectively to identify memory leaks. 

To achieve a substantial reduction the above-mentioned measures will probably not suffice. An even more detailed view of certain classes will be made available. The developer states the type of classes for which detailed per instance information is needed. The monitor logs all referents of these instances.  

With this information, more invasive approaches to cut down the memory footprint become possible. Based on the data gathered in the earlier experiments it will have to be discussed which approach is worth to be investigated further: 

* Can we omit some references that keep objects alive unnecessarily or create reference cycles? 
      * If reference cycles can't be avoided, they can be broken by replacing one or more (strong) references with weak references. 
* Does it make sense to compute derived values on the fly instead of storing it into the object? 
* Can we share redundant information between multiple instances of the same class? 
      * If there's a large amount of redundancy, it may make sense to instate the [Flyweight pattern](http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html#flyweight). 
* Is it possible to store rarely accessed data out-of-core?  
      * To monitor access patterns, class members of interest could be replaced by Python properties with accessor functions tracking the access times. 
An idea which could also help to improve runtime performance is to save the DAG (or parts thereof) to disk and stream it in at successive builds. This is an optional task and would only be dealt with if there is enough time left. Moreover, this would be a rather huge undertaking and would probably just result in a foundation work to be finished later. 


## Scope of Work


### Deliverables

* [01] (./) Check-In tests for basic heap monitor usage (single instance, lifetime tracking, snapshot facility) 
* [02] (./) Wiki page describing basic heap monitor functionality 
* [03] (./) Check-In basic implementation with method stubs 
* [04] (./) Check-In and integrate asizeof 
* [05] (./) Check-In heap monitor (passes all tests) 
* [06] (./) Check-In adapted debug output tests 
* [07] (./) Check-In size-annotated debug output 
* [10] (./) Check-In tests for advanced heap monitor usage (log emitter/analyzer, garbage tracker, background monitoring, detailed log) 
* [11] (./) Wiki page describing advanced heap monitor functionality and external log analyzer API 
* [12] (./) Check-In data serialization functions 
* [13] (./) Check-In log analyzer 
* [14] (./) Check-In reference cycle tracker 
* [15] (./) Check-In background monitoring 
* [16] (./) Check-In detailed per instance logger 
* [17] (./) Passes all tests (#10) 
* [20] (./) Demo application ready to illustrate log analyzer (outputs statistics as HTML, delivered as an external module) 
* [30] (./) Wiki page(s) describing test scenarios and the results of different memory reduction strategies 
         * [Lazy initialization](WikiUsers/LudwigHaehne/LazyInitialization) 
         * [Breaking Reference Cycles](WikiUsers/LudwigHaehne/ReferenceCycles) 
         * [Block-wise MD5 hashing](WikiUsers/LudwigHaehne/ChunkHashing) 
         * [Classes with __slots__](WikiUsers/LudwigHaehne/SlotClasses) 
* [31] (./) Check-In successful memory reduction tweaks (passing all tests) 
         * [[!bug 2179]], [[!bug 2180]], [[!bug 2181]], [[!bug 2178]], [[!bug 2149]], [[!bug 2177]] 
* [40] (./) Wiki page with [low memory footprint SCons usage recommendations](ReduceMemory) 
* [50] (./) Review Tigris issues concerning MD5 signatures [[!bug 1459]], [[!bug 1646]], quantify and commit fix if applicable 
* [51] (./) Review [Memory savings with new style classes](http://scons.tigris.org/servlets/ReadMsg?listName=users&msgNo=11883), quantify and commit fix if applicable 
* [A] [!] _Optional:_ Cache DAG on disk prototype (delivered as a patch) 
* [B] [!] _Optional:_ More elaborate data representation prototype (GUI, delivered as an external module) 
(./) Completed; (!) Work in progress; [!] Won't be implemented 


### Schedule

* 
 timeline | tasks
 --- | ---
 Community bonding period  |  Formalize requirements, assemble test suite for heap monitor 
 26.05. - 31.05.  |  #01, #02 Basic functionality tests and Wiki description 
 02.06. - 07.06.  |  #03, #04 Basic implementation, Integration of asizeof 
 09.06. - 14.06.  |  #05, #06, #07 Heap monitor passes tests, Annotate debug output 
 16.06. - 21.06.  |  #10, #11 Advanced functionality tests and Wiki description 
 23.06. - 28.06.  |  #12, #13 Data serialization and log analyzer  
 30.06. - 05.07.  |  #14, #15 Reference cycle tracker, background monitoring 
 07.07. - 12.07.  |  #16, #17 Per-Instance Logger, passes tests 
 14.07. - 19.07.  |  #20 Log analyzer demo 
 21.07. - 02.08.  |  #30, #31, #50, #51 Memory reduction attempts and documentation 
 04.08. - 09.08.  |  #A or #B Optional task 
 11.08. - 16.08.  |  #40 Document memory reduction recommendation, Review introspection API 
 18.08. - 31.08.  |  Final evaluation 
"""]]


## Constraints

I will be available for the full time. However, I plan to take one week off for vacation. 


## Biography

I study computer science in the final year at the [Technische Universität Dresden](http://tu-dresden.de). My main fields of interest are software development toolchains, operating-, realtime-, and embedded systems. 

I have been working as a software developer for the Fraunhofer society for three years. In the [Institute for Ceramic Technologies and Systems](http://www.ikts.fraunhofer.de) I developed measurement and instrumentation control software and was responsible for the software infrastructure of the Linux measurement stations. Furthermore, I have been working on the open source project [RosAsm](http://www.rosasm.org) for two years. During this time I developed the integrated debugger and submitted a number of patches. Due to RosAsm's very limited scope of application I moved on to different projects.  

The last few months I have been working on a student research project for the operating systems department of my university. The goal is to examine if it is feasible to replace an existing GNU Make based build system with SCons. I learnt a lot about SCons internals and general build system concepts along the way. The empiric results revealed the huge gap between Make and SCons with regards to memory consumption. As SCons performed well in other tests and I took a great fancy toward SCons, I felt tempted to do something about the memory consumption problem. I would very much like to apply my previous experience to your project's continued success. 

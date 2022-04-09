

# Ideas for Google Summer of Code 2006


## Introduction

SCons is a truly unique tool, used by many free software projects and by lots of companies. As such, it is important to give students the opportunity to learn its internal architecture and to let them interact with developers to improve it. 


## Learning Opportunities for Students

Here is a short list of what students can learn by working on SCons: 

* Use cases of building **enterprise-grade** software.  SCons uses a very strong test-driven development methodology to make sure things don't break 
* Learn the **architecture** of a truly unique project and advanced **object-oriented programming** in Python 
* Handle portability rules in practice, encounter **real-world engineering issues** 
* Apply **complexity analysis** techniques to understand the bottlenecks. 
* Apply **data mining techniques** on real sets of data to understand the algorithm parameters. 
* Use **visualization** tools to view data and interpret results. 

## Ideas for Google Summer of Code 2006

The following is a list ideas for [Google's Summer of Code 2006](http://code.google.com/soc/): 


### Better Build Performance

Like other build tools, SCons creates a directed acyclic graph (DAG) identifying the dependencies.  Unlike other build tools, Scon's DAG can be modified based upon decisions made by other nodes.  Moreover, SCons can drive multiple worker processes for building.  As a result, the algorithm (and the corresponding code) for evaluating the DAG is complex and difficult to understand; it is best described as a hybrid topological sort with warts.  And it can perform very poorly; there are cases where the dispatcher is compute-bound and yet workers are starved. 

The intent of  this project is to evaluate algorithms to see if any will perform better.  The deliverable will be a testbed for running algorithms that will report on their performance.  It is expected that at least three algorithms will be implemented for testing: the current algorithm, a new algorithm based upon a dynamic topological sort, and an algorithm using a Linda tuplespace. 

A secondary focus of this task is to implement a way of efficiently saving and restoring DAGs.  We will want to be able to capture DAGs after they have been created by a normal SCons run, then evaluate them in the testbed.  This will give us access to many DAGs for testing, so a scheme that minimizes saved size is preferred (although not at the cost of performance). 

If a better algorithm is identified and there is time left on the project, the algorithm will be transcribed for incorporation into SCons itself. 

The partial list of tasks (the student should suggest a full set): 

* Modifications to SCons to capture a DAG, either after parsing or after building. 
* A test framework that will read in the DAG and run an algorithm under test. 
* A test implementation of the current algorithm. 
* A test implementation of an algorithm using a dynamic topological sort. 
* A test implementation of an algorithm using Linda tuplespaces. 
* A tool to show the relative performance of the algorithms under test. 
* A report giving the results of the tests and suggestions for further improvement. 
[parallel programming, threading in Python, complexity analysis, performance analysis, data visualization] 

Mentor: [GregNoel](GregNoel) 


### Adding Autotools Features

[This scheme](SummerOfCodeIdeas/AutotoolSCons) for adding Autotools functionality to SCons is just the thinnest of outlines, but it shows the pieces that will be needed.  It represents many man-months of labor, but the intent is that this outline is the skeleton where individual organs can be attached. 

To be an organ donor, your project proposal will need a lot more detail than in the outline.  Here's a partial list of what a proposal should contain: 

* What part of the scheme you want to do.  Some pieces are huge; be precise in saying exactly what you want to do. 
* What SCons does currently and what your proposal would add. 
* A discussion of what techniques you plan to use. 
* For pieces with an external interface, your thoughts about what the API will entail.  Be concrete. 
* Some examples to show how it would operate. 
* How you plan to test it.  (Tests are a deliverable.) 
* How you plan to document it.  (Documentation is a deliverable.) 
* A list of tasks.  Most tasks result in a deliverable. 
Mentor: [GregNoel](GregNoel) 


### Add Support for Running Unit Tests from SCons

* Extend the architecture for **unit testing** [advanced object-oriented programming] 
* SCons doesn't support execution of unit tests as nicely as it should 
* SCons has plenty of good underlying infrastructure, though, including the ability to express dependencies on non-file entities like Python values 
* This project would likely involve: 
   * Gathering requirements for an SCons-based unit testing infrastructure, probably by polling the SCons user community 
   * Coming up with a design that encompasses: 
      * Executing unit tests 
      * Storing test results (perhaps) 
      * Other gathered requirements 
   * Evaluating existing technologies for sources of ideas and/or actual integration 
      * [QMTest] is a Python-based testing framework that may fit well here 
   * Implementing the design, including testing, of course 
* Mentors: [StevenKnight](StevenKnight)? 

### Timing and Visualization Infrastructure

* **Implement an infrastructure** for **timing** any arbitrary configuration and study the parameters involved [data mining, complexity analysis, visualization] 
* SCons already has some hooks for capturing timing information (and other metrics): --debug=profile, --debug=memory, etc. 
* Some of these are already used to capture and display ["timing data"](http://www.scons.org/Timings/0.96-timings.html) for SCons development 
* Right now, this is done by some _ad hoc_ scripts, not in an organized fashion 
* Cutting-edge SCons users would like some timing infrastructure productized so that it would be easy to do some or all of the following: 
   * Time their configurations against various revisions from the SCons source tree 
   * Capture timing data 
   * Display graphs 
   * Shrink-wrap their timing configurations 
   * Submit them for possible inclusion in a standard set of timing configurations used during SCons development 
* This project would involve: 
   * Defining the requirements for a productized timing infrastructure, probably including polling the SCons user community for input 
   * Evaluating the current prototypes to see if there's any re-usable technology 
   * Coming up with a proposed design, including consideration of packaging issues (should it be a separate package, or part of base SCons?) 
   * Implementing the design 
   * Getting the code released to the world. 
* Mentor:  [StevenKnight](StevenKnight) 

### Logging Framework

* Develop a **logging framework** in order to **centralize the debugging and logging** features of SCons, similar to [loggers and listeners in Ant](http://ant.apache.org/manual/listeners.html).  This is one area that SCons has been lacking in. 
   * Currently the only way to get results from SCons is to capture standard out and parse it.  This is not very useful, however, as there is no: 
      * distinction which target is being built 
      * whether what's being built is a executable, shared library, etc. 
      * overall result document that provides a summary 
Ideally, there would be multiple ways to output and format results.  This lends itself to a concept similar to the [Python logging module](http://docs.python.org/lib/module-logging.html).  Specifically, there will be a notion of formatters and handlers, interchangeable and joinable like LEGO parts: 

      * handlers 
         * ConsoleHandler: prints to stdout/stderror 
         * FileHandler: prints to a File 
         * DBHandler: sends results to a DB 
      * formatters 
         * SimpleFormatter: just prints out everything 
         * XMLFormatter: print out an XML to some predefined schema 
         * FancyFormatter: simply prints to stdout/stderr, but gives more information such as time, etc. 
The following [UML](http://www.uml.org/) diagram illustrates this relationship: [[/SummerOfCodeIdeas/SCons-loggers_and_handlers.png]]
Using this vocabulary, the current SCons default would be a ConsoleHandler with a SimpleFormatter. The final goal would be to allow SCons to integrate easily with build tools such as: 

      * [CruiseControl](http://cruisecontrol.sourceforge.net/) 
      * [BuildBot](http://buildbot.sourceforge.net/) 
      * [Maven](http://maven.apache.org/) 
[aspect-oriented programming, software architecture][possible mentor: [ThomasNagy](ThomasNagy)] 


### Provide release and packaging functionality

* This idea started life as the question: Can SCons replace distutils? 
* However, there is a need for general release and packaging functionality in SCons 
* In this case, [Python Eggs](http://peak.telecommunity.com/DevCenter/PythonEggs) or bdist_wininst installers of a Python package become one of many possible packagers 
* Other possible packagers could support RPM, DEB, Windows MSI, etc. 
* Possible mentor: [StefanSeefeld](StefanSeefeld) 
* Applicant: [PhilippSchollProposal](PhilippSchollProposal) 

## Links

* [http://code.google.com/soc/](http://code.google.com/soc/) 
* [http://code.google.com/soc/mentorfaq.html](http://code.google.com/soc/mentorfaq.html) 

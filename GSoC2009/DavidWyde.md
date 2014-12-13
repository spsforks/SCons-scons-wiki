

# Improved Java and Batch Builder Support for SCons

I plan to revamp the way SCons builds Java projects, through improvements to batch building.  This will take the form of work on "batch clustering", and the creation of a Java source file "recognizer" to allow .java files to be grouped into batches. 


### Contact Information
[[!table header="no" class="mointable" data="""
 Name  |  David Wyde 
 Email  |  david dot wyde at gmail dot com 
 Timezone  |  UTC-7 
 Place of Residence  |  Mercer Island, Washington, USA 
"""]]


## Abstract


### Overview

I propose to enhance support for batch builders in SCons, with a focus on Java.  The two main components of this project are: 1) general improvements to the batch building infrastructure (in the form of "batch clustering"), and 2) a Java-specific "recognizer" to parse through source files and determine what needs to be rebuilt.  The emphasis would be on clustering support, with Java serving as an initial client. 

As time allowed, I would also work on a variety of smaller tasks.  This would probably include documentation for the Java Builder and fixes for bugs related to my project. 


### Benefits

My proposed project would have a number of benefits for SCons.  First and foremost, batch building allows for improved efficiency of certain builds.  Improved Java support would increase the size of the SCons user base -- something important for any open source project.  More users means greater publicity, and potentially more developers.  Better functionality for the Java Builder would be helpful to people working on mixed-language projects, as well as purely Java ones. 


## Detailed Description


### Analysis

The idea of a batch builder suits Java compilation very well, for two main reasons.  First of all, the Java compiler resolves dependency cycles if the source files in question are passed to it simultaneously.  Additionally, each call to "javac" starts up a separate JVM, and this results in decreased performance.  Compiling all of the needed files at once is therefore important, and there practically isn't a command line length limitation for javac: it's possible to pass in a text file listing each .java file that needs to be compiled.  There is obviously some file I/O overhead for that, so I would have to do some further research on the tradeoff between taking the risk of passing too many command line arguments and incurring the performance cost of writing to a file. 

My attempt at enhancing batch builder support for SCons would be based on the procedure described in Greg Noel's April 15th, 2009, comment to [Bug#1086](http://scons.tigris.org/issues/show_bug.cgi?id=1086).  This describes batch clustering and the "MxN problem": grouping source files so that the related ones can be analyzed and handled together.  Making this process efficient will require a good deal of research on my part, which I would plan to do during the bonding period.  Once I get a working solution on the clustering front, I will work on a Java source file recognizer that determines which .java files need to be recompiled.  The needs of batch building for Java and other languages (e.g., ones that are mentioned in issues blocked by #1086) will lead to a stream of revisions to the initial clustering implementation, so I will continue to revise that throughout the summer. 

I plan to use Python's built-in support for regular expressions as the basis for the Java recognizer.  This recognizer will take the place of SCons' current Java source file parser (found in "src/engine/SCons/Tool/JavaCommon.py").  If the Python "re" module proves insufficient for creating a recognizer, ANTLR is one external project that could be helpful.  It was mentioned to me in a couple of emails on the SCons developer mailing list.  The main issue here seems to be one of speed, but ANTLR might prove useful if I could figure out some performance improvements.  I had initially thought of analyzing .class files or using classes from Java Specification Request (JSR) 199 to help figure out which .java files need to be rebuilt, but these techniques now seem unlikely to be effective. 


### Backward Compatibility

Although I intend on making substantial modifications to the Java Builder, scripts that make use of it would ideally continue to work as before; that is, the backend would be refined, but the frontend would basically stay the same.  My idea is to keep the "Java('classes', 'src')" syntax but only create or modify the .class files that need to be (re)built.  Similarly, passing in a single file would only (re)compile classes that are depended upon; a list of files would be treated the same way. 


### Special Techniques


### References


### Plan

The two main components of my project are batch building enhancements and the Java recognizer.  I'll do research on a number of facets of the project during the Community Bonding Period (see Schedule).  My initial coding will focus on algorithmic work for batch building: batch clustering.  Once I have a way to process batches of source files, I will work on creating a new "recognizer" for Java.  The current Java source file recognizer should be adequate for an initial implementation of batch clustering, but I plan to develop a new one that is designed specifically for batch building.  The Python regular expression module will hopefully be sufficient for this, but I might use something like ANTLR if I need to.   

I plan to round out my project with bug fixes and documentation writing.  I'll start with issues that are blocked by #1086 (currently 1766, 1888, 1923, and 2147).  These issues will help balance my work on batch building because the ones other than 1766 represent the needs of languages besides Java.  One potential topic for documentation I might write is a comparison of SCons' Java Builder with the approaches that other projects use to manage Java builds.   


## Scope of Work


### Deliverables

* Improvements to the batch builder infrastructure 
      * "Batch clustering", as described in a comment to Issue #1086 
      * Work on the MxN problem 
* A Java source file "recognizer" written in Python 
      * Designed to determine which files to compile 
      * This will probably be based on the Python regular expression module 
      * If that doesn't work, I might make use of something like ANTLR 
* Formal tests to ensure the accuracy of batch clustering for Java, and the new recognizer 
      * This will be a large component of my project, spread over the duration of the summer 
* Documentation 
      * A specification of the internal API for batch building 
      * A comparison of SCons' Java Builder with similar projects, e.g., Ant and Maven 
* Assorted bug fixes 
      * Focusing on issues related to batch building: e.g., those blocked by #1086 

### Schedule
[[!table header="no" class="mointable" data="""
 Community Bonding Period  |  I'll start by researching the "MxN problem" and the quirks of the Java compiler that I'll have to work around later.  I'll also be sorting out the internal API for batch builders at this time, on the dev mailing list. 
 Week 1  |  Work on batch clustering support.  Some of the legwork for this will have been done over the bonding period, so I should be able to get started quickly.  
 Week 2  |  More algorithmic work (i.e., on batch clustering) 
 Week 3  |  Deliverable: An initial implementation of batch clustering.  This will continue to be revised to meet the needs of various Builders (starting with Java). 
 Week 4  |  Work on the Java recognizer for batch building: writing code, and tests. 
 Week 5  |  Continuing work from the previous week, and hopefully get the recognizer to work in most standard situations.  I imagine there will be a number of edge cases that cause problems at this point. 
 Week 6  |  Deliverable: Java source file recognizer that determines which classes should be passed to the batch builder.  I'll also write documentation that compares the SCons Java builder with the approaches taken by similar projects. 
 Midterm  |  Writing evaluations.  After this point, I plan to mostly be making minor fixes and improvements. 
 Week 7  |  Writing more tests and documentation for the Java recognizer.  This should be very close to, if not actually, complete. 
 Week 8  |  Deliverable: tests to demonstrate batch building/clustering support for Java.  
 Week 9  |  This week is dedicated to something taking longer than expected. 
 Week 10  |  If everything goes according to plan, I'll spend the bulk of weeks 10-13 working on fixing problems from the Issue Tracker (the ones blocked by #1086).  I might still be cleaning things up from the batch clustering and recognizer components, but that will depend on how the testing goes. 
 Week 11  |  Deliverable: one or more fixes for issues blocked by #1086.  
 Week 12  |  Deliverable: documentation for batch building, and for the Java builder and recognizer. 
 Week 13  |  Final preparations for the end of my project: tying up loose ends, cleaning up code, etc. 
"""]]


## Availability

The past few summers, I've spent a couple of weeks teaching at "chess camps", i.e., 9am-3pm day camps for elementary and middle school students that are centered around playing and learning chess.  I might be doing this again for at most 2-3 weeks spread throughout the summer, but I shouldn't have too many time commitments other than that. 


## Biography

I'm currently a 2nd-year Computer Science student at New College of Florida in Sarasota, Florida, USA.  I'm passionate about open source, which is best demonstrated by my infatuation with Linux (Arch is my distro of choice).  Java is my strongest programming language, but I've recently developed an interest in Python.  I'm taking a class on Python this semester, and I've been reading through other people's source code and playing with PyGTK on the side. 

I'm also currently in a course on compilers that uses "Engineering A Compiler" by Cooper and Torczon as a text, and it definitely provides some context for writing a parser.  During the Fall 2008 semester, I took a class called "Graphs, Networks, and Algorithms" that used the Dieter Jungnickel book with the same title.  We covered several topics that are relevant to SCons, such as complexity (e.g., big-O notation) and basic graph theory. 

I participated in Summer of Code 2008, creating a new API for the Coppermine Photo Gallery project.  I worked mostly in PHP, with some XML.  It was a really great experience, and I learned a number of fundamental things about open source development.  Two such lessons are that peppering a Subversion repository with minor changes to a bunch of different source files, and not having a coherent testing policy, are both ineffective development methodologies.  I would love to get another opportunity to start making an impact on an open source project, and I feel that I now understand what it takes for a very successful Summer of Code. 

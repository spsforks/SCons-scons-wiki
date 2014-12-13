

# Comments Stripping Framework and Python Binary Builder for SCons

Really reliable signature checking system and easier Python applications installation! 


### Contact Information

Mateusz Gruca 

[mati.gruca@gmail.com](mailto:mati.gruca@gmail.com) 

Timezone: UTC+1 


### Current documentation

Read more here: 

* [Comments Stripping Framework](http://www.scons.org/wiki/GSoC2008/MatiGruca/StrippingFramework) 
* [Python Binary Builder](http://www.scons.org/wiki/GSoC2008/MatiGruca/InstallPython) 
* [CheckPython, CheckPythonHeaders, CheckPythonModule functions](http://www.scons.org/wiki/GSoC2008/MatiGruca/CheckPython) 

# Abstract

A build tool ought to be able to check source files for changes in case of rebuild. SCons provides two ways of deciding if a file has changed. More traditional and less reliable way is to use timestamps. And the second is using MD5 signatures (default). 

Unfortunately, MD5 checksum is counted for the whole file, not for this part of file which counts in particular case. For example, adding a comment to a C source code changes the file's checksum. Different checksum obligates SCons to rebuild the source file, even though it is not really needed. 

My project aims to enrich SCons with a framework responsible for stripping out comments (or any content not regarded as significant in particular case) and counting checksums only for significant content. <ins>Benefits</ins>: some CPU cycles and user's time saved; MD5 signatures mechanism more reliable. 

As it may not fill whole summer I would also like to add a Python Binary Builder. When an application is installed in a directory not writable by the users, build tool (namely, SCons) has to compile the files to byte-code and place them in install location along with source files. <ins>Benefits</ins>: simplified installation process for applications written in Python. 


# Detailed Description


## Analysis

The hard part of [''Don't Rebuild if Only "Comments" Differ''](http://www.scons.org/wiki/GSoC2008#head-6f1b3d2cb63813df92fdebf292c38133fed604b5) project is that the concept of comment depends on the target type. For example, C file can be both a source code for compiler and source of documentation for Doxygen or any other documentation generator tool. Thus, SCons has to strip the comments when deciding if the object file is up-to-date, but it has to strip the source code to decide if the Doxygen file is up-to-date. 

The idea is to create a set of functions capable of stripping comments for various languages, and then replacing general get_contents() method (in Node/FS.py:get_csig()) with its replacement accurate for particular task. The question how to do this in an elegant way is a task I would like to accomplish during so-called Community Bonding Period (April 14 - May 26). 

For flexibility reasons I would like to provide some sort of API so that users could provide their own comment-stripping functions. That API depends on the answer for above question and is also a matter of discussion on Dev Mailing List. Nevertheless, I would like to earn a consensus for those matters around May 26 so that I could begin coding at full speed and with clear idea what to do and how to do this. 

Second part of my project is [adding a Python Binary Builder](http://www.scons.org/wiki/GSoC2008#head-f8e29140292789a887ded86180359f070edb69fd). There are [three easy ways to compile Python source code to byte code](http://effbot.org/zone/python-compile.htm), two of them worth mentioning (both available at least since Python 1.5): using py_compile module and using compileall module. Py_compile module explicitly compiles single Python module to bytecode. Compileall module compiles all modules in the given directory tree to byte code. 

According to [Python Tutorial](http://docs.python.org/tut/node8.html): 'When the Python interpreter is invoked with the -O flag, optimized code is generated and stored in .pyo files'. As the documentation says, the optimizer doesn't help much. Still I would like to provide a way for the user to decide which option to use: compile and install .pyc files (default) or compile and install .pyo files. 


## Compatibility

Python Binary Builder won't break anything. Sitution for Comments Stripper is a bit more complicated. I have already thought of a few ways to implement it, but these were not backwards compatible. I will continue to refine the details of the API during the bonding period to make sure it is backwards compatible. 

Learning how to think about backwards compatibility could be one of my greatest experience gains from participating in SCons. 


## Techniques

To adjust myself into SCons development I plan to use Subversion and QMTest applications. Since backwards compatibility is important for SCons, I will install Python 1.5.2 and Python 2.2, and use it along with Python 2.5. As a Python 2.x programmer I may use some language features that are incompatible with Python 1.5.2. To avoid any problems I will work with Python 1.5.2, Python 2.2 and Python 2.5.  Since support for Python 1.5.2 may be dropped in the future I will comment in my code what solution would be used with a Python 2.2+ base. 


## Plan


### I. Comments Stripping Framework

This part of my project to some extent will be invisible to SCons users. Assuming that comments stripping is turned on by default it should just do its background work. The only noticeable part will be an API to provide user-defined comment-stripping functions. Users will also be informed about predefined stripping functions, so that they could make use of those functions when dealing with languages not recognized by SCons. 

Since SCons comes with a strong support for C/C++, Fortran and Java, I feel obligated to provide stripping functions for those languages. I will also provide a generic "strip hashes" function, for this way of commenting is very popular among scripting languages (Python, Perl, Ruby, shell scripts to name a few). My work would be incomplete without extending it with D's nested comments. With the support for C/C++/Java comments implemented before it will be just a small step for me and a significant faciliation for D programmers. 


### II. Python Binary Builder

Python Binary Builder will also "just work". Installing Python script with Install/InstallAs methods (or maybe new [InstallPython](InstallPython) method to make it clear and simple - but it is a matter of further design analysis and acquiring SCons's community consensus) will result in creating pyc or pyo file and then copying both, source and binary, to target directory. Pyc is deafault. Pyo can replace it if appropriate Environment variable was set. 

To make Python Binary Builder work I will create a tool-specific initialization for Python interpreter. The lesson learned while implementing it will give me the knowledge necessary to work with the optional tasks that I determine below to make sure that my summer will be filled with coding until the last day of GSoC. 


### III. Optional tasks

It might happen that I will finish my project before GSoC ends. In this case I would like to fill the rest of time with research on builders for languages such as Perl or Ruby and likely delivering them before final evaluations deadline. 


# Scope of Work


## Deliverables


### I. Comments Stripping Framework

1. Implement tests for stripping functions. 

2. Implement stripping functions. 

3. Implement tests for framework. 

4. Implement framework. 

5. Write documentation for stripping functions and for the API for user-defined functions. 

6. Update documentation for using MD5 signatures. 


### II. Python Binary Builder

1. Implement tests for Tool-specific initialization for Python interpreter. 

2. Implement Tool-specific initialization for the Python interpreter. 

3. Update user documentation for Install/InstallAs Builder and 'Appendix B: Builders' documentation. 


## Project Schedule
[[!table header="no" class="mointable" data="""
**Project Schedule** |||
**Comments Stripping Framework** |||
**Duration**  | **Task**  | **Description** 
April 21 - June 1  | Planning and working out a consensus  | The main question is how to design a framework responsible for replacing get_contents() method with one of the functions appropriate for reading contents of the file in the given context. My role here is to research the sources and propose an idea. I already know that I can count on community's critical eye. 
June 2 - June 8  | Coding tests for stripping functions  | N/A 
June 9 - June 15  | Coding stripping functions  | I will create some predefined functions for the common use cases such as: strip C-like comments (usable for C/C++, Java), strip Fortran comments, strip hash comments (for Python, shells, Perl or Ruby). To make it more complete I will add a function to strip D's nested comments. On the other hand I will also create a set of functions to strip source code and leave comments. 
June 16 - June 22  | Coding tests for framework  | N/A 
June 23 - June 29  | Implementing framework  | N/A 
June 30 - July 7  | Testing and writing documentation  | As implementation of the Comments Stripping Framework may deal with many files of SCons source code I would like to leave some time for testing SCons with my changes applied. The rest of time will be devoted to writing/updating documentation. 
**Mid-term evaluation** |||
July 8 - July 10  | Writing mid-term evaluation  | Comments Stripping Framework will be finished before mid-term evaluation. 
**Python Binary Builder** |||
July 11 - July 15  | Planning and designing  | By the time I get to this task I should already know SCons good enough to propose a resolution to this task that will be acceptable for SCons community without long discussion. 
July 16 - July 22  | Writing tests for Tool-specific initialization for Python interpreter  | N/A 
July 23 - July 29  | Implementing Tool-specific initialization for Python interpreter  | N/A 
July 30 - August 6  | Testing and writing documenatation  | N/A 
"""]]


# Constraints


## I. Availability

June is a month of exams here in Poland. Thus I would like to work 6-7 hours a day five days a week until the end of June. After that period GSoC will be my only obligation so I could work 9-10 hours a day 5 days a week. 


## II. Other proposals

I only apply to SCons. At the beginning I was interested in three projects and I had to share my time between them. Finally I decided to dig into SCons only. I follow the rule: quality is better than quantity. 


# Biography

I study International Relations at Faculty of Social Sciences on the [University of Wroclaw](http://international.uni.wroc.pl/s4f.php), Poland. I have already achieved BA degree, and currently I am working on MA degree. 

I am programming for about three years now. I started learning programming because of curiosity. I wanted to be able to understand and change the software I am using. 

I don't plan to work in IT, but I think that I know enough to stop being a passive Open Source user, and start contributing. GSoC and SCons are a big challenge for me. But I need a challenge to feed my passion with something new. 

I am also keen on sport, especially football (soccer in American English) and basketball, both as a supporter and player. 

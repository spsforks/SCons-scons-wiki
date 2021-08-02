
# Programming with Scons


# Tutorial 1 - An Introduction to SCons


## Introduction

After you've decided what to program, there is a tedious problem common to all software projects: the build system that will track dependencies and compile everything in required order. Build system is essential for software in compiled languages, such as C, C++, Java, D or Fortran, but also useful for building documentation or making distributives. This tutorial describes SCons primarily for C/C++ programming, but things described are rather simple to be interesting for everyone. 

There are several tools available to control a project's build process. One of the first of them is 'make' often used in combination with 'autoconf'. Historically it became de-facto standard for *nix systems. Sadly, autoconf is extremely difficult to master. (For a lengthy discussion on autoconf visit a freshmeat editorial [here](http://freshmeat.net/articles/view/889/).) There were many attempts to create alternative build systems and they even succeeded in some areas (like Ant for Java), but none of them is universally popular. 

There is hope at the end of the rainbow though, and that hope is SCons. SCons is a very well thought out python based replacement to make. It offers similar functionality, but benefits from the power that a scripting language like python can bring. One of the key benefits of SCons is its cross platform abilities, so most of what goes on here will work in Windows even if was tested on Linux system. 

This series of tutorials will cover a wide variety of topics on using SCons. Each tutorial will cover one small area of SCons. I hope to break down the lengthy documentation at scons.org into a readable and informative set of informal tutorials. This tutorial will cover creating a simple C program. 

This series is written very informally - I don't intend this to be a reference manual or anything. It is largely from my own notes that I took while learning SCons, and I'm sure it contains spelling and grammatical errors. Please don't bug me about it. If there are glaring factual mistakes, I would like to hear from you though. 

It is assumed that the reader has a grasp of creating programs in the languages used, and a grasp on basic programming jargon and definitions.  However, no prior knowledge of Python is required. 


## Installing Scons

First you need Python installed. Then the most recent version of SCons can always be found on the Scons.org website ([http://www.scons.org/download.php](http://www.scons.org/download.php)). Windows users can download a Win32 installer. For [RedHat](RedHat) users there is RPM package. In Ubuntu or other Debian based systems it is enough to run `"sudo apt-get install scons"`. If you are running another distribution, simply download the scons-XYZ.tar.gz package. Unpack this package, and change to the directory it creates. At this point, run - "python setup.py install". Your SCons installation should now be ready. You can test it by running "scons --version". If the install has worked, a Copyright notice and version statement should be displayed. 


## The SConstruct Syntax

Every project using SCons must have a SConstruct file. This file directs the operation of the build. The format of the SConstruct file should be familar for Python users. Other uses will be interested in knowing that names are case sensitive, comments can be started with a pound(#) and continue until the end of the line. Also, indentation matters in the SConstruct and should only be used under specific circumstances which we will discuss later. 


### Comments

Comments in the SConstruct file begin with a pound('`#`') and last to the end of the line. Comments may be placed on the same line as SConstruct commands, but still last to the end of the line. 


### Data

SCons(or Python) follows a syntax similar to C for that of Data. Strings are contained in either double quotation marks(`""`) or single quotation marks(`''`): `'hello nurse'`, `"Helloooooo Nurse"`. In strings there are also escape characters which can be used to express other characters.  Escape characters, as in C, as preceded by a backslash(`'\'`) and followed by the escaped character.   Basic characters are the newline(`'\n'`), quotation(`'\"'`), or the tab(`'\t'`). Integers are simply written out as they would appear: `0`, `1`, `2`, `3`. 


### Lists

Now that the environment is created, we will take a little sideroad and talk about lists in Sconstruct files. Many of the operations that are used in SCons require the use of lists. A list is encapsulated with brackets('`[]`'). Each list item is followed by a comma, inside these brackets. For example, this would be a list of numbers: `[4, 2, 1, 4]`. Most of the time though, we will be using lists of strings: `["abraham.c", "compiler.c", "helpme.cpp"]` 


### Variables

As Scons uses Python, the full abilities of the Python programming language are at your disposal. This includes variables. To create a variable assemply assign data to it. Variables are assigned use the ('`=`') operator. For example... 

`myFirstSconsVariable = "Hello World"` 

...creates the variable `myFirstSconsVariable`, and assigns `"Hello World"` to it. 


### More Advanced Features

There are other things that Scons files may contain within them, but these will be considered in future tutorials. 


## Building a Simple Program


### The Environment

In order to interact with SCons, the first thing done in an SConstruct file is to create an Environment. Environments contain various information about the system including C compiler flags, linker flags, and so on. We initialize the Environment with a single line: 

`env = Environment()  # Initialize the environment` 

Again, recall that the SConstruct file is white space sensitive. This should appear starting in the first column of text. 


### Creating a Program

The environment is not a simple variable.  It is an object with various methods or subroutines of it's own.  The methods and subroutines allow the creation of programs whether they are in Java, C++, or C.  Today we will create a simple C program.  A basic tutorial for compiling FORTRAN programs can be found [here](llarsen/FortranTutorial). Once the environment is created, the C program creation is simple: 

`env.Program(target = 'helloworld', source = ["helloworld.c"])` 

Here we introduce several new concepts.  First, the target.  A target in SCons is similar to targets in make.  The target is the logical result of the operation.  Here, the target is the program helloworld.  Note that it is not necessary to write helloworld.exe. The extension is chosen by SCons for you.  Targets are built from a list of sources.  Here the list of sources contains only one item: the C file "helloworld.c". SCons will automatically pick a compiler, and compile time flags to compile the source for you.  While this tutorial only covers C, SCons understand and can build a vast array of source types: 

* .c - a C source file 
* .cpp/.c++/.C++/.cxx/.cc - a C++ source file 
* .f/.for/.fpp - Fortran with optional C preprocessor in POSIX 
* .s/.SPP - an assembly file  with optional C preprocessor in POSIX 

## Running SCons

A complete list of options in running SCons can be found at the scons.org website: [http://www.scons.org/doc/HTML/scons-man.html](http://www.scons.org/doc/HTML/scons-man.html).  Only the basic options will be considered here.  Simply executing SCons will cause all targets to be built in or above the current directory.  In addition, it's possible to give SCons a target to have it build, for example: `"scons helloworld"`, would cause the hello world program above to be built.  Further, directories can be passed to SCons.  When a directory is given, all targets in and above that directory are built.  Thus: `"scons ."` would have the same result, in general, as running `"scons"`. To have everything done, including installation of programs, simply run `"scons /"`, or in Windows, `"scons C:"`.   (More on installation later.) 


## Finishing Up

It should be clear from this simple introduction that SCons is a powerful tool, capable of making your life a lot easier in building large projects.   Future tutorials will cover shared libraries, and simple programming inside the SConstruct files. 

Functions Covered in this Tutorial: Environment(), env.Program() 

Code: [sconstutorial1.tar.gz](https://github.com/SCons/scons/wiki/SconsTutorial1/sconstutorial1.tar.gz) 



# Programming with Scons


# Tutorial 2 - More Syntax, Shared Libraries, Install Targets


## Introduction

So now you have created your first program using scons.  This is all well and good, but there are several aspects that we are currently missing.  The biggest of these is creating an installation target.  After all, what good would a replacement to configure; make; make install be without install? (We'll get to setting up a configuration target in coming tutorials.)  This tutorial will cover install targets, and as an added bonus, we'll take a short look at shared libraries.  If you don't care about shared libraries, that section still has several hints helpful for different types of scons development. 


## Keyword Arguments

You may have noticed the use of keyword arguments in the last tutorial.  Bellow, we see an example of keyword arguments: 

`env.Program(target = "hello", source = ["helloworld.c"])` 

Here, the keyword arguments specify the "target", and the "source".  The keywords are "target" and "source".  The use of keyword arguments allows the arguments to be specified in the order that you desire.  For example, the above example might also be: 

`env.Program(source = ["helloworld.c"], target = "hello")` 

Keyword arguments also allow you to only enter a minimum of parameters.  Unneeded parameters simply stay at their default values. 


## Creating a Shared Library

Shared libraries are the life blood of modern operating systems.  SCons makes creating shared libraries as easy as creating programs.  Instead of using the env.Program() construct, we'll use env.[SharedLibrary](SharedLibrary)().  Seems logical doesn't it? Here is the syntax: 


```txt
lib_target  = "hello"
lib_sources = ["libhello.c"]

env.SharedLibrary(target = lib_target, source = lib_sources)
```
Note that in this example I use variables to determine the source list and target.  Variables can be used in place of any string and such in Scons.  (It must be of the same type though.)  There are a few important things to note about this code. 

First, the library prefix and suffix are determined automatically by SCons. In MacOS X, the extension will be correct.  In Linux, the extension will be correct. In addition, under Unix systems, "lib" will be automatically prepended to the target filename. It is possible to change the prefix however.  Recall that SCons uses keyword arguments.  To specify another shared library prefix, we can use the keyword argument SHLIBPREFIX: 

`env.SharedLibrary(target = lib_target, source = lib_sources, SHLIBPREFIX='')` 

In the example above, the shared library prefix is set to an empty string.  The shared library created then will have only the suffix.  For more on things like this, read the SCons manpage. 


## Advanced Topics

In this tutorial series several of the more advanced topics will be skipped over.  These are far too many and too numerous to mention in a simple tutorial series.  If you are interested in these advanced topics, the documentation for SCons is very complete and should help in the creation of any more advanced SConstruct. 


### Creating Installation Targets

Now that we've got our program and shared library, it's time to install them.  This part is fairly Unix specific.  (We'll get into how to make this more general later.) The first thing to realize, is that whenever we use env.Program, env.[SharedLibrary](SharedLibrary), or similar they have a return value that can be used to create install targets.  This return value might be thought of as a string containing the full name of the newly created object.  To use this name, all we must do is assign the return value to a variable. 

`hello = env.Program(source = ["helloworld.c"], target = "helloworld")` 

Now, we have an object representing the newly created program.  This object can then be used as an installation source.  To do this, we will use the env.Install() function.  Using the install function, it isn't neccessary to use keyword arguments as it only takes two arguments: the directory(keyword: dir), and the source(keyword: source). 

`env.Install("/usr/local/bin", hello)` 

This is the same as: 

`env.Install(dir = "/usr/local/bin", source = hello)` 

Now, at this time, we can install the program by running "scons /usr/local/bin".  To create the /usr/local/bin target.  Recall from the previous tutorial how the scons syntax works for directories.  Now, this isn't easy on users so we must do something to create an actual install target. 


### Target Aliases

**or, How to Make "scons install" Work** 

Sometimes it might be nice to have "scons" followed by a function name or target work.  But, at the same time, you don't want to require the user to enter multiple filenames, directories, or paths.  To get around this, scons has something called target aliases. The alias function accepts two arguments: the alias name(keyword: alias), and a list of targets(keyword: targets).  Now, recall that installation targets just happen to be the directory we are installing to.  So, to create an install target, we simply create an alias for the target install, that maps to ALL the directories we are installing to: 

`env.Alias('install', ['/usr/local/bin'])` 

And we're done! 


## Finishing Up

You should now be able to create shared libraries, use keyword arguments, and specify installation targets. 

Functions Covered in this Tutorial: Environment(), env.[SharedLibrary](SharedLibrary)(), env.Install(), env.Alias() 

Code: [sconstutorial2.tar.gz](sconstutorial2.tar.gz) 

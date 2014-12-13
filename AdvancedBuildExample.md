
**NOTE:  This page was edited by hand into its current format by cutting-and-pasting a copy of the page that was saved at archive.org.  It is entirely possible that some formatting or other errors crept in during the editing process.  If you notice any errors, please correct them.** 

This document describes the build used on the [Bombyx Project](http://bombyx.sourceforge.net/) in a way that is a tutorial of SCons. It covers various advanced topics in a bit of detail, and gives pointers to other documents that describe the technique in more detail. Some of the things shown here are "voodoo" and probably not standard. If you find a better way to do something, then please contact [me](mailto:zedshaw@zedshaw.com) with your suggestion. 

[[!toc ]] 


# Introduction

The great thing about SCons is that it is very flexible, but still very easy to use. The one bad thing is that there are few examples to get a person started. You can read the man page, but there's nothing that really shows you some best practices to follow at first. After working with SCons for a while, I've come up with a fairly well laid out build environment that works on multiple platforms with very little configuration. It follows a logical configuration where SCons can configure itself based on information it finds. It also breaks out the "configuration" of the build (such as where libraries are, and what header file paths are needed) from the actual Environment object specification. This is important when supporting multiple developers who use different systems, or when building on heterogeneous systems. This lets the user configure the build for the target system without modifying the operation of the build. 


## Key Terms

I'll be filling these in as I find things that I need to explain a bit better. 


# Build Design

The goal of the Bombyx build system is to create a logical build configuration that will make it very easy to build the software on multiple systems in a consistent manner. It also tries to separate the different levels of configuration from each other to allow for a modular design. Finally, it has a couple of advanced features which might interest you. 

I also wanted to make it easier to localize builds in the right place, and "autoconfigure" from the common config scripts found in many libraries (like, GTK+ has gtk-config, and FLTK has fltk-config). 

To accomplish this, I have the following: 

         * A file that contains the general build variables that you need to set no matter what target platform you have, like targets and sources and so on. 
         * A file that contains any functions you need to support your build outside of those provided by SCons. 
         * A single top-level SConstruct file that handles the major configuration work and target build directory selection. 
         * A SConscript file in a target build directory that makes final configurations for that platform. This also localizes build results into a single directory. 
The next section covers this layout in detail and gives some of the benefits of it. 


# Layout & Structure

First, we need to configure the locations of the different files necessary for the build, and describe what each does: 

         * _ROOT/_ 
                     * build_config.py 
                     * build_support.py 
                     * SConstruct 
                     * _src/_ 
                                 * main.cpp 
                     * _build/_ 
                                 * _linux/_ 
                                             * SConscript 
                                 * _freebsd/_ 
                                             * SConscript 
                                 * _win32/_ 
                                             * SConscript 
                                 * _darwin/_ 
                                             * SConscript 
                                 * _default/_ 
                                             * SConscript 
                     * _tests/_ 
                                 * testrunner.cpp 
                                 * test1.h 
The italicized things are directories (root, src, build, etc.) the other things are files used SCons in the build (SConstruct, build_support.py), and the .h and .cpp are example source files. The _root_ directory is just whatever you call the directory where you do your work. 

The first thing to notice is that, in addition to the SConstruct file in the _ROOT/_ directory, there's two more files, "build_config.py" and "build_support.py". The build_config.py file has basic configuration information that each developer would probably need to modify on different platforms. The build_support.py file contains any support functions you need that don't fit into the SCons system. I have a few nice little tricks in this file that make builds more automatic. 

The next thing of importance is the _build/_ directory and its contents. The _build/_ directory is where the program is built for each target system, using additional configuration information necessary for that system (in the SConscript file there). This build directory is switched automatically by a function in the build_support.py file depending on the platform indicated by Python. 

Finally, there's the _tests/_ and _src/_ directories, which hold the source code for the system. The _tests/_ directory is currently not used quite yet, but it will eventually hold Unit Tests from the [CxxTest](http://cxxtest.sourceforge.net/) project which this build configuration will run automatically and produce reports. The _src/_ directory just holds the source for your system. You can organize this directory how you wish, and I may have a configuration in the future that will allow SCons scan this directory and build different targets depending on how it is structured. 

Based on this, here's an example of what happens when you run SCons from the _ROOT/_ directory on a Mac OS X (Darwin) system: 

      1. SCons reads the SConstruct file 
      1. SConstruct imports the contents of build_support.py and build_config.py 
      1. SConstruct uses a function ([SelectBuildDir](SelectBuildDir)) from build_support.py to figure out what the target build directory should be. 
      1. The [SelectBuildDir](SelectBuildDir) function does some magic (explained later) to figure out that the darwin target should be built in _ROOT/build/darwin_. 
      1. SConstruct switched to _ROOT/build/darwin_ and loads the SConscript file there 
      1. This final SConscript file makes any last minute changes necessary to build on the target system and then starts the build like normal. 
While this may seem complex at first, it has a few very big advantages over just a single SConstruct build: 

      1. If you want to change the configuration for a build, you just edit build_config.py 
      1. If something weird needs to be done on a target platform, you just edit the ROOT/build/&lt;target&gt;/SConscript file. 
      1. You shouldn't have to edit the ROOT/SConstruct file after you have it configured (even when you switch to a new target). 
      1. Adding a new target is as easy as just making a new directory in _ROOT/build_ and adding an SConscript file with the required changes. 
      1. SCons will default to the _ROOT/build/default_ directory if present, letting you put a generic SConscript file for any unkown targets. 
      1. The build is localized to a single directory, which makes it a bit easier to organize multi-target builds. 
Finally, I have done most of the work for you, so you should just have to modify the files a bit to get things going and then you're done. 


# Support Library

The build_support.py file has some functions that the SConstruct build uses to do some work. These files really don't have anything to do with the current build setup, and only clutter the SConstruct files if you put them there. By moving these support routines into your own file, you localize them and make them easier to maintain. It also keeps the SConstruct files clean from anything unecessary. 

The code for the first function used in Bombyx is very interesting: 
```txt
def ParseConfig(env,command,options):
    env_dict = env.Dictionary();
    static_libs = []

    # setup all the dictionary options
    if not env_dict.has_key('CPPPATH'):
        env_dict['CPPPATH'] = []

     if not env_dict.has_key('LIBPATH'):
         env_dict['LIBPATH'] = []

     if not env_dict.has_key('LIBS'):
         env_dict['LIBS'] = []

     if not env_dict.has_key('CXXFLAGS'):
         env_dict['CXXFLAGS'] = []

     if not env_dict.has_key('LINKFLAGS'):
         env_dict['LINKFLAGS'] = []

     # run the config program to get the options we need
     full_cmd = "%s %s" %  (WhereIs(command), join(options))

     params = split(os.popen(full_cmd).read())

     i = 0
     while i < len(params):
         arg = params[i]
         switch = arg[0:1]
         opt = arg[1:2]
         if switch == '-':
             if opt == 'L':
                 env_dict['LIBPATH'].append(arg[2:])
             elif opt == 'l':
                 env_dict['LIBS'].append(arg[2:])
             elif opt == 'I':
                 env_dict['CPPPATH'].append(arg[2:])
             elif arg[1:] == 'framework':
                 flags = [env_dict['LINKFLAGS']]
                 flags.append(join(params[i:i+2]))
                 env_dict['LINKFLAGS'] = join(flags)
                 i = i + 1
             else:
                  env_dict['CXXFLAGS'].append(arg)
         else:
             static_libs.append(arg)
         i = i + 1

     return static_libs
```
What this function does is take an SCons Environment object to work on, a command to run which should output compiler options, and a list of options to pass to the command. It then takes the standard output from this command, parses it, and modifies the Environment appropriately so that the library will work. It is used like so: 
```python
#!python
ParseConfig(env, "fltk-config","--static")
```
The function then runs "fltk-config --static", takes the output that the script gives (which are the compiler options needed to use FLTK), and modifies the Environment object _env_ so that it reflects those options. Since SCons doesn't allow you to specify static libraries in the list of libraries, it returns the statis libraries so you can append them to the build sources in your targets. 

/!\ Bombyx currently doesn't use this function since I've switched to using FOX, which doesn't have a configure script. Still, it's a very useful function, feel free to steal it. 

The next function simple takes a build directory and a platform (if you don't give a platform, it will ask Python what it thinks the platform is). It then for a build directory under _ROOT/build_ that matches the platform name. If a platform is not found then it defaults to the _ROOT/build/default_ directory, so that you can at least attempt building on unknown platforms. 
```python
#!python
def SelectBuildDir(build_dir, platform=None):

    # if no platform is specified, then default to sys.platform
    if not(platform):
        platform = sys.platform

    print "Looking for build directory for platform '%s'" % platform

    # setup where we start looking at first
    test_dir = build_dir + os.sep + platform
    default_dir = build_dir + os.sep + 'default'


    # we look for a directory named exactly after the
    # platform so that very specific builds can be done
    if os.path.exists(test_dir):
        # make sure it is a directory
        target_dir = test_dir
    else:
        print "Exact match not found, finding closest guess"

        # looks like there isn't an exact match
        # find the closest matching directory
        dirs = os.listdir(build_dir)
        found_match = 0
        for dir in dirs:
            if platform.find(dir) != -1:
                 # found a match (hopefully the right one)
                 target_dir = build_dir + os.sep + dir
                 found_match = 1
                 break
        if not(found_match):
            print "No match found, looking for 'default' directory"
            # looks like this platform isn't available
            # try the default target
            if os.path.exists(default_dir):
                target_dir = default_dir
            else:
                # bad, nothing is available, tell the user
                print "No build directories found for your platform '%s'" % platform
                return None

    print "Found directory %s, will build there" % target_dir
    return target_dir

```
This function is the core of the Bombyx build setup, as it allows you to create different build target directories and easily configure them. I would like to add the ability to select the closest matching build directory if an exact match isn't found. So, if netbsd doesn't exist, then it will try bsd, and if that isn't found then default is chosen. 

The next file is simply a nice thing to have if you absolutely must have a file. SCons doesn't give good error messages when a missing library or something (it just lets the compiler do it). Using this function let's you require a particular set of files before continuing. It exits whenever it encounters a file not found so that the user can correct the problem. 
```python
#!python
def RequireFiles(files, found_files, search_path):
    i = 0
    for file in found_files:
        if not(file):
            print "ERROR:  Could not find the %s file in:" % files[i]
            print "ERROR:  \t%s" % search_path
            print "ERROR:  Edit the build_config.py file and add"
            print "ERROR:  the location of this file to the appropriate variable."

            sys.exit(1)

        else:
            i = i + 1

```
These functions are hidden away in the build_config.py so that the SConstruct files are easier to understand and modify later. 


# Configuration File

The next part of this build is the build_config.py file, which contains the variables that all targets need, usually consisting of variable assignments. Here's the build_config.py from Bombyx: 
```python
#!python
import os

## where we find libsilcclient.a, libsilc.a, and other STATIC libraries
lib_search_path = ['/lib','/usr/lib','/usr/local/lib','/usr/local/silc/lib']

## where we should find things to include
include_search_path =  ['/usr/local/silc/include','#src']

## These are our source files
sources = ['ChatWindow.cpp', 'dbg.cpp', 'FXBroadcast.cpp', 'MainWindow.cpp', 'Server.cpp','main.cpp']
test_sources = ['ChatWindow.cpp', 'dbg.cpp', 'FXBroadcast.cpp', 'MainWindow.cpp', 'Server.cpp','#tests/testrunner.cpp']

# update the environment with options from fltk-config
static_libs = ['/usr/local/lib/libFOX.a']

#### You should not change these.  These are only here
#### If you want to start your own build setup with a
#### different layout than mine.
source_base_dir = 'src'
build_base_dir = 'build'
target_name = 'bombyx'

```
As you can see, this is pretty simple stuff. The nice thing is that even the source_base_dir, build_base_dir, and target_name variables are configurable. This lets potential users change the layout of the directory structure if they don't like the name 'src' and 'build'. 

The target_name variable is probably not useful if you need to compile multiple target files (programs, libraries, etc.). Right now Bombyx just has one target file (bombyx) and eventually a test target. I'll have to develop a way that you can configure multiple sources-&gt;target configurations. But, this is good enough for now, and any more would probably just confuse things. 

The key to this file is that, when you go to a different target platform, you can just go into this file and make the changes you need easily. Also, if you need to add a new source file, you just edit the build_config.py file again. 

/!\ Currently the test_sources is only used for my development of the testing framework for Bombyx. I'll be updating this document with that when I'm done with it. For now, just ignore. 


# Top Level SConstruct File

Now that all the support stuff is out of the way, I'll cover the top level SConstruct file. This file acts as the major configuration entry point, and coordinates all the other SConstruct files. It does as much configuration as it can for all target platforms, then it switches to the platform specific SConscript file for each platform in _ROOT/build_. 

The top level SConstruct file follows: 
```python
#!python
import os
import sys
from build_support import *
from build_config import *


# Setup some of our requirements

env = Environment()

# setup the include paths where FLTK and silc should live
env.Append(CPPPATH=include_search_path)
env.Append(LIBS=['m', 'jpeg', 'png', 'tiff', 'z', 'Xext', 'X11'])
env.Append(LIBPATH=['/usr/X11R6/lib'])

# variables the sub build directories need
Export('env', 'sources', 'static_libs', 'test_sources')


# start the build
target_dir = '#' + SelectBuildDir(build_base_dir)
SConscript(target_dir + os.sep + 'SConscript')
BuildDir(target_dir, source_base_dir, duplicate=0)
Default(target_dir + os.sep + target_name)

# this sets up an alias for test that will compile the unit tests
# into the resulting testrunner program.
env.Alias('test', target_dir + os.sep + 'testrunner')

```
You should be careful of line #23 since it contains the "duplicat=0" argument to ?[BuildDir](BuildDir). This tells SCons to not copy files to the platform build dir (like .h and .cpp stuffs) when it does the build. This is important because the **scons -c** command does not properly clean these files out, and when there are errors you'll get the line numbers from the copied files and not the actual files. This makes it really difficult to find the errors automatically in things like Emacs or Vim. 

This file imports the stuff it needs, sets up the basics of the Environment variable, exports the necessary variables to the platform SConscript file, and then switches to that file. It also has some stuff specific to the Unit Testing framework I'm developing for SCons which we'll ignore. 

I'll cover this file line by line as it is the general culmination of what we've covered so far: 
[[!table header="no" class="mointable" data="""
1 to 4 | Imports some Python libraries and the build_support.py and build_config.py files to get the required configuration variables and support functions. Notice it uses a from statement to to the imports for build_support.py and build_config.py so that they can be refered to directly (it's inconvenient to have to say build_config.build_dir).
9 | Sets up the Environment object env that we'll use to configure the build.
12 to 14 | Appends some additional information that all targets need (targets that don't need it can remove them in the platform SConscript file).
17 | Exports the variables that each platform SConscript file will need to complete the build configuration. These are later Imported by the platform SConscript file.
21 | This runs the ?[SelectBuildDir](SelectBuildDir) function defined in the build_support.py file to figure out what the platform build directory should be.
22 | Tells SCons to use continue processing with the SConscript file in the platform build directory.
23 | Tells SCons to use the build directory that [SelectBuildDir](SelectBuildDir) returns. The duplicate=0 says not to copy the files from source to the build dir when it builds. This has some consequences, but gives you better error messages.
24 | Sets up the default target to whatever we described in the build_config.py file. This is only a convenience so that people can type "scons" without having to say "scons build/darwin/bombyx".
28 | This is for the future Unit Test running setup. It creates an alias from "test" to the testrunner program. This lets users do "scons test" and have the testrunner build. This currently works, but I need to add running the test program and also building reports.
"""]]

This is pretty straight forward and demonstrate some of the features of SCons. You could move things from build_config.py as you see fit. For example, if I wanted to have multiple targets, I would probably want to move them to this file where I have more flexibility (build_config.py usually just has variable assignments, where SConstruct files can use all of SCons). 


# Platform SConscript Files

Next I'll cover the most complicated platform SConscript file, that for the Mac OS X platform. This platform is interesting since it has such a wildly different installation of GCC, which defaults to strange locations and uses GCC 2.95.2 by default. This requires us to make major changes to the environment in the platform SConscript file. Here's the file: 
```python
#!python
# import these variables from the parent build script
Import('env', 'sources', 'static_libs', 'test_sources')

# add the specific things needed by MacOSX GCC
macosx_incs=[]

env.Replace(CXX='g++3')
env.Replace(CC='gcc3')
env.Replace(CPP='gcc3')
env.Replace(LINK='g++3')
env.Append(CXXFLAGS='-DDBG_ENABLED')
env.Append(CPPPATH=macosx_incs)


# add the bombyx target to the environment
env.Program(target='bombyx', source=sources + static_libs)

# add the testrunner target to the environment
env.Program(target='testrunner', source=test_sources + static_libs)
```
We'll cover this file line by line also so that you can understand each thing going on. It's pretty simple, and I'll demonstrate a regular build for the Linux platform later. 
[[!table header="no" class="mointable" data="""
2 | Imports the variables the the root SConstruct file Exported previously (go look, this is really, really important in this build setup). Make sure you understand this concept. You can call Export() from one SConstruct, switch to another SConscript and then Import those same (or less) variables.
7 to 12 | We just replace some variables that Mac OS X needs configured differently. This is an example of modifying what the root SConstruct file thinks is correct. Usually you won't have to do this, but Mac OS X is just weird. You could also add extra libraries and other options here.
16 | This adds a Program target for the 'bombyx' program and sets the sources to the sources and static_libs variables. The sources and static_libs variables were variables we set in the build_config.py file, which were exported by the root SConstruct file (and then imported by us). I decided not to use the target I configured in the build_config.py to demonstrate that you can change it.
19 | This file sets up a Program target for 'testrunner' that is used to run the Unit Tests. it works the same as what we did in lin 16.
"""]]

Pretty simple huh? Now, the nice thing is that, when you hit another platform that is similar to Mac OS X (NeXT?), you just make a new directory, copy this SConscript file into it, and make any changes you need. You shouldn't have to edit anything else. 

When you run SCons with this command: 

scons 

Then SCons will read the build_config.py, build_support.py, _ROOT/Sconstruct_, and then the _ROOT/build/darwin/SConscript_ file to figure out how to build your program. After that, it just builds it as specified and puts the results in the _ROOT/build/darwin_ directory. 

Just for completeness, here's the build file for Linux: 
```python
#!python
# import these variables from the parent build script
Import('env', 'sources', 'static_libs')

# add the bombyx target to the environment
env.Program(target='bombyx', source=sources + static_libs)
```
That's it. You just import the stuff you exported and setup your targets. Actually, this is so common that you could just put this file in the _ROOT/build/default_ directory, and then you'll only need to create a directory for the strange platforms. 


# Modifying The Setup

If you want to modify this setup, just make sure you understand it and then change the files that are appropriate. This list will help guide you in where to go to make major changes. If you just want to use the setup, then you should only need to change the _ROOT/build_config.py_ file, and create platform specific files in the _ROOT/build_ directory. 

**ROOT/build_config.py** 

         * This is where you put common variable assignments that are used in all SConstruct files (or most of them). 
**ROOT/build_support.py** 

         * Put your support functions and other code that you need for your build. 
**ROOT/SConstruct** 

         * This is primary place where SCons does most of its work. Generally, you put things in here if they require SCons features, but they are common to all targets. 
**ROOT/build/default/SConscript** 

         * Set this file up for the targets that you can configure with the same platform configuration. 
**ROOT/build/PLATFORM/SConscript** 

         * Put the things that are specific to PLATFORM in here. This localizes what is needed for each platform in a consistent location. 
Once you figure out where you need to make your changes, pick a familiar platform and get your build to work with it. Once it works for that platform, go onto another and try configuring it by just creating a platform SConscript file. If you need to make changes to the other files, then see if the changes are necessary to your already working platforms. If not, try using the SCons methods mentioned in the man page to modify the build in the platform SConscript file. 


# Further Information

I hope this document helps you get some work done. This configuration is a bit complicated, but once you grok it, it is very nice to work with. There are some bugs in it (which I've noted with /!\ symbols) but these are minor and only affect a few platforms. 

If you want to get this build, then you can go to the [Bombyx](http://bombyx.sourceforge.net/) site and check out (anonymously) the CVS root. You'll need to check-out the BOMBYX_MS1 branch to get these changes. If you don't know how to do this, then just wait a while and I'll make a release with all the changes in it. Until then, all the code in the Bombyx build is in this document. You could just hit the "Edit" link below and cut and paste the code right out (it's inlined verbatim). 

If you have any suggestions for improvements, or questions, then just e-mail me at [zedshaw@zedshaw.com](mailto:zedshaw@zedshaw.com). Enjoy! 

**Table of Contents**

[TOC]

# Windows

* Also see [SconsToolbox](SconsToolbox) for more Windows-related tools 


## Good to know

Environment space and environment variable limitations must be kept in mind. At [http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/ntcmds_shelloverview.mspx?mfr=true](http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/ntcmds_shelloverview.mspx?mfr=true) Microsoft says... 

* The maximum individual environment variable size is 8192bytes. The maximum total environment variable size for all variables, which includes variable names and the equal sign, is 65,536KB. 
But at [http://support.microsoft.com/kb/830473](http://support.microsoft.com/kb/830473) they also say... 

* Even though the Win32 limitation for environment variables is 32,767 characters, Command Prompt ignores any environment variables that are inherited from the parent process and are longer than its own limitations of either 2047 or 8191 characters (as appropriate to the operating system). For more information about the [SetEnvironmentVariable](SetEnvironmentVariable) function, visit the following Microsoft Web site: [http://msdn2.microsoft.com/en-us/library/ms686206.aspx](http://msdn2.microsoft.com/en-us/library/ms686206.aspx) 
In order to find native libs required by python and its extension the location of these libs can be put into the PATH environment variable. If this is what SCons does, does it detect overflowing the process' environment space or the maximum size of the PATH environment variable? If it does not, at some point it will break, and worse, because everyone checks out to a different path, so that the resulting locations will vary in length, it will break down more or less at random. 


## Manifests

* [EmbedManifestIntoTarget](EmbedManifestIntoTarget): how to embed the manifest file into your target file using the Microsoft Manifest Tool 

## Visual C++

* If using Microsoft Visual C++, you need to set 'INCLUDE', 'LIB' and 'PATH' in your environment, then import them when you create your 'Environment' object. These will be used to locate the MSVC++ tools and set 'CPPFLAGS' etc. 
* If you need to #include <windows.h>, make sure you **don't** use the '/Za' compiler flag. You'll get a whole lot of errors, the reason for which will not be apparent from the messages. 
* Note, on the other hand that if you want to process 'bison' output with MS VC++, you **will** need to use CCFLAGS=['/Za']. 
* [SconstructShortMsvcWin32](SconstructShortMsvcWin32): The shortest SConstruct using MSVC under Win32. 
* [SconstructShortMsvcExpWin64](SconstructShortMsvcExpWin64): The shortest SConstruct using MSVC Express under Win64. 
* [SconstructShortMsvcWin32BuildDir](SconstructShortMsvcWin32BuildDir): MSVC under Win32, with build dir. 
* [SconstructShortMsvcWin32CompileParms](SconstructShortMsvcWin32CompileParms): MSVC under Win32, with build dir, compile parms 
* [SconstructShortMsvcWin32DebugRelease](SconstructShortMsvcWin32DebugRelease): MSVC under Win32, with build dir, debug/release 
* [MsTest](MsTest) - running MS VS unittests (mstest) and generating coverage reports as html 
* [MsvsMultipleVersions](MsvsMultipleVersions): how to select MSVS version when multiple versions are installed 

## MinGW

* [CrossCompilingMingw](CrossCompilingMingw): Enable building on Unix for itself and for Win32 with mingw32 cross compiler 
* [SconstructShortMingwWin32](SconstructShortMingwWin32): The shortest SConstruct using Mingw under Win32. 
* [UsingPkgConfigMsysShellScripts](UsingPkgConfigMsysShellScripts): how do you use shell scripts that behave similar to pkgconfig one Windows with MSys/MinGW?  One example is wx-config 
* [LongCmdLinesOnWin32](LongCmdLinesOnWin32) helps with the severe problem of having very long shell commands not working with Windows. You typically encounter this when dealing with linking large projects with MingW.  


---

 
# Linux

* When linking Fortran and C objects, especially if you're using G77 to compile the Fortran, you'll often need to explicitly link to 'libg2c'. The location of this file is usually **not** /usr/lib -- it will be somewhere in a subdirectory there, which you need to explicitly add to your 'LIBPATH'. 


---

 
# Mac OS X

* [MacOSX](MacOSX): tips for using SCons with Mac OS X. 


---

 
# Palm

* [PalmApplications](PalmApplications): how to build Palm applications on Linux and Windows(cygwin) with the Palm prc-tools 


---

 
# Pocket PC

* [PocketPc](PocketPc): Building a Pocket PC application with the Pocket PC 2002 SDK 
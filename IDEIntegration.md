**Table of Contents**

[TOC]

# Integrating scons into IDEs

IDEs can often parse the output of build tools like scons which output the warnings and errors from the compiler etc as if the IDE had called the compiler itself. By using scons with your favourite IDE the best of both worlds can be obtained. 

* The build process is developed in a cross platform, text based flexible form, instead of all the build settings being recorded in some form only editable through GUI. 
* All of the great features of the IDE - Text editors with code completion, debugging etc, clicking on errors to see the line of code that caused them etc 
Below are instructions to get started using scons with some particular IDEs. 


## Visual Studio .NET 2003 / Visual Studio 2005 (Windows)

1. Launch Visual Studio with the /useenv command line switch otherwise it won't be able to find scons. 
1. File->New Project General->Make File Project 
1. Save the project into the same directory as your SConstruct file. 
1. In the project settings, just add "scons" as the build command , and "scons -c" as the clean command and configuration is done. 
1. You should now be able to build using scons by using the build menu from visual studio. 
Note: VS2005 seems to need absolute paths to filenames for the click-on-errors integration to work. --[björnen](björnen) 
1. For debug build the command should be "scons debug=1"
1. For Rebuild All: "scons -c & scons" ("scons -c & scons  debug=1" for debug)

Alternatively, you can use [the `MSVSProject()` builder](http://scons.org/doc/production/HTML/scons-user.html#b-MSVSProject) in your SConstruct file to generate a Visual Studio project file.

## Xcode (Mac OS X)

1. File->New Project, choose "External Build System" 
1. Save the project into the same directory as your SConstruct file. 
1. In Groups and Files -> Targets, double click the target that was automatically created. 
1. In the Build Tool field, put the full path to scons - like "/System/Library/Frameworks/Python.framework/Versions/2.3/bin/scons 
1. Set the Directory field to the directory that contains the SConstruct file. 
1. You should now be able to build using the Build command from Xcode 
1. Right click "Executables" and choose "Add new custom executable" and point it to the executable you are building and then you can debug using Xcode. 
1. Use Debug -> Breakpoints menu to add a symbolic breakpoint at main() - just type main where it says 'Double click for Symbol' - if you don't add this break point none of the breakpoints set in the editors will work, because gdb doesn't have the symbol information until you start debugging ([Jim Ingham suggests](http://www.cocoabuilder.com/archive/message/xcode/2006/8/15/8869) turning off "Lazy Symbol Loading" in Debug Preferences.) 
See also the hint to get proper error parsing on [MacOSX](MacOSX). 

Alternatively, you can use [scons-xcode](https://bitbucket.org/al45tair/scons-xcode) to generate project files automatically.

## Eclipse

SConsolidator is an Eclipse plug-in that provides tool integration for SCons in Eclipse for a convenient C/C++ development experience. Its main features are: 

* Convertion of existing CDT managed build projects to SCons projects 
* Import of existing SCons projects into Eclipse with wizard support 
* Interactive mode to quickly build single source files speeding up round trip times 
* A special view for a convenient build target management of all workspace projects 
* Graph visualization of build dependencies with numerous layout algorithms and search and filter functionality that enables debugging of SCons scripts 
More information can be found at [http://sconsolidator.com](http://sconsolidator.com) and its update site is available at [http://www.sconsolidator.com/update](http://www.sconsolidator.com/update). 



---

 There is also and older Eclipse Plug-in for SCons, though its documentation is scarce to nonexistent (see [plugin](EclipsePlugin)). 

Pros: It offers integrated support for building doxygen documentation and cppunit tests. 

Cons: It imposes a build tree hierarchy which may work for smaller projects, but would be cumbersome for larger projects. 


## KDevelop

See [SCons Setup](http://www.kdevelop.org/mediawiki/index.php/FAQ#How_can_I_set_up_a_project_with_SCons.3F) and [Custom Project](http://www.kdevelop.org/mediawiki/index.php/FAQ#How_to_create_a_simple_project_with_just_a_Makefile_.28also_known_as_Custom_Project.29_.3F) at the KDevelop FAQ. Here's a quick copy of these two topics. 


### How can I set up a project with SCons?

[SCons](http://www.scons.org) is a software construction tool.  KDevelop (as of version 3.2.2) does not support SCons projects directly.  However, it is possible to set up a project very simply using SCons by writing a "stub" Makefile and using the "Custom Makefiles" project type.  An example of a simple stub Makefile is the following (note that lines after target names should be indented with tabs, not spaces): 

* project_name: 
   * scons clean: 
   * scons --clean 
This will enable the _Build Project_ and _Clean Project_ actions to work. 


### How to create a simple project with just a Makefile (also known as Custom Project) ?

Create a Custom Project. There is no direct way to create a custom project (i.e. a project which does use its own makefiles). Use Project->Import Existing Project instead. Remember to set the appropriate Project Type, labeled by an additional (Custom Makefiles) in the dialog. Use Project Options Early. Whenever you start a new project do not forget to set the Project->Project Options... to your needs. 


## Emacs and XEmacs

First of all, you are going to want [PythonMode](http://www.emacswiki.org/cgi-bin/wiki/PythonMode) if you don't have it already.  If you are running on a system with a package manager, you might wish to look there first.  On my Fedora system, the base XEmacs install was missing many useful accessories.  I achieved a more complete installation with the command: 

* sudo yum install xemacs-packages-base xemacs-packages-base-el xemacs-packages-extra xemacs-packages-extra-el xemacs-packages-extra-info 
For Emacs, it is suggested to add the following to your .emacs files, to enable Python mode for SConstruct and SConscript files. 


```txt
 (setq auto-mode-alist
      (cons '("SConstruct" . python-mode) auto-mode-alist))
 (setq auto-mode-alist
      (cons '("SConscript" . python-mode) auto-mode-alist))
```
For XEmacs, a different reference suggests an alternate syntax added to your ~/.xemacs/init.el: 


```txt
 (add-to-list 'auto-mode-alist '("SConstruct" . python-mode))
 (add-to-list 'auto-mode-alist '("SConscript" . python-mode))
```
If you wish to invoke a compilation via SCons from within Emacs/XEmacs, there are two ways to go about it.   You can add a simple Makefile stub to your project directory with a rule to immediately delegate to SCons instead.   The simplest example is just: 

* main: 
   * scons 
Make certain the second line begins with a tab character.  make and gmake have a hangup about that.  This is also helpful for others to invoke your project build who aren't used to invoking SCons directly.  Emacs/Xemacs will normally invoke make or gmake as the default compile command, and this simple Makefile will then transfer the build to SCons. 

You can also change your Emacs/XEmacs default compile command by adding the following to your init file: 

* (defvar compile-command "scons") 
This setting might affect other projects you compile normally with make or gmake, but if you compile everything via SCons, it eliminates the clutter and indirection of the Makefile stubs.  If you use Makefile stubs, you might discover you need a separate Makefile stub in each project subdirectory where you compile code. 


### Compilation mode and error navigation

Compilation mode and its usage is documented as part of the [GNU Emacs Manual](http://www.delorie.com/gnu/docs/emacs/emacs_319.html). 

If you employ a custom or unusual build tool as part of your build process, you might find your Emacs/XEmacs is unable to navigate the error text in the *compilation* buffer.  To fix this, you can provide a custom regular expression for the variable _compilation-error-regexp-alist_. 

This is a fairly advanced undertaking.  The page [(efaq)Compiler error messages](http://www.cs.cmu.edu/cgi-bin/info2www?(efaq)Compiler%20error%20messages) can get you started.  It suggests cribbing something similar to what you require from the Emacs source for compile.el, which contains many elaborations.  On my Fedora system, this file is located at _/usr/share/xemacs/xemacs-packages/lisp/xemacs-base/compile.el_, but only after I manually installed the package sources (.el files) as described above.  If you only find compile.elc, you have the package installed, but not the package sources. 

Hi [MaxEnt](MaxEnt) -- here's what I use, it's much simpler.  You'll need a recent emacs (more recent than 21.1).  It just processes the filenames to remove the build dirs. 


```txt
;;; SCons builds into a 'build' subdir, but we want to find the errors
;;; in the regular source dir.  So we remove build/XXX/YYY/{dbg,final}/ from the
;;; filenames.
(defun process-error-filename (filename)
  (let ((case-fold-search t))
    (setq f (replace-regexp-in-string
             "[Ss]?[Bb]uild[\\/].*\\(final\\|dbg\\)[^\\/]*[\\/]" "" filename))
    (cond ((file-exists-p f)
           f)
          (t filename))))

(setq compilation-parse-errors-filename-function 'process-error-filename)
```
-- [GaryOberbrunner](GaryOberbrunner) 


## Qt Creator

[Qt Creator](http://qt.nokia.com/products/developer-tools/developer-tools) is a free, cross-platform, lightweight IDE. Although designed to integrate with Qt, it can be used for any C++ project. 

To use it with scons: 

* File | New file or project | Other project | Import existing project. Click the Choose button. 
* Enter a name for the project and navigate to the source directory. 
* Verify that the File selection is as you want or fine-tune it. Click the Continue button. 
* Optional: choose if you want to add the files to a version control system. 
* Click the Done button. 
Qt Creator will add four files to the top-level directory: 

* $PROJECT_NAME.files 
* $PROJECT_NAME.includes 
* $PROJECT_NAME.config 
* $PROJECT_NAME.creator 
The most important one is $PROJECT_NAME.files, which is just a list of all the files you want to show in the IDE. See [http://doc.qt.nokia.com/qtcreator/creator-project-generic.html](http://doc.qt.nokia.com/qtcreator/creator-project-generic.html) for details. 

Now you have to add the SConstruct and SConscript files to the IDE. Either edit by hand the $PROJECT_NAME.files or, in the IDE project browser, right click on the top-level directory and select "Add existing files", and then select SConstruct from the list. Do the same for the SConscripts. 

Last step: adding a build and a clean target. 

On the left pane, click "Projects". Verify that the tab name is actually your project. Click on "Build Settings". The "build directory" field is a bit misleading with scons. Don't modify the default, it will use the source top-level directory. Same for the "Tool chain" pull-down menu, leave the default, it is not used by scons. 

Under "Build Steps", remove the "Make" item by hovering on "Details" and clicking the X that appears. 

Click "Add Build Step", select "Custom process step", tick the "Enable custom process step", under "Command" enter the full path to scons. Leave the other fields as they are. Eventually pass a -j2 in the "Commands arguments". 

Under "Clean Steps", do the same thing as for "Add Build Step", only difference is that you will add "-c" to "Commands arguments". 

You are all set! :-) 

On the left pane, click on "Edit". You will find the previous view, with the project browser. Your scons project is ready to be be built. 


## Geany

[Geany](http://www.geany.org/) is a free, cross-platform, lightweight IDE. 

To use it with scons: 

Project -> New (store the project file anywhere) 

Project -> Properties -> On the Project tab : set the base path of the project to where the SConstruct file is. 

Open a source file in the file browser : geany appears to keep different build settings for different source types. 

Project -> Properties -> On the build tab : 

set the compile and build command for the source type to "scons -j <cpu count>" 

set the working dir to "%p" (which is the base path of the project where the SConstruct file is). 

Optional : set the source file independant build commands too, and scons -c for clean, all with %p as the working dir. 
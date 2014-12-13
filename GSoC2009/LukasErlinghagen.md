

# Improving SCons on Windows

This project aims to improve the installation and usage of SCons on Windows systems by providing a self-contained installer, documentation and a GUI front-end for SCons. Some deliverables will also be useful for other platforms such as Linux and Mac OSX. 


### Contact Information
[[!table header="no" class="mointable" data="""
 Name  |  Lukas Erlinghagen 
 Email  |  erlukcreinfeldeATgmailDOTcom 
 Timezone  |  CEST (currently UTC+2) 
 Place of Residence  |  Karlsruhe, Baden-Württemberg, Germany 
 ICQ  |  33 69 47 32 6 
"""]]


## Abstract


### Overview

For Windows users, SCons currently provides a simple installer to install it into a Python distribution on the user's machine. Currently, there are several drawbacks: 

* Users need to have Python installed 
* SCons is not added to the %PATH% and thus cannot be called directly from the command line 
* The installer is not aware of Vista's User Account Control (UAC) 
* SCons is not integrated into the start menu 
* The installer provides no documentation or 'uninstall' option 
The project will improve on this by combining a self-contained SCons executable, documentation and Windows Explorer integration into a convenient installer. Users will only need this installer in order to use SCons in their projects. 


### Benefits

Providing a single installable package will help SCons being accepted by Windows users. By not relying on a system-wide Python installation, SCons can be locally installed by users that do not have Administrator privileges on their development machines. 

Simple improvements such as installing the documentation alongside the SCons executable itself, being able to run SCons from the command line as well as the Windows Explorer, and providing a clean uninstall option will make using SCons on Windows simpler and more enjoyable. 


## Detailed Description


### Analysis


#### The program itself

Currently, using SCons on Windows requires users to have a working Python installation. Providing a self-contained executable instead of installing SCons into the Python distribution's 'site-packages' provides several benefits: 

* Users do not have to have Python installed 
* Users do not have to have write access to their Python installation 
* In some development environments, standards are in place that prohibit installation of additional software without prior approval. Reducing dependencies of a software makes it easier to get said approval 
* An independent executable makes it easier to add SCons to the %PATH% and to run it from the command line 
* Having that executable include the Python runtime for SCons simplifies bug hunting, since the version of Python used to run SCons is known 
Therefore, the first step of this project is to produce a self-contained version of SCons that can be used on Windows without any Python installation. After this is completed, it will be possible to run a build from the command line using the stand-alone executable. 

Given that the development tool chain for the project to be built is installed, SCons should be able to correctly perform the build. During this step, tests will be created to make sure that the stand-alone executable behaves the same way as a Python-based installation of SCons. 

There are several tools to turn Python programs into self-contained executables, such as py2exe or [PyInstaller](http://www.pyinstaller.org/). Since PyInstaller targets Windows, Linux and Mac OSX (currently experimental), it is the obvious choice to build a self-contained SCons. While this project will focus on Windows, the PyInstaller build mechanism can be reused on other platforms. 


#### The installer

Another important aspect of software usability is the installation process. A good Windows installer will 

* bundle a program and additional material such as plug-ins, examples or documentation 
* give users the choice of what to install, and where to install it 
* provide optional start menu entries 
* provide an uninstall option and integrate it into the corresponding Windows command panel applet 
* check for sufficient disk space and access rights 
* work correctly with Vista's UAC 
* possibly download additional dependencies (MSVC runtime components, for example) 
* add programs to the %PATH% 
* make the SCons engine available to all local Python installations 
The second part of this project will focus on creating an installer for SCons that meets all of the above requirements. 

Some popular open source installer creation systems are [WiX](http://wix.sourceforge.net/), [Inno Setup](http://www.jrsoftware.org/isinfo.php), and [NSIS](http://nsis.sourceforge.net/Main_Page). Further research is needed to determine which one should be used to create the SCons installer. 

Tests for this stage will need to ensure that the installer can be built without errors. It might also be possible to run the installer under 'wine' and check whether the installation succeeded. 

Another aspect of this stage is updating the release mechanism to build and distribute this installer instead of the current, 'distutil'-based one. 


#### Windows integration

Many Windows users are not used to working on the command line to build software, so it should be possible to start a SCons build from inside the Windows Explorer. In addition to SCons and the corresponding documentation, the installer package described above will optionally provide 

* an "Open command prompt here" entry in the context menu of folders 
* a "Quick SCons build" option in the same place that will launch SCons without any arguments 
* a GUI front-end to SCons (see below) 
* a "Run SCons GUI" entry in the context menu of folders 

#### GUI front-end

The planned front-end will allow launching SCons builds using a GUI. It will be possible to select a directory and the options that are passed to SCons. Besides manual entry, the front-end will allow quick access to the command line options such as '--quiet' and an area to specify name-value-pairs. A possible future improvement is a project scanner that will determine all possible targets inside a build tree and let the user select which one(s) to build. 

The final part of this project is to implement this GUI application. It will be written in Python using [TkInter](http://wiki.python.org/moin/TkInter), since SCons itself is written in Python, and [PyInstaller](PyInstaller) provides an option to add TkInter to an executable it creates. This is also something that can be used on Platforms besides Windows. 


### Backward Compatibility

The Python version shipped with the self-contained SCons may be different from the system-wide Python installation. I'm currently not sure if this will turn out to be a problem, so I definitely need input from the SCons developers here. 

Given that there are currently some i18n bugs with SCons that rely on a minimum Python version, it might be advisable to ship the Windows version of SCons with Python 2.X. Again, this is a point the SCons developers will have to decide. 


### Python 3.0 Compatibility

Python 3.0 introduced several changes that are incompatible with earlier versions. One of these is the restructuring of TkInter. Therefore, SCons' 'compat' module will have to be expanded to hide the differences between TkInter 2.X and 3.X . 


### External Tools
[[!table header="no" class="mointable" data="""
 [PyInstaller](http://www.pyinstaller.org/)      |  Creates self-contained executables from Python applications 
 [WiX](http://wix.sourceforge.net/)              |  Open source Windows installer creation system               
 [NSIS](http://nsis.sourceforge.net/Main_Page)   |  Another installer creation system                           
 [Inno Setup](http://www.jrsoftware.org/isinfo.php)  |  Yet another installer creation system 
 [TkInter](http://wiki.python.org/moin/TkInter)  |  One of the most 'widely used' GUI toolkits for Python       
"""]]


### References
[[!table header="no" class="mointable" data="""
 [CrystalSpace](http://www.crystalspace3d.org)  |  3D Toolkit that includes some Python scripts to create WiX installers ([SVN repository](http://crystal.svn.sourceforge.net/viewvc/crystal/CS/trunk/scripts/msi/)) 
"""]]


### Plan

This project consists of three major phases: Stand-alone SCons, improved installer, and front-end.  


#### Phase 1: Stand-alone SCons

At first, I will concentrate on PyInstaller, how to use it, how to build simple programs, and how to use it to package SCons. This will involve finding out if it is sufficient to just wrap the 'scons' script and the 'SCons' module, or if there are additional steps to be taken. Another important aspect is determining all components that need to be deployed on a vanilla Windows installation in order to run SCons. 

Once this is accomplished, I will test the executable on different versions of Windows with and without Python installations. The test systems will be [VirtualBox](http://www.virtualbox.org/) virtual machines which are quite time-consuming to set up, so the extent of these tests will have to be discussed with my mentor. 

In addition to this, the end-to-end test suite will have to be adapted to run all possible tests using this stand-alone executable as a black-box. These tests will ensure that there is no difference in functionality between this version and the Python installation-based one. 

During this phase, I will also create documentation detailing how to build the executable by starting from a checkout of the SCons source code. 


#### Phase 2: Improved installer

During the second phase, I will create an installer that fulfills all of the requirements listed in the analysis section. This builds on the first phase and will involve deciding whether to use WiX, Inno Setup, or NSIS, creating a feature checklist for the installer, and actually implementing those features. If time permits, I would also like to convert the HTML help files into a single .chm file and include that with the installer. 

Besides creating the actual installer, I will also add the necessary builder(s) for the installer to SCons, so that it can be created during the usual release preparations. NSIS can cross-build installers from Linux, but if another installer toolkit is selected, further research will show whether building the installer will have to be done on windows.  

Again, the finished installer will be tested on a variety of platforms. Special attention will be needed on Vista to ensure smooth cooperation with UAC. 

I will also write a detailed test guide for the installation process and the functionality of the installer itself. If possible, this guide will be used to create automated tests to be run without supervision. The installer should include 'quiet' installation and uninstallation options; these will be easiest to test. Automated tests can run the installer in this mode and check whether it performs the expected actions such as adding files or adjusting environment variables. The graphical mode, however, will most likely have to be tested manually. 

Another issue to be aware of is finding the correct, locale-dependent default locations for different aspects of Windows, including the start menu folder, shell registry keys, and more. Regardless of whether automated or manual tests are performed, the machines used in testing have to offer a variety of Windows versions and locales. 

A decision needs to be made about whether to officially support installation on Windows via setup.py, or if this should be reduced to an engine-only installation that directs the user to the downloadable installer for all other features. 


#### Phase 3: The front-end

The final phase involves the creation of a GUI front-end for SCons. At first, this will be a simple window with two text entry controls that specify the command line arguments for SCons and the directory to run SCons in. Further iterations will include an easy way to specify options such as '--verbose' by checking checkboxes, a name-value-pair editor, synchronization between the convenience controls and the text form of the command line, integration of the SCons helpfile, and possibly a list of all targets available in a build directory by parsing the SConscripts. 

Testing this front-end will prove difficult. At the moment, I can see the following options: 

* Run (and interact with) a virtual X11 server to test the application on 
* Recreate TkInter as a mock module 
* Separate the GUI from the actual functionality as possible, only perform automated tests on the latter part, and conduct code reviews to ensure the correctness of the GUI part 
* Require access to a screen in order to be able to run the tests 
Once the GUI is sufficiently mature (directory selection, command line, options selector, name-value-editor), it will be included in the installer. 


#### Additional tasks

In case there is some time left at the end of the programme, I'd like to work on some smaller bugs in order to get to know the SCons codebase better. One possible candidate would be issue 2351 (_"ENV" execution environment not case-insensitive on Windows_). 


#### Polishing and open questions

* Provide translations for the installer and the context menu entries 
* Provide translations for the GUI 
* Investigate side-by-side installation of different versions of SCons 
* Provide per-directory-persistence for the options selected inside the GUI 
* What version of Python should be used to build the self-contained executable? 

## Scope of Work


### Priorities
[[!table header="no" class="mointable" data="""
 P1  |  high                                       
 P2  |  normal                                     
 P3  |  low (_i.e._, after SoC)                  
 P4  |  secondary tasks in case the project stalls 
"""]]


### Deliverables

* P1 Automatable Tests for every new or changed functionality 
      * P1 Test the stand-alone executable to make sure there is no functional difference to the Python-installation based version of SCons 
      * P1 Test the creation of the installer 
      * P2 Test the actual functionality of the (un-)installer 
      * P1 Test the core functionality of the front-end 
      * P2 Test the GUI layer of the front-end 
      * P1 Test the updated SCons build script 
* P1 A single executable (or directory) that can be used to run SCons 
* P3 SCons documentation in .chm format 
* P1 An installer that can be used to 
      * P1 install the stand-alone Scons 
      * P1 add it to the %PATH% 
      * P2 install the HTML documentation 
      * P3 install the .chm documentation 
      * P2 add context menu options 
      * P1 install the GUI front-end 
      * P3 detect and support side-by-side installation of multiple SCons versions 
      * P2 make the SCons engine available to local Python installations 
* P1 A GUI program that allows to specify the directory and command line arguments for SCons 
      * P2 allow easy selection of options 
      * P2 provide a name-value-pair editor 
      * P3 list all possible build targets inside a directory 
      * P3 store the selected options per directory 
      * P3 allow the selection of a specific SCons version if more than one is installed 
* P1 An updated SCons build script to create and distribute the new installer 
* P1 New or improved SCons builders needed by the build script 
* P2 A localized version of the installer 
* P2/P3 A localized version of the front-end 
* P1 Documentation, including 
      * a description of the tools and techniques used to create the stand-alone SCons executable 
      * how the SCons build script was changed 
      * a description of the tools and techniques used to create the installer 
      * a list of issues that came up during SoC and couldn't be addressed yet 
      * weekly updates on the project's progress, posted to [dev@scons.tigris.org](mailto:dev@scons.tigris.org) 
      * a development log, detailing problems and design choices 
* P4 A bugfix for issue 2351 
[Task list](GSoC2009/LukasErlinghagen/TaskList) 


### Schedule


#### Community Bonding Period

* Set up PyInstaller, WiX, NSIS, VirtualBox 
* Create several VMs to be used for testing 
* Discuss project details on the development list 
* Have a go at fixing some 'Easy' bugs 
* Write a detailed list of tasks and publish it on the wiki 
* If it is acceptable for Google and/or the mentor(s): start working on implementing the proposal before 2009-05-23 

#### Week 1 (2009-05-23 - 2009-05-29)

* Build a stand-alone SCons executable 
* Write documentation detailing the build process 
* Update the SCons build script 
* Add or update necessary builders 
* Test the stand-alone executable on different versions of Windows 
* Adapt the automated end-to-end test suite to use the stand-alone executable 

#### Week 2 (2009-05-30 - 2009-06-05)

* Further testing of the executable 
* Finalize the feature list for the installer 
* Evaluate the installer toolkits (WiX, NSIS) 
* See Availability 

#### Week 3 (2009-06-06 - 2009-06-12)

* Create the initial installer 
* Test installation and uninstallation on different versions of Windows 
* Update the SCons build script 
* Add or update necessary builders 
* Run a test release procedure 

#### Week 4 (2009-06-13 - 2009-06-19)

* Convert the HTML help files to the .chm format 
* Update the SCons build script 
* Add or update necessary builders 
* Buffer time to compensate for delays during the previous weeks 

#### Week 5 (2009-06-20 - 2009-06-26)

* Get up to speed with TkInter 
* Create the basic front-end 
* Create a stand-alone executable using PyInstaller 
* Integrate it into the installer 
* See Availability 

#### Week 6 (2009-06-27 - 2009-07-03)

* Add command line option selection to the installer 
* Provide synchronization between the option selection and the command line text 
* See Availability 

#### Week 7 (2009-07-04 - 2009-07-10)

* Add name-value-editing and synchronization 
* Integrate the updated front-end into the installer 
* Provide a drop-down-selection of common build targets 

#### Week 8 (2009-07-11 - 2009-07-17)

* Integrate the help file with the front-end 
* Integrate the updated front-end into the installer 
* Add localization to the installer 

#### Week 9 (2009-07-18 - 2009-07-24)

* Add localization to the front-end 
* Buffer time to compensate for delays during the previous weeks 
* Polishing 

#### Week 10 (2009-07-25 - 2009-07-31)

* Buffer time to compensate for delays during the previous weeks 
* Final polishing and testing of the installer package 

#### Week 11 (2009-08-01 - 2009-08-07)

* Bug fixing? 
* Start on adding localization to SCons itself? 

#### Week 12 (2009-08-08 - 2009-08-14)

* Bug fixing? 
* Start on adding localization to SCons itself? 

## Availability

I plan on attending some courses at university during the summer, so I will most likely do the majority of the work during the afternoons and weekends. In addition to that, I will be doing the lighting design and run the lightshow at a charity event taking place from 2009-06-03 to 2009-06-05. There is a big summer festival at my university where I will be helping, so I will be unavailable from 2009-06-26 to 2009-06-28. 

I also plan to attend the Leo Europe Forum (LEF) in Italy starting 2009-08-15, so my suggestion for the 'pencils down' date is 2009-08-12. 

To compensate for this, I'd like to start implementing the proposal during the community bonding period, as long as that is acceptable for Google and/or the mentor(s). 


## Biography

My Name is Lukas Erlinghagen. I'm studying Electronics Engineering in my tenth semester at the University of Karlsruhe, which will transform into the Karlsruhe Institute of Technology ([KIT](http://www.kit.edu)) some time during 2009. My specialization is hardware-software-co-design and system-on-chip technology, and I plan to finish my diploma around May 2010. 

Up until now, I have only used Python to write some small utility scripts, but I have attended several lectures on software engineering and worked on several object-oriented-design-driven research projects, including implementing the physical layer of a digital television broadcasting system on a reconfigurable hardware platform. I usually program in C++ and C#. Working on a larger Python project won't be a problem, since I'm familiar with the underlying programming concepts, so picking up language details during the project won't be a problem. 

I'm currently looking for a cross-platform build system that supports MSVC project file generation for a project of my students' council, and that is why SCons caught my attention. Since I have no experience using SCons, I chose to submit this project proposal, which doesn't require in-depth knowledge of SCons' architecture but is still useful to the SCons community (and, ultimately, myself). 

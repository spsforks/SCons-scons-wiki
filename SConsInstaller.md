

# SCons Binary and Installer


## Historical Background

SCons is written in Python and basically it is a set of Python scripts or modules that are gathered into main SCons package and one entrypoint scons.bat file placed elsewhere. <span style="display:none">insert linux term here</span> SCons versions prior and including 1.3.x were distributed as a Python package. Package required that Python is preinstalled, it was installed by Python and into Python library (site-packages/ dir on Windows). Bootstrap scons.bat file was added into shared Python /Scripts directory that was not available from %PATH% by default. This was acceptable in times of expensive bandwidth and slow speeds, because otherwise SCons would need to bundle Python with itself. 

Disadvantages of installation into Python library: 

* when Python is removed, SCons stops to work 
         * _I usually do full cleanup on major Python upgrade_ -- [techtonik](techtonik) 2010-05-05 22:06:22 
* when default version of Python is changed, SCons stops to work (this was fixed in recent scons.bat) 
* when shared /Scripts directory with scons.bat is added to %PATH%, all other scripts are also added there 
* scons.bat is not added to %PATH% 
* people don't usually read docs to know all above 
* people couldn't just download,install and run 'scons' 
Advantages of this approach: 

* easy pythonic installation 
      * **python -m easy_install** 
* easy pythonic execution 
      * **python -m scons** (this never worked) 
So a standalone installer with scons.exe that is automatically added to %PATH%, with shortcuts in Start Menu and Documentation shortcuts would be highly appreciated by everybody. Luckily [Lukas Erlinghagen](GSoC2009/LukasErlinghagen) stepped in as a student in GSoC 2009 program to implement this project. 

A note of warning about plugins though. New [PluginArchitecture](PluginArchitecture) will make it possible to extend SCons functionality when SCons is already installed, by specifying extensions directory with some command line/configuration parameter. _scons.exe_ should be able to discover plugins from this directory. It will be self-sufficient executable (aka Frozen) independent on PYTHONPATH. Therefore it will be unable to discover/import plugins installed system wide. Another common problem (for example, with frozen Mercurial 1.5) is that it imports extensions implicitly and when extension requires another import in a directory relative to extension itself - the import fails. Might be no issue for SCons, but still requires investigating. 


## GSoC Installer

During Google's Summer of Code 2009, a binary version of SCons for windows was created. It can currently be found in the 'installer' svn branch. 

The installer comes in two versions: a binary-only installer which only includes the stand-alone (i.e.: not dependant on a Python installation) executables for SCons and SConsign, and the full installer, which additionally offers Documentation, the older installer for SCons' Python modules and scripts, and a copy of the 'local' version of SCons, which can be shipped with projects that use SCons as their build system. 


## Differences between binary & script, branch & trunk

The binary is a fully functional version of SCons. Nonetheless, there have been some changes that all users of the binary should be aware of: 

* sys.executable won't neccessarily refer to a Python interpreter. SCons.Util.python_interpreter_command() has been added to compensate; it returns the path to a Python interpreter if one is available 
* The optional 'scons_executable' parameter has been added to the MSVSProject builder. Project files generated with this version of SCons will default to calling 'scons' instead of Python for building. This parameter can be used to override the command (i.e.: provide a full path or the older Python invocation). 
* By default, the SCons binary will only search its own directory and the library.zip file therein. If your build scripts rely on additional Python modules, make sure you've set your PYTHONPATH environment variable accordingly. 
* Currently, the binary includes a Python 2.6.2 interpreter. If your build scripts must use a different version, you should install SCons' Python modules that version and use the SCons batch file in the 'Scripts' subdirectory of that Python installation. 
* The uninstaller will not remove the Python scripts and modules. Instead, use the Control Panel to uninstall; the uninstaller will be called 'Python x.x SCons'. 

## Features

* Binary-only installer 
      * Stand-alone SCons binary 
      * Add the binary to the path 
      * Uninstaller 
      * L10n support (Current languages: English, German) 
      * Supports per-user and per-machine installations 
* Full installer 
      * Stand-alone SCons binary 
      * Add the binary to the path 
      * Documentation in HTML and PDF format 
      * A zipped copy of the SCons code (local version, to be distributed alongside projects that use SCons for building) 
      * Includes the installer for the Python modules 
      * Uninstaller 
      * L10n support (Current languages: English, German) 
      * Supports per-user and per-machine installations 

## Building the Binary and Installer

The binary-only installer can be built on both Windows and Linux, but the full installer can only be built on Linux. 


### Prerequisites

* A checkout of the 'installer' branch ([http://scons.tigris.org/svn/scons/branches/installer](http://scons.tigris.org/svn/scons/branches/installer)) 
* On Windows: 
      * Python 2.4 or later 
      * Python Win32 extensions (as an alternative, you can install ActiveState's ActivePython, which already includes these) 
      * cx_Freeze ([http://cx-freeze.sourceforge.net/](http://cx-freeze.sourceforge.net/)) 
      * A recent version of NSIS ([http://nsis.sourceforge.net/](http://nsis.sourceforge.net/)) 
* On Linux: 
      * A toolchain that can build SCons as well as the documentation 
      * Wine 
            * Python 2.4 or later, installed via Wine 
            * If your Wine installation of Python cannot find msvcr90.dll, copy that file and the manifest from the 'installer' subdirectory of your checkout to Python's installation directory (usually $HOME/.wine/drive_c/Pythonxx/) 
            * Python Win32 extensions for Wine-Python 
            * cx_Freeze for Wine-Python 
      * A recent version of NSIS 

### Building

Once you meet all the prerequisites, just run 'python bootstrap.py'. If there are no errors during the build, you will find the binary (and, if you are on Linux, the full) installer in 'build/dist'. Note that at the moment, you cannot use other versions of SCons for building since they don't include SCons.Util.python_interpreter_command() yet. 

You can change the Wine environment used for building by setting the WINE_PREFIX environment variable accordingly. 


## Behind the scenes


### The stand-alone binary

There are several tools to convert a Python application into a stand-alone executable. Among the most popular are py2exe, cxFreeze, and PyInstaller, which were chosen as candidates for the SCons binary. Py2exe and cxFreeze extend distutils, while PyInstaller is a set of scripts independent of distutils. 

Even though PyInstaller is the only tool that provides support for cross-building a Windows executable on a Linux system, and the only tool to support Mac binaries, it was not chosen for three reasons: 

1. The cross-platform support is only in the subversion repository, but there hasn't been a stable release for quite some time. 
1. Configuration of both the tool and a specific build are more complicated than with a distutils-based tool. 
1. In order to cross-build from Linux, PyInstaller needs access to a partition containing an installation of Windows. In order to enable people without a Windows license to build the executables, a Wine-based approach was used instead. 
Once a new, stable release of PyInstaller is available, it might be advisable to reconsider it for building the binary. The branch's SConstruct file contains an example of how to build the SCons binary with PyInstaller. 

Of the other two tools, cxFreeze was chosen for its ability to build a stand-alone Linux binary in addition to the Windows support, which was one of the possible future ideas on the Summer of Code ideas page. 

In order to combine both the documentation and the binaries into one installer, there has to be a way to build the binaries on Linux, since the documentation cannot be built on Windows. Installing Python and cxFreeze via Wine creates a Windows-like environment on Linux machines that can be used for this task. Since Wine doesn't implement the ImageHlp:BindImageEx Win32 API function, the binary dependencies of the SCons binaries have to be included explicitly by the build script. This is accomplished by the wine_sanity_check function in the SConstruct file. 


### The installer

There are several open-source installer generators for Windows, such as !WiX, InnoSetup, and NSIS. However, only NSIS is available for Linux, so it was selected for this project. It has out-of-the-box support for multiple languages, multi-user and unprivileged installations, registry access, and an auto-generated uninstaller. It can also be extended using plugins such as this [Python plugin](http://nsis.sourceforge.net/NsPython_plug-in). 

In order to integrate the installer creation into the build process, the NSIS builder from this wiki was modified and added to SCons. Several tests have been added for it as well. 


### The build process

1. The build script checks whether all necessary tools are available: 
      1. On Windows, it checks whether there is a Python interpreter, and whether the interpreter has the cxFreeze module. 
      1. On Linux, it checks for Wine, a Wine-Python installation, and whether that Python installation has the cxFreeze module. 
      1. Finally, the script checks whether the NSIS tool is available in the SCons environment. 
1. The binary is then built by running a copy of the standard SCons setup.py script, modified for cxFreeze. 
      1. The Python interpreter found in 1a or 1b is used to run the modified setup.py script. 
      1. A sanity check is run on the output directory to make sure all binary dependencies of the stand-alone executables are available. This is needed since cxFreeze doesn't pick them up on Wine. 
      1. The output directory is scanned to insert all output files of steps 2a and 2b into SCon's dependency graph. Since not all output files are known beforehand, this scanning has to take place after the binaries have been built, so a special builder was created for this step.. 
1. The binary-only installer is built: 
      1. A Substfile builder creates the input file for makensis from a template file. It substitutes the package name, version, license, and the lists of files to install or uninstall. Those lists are created by special scanning functions that use env.Glob() to find all needed files, using the extended dependency graph of step 2c 
      1. The NSISInstaller builder is run to build the actual installer. Since its input file doesn't always exist at the time the SConscript file is read, the automatic target detection of the builder's emitter cannot be used. A default name is therefore assumed for the installer. 
      1. As a final step, the installer is copied to the 'dist' directory under its desired name. 
1. To build the full installer, the build script first checks whether the wrapper script for jadetex is available. If it is, the build script assumes that the documentation can be (and has been) built. 
      1. The documentation build directory is scanned, similar to step 2c. 
      1. Another makensis input file is created by a Substfile builder. In addition to the options of the binary-only installer, it also has file lists for the documentation, the scons-local zip file, and the Python module installer. These lists are created similar to step 3a. 
      1. The installer is created by the NSISInstaller builder. 
      1. Finally, the installer is copied to the 'dist' directory under its desired name. 
More details can be found in the source code itself: The main SConstruct file, starting around line 1200, and the contents of the 'installer' directory. 

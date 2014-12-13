

# GSoC 2009: SCons on Windows - Task List


## Test systems

* Set up virtual machines to run tests on 
      * <del>Windows XP, Python 1.5.2 (oldest supported version)</del>  
      * <del>Windows XP, Python 2.1 (oldest supported version for python2-scons, according to setup.py)</del> 
      * <del>Windows XP, Python 2.6.2 (current release of Python 2)</del> 
      * <del>Windows XP, Python 3.0.1 (current release of Python 3)</del> 
      * <del>Windows XP, ActiveState ActivePython 2.6.2 (current release of ActivePython 2, to see if there are any differences between this version and python.org's Python)</del> 
      * <del>Windows Vista, restricted user (to test local installations)</del> 
      * <del>Windows Vista, admin (to test global installations)</del> 
      * <del>Windows XP, admin (to test global installations on a system without UAC)</del> 

## Stand-alone executable

* <del>Research available tools to convert python programs to stand-alone entities</del> 
      * <del>[py2exe](http://www.py2exe.org/)</del> 
      * <del>[pyinstaller](http://www.pyinstaller.org/)</del> 
      * <del>[Python's freeze](http://svn.python.org/view/python/trunk/Tools/freeze/)</del> 
      * <del>[cx_freeze](http://cx-freeze.sourceforge.net/index.html)</del> 
      * <del>[Squeeze](http://www.effbot.org/zone/squeeze.htm)</del> 
* <del>Select one of these tools</del> 
      * <del>Is cross-building (build Windows .exe on Linux) available?</del> 
      * <del>Is it wine-compatible?</del> 
      * <del>How does it deal with Tcl/Tk/TkInter?</del> 
      * cx_Freeze was chosen 
* <del>Document the alternatives, the choice, and why it was made</del> 
      * [http://scons.org/wiki/SConsInstaller](http://scons.org/wiki/SConsInstaller) 
* <del>Manually create a stand-alone SCons</del> 
      * <del>Generate input files for the converter</del> 
* <del>Document the method to produce the input file(s)</del> 
      * No real input file, just a stripped-down setup.py 
* <del>Run the end-to-end tests using that manually created SCons</del> 
* <del>Integrate the stand-alone exe creation into the build script</del> 
      * <del>Converter input files</del> 
      * <del>Actually building the exe</del> 
      * <del>Write a Builder?</del> 
      * Building the executables is a simple distutils command 
* <del>Document necessary changes/additions</del> 
      * The relevant code in the SConstruct file starts around line 1200 
* <del>Research building on Linux</del> 
      * <del>Cross-building via one of the tools mentioned above?</del> 
      * <del>Use Wine?</del> 
      * cx_Freeze via Wine 
* Document the requirements for building on Linux 
      * [http://scons.org/wiki/SConsInstaller](http://scons.org/wiki/SConsInstaller) 

## Better installer

* Features: 
      1. Select features to install 
            1. <del>SCons stand-alone</del> 
            1. <del>SCons engine (into Python's site-packages)</del> Uses the standard Python installer 
            1. <del>Documentation</del> 
            1. <del>Frontend</del> 
            1. <del>Add SCons to the path</del> 
            1. <del>Set the $SCONS environment variable</del> 
            1. <del>Integrate the frontend into Explorer's context menus</del> 
      1. <del>Works correctly with [UAC](http://msdn.microsoft.com/en-us/library/bb756973.aspx)</del> 
      1. <del>Detects insufficient write privileges</del> 
      1. <del>Uninstaller</del> 
      1. <del>Localized user interface</del> 
* <del>Research installer creation tools</del> 
      * <del>[NSIS](http://nsis.sourceforge.net/Main_Page)</del> 
      * <del>[InnoSetup](http://www.jrsoftware.org/isinfo.php)</del> 
      * <del>[WiX](http://wix.sourceforge.net/)</del> 
* <del>Select one of those tools</del> 
      * <del>Cross-build capability?</del> 
      * <del>Support for extensions/scripts?</del> 
      * NSIS was chosen since it is the only option available on Linux 
* <del>Document the alternatives, the choice, and why it was made</del> 
* <del>Manually build an installer, containing features 1.1, 1.5, 1.6, 2, 3, 4</del> 
* <del>Document the method</del> 
* <del>Create/update a Builder for the selected installer tool</del> 
      * Updated NSIS builder from the wiki 
* <del>Integrate installer creation into the build script</del> 
* Document necessary changes/additions 
* <del>Convert the manual to .chm</del> This feature has been dropped 
* <del>Create/update a .chm Builder</del> This feature has been dropped 
   * <del>Document necessary changes/additions</del> 
* <del>Integrate the manual into the installer</del> 
* <del>Perform test installs (Tools: [FileMon](http://technet.microsoft.com/de-de/sysinternals/bb896642.aspx), [RegMon](http://technet.microsoft.com/de-de/sysinternals/bb896652.aspx), [Process Monitor](http://technet.microsoft.com/de-de/sysinternals/bb896645.aspx))</del> 
* Document the expected actions of the installer 

## GUI Front-end

* Research different ways to test [TkInter](TkInter) programs when no display is available 
      * xvfb? 
      * Mock version of [TkInter](TkInter)? 
      * Test cases that have to be executed by human testers? 
* Create a test application that changes a text label when a button is clicked 
* Set up the testing infrastructure for that application 
* Document the testing methods 
* <del>Create the first version of the front-end</del> 
      * <del>Text box to specify a working directory for SCons</del> 
      * <del>Text box to specify command line arguments for SCons</del> 
      * <del>An output window that captures all output by SCons</del> 
* Create tests for this version 
      * Window creation testing is in place, headless testing is still missing 
* <del>Build a stand-alone application</del> 
* <del>Integrate the front-end into the Windows Explorer as a context menu entry for directories</del> 
* <del>Add the basic front-end to the installer</del> 
* Extend the front-end 
      * <del>Add a way to specify name-value pairs on the command line</del> 
      * <del>Bi-directional transfer between the command line string and user interface elements</del> Has been changed to "option selection -> command line string" 
      * <del>Add a way to access SCons command line options</del> 
      * If possible, integrate the user manual to provide context help 
      * If time permits, add a module that parses SConstruct files and lets the user select targets to be built 
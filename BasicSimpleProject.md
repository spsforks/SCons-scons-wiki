
My goal was to convert the Gambit system to build with SCons instead of the configure/make dance.  The main reason for walking down this path is that the autotools system handles cross-compiling very poorly, and I eventually want to port Gambit to an embedded system. 

My main problem: the SCons documentation is weak.  It's more of a reference manual than a user manual.  It needs lots more full examples that aren't hugely complicated.  That's why I actually took the time to write this page.  Since I don't know SCons that well, I can't fix the main documentation to make it better.  However, I can provide an example for other new people to follow as well as some of my thinking and issues. 

The lack of discoverability in SCons is a real issue.  SCons probably does *what* you want; figuring out *how* to get SCons to do it is an adventure.  Don't waste a lot of time diving into the SCons code; it has been abstracted enough that the multiple layers of indirection make it too opaque.  Search the mailing list, first.  Then, ask the mailing list if you are still stumped. 

Things that I found surprising.  Bear in mind that these are likely to be failures of understanding, not failures of SCons: 

* Source files cannot have dependencies 
   * I'm not sure if I consider this a limitation which needs to be remedied or not. I'll probably wait until I understand how to write a Scanner before passing judgment on this. 
* The "single_source" keyword on Builder 
   * This is *huge*.  Really.  Anytime you put together a Builder, you really need to think about what the value should be.  It's description in any of the documentation does not highlight its importance. 
* Subsidiary SConscripts 
   * SCons is really tied to the idea of having subsidiary SConscript files.  Don't try to fight it.  I originally wanted everything in one SConstruct, but the build_dir functionality will fight you if you try to do this. 
* Need to use SCons.Util to break apart suffixes and base names for Entry 
   * I'm surprised that the Entry itself isn't just keeping these in its own dictionary.  Having to disassemble and reassemble strings is error prone and limiting.  Specifically, it means that suffixes *must* use a "." separator.  I got bitten when I wanted a suffix of "_.c" and then later got a suffix of ".c" from that file. 
* Use generated targets and variables as much as possible and avoid strings 
   * While it may be convenient to Depends("foo.o", "somedependency.h") for "foo.c" rather than "fooTarget = Object("foo.c"); Depends(fooTarget, "somedep.h")", don't do it.  Use the reference.  You'll thank yourself later. 
The Files (Discussion included on the page itself): 

* [SConstruct](APLSConstruct01-top) (top-level) -- Most of the magic occurs here 
* [SConscript](APLSConscript01-lib) (lib subdirectory) -- Compiles the main Gambit library 
* [SConscript](APLSConscript01-gsi) (gsi subdirectory) -- Compiles the interpreter executable 
* [SConscript](APLSConscript01-gsc) (gsc subdirectory) -- Compiles the compiler executable 
* [Full Build Log](APLBuildLog01) (for completeness) 
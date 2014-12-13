## What we need for proper Tool support:
- A common module for detecting, storing and retrieving infos about the current host architecture, processor type and OS (this would be the [PlatformInfo](PlatformInfo) the platform, the CPU, the vendor, the kernel, and the OS). It should be used throughout the whole source tree, including the test framework and the tests themselves. - Introduce Toolchains, as an abstraction for a series (=list) of tools that should get initialized by a single keyword. It should be possible to: 
* Check whether we can load/use a toolchain or single tool in our current environment (as given by os.environ['PATH']) 
* Check whether we can load/use a toolchain or single tool in a special environment. 
* Get a list of possible toolchains for a "Tooltopic" (can't think of another name right now). A "Tooltopic" would be "C++", and possible toolchains include "mingw" and "msvs". This selection would depend on the [PlatformInfo](PlatformInfo). 
* Get a default toolchain for a topic, that is actually installed in the current system. 
* Dynamically add new toolchains. 
* Dynamically add new tools to a toolchain. 
* Dynamically change the preferred order in which toolchains are tried. 
* Should provide an easy way to statically add new Toolchains, that contain parameterized versions of existing tools, e.g. a      "cxx-embedded" for a cross-compiling gcc that requires special options. 
* Single Tool support should work as before. 
* Provide infos about what would be selected, if...right now. 
TODO: Talk about cross-compile support here 


## For the support of external tools we need:

* a way to install a Tool in the local SCons distribution 
* a way to deinstall it 
* SCons should be able to display (--version) that there are external tools installed and, on request (--list-external) which Tools exactly (and in which version!) 
* Single tools should support a version string 
* Would be nice if we could add a way to simply download and install a SCons external module (like via EGGs, or somethin') 

## For the support of tools in general:

* An easy way to check from a SConstruct/SConscript whether a Tool (internal or external) is installed on the current system. 
* Like above, but here we check whether the Tool could actually be called (all prerequisites, in the form of executables, additional modules, whatever...are met). 

## As found on the PlatformToolConfig page:

(Comment: As I was writing this page, I found myself flipping back and forth as to whether a Tool module configured a tool (that is, a single command) or a toolchain (that is, a series of commands). The current Tool modules actually implement toolchains (e.g., the gcc.py module provides the environment variables for the compiler, the linker, the static archiver, the shared archiver, and the bundle archiver). This isn't good modularization, which suggests that there should be a higher-level module explicitly for toolchains that can invoke one or more tool modules as building blocks. That isn't in this proposal (should it be?), but it's something that should be kept in mind for the future.) 

Since we try to provide a framework for build systems, our Tool shouldn't care. Both should be possible ways for a user to extend the build engine. A Tool can be used to change an existing Environment, for example by decorating it with custom Builders. 

The question is though: How do we want our Tools to be organized for the standard SCons implementation? Especially, when we have a Tool like "latex" that basically looks the same for all distributions (miktex, texlive, ...) in terms of command calls. Do we want a "miktex" Tool under the covers, that gets automatically selected by the "latex" Toolchain? Should there be a [LatexCommon](LatexCommon).py in cases like this? And how do we go about tests for these toolchains? 

Is a Tool ultimately responsible for detecting paths to possible alternatives of executables? Idea: 

   * Tool can return a list of paths, that can be used to realize a given "toolchain" link...while doing so it should access infos from the [PlatformInfo](PlatformInfo). 
Problem: How to synchronize toolchain names between SCons and the Tools? Probably best, that SCons doesn't keep a list of them...but can request the list of ids this Tool realizes, from the Tool package itself. 

Probably handled as another SEP: Extending the build system such that a Tool (=Builder) can decide to run all (or only some) commands (=Actions) locally!!! 

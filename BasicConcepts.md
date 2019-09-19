**Construction Environment** - when SCons starts building the project, it creates its own environment with dependency trees, helper functions, builders and other stuff. The SCons environment is created in memory and some parts of it are saved to disk to speed up things on the next start. It is often referred to as just **Environment**, which can be a little confusing as there many things in computing called environment (see especially *System Environment*).

**System Environment** - is a familiar operating system container with [environment variables](http://en.wikipedia.org/wiki/Environment_variable "Wikipedia article") such as `PATH`, `HOME` etc. It is accessible via the `os.environ` mapping in Python and therefore in SCons too. SCons doesn't import any settings from _System Environment_ (like flags for compilers, or paths for tools) implicitly, because it's designed to be a crossplatform tool with predictable/repeatable behavior. That's why if you rely on any system `PATH` or environment variables you need to extract those in your *SConscript*s explicitly.

**SConstruct** - the default name of the main build configuration script SCons will execute to process the build. Even if given a different name and invoked as `scons -f scriptname` it will still be referred to as the _sconstruct_ in conversation.

**SConscript** - default name for additional SCons configuration scripts, usually placed in subdirectories of the project. They are used to help organize hierarchical builds. Need to be included in the build explicitly (for example by calling the `SConscript` method).  Generically, the entire collection of build scripts will often be referred to as "the sconscripts" even if other names are used (the term tends to include the sconstruct as well).

**Builder** - an SCons object that you explicitly call from the sconscript to tell SCons the relationship between a set of sources and a build target. The power of SCons is in the fact that dependencies are tracked automatically. When source files change, the system automatically detects which targets should be rebuilt.

**Action**: Actions are callable objects that do something (execute an external command or call a python function, for instance). A Builder retains a list of Actions needed to update its target; those Actions are run when needed.

**Node**: a Node normally represents a filesystem object such as a file or directory. Nodes form the nodes of the dependency graph; the arcs, which represent dependencies, are created by using Builders. There are also Alias nodes and Value nodes which represent SCons Aliases and a string value, respectively.

**Scanner** - Scanner objects are used to scan source files for additional dependencies referenced inside a file (for instance, identifying a file included by a C preprocessor `#include` statement), but not passed as sources to a Builder.

**Tool** - is any external component that adds Builders, Scanners and other helpers to SCons environments for use within scripts. SCons scans several locations to find tools - there can be project-specific or installation-specific add-ons for extending core functionality.
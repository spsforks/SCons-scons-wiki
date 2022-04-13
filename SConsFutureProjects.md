

<div>
****VERY PRELIMINARY; MOSTLY ONLY HAS TOPIC TITLES; NEEDS TO BE FILLED IN.**** 

****_REWORD THIS SECTION!_**** 

****These are projects that the SCons team would like to do that are larger than a bugfix.  Presence on this page is not a commitment that the project will be done, nor does the ordering imply any sense of priority.  For that information, see the [Roadmap](Roadmap) page.**** 

****This page is only a list of projects and a brief description (with links to more information, if any).  Debates about what does (and does not) belong in this page should go in the [discussion page](SConsFutureProjects/Discussion).**** 
</div>
[[!toc 1]] 



---

 <a name="subst"></a> 
# subst

Steven has posted some information on what he wants to do; it should be referenced here.  For an alternative formulation that involves compiling environment variables, see [SubstQuoteEscapeCache](SubstQuoteEscapeCache). 



---

 <a name="node_hierarchy"></a> 
# Refactor node hierarchy

Convert the Node hierarchy to use composition instead of inheritance. 



---

 <a name="iapat"></a> 
# IAPAT framework

See [PlatformToolConfig](PlatformToolConfig) 
## IAPAT initialization

Set up platform and other one-time stuff. 
## Cross-compile

Set up IAPAT for cross-compile if targeted platform is not same as build host. 



---

 <a name="iapat_config"></a> 
# IAPAT-based configure

See [PlatformToolConfig](PlatformToolConfig) 
## Command-line options

Some replacement for Add``Option() moves here. 
## Command-line variables

Functionality of Variables() moves here. 
## Probes of platform information

Functionality of configure contexts moves here. 
## Create header files

Replacement for the `config_h` configuration parameter moves here. 



---

 <a name="toolchain"></a> 
# Toolchain

Modifies IAPAT so Environments created from it have specified set of tools. 



---

 <a name="subprocess"></a> 
# Convert (P)SPAWN to subprocess

Replace the deprecated `spawn` functions with the `subprocess` module, hopefully eliminating the `SPAWN` and `PSPAWN` environment variables at the same time. 



---

 <a name="tng"></a> 
# Taskmaster next generation

Rewrite the ad-hoc bottom-up evaluation driven by the Jobs module to be a top-down topological sort that drives the Jobs module. 



---

 <a name="componentization"></a> 
# componentization model / Parts integration



---

 <a name="test_as_dir"></a> 
# tests as dirs + expose test strings + unittest

Setting up and editing tests for the core functionalities and Tools can get tedious. File contents and the file/folder structure have to be hard-coded in the test script itself. As discussed on the [SConsTestingRevisions](http://scons.org/wiki/SConsTestingRevisions) page, the framework should provide "fixtures" for files and complete folders and also have less dependencies on the SCons core in general. The latter is important for the support of external Tools (see [ToolsIndex](ToolsIndex)), a first draft exists at [https://code.launchpad.net/~dl9obn/sconsaddons/scons-test-framework](https://code.launchpad.net/~dl9obn/sconsaddons/scons-test-framework). 



---

 <a name="tools_as_plugins"></a> 
# take many tools out of scons core, make them plug-ins

Shift some of the core Tools out, by making them external plug-ins (see [ToolsIndex](ToolsIndex)). The critical part of this work will probably be the decision about which Tools should comprise the Core...and which do not. 



---

 <a name="Help"></a> 
# refactor Help()

The =Help()= function is too coarse. Any call overwrites the local options added via the `AddOption()` function. The `AddOption()` function itself doesn't support grouping options. You can't get help about local options unless you read all the `SConscript` files. The whole thing needs a refactoring to address more sophisticated, modern needs. 



# SConsolidator

SConsolidator provides tool integration for SCons in Eclipse for a convenient C/C++ development experience. Its main features are: 

* Convertion of existing CDT managed build projects to SCons projects 
* Import of existing SCons projects into Eclipse with wizard support 
* Interactive mode to quickly build single source files speeding up round trip times 
* A special view for a convenient build target management of all workspace projects 
* Graph visualization of build dependencies with numerous layout algorithms and search and filter functionality that enables debugging of SCons scripts 
More information can be found at [http://sconsolidator.com](http://sconsolidator.com) and its update site is available at [http://www.sconsolidator.com/update](http://www.sconsolidator.com/update). 


# Eclipse SCons Builder Plug-in

The Eclipse SCons Builder plugin can be found at [http://nic-nac-project.de/~lothar/eclipse/update/SConsBuilderPlugin.html](http://nic-nac-project.de/~lothar/eclipse/update/SConsBuilderPlugin.html) 

This builder plugin is an addon to the Eclipse >= 3.0 C/C++ Development tools CDT >= 2.0.  It was authored by Lothar Werzinger and Rafael de Pelegrini Soares.  Early versions were licensed under the CPL (common public license).  Later versions were licensed under the EPL (Eclipse public license). 

As of January 2009, the last released version was 29 June 2007.  Compatibility with CDT 4.0 and CDT 5.0 is uncertain.  You can install it and then use New, Other, C++, Convert Project to SCons, and it tries to find SCons, but given the scant documentation, it's not very helpful. The best approach at the moment seems to be to run SCons as an External Tool, which worked for one editor. 


## Tutorial

Build C++ Programs With SCons in Eclipse Using SConsBuilder Plugin(MS Windows) by Tabrez Iqbal, 24 October 2007 [http://beans.seartipy.com/2007/10/24/build-c-programs-with-scons-in-eclipse-using-sconsbuilder-pluginms-windows/](http://beans.seartipy.com/2007/10/24/build-c-programs-with-scons-in-eclipse-using-sconsbuilder-pluginms-windows/) 

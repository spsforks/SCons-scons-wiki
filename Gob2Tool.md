

# The SCons Gob2 tool

This tool offers a simple Builder named `Gob2()` for creating C/CPP and header files from `*.gob` input. It does so by calling the GObject builder executable `gob2`. 


## Install

Installing it requires you to copy (or, even better: checkout) the contents of the package's `gob2` folder to 

* "`/path_to_your_project/site_scons/site_tools/gob2`", if you need the Gob2 Tool in one project only, or 
* "`~/.scons/site_scons/site_tools/gob2`", for a system-wide installation under your current login. 
For more infos about this, please refer to  

* the SCons User's Guide, chap. 19.7 "Where to put your custom Builders and Tools" and 
* the SCons Tools Wiki page at [http://scons.org/wiki/ToolsIndex](http://scons.org/wiki/ToolsIndex). 

## How to activate

For activating the tool "gob2", you have to add its name to the Environment constructor, like this 


```txt
env = Environment(tools=['default','gob2'])
```
On its startup, the Gob2 tool tries to find the `gob2` executable. So make sure that it is added to your system's environment `PATH` and can be called directly, without giving its full path. 


## Using it

Simply call 


```txt
env.Gob2('*.gob')
```
for C files, or 


```txt
env.Gob2Cpp('*.gob')
```
for CPP output. 

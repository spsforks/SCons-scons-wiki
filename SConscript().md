

# SConscript()/env.SConscript()


## Syntax

**SConscript**(scripts, [exports, variant_dir, src_dir, duplicate])   
 **env.SConscript**(scripts, [exports, variant_dir, src_dir, duplicate])   
 

**SConscript**(dirs=subdirs, [name=script, exports, variant_dir, src_dir, duplicate])   
 **env.SConscript**(dirs=subdirs, [name=script, exports, variant_dir, src_dir, duplicate]) 


## Description

This tells scons to execute one or more subsidiary SConscript (configuration) files. There are two ways to call the [SConscript()](SConscript()) function. 

The first way you can call [SConscript()](SConscript()) is to explicitly specify one or more scripts as the first argument. A single script may be specified as a string; multiple scripts must be specified as a list (either explicitly or as created by a function like [Split()](Split())). 

The second way you can call [SConscript()](SConscript()) is to specify a list of (sub)directory names as a **dirs=subdirs** keyword argument. In this case, scons will, by default, execute a subsidiary configuration file named 'SConscript' in each of the specified directories. You may specify a name other than SConscript by supplying an optional **name=script** keyword argument. 

The optional **exports** argument provides a list of variable names or a dictionary of named values to export to the script(s). These variables are locally exported only to the specified script(s), and do not affect the global pool of variables used by the [Export()](Export()) function. The subsidiary script(s) must use the [Import()](Import()) function to import the variables. 

In effect, the optional **variant_dir** argument causes the files (and subdirectories) in the directory where script resides to be copied to **variant_dir** and the build performed in **variant_dir**. Thus, all of the targets (for example, object files and executables) that would normally be built in (or underneath) the directory containing script would actually be built in (or underneath) **variant_dir**. See the description of the [VariantDir()](VariantDir()) function for the details and restrictions. **variant_dir** is interpreted relative to the directory of the calling SConscript file. 

Normally, the source for the variant build is the directory containing script. If the sources are not in script's directory, the optional **src_dir** argument provides the location of the sources. **src_dir** is interpreted relative to the directory of the calling SConscript file. 

By default, scons will link or copy (depending on the platform) all the source files into the variant directory tree. This behavior may be disabled by setting the optional **duplicate** argument to 0 (it is set to 1 by default), in which case scons will refer directly to the source files in their source directory when building target files. See the description for [VariantDir()](VariantDir()) for the details and restrictions. 

Any variables returned by script using [Return()](Return()) will be returned by the call to [SConscript()](SConscript()). 


## Examples


```python
#!python 
SConscript('subdir/SConscript')
foo = SConscript('sub/SConscript', exports='env')
SConscript('dir/SConscript', exports=['env', 'variable'])
SConscript('src/SConscript', variant_dir='build', duplicate=0)
SConscript('bld/SConscript', src_dir='src', exports='env variable')
SConscript(dirs=['sub1', 'sub2'])
SConscript(dirs=['sub3', 'sub4'], name='MySConscript')
```
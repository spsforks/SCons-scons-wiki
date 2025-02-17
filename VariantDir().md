# VariantDir / env.VariantDir

## Syntax

 * `VariantDir(variant_dir, src_dir, [duplicate])`
 * `env.VariantDir(variant_dir, src_dir, [duplicate])`
 
## Description

In effect, the _src_dir_ directory tree is copied to _variant_dir_ so a build can be performed there. `VariantDir()` can be called multiple times with the same _src_dir_ to set up multiple builds with different options (variants). _src_dir_ must be in or underneath the SConstruct file's directory, and _variant_dir_ may not be underneath the _src_dir_.  

The default behavior is for scons to duplicate the source files in the variant tree and then build the derived files within the variant tree. This guarantees correct builds regardless of whether intermediate source files are generated during the build, whether preprocessors or other scanners search for included files relative to the source file, or whether individual compilers or other invoked tools are hard-coded to put derived files in the same directory as source files.  

If possible on the platform, the duplication is performed by linking rather than copying; see also the `--duplicate` command-line option. Moreover, only the files needed for the build are duplicated; files and directories that are not used are not present in _variant_dir_.  

Duplicating the source tree may be disabled by setting `duplicate=0`. This will cause scons to invoke Builders using the path names of source files in _src_dir_ and the path names of derived files within _variant_dir_. This is always more efficient than the default `duplicate=1`, and is usually safe for most builds (but see above for cases that may cause problems).  

Note that `VariantDir()` works most naturally with a subsidiary SConscript file. However, you would then call the subsidiary SConscript file _not in the source directory, but in the variant directory_, regardless of the value of _duplicate_. This is how you tell scons which variant of a source tree to build. For example:  


```python
VariantDir('build-variant1', 'src')
SConscript('build-variant1/SConscript')
VariantDir('build-variant2', 'src')
SConscript('build-variant2/SConscript')
```
See also the [SConscript()](SConscript()) function for another way to specify a variant directory in conjunction with calling a subsidiary SConscript file. 


## Users Guide

Use the `VariantDir()` function to establish that target files should be built in a separate directory from the source files:
  
```python 
VariantDir('build', 'src')
env = Environment()
env.Program('build/hello.c')
```
Note that when you're not using an SConscript file in the src subdirectory, you must actually specify that the program must be built from the `build/hello.c` file that SCons will duplicate in the build subdirectory.  

When using the `VariantDir` function directly, SCons still duplicates the source files in the variant directory by default:  
```bash
% ls src
hello.c
% scons -Q
cc -o build/hello.o -c build/hello.c
cc -o build/hello build/hello.o
% ls build
hello  hello.c  hello.o
```
    

You can specify the same `duplicate=0` argument that you can specify for an `SConscript()` call:  


```python
VariantDir('build', 'src', duplicate=0)
env = Environment()
env.Program('build/hello.c')
```
    

In which case SCons will disable duplication of the source files:  


```bash
% ls src
hello.c
% scons -Q
cc -o build/hello.o -c src/hello.c
cc -o build/hello build/hello.o
% ls build
hello  hello.o
```

## Examples

```python
VariantDir('build-variant1', 'src')
SConscript('build-variant1/SConscript')
VariantDir('build-variant2', 'src')
SConscript('build-variant2/SConscript')
```

## See Also

* [SConscript()](SConscript()) 
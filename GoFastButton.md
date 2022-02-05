By default SCons goes to great lengths to give you an accurate and reproducible build. If you have a slow computer or a large build, there are various options that can make SCons faster by sacrificing accuracy. 

TL;DR: this command will probably execute your build as fast as possible, but please read on to understand what you're doing:
```py
scons --max-drift=1 --implicit-deps-unchanged
```

Details of various speedups:

* `env.Decider('content-timestamp')`: you can choose the Decider function for a given environment.  *content-timestamp* says if the timestamp hasn't changed, don't bother recomputing the file signature.  Having to fully read lots of files to compute the hashes only to find they didn't change is expensive.  See the man page for more info.
* `--max-drift`: By default SCons will calculate the signature hash of every source file in your build each time it is run, and will only cache the checksum after the file is 2 days old. This default of 2 days is to protect from clock skew from NFS or revision control systems. You can tweak this delay using `--max-drift=SECONDS` where `SECONDS` is some number of seconds. Decreasing `SECONDS` can improve build speed by eliminating superfluous signature calculations. Instead of specifying this on the command line each run, you can set this option inside your SConstruct or SConscript file using `SetOption('max_drift', SECONDS)`. 
* `--implicit-deps-unchanged`: By default SCons will rescan all source files for implicit dependencies (e.g. C/C++ header #includes), which can be an expensive process for the same reason computing the hashes is expensive: you have to do the I/O to read the whole file, and doing so may cause other file system cache data (not SCons' cache) to flush that you might otherwise have been able to make use of. You can tell SCons to cache the implicit dependencies between invocations using the `--implicit-deps-unchanged`. By using this option telling SCons that you didn't change any of the implicit dependencies since it was last run - which is often the case when you're doing small icremental changes while coding actively on your project - so it doesn't need to bother. If you do change the implicit dependencies, then using `--implicit-deps-changed` will cause them to be rescaned and cached. Note you cannot set this option from within the SConstruct or SConscript files. 
* `--implicit-cache`: This option tells SCons to intelligently cache implicit dependencies. It attempts to determine if the implicit dependencies have changed since the last build, and if so it will recalculate them. This is usually slower than using `--implicit-deps-unchanged`, but is also more accurate. Instead of specifying this on the command line each run, you can set this option inside your SConstruct or SConscript file using `SetOption('implicit_cache', 1)`. 
* `CPPPATH`: normally you tell Scons about include directories by setting the CPPPATH construction variable, which causes SCons to search those directories when doing implicit dependency scans and also includes those directories in the compile command line. If you have header files that never or rarely change (e.g. system headers, or C run-time headers), then you can exclude them from CPPPATH and include them in the CCFLAGS construction variable instead, which causes SCons to not consider those directories when scanning for implicit dependencies. Carefully tuning the include directories in this way can usually result in a dramatic speed increase with very little loss of accuracy. 
* <s>Avoid RCS and SCCS scans by using `env.SourceCode(".", None)` - this is especially interesting if you are using lots of c or c++ headers in your program and that your file system is remote (nfs, samba).</s> **Note: _this option has been removed from SCons_**
* When using `VariantdDir`, use it with "duplicate" set to 0: `VariantDir(variant_dir, src_dir, duplicate=0)`. This will cause scons to invoke Builders using the path names of source files in `src_dir` and the path names of derived files within `variant_dir`. However, this may cause build problems if source files are generated during the build, IF any invoked tools are hard-coded to put derived files in the same directory as the source files. 
* On a multi-processor machine it may be beneficial to run multiple jobs at once - use the --jobs N (where N is the number of processors on your machine), or `SetOption)('num_jobs', N)` inside your SConstruct or SConscript.  On Windows machines, the number of processors is available in the environment variable `NUMBER_OF_PROCESSORS`.
* If you have more than a few dozen preprocessor defines (`-DFOO1 -DFOO2`) you may find from using `--profile` that SCons is spending a lot of time in the `subst()` method, usually just adding the -D string to the defines over and over again. This can really slow down builds where nothing has changed. As an example: with 100+ defines I saw a do-nothing build time drop from 35s to 20s using the idea described in "Caching the CPPDEFINES" elsewhere on this page. 


Another trick to making things faster is to avoid relinking programs when a shared library has been modified but not rebuilt. See [SharedLibrarySignatureOverride](SharedLibrarySignatureOverride) 

---

The following was suggested by [leanid nazdrynau in scons-users, May 2006](http://scons.tigris.org/servlets/ReadMsg?list=users&msgNo=7713):

```python 
# Next line is important, it deactivates tools search for default variable.
# just note that now in SConscript you have to use env.Program(...) instead of simply Program().
SCons.Defaults.DefaultEnvironment(tools=[]) 
```

## Note on the `CPPPATH` trick

The `CPPPATH` trick mentioned above made a great difference for me, because I have many libraries installed in non-standard directories (e.g. these from Fink), and these directories end up explicitly referenced in compiler command lines. 

However, for this trick to work, `CCFLAGS (CXXFLAGS)` has to come *after* `CPPFLAGS` (which are in `$_CCCOMCOM`) in the compiler command line. If not, the compiler will typically include the _installed_ headers from the library I am developing, instead of including the local headers referenced by, say, `env.Prepend(CPPPATH0='#mylibheaders'])`. 

Here is the code I use to put `CCFLAGS` after `CPPFLAGS`. It also imports software resource paths  from env variables. (Any comments to make this easier would be welcome.) 

```python 
# CPPPATH trick, see http://www.scons.org/wiki/GoFastButton

# For this to work, CCFLAGS (CXXFLAGS) have to come *after*
# CPPFLAGS (which are in $_CCCOMCOM)
if env['CXXCOM'] == "$CXX -o $TARGET -c $CXXFLAGS $_CCCOMCOM $SOURCES":
  # SCons 0.97
  env['CXXCOM'] = "$CXX -o $TARGET -c $_CCCOMCOM $CXXFLAGS $SOURCES"
elif env['CXXCOM'] == "$CXX -o $TARGET -c $CXXFLAGS $CCFLAGS $_CCCOMCOM $SOURCES":
  # SCons 0.98
  env['CXXCOM'] = "$CXX -o $TARGET -c $_CCCOMCOM $CXXFLAGS $CCFLAGS $SOURCES"
else:
  print "Unexpected default CXXCOM"
  Exit(1)

if env['SHCXXCOM'] == "$SHCXX -o $TARGET -c $SHCXXFLAGS $_CCCOMCOM $SOURCES":
  # SCons 0.97
  env['SHCXXCOM'] = "$SHCXX -o $TARGET -c $_CCCOMCOM $SHCXXFLAGS $SOURCES"
elif env['SHCXXCOM'] == "$SHCXX -o $TARGET -c $SHCXXFLAGS $SHCCFLAGS $_CCCOMCOM $SOURCES":
  # SCons 0.98
  env['SHCXXCOM'] = "$SHCXX -o $TARGET -c $_CCCOMCOM $SHCXXFLAGS $SHCCFLAGS $SOURCES"
else:
  print "Unexpected default SHCXXCOM"
  Exit(1)

# process env variables
for K in ['CPPFLAGS', 'CFLAGS', 'CXXFLAGS', 'LDFLAGS', 'CC', 'CXX']:
  if K in os.environ:
    dict = env.ParseFlags(os.environ[K])
    # These headers are supposed static. Don't check at each build.
    for i in dict['CPPPATH']: 
      dict['CCFLAGS'].append('-I' + i)
    dict['CPPPATH'] = []
    env.MergeFlags(dict)
```
Another solution was suggested by Roberto De Vecchi on scons-users: 

After the env initialization, I'm overriding _CCINCFLAGS as follow: 


```python
env['_CPPINCFLAGS']='$( ${_concat(INCPREFIX, CPPPATH, INCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)' +\
                    '$( ${_concat(INCPREFIX, CPP3RDPARTYPATH, INCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
```
So I can selectively add an include path to `CCPPATH` or `CPP3RDPARTYPATH` and have both of them passed to the compiler but only having scons scan the `CPPPATH` dirs.. 


## Caching the `CPPDEFINES` flags in the compiler command


```python
c_defs = ['FOO1', 'FOO2'. ... , 'FOO100']
import copy
def_str = ' -D'.join(c_defs)

cccom = copy.copy(env['CCCOM'])
cccom = cccom.replace('CCFLAGS', 'CCFLAGS -D%s ' % def_str)

shcccom = copy.copy(env['SHCCCOM'])
shcccom = shcccom.replace('CCFLAGS', 'CCFLAGS -D%s ' % def_str)

cxxcom = copy.copy(env['CXXCOM'])
cxxcom = cxxcom.replace('CCFLAGS', 'CCFLAGS -D%s ' % def_str)

shcxxcom = copy.copy(env['SHCXXCOM'])
shcxxcom = shcxxcom.replace('CCFLAGS', 'CCFLAGS -D%s ' % def_str)

fasterEnv = env.Clone(
    CCCOM = cccom,
    CXXCOM = cxxcom,
    SHCCCOM = shcccom,
    SHCXXCOM = shcxxcom,
    )   
```

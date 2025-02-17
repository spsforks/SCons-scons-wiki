

# Compiling Multiple Source Files with a Single Invocation of the Compiler

Many compilers support the ability to compile (and not necessarily link) multiple source files on a single command line.  This may not be a big draw to GCC, but for proprietary compilers it can make a big difference in license checkout time.  Compilers with floating network licenses can easily spend more time checking out the license than doing actual work, slowing down your build to a crawl.  The best solutions to this problem would be to switch to a free compiler or crack the DRM, but if those aren't options then here is an alternative.  Since the license checkout happens once per compiler invocation, then by compiling multiple source files at the same time you can reduce the total number of license checkouts necessary. 

This is a challenging recipe, because it violates the fundamental philosophy of build tools: every target is a product of its sources and can be built independently.  What we will do is define multi-target nodes that depend on multiple sources.  That part is fairly easy.  But if the programmer modifies one source file, we don't want SCons to recompile all the sources.  Instead, we will use a Generator to produce a custom action at build-time that will only compile the out of date sources.  That's the crux of the solution.  But as they say, the devil is in the details, and most of the code is devoted to getting dependency scanning working the way we need. 

The tool can be found at [https://code.edge.launchpad.net/~asomers/sconsaddons/mfobject](https://code.edge.launchpad.net/~asomers/sconsaddons/mfobject) (for a full list of external SCons Tools check out the [ToolsIndex](ToolsIndex)).  It covers both C and C++ compilation, but it should be easily extended to other languages as well.  My example includes a [VariantDir](VariantDir), because getting the include directories to work with [VariantDirs](VariantDirs) was non-trivial.  The example works on a tree of three directories: / , /src , and /obj .   and the example SConstruct is below. 


```txt
env = DefaultEnvironment(tools = ['default', 'mfobject'])
SConscript('src/SConscript', exports='env', variant_dir='obj', duplicate=0)
```
Here is the src/SConscript: 
```txt
Import('env')
objects = env.MFObject(['main.cc', 'foovar.cc'])
pgm = env.Program(['main.o', 'foovar.o'])
```
And here are the example source files.  The headers can be empty. 
```txt
#include "main.h"
#include "common.h"
int main(int argc, char** argv){
  return 0;
}
```

```txt
#include "common.h"
#include "foo.h"
int foovar;    
```
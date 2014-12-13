
To generate a Visual Studio project a list of headers and a list of sources are required, but the builtin Find``Source``Files will only find sources, not headers used by those sources. These can be entered manually, or automatically grabbed from the output of a Shared``Library/Static``Library/Program/Object builder so that they will automatically be updated when the targets change (perhaps by configuration, perhaps by adding new sources to the target).  

Here is the code to provide such a functionality, and an example on how it can be used: 


```txt
import SCons

def FindAllSourceFiles(self, target):
    def _find_sources(tgt, src, hdr, all):
        for item in tgt:
            if SCons.Util.is_List(item):
                _find_sources(item, src, hdr, all)
            else:
                if item.abspath in all:
                    continue

                all[item.abspath] = True

                if item.path.endswith('.c'):
                    if not item.exists():
                        item = item.srcnode()
                    src.append(item.abspath)
                elif item.path.endswith('.h'):
                    if not item.exists():
                        item = item.srcnode()
                    hdr.append(item.abspath)
                else:
                    lst = item.children(scan=1)
                    _find_sources(lst, src, hdr, all)

    sources = []
    headers = []
    
    _find_sources(target, sources, headers, {})

    return sources, headers

from SCons.Script.SConscript import SConsEnvironment # just do this once
SConsEnvironment.FindAllSourceFiles = FindAllSourceFiles

env = Environment()

prog = env.Program('foo', ['main.c', 'foo.c', 'bar.c'])
sources, headers = env.FindAllSourceFiles(prog)

env.MSVSProject(
    ...,
    ...,
    srcs = sources,
    incs = headers,
    ...,
    ...
)

```
This version adds .c-files to sources and .h-files to headers, append checks for whatever sources you have ('.cpp', '.cc', '.hpp' for example). Worth noting is that it adds a performance penalty compared to having a static list of headers/sources, but in some cases it makes very much sense in having generated Visual Studio projects. The penalty is of course related to the number of files in the project, how many diffrent file types that should be included, but should be very low for most projects. 

**NOTE**: As of SCons snapshot release 20070918 implicit command dependencies are enabled. This will add more nodes (dependencies on the tools) to be processed thus degrading the performance quite a bit. To disable this, do the following: 


```txt
env = Environment(IMPLICIT_COMMAND_DEPENDENCIES = 0)
```
Here is a more general version that accepts a list of file extensions as argument. It's slightly slower than the above version (may have room for improvements) but still much faster than the SCons Find``Source``Files. Failsafe input checks should be added. 


```txt
def FindAllSourceFiles(self, target, *args):
    def _find_sources(ptrns, tgt, all):
        for item in tgt:
            if SCons.Util.is_List(item):
                _find_sources(ptrns, item, all)
            else:
                if item.abspath in all:
                    continue

                all[item.abspath] = True

                for pattern, lst in ptrns.items():
                    if pattern.match(item.path):
                        if not item.exists():
                            item = item.srcnode()
                        lst.append(item.abspath)
                        break

                else:
                    lst = item.children(scan=1)
                    _find_sources(ptrns, lst, all)

    patterns = {}
    for arg in args:
        patterns[re.compile('.+\\.('+'|'.join(arg) + ')$', re.IGNORECASE)] = []

    _find_sources(patterns, target, {})

    return patterns.values()

from SCons.Script.SConscript import SConsEnvironment # just do this once
SConsEnvironment.FindAllSourceFiles = FindAllSourceFiles

env = Environment()

prog = env.Program('foo', ['main.c', 'foo.c', 'bar.c', 'baz.s'])
sources, headers = env.FindAllSourceFiles(lib, ['c', 's'], ['h'])
```
## Building SWIG wrappers with SCons

SWIG already works out the the box, you just add your `.i` files to the list of source files and it will all turn out fine. Built-in SWIG doesn't track down dependencies though, so try this snippet from Mattias on the mailing list: **Update 19 July 2007:**  Support for tracking SWIG dependencies has been added to the SCons code base and will be available next release (most likely `0.97.1`). The configuration is controlled by a `$SWIGPATH` variable that is searched for `.i` files and which gets translated into `-I` options on the command line (like the `$CPPPATH` variable does for C preprocessing). 

```python
import SCons.Script

#... then, later...

SWIGScanner = SCons.Scanner.ClassicCPP(
    "SWIGScan",
    ".i",
    "CPPPATH",
    '^[ \t]*[%,#][ \t]*(?:include|import)[ \t]*(<|")([^>"]+)(>|")'
)

env.Prepend(SCANNERS=[SWIGScanner])
```

Mattias also writes: "Regarding the _wrap.h for directors I just add it add a `SideEffect()` and a `Clean()` call for it. You might also considering throwing a `Depends()` in there. Do the same for the generated .py file." -- [JohnPye](JohnPye) 

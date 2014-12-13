
This recipe demonstrates how to call the C/CPP scanner on one of your source files manually, and get the contained list of include files (headers) returned. 

Note, that you normally don't have to do this by hand, since SCons implicitly scans all source files in the background for you. However, you might want to get at the list of found includes for a source file, too. The background of this recipe was that a user wanted to prescan his CPP files for include statements. He would then use this list of headers, in order to decide which source files would get compiled into the final executable (see [http://four.pairlist.net/pipermail/scons-users/2014-March/002253.html](http://four.pairlist.net/pipermail/scons-users/2014-March/002253.html)). 


```txt
a.cpp:
------

#ifdef BALLA
#include "b.h"
#else
#include "c.h"
#endif

void test()
{
  ;
}


b.h:
----

#define B


c.h:
----

#define C


SConstruct:
-----------

#
# Simple example of how to call C/CPP source scanners directly.
#
import SCons.Scanner

env = Environment(CPPPATH=['.'])

# Uncomment/comment the next line, such that either
# "b.h" or "c.h" get found for the full preprocessing approach...
env.Append(CPPDEFINES=['BALLA'])

f = env.File("a.cpp")

#
# Scanning with the "classic" approach (no #ifdefs are parsed)
#
scanner = SCons.Scanner.C.CScanner()
includes = scanner(f, env, scanner.path_function(env))
print "\nClassic approach:"
for i in includes:
    print "  + %s" % str(i)


#
# Full preprocessing during scanning for includes
#
prescan = SCons.Scanner.C.SConsCPPScannerWrapper('prescanner','.')
fincludes = prescan(f, env, prescan.path(env))
print "\n\nFull preprocessing:"
for f in fincludes:
    print "  * %s" % str(f)

print "\n"


```
Depending on whether you comment/uncomment the line where the definition of the variable `BALLA` gets appended, the output would look either: 


```txt
Classic approach:
  + b.h
  + c.h


Full preprocessing:
  * b.h

```
or 


```txt
Classic approach:
  + b.h
  + c.h


Full preprocessing:
  * c.h

```


## Simple Analysis of Automake Syntax

If the `make`-like target syntax is ignored, an Automake input file looks like a series of assignments to structured variables:  
 `     variable = item ...`  
 where the list of items actually is tokenized as if it were on a shell command line, with quotes and limited variable substitution; configure-time substution is introduced with a strudel (at-sign) character.  Some examples:  
 `     common_subs = foo.c bar.c`  
 `     bin_PROGRAMS = polly`  
 `     polly_SOURCES = main.c $common_subs`  
 `     polly_CPPFLAGS = -DSUBST="string with spaces"`  
 `     polly_CFLAGS = -O`  
 `     polly_LIBADD = curses @EXTRALIBS@`  
 `     SUBDIRS = src`  
 

The variable is cracked right to left, breaking at underscores.  There are three flavors: 
Primary targets
: 
      * The first value is one of `PROGRAMS`, `LIBRARIES`, `LTLIBRARIES`, `SCRIPTS`, `DATA`, `HEADERS`, `MANS`, `TEXINFOS`, `LISP`, `PYTHON`, or `JAVA`. 
      * The second value is either the keyword `EXTRA`, the keyword `check`, or a directory identifier.  A directory identifier refers to an Automake variable with `dir` appended to the name; thus if there's an Automake variable with the name `foodir` (presumably containing a directory path) then `foo` is the directory identifier that specifies that path. 
            * There are some predefined directory identifiers (and corresponding variables): `bin`, `data`, `doc`, `include`, `info`, `lib`, `libexec`, `localstate`, `man`, `oldinclude`, `pkgdata`, `pkginclude`, `pkglib`, `sbin`, `sharedstate`, and `sysconf`.  (I may have missed some.) 
            * Other directory identifiers are set up by standard Automake macros: `lisp`, `python`, `pkgpython`, `pyexec`, and `pkgpyexec`. 
            * The user may also set up a variable ending in `dir` and use the associated directory identifier. 
      * The third, fourth, and fifth values are optional prefixes from the set `inst`, `noinst`, `dist`, `nodist`, and `nobase`. 

Per-target modifiers
: 
      * The first value is one of `AR`, `CCASFLAGS`, `CFLAGS`, `CPPFLAGS`, `CXXFLAGS`, `DEPENDENCIES`, `FFLAGS`, `GCJFLAGS`, `LDADD`, `LDFLAGS`, `LFLAGS`, `LIBADD`, `LINK`, `OBJCFLAGS`, `RFLAGS`, `SHORTNAME`, `SOURCES`, `UPCFLAGS`, or `YFLAGS`.  (It's not clear if this set is extensible, or if I missed any.) 
      * The next value is either the keyword `AM` or an item identified in a primary assignment.  The item name is canonicalized.  Since the canonical name is created by replacing characters with underscores, teasing out the boundary of the name can be tricky. 
      * The third, fourth, and fifth values are optional prefixes from the set `inst`, `noinst`, `dist`, `nodist`, and `nobase`. 

Simple variables
: 
Anything not covered by the above cases is a **simple variable**.  Some variables have semantics associated with them (_e.g._, `SUBDIRS` says which subdirectories should be examined for further build instructions).  There are variables like `EXTRA_SOURCES` that look like they ought to be one of the first two categories, but have their own semantics.  (((There should be a list here of the simple variables with special semantics.))) 




## A few bits about semantics

* Some combinations of structured variable names are meaningless and are disallowed.  For example, `PROGRAMS` can't be installed in a `man` directory, and `inst` and `noinst` can't both occur as prefixes. 
* Many simple variables aren't so simple and have their own specialized semantics.  There needs to be a list of some of them here. 
   * Although it looks like a primary with a directory identifier, `EXTRA_DIST` is a simple variable with primary-like semantics. 
   * `SUBDIRS` is a list of subdirectories containing `Makefile.am` files that are to be included in the build. 
* The `Makefile.in` resulting from an Automake run has a bazillion targets: `all`, `install`, `install-strip`, `install-exec`, `install-data`, (*,`install-`*) for [`man`, `dvi`, `html`, `info`, `ps`, `pdf`], `uninstall`, `test`, `dist` (and `dist-`* for [`bzip2`, `gzip`, `shar`, `tarZ`, `zip`]), `distdir`, `check`, `distcheck`, `installcheck`, `doc`, `tags` and `ctags`, `clean`, `mostlyclean`, `distclean`, `realclean`, `maintainer-clean`, `clobber`, and their *`-local` and *`-hook` variants.  And this list isn't complete. 
This grid identifies what I believe to be the install locations for each primary type.  (Automake probably allows more combinations; if you know of any, please let me know and I'll update it.)  It's a useful checklist to ensure minimal coverage of the concepts.  It's been extended to include additional SCons builders that don't seem to be included in the list of Automake primaries and for additional install locations that are implied but not specifically mentioned. 

* - SCons Builders and additional directories  
 E - Executable, platform-specific  
 e - Executable  
 P - Platform-specific  
 S - Single-machine information  
 X - Architecture-independent 
[[!table header="no" class="mointable" data="""
Primary  
Builder  
  
  
  
  
  
  
  
Install  
Directory  | P  
R  
O  
G  
R  
A  
M  
S  | L  
I  
B  
R  
A  
R  
I  
E  
S  | *  
S  
h  
a  
r  
e  
d  | *  
L  
o  
a  
d  
a  
b  
l  
e  | L  
I  
B  
T  
O  
O  
L  | S  
C  
R  
I  
P  
T  
S  | D  
A  
T  
A  | H  
E  
A  
D  
E  
R  
S  | M  
A  
N  
S  | T  
E  
X  
I  
N  
F  
O  
S  | *  
D  
V  
I  | *  
P  
D  
F  | *  
P  
o  
s  
t  
S  
c  
r  
i  
p  
t  | *  
H  
T  
M  
L  | L  
I  
S  
P  | P  
Y  
T  
H  
O  
N  | J  
A  
V  
A  | ?  
P  
e  
r  
l | Notes
bin | E |   |   |   |   | e |   |   |   |   |   |   |   |   |   |   |   |   |  
sbin | E |   |   |   |   | e |   |   |   |   |   |   |   |   |   |   |   |   |  
libexec | E |   |   |   |   | e |   |   |   |   |   |   |   |   |   |   |   |   |  
*pkglibexec | E |   |   |   |   | e |   |   |   |   |   |   |   |   |   |   |   |    |  
lib |   | P | P | P | P |   |   |   |   |   |   |   |   |   |   |   |   |   |  
pkglib |   | P | P | P | P |   |   |   |   |   |   |   |   |   |   |   |   |   |  
data |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |   |   |  
pkgdata |   |   |   |   |   |   | X |   |   |   | X | X | X | X |   |   |   |   |  
doc |   |   |   |   |   |   |   |   |   |   | X | X | X | X |   |   |   |   |  
include |   |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |   |  
pkginclude |   |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |   |  
oldinclude |   |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |   |  
info |   |   |   |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |  
man |   |   |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |  
sysconf |   |   |   |   |   | e | S |   |   |   |   |   |   |   |   |   |   |   |  
*pkgsysconf |   |   |   |   |   | e | S |   |   |   |   |   |   |   |   |   |   |   |  
localstate |   |   |   |   |   |   | S |   |   |   |   |   |   |   |   |   |   |   | writable
*pkglocalstate |   |   |   |   |   |   | S |   |   |   |   |   |   |   |   |   |   |   | writable
sharedstate |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |   |   | writable
*pkgsharedstate |   |   |   |   |   |   | X |   |   |   |   |   |   |   |   |   |   |   | writable
Directories inserted by associated Builder?||||||||||||||||||||
lisp |   |   |   |   |   |   |   |   |   |   |   |   |   |   | X |   |   |   |  
python |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | X |   |   |  
pkgpython |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | X |   |   |  
pyexec |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | X |   |   |  
pkgpyexec |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | X |   |   |  
*java |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | ? |   | ???
"""]]

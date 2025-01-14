

# Steps in the Autotools toolchain

This page is still **very preliminary**.  If you have comments or corrections, please send them to [GregNoel](GregNoel) for integration rather than editing the page yourself. 

GNU Autotools is a system that attempts to ease some of the difficult of project development, while enforcing the use of the GNU coding conventions (that is, it's part of the GNU virus).  This page is a synopsis of what the tools do and how they fit together. 

The toolchain consists of eight steps.  For the most part, they are done in the order given below. 

Nifty ASCII art is based on the diagrams in the _[Autobook](http://sourceware.org/autobook/)_. 


## 1. autoscan and ifnames

The starting point is to determine just which configure tests should be done.  The `autoscan` program looks at the program's sources and tries to determine if anything might be a portibility issue.  If it finds anything, it adds a test for it in the output file, which is then used as a draft for the actual configuration macros. 


```txt
user input files    optional input     process          output files
================    ==============     =======          ============

                    configure.ac - - - - -.
                                          V
                                      .--------,
{project sources} ------------------->|autoscan|------> configure.scan
                                      `--------'
```
* Scans source code to determine what configurable features the program uses 
* Picks up additional tests from existing `configure.ac` 
* Generates `configure.scan` as a draft for a new `configure.ac` 
* (Implemented in `Perl`?) 
* Identifies and generates tests for: 
   * programs used (`awk`, `cc`, `cpp`, _et.al._) 
   * preprocessor tokens 
   * header files used (special for dirent and others) 
   * libraries that will be needed (or just placeholder?) 
   * various structures and typedefs used 
   * various compiler features used 
   * use of certain problematical library functions 
* User edits `configure.scan` to produce `configure.ac` 
* User can use `ifnames` to get list of macro symbols 

## 2. autopoint

The `autopoint` program provides the appropriate configuration macros for the release of `gettext` being used within the project. 


```txt
user input files    optional input     process          output files
================    ==============     =======          ============

                                     .---------,
configure.ac ----------------------->|autopoint|------> {macro files}
                                     `---------'
```
* Scans `configure.ac` for the version of `gettext` 
* Installs the appropriate versions of the configuration macros 

## 3. aclocal

The `aclocal` program consolidates the macros used by the configure script into a single file.  The apparent intent is to allow a distribution that is independent of `autotools` and yet still be able to regenerate the `configure` script if need be. 


```txt
user input files   optional input     process          output files
================   ==============     =======          ============

                    acinclude.m4 - - - - -.
                                          V
                                      .-------,
configure.ac ------------------------>|aclocal|
                 {user macro files} ->|       |------> aclocal.m4
                                      `-------'
```
* Scans `configure.ac` to determine autotool macros used 
* Collects automake macros from `acinclude.m4` 
* Collects user macros from project files 
* Produces `aclocal.m4` containing automake macros and user macros 
* (functionality will eventually be included in `autoconf`?) 

## 4. autoheader

Processes the configure macros to determine the `#define` tokens generated. 


```txt
user input files    optional input     process          output files
================    ==============     =======          ============

                    aclocal.m4 - - - - - - - .
                    (acconfig.h) - - - -.    |
                                        V    V
                                     .----------,
configure.ac ----------------------->|autoheader|----> config.h.in
                                     `----------'
```
* Scans `configure.ac` to determine generated `#define`s 
* Implemented by redefining some of the macros then running M4 over the input 
* Older releases used `acconfig.h` as a template, newer releases use `AH_`* macros for same effect 
* Produces `config.h.in` 

## 5. automake and libtoolize

The `automake` program takes a [simplified, stereotyped description](http://www.gnu.org/software/automake/manual/html_mono/automake.html#Program%20Sources) and generates a parameterized file that can be processed by `configure` to produce a `Makefile` that does the actual build.  If the build deals with libraries, `libtoolize` is invoked to generate equivalent parameterized files for manipulating libraries. 


```txt
user input files   optional input   processes          output files
================   ==============   =========          ============

                                     .--------,
                                     |        | - - -> COPYING
                                     |        | - - -> INSTALL
                                     |        |------> install-sh
                                     |        |------> missing
                                     |automake|------> mkinstalldirs
configure.ac ----------------------->|        |
Makefile.am  ----------------------->|        |------> Makefile.in
                                     |        |------> stamp-h.in
                                 .---+        | - - -> config.guess
                                 |   |        | - - -> config.sub
                                 |   `------+-'
                                 |          | - - - -> config.guess
                                 |libtoolize| - - - -> config.sub
                                 |          |--------> ltmain.sh
                                 |          |--------> ltconfig
                                 `----------'

```
* (`automake` is Perl script) 
* Simpler syntax than makefile 
* Scans `configure.ac` to see what symbols can be substituted. 
* Converts `Makefile.am` into `Makefile.in` with [standard targets](http://fill.in.ref) 
* Generates other GNU files (`COPYING`, `INSTALL`, `stamp-h.in`) 
* Generates other GNU scripts (`install-sh`, `missing`, `mkinstalldirs`) 
* Generates `config.guess` and `config.sub` 
* For `libtool`, generates `ltmain.sh` and `ltconfig` 

## 6. autoconf and autoreconf

The `autoconf` program converts the configure macros into a shell script. 

The `autoreconf` program is intended to update the generated files if the toolchain has been updated.  It simply runs `autopoint`, `aclocal`, `autoheader`, `automake`, `libtoolize`, and `autoconf`  as appropriate. 


```txt
user input files   optional input   processes          output files
================   ==============   =========          ============

                   aclocal.m4 - - - - - -.
                                         V
                                     .--------,
configure.ac ----------------------->|autoconf|------> configure
                                     `--------'
```
* package for generating configure scripts 
* Reads `configure.ac` and `aclocal.m4` 
* Evaluates [standard macros](http://www.gnu.org/software/autoconf/manual/autoconf-2.57/html_node/autoconf_194.html) 
* Runs M4 over the macros to get `configure` 

## 7. configure

The configure tests are run and the results are inserted in the various input files. 


```txt
user input files   other input      processes          output files
================   ===========      =========          ============

                                     .---------,
                   config.site - - ->|         | -----> config.status
                  config.cache - - ->|configure| - - -> config.cache
                                     |         +-,
                                     `-+-------' |
                                       |         |----> config.h
                   config.h.in ------->|config-  |----> Makefile
                   Makefile.in ------->|  .status|----> stamp-h
                                       |         +--,
                                     .-+         |  |
                                     | `------+--'  |
                   ltmain.sh ------->|ltconfig|-------> libtool
                                     |        |     |
                                     `-+------'     |
                                       |config.guess|
                                       | config.sub |
                                       `------------
```
* Evaluates command-line options (REF NEEDED) 
* reads `config.site` for other options 
* reads `config.cache` for current options 
* Evaluates feature tests 
* cross-compilation 
* updates `config.cache` 
* produces `config.status` 
* runs `config.status` 
   * converts `<foo>.in` to `<foo>` 
* runs `ltconfig` 
   * reads `ltmain.sh` 
   * generates `libtool` script 

## 8. make and libtool

The program is built. 


```txt
user input files   other input      processes          output files
================   ===========      =========          ============

                                   .--------,
                   Makefile ------>|        |
                   config.h ------>|  make  |--------> {project targets}
{project sources} ---------------->|        |
                                 .-+        +--,
                                 | `--------'  |
                                 |   libtool   |
                                 |   missing   |
                                 |  install-sh |
                                 |mkinstalldirs|
                                 `-------------'
```
* Evaluates DAG 
* `make` runs `libtool` 
   * Library and shared object support 
* (mostly covered already in SCons) 
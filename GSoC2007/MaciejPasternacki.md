

# Automatic build graph generation for SCons modeled on Automake


## Contact Information

Maciej Pasternacki <[gsoc2007@japhy.fnord.org](mailto:gsoc2007@japhy.fnord.org)> 

* Jabber IM: [xmpp:maciekp@japhy.fnord.org](xmpp:maciekp@japhy.fnord.org) 
* IRC: japhy or japhie on IRCnet (#PLD channel), sometimes some variant of japhy on Freenode (#lisp channel) 
* Timezone: CEST (UTC+2) 

## Synopsis

As of now, SCons functionality is similar to standard Make's -- it takes build graph description as input and from this graph it produces required targets.  Aim of the project is to augment SCons with functionality similar to GNU Automake which automatically generates Make's Makefiles (i.e. generate build graph description based on high-level project description, and complying to GNU packaging guidelines). 

Final product will include Python API for high-level project specification for SCons within SConstruct/SConscript files, inner program logic that generates relevant build graph from this description and transition tool to convert from Automake to SConstruct (without full Automake support, but supporting most common use cases). 

Project will be developed in test-driven manner and based on mock project descriptions for real-world non-trivial applications that are now Automake-based. 


## Benefits to the SCons Community

* SCons will become a better tool -- high-level project description and build model will be deliered. 
* User base will grow -- non-trivial projects that now use Automake for simplicity will be able to use SCons easily. 

## Project Details


### Analysis

Completed project will provide way of passing high-level project description to SCons by user.  This description will be in form semantically similar to one used by Automake in its Makefile.am files.  SCons inner logic will be provided to internally produce detailed build graph from such description.  Way of building this graph will be documented and standarized and will aim at maximum closeness to GNU release process stadards. 

Syntactically, high-level description language will be new Python API added to current SConstruct/SConscript API.  Inner logic for producing detailed build tree will be built on top of existing APIs.  Possibly some concepts from WAF will also be incorporated. 

Optionally, a separate migration tool allowing user to parse simple Automake input files and create SConscript files based on them will be also delivered. 


### Compatibility

Backwards compatibility is not a problem.  Project will extend and build on current SCons code base, without altering existing behaviour. It is possible that extension of current behaviour or new features will be needed, but there will be no incompatible changes. 

SCons packaging extension, which will be soon included, overlaps partially with Automake's functions.  This is a potential problem area and care must be taken to achieve both maximum functionality and compatibility with GNU guidelines by default. 

As for compatibility with outside world, project will aim at achieving partial compatibility with Automake, by means of transition script translating Makefile.am files to SConscripts. 


#### Automake compatibility and priorities

Automake supports eleven primary targets: PROGRAMS, LIBRARIES, LTLIBRARIES, SCRIPTS, DATA, HEADERS, MANS, TEXINFOS, LISP, PYTHON, and JAVA.  Essential three are PROGRAMS, LIBRARIES, and DATA; these are general targets, independent on actual file type, and they must be provided.  HEADERS, MANS, TEXINFOS, LISP, PYTHON, and JAVA relate to specific file types and hard-code magical logic to Autoconf-generated rules.  These may not be supported literally, but rather by specialization of relevant classes.  LISP, PYTHON and JAVA targets, as most specific, have lowest priority in implementation.  LTLIBRARIES (Libtool-built libraries) will probably not be implemented because of fact that Libtool itself is tightly integrated with Autotools and it may not be even possible to use it succesfully outside Autotools environment. 

Automake, cooperating with Autoconf, has possibilities such as modifying install names at compile- and install-time by command line options or cross-compiling.  In design stage, exact relation between Autoconf and Automake and degree of support for Autoconf-related features will be determined.  However, project is centered on Automake, not Autoconf, so re-implementing large parts of Autoconf logic is not in scope of this project. 

Special attention will be paid to Automake's dynamic features (e.g. per-target flags, -hook and -local targets, install names modification).  If it will be impossible to implement all of them in given time frame, design will make it possible to implement and integrate those features in the future, and design documentation will describe needed semantics. 

Automake defines lots of intermediate and final targets.  Scheme of naming intermediate targets will be examined and, if feasible, implemented (though possibly only partially). 

As for final targets, GNU release proces guidelines define twelve of them (not counting 'install-html', 'install-dvi', 'install-pdf', 'install-ps', 'dvi', 'html', 'pdf', and 'ps', which are too specific to be explicitly supported).  As much of them as possible within given time frame will be implemented.  Targets 'all' and 'install' have biggest priority and must be implemented; various levels of `clean', 'dist' and 'check' come next; lowest priority have 'info', 'uninstall', 'install-strip' and 'installdirs'.  'installcheck' is not an issue since it is a combination of two other targets. 

Almost all of final targets defined by Automake is install-related or clean, and should not be built by default; on the other hand, using Automake-related functionality should not alter other behaviour of SCons.  In order to achieve this, probably '[NonDefault](NonDefault)()' function, being an inverse of Default() will have to be implemented after discussing its exact semantics. 


### Techniques

Project will be test-driven, based on real world applications.  After period of Automake and WAF analysis, few chosen non-trivial real-world applications (called `model applications' later on) that are currently built with Automake will be chosen and analyzed.  Based on these analyses a model for build graph generation logic and high-level description language (preliminary API description) will be made. 

Based on this logic and description, mock descriptions of model application building in new API will be created.  This will serve as functional test suite being final milestone. 

Functional tests will be split into smaller test cases testing and describing single fragments of functionality.  These will serve as unit tests and will be basis for actual development. 


### Plan

As written earlier, my project won't change much of existing SCons internals and APIs, but rather will be built on them and use them. I plan to introduce new SConstruct/SConscript APIs for delivering high-level project description.  These APIs will generate and run traditional, detailed build graph on the fly. 

Draft of the APIs and internal model will be delivered early (before and during writing functional tests) in form of Wiki page and subject to discussion and further evolution. 

One main reason I don't plan full details now is not to get fixed on a solution before I have full understanding of problem and research on Automake, WAF and internals of SCons itself done. 

Mock descriptions and test cases won't be fixed -- they may be subject to change as need arises.  Probably some tool to partially parse reasonable subset of Makefile.am syntax and convert it to a SConscript will be created at some point. 


### References

Automake documentation ([http://sources.redhat.com/automake/automake.html](http://sources.redhat.com/automake/automake.html)): Source of inspiration, high-level description and logic model. 

GNU Coding Standards, chapter 7 'The Release Process' ([http://www.gnu.org/prep/standards/standards.html#Managing-Releases](http://www.gnu.org/prep/standards/standards.html#Managing-Releases)): Minor goal is to keep as close as possible to GNU standards to make packagers feel at home and make it possible to use existing automatics (e.g. RPM build macros in distros) to build SCons-based projects. 


### Examples

Pre-preliminary view on how SConstruct for amhello, described in Automake docs at [http://sources.redhat.com/automake/automake.html#Creating-amhello](http://sources.redhat.com/automake/automake.html#Creating-amhello), might look like (src/ subdirectory removed for brevity): 


```python
#!python 
env = Environment(
    NAME='schello',
    VERSION='1.0')
env.Bin(program='hello').Sources('main.c')
env.Dist(doc='README')
```
Note that this is only literal copy of amhello's Makefile.am in Python syntax resembling existing SConstruct API, done before in-depth research, so it can't be treated as actual API proposal. 


## Deliverables

1. Add support for standard directory locations recognized by Automake, described in GNU standards, to SCons. 
1. Description of build tree generation model, based on Automake and WAF research and existing SCons mechanics (preliminary internals documentation, subject to discussion and meant to evolve during the development); 
1. Outline of high-level specification language (preliminary API documentation, subject to discussion and meant to evolve during the development); 
1. Choice of model applications; 
1. Mock SConstruct files for model applications; 
1. Transition script for simple applications; 
1. Simple test cases; 
1. Single-directory simple project support (amhello compatibility level); 
1. Full description of high-level specification language (final API documentation); 
1. Transition script for complex applications; 
1. Complex test cases; 
1. Complex project support (model projects compatibility level); 
1. Incorporation of final API documentation into man page and tutorial. 
I propose deliverable (7) as a mid-term evaluation milestone. 


## Project Schedule

Interim period: support for standard directory locations (1) and discussing and implementing [NonDefault](NonDefault)() function, as smaller-scale separate projects to get familiar with SCons internals, development methodology and testing procedures. 

Weeks (parenthesised numbers refer to deliverables): 

1. Automake and WAF analysis. 
1. Description of build tree generation model (2). 
1. Outline of high-level specification language (3), Choice of model applications (4); 
1. Mock SConstruct files for model applications (5); 
1. Simple transition script (6), Simple test cases (7); 
1. Simple project support (8); 
1. Full description of high-level language (9); 
1. Transition script for complex applications (10); 
1. Complex test cases (11); 
1. Implementation of complex functionality; 
1. Compatibility at non-trivial program level (12); incorporation of API docs into official documentation (13); 
1. Buffer week for unexpected delays. 
Due to fact that main channel of communication between developer is a mailing lists and to big time zone differences, which may result in long time between responses, parts of analysis, discussion and design will take place in interim preparation period (May 1-28). 

In case not everything can be implemented in specified time frame, features to implement will be prioritized based on functional tests -- features used in most of chosen model programs will have greatest priority, so that at the end of summer most model programs will compile correctly. 

Also, full transition script might be left out if project will be out of schedule, giving more time to polish actual features. 


## Other Proposals

I intend to submit proposal also to LispNYC (Enhancing Exscribe -- [http://lispnyc.org/wiki.clp?page=soc07-details/excribe](http://lispnyc.org/wiki.clp?page=soc07-details/excribe)). SCons is my preferred project, as it seems most interesting and challenging. 


## Brief Biography

I am Polish CS student, on third year of five-year Masters program at University of Gdańsk ([http://www.ug.gda.pl/](http://www.ug.gda.pl/)).  I also work half-time as programmer for last three years.  Before that I was administrating Linux systems for about an year.  From 2004-2005 I worked on Python Zope webapp for Polish DTP-related company Afila (project got cancelled before finished).  Since 2005 I work for Polish-Japanese company Sentivision ([http://www.sentivision.com/](http://www.sentivision.com/)) as Common Lisp programmer.  While CL is my favourite language, Python is my second language of choice.  I also co-develop RPM-based PLD Linux Distribution ([http://www.pld-linux.org/](http://www.pld-linux.org/)). 

During work for Sentivision I contributed to Open Source Common Lisp projects, especially Embedded Common Lisp ([http://ecls.sourceforge.net/](http://ecls.sourceforge.net/)), Bese project ([http://common-lisp.net/project/bese/](http://common-lisp.net/project/bese/)) and [UnCommon](UnCommon) Web application server ([http://common-lisp.net/project/ucw/](http://common-lisp.net/project/ucw/)).  Quality of my code contributed to these projects was considered good enough by leading developers that I got direct write access to these repos.  My activity in these projects can be traced in both commit logs and on relevant mailing lists. 

I know GNU toolchain, including Autotools, both as a developer (worked a lot on autotools-based build system of Embedded Common Lisp) and as a packager for Linux distribution (wrote or contributed to many packages in PLD Linux, used to write add-on packages for Openwall GNU/*/Linux). 

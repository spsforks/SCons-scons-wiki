A page for the specific use case(s) we're trying to design for. 

This is _not_ intended to cover all of the functionality, but instead to list the common use cases that we believe cover "90%" of what users want from SCons.  The goal is to design the architecture for optimal performance of these "90%" cases.  Functionality outside of the "90%" use cases defined here will be supported (eventually), but performance may suffer. 

[TOC]


# THE Performance Test Configuration

(((SK:  I'm going to suggest that we try to create _one_ configuration that will represent our canonical test bed for performance tests.  It will be a reasonably large, multi-language project that contains at least some of all of the common tools that we want, as well as use of key features within the "90%" scope.)))   
(((JGN: Although I agree with the general idea, I view this as the integration test, the performance test for everything combined.  But there also should be <ins>unit</ins> tests, where a single component is exercised in detail.  Since we're not going to get to this level of testing overnight (or even soon), the most productive route is to create the all-in-one test first and then create more focused tests as we go along.))) 

Note that the specific numbers below are simply stakes in the ground for a default canonical use case for initial testing/design purposes. 

The implementation will actually generate test configurations, not (_e.g._) check in a hard-coded set of files, and the implementation will allow these settings to be tweaked. 

That said, the suggested default values can be adjusted in response to better input (i.e., suggestions welcome), or may very well be lowered to keep the "main" performance test configuration reasonably quick once we start actually trying to to test it. 

(((SK:  I'm re-evaluating my thinking here.  I added your suggestions re: test generation, and I agree about the need for performance test cases of specific components, and for the ability to scale factors in the larger test case like this.  My concern is that monolithic thinking has gotten us into trouble into trouble in the SCons architecture itself, so why do I think it wouldn't be a problem here?  My problem is I don't have a good model in my head for how to break this down into smaller test cases, because (IMHO) most of `O(N*M)` interactions that kill us are coming from interactions between subsystems that aren't going to show up unless you combine them in a performance test.   
As a concrete example, the actual search of (e.g.) `CPPPATH` directories for include files is already micro-optimized and would probably show adequate performance in isolation under a test configured to "search 100 `-I` directories for a program that include 100 distinct `.h` files."  It's not until you also say that you want to do that for 100 distinct `.cc` files that the larger algorithm breaks down.  And once you have to combine factors like this, it felt like the camel's nose under the tent that meant you might as well go with a large configuration anyway....   
Upshot:  I'm suspicious that my suggestion is really just because I don't know how to break this down profitably.  I would encourage someone else with a clearer conception to rewrite this (or to add an alternative structure) to try to break it down into more manageable subsets.)))   
(((JGN: I actually think you're making my point, but you're misunderstanding the details of what I think the test generator should do.  It should be possible to dial <ins>all</ins> of the parameters individually, not just a single dial with settings for 'small', 'medium', and 'large'.  You'd be able to dial up a case with a hundred include directories each with a hundred headers and one library with 100 sources, with all the other settings at zero or one.  In fact, you'd be able to dial each setting from ten to a thousand and compare the performance.  If there's a M*N interaction, that would show it.  If there appears to be a problem with performance-in-the-large, this would allow you to isolate the component(s) that are causing the problem.)))   
(((SK:  I totally understood that you were suggesting each setting should be separately configurable.  I agree.  But it's unhelpful to stop there.  The problem is not solved by just saying, "Oh, we'll make everything configurable."  Parameter configurability will make for a very useful performance testing infrastructure; great.  Now, if we're actually going to dial those settings appropriately in a set of smaller, non-monolithic use cases that identify the performance bottlenecks we want to measure ourselves against, _what should those use cases be_?  I don't have a good handle on how to start defining those configurations.)))   
(((JGN: I don't know that we can identify those use cases in advance, or that we should try.  A couple of cases, sure, but if we knew what the performance problems were, we wouldn't be here in the first place.  I want to be in the position that when we become suspicious that we have a problem, we can easily create a stress test.  But see below for some known stressors.))) 


## Common code plus three variants

We'll configure the entire build with a set of common code and a set of code built into a configurable number of variants.  The default will be three variants, representing a Release variant, a Debug variant (Microsoft terminology) and a Profile variant: 

* Common code 
  * Documentation 
  * Java compilation 
* Variant code 
  * C/C++ compilation 

## One repository

The entire build will also be configured to refer to a configurable number of repositories for source files.  We intend to test the following cases 

   * 0 repositories 
   * 1 repository 
   * 3 repositories 
The "canonical" performance case will be one repository. 


## C/C++ Compilation

C/C++ compilation will be tested with the following default configuration: 

   * Sources 
       * 1000 source `.c` / `.cpp` / `.cc` files 
       * 3 `.y` (yacc/bison) files 
       * 3 `.l` (flex/lex) files 
   * Targets 
       * 50 libraries 
       * 20 executable programs: 
          * one that incorporates all 50 libraries (representing the "main product") 
          * 19 other smaller programs (representing smaller associated utilities or test programs) 
   * 100 `-I` (include) directories  
Note:  this will actually expand to 200 `-I` options on the command line due to variant builds (or possibly 400 `-I` options if we use variant + repository) 
   * 10 `-L` (libpath) directories  
Note:  this will actually expand to 20 `-L` options on the command line due to variant builds (or possibly 40 `-L` options if we use variant + repository) 
Note that all values will be configurable in the generated test, of course. 

(((JGN: Humpf.  That's a pretty large "medium" build.  I'd want to be able to dial this between about fifty sources for a small build and 5,000 for a huge build.  I'd organize it as one subdirectory per library or program, configurable numbers of files per directory, and let the `-L` scale itself from that.  A hundred include directories seems extreme, even for a huge build; each library subdirectory would need itself, the program subdirectories would need all the library directories, then each would have a dialable number between, say, ten and fifty, unless you have some evidence that the number can be that much higher.  I could imagine a custom test that might want to stress that number, but I'm under the impression that you want more-or-less representative numbers for this test.)))   
(((SK:  One hundred include directories is taken from a real-life example that I'm wrestling with:  WebKit builds this way, sticking the `.h` files next to their `.cpp` files in a large, modular tree, and then just listing all of the directories as `-I` options.  Needless to say, our performance sucks on this case.  Maybe it's extreme, but if we don't handle it well, then I'll have a hard time thinking of the effort as successful...)))   
(((JGN: point taken, but I'd suggest that a hundred include directories is not "representative" and sounds like a candidate for a specialized configuration.  Other extremes are a single include leading to hundreds or thousands of implicit dependencies (like the wx library does) or a build that uses hundreds of libraries (like the mozilla builds).  There should be a couple of test cases to monitor performance specific to those circumstances.)))   
(((SK:  Okay.  Care to define those "couple of test cases?")))   
(((JGN:  In detail or broad brush?  Broad brush, the "WebKit" test has one hundred source directories, each with ten sources and ten headers; each source refers to all one thousand headers.  The "wx" test has one include directory with 1110 files (ten that refer to ten each that refer to ten each) and a program directory with ten files, each referring to the first ten include files.  The "mozilla" build has one hundred libraries of ten files each and a single program directory with ten files, each referring to ten distinct libraries.  Otherwise, each test case has no Java files, no repositories, no documentation, and builds into one variant directory.  Each test is run twice, once at one-tenth scale to set the yardstick and once at full scale; the larger test should take ten times as long (assuming linearity; otherwise a fit to the Big-O estimate).  Specific numbers vary to fit circumstances.  Is that enough?))) 


## Java

Default Java configuration: 

   * Sources 
       * 500 source `.java` files 
   * Targets 
       * 500 generated `.class` files 
       * 50 output `.jar` files ??? 
   * classpath directories??? 
   * what else ??? 
All values configurable. 

(((JGN: That seems like a lot of `.jar` files to me, but what do I know?))) 


## Documentation

   * Sources 
     * Source scatter in ??? subdirectories 
     * 100 input `.tex` files 
     * 100 input `.latex` files 
     * 100 input `.jpg` (or other graphics) files 
   * Targets 
     * ??? man pages 
     * ??? HTML pages 
     * ??? PDF files 
     * ??? PostScript files 
   * what else ??? 
Configurable. 


## Hierarchy

   * 100+ subdirectories (representing individual "components:" the libraries, the program(s), the Java) 
   * Every subdirectory has a separate `SConscript` file 
   * Every `SConscript` file creates a copy of an imported Environment 
(((JGN:  Wow, 100+?  SCons has fewer than 150 directories in the entire tree, a hundred under test alone, and if we were doing our packaging via SConscripts in all reasonable places, I doubt that there would be more than thirty all told.  I think you should allow this to be self-scaling based on the other characteristics chosen.)))   
(((SK:  Agreed re: self-scaling, this is just to try to put a stake in the ground for a reasonable aggregate number.  Feel free to restructure this if you think of a better way to represent that.))) 

   * Each library, program, documentation, and Java directory will have its own SConscript.  Each SConscript will describe how to build, install, stage, package source, and package for distribution. 
   * Each install directory will have its own SConscript.  Each SConscript will describe how to install, stage, package source, and package for distribution. 
   * Other types of directories? 
   * Every SConscript creates a clone of an imported Environment. 
   * The SConstruct xxx 
(((JGN: I think that's better, but it's still incomplete and needs to be filled out.))) 


## Packaging

(((JGN: source, binary, staging directories[*], direct installation, ...)))   
(((JGN: also zip, tar, ...))) 

[*] JGN: Using a staging directory is something not well handled by SCons today.  However, it comes up regularly in a number of guises (this is Ken's major heartache, for example) so we should at least have a place to put it when better support comes along.))) 


## Configuration(???)

(((JGN: everybody does a little: env[PLATFORM], `sys.xxx`, `os.yyy`, config contexts, ...)))   
(((JGN: Although most of this should be once per run, I'd like to see some of it done once per variant just to be sure those paths get exercised.)))   
(((SK: Good point re: some configuration things being per-variant, not per run.  Need to make sure this is covered somewhere, and that the distinction is reasonably clear to users.))) 


## Qt(???)

(((JGN: low but steady demand, lower priority, probably not initially, but put it in the test generator eventually.))) 


# Use Cases for the configuration

These list the specific things that we expect a hypothetical user to _build_ in this configuration.  These are the things that we want to optimize as much as posible by making sure they use a common path through the code. 

All build steps will be stubbed so the test can be run anywhere, and so that wall-clock time to run the test isn't completely dominated by "compilation" time. 

(((SK:  Should use of `-n` be called out specifically as a (set of) distinct use case(s)?  It's something developers do (or at least, I do) somewhat regularly to see what would be rebuilt.  It's also very useful to isolate SCons overhead from wall-clock compilation time.)))   
(((JGN: Good thought.  In fact, if `--touch` was implemented, we could possibly simulate all of this without having to use stubs at all, and the timing would be much more consistent.  Hmmm...))) 


## Full-tree build

All the languages, all the variants. 


## Null build

Rebuild the entire tree and verify that everything is up to date. 

This is important for isolating the SCons overhead in deciding that targets are up-to-date, but is not that importnat as a real-world use case.  In practice, people rarely do builds where nothing has changed, apart from the occasional "is everything up to date?" sanity check. 

(However:  Visual Studio, at least, gives a virtually instantaneous "up to date" response when no files have changed, doubtless because it's using Windows file-monitoring hooks to recognize that there have, in fact, been no changes since the last build, without having to actually look at anything on disk.  Trying to do something similar is perfectly all right, provided it doesn't slow down the Null+1 or Full-tree build cases unreasonably.) 


## Null+1 .c build

Canonical C/C++ developer workflow:  change a single `.c` file and rebuild. 

In practical, real-world terms, this is probably _the_ most important use case.  A given developer will do dozens of Null+1 builds a day.  A full-tree build, while still important, isn't done as frequently, and is usually automated, so it doesn't have the same in-your-face frustration factor that a slow Null+1 build does. 


## Null+1 .h build

Additional common C/C++ developer workflow:  change a single heavily-included `.h` file and rebuild. 


## Null+1 .java build

Canonical Java developer workflow:  change a single `.java` file and rebuild. 


# Out-of-scope things

This section should list things that we specifically do _not_ want to consider part of the "90%" performance criteria.  They will still function, and should not cause unreasonably slow performance.  But it's all right if these features deviate from the main processing path that we want to provide highly optimized performance for the "90%" use cases. 


## Generated Header Files

SCons should definitely handle them as well as it does now, including discovery of implicit dependencies in generated header files nested arbitrarily deep.  But it's all right if use of generated header files slows down processing (within reason) from the 90%-use-case optimized target. 

(((JGN: Uh, is this heading for PCH or for building an implicit dependency?  I could read it either way.  Whichever, both should probably be mentioned here.)))   
(((SK:  PCH?  Are you using the right acronym here (and above)?  PCH is "Pre Compiled Headers" which is a different thing than just handling the case of `#include` of a `.h` file that you generate from a build step.  Discovering implicit dependencies through generated `.h` files is a significant differentator for SCons, but it's uncommon enough that it shouldn't slow down the main code path.)))   
(((JGN: The problem is the word "generated" which could be interpreted as "pre-compiled".  It's why I used "built" to describe the same thing for source files.  Neither word is quite right, but I can't think of anything better.))) 


## Pre-Compiled Headers

Supporting Visual Studio's and/or `gcc`'s implementations of pre-compiled headers to speed up compilation performance should be supported, of course.  If it has to be done by straying from the main, optimized code path, that's okay. 


## Built Source Files

(((JGN: Probably a bit more important than either PCH or built implicit dependencies, but still not 90%-use-case.  On the other hand, it's really no different from other instances of chaining, so it ought to have no performance impact.))) 


## Fortran programs

An important niche, to be sure (no one else seems to pay as much attention to this as we do...), but definitely a niche.  Although I don't think we have to make them pay a penalty and believe they'll benefit as much as the C/C++ programmers do from all of these anticipated improvements, in terms of absolute "90%" requirements, they're definitely a niche.   We should not, if we ever have to choose, slow down the rest of the world just for Fortran. 


# Test Configuration Generator

(((JGN: More-or-less written off the top of my head.  Don't consider it a real design.))) 

The test configuration generator consists of a number of components.  Each component generates one specific type of test case.  In general, each component is responsible for creating and populating one directory.  There are a number of functions (not described here) that perform common actions like creating files, managing the SConscript for the directory, and so forth. 

(((JGN: could easily toss in more depth to the hierarchy by adding a project level with multiple projects, each with their own includes, sources, _etc._, or subdirectories of sources feeding up to a library or program.  Or both, for that matter.)))   
(((SK:  Good start.))) 

(((JGN: If I were designing this program, and it's really too early to do that, I'd make the control file be Python, just like a SConscript, with a repertoire of building blocks that it could mix and match, and the ability to specify, uh, call them content creators (_i.e._, some form of callback) that could tailor a particular building block to suit.  Some of the building blocks would create certain kinds of files (headers and sources and Java, oh my!), while others would create directories of files, and others would build trees of SConscripts in the directories.  Each building block would return something self-descriptive, so that most of the time, all the test builder had to do was pass a list of lower-level blocks to a higher-level builder.  Lots and lots and <ins>lots</ins> of details to work out, but there's the 10,000 meter overview.))) 


## Top-level SConstruct

(((Configures, calls top-level SConscript for each variant.  Could call sub-SConscript for common documentation, whatever.))) 


## Top-level SConscript

(((Minor configure, calls sub-SConscripts for include(?), doc(?), src, java, ...))) 


## Include

(((Generates some header files.))) 


## Libraries

(((Generates a number of compilable files and a few local header files.  Files are compiled with the common includes and the local includes.  A library is built.))) 


## Programs

(((Generates a number of compilable files and a few local header files.  Files are compiled with any common includes and the local includes.  A program is built.))) 


## Java

(((Very roughly, populates a source tree and builds a `.jar` file.  Needs input from Java folks.))) 


## Documentation

(((Several flavors, based on source type and target type(s).  Needs input from users to determine most popular scenarios.))) 


## Source

(((Contains some number of sources and/or headers.  Subroutine for other categories.  If not used in the current directory, the sources are used by a higher-level directory and the headers are added to the include list.)))
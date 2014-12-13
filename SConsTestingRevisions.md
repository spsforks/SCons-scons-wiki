
**This is old now -- pretty much all of this has been added to our test infrastructure as of December 2012.** -- [GaryOberbrunner](GaryOberbrunner) 



---

 


<div>
Very preliminary.  Don't hesitate to add your ideas.  Note that the original topic has been extended by a new section on using the test infrastructure with third-party extensions. 

[[!toc 2]] 


# SCons Testing (and QMTest)

In a mailing list message, [StevenKnight](StevenKnight) mentioned that the QMTest framework we're using wasn't giving us all the improved reporting for which we were hoping.  I ([GregNoel](GregNoel)) had been thinking along similar lines, so I promised to create a page of changes that should be made to the SCons testing framework. 


## Turn off QMTest by default

(./) This has already been done. 

**GN:** Change `runtest.py` to default to `--noqmtest` to get rid of the warning that almost always occurs.  If somebody has QMTest installed, they can use `--qmtest` on their command line. 


## Dropping QMTest

**GN:** In brief, I think we should drop QMTest.  I think that it would only take a few modifications to runtest.py to get a better display like QMTest, and we could probably add more features that are directly beneficial to us. 

On the other hand, I'd rather not reinvent the wheel, so we should look carefully at other testing frameworks to see if they make sense for us (or if we can steal ideas from them). 

**SK:**  The reporting wasn't the only thing we were hoping to get from QMTest.  Changing how runtest.py displays its results to look like QMTest is trivial (although I personally don't feel it would be an improvement).  My real hope was that we'd get the ability to run tests in parallel by using a test infrastructure that already had all the thorny details of timing out and capturing output and the like worked out. 

**GN:** (*shudder*) Maybe <ins>_you_</ins> want to run the regression tests in parallel on your incredible box, but <ins>_I_</ins> want some way of throttling back the resource consumption so running the tests doesn't completely tie up my box. 


## Common foundation for unit tests and integration tests

**GN:** I think `unittest` (or some viable alternative[1]) should be made the base class for the SConsTest hierarchy, making those functions available for integrated tests as well. 

[1] There are a number of possible [testing tools on pycheesecake.org](http://pycheesecake.org/wiki/PythonTestingToolsTaxonomy).  As far as I know, only `unittest` is a standard Python module, making it more widespread, but it might be useful to explore other possible tools as well. 

**SK:**  I have a prototype of a `unittest` subclass that executes our stand-alone test scripts.  We could switch to it pretty easily.  It has the advantage of using `unittest`, but that doesn't get us test execution in parallel. 

**GN:** In more detail, there several paradigms that are used in the unit tests that should be gathered into one place (resetting the SCons module is the biggie) and made available to all.  I would gather these into a superclass of `unittest` and then make that a base class of the SCons testing hierarchy. 

**SK:**  Superclass of `unittest`, or subclass?  I agree that collecting more of the scattered infrastructure would be a Good Thing to Do. 

**GN:**  Sigh.  I always get subclass and superclass confused; the word choice just seems backward.  I try to use "derived from" instead to avoid confusion.  So let me make it explicit this way: I think a class, `CommonStuffUsedByANumberOfSConsTests`, should be derived from `unittest` (how can it be a "subclass" if it's got <ins>more</ins> in it than the original class?).  That class would be used in place of `unittest` for our unit tests.  Further, the `TestCmd` class (I think that's the one, the root of all the testing classes) should also be derived from the common class so that the functions in it would be made available to the integration tests.  Is that clear enough? 


## Test times

**GN:** I think the tests should be timed, and the times reported.  The reporting format should be such that it is easily parsed (and sorted) by other tools. 

**SK:**  `runtest.py` already has the ability to time tests using the -t option.  The results are just printed on stdout, though, not structured. 

**GN:** I've never tried it; I should turn it on and see what it does.  As a start, I want to be able to do something as simple as   
{{{    grep ... | sort ... 
</div>
  
 and look at the worst offenders.  It doesn't have to be that complicated.

**GN:** It should be possible to set a threshold and have all tests that take longer than that time be summarized in a separate section.  I think the default should start at about 150 seconds and be lowered over time; in the long run, it should be on the order of 30 or less. 

**SK:**  This is another example of a timing-type thing that would be nice to not have to reinvent, although it doesn't seem like it would be that difficult to just code up. 

**GN:**  Nothing in almost any test framework is all that difficult to code up, it's just that somebody else has already done it.  Our problem is that we've already got so much invested in our own infrastructure that it's easier to go forward with a small addition than to convert to an infrastructure that already has it. 


## Test timeout

**GN:** I think there should be a timeout on the tests, so if they run more than NNN seconds (start with 300 and move down) the test is aborted.  This is mostly aimed at KeyboardInterrupt which still has a tendency to hang, but it could be used as a rude way to force the longer tests to be sped up. 

**SK:**  ...and another... 

**GN:**  Yeah, but this one is <ins>really</ins> annoying, as I might not notice for hours that a test is hung and give it a kick.  Having the framework watch it for me would be a real plus. 


## Tests always report

**GN:** I think tests should always make a positive assertion about what happened, so we don't get any more of those cases where flow accidentally runs off the bottom. 

**SK:**  Agreed.  Any cases now where that doesn't happen are outright bugs. 

**GN:** More specifically, I think identifying at least these classes of test results are useful distinctions (others are possible as well, suggestions welcome): 

1. NO RESULT meaning that the test exited without specifying a status.  This is a test failure and is reported in the summary section. 
1. PASSED meaning that the test ran and everything succeeded. 
1. FAIL-BUT-OK meaning that the test failed, but it's listed in the `.xxx` file, so it's expected to fail. 
1. UNRUNNABLE meaning that the test was not run and nothing can be done to make it work on this hardware/OS combination (e.g., wrong OS, wrong instruction set, wrong Python version, whatever). 
1. MISSING-DEPENDENCY meaning that the test was not run, but some change to the system environment would allow it to be run (e.g., TeX not present but could be, old version of SWIG, VS not installed, whatever).  These tests should be (optionally) summarized (in a section separate from the failing tests) to encourage those missing elements to be installed. 
1. SHOULD-FAIL meaning that the test was run and succeeded but is listed in the `.xxx` file, indicating that it's expected to fail.  These results should be summarized with the other failing tests. 
1. FAILED meaning that the test was run and found some problem.  These tests should be summarized with the other failing tests. 
1. ABORTED meaning that test ran too long or some such.  This should be summarized with the other failing tests. 
**SK:**  I see the utility of these sorts of distinctions, but I'm not sold on lumping them all into different return values from the tests themselves.  It partly depends on what layer is going to interpret the codes, and for what purposes. 

For example, the FAIL-BUT-OK and SHOULD-FAIL strike me as decisions that the test script itself should not make.  It seems much less complicated to have test script just return PASSED or FAILED, and let the harness decide whether that result is expected or not--based on consulting file .xxx, or because the user passed an argument that says, "Ignore failures in this subdirectory," or just because it's Wednesday and the moon is full.  In short, I think we get more flexibility here by keeping the return codes simple and not baking in one way of determining "okayness" into the test scripts (or their infrastructure) themselves. 

I could _maybe_ go with separate return codes for UNRUNNABLE and MISSING-DEPENDENCY, because they do represent valuable information that's only known by the test scripts themselves.  But still, aren't these just different flavors of NO RESULT?  Is there serious added value in pushing the distinction between these three into the test exit code itself, as opposed to, say, just having the tests print a message saying something like, "NO RESULT:  UNRUNNABLE:  can't test Visual Studio on Linux", or "NO RESULT:  MISSING DEPENDENCY:  No D language compiler installed."  Seems like that would provide a pretty easy ability to grep logs for the necessary information, without complicating the exit-code interface between the test scripts and the test harness. 

If I'm overlooking some benefit of pushing these distinctions into the exit code, let me know. 

**GN:**  You are correct that my PoV here was the distinctions the scaffolding should be creating, rather than what the tests should be reporting.  The tests themselves should be only concerned with PASSED, FAILED, UNRUNNABLE, and MISSING-DEPENDENCY. 

If you want the tests to report out UNRUNNABLE and MISSING-DEPENDENCY as NO-RESULT with a patterned message that can be interpreted by the scaffolding to distinguish them, that's fine, although I think it's an extra step, as the test would have to make the distinction to report out the case, then collapse it into a single return code, which the scaffolding would then have to disambiguate.  In any event, it's a detail in the design of the tests. 

I <ins>_do_</ins> think the distinction is useful, as I'd like to see the MISSING-DEPENDENCY cases optionally reported.  Users could look at this report to see what they could install to improve their test coverage. 


# Testing out-of-core tools


## Requirements

A few requirements have to be added for support of those SCons tools that are not part of the core, yet. [RusselWinder](RusselWinder) has initiated the [ToolsIndex](ToolsIndex) page, pointing to various packages that are managed externally with a DVCS (Bazaar, Git, Mercurial,...). This outsourcing helps in keeping the development alive, but also poses some problems for testing: 

* The framework should not rely on the fact, that all tests to be run are kept in the `trunk/test` folder. A tool developer should be able to check out/branch a current version into his workspace (any folder he likes) and then run the provided tests without further ado. 
**SK:**   I don't disagree conceptually, but I'm not clear on the distinction here between "all tests...kept in the `trunk/test` folder" and "check out/branch a current version." 

**DB:**   Here, we are talking about SCons tools that are developed externally. So the user (I at least) wants to check out the basic test framework for SCons to one place, but the DVCS managed code for the module goes into a separate work folder. This makes sense when you work in Eclipse for example...if you check out the tool module into the `trunk/test`, the Subversion plugin picks it up and tries to add the new files automatically. "Run the provided tests" refers to the tests of the external tool only, not the whole suite in `trunk/test`. 

* Since external tools are packages, preferably, they may contain supporting `*.py` files (modules) or even folders as subpackages. We have to be able to distinguish test scripts from files/folders that are part of the tool sources. For this, we could either use naming conventions on the test files/folders or specify their names explicitly in the test scripts. See below, for a more detailed discussion... 

## Minimize checkout for testing

* It would be nice if `runtest.py` (and all other supporting scripts) resided in the `trunk/test` folder, too. Then a user, interested in running tests, would have to check out the "test" folder only...not the complete trunk. 
**SK:**  I agree.  I've wanted to clean up the test/ subdirectory for a while now, mainly by moving all the scons tests into a `test/scons` subdirectory, as a sibling to the current subdirectories for the `sconsign` and `runtest.py` scripts: 


```txt
   +trunk
     +test
       *runtest.py
       +lib          [TestCmd, TestSCons, etc. move here]
       +runtest
       +scons
       +sconsign
       ...
```
**DB:**  I like it. 

**GN:**  Makes sense.  It would take some effort to convert; for one thing, the Build``Bot would have to handle both layouts until all the branches had been converted (which could be a while). 


## Compose test folder from parts

* Support for directory "fixtures" in the test scripts. So far, they use the file-in-a-string approach to create the temporary test folder, which is a pain to work with and debug. It should be possible to set up the complete file/directory structure for a test in a separate folder, e.g. "copied-env-image". Within the test script itself, one could then say: "Use the contents of dir xyz"...as some kind of image. 
**DB:** 
```python
#!python

import TestSCons
test = TestSCons.TestSCons()
test.dir_fixture('copied-env-image')
test.run()
```
Example implementation for `TestCmd.py` (this code is NOT tested yet!): 


```python
#!python

    def dir_fixture(self, srcdir, dstdir=None):
        """Copies the contents of the specified folder srcdir from
        the directory where the script was started, to the current
        working directory.
        The srcdir name may be a list, in which case the elements are
        concatenated with the os.path.join() method. The dstdir is
        assumed to be under the temporary working directory unless it
        is an absolute path name.
        If specified, the dstdir must exist (be created first).
        """
        spath = os.path.join(self._cwd, srcdir)
        if dstdir:
            dstdir = self.canonicalize(dstdir)

        for entry in os.listdir(spath):
            epath = os.path.join(spath, entry)
            dpath = os.path.join(dstdir, entry)
            if os.path.isdir(epath):
                # Copy the subfolder
                shutil.copytree(epath, dpath)
            else:
                shutil.copy(epath, dpath)
```
* The routine `rip_fixture` (as the inverse to dir_fixture) could be used to copy a set up test to a separate directory. This functionality would prove beneficial for debugging or simply converting old test scripts to use "dir_fixtures". (Remark: There is already the `PRESERVE` environment variable that can be set, such that the 
temporary folders do not get deleted afterwards. But using it, one has to manually enter cryptic source paths for copying the contents to another location.) 

* A way of treating the module itself as a test fixture. It would be cool to have 

```python
#!python

test = TestSCons.TestSCons()
test.dir_fixture("basic_test")
test.module_fixture("../*.py","qt4")
```
where the latter copies the current qt4 package into `site_scons/site_tools` of the temporary folder for the test. 


## Discussion: Naming conventions and basic processing

**DB:** For distinguishing test scripts from files/folders that are part of the tool sources, we assume a  directory structure like this: 


```txt
   +qt4
     *__init__.py
     +tests
       *sconstest-copied-env.py
       ...
```
(+ = folder, * = file) 

Test scripts are of the form `sconstest-*.py` and are still executed separately from one another (one file, one test). They are kept in a folder named "tests", located in the root dir of the tool package. 

For handling the "image" folders, we identified two main paths that could be followed..."explicit" vs. an "implicit" method. 

**SK:**  After thinking on this, I don't see why we can't have the best of both worlds.  The automatic copy of the current directory (the "Implicit" method) would still need to use a method like `.dir_fixture()` to do the copy.  The default behavior could be to copy the current directory, but a test that wanted to use a different fixture, or just needed to structure it differently, could override the default `dir_fixtures=` keyword value like so: 


```txt
test = TestSCons.TestSCons(dir_fixtures=['basic_test'])
```
Or completely avoid any initial copy and take care of it later by hand: 


```txt
test = TestSCons.TestSCons(dir_fixtures=None)
# Preparatory steps in here...
test.dir_fixture('basic_test')
```
Does that sound reasonable? 

**DB:**  This sounds good, so +1 from me. But with this approach, we definitely have to touch the treewalk stuff, right? 

**SK:**  We have to touch the treewalk stuff one way or another.  Given that a treewalk is part of the current infrastructure, even if the fixtures are put in separate directories, we would need some way to identify them as fixture directories and avoid treating a `build.py` script in the fixture directory as a test.  Your suggestion seems to implicitly assume that all test scripts would live in one specified directory, or at one specified depth in the heirarchy, so that any deeper subdirectories are test fixtures and not searched.  That could obviously work, but would still mean modifying (or replacing) the treewalk. 

**GN:**  I vote for the implicit approach, at least by default.  I also vote <ins>not</ins> to have all the tests on one level; directories were created by Ghod (in his incarnation as Dennis Ritchie) to organize material, including tests.  I don't want treewalk in the business of figuring out which directories are image folders.  That said, I suggest below that the presence of a `sconstest.skip` file in a directory should cause the directory not to be scanned by treewalk; I think that's a reasonable compromise if such a thing must be done. 

I also like Steven's suggestion for composing the test image.  Extend it so you can cherry-pick among the components of the directory (and include from nearby directories) and it becomes a very powerful concept.  Really cool idea, Steven; I withdraw the idea of a little language in a `sconstest-*.unit` file with a great deal of relief. 

**DB:**  But naming the test scripts `sconstest*.py` is still mandatory, or can we drop this requirement? Apart from this detail, how does development continue/start? Are we ready to collect a list of tasks and prioritize/schedule them? What about documenting our plans in a draft manual for the new testing framework? 

**SK:**  If we drop the requirement for naming test scripts `sconstest*.py`, then how would the treewalk identify which `*.py` scripts are test scripts to be executed, and which `*.py` scripts are part of a `dir_fixture` and should _not_ be executed as tests?  I'm willing to entertain other ways of identifying test scripts, but I don't have a clear idea of what you're suggesting as a different way to make this distinction.  Explicit manifest lists of test scripts?  Some prefix other than `scontest*.py`?  A specific directory layout, such that test scripts live at a one layer of the tree and `*.py` lower in the tree are (presumably) within fixtures?  Separate subdirectories for test scripts vs. fixtures?  What's your vision? 

**DB:**  I don't have a clear vision...that`s why I asked the question in first place ;). I probably still have the explicit approach, with all test scripts in one dir and the dir_fixtures underneath, in the back of my head. After adding the `sconstest.skip` file to the scheme, it seemed to me as if we could get rid of the prefix. But you are right of course, this will not work if we want to support non-test scripts in the dir_fixture folders. So, everything is fine from my side... 

**DB:** ...until we try to set up a test folder like this: 


```txt
   +tests
     *sconstest-with-files-in-strings.py
     +test-as-dir-fixture
       *sconstest-implicit-copy.py
       ...
```
When we have both in a test dir, old single files and new implicit folders...how do we distinguish between the different types of `sconstest*.py` files for the treewalk? It has to "skip" the `tests` folder for an implicit copy, although there is a `sconstest*.py`. <del>My brain hurts!</del> 

Answering myself: then the file `sconstest-with-files-in-strings.py` would have to use the `dir_fixtures=None` option such that no implicit copy is made. Sorry... 

**GN:** Er, no.  The first file would simply be named `files-in-strings.py` or some such, <ins>without</ins> a `sconstest-` prefix.  The scan to find tests is pretty dumb in that it only looks at filenames, not at their content.  In particular, it doesn't run the tests as it goes, but simply collects them for a subsequent pass that will run them (after sorting them so they always occur in a predictable order).  It would have no idea that the test had a `dir_fixtures=None` option. 

**DB:** From the discussion with Steven, four comments above, I understood that we require to have ALL test scripts named `sconstest*.py`. Wouldn't this allow the scan for tests to keep being dumb, by looking for the `sconstest*.py` pattern only? The distinction between "dir_fixture or not" can then be made when the actual test is carried out. Else, we would have different naming conventions for the two test script types (I'd like to have this consistent). 

**SK:** I think this is another area where we can have the best of both, at least for the transition.  GN is right that the directory walk doesn't introspect on any contents to determine what is or isn't a test script.  DB is right that my intention is to move us to a uniform convention.  But at least for the transition, I'm planning to write the walk so that it behaves like it does currently (any `*.py` script is a test script) _unless_ it finds any file named `sconstest*` in a directory, at which point it assumes that it's part of the "new-style" of test and looks only for `sconstest*.py` and skips walking subdirectories.  This is probably more convoluted to describe than it is to just go ahead and code it and start converting a few tests.  I think the concrete example will make things pretty clear.  (Plus, I'll have to write `test/runtest/*.py` scripts for this behavior, anyway...) 

**DB:** I, personally, do not need a transition phase. We can do it the way you suggested, this is absolutely fine with me. But I don't see why we can't rename all the existing tests by adding a `sconstest-` prefix and patch the test script to accept these only, in one swoop...like some sort of atomic operation. This is a first step (phase 1), completely decoupled from the other planned extensions like dir_fixtures and the support of `sconstest.skip` files. Or am I missing something here? 


### Explicit

**SK:** The `sconstest*` scripts are kept outside of the "image" folders, which contain readily-prepared files for a test (or a part of them). 

Folder structure: 


```txt
  +qt4
    *__init__.py
    +tests
      *sconstest-copied-env.py
      +copied-env-image
        *SConstruct
        *SConscript
        ...
```
Within the test script `sconstest-copied-env.py`, the "explicit" call of the `dir_fixture` method copies the folder's files/contents to the temporary test folder. 


```txt
  import TestSCons
  test = TestSCons.TestSCons()
  test.dir_fixture('copied-env-image')
  test.run()
```
Pros: 

* All `sconstest*` files are at the same folder level, whether they use the old file-in-a-string approach or dir_fixtures. 
* Supports merging different folders into a single test for dir_fixtures. 
Cons: 

* You have to specify each folder explicitly. 

### Implicit

**SK:** The test scripts `sconstest*.py` are kept inside the test folders. Their mere existence triggers the copying of the dir's files to the temporary test folder automatically, hence "implicit". 


```txt
   +qt4
     *__init__.py
     +tests
       +copied-env
         *sconstest-copied-env.py
         *sconstest-another-test.py
         *SConstruct
         *SConscript
```
The fixture directories probably end up being named for the specific test configurations they contain, not specific tests, and you can have multiple test scripts that use the same fixture directory. (Of course, in real life there will probably be a lot of directories with single test scripts.) 

The `TestSCons()` invocation would copy the contents of the script's directory tree, ignoring anything with a `sconstest*` prefix. This way, the test scripts are still identifiable in a directory walk as distinct from the other `*.py` scripts that might be in a given test fixture directory. 

For the Pros and Cons, simply negate the lists for the "Explicit" method above ;). 


### Tree walk

Ideas by [GregNoel](GregNoel): 

**GN:** Assume for the moment that the treewalk is a generator that returns a duple (tag,name) and let me recast the types of tests like this: 

* (DIR,[tests]) if there's one or more files `dir/sconstest-*.py` 
* (FILE,name) for any file `*.py` 
where the former takes precedence over the latter. 

Then we can talk about extending this to other match types: 

* (UNIT,[]) if there's a file named `dir/sconstest.skip` 
* (UNIT,[tests]) if there's one or more `dir/sconstest-*.unit` 
* (ARCHIVE,name) for any file `sconstest-*.tz` (or `*.tz?`) 
* (ARCHIVE,name) for any file `sconstest-*.zip` (or `*.zip?`) 
}}} 

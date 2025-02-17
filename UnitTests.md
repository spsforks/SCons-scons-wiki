Want to have "scons test" run your unit tests? 

Here are two suggestions: 

* running with an Alias 
* running with Command 
See [http://spacepants.org/blog/scons-unit-test](http://spacepants.org/blog/scons-unit-test) for another suggestion. 

To have the process of adding unit test nicely encapsulated into an scons Tool, see the section below - "Unit Test integration with an scons Tool". 

[http://snappaction.blogspot.com/2007/02/scons-unit-testing-with-cxxtest-in.html](http://snappaction.blogspot.com/2007/02/scons-unit-testing-with-cxxtest-in.html) shows a way to make adding UnitTests very simple by using CxxTest and automatically finding unit tests in a test directory. 


# Alias


```python
# Build one or more test runners.
program = env.Program('test', 'TestMain.cpp')

# Depend on the runner to ensure that it's built before running it.
test_alias = Alias('test', [program], program[0].path)

# Simply required.  Without it, 'test' is never considered out of date.
AlwaysBuild(test_alias)
```
Check out [PhonyTargets](PhonyTargets) for another way of defining a 'test' target. 

Note that `program[0].path` might give issues when running on OS'es that do not explicitly search for executables in the current directory (Unix-like OS'es where you explicitly need to add '.' as a search path). In that case, you can use the following: 

```python
# Build one or more test runners.
program = env.Program('test', 'TestMain.cpp')

# Depend on the runner to ensure that it's built before running it - Note: using abspath.
test_alias = Alias('test', [program], program[0].abspath)

# Simply required.  Without it, 'test' is never considered out of date.
AlwaysBuild(test_alias)
```
This doesn't work if your unit test program depends on a certain shared library that resides on the same folder as the unit test program since the environment variable LD_LIBRARY_PATH needs to be edited.

# Alias with Command
If you want your unit test being invoked only on demand, the following works for me (java unit test)

```python
# Launches ant -q when typing "scons"
env.Command(
    target="compiled.txt",
    source=mySources,
    action=["ant jar-types  -f build.xml", "type NUL > " + "compiled.txt"],
)

# Launches ant junit-tests when typing "scons runtest"
testAlias = env.Alias(
    "runtest", "", "ant run -f " + os.path.join(javaTestRoot, "build.xml")
)
env.AlwaysBuild(testAlias)
```

# Command

Another idea is inspired on the boost build V2 system, that will create a file stamp if the unittest has run succesful. If it ran succesfull (exit code 0) and there is nothing changed, there is no need to run the unit test again. 


```python
def runUnitTest(env,target,source):
   import subprocess
   app = str(source[0].abspath)
   if not subprocess.call(app):
      with open(str(target[0]),'w') as f:
          f.write("PASSED\n")

program = env.Program('test', 'TestMain.cpp')
Command("test.passed",'test', runUnitTest)
```

# Note by Dov Grobgeld 2005-12-18

I modified the method mentioned above in order to be able to use it in an SConscript file without needing to define `runUnitTest` in each SConscript file. Here is what I did: 

In the SConstruct file: 

```python
def builder_unit_test(target, source, env):
    app = str(source[0].abspath)
    if os.spawnl(os.P_WAIT, app, app)==0:
        open(str(target[0]),'w').write("PASSED\n")
    else:
        return 1

# Create a builder for tests
bld = Builder(action=builder_unit_test)
env.Append(BUILDERS={'Test':  bld})
```
The test may then be declared in each of the library SConscript files by doing: 

```python
Import('env')
# Build the library
...
# Test the library
test_lib = env.Program('test_library', ['test_library.cpp'])
env.Test("test.passed", test_lib)
env.Alias("test", "test.passed")
```
Now I am going to build a builder for automatically running valgrind/purify as well. 


# Note by Matt Doar 2007-01-24

I modified Dov's work to support comparing the results of running a test to a file containing the expected results. I also added an option to regenerate the expected results file. This is working nicely for us in practice. 

In the SConstruct file, first add the boilerplate for the new regenerate option: 

```python
# Add some command line options to SCons to support different build types.
# Example of using an option: scons regenerate=1 ...
command_line_options = Options()
command_line_options.AddOptions(
    ('regenerate', 'Set to 1 to regenerate the expected results of unit tests', 0),
)
# The default build environment, used for all programs
env = Environment(
    options = command_line_options,
)
# Generate the "scons --help" text for the options
Help(command_line_options.GenerateHelpText(env))
# Used in UnitTest
env['REGENERATE'] = 0
if str(ARGUMENTS.get('regenerate', 0)) == '1':
    env['REGENERATE'] = 1
```
Now add the [UnitTest](UnitTest) builder to the environment: 

```python
import os
def run(cmd, env):
    """Run a Unix command and return the exit code."""
    res = os.system(cmd)
    if (os.WIFEXITED(res)):
        code = os.WEXITSTATUS(res)
        return code
    # Assumes that if a process doesn't call exit, it was successful
    return 0

def unit_test_emitter(target, source, env):
    base, ext = os.path.splitext(source[1].abspath)
    source.append(base + '.expected')
    return (target, source)

def UnitTest(target, source, env):
    '''Run some app with an inputfile and compare the output with a .expected file
    containing the expected results.'''
    app = str(source[0].abspath)
    inputfile = str(source[1].abspath)
    base, ext = os.path.splitext(inputfile)
    expected = base + '.expected'
    # Output can come on both stdout and stderr
    cmd = app + ' ' + inputfile + ' 2>&1 | diff ' + expected + ' -'
    if env['REGENERATE'] == 1:
        print "Regenerating expected results file: " + expected
        cmd = app + ' ' + inputfile + ' &> ' + expected
    res = run(cmd, env)
    # If the test passed, create the target file so the test won't be run again
    if res == 0:
        open(str(target[0]),'w').write("PASSED\n")
    return res

# Create a builder for running unit tests
bld = Builder(
    action=Action(UnitTest, varlist=["REGENERATE"]), emitter=unit_test_emitter
)
env.Append(BUILDERS={"UnitTest": bld})

# NOTE: Only apply changes to env above here
Export('env')
```
Using the new Builder in an SConscript file: 


```python
Import('env')
# removed the code to build myapp ...
# Note: this test will look for a file named inputfile1.expected so you may have
# to touch that file to bootstrap the creation of the test.
mytest1 = env.UnitTest("tests/test1.passed", [myapp, 'inputfile1.txt'])
Alias("mytest1", mytest1)
```
First generate the expected results file with "scons regenerate=1 mytest1".  Then run the unit test with "scons mytest1". 


# Unit Test integration with an scons Tool

_Section added by Chris Foster, 23-7-2007_ 

I wanted to integrate unit testing into the [aqsis](http://www.aqsis.org) scons build system, in a way which made it as easy as possible to add tests from our Sconstruct files.  I ended up writing an scons Tool (see listing below) to encapsulate adding the appropriate things to an environment, building on Dov's work above. 

The nice thing about this is that you can very cleanly create add a test environment which includes the tool, and add any libraries which you need to link with to that test building environment.  Here's what a section of a main SConstruct file might look like, when using boost.test for testing: 


```python
# make an initial construction environment
env = Environment()
Export('env')
# Set up the test environment.  We copy the environment so that we can add the
# extra libraries needed without messing up the environment for production
# builds.
#
# Here we use boost.test as the unit testing framework.
testEnv = env.Clone()
testEnv.Tool(
    'unittest',
    toolpath=['build_tools'],
    UTEST_MAIN_SRC=File('build_tools/boostautotestmain.cpp'),
    LIBS=['boost_unit_test_framework']
)
Export('testEnv')
# grab stuff from sub-directories.
env.SConscript(dirs=['onelib'])
```
In some sub-directory, onelib, you can then add tests quite easily, as follows: 


```python
# Unit tests
Import('testEnv')
testEnv = testEnv.Clone()
testEnv.AppendUnique(LIBPATH=[env.Dir('.')], LIBS=['one'])
testEnv.PrependENVPath('LD_LIBRARY_PATH', env.Dir('.').abspath)
# We can add single file unit tests very easily.
testEnv.addUnitTest('two_test.cpp')
# also, multiple files can be compiled into a single test suite.
libone_test_sources = Split("one_test.cpp two_test.cpp")
testEnv.addUnitTest('libone_test_all', libone_test_sources)
# all the tests added above are automatically added to the 'test' alias.
```
Because the tool automatically adds Aliases, it's easy to run a particular test, 


```bash
$ scons two_test
```
or the whole set of tests: 


```bash
$ scons test
```
Here's the code for the tool: 


```python
import os

def unitTestAction(target, source, env):
    """Action for a 'UnitTest' builder object.

    Runs the supplied executable, reporting failure to scons via the test exit
    status.
    When the test succeeds, the file target.passed is created to indicate that
    the test was successful and doesn't need running again unless dependencies
    change.
    """
    app = str(source[0].abspath)
    if os.spawnle(os.P_WAIT, app, env["ENV"]) == 0:
        with open(str(target[0]), "w") as f:
            f.write("PASSED\n")
    else:
        return 1

def unitTestActionString(target, source, env):
    """
    Return output string which will be seen when running unit tests.
    """
    return "Running tests in " + str(source[0])

def addUnitTest(env, target=None, source=None, *args, **kwargs):
    """Add a unit test

    Args:
        target - If the target parameter is present, it is the name of the test
            executable
        source - list of source files to create the test executable.
            any additional parameters are passed along directly to env.Program().

    Returns:
        The scons node for the unit test.

    Any additional files listed in the env['UTEST_MAIN_SRC'] build variable are
    also included in the source list.
    All tests added with addUnitTest can be run with the test alias:
            "scons test"
    Any test can be run in isolation from other tests, using the name of the
    test executable provided in the target parameter:
            "scons target"
    """
    if source is None:
        source = target
        target = None
    source = [source, env["UTEST_MAIN_SRC"]]
    program = env.Program(target, source, *args, **kwargs)
    utest = env.UnitTest(program)
    # add alias to run all unit tests.
    env.Alias("test", utest)
    # make an alias to run the test in isolation from the rest of the tests.
    env.Alias(str(program[0]), utest)
    return utest

# Functions used to initialize the unit test tool.
def generate(env, UTEST_MAIN_SRC=[], LIBS=[]):
    env["BUILDERS"]["UnitTest"] = env.Builder(
        action=env.Action(unitTestAction, unitTestActionString), suffix=".passed"
    )
    env["UTEST_MAIN_SRC"] = UTEST_MAIN_SRC
    env.AppendUnique(LIBS=LIBS)
    # The following is a bit of a nasty hack to add a wrapper function for the
    # UnitTest builder, see http://www.scons.org/wiki/WrapperFunctions
    from SCons.Script.SConscript import SConsEnvironment

    SConsEnvironment.addUnitTest = addUnitTest

def exists(env):
    return 1
reformatted -
All done! ✨ 🍰 ✨
1 file reformatted.
```

# scons check with CxxTest

**While you can still use the code here, I have since created a CxxTest builder. see here: [CxxTestBuilder](CxxTestBuilder)** 

I struggled with CxxTest and scons for a while, and this is the closest thing to 'make check' I have been able to come. It's quite close, I believe, and I tried to minimize the amount of code it took. 

I started with suggestions from here: [http://spacepants.org/blog/scons-unit-test](http://spacepants.org/blog/scons-unit-test), and modified the general idea somewhat for it to work with the CxxTest c++ test framework [http://cxxtest.sourceforge.net/](http://cxxtest.sourceforge.net/). 

Since I am quite new to scons, I wasn't able to figure out how exactly to put my extensions into a separate file to be sourced by scons automatically, and I hope someone can supply that knowledge. 

This also does not support all CxxTest functionality. I only built in what I required, but the result is neat and simple. 

Without further ado, here is the code from my SConstruct: 


```python
from SCons.Script.SConscript import SConsEnvironment

env = Environment()
# required for the cxxbuilder.
# If you use the normal header files, just use .h here.
env["TEST_SUFFIX"] = ".t.h"
# ----------------------------------
# cxx test builder
# ----------------------------------
CxxTestCpp_bld = Builder(
    action="./cxxtestgen.py --error-printer -o $TARGET $SOURCE",
    suffix=".cpp",
    src_suffix="$TEST_SUFFIX",
)
env["BUILDERS"]["CxxTestCpp"] = CxxTestCpp_bld

def UnitTest(environ, target, source=[], **kwargs):
    """UnitTest wrapper function

    a wrapper around the Program call that adds the result
    of the build to the tests-to-run target.
    """
    test = environ.Program(target, source=source, **kwargs)
    environ.AlwaysBuild("check")
    environ.Alias("check", test, test[0].abspath)
    return test

SConsEnvironment.UnitTest = UnitTest

def CxxTest(environ, target, source=None, **kwargs):
    """A wrapper that supplies the multipart build functionality
    that CxxTest requires.
    """
    if source is None:
        source = Split(target + environ["TEST_SUFFIX"])
    sources = Split(source)
    sources[0] = environ.CxxTestCpp(sources[0])
    return environ.UnitTest(target, source=sources, **kwargs)

SConsEnvironment.CxxTest = CxxTest
```

## Usage

The function is modelled to be called as the Program() call is: 

`env.[CxxTest](CxxTest)('target_name')` will build the test from the source `target_name` + `env['TEST_SUFFIX']`, 

`env.[CxxTest](CxxTest)('target_name', source='test_src.t.h')` will build the test from `test_src.t.h` source, 

`env.[CxxTest](CxxTest)('target_name, source=['test_src.t.h', other_srcs])` builds the test `.cpp` from `source[0]` and passes other sources to the Program call verbatim. 

You may also add additional arguments to the function. In that case, they will be passed to the actual Program builder call unmodified. Convenient for passing different CPPPATHs and the sort. 

Anyway, this is the way I call it: 


```python
# #/src/test/SConscript
Import('env')
env['CPPPATH'] = '#' # CxxTest headers are in #/cxxtest/
env.CxxTest('test_quaternion', source='Quaternion.t.h')
env.CxxTest('test_utility', ['utility.t.h', '../utility.cpp'])
```
I run the tests by typing `scons check`. 

The tests do not compile by `scons .` (which is identical to the behaviour of make check) 

If the tests are out of date, they compile - scons dependency tracking works. 

Any suggestions, improvements and/or criticism are welcome. As I said, I am new to scons. 

Cheers, [GasperAzman](GasperAzman) 

-- Comment on Gasper's code by Matt Doar: 

Just what I wanted, and nicely done, thank you. However, I think that the last line in the CxxTest function should be 


```python
return environ.UnitTest(target, source=sources, **kwargs)
```
instead of 


```python
return env.UnitTest(target, source=sources, **kwargs)
```
to make sure that the correct env is propagated to the Program. 

-- Thanks Matt, good spot. It worked in my code due to moonphase. I corrected the code above. Thanks, [GasperAzman](GasperAzman) 


# SConstructs: unit and functional testing

I'm developing quite a complex build process. To have "scons test" isn't an issue for me. Instead, I'm concenrating on checking established internal dependencies, such as: 

* a builder is really added, 
* an user-friendly alias is defined, 
* the source files, the target and the action are right, 
* additional files to delete are registered. 
Here are blog entries (probably should be copied here instead of linking): 

* [http://uucode.com/blog/2006/07/05/unit-testing-for-scons/](http://uucode.com/blog/2006/07/05/unit-testing-for-scons/) 
* [http://uucode.com/blog/2006/07/07/scons-testing-additional-files-to-clean/](http://uucode.com/blog/2006/07/07/scons-testing-additional-files-to-clean/) 
And here are some hints on functional (integration) testing (running scons and checking that the result is as expected): 

* [http://uucode.com/blog/2006/07/17/testing-scons-processes/](http://uucode.com/blog/2006/07/17/testing-scons-processes/) 
* [http://uucode.com/blog/2006/07/29/hijacking-sconsign/](http://uucode.com/blog/2006/07/29/hijacking-sconsign/) 
* [http://uucode.com/blog/2006/08/12/fixing-build-signatures/](http://uucode.com/blog/2006/08/12/fixing-build-signatures/) 
* [http://uucode.com/blog/2006/08/24/scons-signatures-for-python-actions/](http://uucode.com/blog/2006/08/24/scons-signatures-for-python-actions/) 

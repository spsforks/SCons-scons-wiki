# Using a Source Generator to Add Targets Dynamically

Here's what we do to add targets dynamically, from a list which isn't known in advance. 

The scenario in our case is you have a source generator 'srcgen' which is built by scons from sources in the usual way.  It puts out a bunch of other sources whose names can't be predicted in advance.  In our case it also puts out a src-list.text file.  Call the generated sources srcA, srcB, etc. 

Now you want to (say) compile each of those srcX into binX and include those in your final product. 

In our SConscript we do this: 

```python
srcgen = env.Program("srcgen", ...)
srclist = env.Command("src-list.txt", srcgen, "$SOURCE $SRCGEN_ARGS > $TARGET")
dummy = env.ScanSrcs("#dummy-target", srclist, SCANSRCS_FUNC=add_target)
env.AlwaysBuild(dummy)
Alias("TopLevelAlias", dummy)
```
Now when scons goes to build `TopLevelAlias`, the dependencies are set so it builds `srcgen`, runs it to produce the `srclist` (and the other sources), and then runs `ScanSrcs` on the `srclist`.  The interesting thing is that the `ScanSrcs` function will be called _during the build phase_ after its dependencies are up-to-date, rather than while the SConscript is being read.  It will call `Program()` or `SharedLibrary()` or whatever builders we want, which will update the dependency graph while scons is building.  Sounds scary, but it works. 

We made our `ScanSrcs` parameterized so it could be reused.  Note that it's practically all plain python, no SCons calls at all except adding the Builder and checking for construction variables. 

```python
def scansrcs(target, source, env):
    """Scans through the list in the file 'source', calling
    env['SCANSRCS_FUNC'](env,line) on each line of that file.
    Calls env['SCANSRCS_PREFUNC'](env,source) once before scanning. 
    """
    if SCons.Util.is_List(source):
        source = source[0]
    if "SCANSRCS_FUNC" not in env:
        raise Error, "You must define SCANSRCS_FUNC as a scons env function."
    # Call the pre-func
    if "SCANSRCS_PREFUNC" in env:
        env["SCANSRCS_PREFUNC"](env, source.path)

    try:
        f = open(source.path, "r")
    except:
        print "scansrcs: Can't open source list file '%s' in %s" % (
            source.path,
            os.getcwd(),
        )
        raise
    # Scan through the lines
    for line in f:
        src = line.strip()
        # print "Found " + src
        try:
            env["SCANSRCS_FUNC"](env, src)
        except:
            print "SCANSRCS func raised exception:"
            raise
    f.close()


# This is a funky builder, because it never creates its target.
# Should always be called with a fake target name.
env.Append(BUILDERS={"ScanSrcs": Builder(action=scansrcs)})
```

And finally, here's the function `_add_target_`, called from `ScanSrcs`, that does the real work: 

```python
def add_target(env, source):
    """Add scons commands to build a new target from a scanned src generator list file."""
    # Build the new targets in the build dir:
    target = "#" + join(
        env["BUILDDIR"], basename(re.sub(r"\.c$", env.get("PROGSUFFIX", ""), source))
    )
    tgt = env.Program(target, source)
    env.Depends(tgt, "#dummy-target")
    p = env.Install(env["INSTALLDIR"], tgt)
    Alias("TopLevelAlias", p)
```
Note that it adds new Nodes for the program target and the installed version of it, and also adds that to the TopLevelAlias.  This way as the scanner runs scons knows that the new target doesn't exist or is out of date, so it marks the TopLevelAlias out of date; then scons comes around again to look at TopLevelAlias and discovers it now needs to build 'binA', which depends on 'srcA' and so it builds it and installs it as we want it to. 

The above has been cut down from our real version, but I hope it shows how it can be done, and that it's not really that hard. 

---

Here is a version of the code above that you can copy & paste, ready to edit. I added some imports and altered some small stuff that was too related to the code's origins. Now this example works as soon as you change the file names to match those in your project. 

```python
import types
import os.path
import re

env = Environment(BUILDDIR="bin", INSTALLDIR="installdir")

def scansrcs(target, source, env):
    """ Scans through the list in the file 'source', calling
    env['SCANSRCS_FUNC'](env,line) on each line of that file.
    Calls env['SCANSRCS_PREFUNC'](env,source) once before scanning.
    """
    if type(source) is list:
        source = source[0]
    if "SCANSRCS_FUNC" not in env:
        raise Error, "You must define SCANSRCS_FUNC as a scons env function."
    # Call the pre-func
    if "SCANSRCS_PREFUNC" in env:
        env["SCANSRCS_PREFUNC"](env, source.path)

    try:
        f = open(source.path, "r")
    except:
        print "scansrcs: Can't open source list file '%s' in %s" % (
            source.path,
            os.getcwd(),
        )
        raise
    # Scan through the lines
    for line in f:
        src = line.strip()
        # print "Found " + src
        try:
            env["SCANSRCS_FUNC"](env, src)
        except:
            print "SCANSRCS func raised exception:"
            raise
    f.close()

# This is a funky builder, because it never creates its target.
# Should always be called with a fake target name.
env.Append(BUILDERS={"ScanSrcs": Builder(action=scansrcs)})

def add_target(env, source):
    """Add scons commands to build a new target from a scanned src generator list file."""
    # Build the new targets in the build dir:
    target = "#" + os.path.join(
        env["BUILDDIR"],
        os.path.basename(re.sub(r"\.c$", env.get("PROGSUFFIX", ""), source)),
    )
    tgt = env.Program(target, source)
    env.Depends(tgt, "#dummy-target")
    p = env.Install(env["INSTALLDIR"], tgt)
    Alias("TopLevelAlias", p)

srcgen = env.Program("srcgen", "srcgen.c")
srclist = env.Command("src-list.txt", srcgen, "./$SOURCE $SRCGEN_ARGS > $TARGET")
dummy = env.ScanSrcs("#dummy-target", srclist, SCANSRCS_FUNC=add_target)
env.AlwaysBuild(dummy)
Alias("TopLevelAlias", dummy)
```
If you have subsequent build steps that are dependent on results similar to the above see [NonDeterministicDependencies](NonDeterministicDependencies) 

# A simple Builder, and its evolution to a Tool

This small article discusses the different possible approaches while trying to teach SCons how to compile and process exotic file types, in order to support new tools. This can be a compiler for a sparsely used language like [Befunge](http://www.esolangs.org/wiki/Befunge) or a documentation processor like [AsciiDoc](https://asciidoctor.org/docs/what-is-asciidoc/), which aren't supported by the SCons core.

Based on my personal experiences (and preferences!) I outline some of the basic points you have to look out for, when implementing an SCons Tool. Visit the [Tools Index](http://www.scons.org/wiki/ToolsIndex) for a list of currently available extension packages, which can serve as examples for your own code. 

Throughout the text I'll use a rather unknown compiler as example, JAL. This acronym stands for "Just Another Language", and is an alternative to programming PIC microprocessors in Assembler (shudder!). The language itself reminds a bit of PASCAL, decide for yourself whether this is a good or bad thing. `;)` 

If you actually want to give the JAL compiler a try, it can be downloaded from [http://www.casadeyork.com/jalv2/](http://www.casadeyork.com/jalv2/). 


## Start with the command line

From the JAL input file `alarm.jal` the command "`jalv2 alarm.jal`" creates an `*.asm` file, named `alarm.asm`, for the PIC microcontroller (and some other files as well, but let's leave that for later now). As a first simple approach you could try to implement this call as a `Command()` action (chap. 18 _Not Writing a Builder: the Command Builder_ in User Guide) in your SConstruct: 


## Command wrapper


```python
env.Command("alarm.asm", "alarm.jal", "/opt/jalv24n/bin/jalv2 -asm $TARGET $SOURCE")
```
or
```python
env.Command('alarm.asm','alarm.jal','/opt/jalv24n/bin/jalv2 $SOURCE')
```
Both of these calls would properly execute the JAL compiler for the source file in question, but let's look at some of the advantages and disadvantages of this approach. 

**Pros**: In advance to `make`, we now have content-based (MD5 signature) change detection. 

**Cons**: This setup might be okay for a single project with only one input file, but we have a lot of hardwired code here. Application, source and target are given with their full names, which doesn't make the code eligible to reuse very much. 


## Simple Builder

As a next step, we define a simple `Builder()` named `jalbld` (chap. 17 _Writing Your Own Builders_). We call the constructor of the `Builder` class and pass the basic command line as argument to the `action` parameter. Using the `suffix` specifications, we can leave out the suffixes for our target and source files (cf. the following call of the `Jal` function, sect. 17.3 _Letting SCons Handle the File Suffixes_). Note how the Builder gets appended to the current Environment via the `BUILDERS` variable. This is mandatory to make the `Jal` method accessible. 


```python
jalbld = Builder(
    action="/opt/jalv24n/bin/jalv2 $SOURCES",
    suffix=".asm", src_suffix=".jal"
)
env = Environment(BUILDERS={"Jal": jalbld})

env.Jal("alarm", "alarm")
```
**Pros**: We now have support for automatic suffixes, which requires less typing. 

**Cons**: The reusability got improved significantly, but we still have to paste the definition of the builder into each `SConstruct`, or can hide it in a Python module that we would have to import each time. 


## First version of a Tool

Next step of our evolution is a Tool. Tools are SCons' way of changing and modifying a given Environment. They can alter Environment variables or add Builders, which are required for the task at hand. 

Again we construct a Builder `_jal_builder`, with pretty much the same syntax as before. For a proper Tool we also have to define two functions `exists()` and `generate()`. The first method can be called in order to detect whether all the preconditions for our Tool are met. For example, we could check whether the `jalv2` executable is available in the current `PATH`. For now we always return a "`1`", so the loading of the Tool never fails. However, the call of the `Jal` method may stop with an error, depending on whether the compiler can be found at runtime or not. 

The `generate` routine is responsible for the actual changes to the Environment. This is where we add the Builder to its new Environment and make it accessible under the name `Jal`. 

Note: There is no rule that says: "There must be only one Builder for each Tool." Most of the currently existing Tools actually add several Builders to your Environment (see also [#special](ToolsForFools) for a syntax example). 


```python
import SCons.Builder

#
# Builders
#
_jal_builder = SCons.Builder.Builder(
    action="/opt/jalv24n/bin/jalv2 $SOURCES",
    suffix=".asm",
    src_suffix=".jal"
)

def generate(env):
    """Add Builders and construction variables to the Environment."""
    env["BUILDERS"]["Jal"] = _jal_builder

def exists(env):
    return 1
```
That's all, nothing else needed. You can save this file as `__init__.py` (this is not the SConstruct anymore!) and copy it to your `site_scons/site_tools/jal` folder. For more infos about how and where to install your Tools, visit [Tools Index](http://www.scons.org/wiki/ToolsIndex) in the SCons wiki and read section 17.7 _Where To Put Your Custom Builders and Tools_ please. 

For using our new "`jalv2`" Tool we would write an SConstruct, something like this: 


```python
env = Environment(tools=['jal'])
env.Jal('alarm','alarm')
```
Now isn't that much simpler, for you as developer **and** your users? Still we can identify a few problems that we would probably like to get rid of: The path to the executable is hardcoded,  and there is no support whatsoever for additional command line options. 


# Prettying it up


## Detect executable and add Environment variables

First the new code: 

> **Note**
Previous iterations of this article showed inheriting from `SCons.Warnings.Warning`. The base SCons warning class was renamed to `SConsWarning` as of SCons 4.0.0 to avoid conflicts with the Python language `Warning` class.


```python
# MIT License
#
# Copyright The SCons Foundation
#
# ...

"""
Tool-specific initialization for the JALv2 compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

import SCons.Action
import SCons.Builder
import SCons.Util

class ToolJalWarning(SCons.Warnings.SConsWarning):
    pass

class JalCompilerNotFound(ToolJalWarning):
    pass

SCons.Warnings.enableWarningClass(ToolJalWarning)

def _detect(env):
    """Try to detect the JAL compiler"""
    try:
        return env["JAL"]
    except KeyError:
        pass

    jal = env.WhereIs("jalv2") or env.WhereIs("jal")
    if jal:
        return jal

    raise SCons.Errors.StopError(JalCompilerNotFound, "Could not detect JAL compiler")
    return None

#
# Builders
#
_jal_builder = SCons.Builder.Builder(
    action=SCons.Action.Action("$JAL_COM", "$JAL_COMSTR"),
    suffix="$JAL_ASMSUFFIX",
    src_suffix="$JAL_SUFFIX",
)

def generate(env):
    """Add Builders and construction variables to the Environment."""

    env["JAL"] = _detect(env)
    env.SetDefault(
        # Additional command-line flags
        JAL_FLAGS=SCons.Util.CLVar("-quiet"),
        # Suffixes/prefixes
        JAL_SUFFIX=".jal",
        JAL_ASMSUFFIX=".asm",
        # JAL command
        JAL_COM="$JAL $JAL_FLAGS $SOURCES",
        JAL_COMSTR="",
    )

    env["BUILDERS"]["Jal"] = _jal_builder

def exists(env):
    return _detect(env)
```
We now added a small documentation header at the top of our Tool module, together with the well-known SCons copyright. 

What else has changed? 

*  The method `exists` really tries to detect the JALv2 executable and calls `_detect` for this task. As can be seen in this example, the return value doesn't have to be a bool or int. Any non-zero value, like the full path to the found executable, should work fine. 

*  In `_detect`, we try to read the `JAL` var from the current SCons Environment. As a fallback we search in all the `PATH` locations with `WhereIs` and prefer the latest version `jalv2` over its predecessor `jal`. If no application can be found, the method throws an error exception. 

*  In `generate` we now use variables for the path/name of the executable, its flags and the file suffixes. An additional flag `-quiet` is used as default to make the output less verbose. 

*  The `_jal_builder` now uses `SCons.Action.Action` instead of a simple Action string. Like this we can add the `*COMSTR` for printing a special build message if required, e.g. "`JAL_COMSTR='Creating ${TARGET}...'`". 

This is starting to develop into a very cool Tool, so what else could a user ask for? 

Well, so far we didn't care about side effect files. The real JAL compiler doesn't only create an ASM file as its output, it also spits out a `.hex` and `.cod` file in each run. With our current code, these additional files are simply unknown to SCons and wouldn't get removed properly on a cleanup with "`scons -c`". Not very elegant... 


## Using Emitters

Usually each build command is expected to produce the given list of targets from the specified list of source files. For example, 

```python
env.Object('foo.o', 'foo.c')
```
creates the object `foo.o` (target) from `foo.c` (source), and no other files are involved in this step. With our JAL compiler this isn't true. Although we only say 

```python
env.Jal('foo.asm', 'foo.jal')
```
we get the files `foo.hex` and `foo.cod` as additional targets, also known as _side effects_.  

For redefining this common rule in SCons there is the concept of an Emitter (see section 17.6 _Builders That Modify the Target or Source Lists Using an Emitter_). It tells the system which files go in for the build step and what comes out after the job has finished. The default Emitter gets the list of sources and targets, as given by the user in the SConstruct or SConscript, and passes them on unchanged. But for handling side effect files we can override this behaviour by defining our own Emitter, which we are about to do now: 

```python
# MIT License
#
# Copyright The SCons Foundation
#
# ...

"""
Tool-specific initialization for the JALv2 compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

import SCons.Action
import SCons.Builder
import SCons.Util

class ToolJalWarning(SCons.Warnings.SConsWarning):
    pass

class JalCompilerNotFound(ToolJalWarning):
    pass

SCons.Warnings.enableWarningClass(ToolJalWarning)

def _detect(env):
    """Try to detect the JAL compiler"""
    try:
        return env["JAL"]
    except KeyError:
        pass

    jal = env.WhereIs("jalv2") or env.WhereIs("jal")
    if jal:
        return jal

    raise SCons.Errors.StopError(JalCompilerNotFound, "Could not detect JAL compiler")
    return None

#
# Emitters
#
def _jal_emitter(target, source, env):
    jal_suffix = env.subst("$JAL_SUFFIX")
    jal_codsuffix = env.subst("$JAL_CODSUFFIX")
    jal_hexsuffix = env.subst("$JAL_HEXSUFFIX")

    for s in source:
        src = str(s)
        if src.endswith(jal_suffix):
            jal_stem = src[: -len(jal_suffix)]
        else:
            jal_stem = src
        target.append(jal_stem + jal_codsuffix)
        target.append(jal_stem + jal_hexsuffix)

    return target, source

#
# Builders
#
_jal_builder = SCons.Builder.Builder(
    action=SCons.Action.Action("$JAL_COM", "$JAL_COMSTR"),
    suffix="$JAL_ASMSUFFIX",
    src_suffix="$JAL_SUFFIX",
    emitter=_jal_emitter,
)

def generate(env):
    """Add Builders and construction variables to the Environment."""

    env["JAL"] = _detect(env)
    env.SetDefault(
        # Additional command-line flags
        JAL_FLAGS=SCons.Util.CLVar("-quiet"),
        # Suffixes/prefixes
        JAL_SUFFIX=".jal",
        JAL_ASMSUFFIX=".asm",
        JAL_CODSUFFIX=".cod",
        JAL_HEXSUFFIX=".hex",
        # JAL command
        JAL_COM="$JAL $JAL_FLAGS $SOURCES",
        JAL_COMSTR="",
    )

    env["BUILDERS"]["Jal"] = _jal_builder


def exists(env):
    return _detect(env)
```
The routine `_jal_emitter` now adds two filenames to the list of targets, one for HEX and COD files each. Targets and sources come in as lists of file or directory nodes. So when looping over the source files, we have to convert each entry to a string first. However, we add the new targets as strings and return them like that. This is fine for SCons, it automatically creates the required Node objects from them before it continues with the build step.  The new Emitter is given to the Constructor of our Builder, such that the default implementation gets overwritten. 

**Pros**: Like this, we can now say "`scons -c`" and get our HEX and COD files removed as well. Neat. 


## Using a pseudo-Builder

We're now taking our Tool to the next higher level and entering the domain of pseudo-Builders (chap. 19 _Pseudo-Builders: the [AddMethod](AddMethod) Function_). This is a method that you can attach to an existing environment. It may look like a normal builder, but doesn't underly the same restrictions. In the constructor of a normal Builder you can specify only a handful of parameters, but the code that gets executed behind the curtains always stays the same. 

A pseudo-Builder allows for more freedom about how to parse and process its arguments and lets you exploit the full power of Python to control your build process. We use it here for mimicking the Emitter's functionality while specifying the source and target list, and also for taking side effect files into account slightly different from the previous section. 

Note, that you can do far more advanced things with a pseudo-Builder, e.g. have a look at the "`InstallPython`" Builder of the CPython Tool at [http://scons.org/wiki/CPythonTool](http://scons.org/wiki/CPythonTool) and [https://bitbucket.org/dirkbaechle/scons_cpython](https://bitbucket.org/dirkbaechle/scons_cpython), respectively. 


```python
# MIT License
#
# Copyright The SCons Foundation
#
# ...

"""
Tool-specific initialization for the JALv2 compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

import SCons.Action
import SCons.Builder
import SCons.Util

class ToolJalWarning(SCons.Warnings.SConsWarning):
    pass

class JalCompilerNotFound(ToolJalWarning):
    pass

SCons.Warnings.enableWarningClass(ToolJalWarning)

def _detect(env):
    """Try to detect the JAL compiler"""
    try:
        return env["JAL"]
    except KeyError:
        pass

    jal = env.WhereIs("jalv2") or env.WhereIs("jal")
    if jal:
        return jal

    raise SCons.Errors.StopError(JalCompilerNotFound, "Could not detect JAL compiler")
    return None

#
# Builders
#
_jal_builder = SCons.Builder.Builder(
    action=SCons.Action.Action("$JAL_COM", "$JAL_COMSTR"),
    suffix="$JAL_ASMSUFFIX",
    src_suffix="$JAL_SUFFIX",
    single_source=1,
)

def Jal(env, target, source=None, *args, **kw):
    """
    A pseudo-Builder wrapper for the JALv2 executable.
        jalv2 [options] file
    """
    if not SCons.Util.is_List(target):
        target = [target]
    if not source:
        source = target[:]
    if not SCons.Util.is_List(source):
        source = [source]

    result = []
    jal_suffix = env.subst("$JAL_SUFFIX")
    jal_codsuffix = env.subst("$JAL_CODSUFFIX")
    jal_hexsuffix = env.subst("$JAL_HEXSUFFIX")
    for t, s in zip(target, source):
        # Call builder
        jal_asm = _jal_builder.__call__(env, t, s, **kw)
        result.extend(jal_asm)
        # Add cleanup files
        src = str(s)
        if src.endswith(jal_suffix):
            jal_stem = src[: -len(jal_suffix)]
        else:
            jal_stem = src
        env.Clean(jal_asm, [jal_stem + jal_codsuffix, jal_stem + jal_hexsuffix])

    return result

def generate(env):
    """Add Builders and construction variables to the Environment."""

    env["JAL"] = _detect(env)
    env.SetDefault(
        # Additional command-line flags
        JAL_FLAGS=SCons.Util.CLVar("-quiet"),
        # Suffixes/prefixes
        JAL_SUFFIX=".jal",
        JAL_ASMSUFFIX=".asm",
        JAL_CODSUFFIX=".cod",
        JAL_HEXSUFFIX=".hex",
        # JAL command
        JAL_COM="$JAL $JAL_FLAGS $SOURCES",
        JAL_COMSTR="",
    )

    try:
        env.AddMethod(Jal, "Jal")
    except AttributeError:
        # Looks like we use a pre-0.98 version of SCons...
        from SCons.Script.SConscript import SConsEnvironment

        SConsEnvironment.Jal = Jal

def exists(env):
    return _detect(env)
```
For our Jal method, we are now using a pseudo-Builder. It gets added to the Environment by the [AddMethod](AddMethod) function and wraps the Builder `_jal_builder`, which gets called for each source/target pair. 

**Pros**: A simplified filename interface: the user can specify a list of source files, e.g. 


```python
env.Jal(['alarm', 'timetick'])
```
and the target names `alarm.asm` and `timetick.asm` are created automatically. `Clean` (and **not** `SideEffect`!) is now used to specify the created files that should get removed additionally on a "`scons -c`". Check the code to see that the Emitter has gone, we don't need it anymore. 

**Cons**: `AddMethod` was introduced in SCons version 0.98. For earlier distributions, the fallback mechanism of simply slapping the pseudo-Builder on top of the SConsEnvironment will not work, i.e. `Clone()` doesn't behave correctly in all cases. 

<a name="special"></a> 
## Adding specialized builders

Another option for our work with JAL is that we can tell the `jalv2` executable to only create HEX or COD files with the calls 

```console
jalv2 -no-asm -no-hex -codfile foo.cod foo.jal
```
and 

```console
jalv2 -no-asm -no-codfile -hex foo.hex foo.jal
```
. And if `jalv2` has these features, the users of our Tool want them too...rather sooner than later. `:)` 

So here is our final version of the code: 

```python
# MIT License
#
# Copyright The SCons Foundation
#
# ...

"""
Tool-specific initialization for the JALv2 compiler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""

import SCons.Action
import SCons.Builder
import SCons.Util

class ToolJalWarning(SCons.Warnings.SConsWarning):
    pass

class JalCompilerNotFound(ToolJalWarning):
    pass

SCons.Warnings.enableWarningClass(ToolJalWarning)

def _detect(env):
    """Try to detect the JAL compiler"""
    try:
        return env["JAL"]
    except KeyError:
        pass

    jal = env.WhereIs("jalv2") or env.WhereIs("jal")
    if jal:
        return jal

    raise SCons.Errors.StopError(JalCompilerNotFound, "Could not detect JAL compiler")
    return None

#
# Builders
#
_jal_builder = SCons.Builder.Builder(
    action=SCons.Action.Action("$JAL_COM", "$JAL_COMSTR"),
    suffix="$JAL_ASMSUFFIX",
    src_suffix="$JAL_SUFFIX",
    single_source=1,
)

_jal_asm_builder = SCons.Builder.Builder(
    action=SCons.Action.Action("$JAL_ASMCOM", "$JAL_ASMCOMSTR"),
    suffix="$JAL_ASMSUFFIX",
    src_suffix="$JAL_SUFFIX",
    single_source=1,
)

_jal_cod_builder = SCons.Builder.Builder(
    action=SCons.Action.Action("$JAL_CODCOM", "$JAL_CODCOMSTR"),
    suffix="$JAL_CODSUFFIX",
    src_suffix="$JAL_SUFFIX",
    single_source=1,
)

_jal_hex_builder = SCons.Builder.Builder(
    action=SCons.Action.Action("$JAL_HEXCOM", "$JAL_HEXCOMSTR"),
    suffix="$JAL_HEXSUFFIX",
    src_suffix="$JAL_SUFFIX",
    single_source=1,
)

def Jal(env, target, source=None, *args, **kw):
    """
    A pseudo-Builder wrapper for the JALv2 executable.
        jalv2 [options] file
    """
    if not SCons.Util.is_List(target):
        target = [target]
    if not source:
        source = target[:]
    if not SCons.Util.is_List(source):
        source = [source]

    result = []
    jal_suffix = env.subst("$JAL_SUFFIX")
    jal_codsuffix = env.subst("$JAL_CODSUFFIX")
    jal_hexsuffix = env.subst("$JAL_HEXSUFFIX")
    for t, s in zip(target, source):
        # Call builder
        jal_asm = _jal_builder.__call__(env, t, s, **kw)
        result.extend(jal_asm)
        # Add cleanup files
        src = str(s)
        if src.endswith(jal_suffix):
            jal_stem = src[: -len(jal_suffix)]
        else:
            jal_stem = src
        env.Clean(jal_asm, [jal_stem + jal_codsuffix, jal_stem + jal_hexsuffix])

    return result

def generate(env):
    """Add Builders and construction variables to the Environment."""

    env["JAL"] = _detect(env)
    env.SetDefault(
        # Additional command-line flags
        JAL_FLAGS=SCons.Util.CLVar("-quiet"),
        # Suffixes/prefixes
        JAL_SUFFIX=".jal",
        JAL_ASMSUFFIX=".asm",
        JAL_CODSUFFIX=".cod",
        JAL_HEXSUFFIX=".hex",
        # JAL commands
        JAL_COM="$JAL $JAL_FLAGS $SOURCES",
        JAL_COMSTR="",
        JAL_ASMCOM="$JAL $JAL_FLAGS -no-codfile -no-hex -asm $TARGET $SOURCE",
        JAL_ASMCOMSTR="",
        JAL_CODCOM="$JAL $JAL_FLAGS -no-asm -no-hex -codfile $TARGET $SOURCE",
        JAL_CODCOMSTR="",
        JAL_HEXCOM="$JAL $JAL_FLAGS -no-asm -no-codfile -hex $TARGET $SOURCE",
        JAL_HEXCOMSTR="",
    )

    try:
        env.AddMethod(Jal, "Jal")
    except AttributeError:
        # Looks like we use a pre-0.98 version of SCons...
        from SCons.Script.SConscript import SConsEnvironment

        SConsEnvironment.Jal = Jal

    env["BUILDERS"]["JalAsm"] = _jal_asm_builder
    env["BUILDERS"]["JalCod"] = _jal_cod_builder
    env["BUILDERS"]["JalHex"] = _jal_hex_builder

def exists(env):
    return _detect(env)
```
We added specialized builders for creating ASM, COD and HEX files (`_jal_*_builder`), together with the required variables for the new command lines and flags. This time not as pseudo-Builders, because we don't have to take any side effects into account. Only a single file type gets generated when calling one of the Builders `JalAsm`, `JalCod` and `JalHex`. 

All together, this leaves us with a very powerful tool for compiling JAL source files. It should get any user going very quickly, under the assumption that you provided some documentation for it. `;)` 


# Conclusion

After reading through all of this text, you should now have a good understanding of how you can write new Tools for SCons. If some questions remain unanswered, please don't hesitate to ask them on the SCons User Mailing list. We are always happy to hear from people using SCons, and value your efforts in understanding and mastering this fine build system. 

Happy building! 

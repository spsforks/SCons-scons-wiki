

# SCons new toolchain design doc

There are two main objects in the toolchain: a `Tool`, and a `Toolchain`.


## Tools

A Tool's job is to update an Environment with variables and one or more Builders to build something.

This new Tool design preserves the current named-tool syntax but allows currying args to the tool, which we should use to replace the existing method of pre-setting Environment vars which the tool examines.  Tools shouldn't change their behavior anymore based on Env (except for a few well-defined systemwide properties), but instead take args.

tool constructors produce a Tool object.  Each tool object has a name. There's no need for distinct tool instances with the same args (tools don't have internal state apart from their args or derived from them) so they can be memoized.

`tool=Tool(classname, toolname, **kw)`: returns a Tool object of the appropriate subclass.  classname can be any registered tool name. Names are registered by the Tool.

`tool=ToolIntelC(toolname, abi=None, version=None)`: returns a generic ToolIntelC object.

`tool=ToolIntelC(toolname, abi='x86', version='12.0')`: returns a specific ToolIntelC object.

`tool.exists()`: check that commands this tool uses exists.

* this must be fast; can cache results.
`tool.generate()`: apply tool to environment.  Pretty much same as old system.

`tool.version`: tuple of version.  Typically ints: (maj, min, build) but will be compared elementwise.

`tool.author, release_date, license`: strings.  All optional.

`tool.name`: name of the tool.  Setting this registers the name with a tool registry.


### Tool base class

# For now, this is just a sketch of the design.  *Many* details missing.


```python
class Tool(object):
  """base class for all Tools"""

  # XXX: is this needed? # Don't think we ever want to instantiate a base tool.
  def __init__(self, name, *args, **kwargs):
    self._set_name(name)

  @property
  def name(self):
    return _name

  @name.setter
  def _set_name(self, name):
    _name = name

  @classmethod
  def create(name, *args, **kw):
    """Look up tool by name.  Create and return an instance of it."""
    # Tools are memoized by name & args
    tc = tools[name] # this is the tool's class
    return tc(*args, **kw)
```

### Tool example

_Definition: _


```python
class ToolCat(Tool):
    """A trivial tool that calls Un*x 'cat' or 'nl' (number lines)
    depending on the number_lines tool arg."""

    def __init__(self, name, number_lines=False, *args, **kwargs):
        super(Tool, self).__init__(name, *args, **kwargs)  # maybe need this
        self._number_lines = number_lines
        pass

    def exists(self, use_env):
        # check if 'cat' is found in standard places, or
        # if use_env is True, use user's env vars e.g. $PATH
        # Returns (status, message)
        # message can be set if status is true or false
        return False, "No cat found."

    def generate(self, env):
        # create Builder...
        # add vars
        if self._number_lines:
            env.SetDefault('NL', 'nl')  # number lines
        else:
            env.SetDefault('CAT', 'cat')  # use full paths when necessary
        env.SetDefault('CAT_ARGS', None)

    @property
    def vars(self):
        """Return list of vars set or used by this tool"""
        return ('CAT', 'NL', 'CAT_ARGS')

    @property
    def version(self):
        return 1, 0, 0

    def __str__(self):
        return "cat tool"
```

## Toolchain Design

A `SimpleToolchain` is a list of Tools, all of which must exist for the toolchain to be allowed to be used.  (A simple Tool can be used anywhere a `SimpleToolchain` is found.) A Toolchain is either a `SimpleToolchain`, or an OR-list of Toolchains, in which case each toolchain is tried in order and the first one to succeed is used. Any Tool within a Toolchain may be marked as optional; such a tool will be used if the toolchain is used and if it exists, but doesn't need to exist to satisfy its toolchain.

Simple example: (tools here can be tool names, or Tool objects.)


```python
gnu_c_toolchain = SimpleToolchain(['gcc', 'gnulink'])
msvc_c_toolchain = SimpleToolchain([msvc_c, msvc_link, msvc_lib], Toolchain.OPTIONAL, [msvc_mt]) # following tools are optional
intel_c_toolchain = SimpleToolchain(intel_c, intel_link) # requires msvc_c_toolchain on Windows too; how to capture that?
windows_c_toolchain = OrToolchain(intel_c_toolchain, msvc_c_toolchain, gnu_c_toolchain)
```
* What about tool ABIs and other args here?  This doesn't capture x86
   * vs. x86_64, though the base tools in a toolchain can have args, so it's possible to build toolchains that specify ABIs -- it's just not easy to do by default.  Maybe need global vars for this, yuck.
* What about the fact that Intel C requires the base C compiler?  Some
   * form of `Tool.Depends()` or `Toolchain.Depends()`?
* How can user know that optional tools are missing?  (A: mytool.exists())  What happens if they're used?  Should be something sensible.

### Updating Toolchains

SCons base, tool authors, or SConscript-writers can all update toolchains.  The main way is to add alternatives to existing tools.

`new_toolchain = Toolchain.AddAlternative(OtherToolchain, before=False)`:

* if this toolchain is an `OrToolchain`, add `OtherToolchain` to start or end (and return new).
* If this toolchain is a `SimpleToolchain`, return a new `OrToolchain` with both the old and new.
* Returns the new toolchain in both cases.
To replace a tool in a toolchain, what should the interface be?


### Using Toolchains

Simply, the active toolchain runs through all its tools in order and applies them to the given Environment.


## Platform

I'm deliberately staying away from platform specification here (GNU-like tuples with arch, vendor and so on).  It's not relevant to all tools (Java, LaTeX, etc.) so I think its detailed design can be left to the C-like tools/toolchains.


## Error Handling

`Tool.exists` should return end-user-useful error messages, but not throw exceptions.  Toolchains are responsible for displaying those errors when appropriate, and hiding them otherwise (e.g. when testing which toolchain to use).

`Tool.generate` may throw exceptions in error cases because exists() can't always predict perfectly that the tool will work properly; error messages should be extra-helpful here.

Missing but used tools: this shouldn't happen anymore, because the toolchain will give an error as the Environment is being constructed. We should never get into a situation where e.g. $CC is empty when the Object() builder is called.  HOWEVER, just in case it could happen, we should have some kind of requires(toolchain) method in builders to catch this error and tell the user.  This might be a lot of work to thread through everything however.


## Use Cases


### Built-in tools (SCons base)

SCons will create a default toolchain for each platform, keeping it fairly minimal.

`DefaultEnvironment` will use the default toolchain, and it'll be what the current 'default' as a tool(chain) turns into.

There may be some built-in tools that are not in the default toolchain; we'll try to make it fast to create a simple Environment.


### Third-party tools (not shipped with SCons)

Third-party tools go in `site_scons/tools` as usual; they can register themselves as tools and (???) add themselves to toolchains or create new toolchains.


### SConscript-writer

SConscript writers can define tools and toolchains and use them in Environments.  If they're defined before first use of `DefaultEnvironment` then can even override the 'default' toolchain.

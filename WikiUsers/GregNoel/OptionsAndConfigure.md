_This is a historical document capturing design thoughts on refactoring the various ways external data can be supplied to SCons into a more unified approach. While work was done, it was not merged and is no longer available._

# Table of Contents

# Contents
  - <a href="#SingleCharacterFlags">Single-character flags</a>
  - <a href="#WordBasedFlags">Word-based flags</a>
  - <a href="#Variables">Variable Assignments</a>
  - <a href="#ControlFiles">Control Files</a>
  - <a href="#ConfigTests">Configure Tests</a>

# Unifying Options and Configuration

This page presents a position that command-line options (both flags and assignments) and configuration should be unified into a single framework (or, worst case, that they should be derived from a common base class).  The idea behind the position is that these are ways that SCons gets "outside" information; that is, information that is not embedded in the SConscripts. 

Options and configuration results either affect program flow or are converted into into values for construction variables (or both).  Those values are then incorporated into a SCons Environment which is used to build objects.  The message in this wiki page is how those construction variables are calculated and then incorporated. 

The command line consists of four types of tokens: 

* [Single-character flags](OptionsAndConfigure).  These flags are preceded by a single hyphen.  They may or may not take a value (an auxilliary token on the command line).  More than one flag may be grouped after the hyphen. 
* [Word-based flags](OptionsAndConfigure).  These are preceded by two hyphens.  They may or may not take a value; if they do take a value, an equal sign <ins>_always_</ins> separates the name and the value. 
* [Variable assignments](OptionsAndConfigure).  These are `name=value` pairings. 
* Arguments.  Anything that is not a flag option or a variable assignment option.  Arguments are outside the scope of this discussion; the only thing we will say about them is that they are gathered into a list and made available to the SCons scripts. 

Another source of options are [control files](OptionsAndConfigure).  These are text files containing `name=value` pairs similar to command-line variable assignments.  (They are actually Python scripts, so any legal Python value is acceptable.) 

The last source of options are [configure tests](OptionsAndConfigure).  These values are programmatically determined by probing the platform on which the build is run. 

<a id="SingleCharacterFlags"></a> 
## Single-character flags

**Synopsis:** Single-character flags are converted to their equivalent word-based flags. 

Single-character flags are reserved to SCons and may not be specified for user flags.  When the command line is cracked, single-character flags are converted to their equivalent word-based flags; the translation is hard-wired, so single-character flags cannot be extended. 

Here is what single-character flags become.  Any flag not recognized causes an error. 

| Opt | Longopt |   | OPT | Longopt
|:----|:--------|---|:----|:-------
| `-a` | `--always-build` (*) |           | `-A` | ERROR
| `-b` | ignored for compatibility |      | `-B` | ERROR
| `-c` | `--clean` |                      | `-C directory` | `--directory=directory`
| `-d flags` | `--debug=flags` |          | `-D` | `--up=defaults` (*)
| `-e` | -`-environment-overrides `(*) |  | `-E` | ERROR
| `-f file` | -`-file=file` |             | `-F` | ERROR
| `-g` | ERROR |                          | `-G` | ERROR
| `-h` | -`-help` |                       | `-H` | `--help-options`
| `-i` | `--ignore-errors` |              | `-I directory` | `--include-dir=directory`
| `-j N` | `--jobs=N` |                   | `-J` | ERROR
| `-k` | `--keep-going` |                 | `-K` | ERROR
| `-l N` | `--load-average=N` (*) |       | `-L` | ERROR
| `-m` | ignored for compatibility |      | `-M` | ERROR
| `-n` | `--dry-run` |                    | `-N` | ERROR
| `-o file` | `--old-file=file` |         | `-O` | ERROR
| `-p` | `--print-data-base` (*) |        | `-P` | ERROR
| `-q` | `--question` |                   | `-Q` | `--no-status-messages` (*)
| `-r` | `--no-builtin-rules` (*) |       | `-R` | `--no-builtin-variables` (*)
| `-s` | `--silent` |                     | `-S` | `--no-keep-going`
| `-t` | `--touch` |                      | `-T` | ERROR
| `-u` | `--up=dot` (*) |                 | `-U` | `--up=here` (*)
| `-v` | `--version` |                    | `-V` | ERROR
| `-w` | `--print-directory` |            | `-W file` | `--what-if=file` (*)
| `-x` | ERROR |                          | `-X` | ERROR
| `-y` | ERROR |                          | `-Y repository` | `--repository=repository`
| `-z` | ERROR |                          | `-Z` | ERROR


The (*) marks entries that are future or otherwise assume something at variance with the current flags.  Also, the `-W` usage conforms to `GNU make`, not the `--warnings` usage of `automake`.

_TODO: insert a list here with the differences._ 

<a id="WordBasedFlags"></a> 
## Word-based flags

**Synopsis:** When the command line is cracked, flag options are placed in a private list.  A flag may occur more than once on the command line; the multiple occurrences are accumulated.  A _defining instance_ of a flag causes all of its occurences to be removed from the list and a value calculated.  This value is available immediately, so it may be saved or used for further calculations.  Values calculated from the flag value may be accumulated in a pool and passed to an Environment when it is instantiated.  At the end of the parse phase, any flags still on the list cause an error message. 

* _(Note that how the error message is presented is crucial to acceptance; rather than "Unrecognized flag" with the implication that it should have been noticed immediately, it should say something like "Flag never defined during processing; check the spelling.")_ 
(Open question: Command-line flags can have internal dashes.  A `configure` script will convert (most of) these internal dashes into underscores before matching on the name (it's inconsistent). Thus, when comparing flags `enable_foo` is used for `--enable-foo` and `exec_prefix` is used for `--exec-prefix`.  Should SCons convert dashes to underscores prior to matching so that SCons scripts will be more compatible with `configure`?) 

The defining instance can save the calculated value in a Python dict (called FLAGS? OPTIONS? neither is good) where it can be retrieved later by any interested party.  Convenience functions will be provided to implement common paradigms used in specifying flags.  Previously-defined flags are immediately available, so, for example, the value of `prefix` can be determined and used as the default for `exec-prefix`. 

Flag values may be processed into a pool that accumulates construction variables.  The values may be used as-is or they may be calculated. 

One or more pools may then be used to initialize the construction variables of an Environment.  These values may then be used in the construction of command lines in the normal way. 


### Fundamental operation

The fundamental operation on flags removes any flags matching a set of names from the private list, runs the extracted flags through an auditor to determine the value: 
value = Query.Flag(names, audit, args)
: 
The _names_ are a list of one or more strings of flag names to match.  
The _audit_ function takes the matched values and calculates the value to use.  
The _args_ are in a dict and are passed as keyword parameters to the audit function. 

The audit function takes two positional parameters, plus any keyword arguments from the _args_ parameter: 
```py
value = audit(flags, values, **args)
```

The _flags_ are a list of matching flag names from the command line, in the order they appear on the command line.  
The _values_ are a list of the corresponding values for the flags; `None` is used to indicate that the flag was not given a value.  
The _args_ are the keywords given to the `Query.Flag` function. 

Here's a sample implementation of EnableFlag (see below) with little error checking: 

```py
def EnableFlag(key, state="no", default="yes", help=None):
    # could use bound variables for audit function if desired
    def audit(flags, values, state="no", default="yes"):
        if not values:  # not on command line
            state = yesno(state)
            if state == "no":
                return "no"
            return yesno(default)
        f = flags[-1]  # last flag wins
        v = values[-1]
        if f[0:7] == "disable":
            if v is not None:
                print("value ignored for'--%s'" % f)
            return "no"
        if v is None:  # no value for --enable, use default
            v = default
        return yesno(v)

    # Scan the command line for this set of flags
    v = Query.Flag(
        ["enable-" + key, "disable-" + key],
        audit,
        {"state": state, "default": default},
    )
    FLAGS["enable-" + key] = v
    HelpText(help)
    return v
```

### Additional pre-defined flag values

These command-line flags should be pre-defined; they are the flags supported by `configure` (plus `--install` to support RPM and Debian build notions).  Even if they aren't used today, someday we will be glad to have them. 

| Opition | Description [default] |
|:----|:--------|
| **Deployment directories**||
| `--prefix=PREFIX` | install architecture-independent files in PREFIX [/usr/local]
| `--exec-prefix=EPREFIX` | install architecture-dependent files in EPREFIX [PREFIX]
| `--bindir=DIR` | user executables [EPREFIX/bin]
| `--sbindir=DIR` | system admin executables [EPREFIX/sbin]
| `--libexecdir=DIR` | program executables [EPREFIX/libexec]
| `--datadir=DIR` | read-only architecture-independent data [PREFIX/share]
| `--sysconfdir=DIR` | read-only single-machine data [PREFIX/etc]
| `--sharedstatedir=DIR` | modifiable architecture-independent data [PREFIX/com]
| `--localstatedir=DIR` | modifiable single-machine data [PREFIX/var]
| `--libdir=DIR` | object code libraries [EPREFIX/lib]
| `--includedir=DIR` | C header files [PREFIX/include]
| `--oldincludedir=DIR` | C header files for non-gcc [/usr/include]
| `--infodir=DIR` | info documentation [PREFIX/info]
| `--mandir=DIR` | man documentation [PREFIX/man]
| **Packaging**||
| `--install=DIR` | install tree is relative to DIR [empty]  (called DESTDIR by configure and BUILDROOT by RPM)
| **Configuration selection**||
| `--enable-FEATURE[=ARG]` | include FEATURE (ARG=yes)
| `--disable-FEATURE` | do not include FEATURE (same as `--enable-FEATURE=no`)
| `--with-PACKAGE[=ARG]` | use PACKAGE (ARG=yes)
| `--without-PACKAGE` | do not use PACKAGE (same as `--with-PACKAGE=no`)
| **Cross-compilation**||
| `--build=BUILD` | configure for building on BUILD [guessed] (unneeded?)
| `--host=HOST` | cross-compile to build programs to run on HOST [BUILD]
| `--target=TARGET` | programs should produce output for TARGET [HOST]
| `--program-prefix=PREFIX` | prepend PREFIX to installed program names
| `--program-suffix=SUFFIX` | append SUFFIX to installed program names
| `--program-transform-name=PROGRAM` | run '`sed PROGRAM`' on installed program names

Only the last one is problematical.  It's a rarely-used feature, and maybe some other mechanism could be used. 


### Enable/Disable flags

Command-line flags that begin `'--disable-'` are treated as if they were an `--enable-` with the value `'no'`.  That is, `--disable-foo` is turned into `--enable-foo=no`; any value that the flag had is ignored. 

A possible prototype: 
```py
Query.EnableFlag(key, state, default, help=None)
```

Evaluate flags with the names `--enable-`_key_ or `--disable-`_key_.  If no such flag is present, the default state is _state_.  The _state_ parameter must be either **yes** or **no**; if it is not present, **no** is assumed.  If no value is present for an `--enable-`_key_ flag, the _default_ value is used.  If the _default_ parameter is not present, a value of **yes** is returned.  (The values **y**, **yes**, **t**, **true**, **1**, **on** and **all** will be treated as **yes**, and the values **n**, **no**, **f**, **false**, **0**, **off** and **none** will be treated as **no**.)  Any specified help is passed to the help subsytem. 

### With/Without flags

The processing of the with/without flags is very similar to that of the enable/disable flags, except that `--without-foo` is converted to `--with-foo=no`. 

A possible prototype: 
```py
Query.WithFlag(key, state, default, help=None)
```

Evaluate flags with the names `--with-`_key_ or `--without-`_key_.  If no such flag is present, the default state is _state_.  The _state_ parameter must be either **yes** or **no**; if it is not present, **no** is assumed.  If no value is present for an `--with-`_key_ flag, the _default_ value is used.  If the _default_ parameter is not present, a value of **yes** is returned.  (The values **y**, **yes**, **t**, **true**, **1**, **on** and **all** will be treated as **yes**, and the values **n**, **no**, **f**, **false**, **0**, **off** and **none** will be treated as **no**.)  Any specified help is passed to the help subsytem. 


```py
print("with foo?", Query.WithFlag("foo", state="no", default="/with/foo"))
print("with bar?", Query.WithFlag("bar", state="yes", default="/with/bar"))
```

```con
% scons
with foo? no
with bar? /with/bar
% scons --with-foo --with-bar
with foo? /with/foo
with bar? /with/bar
% scons --without-foo --without-bar
with foo? no
with bar? no
% scons --with-foo=/opt/foo --with-bar=/opt/bar
with foo? /opt/foo
with bar? /opt/bar
```

### Other user-defined flags

Here's a sample of possible pre-defined flag types (_i.e._, wrappers with audit functions that are maintained as part of SCons).  These are chosen to indicate the range of functionality possible and may not be realistic as described. 
```py
Query.BoolFlag(key, default, help=None)
```

Evaluate a flag whose initial value is _default_ (False if not present) and the value is reversed each time the flag is specified on the command line.  The flag cannot have a value.  The flag will have the specified _key_ and display the specified _help_ text.  For example: 
```py
tf = pool.BoolFlag('exclusive', False)
```

* Each occurrence of the `--exclusive` flag will flip whether or not it should be exclusive. 
```py
Query.CountFlag(key, help=None)
```

Evaluate a flag whose initial value is zero and the value is incremented each time the flag is specified on the command line.  The flag cannot have a value.  The flag will have the specified _key_ and display the specified _help_ text.  For example: 


```py
number = pool.CountFlag('clean')` 
Query.LastFlag(key, default, help=None)
```

Evaluate the flag(s) specified; return is `None` if the flag is not present, the _default_ if the flag is present without a value, and the value if there is one.  The specified _help_ text will be passed to the help subsystem.  If there are multiple occurences of the flag, the last one wins.  For example: 


```py
opt = pool.LastFlag(['opt', 'optimize'], '-O')` 
Query.EnumFlag((key, default, allowed_values[, map[, ignorecase]], help=None)
```

Like `Options.EnumOption`. 

```py
Query.ListFlag(key, default, names[, map], help=None)
```

Like `Options.ListOption`. 

```py
Query.PackageFlag(key, help, default)
```

Like `Options.PackageOption`. 

```py
Query.PathFlag(key, default[, validator], help=None)
```

Like `Options.PathOption`; the last one on the command line wins. 

```py
Query.PathFlags(key, default[, validator], help=None)
```

Like `PathFlag` except that multiple occurrences are accumulated. 


### Cross-compilation flags

If the `--host` command-line flag is present, SCons cross-compiles files for use on another system.  If the `--target` command-line flag is present (or defaulted from the `--host` flag), the appropriate flags are made available to the compile stages so that their generated output will be for the selected system.  (For compatibility, the `--build` option is processed but must match the current system, as SCons always builds on the system where it is running.) 

TODO: what the flags cause to happen internally; replace config.guess and config.sub?; other stuff (I've edited a number of configure scripts that did cross-compiling, but I've never written one from scratch, so my knowledge of what autoconf does here is small.  Can anyone help?) 


### Thoughts

User-defined validation function:  
 `     def validate(flags, values, arg = value, ...)`  
 The _flags_ are a list of flag names that matched the selection.  
 The _values_ are a list of the corresponding values.  
 The _arg_ parameters are passed through from the Define call. 

Prototype to define flag:  
 `     value = DefineFlag(key, names, validate, args, help options)`  
 The _key_ is the name under which to keep the calculated value.  
 The _names_ are a list of one or more strings of flag names to match.  
 The _validate_ function takes the matched values and calculates the value to use.  
 The _args_ are in a dict and are passed as named parameters to the validate function.  
 The _help options_ will be defined elsewhere. 

Prototype to retrieve flag:  
 `     Fetch(key)`  
 The _key_ specifies the flag value to return 



```py
def audit(flags, values, none=None, default=None):
    if not values:  # not on command line
        return none
    v = values[-1]  # last flag present wins
    if v is None:  # no value specified
        return default
    return v

opt = DefineFlag("opt", ["opt", "optimize"], audit, {"none": "", "default": "-O"})
print("""optimization level is <%s>""" % opt)
```

```con
% scons
optimization level is <>
% scons --opt
optimization level is <-O>
% scons --optimize
optimization level is <-O>
% scons --opt=-O1
optimization level is <-O1>
% scons --opt=-O1 --opt=-O2
optimization level is <-O2>
% scons --optimize=-O1 --opt=O2
optimization level is <-O2>
% scons --opt=-O1 --optimize=-O2
optimization level is <-O2>
```
<a id="Variables"></a> 
## Variable Assignments

When the command line is cracked, variable assignments are placed in a global pool using their _canonical name_ (the primary name for the variable).  Variables are marked valid by encountering a _defining instance_ of the variable (see [DefiningHelpText](DefiningHelpText) for details).  Variable assignments may also be read from an option file; the option file will be rewritten if a value changes.  At the end of the parse phase, any variables not marked valid cause an error message to be generated. 

* _(Note that how the error message is presented is crucial to acceptance; rather than "Unrecognized variable" with the implication that it should have been noticed immediately, it should say something like "Variable never defined during processing; check the spelling.")_ 
The defining instance of a variable may specify semantics to modify the variable's value as it is placed in its pool, or a variable can have a value calculated and placed in a pool.  In this way, the value of a variable may be preserved across runs. 

These values may then be processed into a context that accumulates construction variables.  The values may be used as-is or they may be calculated. 

One or more contexts may then be used to initialize the construction variables of an Environment.  These values may then be used in the construction of command lines in the normal way. 

<a id="ControlFiles"></a> 
## Control Files

<a id="ConfigTests"></a> 
## Configure Tests

**Synopsis:** Configure operates in an infinite sea of tests.  Each test is uniquely named by some convention (probably a tuple that captures all of the salient facts).  When a configuration function is executed, it composes these tests into a DAG; obviously, if the test has already been run, there's no need to repeat it and the result can be used immediately.  Some tests exist only for a side-effect (in which case the "test" is really "Has this side-effect been done?").  Each test produces a result, which can be true/false, values from some enumerated set, or whatever.  These results can in turn be used for calculations.  In some cases, those calculations can be saved in a context that can set the initial values of an Environment's construction variables. 

Access to the sea of tests is via a Config context: 

```py
conf = Config(
    autoconf=None, custom_tests=None, conf_dir="#/.sconf_temp", log_file="#/config.log"
)
```

All tools used in a Config context must be initialized, either by using the autoconf parameter (e.g., `autoconf = ['cc', 'c++', 'python']`) or by calling the appropriate configuration function (e.g., `conf.Prog.CC(cross='yes')`).  In some cases, the initialization is implicit; a test can _require_ that the C compiler be configured and include that test result in its own DAG. 

Header files can be created to pass configure results to program logic: 
```py
conf_h = ConfigHeader(file = 'config.h', lang = 'C')
conf_h.Define(name, value = 1, comment=None)
```

The `conf_h` object is a wrapper for a built file with the given name and a builder that builds the given type of file from the dependencies; the Define() method encapsulates its parameters into some specialty Node type and creates a dependency on the conf_h node.  The file itself is *not* built until it is needed during the build phase; standard dependency checking will prevent it from being regenerated if it hasn't changed. 

If the value in a `conf_h.Define()` is None, the name is specifically undefined (i.e., `#undef name` is generated) in languages that allow it. 


## API

Still not even half-baked. 
Commonality
: 
   * Need a 'pool' object for each type (FlagPool, VariablePool, ConfigPool) where values are filled in from external sources.  One global FlagPool, one global VariablePool plus one for each options file, zero or more ConfigPools. 
   * Need a 'value' object for each type (FlagValue, VariableValue, ConfigValue). 
   * At the defining instance (which also assigns the help text), the external value may be examined and modified before being stored in the pool. 
   * Need an 'accumulating' object (Accumulate) to select from other pools, to be able to mix-n-match values from other pools.  Can transform selected value when accumulating. 
   * After the defining instance, the a pool value can be retrieved and placed in an Accumulator. 
   * Can assign a calculated value to an Accumulator. 



```py
# pool objects, all really the same class
cf = CommandFlags(xxx)
co = CommandOptions(xxx)
fo = FileOptions(xxx)
cc = Config(xxx)
# defining instance
cf.CountFlag("clean", "Clean")
co.ListOption("status", "Marital status", "single,married,divorced,widowed")
fo.ValueOption("CCFLAGS", "Common C/C++ flags", "-Wall")
cc.Prog.CC()
cc.Prog.CXX()
# accumulate, another of the pool object class
a = Accumulate(xxx)
a.Fetch(cf, "prefix")
a.Fetch(fo, "CCFLAGS")
# use
env = Environment(config=[cc, a])
```

---

 _Stuff below this line is retained from an earlier draft.  The basic ideas are OK, but I no longer believe in a lot of the details.  Eventually, this will be re-written into something usable._ 


### Help text

When a command-line option is declared with help text, that is called a _defining instance_ for that option.  There must be at least one defining instance of any option on the command line or it is an error. 

Unfortunately, help text is declared in an Option object.  An Option object is intended as a place to accumulate environment overrides when initializing an environment, so if different objects declare overlapping sets of parameters, help text may be declared multiple times.  Since the help text for a given Option object is added to the global help message as a group, there's no way to coordinate help text for an individual parameter. 

So there should be a way of accumulating the help text on a per-option basis.  If there are multiple defining instances, the text is merged with some smarts (i.e., duplicate texts are combined). 

See the next section. 


## Untangling parameters, help, options, and configure

Command-line parameters are global.  That's pretty obvious, but it means that information about them needs to be global as well.  A parameter value may be consumed many times (with different interpretations), but parameter information should be manipulated on a global basis. 

In particular, help text should be accumulated globally.  If there are multiple definitions of a parameter, the help text should be accumulated intelligently, by merging duplicate copies.  The help subsystem should do its best to organize and lay out the options (the `configure` help display is a good model), but there also should be ways to influence its behavior (accumulate some of the options into a separate subsection, for example).  The default version should be reasonably intelligent, so there's not a lot of temptation to replace it. 

The Option object wants to provide values to an environment, but it's limited in the things it can initialize (for reasons obvious later, the list of tools comes to mind). 

A Configure context accumulates values to modify an environment, but these values have to be exported individually to each construction environment using them. 

Moreover, an Environment object is basically a huge number of operations built around manipulating a construction environment (which is really the only thing needed when constructing a command to be executed). 

Looking at this, the unifying thread among these objects is that they  want to manipulate construction variables.  Maybe the thing to do is expose construction variables in an object that allows them to be inexpensively composed.  This object would then either be a base class (IsA) or a member variable (HasA) of the Configure context, the Option object, and the Environment object (and maybe more; I can believe that the help generator could substitute values into the output it was displaying). 

For the sake of discussion, I'll call this class a Namespace and hope somebody picks a better name if it gets implemented.  It's basically a [SubstitutionEnvironment](SubstitutionEnvironment) with the dross pulled out and some functionality added.  For example, if a value lookup fails in the local Namespace, it should check for the value in a list of alternative Namespaces. 

Configure objects no longer need an Environment to construct commands; all they really need is the Namespace.  (There would be some fiddling to create and manipulate nodes that would have to come from someplace, but that can be worked out.)  If a Configure context configures a tool, it marks that in the Namespace, which would cause any Environment initializing from it to skip its own configuration and use the provided information. 

The Environment constructor is modified so that the 'options=' parameter can take a list of Namespaces, which is used to initialize the source list in its Namespace; no copying is needed to include them.  The same Configure context or Option object can be used in multiple Environments without having to copy the values multiple times. 

There's a lot of detail missing here (distinguishing between 'update' access and 'readonly' access is one), but I hope this sketch is enough to show how it would work. 


### Thoughts

There's a global object called `HelpText`. 

```
HelpText.Wrap('Text printed first', 'Text printed last')

section = HelpText.Section('section_name')

section.Wrap('Text at beginning of section', 'Text at end of section')

HelpText.__call__('section_name', key, short_help, long_help)

section.__call__(key, short_help, long_help)
```

So '`scons -h`' prints a short blurb and the list of sections. 

And '`scons -h target ...`' prints detailed information: 

* If _target_ is a section name, all the keys and their short help is printed, wrapped in the beginning and ending text.  The reserved target '`ALL`' prints all the sections. 
* If _target_ is a key, the long help for the key is printed. 

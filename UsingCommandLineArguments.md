# Passing Arguments to SCons from the Command Line

SCons is mainly instructed about build objectives by writing configuration files - SConscripts. However since build circumstances vary, it is often useful to also be able to control the way scons is invoked, and several ways to do that are provided: through command line options that are provided by scons; through custom command line options that are defined in SConscripts; through command line targets and build variables; and through environment variables.

This discussion is intended to augment the official documentation, but always refer back to it for the definitive word: the [SCons User Guide](http://www.scons.org/doc/production/HTML/scons-user.html#chap-command-line) and a more in-depth presentation of the topic in the [SCons manpage](http://www.scons.org/doc/production/HTML/scons-man.html#commandline_construction_variables).

<!-- TOC -->
## Contents
- [Introduction](#introduction)
- [Command Line Targets](#command-line-targets)
- [Command Line Build Variables](#command-line-build-variables)
- [Adding Custom Options](#adding-custom-options)
- [Environment Variables](#environment-variables)
<!-- /TOC -->

## Introduction

There are three types of arguments that can be given to scons on the command line:

- targets, which represent things SCons should build.
- build variables, which look like Python keyword arguments.
- options, which start with a dash: with a single dash they are called short options; with a double dash they are called long options. Short options can be combined togther or given separately (`-abc` means the same as `-a -b -c`). Some options may require a following argument word, and some options may take an optional following argument word, logically this option-argument is considered together with the option.  The options scons out of the box knows to accept are listed in the manpage; an scons build system can also be extended by defining custom options.

SCons treats each of these pieces of information differently.

## Command Line Targets

Any single-word arguments that don't begin with a dash and don't contain an equal sign are collected as targets. SCons will match the command line targets with the the targets it computes after processing the SConscripts, and adjust the build to meet that request; if there are no targets specified it will build the default target.  Targets can be files to build, or directories, or they can be phony targets defined using the `Alias()` function.  Targets collected from the command line are made available in the special variable `COMMAND_LINE_TARGETS`.

## Command Line Build Variables

Build variables can be set on the command line by using arguments that take the form `key=value`.  These are split only on the first equal sign, such that `foo=bar=baz` will find a key of `foo` and a value of `bar=baz`.

The simplest way to handle these custom arguments is to let SCons do the parsing by creating a `Variables` object and using the `Add()` function, which stores any matching key with its value into a construction environment variable:

```python
vars = Variables(None, ARGUMENTS)
vars.Add(EnumVariable(key='BUILD_TYPE', 
                      help='type of build to use', 
                      default='debug',  
                      allowed_values=('debug', 'release', 'optimized')))

env = Environment(variables=vars)

if env['BUILD_TYPE'] == 'debug':
    print '*** debug build'

if env['BUILD_TYPE'] == 'release':
    print '*** release build'

if env['BUILD_TYPE'] == 'optimized':
    print '*** optimized build'
```

```console
$ scons
scons: Reading SConscript files ...
*** debug build
[...]

$ scons BUILD_TYPE=release
scons: Reading SConscript files ...
*** release build
[...]

$ scons BUILD_TYPE=no_build
scons: Reading SConscript files ...
scons: *** Invalid value for option BUILD_TYPE: no_build.  Valid values are: ('debug', 'release', 'optimized')
```

### the ARGUMENTS variable

When SCons collects command-line build variables, it makes them available in two special variables, `ARGUMENTS`, which is a dictionary, and `ARGLIST`, which is a list of the key-value pairs. You can handle such arguments by examining these special variables.

The `ARGUMENTS` variable presents the values in an easy to consume form. Since you don't know ahead of time if a variable has been set, it us usually best to use the dictionary `get` method, so that a default value can be obtained, rather than taking a `KeyError` exception if not set:

```python
if ARGUMENTS.get('release', '0') == '1':
    print "*** Release build..."
    buildroot = 'release'
else:
    print "*** Debug build..."
    buildroot = 'debug'
```

```console
$ scons myproject
[...]
*** Debug build...
[...]

$ scons myproject release=0
[...]
*** Debug build...
[...]

$ scons myproject release=1
[...]
*** Release build...
[...]
```

As a Python dict, `ARGUMENTS` follows the rule that setting a value for a key replaces any previous value; that means "last one wins" on the command line:

```console
$ scons myproject release=1 release=0
[...]
*** Debug build...
[...]
```

### the ARGLIST variable

Since the `ARGUMENTS` dictionary stores only one the last value for a given keyword, it can be useful in some cases to fetch the command line data from the `ARGLIST` variable instead.  `ARGLIST` is the *ordered* list of (key,value) pairs as they were found on the SCons command line. For example:

```python
build_profiles = [v for k, v in ARGLIST if k == 'profile']
print('*** selected build profiles: ' + str(build_profiles))
```

```console
$ scons myproject profile=debug profile=optimized
[...]
*** selected build profiles: ['debug', 'optimized']
[...]
```

See also:

- `AddVariables()` to add several declarations at once
- `UnknownVariables()` to retrieve command line arguments unknown to the Variables class
- `BoolVariable()` to handle arguments with only true/false value
- `ListVariable()` to handle arguments that can hold several values at once (`BUILD_TYPE=debug,release` / `BUILD_TYPE=all` / ...)
- `PathVariable()` to handle arguments whose value is a path (`CONFIG_FILE=/path/to/my/config`)
- `PackageVariable()` to handle arguments whose value is a package that can be enabled/disabled

## Adding Custom Options

Instead of adding arguments to the command line, there are cases when it is more convenient to use an option.  SCons provides an interface for doing that through the use of the `AddOption` function (using the same interface as the `add_option` function from the `optparse` module of the Python standard library).

One use case for this is to make an SCons build look more like another familiar environment. For example build systems from the GNU/Linux environment quite often take a `--prefix` option to fix where build results are to be installed. Here is an example of adding support for `--prefix` to an SCons setup:

```python
AddOption('--prefix',
          dest='prefix',
          type='string',
          nargs=1,
          action='store',
          metavar='DIR',
          help='installation prefix')

env = Environment(PREFIX=GetOption('prefix'))

installed_foo = env.Install('$PREFIX/usr/bin', 'foo.in')
Default(installed_foo)
```

There is no inherent reason why adding an option this way is better or worse than adding a variable of appropriate type - the prefix example could also have been added as a `PathVariable`, but then would be invoked without the `--` long-option specifier.

### Avoiding Problems with Custom Options

The extra flexibility that comes with using `AddOption` can be very appealing but it does come with a caveat. As mentioned above, targets are made available in `COMMAND_LINE_TARGETS` and build variables in `ARGUMENTS` and `ARGLIST`, so they can be examined in an SConscript.  That means they must be collected before the SConscripts are processed.  Unfortunately, the flexible option processing facility used by SCons exposes some ambiguitites. For long options which take one or more following arguments, we don't know before we have been told what they are: `--prefix=/usr/local/bin` is clear because it is a single word to break up, but `--prefix /usr/local/bin` could be either an option without argument, followed by a standalone argument (which scons would then consider as a command line target) or it could be an option which takes an argument.  The information in the `AddOption()` call removes that ambiguity - but since that appears in an SConscript, that information comes too late, SCons has already collected the argument `/usr/local/bin` and put it in the `COMMAND_LINE_TARGETS` bucket. A similar ambiguity exists with single-letter options: we cannot tell, before we have seen the `AddOption`, whether `-fLOG` is `-f` with an associated argument `LOG` or the four single-letter arguments `-f` `-L` `-O` `-G` run together, nor can we tell if `-f LOG` is option+arg or option-followed-by-target.

To avoid getting into trouble with added options, here are some guidelines:

- Avoid calling scons with command lines that use space rather then `=` as the option/argument separator. Using a space is legal syntax, and is not a problem for the SCons built-in options, but due to the ambiguity exposed when the option is defined in the SConscript, should not be used there.
- Avoid defining single-character options that take a following argument.
- Avoid defining added options which take multiple following arguments. Such arguments will by their nature be space-separated, and thus run into the problem.  Instead, use a style similar to that described in the SCons `ListVariable()` function: use a single following argument which may consist of one or more comma-separated values.
- Consider whether using `VARIABLES` might be a workable solution instead. 


## Environment Variables

One final note: normally, SCons does not forward environment variables from the caller's shell to the SCons invocation, but there is one significant exception: the `SCONSFLAGS` variable can be used to control scons by holding options that could be specified on the command line, and they will then be treated as if they came from the command line.  

For any other environment variables, the SConscripts can fetch the values and use them as they see fit, but they must do so intentionally.

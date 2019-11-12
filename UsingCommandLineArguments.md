**How to pass arguments from the SCons command-line ?**

SCons provides several ways to pass data through the command-line. Short descriptions and examples of the different alternatives can be found in the [SCons User Guide](http://www.scons.org/doc/production/HTML/scons-user.html#chap-command-line) and a more in-depth presentation of the interface in the [SCons MAN page](http://www.scons.org/doc/production/HTML/scons-man.html#commandline_construction_variables).

Solutions:

[TOC]


---


# Adding command-line build variables

SCons provides the ARGUMENTS dictionary and the ARGLIST list containing the command line arguments (as strings).

The simplest way to handle custom arguments is to let SCons do the parsing by creating a `Variables` object and using the `Add()` function:

```python
vars = Variables(None, ARGUMENTS)
vars.Add(EnumVariable('BUILD_TYPE', 'type of build to use', 'debug',  allowed_values=('debug', 'release', 'optimized')))

env = Environment(variables = vars)

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

See also:

* AddVariables() to add several declarations at once
* UnknownVariables() to retrieve command line arguments unknown to the Variables class
* BoolVariable() to handle arguments with only true/false value
* ListVariable() to handle arguments that can hold several values at once (BUILD_TYPE=debug,release / BUILD_TYPE=all / ...)
* PathVariable() to handle arguments whose value is a path (CONFIG_FILE=/path/to/my/config)
* PackageVariable() to handle arguments whose value is a package that can be enabled/disabled


---


# Adding options

Instead of adding arguments to the command line, there are cases when it is more convenient to use an option instead.

SCons provides an interface for doing that, mainly through the use of the AddOption function (using the same interface as the optparse.add_option function of the python library).

A typical example is declaring a prefix for targets installation:

```python
AddOption('--prefix',
          dest='prefix',
          type='string',
          nargs=1,
          action='store',
          metavar='DIR',
          help='installation prefix')

env = Environment(PREFIX = GetOption('prefix'))

installed_foo = env.Install('$PREFIX/usr/bin', 'foo.in')
Default(installed_foo)
```

---


# Doing manual checks

You can also handle the command-line arguments all by yourself by querying the data from ARGUMENTS (dictionary) or ARGLIST (list).

### the ARGUMENTS variable
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

Note however that only the last value provided is stored in ARGUMENTS. For example:

```console
$ scons myproject release=1 release=0
[...]
*** Debug build...
[...]
```


### the ARGLIST variable

Since the ARGUMENTS dictionary stores only one value for a given keyword, it can be useful for some users to fetch the command line data from the ARGLIST variable instead.

It is the *ordered* list of (key,value) found on the SCons command line. For example:

```python
build_profiles = []
for key, value in ARGLIST:
    if key == 'profile':
        build_profiles.append(value)

print '*** selected build profiles: ' + str(build_profiles)
```

```console
$ scons myproject profile=debug profile=optimized
[...]
*** selected build profiles: ['debug', 'optimized']
[...]
```


**How to hide command lines in SCons output ?**

Sometimes you want SCons to only show a summary of the build commands rather than the full things with all the millions of options.

Starting from SCons 0.96.92, there are basically two ways to do this.

Solutions:

[TOC]


# Use CCCOMSTR/LINKCOMSTR/JAVACCOMSTR/...

Define env['CCCOMSTR'] to whatever you want (like "Compiling $SOURCE ..."); that just overrides the C compiler message. All standard commands have a [XXXX]STR variable that is used instead of the actual command line if it's defined.

Example:

```python
#!python
# SConstruct

env = Environment(CCCOMSTR   = "*** Compiling $TARGET",
                  LINKCOMSTR = "--- Linking $TARGET")

env.Program('foo', [ 'foo.c', 'bar.c' ])
```

```txt
$ scons -Q
*** Compiling bar.o
*** Compiling foo.o
--- Linking foo
```

For more information you can refer to the corresponding section of the [User Manual](http://www.scons.org/doc/production/HTML/scons-user.html#idp1378428532) or browse the [Man Page](http://scons.org/doc/production/HTML/scons-man.html) to find a particular XXXXCOMSTR variable.

---

# Use PRINT_CMD_LINE_FUNC

This solution takes a little more work than the XXXXCOMSTR solution but is also more flexible: define a PRINT_CMD_LINE_FUNC that takes over the printing of the command lines.

This function will be called by SCons whenever it needs to print a command line, thus you can do basically any transformation of tha command line output.

Example:

```python
#!python
# SConstruct

def print_cmd_line(s, targets, sources, env):
    """s       is the original command line string
       targets is the list of target nodes
       sources is the list of source nodes
       env     is the environment"""
    sys.stdout.write(" Making %s ...\n"% (' and '.join([str(x) for x in targets])))

env = Environment()
env['PRINT_CMD_LINE_FUNC'] = print_cmd_line
```

I like to use this to print a short version to stdout, while logging the full command to a log file:


```python
#!python
# SConstruct

def print_cmd_line(s, targets, sources, env):
    if config.quiet:
        sys.stdout.write(" %s...\n"%(' and '.join([str(x) for x in targets])))
        # Save real cmd to log file
        open(env['CMD_LOGFILE'], 'a').write("%s\n" % s)
    else:
        sys.stdout.write("%s\n"%s)

env['PRINT_CMD_LINE_FUNC'] = print_cmd_line
env['CMD_LOGFILE'] = 'build-log.txt'
```

You can set config.quiet to 1 however you like; parse from cmdline option, use env['CMDLINE_QUIET'] instead, whatever. Notice it's not a full build-logging solution because the _output_ from the commands doesn't go into the build-log file.  But it's still better than clogging up your shell.


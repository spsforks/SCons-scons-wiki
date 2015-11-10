**How to get the list of targets the user entered on command line ?**

SCons provides a conveniant variable [COMMAND_LINE_TARGETS](http://www.scons.org/doc/production/HTML/scons-user.html#sect-command-line-targets) containing the list of all targets specified on the command line.

This example shows how you can prevent a target ('.' in this case) from being used:

```txt
if '.' in COMMAND_LINE_TARGETS:
   print "error: You may not use the '.' target, please use 'all' or name a specific target."
   Exit(1)

env = Environment()
env.Alias('all', ['.'])
```

Running SCons on this particular SConstruct will provide the following result:

```txt
$ scons .
scons: Reading SConscript files ...
error: You may not use the '.' target, please use 'all' or name a specific target.

$ scons all
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: 'all' is up to date.
scons: done building targets.
```


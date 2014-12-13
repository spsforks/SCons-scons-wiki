
As far as I can tell, SCons does not have a way to run custom clean actions - it only knows how to delete targets. 

If you have some custom work for scons --clean to do, such as an 'ant clean', the following recipe worked for me. The code (for example package names) is approximate because I do not  have scons on this computer and I do not have a printout. Also the behaviour below is to perform a clean action if it is specified on the command line or if '.' was specified and the clean was run from the top level dir. 

The downside of doing it this way is that the actions are processed in the order that they are found, but that isn't usually a problem for clean actions. 


```txt
  def CleanFlagIsSet() :
    import SCons.Script.Main
    return SCons.Script.Main.options.clean

  def LaunchedFromTopDir() :
    return DefaultEnvironment().GetLaunchDir() == Dir('#')

  def CleanAction(name,action) :
    if CleanFlagIsSet() :
      if     len(COMMAND_LINE_TARGETS) == 0 \
          or name in COMMAND_LINE_TARGETS \
          or LaunchedFromTopDir() and '.' in COMMAND_LINE_TARGETS \
          :
        Execute(action)

  #example usage
  Command('ant',['build.xml'],['$ANT_BIN/ant build'])
  CleanAction('ant',Action(['$ANT_BIN/ant clean']))

```
This way if you run 'scons -c ant' or just 'scons -c' and 'ant clean' will get run. 

**Awesome!  Thanks!  Here is my version that seems to work well. (little more rigorous about testing whether clean should be run e.g. if invoked from subdir with -u** 


```txt
# Take list of targets. Return '1' if they should be cleaned based on
# current command line, '0' otherwise.
def TestClean(targets):
    import os
    # want it to execute if:
    #     global clean
    #     higher directory clean
    #     target clean
    import SCons.Script.Main
    # test if clean specified on command line
    if not SCons.Script.Main.options.clean:
        return
    # normalize targets to absolute paths
    for i in range(len(targets)):
        targets[i] = File(targets[i]).abspath
    launchdir=DefaultEnvironment().GetLaunchDir()
    topdir=Dir("#").abspath
    cl_targets=COMMAND_LINE_TARGETS
    if len(cl_targets) == 0:
        cl_targets.append(".")
    for i in range(len(cl_targets)):
        full_target = ""
        if cl_targets[i][0] == '#':
            full_target = os.path.join(topdir,cl_targets[i][1:0])
        else:
            full_target = os.path.join(launchdir,cl_targets[i])
        full_target = os.path.normpath(full_target)
        for target in targets:
            if target.startswith(full_target):
                return 1
    return 0

def CleanAction( targets, action):
    if TestClean(targets):
        Execute(action)
```

## Great - that helps a lot!

But` File(targets[i]).abspath `has some troubles with directories, so - you are right - there is a new version with minor changes: 

* add` env `parameter for` AddMethod() ` 
* use` env.subst() `to get absolute paths of Files _and_ Dirs 
* use` env.GetOption('clean') `instead of` File(targets[i]).abspath ` 

```txt
def TestClean(env, targets):
        import os
        if not env.GetOption('clean'):
                return
        # normalize targets to absolute paths
        targets = env.subst('${TARGETS.abspath}', target=targets).split()
        launchdir = env.GetLaunchDir()
        topdir = env.Dir("#").abspath
        cl_targets = COMMAND_LINE_TARGETS
        if len(cl_targets) == 0:
                cl_targets.append(".")
        for i in range(len(cl_targets)):
                full_target = ""
                if cl_targets[i][0] == '#':
                        full_target = os.path.join(topdir,cl_targets[i][1:0])
                else:
                        full_target = os.path.join(launchdir,cl_targets[i])
                full_target = os.path.normpath(full_target)
                for target in targets:
                        if target.startswith(full_target):
                                return 1
        return 0

def CleanActionFunc(env, targets, action):
        if TestClean(env, targets):
                env.Execute(action)

env.AddMethod(CleanActionFunc, 'CleanAction')
```
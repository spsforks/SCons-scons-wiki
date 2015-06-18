Here is a fragment that illustrates how to make Phony targets that run commands.  The AlwaysBuild line makes sure the command runs even if there happens to be a file named the same as the target. 


```
#!python 
def PhonyTarget(target, action):
        phony = Environment(ENV = os.environ,
                            BUILDERS = { 'phony' : Builder(action = action) })
        AlwaysBuild(phony.phony(target = target, source = 'SConstruct'))

PhonyTarget('TAGS', 'tools/mktags.sh -e')
```
Here's a better implementation that handles multiple targets and doesn't require generating an Environment every time. 


```
#!python 
def PhonyTargets(env = None, **kw):
    if not env: env = DefaultEnvironment()
    for target,action in kw.items():
        env.AlwaysBuild(env.Alias(target, [], action))

PhonyTargets(TAGS = 'tools/mktags.sh -e')

env = Environment(parse_flags = '-std=c89 -DFOO -lm')
PhonyTargets(env, CFLAGS  = '@echo $CFLAGS',
                  DEFINES = '@echo $CPPDEFINES',
                  LIBS    = '@echo $LIBS')
```
The output looks like this: 
```txt
$ scons TAGS
tools/mktags.sh -e
 ...
$ scons CFLAGS
-std=c89
$ scons DEFINES
FOO
$ scons LIBS
m
```
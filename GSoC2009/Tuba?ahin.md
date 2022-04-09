
The simplest way is to do something like this: 


```python
# use GTK
CCFLAGS = ' `pkg-config --cflags gtk+-2.0` '
LINKFLAGS = ' `pkg-config --libs gtk+-2.0` '

env = Environment(CCFLAGS=CCFLAGS, LINKFLAGS=LINKFLAGS)
env.Program('toaster-test.c')
```
Remember to keep them separate, you cannot do what you do in makefiles and specify --cflags and --libs together. 

However, the cleaner, more correct - and really not much harder - way is to use [ParseConfig](https://scons.org/doc/production/HTML/scons-man.html#f-ParseConfig) like this:


```python
env = Environment()

# add support for GTK
env.ParseConfig('pkg-config --cflags --libs gtk+-2.0')

env.Program('toaster-test.c')
```
Of course, the above steps assume pkg-config and GTK+ are installed (though they will almost always be). If you want your configuration to be able to check for the existence of pkg-config, use something like what follows: 


```python
env = Environment()

def CheckPKGConfig(context, version):
    context.Message("Checking for pkg-config... ")
    ret = context.TryAction("pkg-config --atleast-pkgconfig-version=%s" % version)[0]
    context.Result(ret)
    return ret

def CheckPKG(context, name):
    context.Message("Checking for %s... " % name)
    ret = context.TryAction("pkg-config --exists '%s'" % name)[0]
    context.Result(ret)
    return ret

# Configuration:

conf = Configure(
    env, custom_tests={"CheckPKGConfig": CheckPKGConfig, "CheckPKG": CheckPKG}
)

if not conf.CheckPKGConfig("0.15.0"):
    print("pkg-config >= 0.15.0 not found.")
    Exit(1)

if not conf.CheckPKG("gtk+-2.0 >= 2.4.9"):
    print("GTK+-2.0 >= 2.4.9 not found.")
    Exit(1)

# Your extra checks here

env = conf.Finish()

# Now, build:

env.ParseConfig("pkg-config --cflags --libs gtk+-2.0")

env.Program("toaster-test.c")
```

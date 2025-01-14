
We stick this in our SConstruct: 


```python
#!python

def print_config(msg, two_dee_iterable):
    # this function is handy and can be used for other configuration-printing tasks
    print
    print msg
    print
    for key, val in two_dee_iterable:
        print "    %-20s %s" % (key, val)
    print

def config_h_build(target, source, env):

    config_h_defines = {
        # this is where you put all of your custom configuration values
        "install_prefix": prefix_variable_fed_by_user,
        "version_str": "1.0",
        "debug": debug # this is an int.  1 for true, 0 for false
    }

    config_h_defines["foo"] = "hey look i added something else"

    print_config("Generating config.h with the following settings:",
                  config_h_defines.items())

    for a_target, a_source in zip(target, source):
        config_h = file(str(a_target), "w")
        config_h_in = file(str(a_source), "r")
        config_h.write(config_h_in.read() % config_h_defines)
        config_h_in.close()
        config_h.close()
```
If you want to get values directly from your environment you can set config_h_defines to env.Dictionary(): 
```python
#!python
def config_h_build(target, source, env):

    config_h_defines = env.Dictionary()

    print_config("Generating config.h with the following settings:",
                  config_h_defines.items())

    for a_target, a_source in zip(target, source):
        config_h = file(str(a_target), "w")
        config_h_in = file(str(a_source), "r")
        config_h.write(config_h_in.read() % config_h_defines)
        config_h_in.close()
        config_h.close()
```
And we call it like this: 


```python
#!python
env.AlwaysBuild(env.Command('config.h', 'config.h.in', config_h_build))
```
And of course here is our mocked-up config.h.in: 


```txt
#define INSTALL_PREFIX "%(install_prefix)s"

#define VERSION_STR "%(version_str)s"

#define FOO "%(foo)s"

#if %(debug)d
#define YES_THIS_IS_A_DEBUG_BUILD 1
#else
#define NDEBUG 1
#endif

```
This would generate the following config.h.  We assume that the prefix was set to /usr/local and that it is *not* a debug build. 


```txt
#define INSTALL_PREFIX "/usr/local"

#define VERSION_STR "1.0"

#define FOO "hey look i added something else"

#if 0
#define YES_THIS_IS_A_DEBUG_BUILD 1
#else
#define NDEBUG 1
#endif
```
The whole sequence of: 


```txt
#if %(blah)d
#define WHATEVER
#endif
```
Is kind of ugly, I'm pretty sure you could also do: 


```txt
#define WHATEVER %(blah)d
```
and then in your code, check for it by doing #if WHATEVER, instead of #ifdef WHATEVER. 

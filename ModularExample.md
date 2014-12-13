

## Introduction

This page describes one way to create a modular build that can support multiple platforms and support building multiple setups at a time.  This is one way, not necessarily the best way. 


## Supporting multiple builds

To support multiple builds at a time, each build can be separated into a setup file.  One or more files can be specified by the _SETUP_ on the command line.  If none are specified only the command line options are used: 


```python
#!python 
import os
import glob

setup = ARGUMENTS.get('SETUP', None)
if setup is None:
  setup = [ None ] # If not setup specified, do one pass only with ARGUMENTS
else:
  parts = setup.split(os.pathsep)
  setup = []
  for part in parts:
    setup.extend(glob.glob(part))
  if len(setup) == 0:
    print 'SETUP specified but no matching setup files found'
    Exit()
```

## Separating the configuration

To simplify the configuration of the environments and reduce the amount of conditional tests, each supported platform,compiler,etc is separated into a configuration module.  This configuration is specified by the _CONFIG_ option and loaded dynamically.  It contains certain useful functions for creating the options, environment, and configure tests, as well as preparing the environment with any needed variables and flags.  Before creating this configuration, it still needs to be detected from the setup file or command line: 


```python
#!python 
def DetectConfig(file, args):
  import sys

  dummyvars = Variables(file, args)
  dummyvars.Add('CONFIG')
  dummyenv = Environment(options=dummyopts, TOOLS=[])

  name = dummyenv['CONFIG']
  if not name:
    return None

  # Dynamically load the configuration module
  name = 'build.config.' + name
  __import__(name, dict(), dict())

  return sys.modules[name]
```
Then, for each setup file create the options, build environment, tests, etc. 


```python
#!python 
for setupfile in setup:

  config = DetectConfig(setupfile, ARGUMENTS)
  if config is None:
    # Raise error, or log error and continue with next setup
    continue

  # Create variables, first config-specific then the global ones
  vars = config.Variables(setupfile, ARGUMENTS)

  vars.Add(...)

  # Create environment add do config-specific initialization from variables
  # such as loading tools, setting build options, build flags, etc.  Then do
  # and global setup needed
  env = config.Environment(vars)

  ...
  ...

  # Running configure tests by getting them from the config module, passing in any extra
  # tests needed globaly.  The config module will run some config-specific tests and then
  # return the Configure object for any more tests needed
  conf = config.Configure(env, extra_tests)

  conf.Check...

  env = conf.Finish()

  Export('env', 'config')
```
The config module's Environment and Configure functions may also add some helper methods to the base environment.  It should use _env.[AddMethod](AddMethod)_ and not _[AddMethod](AddMethod)_ so that the method added will get rebound for any cloned environment.  In addition other files may also add some helper methods. 


### Platform-specific code

The config module can set up into the environment which platform-specific code directory should be build, so the build system can then use that directory to build the platform specfic code library, and add a method for the later code to use that library: 

src/SConscript: 
```python
#!python 
Import('*')

# First build platform-dependent code library
# The SConscript file will add a method to the base environment 'SetupPlatformLibrary'
SConscript(env['PLATFORMDIR'] + '/SConscript')

# Next prepare and build main code
sources = Glob('*.c')

lenv = env.Clone()
lenv.SetupPlatformLibrary()

program = lenv.Program(sources)

# Remember the target for later packaging in the base environment
env['BUILDTARGETS']['program'] = program
```

Here is a Builder that runs `make`.  It's intended to be used along with [UnTarBuilder](UnTarBuilder) and [AutoConfigBuilder](AutoConfigBuilder) to extract some source code, configure it, and build it. 

The Builder accepts several options to control build targets, execution environment, and make command-line options.  It will also pass the SCons `-j` parameter to the make command (but there's an option to prevent that). 

[[!toc 1]] 


# Definition


```python
#!python 

# Make Builder: Runs make.
#
# Parameters:
#    MakePath -- SCons Dir node representing the directory in which to run make.  REQUIRED.
#    MakeCmd -- The 'make' executable to run.
#               Default: make
#    MakeEnv -- Dictionary of variables to set in the make execution environment.
#               Default: none
#    MakeOpts -- Options to pass on the make command line.
#                Default: none
#    MakeOneThread -- Don't pass any -j option to make.
#                     Default: False
#    MakeTargets -- String of space-seperated targets to pass to make
#                   Default: ""

import os
import subprocess

from SCons.Script import *

def parms(target, source, env):
    """Assemble various Make parameters."""

    if 'MakePath' in env.Dictionary().keys():
        make_path = env.subst(str(env['MakePath']))
    else:
        print "Make builder requires MakePath variable"
        Exit(1)

    make_cmd = 'make'
    if 'MakeCmd' in env.Dictionary().keys():
        make_cmd = env.subst(env['MakeCmd'])
    elif 'MAKE' in env.Dictionary().keys():
        make_cmd = env.subst(env['MAKE'])

    make_env = None
    if env['CROSS_BUILD']:
        make_env = env['CROSS_ENV']
    if 'MakeEnv' in env.Dictionary().keys():
        if make_env == None:
            make_env = {}
        else:
            # We're appending to an existing dictionary, so create a copy
            # instead of appending to the original env['CROSS_ENV']
            make_env = env['CROSS_ENV'][:]
        for (k,v) in env['MakeEnv'].items():
            make_env[k] = v

    make_opts = None
    if 'MakeOpts' in env.Dictionary().keys():
        make_opts = env.subst(env['MakeOpts'])

    make_jobs = GetOption('num_jobs')
    if 'MakeOneThread' in env.Dictionary().keys() and env['MakeOneThread']:
        make_jobs = 1

    make_targets = None
    if 'MakeTargets' in env.Dictionary().keys():
        make_targets = env.subst(env['MakeTargets'])

    return (make_path, make_env, make_targets, make_cmd, make_jobs, make_opts)

def message(target, source, env):
    """Return a pretty Make message"""

    (make_path,
     make_env,
     make_targets,
     make_cmd,
     make_jobs,
     make_opts) = parms(target, source, env)

    myenv = env.Clone()
    # Want to use MakeTargets in the MAKECOMSTR, but make it pretty first.
    if 'MakeTargets' in myenv.Dictionary().keys():
        myenv['MakeTargets'] += ' '
    else:
        myenv['MakeTargets'] = ''

    if 'MAKECOMSTR' in myenv.Dictionary().keys():
        return myenv.subst(myenv['MAKECOMSTR'],
                            target = target, source = source, raw = 1)

    msg = 'cd ' + make_path + ' &&'
    if make_env != None:
        for k, v in make_env.iteritems():
            msg += ' ' + k + '=' + v
    msg += ' ' + make_cmd
    if make_jobs > 1:
        msg += ' -j %d' % make_jobs
    if make_opts != None:
        msg += ' ' + ' '.join(make_opts)
    if make_targets != None:
        msg += ' ' + make_targets
    return msg

def builder(target, source, env):
    """Run make in a directory."""

    (make_path,
     make_env,
     make_targets,
     make_cmd,
     make_jobs,
     make_opts) = parms(target, source, env)

    # Make sure there's a directory to run make in
    if len(make_path) == 0:
        print 'No path specified'
    if not os.path.exists(make_path):
        print 'Path %s not found' % make_path

    # Build up the command and its arguments in a list
    fullcmd = [ make_cmd ]

    if make_jobs > 1:
        fullcmd += [ '-j', str(make_jobs) ]

    if make_opts:
        fullcmd += make_opts

    if make_targets:
        fullcmd += make_targets.split()

    # Capture the make command's output, unless we're verbose
    real_stdout = subprocess.PIPE
    if 'MAKECOMSTR' not in env.Dictionary().keys():
        real_stdout = None

    # Make!
    make = subprocess.Popen(fullcmd,
                            cwd = make_path,
                            stdout = real_stdout,
                            env = make_env)

    # Some subprocesses don't terminate unless we communicate with them
    output = make.communicate()[0]
    return make.returncode

def generate(env, **kwargs):
    env['BUILDERS']['Make'] = env.Builder(
        action = env.Action(builder, message))

def exists(env):
    if env.WhereIs(env.subst('$MAKE')) != None:
        return True
    return False
```

# Installation

To load this Builder into your environment, save the above as `Make.py` in your `site_scons/site_tools/` directory, then add it as a tool to your environment: 
```python
#!python 
env = Environment(tools = ['default', 'Make'])
# or
otherenv.Tool('Make')
```

# Usage

You use this builder by giving it `source` and `target` parameters as usual, but also specifying `MakePath` to tell it in which directory to run `make`. 


```python
#!python 
# Define the sources for the make build, so SCons can track dependencies
# (or just set source=None to have SCons run make all the time and
# let make track dependencies).
src = Glob('foo-1.2.3/*.c')

# Run make inside the foo-1.2.3/ directory
foolib = env.Make(source = src,
                  target = [ 'foo-1.2.3/.libs/libfoo.a',
                             'foo-1.2.3/.libs/libfoo.so' ],
                  MakePath = Dir('foo-1.2.3'))
```
If your environment has `MAKECOMSTR` defined, the builder uses that string to print its command message and also hides the command's output.  Without `MAKECOMSTR` the builder prints the full make command as well as the command's output. 


## Parameters

* `MakePath` -- (**Required**) SCons Dir node representing the directory in which to run make. 

* `MakeCmd` -- (Default: `make`) The 'make' executable to run. 

* `MakeEnv` -- (Default: _none_) Dictionary of variables to set in the make execution environment. 

* `MakeOpts` -- (Default: _none_) Options to pass on the make command line. 

* `MakeOneThread` -- (Default: `False`) Don't pass any -j options to make. 

* `MakeTargets` -- (Default: _none_) String of space-separated targets for make to build. 

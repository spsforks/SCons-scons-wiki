Here is a simple Builder that runs a `configure` script inside a directory.  It's intended to be used along with [UnTarBuilder](UnTarBuilder) and [MakeBuilder](MakeBuilder) to extract some source code, configure it, and build it.

**Table of Contents**

[TOC]

# Definition

```python
#!python 

# AutoConfig Builder:  Runs ./configure inside a directory.
#
# Parameters:
#    AutoConfigParams -- Sequence of parameter strings to include on the
#                        configure command line.
#                        Default: [ ]
#    AutoConfigTarget -- File that configure will create.
#                        Default: config.h
#    AutoConfigSource -- File that configure depends on.
#                        Default: Makefile.in

import os
import subprocess

from SCons.Script import *

def parms(target, source, env):
    """Assemble various AutoConfig parameters."""
    workdir = os.path.dirname(str(source[0]))
    params = None
    if 'AutoConfigParams' in env.Dictionary().keys():
        params = env['AutoConfigParams']
        if not isinstance(params, list):
            print 'AutoConfigParams must be a sequence'
            Exit(1)
    targetfile = 'config.h'
    if 'AutoConfigTarget' in env.Dictionary().keys():
        targetfile = env['AutoConfigTarget']
    sourcefile = 'Makefile.in'
    if 'AutoConfigSource' in env.Dictionary().keys():
        sourcefile = env['AutoConfigSource']
    return (workdir, params, targetfile, sourcefile)

def message(target, source, env):
    """Return a pretty AutoConfig message."""
    (dirname,
     params,
     targetfile,
     sourcefile) = parms(target, source, env)
    if 'AUTOCONFIGCOMSTR' in env.Dictionary().keys():
        return env.subst(env['AUTOCONFIGCOMSTR'],
                         target = target, source = source, raw = 1)
    msg = 'cd ' + dirname + ' && ./configure'
    if params is not None:
        msg += ' ' + ' '.join(params)
    return msg

def emitter(target, source, env):
    """Remap the source & target to path/$AutoConfigSource and path/$AutoConfigTarget."""
    (dirname,
     params,
     targetfile,
     sourcefile) = parms(target, source, env)

    # NOTE: Using source[0] instead of target[0] for the target's path!
    # If there's only one . in the source[0] value, then Scons strips off the
    # extension when it determines the target[0] value.  For example,
    #    AutoConfig('foo.blah')
    # sets
    #    source[0] = 'foo.blah'
    #    target[0] = 'foo'
    # (SCons does NOT do this if source[0] has more than one . )
    # Since this emitter expects the incoming source[0] value to be a directory
    # name, we can use it here for the rewritten target[0].

    return ([ os.path.join(str(source[0]), targetfile) ],
            [ os.path.join(str(source[0]), sourcefile) ])

def builder(target, source, env):
    """Run ./configure in a directory."""
    ( dirname,
      params,
      targetfile,
      sourcefile) = parms(target, source, env)
    real_stdout = subprocess.PIPE
    if 'AUTOCONFIGCOMSTR' not in env.Dictionary().keys():
        real_stdout = None
    cmd = './configure'
    if params is not None:
        cmd = [ cmd ] + params
    return subprocess.call( cmd,
                            cwd = dirname,
                            stdout = real_stdout,
                            stderr = real_stdout)

def generate(env, **kwargs):
    env['BUILDERS']['AutoConfig'] = env.Builder(
        action = env.Action(builder, message),
        emitter = emitter,
        single_source = True)

def exists(env):
    return True
```

# Installation

To load this Builder into your environment, save the above as `AutoConfig.py` in your `site_scons/site_tools/` directory, then add it as a tool to your environment: 
```python
#!python 
env = Environment(tools = ['default', 'AutoConfig'])
# or
otherenv.Tool('AutoConfig')
```

# Usage

You use this builder by giving it the directory of the code you want to configure: 
```python
#!python 
# Run configure in the foothing-1.2.3/ directory
configured = env.AutoConfig('foothing-1.2.3')
```
If your environment has `AUTOCONFIGCOMSTR` defined, the builder uses that string to print its command message and also hides the command's output.  Without `AUTOCONFIGCOMSTR` the builder prints the full configure command as well as the command's output. 


## Parameters

* `AutoConfigParams` -- (Default: _none_) Sequence of parameter strings to pass to the configure script. 

* `AutoConfigSource` -- (Default: `Makefile.in`) The file inside the source directory that SCons should use to decide if the directory needs to be reconfigured. 

* `AutoConfigTarget` -- (Default: `config.h`) The file that the configure process should create.  If this file doesn't get created, SCons will always configure the directory. 

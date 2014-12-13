

```python
#!python
# An SConscript file to untar a package, run configure and then make
# using a build directory.
#
# Replacing this with SConscript files written to compile just the
# parts of the package that we want would be quicker, but would take some time
# to do.

Import('env')

import sys
import os
import SCons.Script

def run(cmd):
    """Run a command and decipher the return code. Exit by default."""
    res = os.system(cmd)
    # Assumes that if a process doesn't call exit, it was successful
    if (os.WIFEXITED(res)):
        code = os.WEXITSTATUS(res)
        if code != 0:
            print "Error: return code: " + str(code)
            if SCons.Script.keep_going_on_error == 0:
                sys.exit(code)

import time
def ConfigureMake(target, source, env):
    """Run configure as necessary and then run make"""
    pkg_name = 'net-snmp-5.1'  # the name of the current snmp package
    baseDir = Dir("#.").abspath
    # BUILD_DIR is the top build directory relative to SConstruct
    buildDir = baseDir + '/' + env['BUILD_DIR']

    startdir = os.getcwd()   # restore cwd at the end
    if not os.path.exists(buildDir):
        os.makedirs(buildDir)
    os.chdir(buildDir)

    # Untar the source tgz file
    if not os.path.exists(pkg_name):
        cmd = 'tar xfz ' + source[0].abspath
        print '... untarring source files'
        run(cmd)

    # Change to the top of the source tree for net-snmp
    here = buildDir + '/' + pkg_name
    os.chdir(here)

    # See if configure needs to be run. Doesn't check for failed configures
    if os.path.exists('config.status'):
        print '... configure is up-to-date'
    else:
        # Customize the stock package here with other files if necessary
        # If configure needs interactive responses, write them to a file
        # config_responses and pass it as input to configure with 
        # >config_responses

        # Now run configure
        print '... running configure: ' +
          time.asctime(time.localtime(time.time()))
        cmd = './configure'
        run(cmd)
        print '... configure done: ' +
          time.asctime(time.localtime(time.time()))

    # Always run make
    print '... running make: ' + time.asctime(time.localtime(time.time()))
    run('make')
    print '... make finished: ' + time.asctime(time.localtime(time.time()))
    os.chdir(startdir)    # restore the original cwd

    return 0

def log_output_fn(target, source, env):
    """The message seen in build logs when this action is called"""
    return "Building '%s'\n from '%s'\n at: %s" % (target[0], source[0], 
      time.asctime(time.localtime(time.time())))

my_prog = env.Command(
    target = 'snmpd', # There are other targets, but this
                      # is one major one for this package
    source = '#/foo/bar/net-snmp-5.1.tar.gz', # Location of
                                              # package in 
                                              # the source tree
    action = Action(ConfigureMake, strfunction = log_output_fn),
)
# So that "scons doit" will run all this
Alias('doit', my_prog)
```
Comments and fixes to Matt Doar, [mdoar@pobox.com](mailto:mdoar@pobox.com) 


This version provides a method [UpdateNew](UpdateNew) which will only update variables that have not already been updated into the envirnment. 


```txt
# File:         variables.py
# Author:       Brian Allen Vanderburg II
# Purpose:      SCons variables wrapper
# Copyright:    This file is placed in the public domain
#
# With the normal varialble usage, any time the variables are updated
# on an enviroment, they will overwrite any changes that were made to
# existing variable, such as fixing paths, etc.  This wrapper behaves
# pretty much like a regular scons Variables object, but has an extra
# function, UpdateNew, which can update the environment with only the
# variables that have not been seen for the specified environment.
#
# Example:
#
# vars = Variables(cache, ARGUMENTS)
# vars.Add('BUILDDIR', 'Where to build', 'build')
# env = Environment(variables=vars)
#
# env['BUILDDIR'] = os.path.normpath(env['BUILDDIR'])
#
# ...
#
# # Maybe in another SConscript file
# vars.Add('ENABLE_PLUGIN', 1)
# vars.UpdateNew(env) # Does not replace modified BUILDDIR
#
# ...
# vars.Save(cache, env)
##############################################################################


# Requirements
##############################################################################

from SCons.Variables import Variables as _Base


# Variables object
##############################################################################
class Variables(_Base):
    def Update(self, env, args=None):
        self.unknown = {}
        _Base.Update(self, env, args)

        # Remember all known variables as being updated (even those with
        # default value of None and no specified value that have not been
        # changed).  A variable updated in a cloned environment is not
        # automatically considered udpated in the parent environment, but
        # a value updated in the parent environment before being cloned will
        # be considered updated in the cloned environment. 
        env['_UPDATED_VARIABLES_'] = [option.key for option in self.options]


    def UpdateNew(self, env, args=None):
        # Remember original values of already updated existing variables
        original = {}
        nonexist = []

        try:
            updated = env['_UPDATED_VARIABLES_']
        except KeyError:
            updated = None

        for option in self.options:
            if updated and option.key in updated:
                try:
                    original[option.key] = env[option.key]
                except KeyError:
                    nonexist.append(option.key)

        self.Update(env, args)

        # Restore original values for previously updated keys
        for key in original:
            env[key] = original[key]

        for key in nonexist:
            try:
                del env[key]
            except KeyError:
                pass


```
This is a slightly improved version.  It just remembers the values of the options not updates, and restores them afterward. 


```txt
# Requirements
##############################################################################

from SCons import Script
from SCons.Variables import Variables as _Base


# Variables object
##############################################################################
class Variables(_Base):
    def Update(self, env, args=None):
        self.unknown = {}
        _Base.Update(self, env, args)

    def UpdateSome(self, env, keys, args=None):
        # Make sure it is a list
        keys = Script.Flatten(keys)

        # Remember original values of the environment
        original = {}
        nonexist = []

        for option in self.options:
            if not option.key in keys:
                try:
                    original[option.key] = env[option.key]
                except KeyError:
                    nonexist.append(option.key)

        # Update into the real environment
        self.Update(env, args)

        # Restore the values for keys not to be updated
        for key in original:
            env[key] = original[key]

        for key in nonexist:
            if key in env:
                del env[key]



```
The version below is left for history.  It has the following problem I experienced.  If an option is added to variables with a default value of None, then it should not be modified in the environment if it is not found in the arguments.  This is good for values where you only want to modify the value if the user specifies it, but if not, leave it as is.  An example could be CFLAGS/etc:  If it is not in the arguments, don't modify it in the environment.  The problem is, if the internal environment somehow has the value but the external environment does not, then during [UpdateSome](UpdateSome), the internal environment's value will not be modified, but it will be copied to the external environment, modifying it even though the default value for the option was None. 


```txt
# File:         variables.py
# Author:       Brian Allen Vanderburg II
# Copyright:    This file is placed in the public domain
##############################################################################


# Requirements
##############################################################################

from SCons import Script
import SCons.Util
import SCons.Errors
from SCons.Variables import Variables as _Base


# Variables object
##############################################################################
class Variables(_Base):
    def __init__(self, *args, **kwargs):
        _Base.__init__(self, *args, **kwargs)
        self._env = Script.Environment(TOOLS=[])

    def Update(self, env, args=None):
        self.unknown = {}
        _Base.Update(self, self._env, args)
        _Base.Update(self, env, args)

    def UpdateSome(self, env, keys, args=None):
        self.unknown = {}
        _Base.Update(self, self._env, args)
        if not SCons.Util.is_Sequence(keys):
            keys = [ keys ]

        for key in keys:
            env[key] = self._env[key]

    def Save(self, filename, env=None):
        if env is None:
            env = self._env
        _Base.Save(self, filename, env)

    def GenerateHelpText(self, sort=None):
        return _Base.GenerateHelpText(self, self._env, sort)
```
The [UpdateSome](UpdateSome) method can be used to only update some variables.  Also, since it uses an internal environment, the variables can be updated into a cloned environment instead of the main environment if desired, and when saving the variables out, it will use the internal environment as well.  If another environment is specified during saving, it will use it instead.  This can be used to save out the modified values instead of the originally values. 

SConstruct: 
```txt
import os
import tools.scons # package provides Variables (among other things)

cache = ARGUMENTS.get('CACHE')

defvars = tools.scons.Variables(cache, ARGUMENTS)
defenv = Environment(TOOLS=[], ENV=os.environ)

Export('defvars', 'defenv')

SConscript('tools/config/config.py')
SConscript('src/SConscript')

if cache:
    defvars.Save(cache)
```
tools/config/config.py: 
```txt
Import('*')

defvars.Add('CONFIG', 'Which configuration to build', 'linux')
defvars.Add('BUILD', 'Build in debug or release', 'release')
defvars.Add('BITS', 'Build for 32 or 64 bit system', '')
defvars.UpdateSome(defenv, ('CONFIG', 'BUILD', 'BITS'))

# Detect bits if needed
if not defenv['BITS']:
   ...

defenv.SConscript('config_${CONFIG}.py')
```
Some later part of the build could then do this: 

src/plugins/morph/SConscript: 


```txt
Import('*')

defvars.Add(BoolVariables('ENABLE_MORPH_PLUGIN', 'Enable building the morph plugin', True))
defvars.UpdateSome(defenv, 'ENABLE_MORPH_PLUGIN')

if not defenv['ENABLE_MORPH_PLUGIN']:
    Return()

... Build the morph plugin
```
If BITS is not specified when executing SCons, it will use the default variable value in the environment.  After detecting 32 or 64 bits, the environment will be modified.  A later call to defvars.Update(defenv) would re-apply the variables to the environment, overwriting the changes to BITS.  Using [UpdateSome](UpdateSome) allows updating only the desired variables while leaving others in tact. 

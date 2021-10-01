
SCons has built-in facilities to save variables to a file and load them back - especially useful to store information like installation prefix (if you want to make an uninstall target, for instance), or the results of a configure step. 

First create a Variables object 
```python
# specify the name of the file in which variables are/will be stored
vars = Variables('build-setup.conf')

# Register which variables we're interested in and
# get values from a saved file if any.
vars.Add('config', help='', default='release')
vars.Add('prefix', help='', default='/usr/local')
vars.Add('platform', help='', default='auto')
vars.Add('glut_enabled', help='', default=False)
vars.Add('havegettext', help='', default='')

# update these variables in your environment
vars.Update(env)

# do your stuff with the variables

if env['config'] == "debug":
    env.Append(CCFLAGS=['-g', '-Wfatal-errors'])
elif env['config'] == "release":
    env.Append(CCFLAGS=['-O3', '-DNDEBUG'])

# change variables if needed (e.g. if you're running a
# 'configure' step, or if environment changed)
if changing_values:
    env['platform'] = "unix"
    # save new values
    vars.Save('build-setup.conf', env)
```

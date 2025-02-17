
* Also see [SavingVariablesToAFile](SavingVariablesToAFile) 

It's very common practice (and useful for sysadmins) to allow users to be able to specify a base directory to install a package into. This base directory is known as the prefix. Common prefixes on UNIX systems are /usr, /usr/local, /opt/appname/, or ~/.local/ . 

Here's how I set up my builds to allow installation to custom prefixes: 
```python
#!python
# SConstruct file for WidgetMaster
env = Environment()

# Get our configuration options:
opts = Variables('wm.conf') # Change wm to the name of your app
opts.Add(PathVariable('PREFIX', 'Directory to install under', '/usr', PathVariable.PathIsDir))
opts.Update(env)
opts.Save('wm.conf', env) # Save, so user doesn't have to 
                          # specify PREFIX every time

Help(opts.GenerateHelpText(env))

# ... put your configuration here ...

# Here are our installation paths:
idir_prefix = '$PREFIX'
idir_lib    = '$PREFIX/lib'
idir_bin    = '$PREFIX/bin'
idir_inc    = '$PREFIX/include'
idir_data   = '$PREFIX/share'
Export('env idir_prefix idir_lib idir_bin idir_inc idir_data')

# ... build your program here, or call SConscript files ...

libwm = env.SharedLibrary('wm', ['widget.c', 'master.c'])

env.Install(idir_lib, libwm)
env.Install(idir_inc, ['widget.h', 'master.h'])
env.Alias('install', idir_prefix)
```
If you call SConscript files, this is what one would look like: 
```python
#!python
# SConstruct file for WidgetMaster
Import('env idir_bin')
wm = env.Program('wm', ['widget.c', 'master.c', 'sprocket.c'])

env.Install(idir_bin, wm)
env.Alias('install', idir_prefix)
```
Now, the first time a user builds your application, they specify the prefix like this: 
```txt
$ scons -Q PREFIX=/opt/wm install
or
$ scons -Q PREFIX=/usr;scons -Q install
```
They only have to specify the PREFIX variable the first time they call scons, because subsequent builds read it from the file "wm.conf" which is generated automatically by the Save() function. 

** Caveats ** 

1. Using PathVariable by default makes scons fail if the user specifies a path that doesn't yet exist. Look in the man page under PathVariable for details about PathAccept (don't do validation) and other possibilities such as PathIsDirCreate (validate directory and create if not existing). 

2. Normally, autoconf and friends allow the user to specify different paths for installing binaries, libraries, etc. You could use this template to support this, if you think it is necessary. 

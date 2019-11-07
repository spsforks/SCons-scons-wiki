### Random notes to be sorted out in wiki ###

Yocto build system is supporting scons using scons class to

* http://git.yoctoproject.org/cgit.cgi/poky/plain/meta/classes/scons.bbclass

But there is a (semi minor) issue with PATH variable, Yocto updates some variables to use sysroot, while Scons avoid to be polluted by env variables.

http://scons.org/faq.html#Why_doesn.27t_SCons_find_my_compiler.2BAC8-linker.2BAC8-etc..3F_I_can_execute_it_just_fine_from_the_command_line.

You could use this code snippet as one solution to export/import env between 2 worlds:


Add in your bitbake file :

```bitbake
   inherit scons pkgconfig
   EXTRA_OESCONS += " CONFIG_ENVIRONMENT_IMPORT=True "

```


To this SConscript
 
```python
# Import env variables only if reproducibility is ensured
if target_os in ['yocto']:
    env['CONFIG_ENVIRONMENT_IMPORT'] = True
else:
    env['CONFIG_ENVIRONMENT_IMPORT'] = False

if env['CONFIG_ENVIRONMENT_IMPORT'] == True:
    print "warning: importing some environment variables for OS: %s" % target_os
    for ev in ['PATH', 'PKG_CONFIG', 'PKG_CONFIG_PATH', 'PKG_CONFIG_SYSROOT_DIR']:
        if os.environ.get(ev) != None:
            env['ENV'][ev] = os.environ.get(ev)
    if os.environ['LDFLAGS'] != None:
        env.AppendUnique(LINKFLAGS = Split(os.environ['LDFLAGS']))


```

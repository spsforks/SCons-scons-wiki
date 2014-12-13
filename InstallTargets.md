
It's often useful to be able to run "scons install" to copy the programs and shared libraries to their correct locations. Here's one way to do that: 


```python
#!python
prefix = "/usr/local"

someshlib = env.SharedLibrary('foo', "foo.c")
someprogram = env.Program("fooprog", "fooprog.c")

# the install target
env.Alias("install", env.Install(os.path.join(prefix, "lib"), someshlib))
env.Alias("install", env.Install(os.path.join(prefix, "bin"), someprogram))
```
Basically we alias 'install' to a couple of Install nodes, returned by the Install() method. That's all. 

NB: There is no need to add something like 'Depends(install, someshlib)', since SCons does find this dependency automatically. 

If you need some fine-grained install targets, you may use something like this: 


```python
#!python
Alias('install-lib', Install(os.path.join(prefix, "lib"), ...))
Alias('install-bin', Install(os.path.join(prefix, "bin"), ...))
Alias('install', ['install-bin', 'install-lib'])
```

## Permissions

Question:  how to set permissions properly (binaries get 755, headers get 644, etc.) after an install? 

* One way to do it is to create a method that acts like Install() but has an additional permission argument. Wrappers with predefined permissions are useful for cleaner markup: 

```python
#!python
import SCons

# define the custom function
from SCons.Script.SConscript import SConsEnvironment
SConsEnvironment.Chmod = SCons.Action.ActionFactory(os.chmod,
        lambda dest, mode: 'Chmod("%s", 0%o)' % (dest, mode))

def InstallPerm(env, dest, files, perm):
    obj = env.Install(dest, files)
    for i in obj:
        env.AddPostAction(i, env.Chmod(str(i), perm))
    return dest

# put this function "in" scons
SConsEnvironment.InstallPerm = InstallPerm

# great, we're ready to use it!
env.InstallPerm(bindir, ['fooprog', 'barprog'], 0755)

# but let's say we're not happy yet, we'd prefer nicer names.
SConsEnvironment.InstallProgram = lambda env, dest, files: InstallPerm(env, dest, files, 0755)
SConsEnvironment.InstallHeader = lambda env, dest, files: InstallPerm(env, dest, files, 0644)

# great, now you can also install by calling a method named 'InstallHeader' or 'InstallProgram'!
env.InstallHeader(incdir, ['foo.h', 'bar.h'])
```
Don't forget to set the umask, or created directories might get wrong permissions on Unix and Windows: 


```python
#!python
try:
    umask = os.umask(022)
    print 'setting umask to 022 (was 0%o)' % umask
except OSError:     # ignore on systems that don't support umask
    pass
```
* Another similar method to install data with correct permissions is to use a Command : 

```python
#!python
source="./data/icon.png"
target="/usr/local/share/X/icon.png"

env.Alias("install", target)
env.Command( target, source,
[
Copy("$TARGET","$SOURCE"),
Chmod("$TARGET", 0664),
])
```
where target and source could be set in a directory parsing loop for conveniance : 
```python
#!python
# where you need to implement 'RecursiveGlob' yourself 
for file in RecursiveGlob("./data", "*"):
    # strip 'data/' out to have the filepath relative to data dir
    index = file.find("data/") + len("data/")
    filename_relative = file[index:]
    source = os.path.join("./data", filename_relative)
    target = os.path.join(data_dir, filename_relative)
            
    env.Alias("install", target)
    env.Command( target, source,
    [
    Copy("$TARGET","$SOURCE"),
    Chmod("$TARGET", 0664),
    ])
```
For best results, also make sure the umask is set like described above. 


## Locale files

Installing locale files on UNIX systems can be a little tricky : 

This is an example that will handle installing .mo files for a source layout of **/po/[language code]/app_name.mo**. 
```python
#!python
# install .mo files
locale_dir = "/usr/local/share/locale"

mo_files = Glob("./po/*/app_name.mo",strings=True)
for mo in mo_files:
    # extract language code
    index_lo = mo.find("po/") + len("po/")
    index_hi = mo.find("/app_name.mo")
    lang_name = mo[index_lo:index_hi]
    # copy file
    install_location = locale_dir + "/" + lang_name + "/LC_MESSAGES/app_name.mo"
    env.Alias("install", env.InstallAs( install_location, mo ) )
```
It should be simple enough to adapt this code to layouts like **/po/[language code].mo** or any other. 


## Uninstall targets

Here's a sample uninstall function : 


```python
#!python
def create_uninstall_target(env, path, is_glob):
    if is_glob:
        all_files = Glob(path,strings=True)
        for filei in all_files:
            env.Command( "uninstall-"+filei, filei,
            [
            Delete("$SOURCE"),
            ])
            env.Alias("uninstall", "uninstall-"+filei)   
    else:
        env.Command( "uninstall-"+path, path,
        [
        Delete("$SOURCE"),
        ])
        env.Alias("uninstall", "uninstall-"+path)  
```
You can use it like this : 
```python
#!python
if 'uninstall' in COMMAND_LINE_TARGETS:
    # create uninstall targets
    create_uninstall_target(env, "/usr/local/bin/myapp", False)
    create_uninstall_target(env, "/usr/local/share/myapp/", False)
    create_uninstall_target(env, "/usr/local/share/locale/*/LC_MESSAGES/myapp.mo", True)
```
If you want to uninstall all the files installed using Install or [InstallAs](InstallAs), there is a more expeditive way: 
```python
#!python
env.Command("uninstall", None, Delete(FindInstalledFiles()))
```
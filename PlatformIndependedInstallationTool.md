
# Platform independent installation


## Introduction

Multiplatform project may have some files which should be installed to different directories on different platforms or some files which should not be installed at all on some platforms. This Tool provides set of pseudo builders to install files using default installation directory structure of the target operation system and set correct permissions on POSIX systems. It creates alias target 'install' to install all targets at once. 


## How to get the tool

Tool is available in the following git repository: [http://repo.or.cz/r/vestnik_site_scons.git](http://repo.or.cz/r/vestnik_site_scons.git) in the file smartinstall.py 

To get the latest version run: 
```console
git clone http://repo.or.cz/r/vestnik_site_scons.git
```
You can put this file into the site_scons/site_tools directory. 


## Usage

1. Set the name of your program or library to the env['package'] variable in your environment. This key should exist in the environment before tool initialization since it's used to calculate default installation paths. 
1. Initialize the tool with the Tool() method in the Environment object. 
1. You may want to change some of installation paths using the following available environment variables: 
    * env['prefix'] installation path prefix. Default value: '/usr/locla' on Linux or 'C:\Program Files\$package' on Windows 
    * env['prefix_bin'] your program installation path. On windows it's used to install *.dll files. Default value: '$prefix/bin' 
    * env['prefix_lib'] libraries installation path. Default: '$prefix/lib' 
    * env['prefix_pc'] pkg-config *pc files installation path. Default: '$prefix/lib/pkgconfig' 
    * env['prefix_inc'] header files installation path. Default: '$prefix/include/$package' on Linux or '$prefix\include' on Windows 
    * env['prefix_data'] application data installation path. Default: '$prefix/share/$package' on Linux or '$prefix\data' on Windows 
    * env['install_dev'] Install or not development files. Should be True or False Default: False 
1. Now you can use the following pseudo builders: 
    * [InstallProgram](InstallProgram)() installs files to '$prefix_bin' directory and sets 0755 permissions on Linux 
    * [InstallLibrary](InstallLibrary)() installs files to '$prefix_lib' except *.dll files on Windows which are installed to '$prefix_bin'. Sets 0755 permissions to .so files and 0644 permissions to other files on Linux. If '$install_dev' is False this builder will install only shared libraries (*.so on Linux or *.dll on Windows) other files will be ignored. **TODO**: add installing .so files with version suffixes and correct symlink creation (libMy.so -> libMy.so.1 -> libMy.so.1.2 -> libMy.so.1.2.3) on Linux. 
    * [InstallPkgConfig](InstallPkgConfig)() installs files to the '$prefix_pc' dir. Sets 0644 permissions on Linux. Doesn't install anything if '$install_dev' is False. 
    * [InstallHeader](InstallHeader)() installs files to '$prefix_inc' dir. Sets 0644 permissions on Linux. Doesn't install anything if '$install_dev' is False. 
    * [InstallData](InstallData)() installs files to '$prefix_data' dir. Sets 0644 permissions on Linux. 
1. All builders checks that 'install' target is specified and return None if not. Alias target 'install' created to install all files passed to those builders. 
1. Use `scons install` to install your package and `scons install -c` to uninstall it. 

## Example


```python
env = Environment()
env['package'] = 'foo'
env.Tool('smartinstall')

lib = env.SharedLibrary('bar',[... lib sources here ...])
prog = env.Program('foo',[... lib sources here ...], LIBS='bar')

env.InstallProgram(prog)
env.InstallLibrary(lib)
```
Running 
```console
scons install
```
will create the following installation: 

 **Linux**  |  **Windows** 
:---|:----
 `/usr/local/bin/foo`  |  `C:\Program Files\foo\bin\foo.exe` 
 `/usr/local/lib/libbar.so`  |  `C:\Program Files\foo\bin\bar.dll` 


`bar.lib` created by [SharedLibrary](SharedLibrary) builder will be ignored since '$install_dev' is set to False by default. If you explicitly set it to True

```python
env = Environment()
env['package'] = 'foo'
env['install_dev'] = True
env.Tool('smartinstall')

lib = env.SharedLibrary('bar',[... lib sources here ...])
prog = env.Program('foo',[... lib sources here ...], LIBS='bar')

env.InstallProgram(prog)
env.InstallLibrary(lib)
```
the following files will be installed: 


 **Linux**  |  **Windows**
:----|:----
 `/usr/local/bin/foo`  |  `C:\Program Files\foo\bin\foo.exe` 
 `/usr/local/lib/libbar.so`  |  `C:\Program Files\foo\bin\bar.dll`<br> `C:\Program Files\foo\lib\bar.lib` 


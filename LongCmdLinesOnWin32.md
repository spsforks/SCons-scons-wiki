
## Very long command lines on Windows

by [PhilMartin](PhilMartin) 


### Short version

We found some problems with MingW on Windows during the link phase. The command line length could exceed 10000 characters, and this was causing problems. 

Just skip to the Python Code section for the code we used to fix it. 


### Long version (for those interested in the reasons)

When we changed the build process for [Aztec](http://aztec.sourceforge.net/) to use SCons, we encountered a few problems along the way. Our project contained a number of SharedLibrary builder calls and a number of Program calls as well, and wanted to build them on Windows, using both Microsoft Visual C and MingW. 

MingW had some problems during the link phase of the build process. It turned out our link lines were in excess of 10000 characters, and this was causing some major grief with python calling spawn(). 

After some investigation, it turns out this is not a limitation of Windows, but a limitation of the C Runtime that MSVC uses (which Python was compiled with). This meant that it was at least fixable. Thanks to the flexible design of SCons, it was not only fixable, but it was very easy to do. 

All we need to do was to change the env['SPAWN'] to use our own custom spawn function. We should replace PIPED_SPAWN as well, but that never got called in our build process, so we never got around to it. The fix uses the Win32 API directly, so we avoid the command line length problem entirely. 

Here is the code that we placed in our Scons files, and it solves the linking problem with MingW quite well. The interesting part is that it does not handle the standard Windows commands, like del or mkdir. Special consideration has to be made for these. 

Here is the final section of code to achieve what we wanted. 

### Python Code


```python
if env['PLATFORM'] == 'win32':
    import win32file
    import win32event
    import win32process
    import win32security

    def my_spawn(sh, escape, cmd, args, spawnenv):
        for var in spawnenv:
            spawnenv[var] = spawnenv[var].encode('ascii', 'replace')

        sAttrs = win32security.SECURITY_ATTRIBUTES()
        StartupInfo = win32process.STARTUPINFO()
        newargs = ' '.join(map(escape, args[1:]))
        cmdline = cmd + " " + newargs

        # check for any special operating system commands
        if cmd == 'del':
            for arg in args[1:]:
                win32file.DeleteFile(arg)
            exit_code = 0
        else:
            # otherwise execute the command.
            hProcess, hThread, dwPid, dwTid = win32process.CreateProcess(None, cmdline, None, None, 1, 0, spawnenv, None, StartupInfo)
            win32event.WaitForSingleObject(hProcess, win32event.INFINITE)
            exit_code = win32process.GetExitCodeProcess(hProcess)
            win32file.CloseHandle(hProcess);
            win32file.CloseHandle(hThread);
        return exit_code

    env['SPAWN'] = my_spawn

```


---

 


### Acknowledgements

Many thanks to Tobias Sargeant for working out most of this, especially the Python side of things. 



---

 


### Remarks

* This solution based on CreateProcess works great. Thank you very much. Many people out there ignore how many toolchains don't accept any kind of command line indirection (because based on GNU gcc without many changes) but only work on MS Windows (because the provider wanted to have a nice MFC-based IDE around it, for example). Even when the toolchain accepts indirection files, the solution you give here is preferable because it is slightly faster. 
* This solution requires win32 extension. It comes standard with ActiveState distributions, for example, but not with all Python distributions. 
* The maximum command line length that you can pass to CreateProcess is **32766**. Past that limit, you get an error msg saying 'parameter incorrect' (but not which parameter and not why is it incorrect). You still need the TempFileMunge trick to deal with lines longer than that. 
* There is no such thing as "standard Windows commands". The one you name are actually shell commands. You should expect that they are not executed by the CreateProcess because that one takes executables. They will be executed as expected if you pass the shell as executable (cmd.exe) and then your commands (del, mkdir, etc.) as arguments. 
* It is good to know that this solution works if you give a full absolute path for the executable to run. If not, CreateProcess does some search, but not the PATH search that you may expect (see the MSDN doc on it). If you fail to give the complete path or if the executable is not there for some reason, you get an error msg saying "file not found" but not which file is not found. 
* This solution is known not to work with some toolchains (RealView ARM, Infineon TriCore). They give internal errors even when env['ENV'] has all the environment variables that they require. Fortunately, they all accept indirection of the command line to a temporary file. 
* An alternative solution is to use another Python. I used successfully the Cygwin-based Python interpreter to drive MS Windows-based toolchains not accepting any indirection. That also stops working at the 32kb limit. But the solution based on win32 extension you present here is simpler to set up and to use. 
by [AdrianNeagu](AdrianNeagu) 


### Some Other Tricks

We had the problem with "command line too long" error message only on Windows 2000 (XP builds would work okay). This issue is "addressed" here: [http://support.microsoft.com/default.aspx?scid=kb;en-us;830473](http://support.microsoft.com/default.aspx?scid=kb;en-us;830473) 

The solution we used was the discovery that ARM toolchain can also parse command line options  from file (via file) and add custom builder for building libraries. 

by [Amit Chakradeo](http://amit.chakradeo.net/) 


### Another way

You can also use the subprocess module (since Python 2.4). 
```python
class ourSpawn:
    def ourspawn(self, sh, escape, cmd, args, env):
        newargs = ' '.join(args[1:])
        cmdline = cmd + " " + newargs
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(cmdline, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, startupinfo=startupinfo, shell = False, env = env)
        data, err = proc.communicate()
        rv = proc.wait()
        if rv:
            print "====="
            print err
            print "====="
        return rv

def SetupSpawn( env ):
    if sys.platform == 'win32':
        buf = ourSpawn()
        buf.ourenv = env
        env['SPAWN'] = buf.ourspawn
```
Call [SetupSpawn](SetupSpawn)(env) when you need this. Thanks to xuru on #scons, we can now build and link Blender without the need to split large libraries into smaller parts. 

by Nathan Letwory (jesterKing) 

This works great, except for when there is redirection.  Is there a way to improve on this so that it can handle redirection, or even if it could go back to the old way if there is redirection? 

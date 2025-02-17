
SCons attempts to be a _clean_ build tool and only generates the environment for build operations that is necessary for success of those build operations. This is the philosophical other end of the scale from **make**, where all of the environment variables of the process are automatically active within the build statements. 

This is a good thing, since it prevents _hidden_ dependencies and other problems (even trojan horses) from affecting the build environment from one user or platform to another. 

However, sometimes you do want to import settings from your environment (see the [ExternalTools](ExternalTools) example). 

/!\ First, you should think about importing **ONLY** those settings you want: 


```txt
env = Environment()
env.Append(CCACHEDIR = os.environ['CCACHEDIR'])
```
If this is too awkward, /!\ think again, and again! 

Do you _really_ want to open this Pandora's box?! 

If you still do, then you could use the simple method shown in [ExternalTools](ExternalTools): 


```txt
env = Environment(ENV = os.environ)
```
but this is likely to break for some platforms (e.g. Win32) because the Platform initialization of SCons may have already prepared some settings (like paths, etc.) that would be overwritten and lost by the above substitution. The following method is a little more involved, but makes sure that combinative elements like paths are correctly concatenated rather than replaced: 


```txt
def ENV_update(tgt_ENV, src_ENV):
    for K in src_ENV.keys():
        if K in tgt_ENV.keys() and K in [ 'PATH', 'LD_LIBRARY_PATH',
                                          'LIB', 'INCLUDE' ]:
            tgt_ENV[K]=SCons.Util.AppendPath(tgt_ENV[K], src_ENV[K])
        else:
            tgt_ENV[K]=src_ENV[K]

env = Environment()
ENV_update(env, os.environ)
```
I tried the above and got the following error 
```txt
AttributeError: SConsEnvironment instance has no attribute 'keys':
  File "SConstruct", line 14:
    ENV_update(env, os.environ)
  File "SConstruct", line 7:
    if K in tgt_ENV.keys() and K in [ 'PATH', 'LD_LIBRARY_PATH',
```
I suspect ENV_update is supposed to be called as follows 
```txt
ENV_update(env['ENV'], os.environ)
```
SCons 0.96.1; Python 2.4.1; WinXP; - [TomHoward](TomHoward) 



---

 

Sorry to ruin this page. I run scons 0.95 on Windows ME with VC6. I alway get the anonying messages of 'Bad command or filename' when invoking cl.exe or link.exe, and my environment is OK. Finally, I change 
```txt
args = [sh, '/C', escape(string.join(args))]
```
in Platform\win32.py to 
```txt
args = [sh, '/E:4096 /C', string.join(args)]
```
Everything seems right then. That's all. 

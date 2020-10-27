

#### This is how you can get scons to behave like autoconf (having a 'configure' step first)

Many people need autoconf like functionality in their build, SConf provides this in scons.   Say you have program X which depends on stdio.h, math.h, stdlib.h, libSDL.so.  You could check for these in your build like this. 

First you must create your configuration environment. 
```python
#!python
conf = Configure(env)

# ... use conf to perform checks here ...

# keep any changes you may have performed
env = conf.Finish()

```
A good first check (that autotools usually does first) is to check that the compiler is installed and working 
```python
#!python
# ---- check for compiler and do sanity checks
if not conf.CheckCXX():
    print('!! Your compiler and/or environment is not correctly configured.')
    Exit(0)

if not conf.CheckFunc('printf'):
    print('!! Your compiler and/or environment is not correctly configured.')
    Exit(0)
```
Now we can run some checks for headers. 
```python
#!python
# check for stdio.h
if not config.CheckHeader('stdio.h'):
   print("You need 'stdio.h' to compile this program")
   Exit(1)

# check for math.h
if not config.CheckHeader('math.h'):
   print("You need 'math.h' to compile this program")
   Exit(1)
else:
  config.env.Append('-DHAS_MATH')

# check for stdlib.h
if not config.CheckCHeader('stdlib.h'):
   print("You need 'stdlib.h' to compile this program")
   Exit(1)
```
We can also check for libraries. 
```python
#!python
# check for libSDL.so
if not config.CheckLib('libSDL'):
   print("You need libSDL to compile this program")
   Exit(1)
```
You can store the results of checks as variables in the environment : 
```python
#!python
if not conf.CheckLib('openal'):
    conf.env['haveopenal'] = "no"
```
When we are all finished we call Finish() which returns an Environment.  Don't run any more checks after a call to Finish().  Any changes to the environment not made through `Configure(env).env` after the Configure() object was created and before Finish() was called will be lost, so don't change the environment after you run Configure() until you have Finish()ed. 


```python
#!python
# we are all done, don't run any checks after this
env = config.Finish()
```
Configurations are also often a good place to allow the user to define custom build flags without importing the entire environment : 
```python
#!python
# ---- check for environment variables
if 'CXX' in os.environ:
    conf.env.Replace(CXX = os.environ['CXX'])
    print(">> Using compiler " + os.environ['CXX'])

if 'CXXFLAGS' in os.environ:
    conf.env.Append(CCFLAGS = os.environ['CXXFLAGS'])
    print(">> Appending custom build flags : " + os.environ['CXXFLAGS'])
    
if 'LDFLAGS' in os.environ:
    conf.env.Append(LINKFLAGS = os.environ['LDFLAGS'])
    print(">> Appending custom link flags : " + os.environ['LDFLAGS'])
```

## When to run

You may want to check if you are cleaning before you start configuring. 
```python
#!python
# are we configuring?
if env.GetOption('clean'):
   print("We are cleaning, skip the config")
else:
   print("We are staying dirty, let's go!")
```
How can you skip the config step if which targets should be built (and therefore also cleaned) is determined during the configure step? 

If you want to do the configure only once you can check for the conf.log file which is created after each configure. 
```python
#!python
if not os.path.exists("config.log"):
        print('Configuring... ')
        conf = Configure(env)
        #do your checks...
        env = conf.Finish()
```
_note_: The above does not work if you are using Configure to auotoadd the locations of your libs to LIBS, also I suspect the above will not work if the configuration failed. 

If you'd rather have a autotools-like 'configure' step done first and once by calling 'scons configure', then call 'scons' to build, do a check like this : 
```python
#!python
if 'configure' in COMMAND_LINE_TARGETS:
```
in order to have the results of such a configured step be remembered, check article [SavingVariablesToAFile](SavingVariablesToAFile). 


## More documentation

The SConf functions of scons are documented in the scons user guide. 

More (very detailed) information can be found under the "Configure Contexts" section of the scons [manpage](http://www.scons.org/doc/HTML/scons-man.html).  There are also instructions on how to write your own checks there. 

Other autoconf macros have been contributed in scons format in article [AutoconfRecipes](AutoconfRecipes) 

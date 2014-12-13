
_Moved this from [SconstructShortMsvcWin32](SconstructShortMsvcWin32)_ 

---

 Just a quick comment:  the above isn't _really_ the shortest SConstruct possible.  That would be something like this: 
```txt
#create a.exe from a.c (assuming win32)
Program('a.c') 
```
which would build `a.exe` from `a.c` using all the defaults.  Notice that as of SCons 0.95 or so, you can use the default environment so you don't even need to create one separately. 

-- Gary O 

_you're right! I'm more verbose than I thought. JohnA_ 

`SideEffect(side_effect, target)`:
  A _side effect_ is a target that is created as a side effect of building other targets. (For example, a Windows PDB file is created as a side effect of building the `.obj` files for a static library.) This method declares **side_effect** as a side effect of building **target**. Both **side_effect** and **target** can be a list, a file name, or a node. If a target is a side effect of multiple build commands, SCons will ensure that only one set of commands is executed at a time. Consequently, you only need to use this method for side-effect targets that are built as a result of multiple build commands. 

It should be noted that side effects are not automatically cleaned by `scons -c`. To do that, please see `Clean`. 

For example, if there are two commands that write information to a shared log file, the two commands should not be run in parallel: 
```
f1 = Command('file1.out', 'file1.in', './build --log log.txt $SOURCE $TARGET')  
f2 = Command('file2.out', 'file2.in', './build --log log.txt $SOURCE $TARGET')
```
The `SideEffect()` method can be used to say that these two commands should not be run at the same time.  It can be specified a number of ways: 
```
SideEffect('log.txt', f1 + f2)
``` 
or equivalently: 
```
SideEffect('log.txt', ['file1.out', 'file2.out'])
``` 
Side effects accumulate, so this sequence is equivalent as well: 
```
SideEffect('log.txt', 'file1.out')  
SideEffect('log.txt', 'file2.out')
```
As is this sequence: 
```
SideEffect('log.txt', f1)  
SideEffect('log.txt', f2)
``` 
The `SideEffect()` method returns a list of the side-effect files, so this will also work: 
```
s = SideEffect('log.txt', f1) 
SideEffect(s, f2)
```
The file need not exist (or ever be created); by specifying a dummy side-effect file, this method still prevents parallel builds: 
```
f1 = Command('file1.out', 'file1.in', './build $SOURCE $TARGET')  
f2 = Command('file2.out', 'file2.in', './build $SOURCE $TARGET')  
SideEffect('a.dummy.file', f1 + f2)
``` 
_TODO: Add an example of a Builder that contains a `SideEffect()` call._ 

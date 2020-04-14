
When you use `Depends()` like this: 
```python
tgt = env.Command(...)
env.Depends(tgt, 'SomeAlias')

anothertgt = env.Command(...)
env.Alias('SomeAlias', anothertgt)
```
it most likely won't work like you expect it to. The string `'SomeAlias'` in this example is assumed to be the name of a sub-directory in the current directory, e.g. you will get an error saying that scons doesn't know how to build `'currdir\SomeAlias'`. 

On the other hand, if `'SomeAlias'` is defined prior to the `Depends()` being executed, then all works as expected: 
```python
anothertgt = env.Command(...)
env.Alias('SomeAlias', anothertgt)

tgt = env.Command(...)
localenv.Depends(tgt, 'SomeAlias')
```
the target tgt will depend on the target 'anothertgt'. 

The problem is that this fact (apparently) forces you to order your calls to `Alias()` and `Depends()` based on the dependency order. Not a good thing. 

The solution is to not use a naked string in the Depends, if you expect it to be an Alias: 
```python
tgt = env.Command(...)
env.Depends(tgt, env.Alias('SomeAlias'))

anothertgt = env.Command(...)
env.Alias('SomeAlias', anothertgt)
```
As Anthony Roach (who proposed the solution) says: 

"That tells SCons that `SomeAlias` is an alias, even if the alias definition hasn't been seen yet." 

Perfect! 

Now there's a twist to this if you happen to use env.Clone(). For example, if you have an sconscript that looks like this: 
```python
Import('env')
localenv = env.Clone()
tgt = localenv.Command(...)
localenv.Depends(tgt, localenv.Alias('SomeAlias'))
```
you might get a warning that `'SomeAlias'` is defined in two environments. In this case, in the current local copy and in the environment where `'SomeAlias'` is previously (or in future) defined. In my system, I got around this by putting all the aliases in one environment, like so: 
```python
Import('env')
localenv = env.Clone()
tgt = localenv.Command(...)
localenv.Depends(tgt, env.Alias('utx'))
localenv.Depends(tgt, env.Alias('SimpleXml'))
```

This value node has a string argument which substitutes values from the environment. This is usefull for:

* Generating small initialization files
* Ensuring that builders which are python function gets the correct dependencies if the function uses environment values.

```python
import SCons.Node.Python

class EnvValue(SCons.Node.Python.Value):
    """Node class which substitutes variables from the environment"""
    def __init__(self,env,value):
        """Initialiser takes an Environment and a string to be expanded."""
        SCons.Node.Python.Value.__init__(self,value)
        self.env=env
    def __str__(self):
        return env.subst(self.value)
```
Now you can do something like this:


```python
env.Command('target',EnvValue(env,'$MYVAR'),'echo $SOURCE > $TARGET')
env['MYVAR']='SomeValue'
```
There is one scenario in which the results might not be as expected. This is when the builder creates an override environment. In this case the environment used for the value node is not the same as that used for the builder:


```python
env['MYVAR']='DefaultValue'
env.Command('target',EnvValue(env,'$MYVAR'),'echo $SOURCE > $TARGET',MYVAR='SomeValue')
```
In this example the command becomes


```console
echo DefaultValue
```

For a builder which is a python function which references environment values, you might want to have add an emitter function which adds a EnvValue as a dependency (I have not tried that yet).

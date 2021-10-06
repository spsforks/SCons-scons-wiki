
The `$STRING` expansion in actions makes some assumptions: 

* if the expanded variable is a list of strings, each of them is a single argument to the final command. 
* if the expanded variable is a single string, it is a space-separated list of arguments to the final command. 

If you want to force a single string variable to be treated as a single argument, you can do this: 

```python
action = "compiler.exe ${[MYVAR]}" 
```

The curly braces cause `[MYVAR]` to be evaluated as a Python expression. `[MYVAR]` is a list containing the single string `MYVAR`. So your end result is that `MYVAR` will be quoted as a single arg if it happens to contain spaces. 

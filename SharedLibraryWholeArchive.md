Scons does not currently have support for -Wl,--whole-archive.  However, there is a simple workaround that can be used.  Add the following to your scons file:

```
#!python

whole_archive = env.Command('-Wl,--whole-archive', [], '')
no_whole_archive = env.Command('-Wl,--no-whole-archive', [], '')
```

Now you can wrap the necessary libraries with whole-archive/no-whole-archive in any combination. Example:
```
#!python

so_libs = env.SharedLibrary('myso', whole_archive+['libfoo1.a']+no_whole_archive+['libbar.a']+whole_archive+['libfoo2.a']+no_whole_archive)
```

This technique can be used for any option where the order/position of the option relative to input files matter.
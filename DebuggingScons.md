

# Tips for debugging SCons code and your scripts


## To use local scons source rather than installed:

Put these lines in a shell script and run the script.  If you want to run it regularly, make the script executable and put it in your private bin directory. 


```python
#!python 
SCONS_LIB_DIR=/path_to_scons/src/engine
export SCONS_LIB_DIR
exec python /path_to_scons/src/script/scons.py .
```
You can also run from a checked-out SCons source dir using bootstrap.py, which takes the same args as SCons.  That should always use the SCons engine from where bootstrap.py is found. 
```python
#!python 
python /path_to_scons_src/bootstrap.py .
```
If you run the commands by hand, don't include the "exec" in the final line. 


## To run under debugger:


```python
#!python 
scons --debug=pdb <args...>
b SCons/Tool/msvc.py:158 # to stop at that file:line, looks for file in sys.path e.g. your SCONS_LIB_DIR
```

## Debugging in Eclipse/PyDev

Laurent Marchelli: 

I use Eclipse [PyDev](PyDev) visual debugger instead than pbd, it works to dig into scons and for debugging my SConscript even on my bitbucket fork ([PyDev](PyDev) environment : SCONS_LIB_DIR=C:\dev\scons\scons-morpheus\src\engine). 

For debugging test scripts (runtest.py), this solution has to get extended somewhat: 

Because runtest.py launch another process to execute the test, the pydev debugger is not enough, the pydev remote debugger must be used. 

Solution in 5 steps: 

1. Into your debug configuration's environment variables, add the PYTHONPATH to the pydevd.py script.(Pydev Remote debugger) 
1. Add following line at the top of your test script (e.g. msvsTests.py) 
         * `import pydevd; pydevd.settrace()` 
1. Launch [PyDev](PyDev) Debug Server. 
1. Launch the debugger on runtest.py, the remote debugger will handle the break into your test script. 
1. Enjoy `;-)` 
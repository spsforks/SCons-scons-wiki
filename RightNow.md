
Sometimes you wish that SCons could build a file right after you create its node in the SConscript, before you've finished processing the rest of the SConscript.  Maybe the output of that file will determine what other targets you need to build, or what options you build them with.  [DynamicSourceGenerator](DynamicSourceGenerator) and [BuildTimeCallback](BuildTimeCallback) may be able to solve your particular problem, but maybe not.  Even if they can, they may be too awkward to use.  RightNow fills that gap.  When you tell SCons to build a target RightNow, it builds it (if it's out of date), Right Now. 

RightNow is a function that takes any list of nodes (such as the return value from a Builder) as its sole argument and builds them all if any are out of date.  You can find the code at [https://code.edge.launchpad.net/~asomers/sconsaddons/rightnow](https://code.edge.launchpad.net/~asomers/sconsaddons/rightnow) (for a full list of external SCons Tools check out the [ToolsIndex](ToolsIndex)).  An example SConstruct is below.  In the example, in should contain the name of the file that you wish for your final output. 


```python
env = DefaultEnvironment(tools=["default", "rightnow"])
x = Command(["intermediate"], ["in"], """cat $SOURCE > $TARGET""")
env.RightNow(x)

try:
    with open("intermediate", "r") as f:
        outname = f.read().rstrip("\n")
    Command([outname], ["intermediate"], """cat $SOURCE > $TARGET""")
except IOError:
    # Intermediate file must not yet exist
    pass
```

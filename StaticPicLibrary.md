
This builder is exactly like the [StaticLibrary](StaticLibrary) builder, but uses position independant code (pic). It is useful when the library is meant to be statically linked to a shared library. 


```txt
def createStaticPicLibraryBuilder(env):
    """This is a utility function that creates the StaticExtLibrary Builder in
    an Environment if it is not there already.

    If it is already there, we return the existing one."""
    import SCons.Action

    try:
        static_extlib = env['BUILDERS']['StaticPicLibrary']
    except KeyError:
        action_list = [ SCons.Action.Action("$ARCOM", "$ARCOMSTR") ]
        if env.Detect('ranlib'):
            ranlib_action = SCons.Action.Action("$RANLIBCOM", "$RANLIBCOMSTR")
            action_list.append(ranlib_action)

    static_extlib = SCons.Builder.Builder(action = action_list,
                                          emitter = '$LIBEMITTER',
                                          prefix = '$LIBPREFIX',
                                          suffix = '$LIBSUFFIX',
                                          src_suffix = '$OBJSUFFIX',
                                          src_builder = 'SharedObject')

    env['BUILDERS']['StaticPicLibrary'] = static_extlib
    return static_extlib
```
You then just have to call the function createStaticPicLibrary(env), and then call the StaticPicLibrary builder, which has exactly the same semantics as the [StaticLibrary](StaticLibrary) one. The only difference with [StaticLibrary](StaticLibrary) is the src_builder: instead of calling [StaticObject](StaticObject), it uses [SharedObject](SharedObject). 

Note that since scons uses a different suffix for pic object code and non pic object code, it may confuse some tools which expects .o in static libraries. 

Question (thank you in advance [AdrianNeagu](AdrianNeagu)): 

* I see how this works when the builder is given a set of *.c files as sources. But how does it check the input when  I provide compiled object Scons nodes? How does it check that I provided only [SharedObject](SharedObject)() nodes and no [StaticObject](StaticObject)() node in the list of input nodes? 
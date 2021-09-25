
Line 5: Set your environment!  Lots of people get burned by the fact that SCons erases most of the environment variables. 

Line 12: A very basic Builder.  Note that single_source is set to True.  This means that a set of sources [ "foo1.scm", "foo2.scm", "foo3.scm" ] will get converted to [ "foo1.c", "foo2.c", "foo3.c" ] rather than all being piled into [ "foo1.c" ]. 

Line 15: Add the new builder to the Environment for later use 

Line 19: A fairly basic Emitter.  This was used because of the previously mentioned issue that I wanted a suffix of "_.c" and the suffixes are tied to being only after a ".".  Also, the default for when single_source is False is to take the first mentioned source and convert it into the target.  This is different from the  default behavior of gsc which uses the last source file.  Since I wanted to emulate that as well, I created a custom emitter. 

Line 32: Another simple Builder.  This time single_source is set to False.  This means that all of the sources get compiled into a single file.  In this instance, that is what we want. 

Line 36: Add the new builder to the Environment for later use 

Line 43: Note that I make a Copy() (soon to be Clone()) of environments so that I can mangle them later. 

Line 44: This is a basic override of the default C compilation flags.  I'm a bit verbose here because I am going to do cross-compiling later. 

Line 48: Call the SConscript which will build the main library.  Interesting things to note here: 

* You have to explicitly export an environment in order to use it in the subsidiary SConscript.  This does catch people. 
* I am explicitly returning a reference to the library itself which I will use later.  This is in keeping with the whole idea of avoiding strings for referencing targets. 
Line 60: Call the SConscript which will build the main interpreter.  Note that I am passing in both "env" and "libgambc" references.  Those will show up again in the subsidiary SConscript files. 

Line 65: Call the SConscript which will build the main compiler.  Note that I am passing in both "env" and "libgambc" references.  Those will show up again in the subsidiary SConscript files. 


```python
#!python
# -*-python-*-

import SCons

rootEnv = Environment(BUILDROOT="build",
                      ENV = {"PATH": ["/bin", "/usr/bin",
                                      "/opt/bin", "/usr/local/bin", "/sw/bin"]})


# Add the Gambit compiler builder to the main Environment
# FIXME: Should probably find some way to make /home/gambit/4.0b20 a variable
gambitCompilerBuilder = Builder(action = '/home/gambit/4.0b20/bin/gsc -:="/home/gambit/4.0b20" -f -o $TARGET -c -check $SOURCE',
                                suffix = ".c", src_suffix = ".scm",
                                single_source=True)
rootEnv.Append(BUILDERS = {"GambitCompiler" : gambitCompilerBuilder})


# Add the Gambit library builder to the main Environment
def gambitLinkerEmitter(target, source, env):
    # target and source are always lists--makes keywords more descriptive
    # for the next time I actually touch the SConstruct
    (targets, sources) = (target, source)

    # Grab the last source file the way a gsc without -o would
    # ARGGGGHHH!  Is this really the only way to get the base name?
    baseName = SCons.Util.splitext(str(sources[-1].name))[0]

    targets = [SCons.Util.adjustixes(baseName, None, "_.c")]

    return (targets, sources)

gambitLinkerBuilder = Builder(action = '/home/gambit/4.0b20/bin/gsc -:="/home/gambit/4.0b20" -f -link -o $TARGET $SOURCES',
                              emitter=gambitLinkerEmitter,
                              src_suffix = ".scm",
                              single_source=False)
rootEnv.Append(BUILDERS = {"GambitLinker" : gambitLinkerBuilder})



# Compile the main Gambit library
gambitLibCCFLAGS = '-no-cpp-precomp -Wall -W -Wno-unused -O1 -fno-math-errno -fschedule-insns2 -fno-trapping-math -fno-strict-aliasing -fwrapv -fexpensive-optimizations -fforce-addr -fpeephole2 -falign-jumps -falign-functions -fno-function-cse -ftree-copyrename -ftree-fre -ftree-dce -fregmove -fgcse-las -freorder-functions -fcaller-saves -fno-if-conversion2 -foptimize-sibling-calls -fcse-skip-blocks -funit-at-a-time -finline-functions -fomit-frame-pointer -fPIC -fno-common -mieee-fp -DHAVE_CONFIG_H -D___PRIMAL -D___LIBRARY -D___GAMBCDIR=\\\"/home/gambit/4.0b20\\\"'

libEnv = rootEnv.Copy()
libEnv.Replace(CCFLAGS=gambitLibCCFLAGS)

env = libEnv
Export("env")
libgambc = libEnv.SConscript("lib/SConscript", build_dir="$BUILDROOT/lib", exports="env")


# Compile the Gambit gsi and gsc executables
gambitExecutableCCFLAGS = '-no-cpp-precomp -Wall -W -Wno-unused -O1 -fno-math-errno -fschedule-insns2 -fno-trapping-math -fno-strict-aliasing -fwrapv -fexpensive-optimizations -fforce-addr -fpeephole2 -falign-jumps -falign-functions -fno-function-cse -ftree-copyrename -ftree-fre -ftree-dce -fregmove -fgcse-las -freorder-functions -fcaller-saves -fno-if-conversion2 -foptimize-sibling-calls -fcse-skip-blocks -funit-at-a-time -finline-functions -fomit-frame-pointer -fPIC -fno-common -mieee-fp -DHAVE_CONFIG_H'

gsiCCFLAGS = gambitExecutableCCFLAGS
gsiEnv = rootEnv.Copy()
gsiEnv.Replace(CCFLAGS=gsiCCFLAGS)

env = gsiEnv
Export("env")
gsi = env.SConscript("gsi/SConscript", variant_dir="$BUILDROOT/gsi", exports=["env", "libgambc"])

# Compile the Gambit gsc executable
env = gsiEnv
Export("env")
gsc = env.SConscript("gsc/SConscript", variant_dir="$BUILDROOT/gsc", exports=["env", "libgambc"])

```

SCons treats dependencies on shared libraries that are generated in a simplistic manner, if the library is rebuilt, any programs that link against it are also rebuilt. 

Most of the time it is not necessary to rebuild the programs, as changes are usually to the implementation of the source not interface changes.  In the case of a shared library it is relatively easy to figure out if the change needs a relink by generating a signature based on the actual external symbols published and required by the library.  This is in addition to the dependencies on the headers, which scons already determines automatically. 

The following builder is a way of achieving this by separating changes to the implemention from changes to the interface.  It uses a bunch of files to do this.  There are probably better ways to achieve the same end, ideally scons would allow a custom signature technique to the plugged in for a node, typically by the builder. 

The builder uses 2 common output directories for the libraries, #lib gets the latest builds of the shared libraries installed into it.  The libraries in `#linklib` directory gets updated only when the interface changes.  All programs get linked against the `#linklib` directrory.  The developer sets their `LD_LIBRARY_PATH` to the libraries in `#lib` when testing. 

The builder sets up an indirect dependency between the library in each version, and uses a nm command extract the global symbols from the updated library, and stored this in a file that is used as the interface signature of the library. 

Note it is also overriding the standard `SharedLibrary()` builder within the `env` environment. However I am not convinced this is the best way to do this. 


```python
####################################################
# override SharedLibrary to only update the libs in '#shlib/' if the symbols
# change.  This is to avoid rebuilding binaries when a shared library has
# changes.
# This would be MUCH simpler to implement if we could override the
# signature to used for the SharedLibrary node itself directly. That is
# certainly possible, but would rely on the internal structure of SCons.


def fasterSharedLibrary(env, library, sources, **args):
    # use the 'quicker' shallow copy method!
    envContentSig = env.Clone()
    envContentSig.TargetSignatures("content")

    cat = env.OriginalSharedLibrary(library, sources)

    # copy all the latest libraries to ONE directory..
    # for our convenience. Could modify the above to
    # build directly to this dir instead.
    catLib = env.Install("#lib", cat)  # the CURRENT lib dir

    # now generate the 'interface' file, using the
    # content signature for its target
    catIF = envContentSig.Command(
        "%s.if" % (library),
        catLib,
        "nm --extern-only $SOURCES | cut -c 12- | sort &gt; $TARGET",
    )

    # install command to copy lib to shlib, where the link
    # actually occurs.  Explicitly make this depend only on
    # the IF file, which has a target content signature.
    # ie only if the Global Symbol list changes, is copied and this the
    # Programs it relinked.
    catLink = env.Command(
        "#linklib/${SHLIBPREFIX}%s${SHLIBSUFFIX}" % (library),
        "",
        Copy("$TARGET", catLib),
    )

    # Dir('#lib')
    envContentSig.Depends(catLink, catIF)

    global libs
    libs += catLib

    return cat


# declaring OriginalSharedLibrary is a bit marginal.  Probably should use
# a functor style object so we can store it in side the object?
env["BUILDERS"]["OriginalSharedLibrary"] = env["BUILDERS"]["SharedLibrary"]
env["BUILDERS"]["SharedLibrary"] = fasterSharedLibrary
```


Using Microsoft Visual C++ with SCons is hard. We struggled for a long time to get decent build speed in a "debug" configuration. 

It turns out that incremental linking is the only way to get fast "debug" builds. However, we found problems at every step along the way to get this feature working within SCons. 

The easiest and most elegant way we could find to make this the default behavior was to replace the `Program` and `SharedLibrary` builders with custom ones that do extra steps. 

Here's what we did: 


```python
#!python
envDebug = "... your global environment ...".Clone()

# Link with debugging informations
envDebug.AppendUnique(LINKFLAGS=["/DEBUG"])

# Dynamically link with the debugging CRT
envDebug.AppendUnique(CCFLAGS=["/MDd"])

# Disable optimizations
envDebug.AppendUnique(CCFLAGS=["/Od"])

# Produce one .PDB file per .OBJ when compiling, then merge them when linking.
# Doing this enables parallel builds to work properly (the -j parameter).
# See: http://www.scons.org/doc/HTML/scons-man.html section CCPDBFLAGS
envDebug["CCPDBFLAGS"] = "/Zi /Fd${TARGET}.pdb"
envDebug["PDB"] = "${TARGET.base}.pdb"

# Link incrementally. Produces larger (and possibly corrupted files,
# but takes less time to build. Not recommended for final build.
envDebug.AppendUnique(LINKFLAGS=["/INCREMENTAL"])

# Hacks to allow incremental linking on Microsoft Visual C++.
#
# 1 - Don't generate a .manifest file, we're doing that below
envDebug.AppendUnique(LINKFLAGS=["/MANIFEST:NO"])

# 2 - Override the SharedLibrary builder to add some extra steps
def SharedLibraryIncrementallyLinked(env, library, sources, **args):
    # Hack 1: Embed a manifest while linking
    #
    # Since we can't embed the .manifest file *AFTER* linking, because it
    # would modify the binary and prevent subsequent incremental linking,
    # we must embed it *WHILE* linking. We achieve that by generating a
    # manifest file from a dummy program created with the current
    # environment. This manifest file is then added to a resource, which
    # is compiled into an object file and linked into the final binary.
    subBuild = env.Clone()
    subBuild["WINDOWS_INSERT_MANIFEST"] = True
    subBuild.AppendUnique(LINKFLAGS="/MANIFEST")
    subBuild.AppendUnique(LINKFLAGS="/INCREMENTAL:NO")
    if "/MANIFEST:NO" in subBuild["LINKFLAGS"]:
        subBuild["LINKFLAGS"].remove("/MANIFEST:NO")
    if "/INCREMENTAL" in subBuild["LINKFLAGS"]:
        subBuild["LINKFLAGS"].remove("/INCREMENTAL")
    if "/DEBUG" in subBuild["LINKFLAGS"]:
        subBuild["LINKFLAGS"].remove("/DEBUG")
    del subBuild["PDB"]

    def createDummySourceFile(env, target, source):
        file(target[0].abspath, "w").write("int main(int, char **) { return 0; }\n")

    dummyName = library[0] + "_dummy_for_manifest"
    dummySourceFile = subBuild.Command(dummyName + ".cpp", None, createDummySourceFile)
    dummyProgram = subBuild.ProgramOriginal(dummyName + ".exe", dummySourceFile)
    dummyManifest = dummyProgram[1]

    def createManifestResourceFile(env, target, source):
        file(target[0].abspath, "w").write(
            '2 24 "%s"' % source[0].abspath.replace("\\", "\\\\")
        )

    manifestResourceFile = subBuild.Command(
        dummyName + ".rc", dummyManifest, createManifestResourceFile
    )
    manifestResource = subBuild.RES(dummyName + ".res", manifestResourceFile)
    
    # Hack 2: Precious binary
    #
    # By default, SCons will delete the files before re-building them.
    # This prevents incremental linking from working because it relies
    # on timestamps. Therefore, we must prevent SCons from deleting the
    # the build products. This is achieved by making them as "Precious".
    library = env.SharedLibraryOriginal(library, [sources, manifestResource], **args)
    env.Precious(library)
    return library


envDebug["BUILDERS"]["SharedLibraryOriginal"] = envDebug["BUILDERS"]["SharedLibrary"]
envDebug["BUILDERS"]["SharedLibrary"] = SharedLibraryIncrementallyLinked

# 3 - Override the Program builder to add some extra steps
def ProgramIncrementallyLinked(env, program, sources, **args):
    # Hack 1: Embed a manifest while linking
    #
    # Since we can't embed the .manifest file *AFTER* linking, because it
    # would modify the binary and prevent subsequent incremental linking,
    # we must embed it *WHILE* linking. We achieve that by generating a
    # manifest file from a dummy program created with the current
    # environment. This manifest file is then added to a resource, which
    # is compiled into an object file and linked into the final binary.
    subBuild = env.Clone()
    subBuild["WINDOWS_INSERT_MANIFEST"] = True
    subBuild.AppendUnique(LINKFLAGS="/MANIFEST")
    subBuild.AppendUnique(LINKFLAGS="/INCREMENTAL:NO")
    if "/MANIFEST:NO" in subBuild["LINKFLAGS"]:
        subBuild["LINKFLAGS"].remove("/MANIFEST:NO")
    if "/INCREMENTAL" in subBuild["LINKFLAGS"]:
        subBuild["LINKFLAGS"].remove("/INCREMENTAL")
    if "/DEBUG" in subBuild["LINKFLAGS"]:
        subBuild["LINKFLAGS"].remove("/DEBUG")
    del subBuild["CCPDBFLAGS"]
    del subBuild["PDB"]

    def createDummySourceFile(env, target, source):
        file(target[0].abspath, "w").write("int main(int, char **) { return 0; }\n")

    dummyName = program[0] + "_dummy_for_manifest"
    dummySourceFile = subBuild.Command(dummyName + ".cpp", None, createDummySourceFile)
    dummyProgram = subBuild.ProgramOriginal(dummyName + ".exe", dummySourceFile)
    dummyManifest = dummyProgram[1]

    def createManifestResourceFile(env, target, source):
        file(target[0].abspath, "w").write(
            '1 24 "%s"' % source[0].abspath.replace("\\", "\\\\")
        )

    manifestResourceFile = subBuild.Command(
        dummyName + ".rc", dummyManifest, createManifestResourceFile
    )
    manifestResource = subBuild.RES(dummyName + ".res", manifestResourceFile)
    
    # Hack 2: Precious binary
    #
    # By default, SCons will delete the files before re-building them.
    # This prevents incremental linking from working because it relies
    # on timestamps. Therefore, we must prevent SCons from deleting the
    # the build products. This is achieved by making them as "Precious".
    program = env.ProgramOriginal(program, [sources, manifestResource], **args)
    env.Precious(program)
    return program


envDebug["BUILDERS"]["ProgramOriginal"] = envDebug["BUILDERS"]["Program"]
envDebug["BUILDERS"]["Program"] = ProgramIncrementallyLinked
```
Then you use the builders as usual and you'll get incremental linking: 
```python
#!python 
env = envDebug
env.Program("MyProgram", "MyProgram.cpp")
env.SharedLibrary("MyLibrary", "MyLibrary.cpp")
```

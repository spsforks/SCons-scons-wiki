
Line 3: Imports the env from the parent script 

Line 5&7: Sets up the C compiler to look in both the current directory and the include directory **underneath the main directory in which SCons was started**.  Note the "#" in the "#include".  This is important.  That include directory contains a "config.h" file that almost all the C code references and it is **not** copied over to the build/etc/etc hierarchy. 

Line 9: Gambit Scheme input files (sources) 

Line 12: C input files (more sources) 

Line 15: Converts the Gambit Scheme input files into C output files (targets) via the [GambitCompiler](GambitCompiler) Builder defined in the top-level SConstruct.  ie.  _io.scm becomes _io.c.  Note that I am saving the targets here for later reference. 

Line 17&19: Add dependencies to the targets since I can't add them to the sources.  These dependencies are actually included by the ".scm" files, but I can't reference those.  Also, note that I am using the reference to the targets that I stored (gambitTargetFiles) rather than explicitly trying to name the ".c" files (ie. "_io.c") 

Line 23: Use the normal SCons [StaticLibrary](StaticLibrary) builder to convert all the ".c" files into a static library.  Note that this will generate a bunch of ".o" files first.  Store the SCons reference to this library. 

Line 24: Return the reference to the newly built library so that I don't have to hunt for it using a filename 


```python
#!python
# -*-python-*-

Import(["env"])

cpppath = [".", "#include"]

env.Replace(CPPPATH=cpppath)

gambitSourceFiles = ["_io.scm", "_num.scm", "_std.scm", "_kernel.scm", "_nonstd.scm", "_repl.scm",
                     "_eval.scm", "_thread.scm", "_system.scm"]

cSourceFiles = ["main.c", "os_tty.c", "c_intf.c", "os_io.c", "setup.c", "mem.c", "os_files.c", "os.c",
                "os_base.c", "os_time.c", "os_shell.c", "os_dyn.c", "_gambc.c"]

gambitTargetFiles = env.GambitCompiler(gambitSourceFiles)

env.Depends(gambitTargetFiles, ["header.scm"])
#FIXME: Really need a scanner for this.  With Scheme, this should be pathetically easy to make
env.Depends(gambitTargetFiles, ["_kernel#.scm", "_thread#.scm", "_system#.scm", "_num#.scm", "_io#.scm",
                                "_eval#.scm", "_repl#.scm", "_std#.scm", "_nonstd#.scm"])


libgambc = env.StaticLibrary("gambc", [gambitTargetFiles, cSourceFiles])
Return("libgambc")
```
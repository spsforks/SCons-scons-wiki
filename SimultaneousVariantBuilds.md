
This page demonstrates how to tell SCons to build multiple variants of your software all at the same time, for example: 

* debug and release versions 
* host and target versions 

`SConstruct`: 
```python
release_env = Environment(CCFLAGS=["-O2"])
debug_env = release_env.Clone(CCFLAGS=["-g"])

SConscript("src/SConscript", variant_dir="release", exports={"env": release_env})
SConscript("src/SConscript", variant_dir="debug", exports={"env": debug_env})
```
`src/SConscript`: 
```python
Import('env')
env.Program('hello', ['hello.c'])
```
Output: 
```bash
$ scons
gcc -g -c -o debug/hello.o debug/hello.c
gcc -o debug/hello debug/hello.o
gcc -O2 -c -o release/hello.o release/hello.c
gcc -o release/hello release/hello.o
```
Here's the same sort of thing for windows using the Microsoft C++ compiler.  In the `SConstruct`: 
```python
base_env = Environment(tools=["msvc", "mslink"])

# Build different variants:
for flavour in ["Debug", "Release"]:
    env = base_env.Clone()

    # Set up compiler and linker flags:
    if flavour == "Debug":
        # Use debug multithreaded DLL runtime, and no optimization
        env.Append(CCFLAGS=["/MDd", "/Od"])
        # Each object has its own pdb, so -jN works
        env.Append(CCFLAGS=["/Zi", "/Fd${TARGET}.pdb"])
        env.Append(LINKFLAGS=["/DEBUG"])
    else:
        # Use multithreaded DLL runtime, and some sensible amount of optimization
        env.Append(CCFLAGS=["/MD", "/Ox"])

    # Call the SConstruct for each subproject.
    SConscript(
        "hello/SConscript",
        exports=["env"],
        variant_dir=flavour + "/hello",
        duplicate=0,
    )
    SConscript(
        "world/SConscript",
        exports=["env"],
        variant_dir=flavour + "/world",
        duplicate=0,
    )
```
And this is the contents of `hello/SConscript`: 
```python
# Make sure we don't change the imported environment by mistake:
Import("env")
imported_env = env
env = env.Clone()

# Set up things for this project
env.AppendUnique(CPPPATH=["."])

hello_t = env.Program(
    target="hello",
    source=["hello.c"],
)
```
And the output: 
```txt
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
cl /nologo /MDd /Od /Zi /FdDebug\hello\hello.obj.pdb /IDebug\hello /Ihello /c hello\hello.c /FoDebug\hello\hello.obj hello.c
link /nologo /DEBUG /OUT:Debug\hello\hello.exe Debug\hello\hello.obj
cl /nologo /MD /Ox /IRelease\hello /Ihello /c hello\hello.c /FoRelease\hello\hello.obj hello.c
link /nologo /OUT:Release\hello\hello.exe Release\hello\hello.obj
...
scons: done building targets.
```
Thanks to Werner Schiendl for posting this solution to the mailing list. 

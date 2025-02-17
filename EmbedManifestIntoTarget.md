
# How To Embed Manifest Into Target

Here I do a fast explanation how to embed your manifest file into your target using the Microsoft Manifest Tool. 

To use this tip, you must to create your environment as usual, but at the final, you must to add a line. 

```python
# Create your environment as usual.
env = Environment()

# Here I'm building a Shared Library, but you can use this tip for all build types.
env.SharedLibrary(
    target='library_name',
    source=['mysource.cpp'],

    # If you must embed the manifest file into your target, use the line below.
    # The number at the end of the line indicates the file type (1: EXE; 2:DLL).
    LINKCOM  = [env['LINKCOM'], 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;2']
)
```

That's it. Enjoy! 


# Another Way to Embed a Manifest File

You can also run the Microsoft Manifest Tool (mt.exe) as a post-build step. I have found this to be more reliable than adjusting LINKCOM as the method above does.

```python
# Create your environment as usual.
env = Environment()

# Here I'm building a Shared Library, but you can use this tip for all build types.
buildResult = env.SharedLibrary(target='library_name', source=['mysource.cpp'])

# Add a post-build step to embed the manifest using mt.exe
# The number at the end of the line indicates the file type (1: EXE; 2:DLL).
env.AddPostAction(buildResult, 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;2')
```

# Yet Another Way to Embed a Manifest File

Here's a two-liner that sets up the correct link environment to automatically embed manifest files, for both executables and shared libraries: 

```python
# Create your environment as usual.
env = Environment()

env['LINKCOM'] = [env['LINKCOM'], 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;1']
env['SHLINKCOM'] = [env['SHLINKCOM'], 'mt.exe -nologo -manifest ${TARGET}.manifest -outputresource:$TARGET;2']
```

# How to Embed a Manifest File Using MinGW

If you don't want to use the Microsoft compiler and tools, using MinGW one needs to do the following: 

1. Create a .manifest file 
1. Create a simple .rc file that refers to that manifest file 
1. Compile the .rc file into an object using MinGW's windres command 
1. Add the object to the LINKFLAGS 

## Creating the Manifest File

In this example, I will embed a manifest file for linking against the Microsoft VC Runtime library.  Python 2.6 installs one for us on the system and includes a package called **msvcrt**.  Below, ask Python for the specific name, version, and key.  Then write it out to a file: 

```python
import sys

# Defaults
name    = "Microsoft.VC90"
version = "9.0.21022.8"
key     = "1fc8b3b9a1e18e3b"

try:
    import msvcrt

    name    = msvcrt.LIBRARIES_ASSEMBLY_NAME_PREFIX
    version = msvcrt.CRT_ASSEMBLY_VERSION
    key     = msvcrt.VC_ASSEMBLY_PUBLICKEYTOKEN

except:
    pass

template = '''\
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="false"></requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity type="win32" name="%s.CRT" version="%s" processorArchitecture="*" publicKeyToken="%s"></assemblyIdentity>
    </dependentAssembly>
  </dependency>
</assembly>''' %(name, version, key)

# Write it out to a file.
fout = open("msvcrt.manifest", "w")
fout.write(template)
fout.close()
```

## Creating the .rc File

Create an .rc file with the following text for embedding into an executable: 

```python
with open("msvcr.rc", "w") as fout:
    fout.write("""
#include "winuser.h"
1 RT_MANIFEST  msvcrt.manifest
""")
```
The "**1**" above indicates this manifest to be embedded into an executable, change it to "**2**" for use with a .DLL. 


## Compile the .rc File Using the windres Command

On the command line one would do: 

```bash
$ windres --input msvcr.rc --output msvcrc.o
```
From Python, open a subprocess: 

```python
try:
    out = subprocess.Popen(["windres", "--input", "msvcr.rc", "--output", "msvcr.o"],
        stdout = subprocess.PIPE).communicate()
except:
    sys.stderr.write("could not execute 'windres', is mingw installed?\n")
```

## Add The Compiled Manifest To LINKFLAGS

Having separate environments for compiling executables and libraries makes it easy to embed different manifest objects: 

```python
exe_env.Append(LINKFLAGS = " %s " % exe_manifest_obj_filename)
lib_env.Append(LINKFLAGS = " %s " % lib_manifest_obj_filename)
```

## Use Scons Config Tests

If one were to simple copy and paste the Python code above into their SConscript, the code would execute every time scons is called.  Instead, add the code to a custom Scons check context function.  This way, the manifest objects are only built when necessary. 


---

[SohailSomani](SohailSomani) - Why is the second way more reliable? 

[AtulVarma](AtulVarma) - I'm not sure why the second way is more reliable, but it's certainly more readable and architecturally sound, IMO.  The first solution uses a somewhat obscure environment variable in non-obvious way--it's a solution that reminds me of GNU make and everything that makes Makefiles difficult to understand--whereas the latter uses a more universal and understandable object-oriented mechanism to accomplish the same thing.  The latter is also more universally applicable (perhaps this is why its originator called it more "reliable") because it can be used on any kind of target, not just one that was generated by a C/C++ compiler. 

[GaryOberbrunner](GaryOberbrunner) - I actually like the first way better.  It makes it automatic so you don't have to call [AddPostAction](AddPostAction) on every executable or library (for libs, use SHLINKCOM).  I don't find LINKCOM/SHLINKCOM to be obscure at all; they're well-documented as the command (or commands) to use to link an exe or lib.  Running mt as part of the link step seems to me to be quite natural.  Oh yes; if you want to do this for all exes/libs (which seems likely), just put the modification to LINKCOM/SHLINKCOM into the environment.  Then you don't have to touch your [SharedLibrary](SharedLibrary) or Program calls, they remain nicely cross-platform. 

[Kameleon](Kameleon) - I added a third method that is derived from [GaryOberbrunner](GaryOberbrunner)'s suggestion just above. I'm wondering if the first method is buggy: it is building a shared library, but sets the LINKCOM variable. Shouldn't it be setting SHLINKCOM??? 


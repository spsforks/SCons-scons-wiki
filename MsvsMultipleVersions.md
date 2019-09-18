# Selecting MSVC version

By default, SCons' MSVC tool uses the highest installed version of the Microsoft Visual C++ compiler.  To change this, you must change the `MSVC_VERSION` construction variable. You can certainly just set the value in your SConscript, but it is often interesting to be able to specify the version you want on the command line without editing the scripts, such as when you want to perform verification builds against several different compiler versions. The following examples show a few different approaches. The manpage for the scons version you are using (see https://scons.org/docversions.html) shows the currently valid Visual C++ versions.

``` python
# This creates an environment which will use the 14.0 compiler even if higher
# versions are installed on the machine.
env60 = Environment(MSVC_VERSION='14.0')

# This uses the value of an environment variable for the compiler version.
# invoke as:   MSVC_VERSION=14.0 scons   (on linux/mac)
import os
msvc_version = os.environ.get('MSVC_VERSION', '14.2')
env = Environment(MSVC_VERSION=msvc_version)

# This recognizes a command-line setting without specifically defining an option.
# invoke as:  scons MSVC_VERSION=14.0
msvc_version = ARGUMENTS.get('MSVC_VERSION', '14.2')
env = Environment(MSVC_VERSION=msvc_version)

# This creates an option the developer can use to select between v14.0, v14.1 and
# v14.2.  If no option is specified, the default value is used.
# invoke as:  scons MSVC_VERSION=14.0
vars = Variables()
vars.AddVariable(EnumVariable('MSVC_VERSION',
                              'MS Visual C++ version',
                              default='14.2',
                              allowed_values=('14.0', '14.1', '14.2')))
env = Environment(variables=vars)
```

---
> Note: the following is old, `Options` objects have been replaced by `Variables`, and `MSVS_VERSION` is deprecated in favor of `MSVC_VERSION`. 

 This worked for me:

``` python
opts = Options("SConsOptions")

opts.AddOptions(
    EnumOption("TOOL", "The tool chain to use", defaultTool, ("vc6", "vc8", "gnu"))
    )

env = Environment(options = opts)
Help(opts.GenerateHelpText(env))

if env["TOOL"] == "vc6":
    env["MSVS"] = {"VERSION": "6.0"}
    env["MSVS_VERSION"] = "6.0"
    Tool("msvc")(env)
elif env["TOOL"] == "vc8":
    env["MSVS"] = {"VERSION": "8.0"} 
    env["MSVS_VERSION"] = "8.0"
    Tool("msvc")(env)
elif env["TOOL"] == "gnu":
    Tool("g++")(env)
```
-- [IlguizLatypov](IlguizLatypov) 

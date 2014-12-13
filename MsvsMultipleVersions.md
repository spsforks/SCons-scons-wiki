

# Selecting MSVS version

By default, Scons' MSVS tool uses the highest installed version of MSVS for the compiler.  To change this, you must change the MSVS_VERSION construction variable. 


```txt
  # This creates an environment which will use the 6.0 compiler even if higher
  # versions are installed on the machine.
  env60 = Environment(MSVS_VERSION = '6.0')

  # This creates an option the developer can use to select between v6.0 and
  # v7.1.  If no option is specified, the environment will revert to the regular
  # behavior (highest installed version).
  opts = Options()
  opts.Add(EnumOption('MSVS_VERSION', 'MS Visual C++ version', None,
    allowed_values=('6.0', '7.1)))
  envOption = Environment(options = opts)
```


---

 This worked for me: 
```txt
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

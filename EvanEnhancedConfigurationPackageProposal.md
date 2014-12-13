

# Prelimaries

First, this page is posted for feedback, so feel free to edit. However, so it's easy to spot edits, I suggest treating this page like a talk page at Wikipedia or whatever, and indent and sign responses. 

Throughout, the term _builder_ will refer to the person building the software (the one typing `scons`), and _developer_ to the person writing the `SConstruct`/`SConscript` files. (Obviously the developer will often be playing the role of the builder.) 

The term _compiler model_ will refer to how SCons figures out the compiler flags that it treats in a tool-independent manner (from the developer's point of view), e.g. how it combines the `CPPPATH`s or `LIBS` into compiler/linker flags. I call these flags _abstract flags_; one goal of this project is to increase the number of supported abstract flags (e.g. for debugging, optimization, and warning). (The actual flags, e.g. `-g`, I'll call "concrete flags". (Can you tell I do stuff in programming languages? :-)) 

"Environment variables" refers to the usual (non-SCons) meaning of things you set with `export` or `set` or whatever. I'll use "env variable" for something you set with `env["FOO"]` or whatever. 

<small>Text in blue discusses rationale.</small> In general, I take inspiration primarily from the Builder interfaces I've seen from projects using autotools and CMake. 

<small>Text in red is a specific question.</small> 

Finally, recognize that I'm coming to this from a very C/C++ perspective. Comments on how my suggestions interact with other languages are welcome, but recognize that if there's a nontrivial effort to get something to work with, say, Fortran, I probably won't do it. (I will, however, be happy to leave open the door to other efforts. But I have a couple years of I wish I had time to program this" projects. :-)) Likewise, an observation that one of my goals or techniques interacts fatally with another language won't get me to _not_ do it unless there's a reasonable alternative. 

Said another way: it'd be wonderful if other people found this useful too, but almost everything in here is something that _I_ want, and I don't have a ton of time to work on this. 


# Goals

* The builder should be able to easily specify all of the following at the command line: 
   * The path to the compiler 
   * The compiler model (but this should be deduced from the path when reasonable) 
   * Compiler flags, both concrete and abstract 
   * Build presets, like "debug" and "release" (basically just preconfigured settings of the concrete & abstract flags) 
   * Install prefixes 
   * Paths to dependencies 
<small>I compile some projects with several different compilers. (I have one project set up to build nightly with Intel CC, MSVC, Pathscale, maybe Open64, and several versions of GCC.) Partially because I didn't start with a very clean base and partially because I made things worse by not doing anything planned when I was trying to get things to work with other compilers, there are a bunch of "if GCC, do this, otherwise do that", except that _those_ became ugly because `CC` isn't just `gcc`, it's usually `/some/path/to/gcc`, so now you need to split the last path component out and ugly ugly ugly. (I consider writing this library to be a part of cleaning that up.)</small> 

<small>In addition, we also have a number of libraries that are also installed in weird locations, so many third-party dependencies (e.g. Boost, if you want a new version) have to have paths specified explicitly somehow.</small> 

<small>The flip side of the previous point is I often _build_ packages to weird locations, so I also want a good way to set the prefix.</small> 

* Ideally, different variants build to different directories, and sometimes with different filenames (e.g. `libspork` and `libsporkd` on the debug build). 
<small>It's nice to be able to test a change on multiple compilers and configuratios at the same time without having to either rebuild everything or copy stuff from one working tree to another (especially without DVCS).</small> 

* Settings stick around run-to-run 
* The developer should get the above by doing as little as possible. 
<small>Hopefully these are uncontroversial. The last goal won't be completely met, but I think I can get the first set of goals with only a small amount of additional boilerplate.</small> 

* Inspired by some of the discussion, the ability for the Developer to specify that a library should only be linked statically (or only dynamically). 
<small>How important is this for the Builder to be able to specify this, either if the `SConstruct` doesn't express a preference or if overriding its preference?</small> 


# How the Builder interface will look

For this section, assume that the Developer is cooperating and using the features I am proposing. 

There will be a number of flags that are set up beforehand and more prompted by configure checks. The user will just pass these flags on the command line: 

`scons SCONS_CXX=/something/icpc SCONS_BUILD_TYPE=RELEASE` 

or set as environment variables. 

<small>Should environment variables be automatically imported? If so, should it be possible to easily _disable_ that importing and still use this library? If not, should it be possible to easily _enable_ that importing? (One goal is to help promote a uniform Builder interface. Making it up to the whim of the Developer whether environment variables are imported works against that goal.)</small> 

This will build things to some directory like `#/.build/release`, using the Intel C++ compiler. 


## Variables I'd like to support

To support the first goal (or first subgoal of the first goal), "the path to the compiler", and second goal, "he compiler model (but this should be deduced from the path when reasonable)": 

* `SCONS_CC` and `SCONS_CXX` to set the path to the compiler 
* `SCONS_TOOLCHAIN` to set the compiler model 
Several other tools (e.g. things like `ar` and `ranlib` that I never replace anyway and things like `SCONS_SHCC` and `SCONS_LD` that are usually redundant in my experience) are much lower priority. 

The value of `SCONS_TOOLCHAIN` would be something like `gcc`, `intelcc`, `msvc`, etc.; the general idea would be to use the SCons tool name that corresponds. (This only sort of works of course, as really there's probably some interaction between different kinds of tools, e.g. `gcc` and `gnulink`.) 

To support the third goal, "compiler flags, both concrete and abstract": 

* `SCONS_C_FLAGS`, `SCONS_CC_FLAGS`, etc. for concrete flags. Basically one for many of the env variables that SCons usually pays attention to.  
<small>Possibly `SCONS_C_FLAGS` should be `SCONS_CFLAGS` etc. to match the spelling in SCons. Personally I don't like the smushed together names, especially stuff like `CPPPATH`, but maybe that's just me. This is some CMake influence.</small> 

* For abstract flags, the following flags, each of which can be set to a value described below or to a string that is substituted in place of whatever flag would have been generated 
   * `SCONS_COMPILER_DEBUG`, True or False (e.g. translates to `-g` with GCC) 
   * `SCONS_COMPILER_WARNING_LEVEL`, some number between 0 and 4ish, though this will probably be a bit tool-dependent (e.g. 3 might translate to `-Wall -Wextra` with GCC, ) 
   * `SCONS_COMPILER_WARNING_AS_ERROR`, True or False 
   * `SCONS_COMPILER_OPTIMIZATION`, some number between 0 and 3ish 
   * `SCONS_C_STANDARD`, "c89", "c99", "c11", capital versions of those, and a couple named constants (from within the build files). Maybe other aliases. 
   * `SCONS_CXX_STANDARD`, "c++98", "c++11", capital versions of those, maybe other aliases. 
More abstract flags would likely be added over time. In addition, for the Developer's interface, all of the abstract flags would also be provided as env vars without the `SCONS_` suffix. 

<small>Suggestions for a better way of doing `SCONS_WARNING_LEVEL` are welcome. I'll probably provide some named constants too, but I like the number idea because it provides a way that a tool can (admittedly ugily) define new levels between existing ones, e.g. a level 3.5.</small> 

<small>The above names, as opposed to something like `SCONS_CC_DEBUG`, afford passing the corresponding flags to other tools like for Fortran or D or whatever, but using one flag for everything obviously means that you can't split it out. How important is that? Should it have just `SCONS_COMPILER_DEBUG`? Just `SCONS_C_DEBUG`, `SCONS_CC_DEBUG`, `SCONS_CXX_DEBUG`, etc.? All, with the more specific one taking precedence?</small> 

To support the fourth and fifth goals, "Build presets, like "debug" and "release" (basically just preconfigured settings of the concrete & abstract flags)" and "Installation refixes" 

* `SCONS_BUILD_TYPE`; by default `RELEASE` and `DEBUG` would be provided, but a package could define their own. Maybe others, e.g. `DEBUG_SHARED` and `RELEASE_STATIC`, but I think there are probably better ways to do that. 
* `SCONS_PREFIX`; a path 
* Probably other prefix variables from the autotools land (e.g. `SCONS_EXEC_PREFIX`) 
To support the last goal, "Paths to dependencies": 

* For each library depended on, a trio of `''LIB''_INC_DIR`, `''LIB''_LIB_DIR`, and `''LIB''_PREFIX` (e.g. `BOOST_INC_DIR`), with the latter automatically registering `''LIB''_PREFIX/include` and `''LIB''_PREFIX/lib` 
<small>General question for this section: The stuff that controls the behavior of my stuff more than the build has the `SCONS_` prefix. Excessive, or no? Again, this is some CMake influence.</small> I'd say there's some interaction between this choice, the `CC_FLAGS` vs `CCFLAGS` issue above, and whether to import environment variables.-~ 


# How the Developer interface will look

I think nearly all of the above can be supported for `SConstruct`s that just call my replacement for `Configure`. Some other things need additional support. 

Here's an example `SConstruct` annotated with what it does. 


```txt
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|                                                   |Creates a new environment. Because the toolchain that should be loaded will be picked    |
|env = Environment(tools=[])                        |during configuration, no tools are loaded yet.                                           |
|                                                   |                                                                                         |
|                                                   |(This is a bit unfortunate that you have to say that explicitly. Theoretically, I could  |
|                                                   |replace the Environment() function with one that doesn't load any tools that will be     |
|                                                   |managed later.)                                                                          |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|                                                   |This registers all of the "preset" command line variables (those starting with `SCONS_`  |
|conf = AwesomeConfigure(env)                       |above) and pulls them in as env variables.                                               |
|                                                   |                                                                                         |
|                                                   |Loads the tools for compiling, linking, etc. for languages it manages.                   |
|                                                   |                                                                                         |
|                                                   |Optional arguments could tell it to ignore or include environment variables (whatever the|
|                                                   |default is not), or get its flags from somewhere else (I'm not totally sure what this    |
|                                                   |means right now). Perhaps also some specification that it shouldn't load the compiler    |
|                                                   |tools, or should only load those in a particular category, or something like that. Also a|
|                                                   |specification of any additional build presets, in the form of a dictionary from preset   |
|                                                   |name to (a dictinoary of variable names and values to apply to env).                     |
|                                                   |                                                                                         |
|                                                   |This name is tongue-in-cheek and temporary. :-)                                          |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|                                                   |Takes three steps:                                                                       |
|conf.RequireLibWithHeader('gmp', 'gmp.h', 'c')     |                                                                                         |
|                                                   |1. Registers `GMP_INC_DIR`, `GMP_LIB_DIR`, and `GMP_PREFIX`; pulls those variables into  |
|                                                   |the environment if they are specified.                                                   |
|                                                   |                                                                                         |
|                                                   |2. Does the normal `conf.CheckLibWithHeader()` thing.                                    |
|                                                   |                                                                                         |
|                                                   |3. If the check fails, outputs an error message saying what the failure is and pointing  |
|                                                   |the user at those variables.                                                             |
|                                                   |                                                                                         |
|                                                   |There will also be a `CheckLibWithHeader` replacement that does the current thing except |
|                                                   |with the new step #1.                                                                    |
|                                                   |                                                                                         |
|                                                   |Optional parameters can specify a different variable to prefix (instead of `GMP`) for the|
|                                                   |variable trio, or disable that feature all together. An optional parameter specifies     |
|                                                   |whether to require a static (or dynamic) library.                                        |
|                                                   |                                                                                         |
|                                                   |~-I'd also like a good way to deal with pkg-config stuff. I'm open                       |
|                                                   |to suggestions here; I'm actually pretty unfamiliar with that tool.-~                    |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|env = conf.Finish()                                |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|env["COMPILER_DEBUG"] = True                       |Modify an abstract flag                                                                  |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|                                                   |Add some weird flag that my thing doesn't have support for.                              |
|if env["COMPILER_MODEL"] == "gcc":                 |                                                                                         |
|    env.AppendUnique(                              |                                                                                         |
|        CCFLAGS="-fdiagnostics-show-option")       |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|env.SConscript("src/SConscript",                   |Build to a directory constructed from some of the compiler settings.                     |
|               variant_dir=env.VariantName())      |                                                                                         |
|                                                   |Optional flags to `AwesomeConfigure()` could specify how things are put together to get  |
|                                                   |the variant name, though I'm not sure totally how yet. By default it would probably be   |
|                                                   |just the value of `SCONS_BUILD_TYPE`.                                                    |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|                                                   |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|(src/SConscript)                                   |(Not starting at beginning)                                                              |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|lib = env.Library("spork", sources)                |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|env.InstallLibrary(lib)                            |Hijack the builder from http://scons.org/wiki/PlatformIndependedInstallationTool which   |
|                                                   |looks like a really nice interface. (Variable names would need to change.)               |
|                                                   |                                                                                         |
|                                                   |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|prog = env.Program("spork-ui", sources_ui)         |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
|`env.InstallProgram(prog)`                         |                                                                                         |
+---------------------------------------------------+-----------------------------------------------------------------------------------------+
```
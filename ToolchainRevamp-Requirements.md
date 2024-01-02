
* Allow installing external tools (pip install or ...) 
   * scons --version (or similar) should list installed tools and toolchains 
   * missing external tools should give sensible errors 
* Tool setup must happen before reading SConstruct somehow 
   * `DefaultEnvironment` and all new Environments should know about all tools 
   * alternative: lazy-construct `DefaultEnvironment` 
   * user-specified tools and toolchains need to be specifiable at beginning of build 
* User should be able to set default tools and toolchains 
   * unused tools shouldn't take any startup time 
* Lazy init of tools and chains 
   * This is faster because unused tools don't matter 
   * It allows missing unused tools to not give errors, but missing used tools can (and should) 
   * But it makes configuring environments much harder for users, because they can't override or append to tool-provided variables until those exist.  This would break a lot of existing SConstructs. 
   * We need to find some kind of compromise here: 
      * Explicitly list tools required by build (where?): this should work well because only the needed tools will be initialized 
      * if nothing explicitly specified, fall back to current method 
* Within a tool: 
   * specify dependencies on other tools 
   * detect existence on system reliably, and without modifying env 
      * need better error messaging: ability to probe silently, but also give sensible errors when needed 
   * constructor needs to allow args: version, path, ABI, etc. (this is important) 
   * allow for common setup (all C compilers, etc.) as now 
   * tools should be versioned so user can check if up to date, etc. 
   * Let a tool declare beforehand which variables it accepts and defines on any platform, without actually completely initializing the tool. 
      * Allows to define additional flags even when unused on the current platform. 
      * Improves auto-generated tool docs 
* Tool chains: 
   * either-or 
   * and 
   * collections 
* Platform 
   * How much do we need to know about the platform, for tools to initialize themselves? 
   * Cross-compilation comes into this, but may be too much to include as a general part of this project. 
   * It may be useful to define toolchains and enable/disable them by platform 
   * Of course the default toolchains need to be different by platform 
   * It may be possible for a default toolchain to just search for all tools in a particular order and pick the first, as long as the tool-dependency system is robust enough. 
* Usability 
   * $CC etc. must never be left blank (without a prior tool-missing error message at least) - this is a common problem 
   * Must be backward compatible, at least for all common cases. 
   * Must not require any new user files (e.g. something in site_scons) for normal operation 
   * Need a clear guide on requirements for new tools 
      * how to make a a tool 
      * how to include tests 
* Considerations 
   * "batteries included?" 
      * Each tool should do its best to set itself up, find executables, etc. 
      * What about SCons policy of not relying on `$PATH`?  Maybe we should relax that or have an option? 
   * minimum magic, maximum flexibility 
   * what about single tools?  Should every tool be required to be part of a toolchain (even if it's just one tool)?  Maybe this doesn't matter much. 
* Non-goals: 
   * New command-line args like autotools (platform, install paths, etc.).  We should build something that would enable that, but it's too much to bite off now. 
   * Persistence -- remember configuration on disk between runs.  This is a performance enhancement which we should address only once we know it's needed.  Better if we can design a system that's fast without needing this. 
* References: 
   * [PlatformToolConfig](PlatformToolConfig) (Greg's original proposal) 
   * [RevampToolsSubsystem](RevampToolsSubsystem) 
   * [PlatformToolConfigAlt](PlatformToolConfigAlt) (my proposal from 2008) 
   * [EvanEnhancedConfigurationPackageProposal](EvanEnhancedConfigurationPackageProposal) 

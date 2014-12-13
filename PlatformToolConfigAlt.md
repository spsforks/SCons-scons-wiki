# Alternate Proposal for configuring platforms and tools
This is based on [PlatformToolConfig](PlatformToolConfig) by Greg Noel.  This is partly an extension of the ideas in that page and partly an exploration of a different direction to see where it leads.  Like [PlatformToolConfig](PlatformToolConfig), it's quite preliminary and exploratory.  Comments welcomed! Starting with a gnu-style config-vendor-os triple is a fine idea.  Some tools won't care about parts of that triple, so a function to match with wildcards will be handy. In my experience, trying to set up tables and complex rules for configuring tools never works that well.  There are too many exceptions and special cases.  What I advocate here is just a hierarchy of lists of functions, each of which can be overridden by the user.  Customizability is the key.  SCons should have a default set of these function lists per known platform, and users should be able to override them by name (in a site_scons/site_init.py file). Here's a sample for explicitness: ```python
#!python 
class AboutPlatformAndTools:
  def __init__(self, platform):
    if platform == 'i686-pc-linux-gnu':
      AllTools={CC_Toolchain, Fortran_Toolchain, 'latex', 'm4' }
      CC_Toolchain = {ToolRequired(ToolAlternate('intelc', 'gcc'))}
      Fortran_Toolchain = {ToolAlternate(...)}
```The idea is that the tool lists contain either other lists (which are recursed into) or strings, which are traditional tool names.  [ToolAlternate](ToolAlternate) creates a callable class that looks like a tool that picks the first existing tool from its arguments.  [ToolRequired](ToolRequired) makes a tool "required" by raising an error if its tool argument is missing (exists() returns 0).  Normally, missing tools are silently ignored.  The Environment constructor just goes through [AllTools](AllTools) and applies each tool found to the environment using its generate() method (or just calling the function if it's a TOOL_XXX(env) function rather than a string, I guess -- functions like this should be assumed to always exist.) The toolchain names defined in [AboutPlatformAndTools](AboutPlatformAndTools) are standardized and documented, so if a user wants a definite C compiler and some additional tools, they just override in their site_init.py: ```python
#!python 
if platform == 'win32': # what's the gnu string for this?
  AboutPlatformAndTools.CC_Toolchain = {'mingw', 'fail'}
AboutPlatformAndTools.AllTools.append('java')
```Some notes: 
* Greg's config guesser/canonicalizer can and definitely should be used here. 
* Greg's proposal has other useful things like initializing the prefix/suffix lists; those should be in here too.  Basically anything environment constructors or tools need to know can get thrown in here. 
* I've explicitly ignored cross-compilation.  Those who want it can easily build their own tool lists from the pieces above, I think.  The wiki could have a list of known-good cross-compilation environments and tool lists. 
* This doesn't make any direct (default) use of command-line args; I'm not sure that's appropriate for scons. 
* I don't actually think the list of toolchain names is very long.  Most tools are not part of any defined toolchain: lex, latex, qt, tar, etc.  Toolchains are c/c++, fortran, and maybe a few others. 
* This method still allows replacing or augmenting individual tools (e.g. "gcc" which is in gcc.py) by putting your own gcc.py in site_scons, but that's not the point of this stuff. 
* I try to strive for minimum magic, minimum change to existing architecture, and maximum flexibility.  Some casualties of that are that it's harder to replace a single tool that's directly in [AllTools](AllTools) for instance; you have to find the current value and copy/paste/change it, or else do some list surgery that's probably fragile. 


---

 Comments here: 

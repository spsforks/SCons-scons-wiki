
Different classes of users have different needs from a toolchain.  This is originally from an email on the scons dev list by Michael Haubenwallner, with some additions by Gary Oberbrunner. 

* The upstream package source maintainer 
   * Specify which language-tools are to be initialized: C89, C99, C++, C++11, JavaC, ... 
      * or let SCons auto-detect used languages along the list of source-files 
   * Avoid the need to take care of platform- and tool-details: 
      * Let the language-tool delegate to (or know about): cl.exe/gcc/xlc/hp-cc/... 
      * Make additional resource-tools a no-op on platforms not using them 
   * Specify package-default (used during development) language-/tool-options 
      * warnings (as errors), debugging, optimization, ... 
      * the language tool implementation filters unsupported flags 
   * Don't care about a library to be static or shared - just define a Library: 
      * fex, AIX traditionally used just _one_ file target for both the static and the shared library (yes, shared objects can be linked statically). 
   * (maybe more) 
* The downstream (distro) package build/integration maintainer 
   * Define the language-tool implementation to use: cl.exe/gcc/xlc/hp-cc/... 
   * Define the actual tool-executable to use (PATH, ...) 
   * Set the final language-/tool-options: 
      * warnings (as errors), debugging, optimization, additional QA flags 
      * override the package-default values 
   * Define to build the Library as static and/or shared. 
   * Define the search path for package dependencies. 
   * (maybe more) 
* The downstream (distro) package build/integration maintainer for SCons: 
   * Define default language-tool implementation to use: cl.exe/gcc/xlc/hp-cc/... 
      * To be used by upstream package source maintainer 
   * Define the default tool-executable to use (PATH, ...) 
   * Define the default search path for package dependencies. 
   * (maybe more) 
* Commercial software developers (in-house) 
   * Define exactly which language/tool implementation to use, including version (optionally) 
      * Possibly overridable by individual developers or external config files 
   * Give good error messages when tools are missing or misconfigured 
For each design decision, IMHO it is important to think of /who/: 

* defines the defaults, 
* overrides the defaults, 
* prepends/appends to the defaults. 
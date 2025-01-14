
# SCons and Eiffel

This is a SCons tool for building [EiffelStudio](https://dev.eiffel.com) projects. It works with EiffelStudio 5.7 and above (although the latest EiffelStudio is recommended, currently 15.12). It has been tested on Windows (XP, 2003, 7, 2008 and 10), Mac OS X (everything from 10.4 to 10.11) and Linux (Ubuntu 7.10 and 10.04). [*update: v23.09 was released in Sept 2023, if anyone has tested with a later release than the 15.12 listed it would be good to update this page*]

Put the builder in a script called `Eiffel.py`, in a directory that you reference with _toolpath_, as shown in the example below; or put it in a directory called _site_scons/site_tools_ as mentioned in the SCons man page. 

It requires Python 2.4 or above, because it uses the _subprocess_ module which was new in Python 2.4. 


### Sources and Targets

This Eiffel builder knows the nuts and bolts of running EiffelStudio's command-line compiler. Each EiffelStudio project has an Eiffel configuration file (`.ecf`) and builds an executable or a DLL. You feed the builder the path to the `.ecf` configuration file; this is the builder's _source_. You can specify additional source dependencies, if you wish (resource files, icons, etc.). 

The `.ecf` file contains one or more **targets**. A `.ecf` target specifies which executable you want to build and how to build it. You specify one of these to the builder. 

The target passed to the builder is not the same as the target that the builder emits. The target passed in is a string (e.g., 'foo'), from which the builder computes the emitted full target path (e.g., `C:\projects\app\EIFGENs\foo\F_code\foo.exe`). The builder's emitter computes the full target path by reading various settings inside the `.ecf` file. (For example, the `executable_name` setting gives the base name of the target file; sometimes this setting is missing, in which case the base name is the same as the `.ecf` document element's `name` attribute. The target file extension is also computed; for example, it is .dll if the `msil_generation_type` setting is `dll`.) 

When calling the builder, you may omit the target if you wish. _By default, the Eiffel builder builds the target with the same base name as the `.ecf` file._ (There will be an error, of course, if the `.ecf` file has no such target.) 

The builder usually emits one target file path (the executable or dll). In some cases, however, it emits more. 

* When building a .NET assembly (say, `Foo.exe` or `Foo.dll`), 'ec' also generates an unmanaged DLL (`libFoo.dll`) in the same directory. The emitter adds it as a second target. 
* When building a shared library on Windows (say, `foo.dll`), 'ec' generates a second file `foo.lib` in the same directory. The emitter adds it as a second target. 
* When building a precompiled library in classic mode (i.e., non-.NET), it emits a `.melted` file in the `W_code` directory, plus the actual precompiled library files in a compiler-specific subdirectory. 
* When C compilation is not performed, no executable or DLL will be built. Instead, the emitted target is the `Makefile.SH` file that controls C compilation. This is handy if the calling script needs to manipulate `Makefile.SH` prior to launching C compilation as a separate step. The emitter also adds `project.epr` as a target, because it is created at the end of the Eiffel compilation and is therefore a good indicator that compilation succeeded. 

### The Scanner

Apart from the `.ecf` file, the most important input to the Eiffel compiler is the universe of **.e** Eiffel class files that it has to compile. These class files are dependencies that the builder figures out for itself, by scanning the `.ecf` file. The Scanner looks for all _cluster_ and _override_ declarations inside the `.ecf`, and finds all .e files in each such directory. Therefore, thanks to the Scanner, if you modify an Eiffel class in one of the clusters named in the `.ecf`, or if you modify the `.ecf` itself, then the builder will know that it needs to rebuild the project. 

If the cluster or override is recursive, then the Scanner scans the subdirectories too. If it's not recursive but has explicitly-named sub-clusters, the Scanner also understands how to scan these sub-clusters. 

As well as **.e** class files, the scanner detects the following dependencies mentioned in the `.ecf` file: 

* **`.ecf` libraries**. (Such libraries are not recursively scanned, however. Although it's useful to detect that the library file itself has changed, a library is a stable thing, so scanning its contents would be a waste of time.) 
* **.NET assemblies**. 
* External object files. 
* **.h** or **.hpp** files inside external include directories. 
Environment variable substitution is performed on the file and directory paths. The Scanner prints warnings if the `.ecf` file uses undefined environment variables. _Construction variables are deliberately ignored, because it would be incorrect to substitute them given that the Eiffel compiler does not know about SCons construction variables._ The following EiffelStudio environment variables are commonly used in `.ecf` files, so if they are undefined the builder tries to define them with sensible platform-specific assumptions: 

* **ISE_C_COMPILER** 
* **ISE_EIFFEL** 
* **ISE_LIBRARY** 
* **ISE_PLATFORM** 
* **ECF_CONFIG_PATH** 

### Choosing an Eiffel Compiler

The builder has a construction variable **EC**, specifying the Eiffel command-line compiler. It defaults to the path to "ec" found in the **PATH** environment variable. Failing that, it uses the **ISE_EIFFEL** environment variable to construct the path to "ec". If this too fails, then it falls back simply to "ec". (Using **ISE_EIFFEL** is helpful, for example, when running SCons on Linux or Mac via **sudo**, which restricts the **PATH** variable, or if the user has not added "ec" to the path.) 

EiffelStudio 6.2 introduced an alternative compiler called "ecb". Its output is identical to the output of "ec", but it reportedly runs about 20% faster. Beware, however, that "ecb" uses its own set of precompiled libraries, rather than the ones installed with EiffelStudio, so if you are using precompiled libraries you will have to build them specially for "ecb". 

I haven't tested the builder with the Gobo Eiffel compiler [gec](http://www.gobosoft.com/eiffel/gobo/gec/index.html), nor with Helmut Brandl's Eiffel interpreter and compiler [tecomp](http://tecomp.sourceforge.net). 


### Eiffel Compiler Flags

The **ECFLAGS** construction variable controls what kind of build is done by the Eiffel compiler. Possible values for ECFLAGS are given by typing `ec -help` at the command line. Here are some common examples: 

* `scons ECFLAGS="-finalize -clean -c_compile"`: build a finalized (i.e. optimized) executable, from scratch, without assertions. _This is the default._ 
* `scons ECFLAGS="-finalize -clean"`: build the C files for a finalized build, from scratch, without assertions, but do not build the executable. 
* `scons ECFLAGS="-finalize -keep -c_compile"`: do an incremental build of a finalized executable, retaining assertions. 
* `scons ECFLAGS="-precompile -clean" -c_compile`: build a precompiled library. 
* `scons ECFLAGS="-freeze -c_compile"`: do an incremental freeze (i.e., make a debug executable). 
* `scons ECFLAGS="-freeze -project_path 62 -c_compile"`: do an incremental freeze, in a subdirectory below the SConscript called "62", rather than the default location below the `.ecf` file. 
* `scons ECFLAGS="-freeze -target app_no_precompile -c_compile"`: do an incremental freeze, using the the `.ecf` target "app_no_precompile". 
Note, in the last example, that specifying the `-target` flag overrides any other way of specifying the target. 

**ECFLAGS** can be set by several means: 

* On the SCons command line (as shown in the examples above); 
* As a named parameter to your Eiffel builder call (as shown in the example below, which is probably the most convenient way to do it); or, 
* By setting `env['ECFLAGS']` explicitly, prior to calling the Eiffel Builder. 

### Logging

The Eiffel compiler 'ec' produces a lot of progress output. Generally you don't want to see this, so the Eiffel builder redirects it to a file, "SCons.Eiffel.log", in the same directory as the SConstruct. You can specify a different file by setting the **ECLOG** construction variable. If you want to let it to go to standard output, set **ECLOG** to nothing (e.g., on the command line, `scons ECLOG=`). 

But you _do_ want to see this output if the build fails! You can open the log file to inspect the reason for failure, which would normally be at the end of the log file. For convenience, however, the Eiffel builder echoes the last thousand characters from the log file onto standard output, which almost invariably proves to be just the right amount of detail to allow you to see what went wrong. 


### Example Usage

The following SConstruct is an example of how to use the EiffelStudioTool. This example assumes that you have previously created an EiffelStudio configuration file called `app.ecf` that has 3 targets: 

* **gobo** to precompile the Gobo library. 
* **app** to build an executable named "app" without any precompiled libraries. 
* **app_using_precompile** to build "app" with the Gobo precompiled library. 

```python
#!python
# Create an Environment that imports "Eiffel.py" from the same directory as the SConstruct.

import os
env = Environment(ENV = os.environ, tools = ['Eiffel'], toolpath = ['.'])

# Build "app" (or, on Windows, "app.exe").
# The build depends on "app.ecf" and "app.rc".
# It also depends on all of the "*.e" files, etc., found by the Scanner.
# (Note how the target does not need to be specified, because by default it builds the target with the same base name "app".)

env.Eiffel(['app.ecf', 'app.rc'])

# Build the precompiled Gobo library.
# (Note how we specify the "gobo" target explicitly.)

gobo = env.Eiffel('gobo', 'app.ecf', ECFLAGS = '-precompile -clean -c_compile')

# Here's how to build "app" with the Gobo precompiled library.
# (Note how it depends on "gobo", and the target is explicitly given.)

env.Eiffel('app_using_precompile', ['app.ecf', 'app.rc', gobo])

```

### Builder


```python
#!python
# EiffelStudio support for SCons
# Written by Peter Gummer, February 2007
# Scanner added - Peter Gummer, May 2007
# Scanner uses xml.dom - Peter Gummer, September 2007
# Fix scanning non-recursive clusters - Peter Gummer, March 2008
# Don't call finish_freezing - Peter Gummer, April 2008
# Support -target and -project_path compiler options and incremental builds - Peter Gummer, May 2008
# Scanner detects more dependencies - Peter Gummer, June 2008
# Emitter computes target by reading `.ecf` file - Peter Gummer, June 2008
# Support -c_compile compiler option rather than hard-coding it - Peter Gummer, December 2008
# Fix scanning on non-Windows platforms - Peter Gummer, August 2010
# Emitter computes target compatibly with EiffelStudio 6.5 and higher - Peter Gummer, August 2010
# Scanner detects "tests" dependencies to be compatible with EiffelStudio 6.7 - Peter Gummer, December 2010
# The EC variable defaults from the the PATH or ISE_EIFFEL environment variable - Peter Gummer, December 2010
# Scanner expands $ECF_CONFIG_PATH in dependency locations - Peter Gummer, May 2011
# Adjust manifest file path in Windows resource file - Peter Gummer, July 2012
# Remove the Files() method; use Glob() instead - Peter Gummer, January 2013

"""
Tool-specific initialisation for EiffelStudio.
This does not work with EiffelStudio 5.6 or earlier.
"""

import os, glob, sys, shutil, datetime, subprocess, re, xml.dom.minidom
from SCons.Script import *
        
log_file = None

def log_open(env):
        global log_file

        if env['ECLOG'] == '':
                log_file = sys.stdout
        elif log_file == None:
                log_file = open(env['ECLOG'], 'w+')
        elif log_file.closed:
                log_file = open(env['ECLOG'], 'a+')

def log(s):
        log_file.write(str(s) + '\n')

def log_date():
        log(datetime.datetime.now())

def log_process(args):
        commandline = subprocess.list2cmdline(args)
        if log_file != sys.stdout: print '  ' + commandline
        log(commandline)
        log_file.flush()
        subprocess.call(args, stdout = log_file, stderr = subprocess.STDOUT)

def log_file_tail():
        """The last thousand characters of the log file."""
        result = ''

        if log_file != sys.stdout:
                if log_file.tell() > 1000:
                        log_file.seek(-1000, 1)
                else:
                        log_file.seek(0)

                result = '... ' + log_file.read()
                log_file.seek(0, 2)

        return result

def ec_action(target, source, env):
        """
        The Eiffel Builder's action function, running the Eiffel compiler.
        Parameters are as returned by ec_emitter():
         * target: the paths to the files to be built, as generated by ec_emitter().
         * source[0]: the ECF file.
         * source[1], source[2], etc.: any additional dependencies.
         * env['ECLOG']: name of file to which all compiler output is logged (stdout if empty).
         * env['ECFLAGS']: Eiffel compiler flags: -finalize, -freeze, -clean, -project_path, -target, etc.
        Result is 0 (success) if all targets are built; else 1.
        (Note that the Eiffel compiler's return code is unreliable: it returns 0 if C compilation fails.)
        """
        result = 0

        log_open(env)
        log('=================== ' + ecf_target(target) + ' ===================')
        log_date()

        rc_copied_to_target = None

        if env['PLATFORM'] == 'win32':
                rc = os.path.splitext(str(source[0]))[0] + '.rc'

                if os.path.exists(rc):
                        project_path = dirname(str(target[0]), 4)
                        rc_copied_to_target = os.path.join(project_path, os.path.basename(rc))

                        if rc == rc_copied_to_target:
                                rc_copied_to_target = None
                        else:
                                f = open(rc, 'r')
                                try: s = f.read()
                                finally: f.close()

                                if s:
                                        icon_pattern = r'(\w+[ \t]+ICON[ \t]+[^"]*")([^"]+")'
                                        manifest_pattern = r'(CREATEPROCESS_MANIFEST_RESOURCE_ID[ \t]+RT_MANIFEST[ \t]+")([^"]+")'
                                        substitution = r'\g<1>' + os.path.dirname(rc).replace('\\', '/') + r'/\g<2>'
                                        s = re.sub(icon_pattern, substitution, s)
                                        s = re.sub(manifest_pattern, substitution, s)
                                        f = open(rc_copied_to_target, 'w')
                                        try: f.write(s)
                                        finally: f.close()

        flags = env['ECFLAGS'].split()
        if not '-target' in flags: flags += ['-target', ecf_target(target)]
        log_process([env['EC'], '-batch', '-config', str(source[0])] + flags)

        for t in target:
                if result == 0 and not os.path.exists(str(t)):
                        print log_file_tail()
                        result = 1

        if rc_copied_to_target: os.remove(rc_copied_to_target)
        if log_file != sys.stdout: log_file.close()
        return result

def ec_emitter(target, source, env):
        """
        The Eiffel Builder's emitter function.
        Parameters:
         * target[0]: the ECF target to be built; if empty then defaults to the first target in the ECF file.
         * source[0]: the ECF file. The paths to the files to be built are computed by reading this file.
         * source[1], source[2], etc.: additional optional dependencies (precompiled libraries, ".rc" files, etc.).
         * env['ECFLAGS']: Eiffel compiler flags. The paths to the files to be built are affected by these.
        Result emits the target and source parameters passed to ec_action().
         * The source emitted is exactly the same as the source parameter passed in.
         * The target emitted contains one or more calculated file paths.
           Each target file is in the directory {-project_path}/EIFGENs/{-target}/{-finalize}, where:
                -project_path if omitted defaults to the current working directory;
                -target if omitted defaults to the base name of target[0] (or else to the first target in the ECF file);
                -finalize evaluates to "F_code", else if omitted defaults to "W_code".
           The number of target file paths emitted, and the actual file names, depend on several factors:
            * Options specified inside the ECF file;
            * The -precompile flag;
            * The -c_compile flag.
        """
        result = None

        if len(target) > 0:
                ec_target = os.path.basename(str(target[0]))
        else:
                ec_target = ""

        if len(source) == 0:
                print '****** ERROR! No source .ecf file specified: cannot build ' + ec_target
        elif not env.Detect(env['EC']):
                print '****** ERROR! The Eiffel compiler ' + env['EC'] + ' is missing from your path: cannot build ' + ec_target
        else:
                ecf = str(source[0])
                ec_path = os.getcwd()
                ec_code = 'W_code'
                exe_name = dotnet_type = is_dotnet = is_precompiling = is_c_compiling = is_shared_library = None

                flags = env['ECFLAGS'].split()

                for i, flag in enumerate(flags):
                        if flag == '-project_path':
                                ec_path = flags[i + 1]
                        elif flag == '-target':
                                ec_target = flags[i + 1]
                        elif flag == '-finalize':
                                ec_code = 'F_code'
                        elif flag == '-precompile':
                                is_precompiling = True
                        elif flag == '-c_compile':
                                is_c_compiling = True

                ecf_as_xml = xml.dom.minidom.parse(ecf)
                ec_target_next = ec_target

                while ec_target_next <> None:
                        t = ec_target_next
                        ec_target_next = None

                        for element in ecf_as_xml.getElementsByTagName('target'):
                                name = element.attributes['name'].value
                                if ec_target == "": t = ec_target = name

                                if t == name:
                                        if element.hasAttribute('extends'):
                                                ec_target_next = element.attributes['extends'].value

                                        for setting in element.getElementsByTagName('setting'):
                                                name = setting.attributes['name'].value

                                                if name == 'msil_generation':
                                                        if is_dotnet == None:
                                                                is_dotnet = setting.attributes['value'].value == 'true'
                                                elif name == 'msil_generation_type':
                                                        if dotnet_type == None:
                                                                dotnet_type = '.' + setting.attributes['value'].value
                                                elif name == 'executable_name':
                                                        if exe_name == None:
                                                                exe_name = setting.attributes['value'].value
                                                elif name == 'shared_library_definition':
                                                        if is_shared_library == None:
                                                                is_shared_library = True

                if exe_name == None:
                        exe_name = str(ecf_as_xml.documentElement.attributes['name'].value)

                if dotnet_type:
                        ext = dotnet_type
                elif is_precompiling:
                        ext = '.melted'
                elif is_shared_library:
                        exe_name = env['SHLIBPREFIX'] + exe_name
                        ext = env['SHLIBSUFFIX']
                else:
                        exe_name = env['PROGPREFIX'] + exe_name
                        ext = env['PROGSUFFIX']

                ec_path += '/EIFGENs/' + ec_target + '/'

                if is_c_compiling:
                        ec_path += ec_code + '/'
                        result = [ec_path + exe_name + ext]

                        if is_dotnet:
                                result += [ec_path + 'lib' + exe_name + '.dll']
                        elif is_precompiling:
                                result += [ec_path + environment_variable(env, 'ISE_C_COMPILER') + '/' + env['PROGPREFIX'] + 'driver' + env['PROGSUFFIX']]
                        elif is_shared_library and env['PLATFORM'] == 'win32':
                                result += [ec_path + 'dll_' + exe_name + '.lib']
                else:
                        result = [ec_path + ec_code + '/Makefile.SH', ec_path + 'project.epr']

        return result, source

ecf_environment_variable_regex = re.compile(r'(\$\||\$\(?\w*\)?|[^$]+)', re.M)

def ecf_scanner(node, env, path):
        """
        All dependencies mentioned in 'node', which is expected to be an ECF file.
        The dependencies consist of:
         * All Eiffel class files found in all clusters (including override clusters) mentioned in the ECF file.
         * All .ecf library files mentioned in the ECF file. (Such libraries are not themselves scanned).
         * All .NET assemblies mentioned in the ECF file.
         * All external object files mentioned in the ECF file.
         * All .h and .hpp files found in external include directories mentioned in the ECF file.
        Because this ignores targets and conditionals in the ECF file, it may cause unnecessary builds.
        """

        def element_location(element):
                """
                The 'location' attribute of 'element', processed to take care of:
                 * Expansion of environment variables.
                 * If 'location' is relative, prefixing with the directory name of 'node'.
                 * If 'location' is a nested cluster, prefixing with the location of the parent element (recursively).
                """
                result = ''
                ecf_config_path = os.path.dirname(os.path.abspath(str(node)))

                for token in ecf_environment_variable_regex.findall(element.attributes['location'].value):
                        if token[0] <> r'$':
                                result += token
                        elif token == r'$|':
                                result += element_location(element.parentNode) + '/'
                        elif token == r'$ECF_CONFIG_PATH' or token == r'$(ECF_CONFIG_PATH)':
                                result += ecf_config_path
                        else:
                                s = environment_variable(env, token)

                                if s:
                                        result += s
                                else:
                                        print '****** WARNING!', str(node), 'uses undefined environment variable', token

                result = result.replace('\\', '/')

                if not os.path.isabs(result):
                        result = os.path.join(ecf_config_path, result)

                return result

        result = []
        ecf_as_xml = xml.dom.minidom.parse(str(node))

        for tag in ['cluster', 'override', 'tests', 'library', 'assembly', 'external_include', 'external_object']:
                for element in ecf_as_xml.getElementsByTagName(tag):
                        location = element_location(element)

                        if os.path.isfile(location):
                                result += [location]
                        elif tag == 'external_include':
                                result += env.Glob(location + '/*.h') + env.Glob(location + '/*.hpp')
                        elif element.attributes.get('recursive', None):
                                result += classes_in_cluster(env, location)
                        else:
                                result += env.Glob(location + '/*.e')

        return result

def ecf_target(target, source = None, env = None):
        """The ECF target corresponding to the given build target."""
        return os.path.basename(dirname(str(target[0]), 2))

def generate(env):
        """Add a Builder and construction variables for Eiffel to the given Environment."""
        default_ec_path = env.WhereIs('ec')

        if not default_ec_path:
                default_ec_path = spec_path(env, 'studio', 'bin/ec')
                if default_ec_path == '': default_ec_path = 'ec'

        vars = Variables()
        vars.Add('EC', "The Eiffel command-line compiler.", default_ec_path)
        vars.Add('ECFLAGS', "Use ec -help to see possible options.", '-finalize -clean -c_compile')
        vars.Add('ECLOG', "File to log Eiffel compiler output.", 'SCons.Eiffel.log')
        vars.Update(env)
        Help(vars.GenerateHelpText(env))

        env['BUILDERS']['Eiffel'] = Builder(action = Action(ec_action, ecf_target), emitter = ec_emitter, target_factory = Entry)
        env.Append(SCANNERS = Scanner(ecf_scanner, skeys = ['.ecf']))
        env.AddMethod(environment_variable, "EiffelEnvironmentVariable")
        env.AddMethod(classes_in_cluster, "EiffelClassesInCluster")
        env.AddMethod(spec_path, "EiffelSpecPath")

        for v in ['ISE_EIFFEL', 'ISE_PLATFORM', 'ISE_C_COMPILER']:
                if not environment_variable(env, v):
                        print '****** WARNING! Undefined Eiffel environment variable ' + v + '.'

def exists(env):
        """Is the Eiffel compiler available?"""
        return env.Detect(env['EC'])

# Utility functions.

def environment_variable(env, var):
        """
        The value of the environment variable 'var' within 'env'.
        If undefined and it is one of the standard EiffelStudio variables, a sensible platform-specific assumption is used; else None.
        """
        result = None
        var = var.lstrip('$').lstrip('(').rstrip(')')

        if env['ENV'].has_key(var):
                result = env['ENV'][var]
        elif var == 'ISE_PLATFORM':
                if env['PLATFORM'] == 'win32':
                        result = 'windows'
                elif env['PLATFORM'] == 'darwin':
                        result = 'macosx-x86'
                else:
                        result = 'linux-x86'
        elif var == 'ISE_C_COMPILER':
                if env['PLATFORM'] == 'win32':
                        result = 'msc'
                else:
                        result = 'gcc'
        elif var == 'ISE_EIFFEL':
                if env.has_key('EC'): result = env.WhereIs(env['EC'])
                if result: result = os.path.abspath(dirname(result, 5))
        elif var == 'ISE_LIBRARY':
                result = environment_variable(env, 'ISE_EIFFEL')

        return result

def classes_in_cluster(env, cluster):
        """All Eiffel class files in the given cluster and its subclusters."""
        result = []

        for root, dirnames, filenames in os.walk(cluster):
                if '.svn' in dirnames: dirnames.remove('.svn')
                result += env.Glob(root + '/*.e')

        return result

def spec_path(env, mid_part, tail):
        """
        A platform-dependent path in the EiffelStudio installation directory of the form:
        $ISE_EIFFEL + mid_part + '/spec/' + $ISE_PLATFORM + '/' + tail
        If either of these environment variables is undefined, then the result is an empty string.
        """
        result = ''
        ise_eiffel = environment_variable(env, 'ISE_EIFFEL')
        ise_platform = environment_variable(env, 'ISE_PLATFORM')

        if ise_eiffel and ise_platform:
                result = os.path.join(ise_eiffel, mid_part)
                result = os.path.join(result, 'spec')
                result = os.path.join(result, ise_platform)
                result = os.path.join(result, tail)
                result = os.path.abspath(result)

        return result

def dirname(path, n):
        """The directory name of 'path', called recursively 'n' times."""
        result = path
        if n > 0: result = dirname(os.path.dirname(path), n - 1)
        return result

```

### Possible Enhancements

The builder should define **ECCOM** and **ECCOMSTR** to support that common idiom. 

On Windows, if one of the ISE_* environment variables is not defined then EiffelStudio looks for it in the registry. The Scanner could simulate this better by likewise looking at the registry. The trouble with this approach (apart from the added complexity) is that it might easily break if EiffelStudio's use of the registry changes in future versions. 

When doing a .NET build, the Scanner prints a warning that **$ISE_DOTNET_FRAMEWORK** is undefined. This is the directory containing .NET framework assemblies. We would not normally expect the environment variable to be defined, so it would be good to suppress the warning, unless a reliable way can be found to guess at its value. 

The Scanner scans all of the dependencies that the `.ecf` mentions, blindly ignoring any targets or conditions specified in the `.ecf`. This can cause unnecessary nodes in the dependency list. 

* Conditional scanning would require handling the various cases that EiffelStudio itself handles. This would be complicated and error-prone, so it may be best not even to try this one! 
* A dependency may be declared only for a particular target in the `.ecf`. There a couple of ways that target-specific scanning might be achieved: 
      * One option would be passing the target to the Scanner. A few ideas for doing this: 
            * Perhaps the `Builder()` keyword argument `target_scanner` could be used. 
            * Perhaps the `Scanner()` keyword argument `path_function` could be abused. 
            * Perhaps the emitter might add the target to `Node.attributes`, for the Scanner to retrieve. 
      * Probably a cleaner option would be to remove the Scanner altogether, instead adding the dependencies to the `sources` list in the emitter. This would also be more efficient, because the `.ecf` file would be parsed only once, not twice. 

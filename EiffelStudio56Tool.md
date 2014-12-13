

# SCons and EiffelStudio 5.6

This is a SCons tool for building [EiffelStudio 5.6](http://www.eiffel.com) projects. It's superseded by [EiffelStudioTool](EiffelStudioTool), which builds current versions of [EiffelStudio](http://www.eiffel.com). It has been tested on Windows XP and 2003, and on Mac OS X 10.4.7. 

Put the builder in a script called _Eiffel.py_, in a directory that you reference with _toolpath_, as shown in the example below. 

It requires Python 2.4 or above, because it uses the _subprocess_ module which was new in Python 2.4. 

It does not attempt to scan the Eiffel project's Ace configuration file to figure out dependencies. This means that, if you modify an Eiffel class, this tool will not know that it needs to rebuild the project. It should be fairly easy to writer a Scanner to do this, but I won't bother because [EiffelStudio 5.7](http://eiffelsoftware.origo.ethz.ch/index.php/EiffelStudio_5.7_Releases) has replaced Eiffel's venerable Ace files with a completely new XML-based ECF file format. So, after editing some classes, you need to run SCons with the -c option to clean the targets before doing a rebuild. Alternatively, you can explicitly build the list of dependencies yourself, using classes_in_cluster(), as in the following example. 


### Example Usage


```python
#!python
# This example assumes that Eiffel.py is in the same directory as the SConstruct.

import os
from Eiffel import classes_in_cluster
env = Environment(ENV = os.environ, tools = ['Eiffel'], toolpath = ['.'])

# Build a precompiled library for the Gobo clusters.
gobo = Alias('gobo', env.Eiffel('gobo/precomp', 'gobo.ace'))

# Build some applications that depend on the gobo precompiled library.
# Each application will be built under the same directory containing its Ace file.
# If finalizing, install them into "/InstallDir".
for name, ace, classes in [
        ['app1', 'app1/app1.ace', classes_in_cluster('app1')],
        ['app2', 'app2/app2.ace', classes_in_cluster('app2')]
]:
        target = env.Eiffel(name, [ace, gobo] + classes)
        Default(target)
        Alias(name, target)
        if len(target) > 2: Install('/InstallDir', target[2])
```

### Builder


```python
#!python
# EiffelStudio 5.6 support for SCons
# Written by Peter Gummer, July 2006
# Amended by Peter Gummer, December 2006

"""
Tool-specific initialisation for EiffelStudio 5.6.
This probably also works with earlier versions of EiffelStudio.
"""

import os, glob, sys, shutil, datetime, subprocess, SCons
        
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

def log_process(args, working_directory):
        commandline = subprocess.list2cmdline(args)
        if log_file != sys.stdout: print '  ' + commandline
        log(commandline)
        log_file.flush()
        return subprocess.call(args, cwd = working_directory, stdout = log_file, stderr = subprocess.STDOUT)

def ec_string(target, source, env):
        return env['ECFLAGS'] + ' ' + os.path.basename(str(target[0]))

def ec(target, source, env):
        """
        Function to be used as the Eiffel Builder's action.
        Build target[0] (the Eiffel project file) and target[1] (the workbench executable) from source[0] (the Ace file).
        Also build target[2] (the finalised executable) if specified.
        All compiler output is logged to a file.
        Note that ec's return code is unreliable: it returns 0 if C compilation fails.
        We return 0 (success) if target[1] (the workbench executable) is built.
        """
        result = 0
        epr = str(target[0])
        exe = str(target[1])
        ace = os.path.abspath(str(source[0]))
        project = os.path.abspath(os.path.dirname(epr))

        log_open(env)
        log('=================== ' + epr + ' ===================')
        log_date()

        shutil.rmtree(project + '/EIFGEN')

        command = ['ec', '-batch', '-ace', ace, '-project_path', project]
        if os.path.basename(epr) == 'precomp.epr': command += ['-precompile']
        log_process(command + env['ECFLAGS'].split() + ['-c_compile'], None)

        if len(target) > 2 and os.path.exists(os.path.dirname(exe)):
                log('--------------------------')
                log_date()
                log_process(['finish_freezing', '-silent'], os.path.dirname(exe))

        if not os.path.exists(exe):
                if log_file != sys.stdout:
                        if log_file.tell() > 1000:
                                log_file.seek(-1000, 1)
                        else:
                                log_file.seek(0)

                        print '... ' + log_file.read()
                        log_file.seek(0, 2)

                subprocess.Popen(['estudio', '-create', project, '-ace', ace])
                result = 1

        if log_file != sys.stdout: log_file.close()
        return result

def ace_to_epr(target, source, env):
        """
        Function to be used as the Eiffel Builder's emitter.
        Parameters:
        1. target[0]: the name of the executable (application or dll) produced by the Eiffel project.
        2. target[1]: the Eiffel project directory. This parameter is optional.
        2. source[0]: the Ace file. If target[1] is not given, this also gives the Eiffel project directory.
        3. Additional source items optionally specify other dependencies, e.g. a precompiled library.
        The result specifies the target and source that will be passed to ec():
        1. Result target[0]: the given project's .epr file, with a directory part.
        2. Result target[1]: the workbench executable target to be built ("driver" if precompiling).
        3. Result target[2]: if finalising and not precompiling, the finalised executable target.
        4. Result source[0]: the given Ace file.
        5. Additional given source items, if any.
        Note: the "driver" executable does not exist for .NET precompiled libraries, so it probably doesn't work.
        """
        result = None, source
        exe = str(target[0])
        epr = os.path.splitext(exe)[0] + '.epr'

        if len(source) == 0:
                print 'No source .ace file specified: cannot build ' + exe
        elif not env.Detect('ec'):
                print 'Please add "ec" to your path: cannot build ' + exe
        else:
                is_precompiling = epr == 'precomp.epr'
                if is_precompiling: exe = env['ISE_C_COMPILER'] + '/driver' + env['PROGSUFFIX']

                project_dir = os.path.dirname(str(source[0]))
                if len(target) > 1: project_dir = str(target[1])

                epr = project_dir + '/' + epr
                exe = project_dir + '/EIFGEN/?_code/' + exe
                result = [epr, exe.replace('?', 'W')]

                if '-finalize' in env['ECFLAGS'] and not is_precompiling:
                        result += [exe.replace('?', 'F')]

                result = result, source

        return result

def c_compiler(env):
        """
        The given Environment's ISE_C_COMPILER variable, if set.
        The Microsoft compiler is the default because ISE_C_COMPILER is normally set on all platforms but Windows.
        """
        if env['ENV'].has_key('ISE_C_COMPILER'):
                return env['ENV']['ISE_C_COMPILER']
        else:
                return 'msc'

def generate(env):
        """Add a Builder and options for Eiffel to the given Environment."""
        opts = SCons.Script.Options()
        opts.Add('ECFLAGS', '"-freeze" for a workbench build.', '-finalize')
        opts.Add('ECLOG', 'File to log Eiffel compiler output.', 'SCons.Eiffel.log')
        opts.Add('ISE_C_COMPILER', 'msc = Microsoft, bcc = Borland, etc.', c_compiler(env))
        opts.Update(env)
        SCons.Script.Help(opts.GenerateHelpText(env))

        ec_action = SCons.Script.Action(ec, ec_string)
        env['BUILDERS']['Eiffel'] = SCons.Script.Builder(action = ec_action, emitter = ace_to_epr, suffix = env['PROGSUFFIX'])

def exists(env):
        """Is the Eiffel compiler available?"""
        return env.Detect('ec')

# Utility functions.

def files(pattern):
        """All files matching a pattern, excluding directories."""
        return [file for file in glob.glob(pattern) if os.path.isfile(file)]

def classes_in_cluster(cluster):
        """All Eiffel class files in the given cluster and its subclusters."""
        result = []

        for root, dirnames, filenames in os.walk(cluster):
                if '.svn' in dirnames: dirnames.remove('.svn')
                result += files(root + '/*.e')

        return result
```
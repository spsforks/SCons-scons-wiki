**Here are some tips for using SCons with Mac OS X. **

**Table of Contents**

[TOC]



# Building Dynamic Libraries

Just use [SharedLibrary](SharedLibrary) as always if you use scons later than 0.96.91.  Otherwise you need to do something like this: 


```python
#!python 
env['SHLINKFLAGS'] = '$LINKFLAGS -dynamic'
env['SHLIBSUFFIX'] = '.dylib'
```

# Building Dynamic Plugins

MacOSX makes big difference on dynamic libs and bundles (plugins). Use [LoadableModule](LoadableModule) builder if you use scons later than 0.96.91. Otherwise you could do something like this to enable Plugins: 


```python
#!python 
def XmmsPlugin(self,target,source):
    self['SHLINKFLAGS'] = '$LINKFLAGS -bundle -flat_namespace -undefined suppress'
    self['SHLIBSUFFIX'] = '.so'
    self.SharedLibrary(target, source)
```

# Creating Bundles

A Bundle is OSX's understanding of an application. It's a directory tree of many individual parts, each with a particular use. For instance, the Info.plist file, the icon, resources, [PkgInfo](PkgInfo), the executable(s), and so on. 

Gary Oberbrunner posted this tool on the users mailing list to help with Bundle creation. There are a few references like 'SCons.Node.Python.Value' in here because I import this into my SConscripts, so it doesn't have regular access to all the scons stuff. If you're putting it directly in your SConstruct/script, you could just say Value(). (Note: as of scons 0.97, you can just say 'from SCons.Script import *'.) 


```python
#!python 
from SCons.Defaults import SharedCheck, ProgScan
from SCons.Script.SConscript import SConsEnvironment

def TOOL_BUNDLE(env):
    """defines env.LinkBundle() for linking bundles on Darwin/OSX, and
       env.MakeBundle() for installing a bundle into its dir.
       A bundle has this structure: (filenames are case SENSITIVE)
       sapphire.bundle/
         Contents/
           Info.plist (an XML key->value database; defined by BUNDLE_INFO_PLIST)
           PkgInfo (trivially short; defined by value of BUNDLE_PKGINFO)
           MacOS/
             executable (the executable or shared lib, linked with Bundle())
    Resources/
         """
    if 'BUNDLE' in env['TOOLS']: return
    if platform == 'darwin':
        if tools_verbose:
            print " running tool: TOOL_BUNDLE"
        env.Append(TOOLS = 'BUNDLE')
        # This is like the regular linker, but uses different vars.
        # XXX: NOTE: this may be out of date now, scons 0.96.91 has some bundle linker stuff built in.
        # Check the docs before using this.
        LinkBundle = SCons.Builder.Builder(action=[SharedCheck, "$BUNDLECOM"],
                                           emitter="$SHLIBEMITTER",
                                           prefix = '$BUNDLEPREFIX',
                                           suffix = '$BUNDLESUFFIX',
                                           target_scanner = ProgScan,
                                           src_suffix = '$BUNDLESUFFIX',
                                           src_builder = 'SharedObject')
        env['BUILDERS']['LinkBundle'] = LinkBundle
        env['BUNDLEEMITTER'] = None
        env['BUNDLEPREFIX'] = ''
        env['BUNDLESUFFIX'] = ''
        env['BUNDLEDIRSUFFIX'] = '.bundle'
        env['FRAMEWORKS'] = ['-framework Carbon', '-framework System']
        env['BUNDLE'] = '$SHLINK'
        env['BUNDLEFLAGS'] = ' -bundle'
        env['BUNDLECOM'] = '$BUNDLE $BUNDLEFLAGS -o ${TARGET} $SOURCES $_LIBDIRFLAGS $_LIBFLAGS $FRAMEWORKS'
        # This requires some other tools:
        TOOL_WRITE_VAL(env)
        TOOL_SUBST(env)
        # Common type codes are BNDL for generic bundle and APPL for application.
        def MakeBundle(env, bundledir, app,
                       key, info_plist,
                       typecode='BNDL', creator='SapP',
                       icon_file='#macosx-install/sapphire-icon.icns',
                       subst_dict=None,
                       resources=[]):
            """Install a bundle into its dir, in the proper format"""
            # Substitute construction vars:
            for a in [bundledir, key, info_plist, icon_file, typecode, creator]:
                a = env.subst(a)
            if SCons.Util.is_List(app):
                app = app[0]
            if SCons.Util.is_String(app):
                app = env.subst(app)
                appbase = basename(app)
            else:
                appbase = basename(str(app))
            if not ('.' in bundledir):
                bundledir += '.$BUNDLEDIRSUFFIX'
            bundledir = env.subst(bundledir) # substitute again
            suffix=bundledir[bundledir.rfind('.'):]
            if (suffix=='.app' and typecode != 'APPL' or
                suffix!='.app' and typecode == 'APPL'):
                raise Error, "MakeBundle: inconsistent dir suffix %s and type code %s: app bundles should end with .app and type code APPL."%(suffix, typecode)
            if subst_dict is None:
                subst_dict={'%SHORTVERSION%': '$VERSION_NUM',
                            '%LONGVERSION%': '$VERSION_NAME',
                            '%YEAR%': '$COMPILE_YEAR',
                            '%BUNDLE_EXECUTABLE%': appbase,
                            '%ICONFILE%': basename(icon_file),
                            '%CREATOR%': creator,
                            '%TYPE%': typecode,
                            '%BUNDLE_KEY%': key}
            env.Install(bundledir+'/Contents/MacOS', app)
            f=env.SubstInFile(bundledir+'/Contents/Info.plist', info_plist,
                            SUBST_DICT=subst_dict)
            env.Depends(f,SCons.Node.Python.Value(key+creator+typecode+env['VERSION_NUM']+env['VERSION_NAME']))
            env.WriteVal(target=bundledir+'/Contents/PkgInfo',
                         source=SCons.Node.Python.Value(typecode+creator))
            resources.append(icon_file)
            for r in resources:
                if SCons.Util.is_List(r):
                    env.InstallAs(join(bundledir+'/Contents/Resources',
                                               r[1]),
                                  r[0])
                else:
                    env.Install(bundledir+'/Contents/Resources', r)
            return [ SCons.Node.FS.default_fs.Dir(bundledir) ]
        # This is not a regular Builder; it's a wrapper function.
        # So just make it available as a method of Environment.
        SConsEnvironment.MakeBundle = MakeBundle

def TOOL_WRITE_VAL(env):
    if tools_verbose:
        print " running tool: TOOL_WRITE_VAL"
    env.Append(TOOLS = 'WRITE_VAL')
    def write_val(target, source, env):
        """Write the contents of the first source into the target.
        source is usually a Value() node, but could be a file."""
        f = open(str(target[0]), 'wb')
        f.write(source[0].get_contents())
        f.close()
    env['BUILDERS']['WriteVal'] = Builder(action=write_val)
```
Note: you will need TOOL_SUBST from the wiki page [SubstInFileBuilder](SubstInFileBuilder). 

With a few small changes I was able to convert the above into an importable module which lets you define more than one application bundle per build tree.  The result is at [SconsMacV2](SconsMacV2). 

* -- [MitchChapman](MitchChapman) 

# Compiling Objective C / Objective C++ files

As of version 0.96.90, Objective C / Objective C++ support is built in to SCons. The expected file suffixes are '.m' for Objective C; '.mm' for Objective C++. 


# Packaging using pkg and disk images

OK, this is way incomplete, but here's something that might help. I haven't toolified any of this yet, it's just inline in my SConscript. 


```python
#!python 
    ...
    type='pmkr'
    creator='pkg1'
    pkgdir='Pkg' # dest dir where the .pkg dir will go
    srcdir='PrePkg' # src dir where all the stuff for the package lives
    pkgname=splitext(basename(SrcDirPath(pkgdir)))[0]
    env.Command(target=[join(pkgdir,"Contents/Archive.pax.gz"),
                        join(pkgdir,"Contents/Archive.bom")],
                source=srcdir,
                action=["(cd ${SOURCE} ; /Developer/Tools/SplitForks . ; pax -w -x cpio . ) | gzip -9 > $TARGET",
                        "mkbom $SOURCE ${TARGETS[1]}"])
    env.WriteVal(target=join(pkgdir, 'Contents/PkgInfo'),
                 source=SCons.Node.Python.Value(type+creator))
    # CUSTOMIZE THIS PART:
    v=float(env['VERSION_NUM'])
    subst_dict={'%SHORTVERSION%': '$VERSION_NUM',
                '%LONGVERSION%': 'This is my product, version $VERSION_NAME',
                '%PRODUCT%': 'MyProduct version $VERSION_NAME',
                '%MAJOR_VERSION%': str(int(v)),
                '%MINOR_VERSION%': str(int((v - int(v)) * 1000)),
                '%YEAR%': '$COMPILE_YEAR',
                '%CREATOR%': creator,
                '%TYPE%': type,
                '%DESTDIR_TOP%': '/Applications/MyAppTopDir',
                '%BUNDLE_KEY%': 'com.example.something',
                '%BUNDLE_NAME%': 'Super App',
                }
    env.SubstInFile(join(pkgdir,'Contents','Info.plist'),
                    join('resources','Info.plist.in'),
                    SUBST_DICT=subst_dict)
```
that more or less works for me, creating a .pkg dir. Then just make a disk image and ship it! :) 


# Installing Mac Created Bundles

The regular env.Install will not work to install Mac bundles since they are directories.  Here's a way to send the output of a env.[MakeBundle](MakeBundle) to this new env.[InstallBundle](InstallBundle). 

EDITED 2/6/06 gary o: This is not a good way to do it.  Using glob() only finds files that already exist when the SCons files are read, not ones that will be built.  See [BuildDirGlob](BuildDirGlob) for better ways to glob over Nodes. 


```python
#!python 
def ensureWritable(nodes):
    for node in nodes:
        if exists(node.path) and not (stat(node.path)[0] & 0200):
           chmod(node.path, 0777)
    return nodes

# Copy given patterns from inDir to outDir
def DFS(root, skip_symlinks = 1):
    """Depth first search traversal of directory structure.  Children
    are visited in alphabetical order."""
    stack = [root]
    visited = {}
    while stack:
        d = stack.pop()
        if d not in visited:  ## just to prevent any possible recursive
                              ## loops
            visited[d] = 1
            yield d
        stack.extend(subdirs(d, skip_symlinks))

def subdirs(root, skip_symlinks = 1):
    """Given a root directory, returns the first-level subdirectories."""
    try:
        dirs = [join(root, x) for x in listdir(root)]
        dirs = filter(isdir, dirs)
        if skip_symlinks:
            dirs = filter(lambda x: not islink(x), dirs)
        dirs.sort()
        return dirs
    except OSError, IOError: return []

def copyFiles (env, outDir, inDir):
    inDirNode = env.Dir(inDir)
    outDirNode = env.Dir(outDir)
    subdirs = DFS (inDirNode.name)
    files = []
    for subdir in subdirs:
        files += glob.glob (join (subdir, '*'))
    outputs = []
    for f in files:
        if isfile (f):
            outputs += ensureWritable (env.InstallAs (outDirNode.abspath + '/' + f, env.File (f)))
    return outputs

def InstallBundle (env, target_dir, bundle):
    """Move a Mac OS-X bundle to its final destination"""
    # check parameters!
    if exists(target_dir) and not isdir (target_dir):
        raise SCons.Errors.UserError, "InstallBundle: %s needs to be a directory!"%(target_dir)
    bundledirs = env.arg2nodes (bundle, env.fs.File)
    outputs = []
    for bundledir in bundledirs:
        suffix = bundledir.name [bundledir.name.rfind ('.'):]
        if (exists(bundledir.name) and not isdir (bundledir.name)) or suffix != '.app':
            raise SCons.Errors.UserError, "InstallBundle: %s needs to be a directory with a .app suffix!"%(bundledir.name)
    # copy all of them to the target dir
        outputs += env.copyFiles (target_dir, bundledir)
    return outputs
```
To use it, try the following: 


```python
#!python 
    prog = env.Program (program, objs + other_objects,
                        LIBS = libs + env ['EXTRA_LIBS'],
                        LIBPATH = libpaths + env ['SDDAS_LIB'])
    env.Default (prog)
    if env ['PLATFORM'] == "darwin" and isNativeOnMac:    # I pass in a boolean telling me that
                                                          # the program is a real Mac app, not a
                                                          # X11 thing or regular command line exe.
       env ['VERSION_NAME'] = program + '.app'
       env.Append (LINKFLAGS = ['-framework', 'Carbon'])  # This is not needed in newer versions of SCons
       bundle = env.MakeBundle (program + '.app', program,
                                'com.SwRI.' + program,    # this key is some sort of Mac-ism,
                                                          # java style, can be anything?
                                'Info.plist',             # Info.plist is an XML thing made with
                                                          # Property List Editor
                                'APPL',                   # tells SCons this is an application
                                'SwRI',                   # Creator code, can be anything?
                                '#/MAC_ICONS/' + program + '.icns')  # Icon for the program
       env.Default (bundle)
       inst = env.InstallBundle (env ['SDDAS_BIN'], bundle)   # env ['SDDAS_BIN'] is the target directory
    else:
       inst = env.Install (dir=env ['SDDAS_BIN'], source=prog)
       env.AddPostAction (inst, env.Action ('strip $TARGET'))
```
4) When you do an "scons install" (or whatever your alias to do the install), it will install the program in the right place. 


# Copying files with resource forks

_ **Note** that as of OS X, resource forks are deprecated and rarely used nowadays; so unless you develop for legacy support, this section should not be relevant._ 

Python, as of 2.3 I believe, comes with a macostools extension module that has a copy function that deals with resource forks. However, the parameter list is a bit different than what SCons expects for Install, so a small wrapper method is needed. 


```python
#!python 
def osx_copy( dest, source, env ):
    from macostools import copy
    copy( source, dest )
```
Remember to set the INSTALL variable for your environment: 


```python
#!python 
env['INSTALL'] = osx_copy
```
Update: I actually get permission denied errors when trying to open the copied executables. Can anyone else confirm this erroneous behavior? 

* -- [MichaelKoehmstedt](MichaelKoehmstedt) 
On Mac OS X, you sometimes have to build files with resource forks. Installing them the usual way with env.Install() won't work, because env.Install() uses cp by default, which doesn't copy resource forks. 

Fortunately env.Install() actually calls whatever python function is in env['INSTALL'], so you can replace it like this: 


```python
#!python 
import os, os.path, shutil
def copyFunc_with_resources(dest, source, env):
    """Install a source file into a destination by copying it (and its
    permission/mode bits, AND MAC RESOURCE STUFF)."""
    st = os.stat(source)
    if sys.platform == 'darwin' and os.path.exists('/Developer/Tools/CpMac'):
       if os.path.dirname(str(dest)) and \
              not os.path.exists(os.path.dirname(str(dest))):
           os.makedirs(os.path.dirname(str(dest)))
       cmd='/Developer/Tools/CpMac "%s" "%s"'%(str(source), str(dest))
       # print "(Using Dev Tools to copy: cmd=%s)"%cmd
       os.system(cmd)
    else:
       shutil.copy2(source, dest)
    os.chmod(dest, stat.S_IMODE(st.st_mode) | stat.S_IWRITE)
    return 0
```
Then when you're creating your environment, do something like this: 


```python
#!python 
env['INSTALL'] = copyFunc_with_resources
```
Then Install() will copy resources. 

You could enhance this by checking whether dest/rsrc exists, and only use [CpMac](CpMac) in that case. dest/rsrc is one way to get to the resource fork of a file; the syntax refers to the file as if it were a directory so it's a little unusual, but it does work. 


# Get absolute path name in error messages (for XCode integration)

If you use SCons as external build tool within an XCode 3.2 through at least 4.5 project, then the parsing of error messages is broken, because XCode expects absolute path names, while SCons calls the C/C++ compiler with relative path names.  Some modifications and intervention is possible so that compiler errors generated through XCode are 'clickable' and browse to the correct source code location.  GCC formats the output in the same way that source files are specified. Therefore, we need to change the way SCons calls the compiler such that it usese absolute path names to source code: 


```txt
  env['CXXCOM'] = string.replace(env['CXXCOM'], '$SOURCES', '${SOURCES.abspath}')
  env['CCCOM']  = string.replace(env['CCCOM'],  '$SOURCES', '${SOURCES.abspath}')
```
This overrides the default C and C++ compiler action and calls the compiler with absolute path names through the ${SOURCES.abspath} syntax. 

The above will fix error reporting for source code directly compiled.  It will not fix errors from incuded files ( .h header files ), because the GCC compiler will still report relative paths for those errors.  The solution is to call scons through a script that will do stream processing on the stderr output, replacing relative path names to absolute paths. 

Here is one such method: 


```txt
#!/bin/bash
#!/bin/bash
# Call this build_script from XCode as 'external build system'
# Macro Definitions:
# $SCONS_EXEC : path to scons command
# $SOURCE_DIR : base path to project source
# $1          : argument passed to script from XCode, i.e. build target

cd $SOURCE_DIR

( $SCONS_EXEC $1 ) 2> >( sed -E "s|^([^/][a-zA-Z/_]+\.h)|$SOURCE_DIR/\1|;s| ([^/][a-zA-Z/_]+\.h)| $SOURCE_DIR/\1|g" >&2 )

# This passes the stderr output from scons (and GCC) through sed to change identified relative path .h files to absolute path.  Note the filename matching criteria [a-zA-Z/_] may need some modification for special characters / numbers in filename.
```

# Generating Xcode project files

The [scons-xcode package](https://bitbucket.org/al45tair/scons-xcode) can generate Xcode project files that work by running SCons.  Once installed, all you need is to add a call to `env.XcodeProject` to your SConstruct file, for instance:

```
env = Environment(tools=['default', 'Xcode'])

myprog = env.Program('build/MyProg', ['src/main.cc'])

env.XcodeProject('MyProject.xcodeproj',
                 products=myprog)
```

See [the project page](https://bitbucket.org/al45tair/scons-xcode) for more information and installation instructions.
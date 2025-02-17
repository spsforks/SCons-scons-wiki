

# Installer

This page describes a minimal installer which tries to mimic autoconf.  It adds the following options to your SConstruct: 

* `prefix` 
* `eprefix` 
* `bindir` 
* `libdir` 
* `includedir` 

## The module

The following code can be saved in a file named `installer.py` : 


```python
#!python

""" installer

This module defines a minimal installer for scons build scripts.  It is aimed
at *nix like systems, but I guess it could easily be adapted to other ones as
well.
"""

import fnmatch, os, os.path
import SCons.Defaults

PREFIX = "prefix"
EPREFIX = "eprefix"
BINDIR = "bindir"
LIBDIR = "libdir"
INCLUDEDIR = "includedir"

def AddOptions( opts ):
        """ Adds the installer options to the opts.  """
        opts.Add( PREFIX, "Directory of architecture independant files.", "/usr" )
        opts.Add( EPREFIX, "Directory of architecture dependant files.", "${%s}" % PREFIX )
        opts.Add( BINDIR, "Directory of executables.", "${%s}/bin" % EPREFIX )
        opts.Add( LIBDIR, "Directory of libraries.", "${%s}/lib" % EPREFIX )
        opts.Add( INCLUDEDIR, "Directory of header files.", "${%s}/include" % PREFIX )


class Installer:
    """ A basic installer. """
    def __init__( self, env ):
        """ Initialize the installer.

        @param configuration A dictionary containing the configuration.
        @param env The installation environment.
        """
        self._prefix = env.get( PREFIX, "/usr" )
        self._eprefix = env.get( EPREFIX, self._prefix )
        self._bindir = env.get( BINDIR, os.path.join( self._eprefix, "bin" ) )
        self._libdir = env.get( LIBDIR, os.path.join( self._eprefix, "lib" ) )
        self._includedir = env.get( INCLUDEDIR, os.path.join( self._prefix, "include" ) )
        self._env = env

    def Add( self, destdir, name, basedir="", perm=0644 ):
        destination = os.path.join( destdir, basedir )
        obj = self._env.Install( destination, name )
        self._env.Alias( "install", destination )
        for i in obj:
            self._env.AddPostAction( i, SCons.Defaults.Chmod( str(i), perm ) )

    def AddProgram( self, program ):
        """ Install a program.

        @param program The program to install.
        """
        self.Add( self._bindir, program, perm=0755 )

    def AddLibrary( self, library ):
        """ Install a library.

        @param library the library to install.
        """
        self.Add( self._libdir, library )

    def AddHeader( self, header, basedir="" ):
        self.Add( self._includedir, header, basedir )

    def AddHeaders( self, parent, pattern, basedir="", recursive=False ):
        """ Installs a set of headers.

        @param parent The parent directory of the headers.
        @param pattern A pattern to identify the files that are headers.
        @param basedir The subdirectory in which to install the headers.
        @param recursive Search recursively for headers.
        """
        for entry in os.listdir( parent ):
            entrypath = os.path.join( parent, entry )
            if os.path.isfile( entrypath ) and fnmatch.fnmatch( entry, pattern ):
                self.AddHeader( entrypath, basedir )
            elif os.path.isdir( entrypath ) and recursive:
                self.AddHeaders( entrypath, pattern, os.path.join( basedir, entry ), recursive )

```

## Using the installer

Once the `installer.py` file is in the SConstruct directory, it can be used like this: 


```python
#!python

import installer

env = Environment()
opts = Options( 'options.conf', ARGUMENTS )
# add your custom options here

# add the installer options
installer.AddOptions( opts )
opts.Update( env )
opts.Save( 'options.conf')
Help( opts.GenerateHelpText( env ) )

# create the installer
install = installer.Installer( env )

# adds a program to the installer
program = env.Program( your_program_options )
install.AddProgram( program )

# adds a library to the installer
lib = env.Library( your_library_options )
install.AddLibrary( lib )

# adds headers to the installer
install.AddHeaders( "path/to/headers", "*.hpp" )

```
You can now install your program in a custom location with a call to 


```txt
scons prefix=/home/sweet/usr install
```
and you can later uninstall with a call to: 


```txt
scons -c install
```

## Shortcomings

* A file named `.sconsign` is installed and never removed 
* The install path options must not change between install and uninstall 
* Library versions are not handled 
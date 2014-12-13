
MSVC compiler has a nice feature - if you build DLL, all symbols should be resolved. After googling for a few hours, I didn't find the necessary combination of GCC flags, to achieve same result for shared libraries. So I created a custom builder based on ldd and c++filt utilities, which dumps unresolved symbols to a text file. 

It is not the perfect solution, but it is good enough for me and may be it will be useful for you too. 

* As a side note: I had more luck with looking for such feature. Linker (at least on linux) has `--no-undefined` option which does exactly this. When you want to pass it to `gcc` or `g++` you have to use `-Wl,--no-undefined` to indicate that option has to be passed to linker. - Tomasz Gajewski 
The builder code: 


```python
#!python 

import os
import re
import subprocess
import SCons.Action
import SCons.Builder
import SCons.Scanner

class dependencies_dumper_t:
    unresolved_lib_re = re.compile( r'^\s+(?P<lib>.*)\s\=\>\snot found.*' )
    undefined_symbol_re = re.compile( r'^\s*undefined symbol\:\s+(?P<symbol>.*)\s\(.*\)' )

    def __init__( self, target, source, env ):
        self.env = env
        self.target = target
        self.source = source

        self.new_os_env = os.environ.copy()
        self.new_os_env['LD_LIBRARY_PATH'] = env['ENV']['LD_LIBRARY_PATH']
        #self.new_os_env['PATH'] = env.get( 'PATH', os.environ.get( 'PATH', '' ) )
        #todo?: may be I need to add source file directory to LD_LIBRARY_PATH

    def write2log( self, msg ):
        print msg

    def __run_ldd( self ):
        try:
            tf = file( self.target[0].abspath, 'w+r' )
            args = [ 'ldd', '-r', self.source[0].abspath ]
            ldd_prs = subprocess.Popen( ' '.join( args )
                                        , shell=True
                                        , close_fds=True
                                        , bufsize=1024*50
                                        , stdout=tf
                                        , stderr=tf
                                        , cwd=os.path.dirname( self.source[0].abspath )
                                        , env=self.new_os_env)

            ldd_prs.wait()

            if 0 != ldd_prs.returncode:
                raise RuntimeError( 'Error during execution of ldd process. Error code: %d'
                                    % ldd_prs.return_code )
            tf.seek(0)
            output = tf.read()
            tf.close()
            lines = output.split( '\n' )
            lines = map( lambda s: s.strip(), lines )
            return filter( None, lines )
        except Exception, err:
            print 'error executing ldd process: ', str(err)
            raise

    def __demangle_symbol( self, symbol ):
        try:
            tmp_f_name = os.path.join( self.env['AIS_B_CFG' ]['TEMP_PATH']
                                       , os.path.basename( self.source[0].abspath ) + '.cppfilt.txt' )
            tmp_f = file( self.env.File( tmp_f_name ).abspath, 'w+r' )
            args = [ 'c++filt', symbol ]
            prs = subprocess.Popen( ' '.join( args )
                                    , shell=True
                                    , close_fds=True
                                    , stdout=tmp_f
                                    , stderr=tmp_f )

            prs.wait()

            if 0 != prs.returncode:
                raise RuntimeError( 'Error during execution of c++filt process. Error code: %d'
                                    % prs.return_code )
            tmp_f.seek(0)
            output = tmp_f.read().strip()
            tmp_f.close()
            return '%s { %s }' % ( output, symbol )
        except Exception, err:
            print 'error executing c++filt process: ', str(err)
            return symbol

    def __list_unknown( self, ldd_result, pattern, gname ):
        unknown = []
        for l in ldd_result:
            m = pattern.match( l )
            if not m:
                continue
            unknown.append( m.group( gname ) )
        return unknown

    def dump(self):
        ldd_lines = self.__run_ldd()
        libs = self.__list_unknown( ldd_lines, self.unresolved_lib_re, 'lib' )
        symbols = self.__list_unknown( ldd_lines, self.undefined_symbol_re, 'symbol' )
        tf = file( self.target[0].abspath, 'w+' )
        if libs or symbols:
            tf.write( 'LD_LIBRARY_PATH:\n' )
            for path in self.new_os_env['LD_LIBRARY_PATH'].split(':'):
                tf.write( '\t' + path + '\n' )
            if libs:
                tf.write( 'unresolved libs: \n' )
                for lib in libs:
                    tf.write( '\t' + lib + '\n' )
            if symbols:
                tf.write( 'undefined symbols: \n' )
                for symbol in symbols:
                    tf.write( '\t' + self.__demangle_symbol( symbol ) + '\n' )
        tf.close()

def build_it( target, source, env ):
    """
    source - executable or shared object
    target - text file, which contains list of other shared libraries it
             depends on and list of undefined symbols. If there are no
             undefined symbols, the file will be empty

    LD_LIBRARY_PATH environment variable will be used to find out the location
    of other shared libraries

    PATH environment variable will be used to find out the location of 'ldd'
    executable
    """
    dependencies_dumper_t( target, source, env ).dump()
    return 0


def register_builder( env, name ):
    """"shared library dependencies builder scanner"""
    builder = env.Builder( action = SCons.Action.Action(build_it, "dumping dependencies '$TARGET'")
                           #target_factory - is a factory function that the Builder will use to turn 
                           #any targets specified as strings into SCons Nodes
                           , target_factory=env.fs.File )
    env.Append(BUILDERS={name: builder })

def exists(env):
    """the "combine" builder always exists"""
    return True 

```
Usage example: 


```python
#!python 

   import dependencies_builder

   env = Environment( ... )
   dependencies_builder.register_builder( env, 'DumpSODependencies' )


   library = env.SharedLibrary( ... )
   installed_lib = env.Install( ..., library )
   library_dependencies = installed_lib[0].abspath + '.txt'
   dependencies = env.DumpSODependencies( library_dependencies, library )
   env.SideEffect('#serialize_dependencies', dependencies)
   env.Alias(targetname, library_dependencies)
   env.AlwaysBuild( library_dependencies )

```
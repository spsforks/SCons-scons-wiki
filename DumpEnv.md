# Dumping the Construction Environment

There are times when it's very helpful to be able to see the contents of the construction environment. Most of the time, dumping the contents of the environment allows you to easily see what's going on inside with the tools being used. And that's a pretty handy task when debugging issues with scons. 

---

_**NOTE: **_since SCons 0.96.90, the code below is no longer needed.  Environments have a method 
[`Dump`](http://www.scons.org/doc/production/HTML/scons-user.html#f-Dump)
built-in.  Just call: 

```python
print env.Dump()  # dump whole env
print env.Dump('CCFLAGS') # dump just one key
```
But if you're using an older version of scons, read on... 

---
 
```python
def DumpEnv(env, key=None, header=None, footer=None):
    """
    Using the standard Python pretty printer, dump the contents of the
    scons build environment to stdout.

    If the key passed in is anything other than 'env', then that will
    be used as an index into the build environment dictionary and
    whatever is found there will be fed into the pretty printer. Note
    that this key is case sensitive.

    The header and footer are simple mechanisms to allow printing a
    prefix and suffix to the contents that are dumped out. They are
    handy when using DumpEnv to dump multiple portions of the
    environment.
    """
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    if key:
        mydict = env.Dictionary(key)
    else:
        mydict = env.Dictionary()
    if header:
        print header
    pp.pprint(mydict)
    if footer:
        print(footer)
```

# Using DumpEnv

Stick the `DumpEnv` function someplace easy to access, like in the SConstruct file and then call it. 


## Dumping the Entire Environment

Put: 


```python
DumpEnv(env)
```
in the SConstruct file. Then running scons will show something like: 


```console
scons: Reading SConscript files ...
{ 'AR': 'ar',
  'ARCOM': '$AR $ARFLAGS $TARGET $SOURCES\n$RANLIB $RANLIBFLAGS $TARGET',
  'ARFLAGS': 'r',
  'AS': 'as',
  'ASCOM': '$AS $ASFLAGS -o $TARGET $SOURCES',
  'ASFLAGS': '',
  'ASPPCOM': '$CC $ASFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS -c -o $TARGET $SOURCES',
  'BIBTEX': 'bibtex',
  'BIBTEXCOM': '$BIBTEX $BIBTEXFLAGS $SOURCES',
  'BIBTEXFLAGS': '',
  'BUILDERS': {'ExpandVersion': &lt;SCons.Builder.BuilderBase instance at 0x404890cc&gt;},
  'CC': 'gcc',
  'CCCOM': '$CC $CCFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS -c -o $TARGET $SOURCES',
  'CCFLAGS': '',
  'CFILESUFFIX': '.c',
  'CPPDEFPREFIX': '-D',
  'CPPDEFSUFFIX': '',
  'CVS': 'cvs',
  'CVSCOFLAGS': '',
  'CVSCOM': '$CVS $CVSFLAGS co $CVSCOFLAGS ${TARGET.posix}',
  'CVSFLAGS': '-d $CVSREPOSITORY',
  'CXX': 'g++',
  'CXXCOM': '$CXX $CXXFLAGS $CPPFLAGS $_CPPINCFLAGS -c -o $TARGET $SOURCES',
  'CXXFILESUFFIX': '.cc',
  'CXXFLAGS': '$CCFLAGS',
  'CXXVERSION': '3.2.2',
  'DEV': '/home/peterk/tmp/emitter',
  'DVIPDF': 'dvipdf',
  'DVIPDFCOM': '$DVIPDF $DVIPDFFLAGS $SOURCES $TARGET',
  'DVIPDFFLAGS': '',
  'DVIPS': 'dvips',
  'DVIPSFLAGS': '',
  'ENV': {'PATH': '/usr/local/bin:/bin:/usr/bin'},
  'ESCAPE': &lt;function escape at 0x4045fb1c&gt;,
  'F77': 'g77',
  'F77COM': '$F77 $F77FLAGS $_F77INCFLAGS -c -o $TARGET $SOURCES',
  'F77FLAGS': '',
  'F77PPCOM': '$F77 $F77FLAGS $CPPFLAGS $_CPPDEFFLAGS $_F77INCFLAGS -c -o $TARGET $SOURCES',
  'GS': 'gs',
  'GSCOM': '$GS $GSFLAGS -sOutputFile=$TARGET $SOURCES',
  'GSFLAGS': '-dNOPAUSE -dBATCH -sDEVICE=pdfwrite',
  'INCPREFIX': '-I',
  'INCSUFFIX': '',
  'INSTALL': &lt;function copyFunc at 0x4041c7d4&gt;,
  'JAR': 'jar',
  'JARCOM': '$JAR $_JARFLAGS $TARGET $_JARMANIFEST $_JARCHDIR $_JARSOURCES',
  'JARFLAGS': 'cf',
  'JARSUFFIX': '.jar',
  'JAVAC': 'javac',
  'JAVACCOM': '$JAVAC $JAVACFLAGS -d ${TARGET.attributes.java_classdir} -sourcepath ${SOURCE.dir.rdir()} $SOURCES',
  'JAVACFLAGS': '',
  'JAVACLASSSUFFIX': '.class',
  'JAVAH': 'javah',
  'JAVAHCOM': '$JAVAH $JAVAHFLAGS $_JAVAHOUTFLAG -classpath ${SOURCE.attributes.java_classdir} ${SOURCES.attributes.java_classname}',
  'JAVAHFLAGS': '',
  'JAVASUFFIX': '.java',
  'LATEX': 'latex',
  'LATEXCOM': '$LATEX $LATEXFLAGS $SOURCES',
  'LATEXFLAGS': '',
  'LEX': 'flex',
  'LEXCOM': '$LEX $LEXFLAGS -t $SOURCES &gt; $TARGET',
  'LEXFLAGS': '',
  'LIBDIRPREFIX': '-L',
  'LIBDIRSUFFIX': '',
  'LIBLINKPREFIX': '-l',
  'LIBLINKSUFFIX': '',
  'LIBPREFIX': 'lib',
  'LIBPREFIXES': '$LIBPREFIX',
  'LIBSUFFIX': '.a',
  'LIBSUFFIXES': ['$LIBSUFFIX', '$SHLIBSUFFIX'],
  'LINK': '$SMARTLINK',
  'LINKCOM': '$LINK $LINKFLAGS -o $TARGET $SOURCES $_LIBDIRFLAGS $_LIBFLAGS',
  'LINKFLAGS': '',
  'M4': 'm4',
  'M4COM': 'cd ${SOURCE.srcdir} &amp;&amp; $M4 $M4FLAGS &lt; ${SOURCE.file} &gt; ${TARGET.abspath}',
  'M4FLAGS': '-E',
  'OBJPREFIX': '',
  'OBJSUFFIX': '.o',
  'PDFCOM': '$DVIPDFCOM',
  'PDFLATEX': 'pdflatex',
  'PDFLATEXCOM': '$PDFLATEX $PDFLATEXFLAGS $SOURCES $TARGET',
  'PDFLATEXFLAGS': '',
  'PDFPREFIX': '',
  'PDFSUFFIX': '.pdf',
  'PDFTEX': 'pdftex',
  'PDFTEXCOM': '$PDFTEX $PDFTEXFLAGS $SOURCES $TARGET',
  'PDFTEXFLAGS': '',
  'PLATFORM': 'posix',
  'PROGPREFIX': '',
  'PROGSUFFIX': '',
  'PSCOM': '$DVIPS $DVIPSFLAGS -o $TARGET $SOURCES',
  'PSPAWN': &lt;function piped_env_spawn at 0x4045f95c&gt;,
  'PSPREFIX': '',
  'PSSUFFIX': '.ps',
  'RANLIB': 'ranlib',
  'RANLIBFLAGS': '',
  'RCS': 'rcs',
  'RCS_CO': 'co',
  'RCS_COCOM': '$RCS_CO $RCS_COFLAGS $TARGET',
  'RCS_COFLAGS': '',
  'RMIC': 'rmic',
  'RMICCOM': '$RMIC $RMICFLAGS -d ${TARGET.attributes.java_lookupdir} -classpath ${SOURCE.attributes.java_classdir} ${SOURCES.attributes.java_classname}',
  'RMICFLAGS': '',
  'SCANNERS': [ &lt;SCons.Scanner.ClassicCPP instance at 0x4041e8cc&gt;,
                &lt;SCons.Scanner.Classic instance at 0x4041e58c&gt;],
  'SHCC': '$CC',
  'SHCCCOM': '$SHCC $SHCCFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS -c -o $TARGET $SOURCES',
  'SHCCFLAGS': '$CCFLAGS -fPIC',
  'SHCXX': '$CXX',
  'SHCXXCOM': '$SHCXX $SHCXXFLAGS $CPPFLAGS $_CPPINCFLAGS -c -o $TARGET $SOURCES',
  'SHCXXFLAGS': '$CXXFLAGS -fPIC',
  'SHELL': 'sh',
  'SHF77': '$F77',
  'SHF77COM': '$SHF77 $SHF77FLAGS $_F77INCFLAGS -c -o $TARGET $SOURCES',
  'SHF77FLAGS': '$F77FLAGS',
  'SHF77PPCOM': '$SHF77 $SHF77FLAGS $CPPFLAGS $_CPPDEFFLAGS $_F77INCFLAGS -c -o $TARGET $SOURCES',
  'SHLIBEMITTER': None,
  'SHLIBPREFIX': '$LIBPREFIX',
  'SHLIBSUFFIX': '.so',
  'SHLINK': '$LINK',
  'SHLINKCOM': '$SHLINK $SHLINKFLAGS -o $TARGET $SOURCES $_LIBDIRFLAGS $_LIBFLAGS',
  'SHLINKFLAGS': '$LINKFLAGS -shared',
  'SHOBJPREFIX': '$OBJPREFIX',
  'SHOBJSUFFIX': '.os',
  'SMARTLINK': &lt;function smart_link at 0x4046f144&gt;,
  'SPAWN': &lt;function spawn_spawn at 0x4045f844&gt;,
  'STATIC_AND_SHARED_OBJECTS_ARE_THE_SAME': 0,
  'SWIG': 'swig',
  'SWIGCFILESUFFIX': '_wrap$CFILESUFFIX',
  'SWIGCOM': '$SWIG $SWIGFLAGS -o $TARGET $SOURCES',
  'SWIGCXXFILESUFFIX': '_wrap$CXXFILESUFFIX',
  'SWIGFLAGS': '',
  'TAR': 'tar',
  'TARCOM': '$TAR $TARFLAGS -f $TARGET $SOURCES',
  'TARFLAGS': '-c',
  'TARSUFFIX': '.tar',
  'TEMPFILE': &lt;class SCons.Defaults.NullCmdGenerator at 0x40414dac&gt;,
  'TEX': 'tex',
  'TEXCOM': '$TEX $TEXFLAGS $SOURCES',
  'TEXFLAGS': '',
  'TOOLS': [ 'default',
             'gnulink',
             'gcc',
             'g++',
             'g77',
             'gas',
             'ar',
             'CVS',
             'dvipdf',
             'dvips',
             'gs',
             'jar',
             'javac',
             'javah',
             'latex',
             'lex',
             'm4',
             'pdflatex',
             'pdftex',
             'RCS',
             'rmic',
             'swig',
             'tar',
             'tex',
             'yacc',
             'zip'],
  'YACC': 'bison',
  'YACCCOM': '$YACC $YACCFLAGS -o $TARGET $SOURCES',
  'YACCFLAGS': '',
  'ZIP': 'zip',
  'ZIPCOM': &lt;SCons.Action.FunctionAction instance at 0x404af5ec&gt;,
  'ZIPFLAGS': '',
  'ZIPSUFFIX': '.zip',
  '_CPPDEFFLAGS': '${_defines(CPPDEFPREFIX, CPPDEFINES, CPPDEFSUFFIX, __env__)}',
  '_CPPINCFLAGS': '$( ${_concat(INCPREFIX, CPPPATH, INCSUFFIX, __env__, RDirs)} $)',
  '_F77INCFLAGS': '$( ${_concat(INCPREFIX, F77PATH, INCSUFFIX, __env__, RDirs)} $)',
  '_JARCHDIR': &lt;function jarChdir at 0x4046ff0c&gt;,
  '_JARFLAGS': &lt;function jarFlags at 0x4046fed4&gt;,
  '_JARMANIFEST': &lt;function jarManifest at 0x4046fe9c&gt;,
  '_JARSOURCES': &lt;function jarSources at 0x4046faac&gt;,
  '_JAVAHOUTFLAG': &lt;function JavaHOutFlagGenerator at 0x40479764&gt;,
  '_LIBDIRFLAGS': '$( ${_concat(LIBDIRPREFIX, LIBPATH, LIBDIRSUFFIX, __env__, RDirs)} $)',
  '_LIBFLAGS': '${_stripixes(LIBLINKPREFIX, LIBS, LIBLINKSUFFIX, LIBPREFIX, LIBSUFFIX, __env__)}',
  '_concat': &lt;function _concat at 0x4041c844&gt;,
  '_defines': &lt;function _defines at 0x4041c8b4&gt;,
  '_stripixes': &lt;function _stripixes at 0x4041c87c&gt;}
scons: done reading SConscript files.
scons: Building targets ...
scons: `.' is up to date.
scons: done building targets.
```

## Dumping a Portion of the Environment


```python
DumpEnv(env, key='TOOLS')
```
Note that the key is case sensitive! Then running scons will show something like: 


```console
scons: Reading SConscript files ...
[ 'default',
  'gnulink',
  'gcc',
  'g++',
  'g77',
  'gas',
  'ar',
  'CVS',
  'dvipdf',
  'dvips',
  'gs',
  'jar',
  'javac',
  'javah',
  'latex',
  'lex',
  'm4',
  'pdflatex',
  'pdftex',
  'RCS',
  'rmic',
  'swig',
  'tar',
  'tex',
  'yacc',
  'zip']
scons: done reading SConscript files.
scons: Building targets ...
scons: `.' is up to date.
scons: done building targets.
```

## Optionally Calling DumpEnv

While it's handy to be able to peek into the environment, it can be annoying to dump the contents out every time. To get around that, add the following to the SConstruct file: 


```python
if 'dump' in ARGUMENTS:
    env_key = ARGUMENTS['dump']
    if env_key == 'env':
        prefix = 'env.Dictionary()'
        env_key = None
    else:
        prefix = 'env.Dictionary( ' + env_key + ' )'
    DumpEnv( env,
             key = env_key,
             header = prefix + ' - start',
             footer = prefix + ' - end' )
```
To dump the environment, you now have to specify an additional argument on the command line: 


```console
scons dump=env
```
Without the dump=env, the environment will not be written out. 

The contents of specific portions of the environment can also be specified. For example, to write out the contents of the TOOLS portion of the environment, use: 


```console
scons dump=TOOLS
```

## Passing Around DumpEnv

Sometimes, is would be nice to be able to dump the environment when in a SConscript file someplace in the bowels of a complex build hierarchy. The easiest way to do this is to modify the environment in the SConstruct file by adding the DumpEnv to it. 


```python
env[ 'DumpEnv' ] = DumpEnv
```
Then from within a SConscript file, use: 


```python
env[ 'DumpEnv' ]( env )
```
to dump the contents of the environment at that point. 

Another way to do this is to make Dump a method of the Environment class. Put this after your definition of DumpEnv: 


```python
from SCons.Script.SConscript import SConsEnvironment
SConsEnvironment.DumpEnv = DumpEnv
```
Then for _any_ environment you can do this in your SConscript: 


```python
env.DumpEnv()
# or
env.DumpEnv(key = 'TOOLS')
```
This requires scons 0.92 or later. 



## Autoconf recipes

Autoconf/automake macros provide a layer of portability that is currently not fully supported by scons. Here is a few autoconf-like functions that I use. I hope that others can fill more stuff in. 


### Examples

MKDIR_TAKES_ONE_ARG 


```txt
def checkMkdirOneArg(conf):
  check_mkdir_one_arg_source = """
#include <sys/stat.h>
int main()
{
  mkdir("somedir");
}
"""
  conf.Message('Checking for the number of args for mkdir... ')
  ret = conf.TryLink(check_mkdir_one_arg_source, '.c') or \
    conf.TryLink('#include <unistd.h>' + check_mkdir_one_arg_source, '.c')
  if ret:
    conf.Result('one')
  else:
    conf.Result('two')
  return ret
```
SELECT_TYPE_ARG1 SELECT_TYPE_ARG234 SELECT_TYPE_ARG5 


```txt
def checkSelectArgType(conf):
  ''' Adapted from autoconf '''
  conf.Message('Checking for arg types for select... ')
  for arg234 in ['fd_set *', 'int *', 'void *']:
    for arg1 in ['int', 'size_t', 'unsigned long', 'unsigned']:
      for arg5 in ['struct timeval *', 'const struct timeval *']:
        check_select_source = '''
#if HAVE_SYS_SELECT_H
# include <sys/select.h>
#endif
#if HAVE_SYS_SOCKET_H
# include <sys/socket.h>
#endif
extern int select (%s, %s, %s, %s, %s);
int main()
{
  return(0);
}
''' % (arg1, arg234, arg234, arg234, arg5)
        ret = conf.TryLink(check_select_source, '.c')
        if ret:
          conf.Result(ret)
          return (arg1, arg234, arg5)
  conf.Result('no (use default)')
  return ('int', 'int *', 'struct timeval *')
```
Check for boost libraries 


```txt
def checkBoostLibraries(conf, lib, pathes):
  ''' look for boost libraries '''
  conf.Message('Checking for boost library %s... ' % lib)
  for path in pathes:
    # direct form: e.g. libboost_iostreams.a
    if os.path.isfile(os.path.join(path, 'lib%s.a' % lib)):
      conf.Result('yes')
      return (path, lib)
    # check things like libboost_iostreams-gcc.a
    files = glob.glob(os.path.join(path, 'lib%s-*.a' % lib))
    # if there are more than one, choose the first one
    # FIXME: choose the best one.
    if len(files) >= 1:
      # get xxx-gcc from /usr/local/lib/libboost_xxx-gcc.a
      conf.Result('yes')
      return (path, os.path.basename(files[0])[3:-2])
  conf.Result('n')
  return ('','')
```

### To use them, do something like:


```txt
conf = Configure(env,
  custom_tests = {
    'CheckIstreambufIterator' : utils.checkIstreambufIterator,
    'CheckMkdirOneArg' : utils.checkMkdirOneArg,
    'CheckStdCount' : utils.checkStdCount,
    'CheckSelectArgType' : utils.checkSelectArgType,
    'CheckBoostLibraries' : utils.checkBoostLibraries,
    'CheckMsgFmt' : utils.checkMsgFmt,
  }
)
```
and then maybe 


```txt
  # MKDIR_TAKES_ONE_ARG
  if conf.CheckMkdirOneArg():
    utils.addToConfig('#define MKDIR_TAKES_ONE_ARG 1')
  else:
    utils.addToConfig('/* #undef MKDIR_TAKES_ONE_ARG */')
```
Note that addToConfig is not part of scons. 


### Standard autoconf macros

Please, if you have implemented one of the following, add your recipe here so that others can use it. (list copied from [http://scons.org/wiki/GregNoel/StandardMacros#preview](http://scons.org/wiki/GregNoel/StandardMacros#preview) ) 

AC_INIT 


```txt
Not needed
```
AC_CONFIG_SRCDIR 


```txt

```
AM_INIT_AUTOMAKE 


```txt
Not needed
```
AM_ENABLE_MULTILIB 


```txt

```
AC_PREREQ 


```txt

```
AC_COPYRIGHT 


```txt

```
AC_REVISION 


```txt
Not needed
```
AC_PREFIX_DEFAULT 


```txt

```
AC_PREFIX_PROGRAM 


```txt

```
AC_CONFIG_AUX_DIR 


```txt

```
AC_CONFIG_COMMANDS 


```txt

```
AC_CONFIG_COMMANDS_PRE 


```txt

```
AC_CONFIG_COMMANDS_POST 


```txt

```
AC_CONFIG_FILES 


```txt

```
AC_CONFIG_HEADERS 


```txt

```
AC_CONFIG_LINKS 


```txt

```
AC_CONFIG_SUBDIRS 


```txt

```
AC_OUTPUT 


```txt

```
AC_DEFINE 


```txt

```
AC_DEFINE_UNQUOTED 


```txt

```
AC_SUBST 

See [SubstInFileBuilder](SubstInFileBuilder), or try this code which uses @KEY_WORD@, just like Autoconf: 


```txt
###############################################################################
#
# ACGenerateFile.py
#
# Taken from the SubstInFileBuilder on the SCons Wiki.  Slightly modified to
# use @ around keys so it behaves like GNU autotools.
#
###############################################################################


import re
from SCons.Script import *

def TOOL_SUBST(env):
    """Adds ACGenerateFile builder, which substitutes the keys->values of
    SUBST_DICT from the source to the target.

    The values of SUBST_DICT first have any construction variables expanded
    (its keys are not expanded).

    If a value of SUBST_DICT is a python callable function, it is called and
    the result is expanded as the value.

    If there's more than one source and more than one target, each target gets
    substituted from the corresponding source.
    """
    env.Append(TOOLS = 'SUBST')

    def do_subst_in_file(targetfile, sourcefile, dict):
        """Replace all instances of the keys of dict with their values.
        For example, if dict is {'VERSION': '1.2345', 'BASE': 'MyProg'},
        then all instances of @VERSION@ in the file will be replaced with
        1.2345 etc.
        """
        try:
            f = open(sourcefile, 'rb')
            contents = f.read()
            f.close()
        except:
            raise SCons.Errors.UserError, "Can't read source file %s"%sourcefile
        for (k,v) in dict.items():
            contents = re.sub("@" + k + "@", v, contents)
        try:
            f = open(targetfile, 'wb')
            f.write(contents)
            f.close()
        except:
            raise SCons.Errors.UserError, "Can't write target file %s"%targetfile
        return 0 # success

    def subst_in_file(target, source, env):
        if 'SUBST_DICT' not in env:
            raise SCons.Errors.UserError, "SubstInFile requires SUBST_DICT to be set."
        d = dict(env['SUBST_DICT']) # copy it
        for (k,v) in d.items():
            if callable(v):
                d[k] = env.subst(v())
            elif SCons.Util.is_String(v):
                d[k]=env.subst(v)
            else:
                raise SCons.Errors.UserError, "SubstInFile: key %s: %s must be a string or callable"%(k, repr(v))
        for (t,s) in zip(target, source):
            return do_subst_in_file(str(t), str(s), d)

    def subst_in_file_string(target, source, env):
        """This is what gets printed on the console."""
        return '\n'.join(['Substituting vars from %s into %s'%(s, t)
                          for t,s in zip(target, source)])

    def subst_emitter(target, source, env):
        """Add dependency from substituted SUBST_DICT to target.
        Returns original target, source tuple unchanged.
        """
        d = env['SUBST_DICT'].copy() # copy it
        for (k,v) in d.items():
            if callable(v):
                d[k] = env.subst(v())
            elif SCons.Util.is_String(v):
                d[k]=env.subst(v)
        Depends(target, SCons.Node.Python.Value(d))
        return target, source

    subst_action=SCons.Action.Action(subst_in_file, subst_in_file_string)
    env['BUILDERS']['SubstInFile'] = Builder(action=subst_action, emitter=subst_emitter)
```
To use do: 
```txt
# Add the tool for use in the environment
from ACGenerateFile import *

# Setup some variables

PACKAGE_NAME = "nsound"

VERSION_A = "0"
VERSION_B = "5"
VERSION_C = "0"

PACKAGE_VERSION = VERSION_A + "." + VERSION_B + "." + VERSION_C

PACKAGE_RELEASE = PACKAGE_NAME + "-" + PACKAGE_VERSION

# create a new empty dictionary
dict = {}

# set the keys in the dictionary 
dict["PACKAGE_RELEASE"] = PACKAGE_RELEASE

endian = conf.checkEndian() # look at AC_C_BIGENDIAN on this wiki

if endian == "little":
        dict["PLATFORM_ENDIAN"] = "PLATFORM_LITTLE_ENDIAN"
elif endian == "big":
        dict["PLATFORM_ENDIAN"] = "PLATFORM_BIG_ENDIAN"

# Add the tool to the build environment
env = Environment(ENV = os.environ,
                  CXXFLAGS = env_CXXFLAGS + " " + custom_cxxflags,
                  CCFLAGS = env_CCFLAGS + " " + custom_ccflags,
                  LINKFLAGS = env_LDFLAGS + " ",
                  tools = ['default', TOOL_SUBST, "DistTar", "DistZip"],
                  toolpath = ".")

env.SubstInFile('src/Nsound/Nsound.h', 'src/Nsound/Nsound.h.in', SUBST_DICT=dict)
env.SubstInFile('src/Doxyfile', 'src/Doxyfile.in', SUBST_DICT=dict)
```
AC_SUBST_FILE 


```txt

```
AC_ARG_VAR 


```txt

```
AH_VERBATIM 


```txt

```
AH_TEMPLATE 


```txt

```
AH_TOP 


```txt

```
AH_BOTTOM 


```txt

```
AC_CHECK_PROG 


```txt
# note that the full command path or none is returned, which can serve as True or False.
def CheckCommand(context, cmd):
       context.Message('Checking for %s command... ' % cmd)
       result = WhereIs(cmd)
       context.Result(result is not None)
       return result
```
AC_CHECK_PROGS 


```txt
Not needed
```
AC_CHECK_TOOL 


```txt

```
AC_CHECK_TOOLS 


```txt

```
AC_PATH_PROG 


```txt

```
AC_PATH_PROGS 


```txt

```
AC_PATH_TOOL 


```txt

```
AC_PROG_AWK 


```txt

```
AC_PROG_EGREP 


```txt

```
AC_PROG_FGREP 


```txt

```
AC_PROG_INSTALL 


```txt

```
AC_PROG_LEX 


```txt

```
AC_PROG_YACC 


```txt

```
AC_PROG_RANLIB 


```txt

```
AC_PROG_LN_S 


```txt

```
AM_GNU_GETTEXT 


```txt

```
AM_PATH_PYTHON 


```txt

```
AM_PATH_LISPDIR 


```txt

```
AM_PROG_LISP 


```txt

```
AM_PROG_AS 


```txt

```
AM_PROG_LEX 


```txt

```
AM_PROG_GCJ 


```txt

```
AC_CHECK_FILE 


```txt

```
AC_CHECK_FILES 


```txt

```
AC_CHECK_LIB 


```txt

```
AC_SEARCH_LIBS 


```txt

```
AM_WITH_MALLOC 


```txt

```
AM_WITH_REGEX 


```txt

```
AC_CHECK_FUNCS 


```txt
implemented as CheckFunc
```
AC_LIBOBJ 


```txt

```
AC_LIBSOURCE 


```txt

```
AC_LIBSOURCES 


```txt

```
AC_CONFIG_LIBOBJ_DIR 


```txt

```
AC_REPLACE_FUNCS 


```txt

```
AC_REPLACE_FNMATCH 


```txt

```
AC_FUNC_ALLOCA 


```txt

```
AC_FUNC_CHOWN 


```txt

```
AC_FUNC_CLOSEDIR_VOID 


```txt

```
AC_FUNC_ERROR_AT_LINE 


```txt

```
AC_FUNC_FNMATCH 


```txt

```
AC_FUNC_FNMATCH_GNU 


```txt

```
AC_FUNC_FORK 


```txt

```
AC_FUNC_FSEEKO 


```txt

```
AC_FUNC_GETGROUPS 


```txt

```
AC_FUNC_GETLOADAVG 


```txt

```
AC_FUNC_GETMNTENT 


```txt

```
AC_FUNC_GETPGRP 


```txt

```
AC_FUNC_LSTAT_FOLLOWS_SLASHED_SYMLINK 


```txt

```
AC_FUNC_MALLOC 


```txt

```
AC_FUNC_MEMCMP 


```txt

```
AC_FUNC_MBRTOWC 


```txt

```
AC_FUNC_MKTIME 


```txt

```
AC_FUNC_MMAP 


```txt

```
AC_FUNC_OBSTACK 


```txt

```
AC_FUNC_REALLOC 


```txt

```
AC_FUNC_SELECT_ARGTYPES 


```txt

```
AC_FUNC_SETPGRP 


```txt

```
AC_FUNC_SETVBUF_REVERSED 


```txt

```
AC_FUNC_STAT 


```txt

```
AC_FUNC_LSTAT 


```txt

```
AC_FUNC_STRCOLL 


```txt

```
AC_FUNC_STRERROR_R 


```txt

```
AC_FUNC_STRFTIME 


```txt

```
AC_FUNC_STRNLEN 


```txt

```
AC_FUNC_STRTOD 


```txt

```
AC_FUNC_UTIME_NULL 


```txt

```
AC_FUNC_VPRINTF 


```txt

```
AC_CHECK_FUNC 


```txt

```
AC_CHECK_HEADERS 


```txt

```
AC_HEADER_DIRENT 


```txt

```
AC_HEADER_MAJOR 


```txt

```
AC_HEADER_STAT 


```txt

```
AC_HEADER_STDBOOL 


```txt

```
AC_HEADER_STDC 


```txt
##############################################################################
#
# By Samarjit Adhikari (adhikari_20022002_at_yahoo_com)
# Usage:
#    conf = Configure(env,custom_tests=\
#                 {'CheckStdCHeader': CheckStdCHeader
#                 },log_file="config.log",config_h="config.h")
#
#    if (not conf.CheckStdCHeader()):
#        ...
#    else:
#        ...
#
##############################################################################
def build_it(target = None, source = None, env = None):
    """
    This function is used to do Preprocessor operation
    on the source and verify the ANSI compliance of the system
    header files.
    """
    strsource = ""
    strtarget = ""
    for src in source:
        strsource += str(src)

    #Assuming only one target FIXME
    strtarget += str(target[0])

    cmd = str(env['CC']) + ' -E -o'+strtarget+' '+strsource

    p = os.popen (cmd)
    return p.close ()

def CheckStdCHeader(context):
    """
    This function is like a autoconf macro 'AC_PROG_CC_STDC'.
    """
    context.Message('Checking ANSI C compliant headers...')

    action_obj = Action (build_it)
    ret        = context.TryCompile(
    """
    #include <stdlib.h>
    #include <stdarg.h>
    #include <string.h>
    #include <float.h>

    int
    main ()
    {
      ;
      return 0;
    }
    """,\
    '.c')

    if ret: # Successful compilation
       retList = []
       ######### Try more specific . Test1 #########
       ret = context.TryAction (action_obj,\
       """
       #include <stdlib.h>
       """,'.c')
       #import pdb;pdb.set_trace()
       if ret[0]==1:
           if(re.search('free',ret[1])):
               retList.append(1)
           else:
               retList.append(0)
       ############### Test2 #####################
       ret = context.TryAction (action_obj,\
       """
       #include <string.h>
       """,'.c')
       if ret[0]==1:
           if(re.search('memchr',ret[1])):
               retList.append(1)
           else:
               retList.append(0)
       ################ Test3 #####################
       ret = context.TryLink(
       """
       #include <ctype.h>
       #if ((' ' & 0x0FF) == 0x020)
       # define ISLOWER(c) ('a' <= (c) && (c) <= 'z')
       # define TOUPPER(c) (ISLOWER(c) ? 'A' + ((c) - 'a') : (c))
       #else
       # define ISLOWER(c) \
                  (('a' <= (c) && (c) <= 'i') \
                    || ('j' <= (c) && (c) <= 'r') \
                    || ('s' <= (c) && (c) <= 'z'))
       # define TOUPPER(c) (ISLOWER(c) ? ((c) | 0x40) : (c))
       #endif

       #define XOR(e, f) (((e) && !(f)) || (!(e) && (f)))
       int
       main ()
       {
         int i;
         for (i = 0; i < 256; i++)
           if (XOR (islower (i), ISLOWER (i))
           || toupper (i) != TOUPPER (i))
             exit(2);
         exit (0);
       }
       """,'.c')
       if ret==1:
           retList.append(1)
       else:
           retList.append(0)
       #Do the final testing.
       if 0 not in retList:
           ret = 1;
       else:
           ret = 0;

    context.Result(ret)
    return ret
```
AC_HEADER_SYS_WAIT 


```txt

```
AC_HEADER_TIME 


```txt

```
AC_HEADER_TIOCGWINSZ 


```txt

```
AC_CHECK_DECL 


```txt

```
AC_CHECK_DECLS 


```txt

```
AC_CHECK_MEMBER 


```txt

```
AC_CHECK_MEMBERS 


```txt

```
AC_STRUCT_ST_BLKSIZE 


```txt

```
AC_STRUCT_ST_BLOCKS 


```txt

```
AC_STRUCT_ST_RDEV 


```txt

```
AC_STRUCT_TM 


```txt

```
AC_STRUCT_TIMEZONE 


```txt

```
AC_CHECK_TYPES 


```txt

```
AC_TYPE_GETGROUPS 


```txt

```
AC_TYPE_MBSTATE_T 


```txt

```
AC_TYPE_MODE_T 


```txt

```
AC_TYPE_OFF_T 


```txt

```
AC_TYPE_PID_T 


```txt

```
AC_TYPE_SIGNAL 


```txt

```
AC_TYPE_SIZE_T 


```txt

```
AC_TYPE_UID_T 


```txt

```
AC_PROG_CPP 


```txt

```
AC_PROG_CXXCPP 


```txt

```
AC_PROG_CC 


```txt

```
AC_PROG_CC_C_O 


```txt

```
AM_PROG_CC_C_O 


```txt

```
AC_C_BACKSLASH_A 


```txt

```
AC_C_BIGENDIAN 


```txt
# This code was tested on Intel, AMD 64, and Cell (Playstation 3)

# Python already knows what endian it is, just ask Python.

def checkEndian(context):
    context.Message("checking endianess ... ")

    import struct

    array = struct.pack('cccc', '\x01', '\x02', '\x03', '\x04')

    i = struct.unpack('i', array)

    # Little Endian
    if i == struct.unpack('<i', array):
        context.Result("little")
        return "little"

    # Big Endian
    elif i == struct.unpack('>i', array):
        context.Result("big")
        return "big"

    context.Result("unknown")
    return "unknown"

conf = Configure(env, custom_tests = { 'checkEndian' : checkEndian }

endian = conf.checkEndian()

if endian == "little" :
    # something

elif endian == "big" :
    # something else

else:
    # unknown endianess
```
AC_C_CONST 


```txt

```
AC_C_VOLATILE 


```txt

```
AC_C_INLINE 


```txt

```
AC_C_CHAR_UNSIGNED 


```txt

```
AC_C_LONG_DOUBLE 


```txt

```
AC_C_STRINGIZE 


```txt

```
AC_C_PROTOTYPES 


```txt

```
AM_C_PROTOTYPES 


```txt

```
AC_PROG_GCC_TRADITIONAL 


```txt

```
AC_PROG_CXX 


```txt

```
AC_PROG_F77 


```txt

```
AC_PROG_F77_C_O 


```txt

```
AC_F77_LIBRARY_LDFLAGS 


```txt

```
AC_F77_DUMMY_MAIN 


```txt

```
AC_F77_MAIN 


```txt

```
AC_F77_WRAPPERS 


```txt

```
AC_F77_FUNC 


```txt

```
AC_LANG 


```txt

```
AC_LANG_PUSH 


```txt

```
AC_LANG_POP 


```txt

```
AC_LANG_CONFTEST 


```txt

```
AC_LANG_SOURCE 


```txt

```
AC_LANG_PROGRAM 


```txt

```
AC_LANG_CALL 


```txt

```
AC_LANG_FUNC_LINK_TRY 


```txt

```
AC_PREPROC_IFELSE 


```txt

```
AC_EGREP_HEADERS 


```txt

```
AC_EGREP_CPP 


```txt
env=Environment()
conf=env.Configure()
import os,os.path,platform
# Only tested on OS X
if platform.system()=="Windows" and not env["CC"].count("gcc"):
   conf.env["CPPFLAG"]="/EP"
elif platform.system().count("VMS"):
   conf.env[optmarker]="/PREPROCESS_ONLY"
else:
   conf.env["CPPFLAG"]="-E -P"
match="main"
def cpp_egrep_gen(target, source, env, for_signature):
    return "%s %s %s | egrep %s"%(env["CC"],env["CPPFLAG"],source[0],match)
cpp_egrep = Builder(generator= cpp_egrep_gen, suffix = '.i', src_suffix = '.c')
conf.env["BUILDERS"].update({'CPP_EGREP' : cpp_egrep})
def Check_cpp_egrep(context,source_string):
    # assumes source and match are type str
    context.Message("Checking cpp | egrep %s :"%match)
    res=context.TryBuild(conf.env.CPP_EGREP,source_string,".c")
    context.Result(res)
conf.AddTests( {'Check_cpp_egrep': Check_cpp_egrep })
test_str="""
#include <iostream>
using namespace std;
int main(){
    cout<<"this is a test\n";
    return 0;
}"""
conf.Check_cpp_egrep(test_str)
env=conf.Finish()

```
AC_CHECK_SIZEOF 


```txt
For example, the following function can be used:
def checkSizeOf(context, type):
    context.Message( 'getting size of ' + type + '... ' )
    #
    # We have to be careful with the program we wish to test here since
    # compilation will be attempted using the current environment's flags.
    # So make sure that the program will compile without any warning. For
    # example using: 'int main(int argc, char** argv)' will fail with the
    # '-Wall -Werror' flags since the variables argc and argv would not be
    # used in the program...
    #
    program = """
#include <stdlib.h>
#include <stdio.h>
int main() {
    printf("%d", (int)sizeof(""" + type + """));
    return 0;
}
"""
    ret = context.TryCompile(program, '.c')
    if ret == 0:
        print "test failed!\n"
        print "Error: cannot run the following test program:"
        print program
        print "Please check your compiler flags."
        Exit(1)
    ret = context.TryRun(program, '.c')
    context.Result(ret[0])
    return ret[1]
#
# This function should then be added to the configure context's
# custom tests
#
conf = Configure(env, custom_tests = {'checkSizeOf' : checkSizeOf})
#
# For example, print the result of sizeof(unsigned long int).
# Of course, in a real SCons file, this result would probably
# be stored in a environment variable or written to a config.h
# file
#
print "sizeof(unsigned long int) is: " + conf.checkSizeOf('unsigned long int')
```

```txt
This is another version, which uses a scheme similar to autoconf for testing the size (without requiring any run, thus being quite faster than methods using TryRun), and is a bit more flexible than the above (same API than the CheckType from SCons, with one more argument for expected size).

# Sensible default for common types on common platforms.
_DEFAULTS = {
    'short' : [2],
    'int' : [4, 2],
    'long' : [4, 8],
    'long long' : [8, 4],
    # Normally, there is no need to check unsigned types, because they are
    # guaranteed to be of the same size than their signed counterpart.
    'unsigned short' : [2],
    'unsigned int' : [4, 2],
    'unsigned long' : [4, 8],
    'unsigned long long' : [8, 4],
    'float' : [4],
    'double' : [8],
    'long double' : [12],
    'size_t' : [4],
}

def CheckTypeSize(context, type, includes = None, language = 'C', size = None):
    """This check can be used to get the size of a given type, or to check whether
    the type is of expected size.

    Arguments:
        - type : str
            the type to check
        - includes : sequence
            list of headers to include in the test code before testing the type
        - language : str
            'C' or 'C++'
        - size : int
            if given, will test wether the type has the given number of bytes.
            If not given, will test against a list of sizes (all sizes between
            0 and 16 bytes are tested).

        Returns:
                status : int
                        0 if the check failed, or the found size of the type if the check succeeded."""
    minsz = 0
    maxsz = 16

    if includes:
        src = "\n".join("#include <%s>\n" % i for i in includes)
    else:
        src = ""

    if language == 'C':
        ext = '.c'
    elif language == 'C++':
        ext = '.cpp'
    else:
        raise NotImplementedError("%s is not a recognized language" % language)

    # test code taken from autoconf: this is a pretty clever hack to find that
    # a type is of a given size using only compilation. This speeds things up
    # quite a bit compared to straightforward code using TryRun
    src += r"""
typedef %s scons_check_type;

int main()
{
    static int test_array[1 - 2 * ((long int) sizeof(scons_check_type) > %d)];
    test_array[0] = 0;

    return 0;
}
"""
        
    if size:
        # Only check if the given size is the right one
        context.Message('Checking %s is %d bytes... ' % (type, size))
        st = context.TryCompile(src % (type, size), ext)
        context.Result(st)

        if st:
            return size
        else:
            return 0
    else:
        # Only check if the given size is the right one
        context.Message('Checking size of %s ... ' % type)

        # Try sensible defaults first
        try:
            szrange = _DEFAULTS[type]
        except KeyError:
            szrange = []
        szrange.extend(xrange(minsz, maxsz))
        st = 0

        # Actual test
        for sz in szrange:
            st = context.TryCompile(src % (type, sz), ext)
            if st:
                break

        if st:
            context.Result('%d' % sz)
            return sz
        else:
            context.Result('Failed !')
            return 0

For example, to check wether long is 4 bytes on your platform, you can do:
config.CheckTypeSize('long', size = 4).
```
AC_PATH_X 


```txt

```
AC_PATH_XTRA 


```txt

```
AC_SYS_INTERPRETER 


```txt

```
AC_SYS_LARGEFILE 


```txt

```
AC_SYS_LONG_FILE_NAMES 


```txt

```
AC_SYS_POSIX_TERMIOS 


```txt

```
AC_AIX 


```txt

```
AC_GNU_SOURCE 


```txt

```
AC_ISC_POSIX 


```txt

```
AC_MINIX 


```txt

```
AC_CANONICAL_BUILD 


```txt

```
AC_CANONICAL_HOST 


```txt

```
AC_CANONICAL_TARGET 


```txt

```
AC_ARG_PROGRAM 


```txt

```
AC_ARG_WITH/AC_WITH 


```txt

```
AC_ARG_ENABLE/AC_ENABLE 


```txt

```
AC_HELP_STRING 


```txt

```
AC_CONFIG_TESTDIR 


```txt

```
AT_INIT 


```txt

```
AT_TESTED 


```txt

```
AT_SETUP 


```txt

```
AT_KEYWORDS 


```txt

```
AT_CLEANUP 


```txt

```
AT_DATA 


```txt

```
AT_CHECK 


```txt

```
AC_MSG_NOTICE 


```txt

```
AC_MSG_ERROR 


```txt

```
AC_MSG_FAILURE 


```txt

```
AC_MSG_WARN 


```txt

```
AC_DIAGNOSE 


```txt

```
AC_WARNING 


```txt

```
AC_FATAL 


```txt

```
AC_CACHE_VAL 


```txt

```
AC_CACHE_CHECK 


```txt

```
AC_CACHE_LOAD 


```txt

```
AC_CACHE_SAVE 


```txt

```
AC_REQUIRE 


```txt

```
AC_REQUIRE_CPP 


```txt

```
AC_BEFORE 


```txt

```
AM_CONDITIONAL 


```txt

```
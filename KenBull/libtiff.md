

## SConstruct for libtiff

The libtiff homepage is [LibTIFF - TIFF Library and Utilities](http://www.libtiff.org/). Get the library itself [here](http://dl.maptools.org/dl/libtiff/). This is setup to use MinGW by default.  If you want to use another compiler or OS you may need to play with it a bit, but not much. This script uses features from Python 2.6 (print function and with statement).  If you are using 2.5.x or below you will either need to upgrade or modify this file appropriately. 


### Code


```python
#!python 
# $Id: SConstruct,v 1.2 2006/03/23 14:54:02 dron Exp $

# Tag Image File Format (TIFF) Software
#
# Copyright (C) 2005, Andrey Kiselev <dron@ak4719.spb.edu>
#
# Permission to use, copy, modify, distribute, and sell this software and 
# its documentation for any purpose is hereby granted without fee, provided
# that (i) the above copyright notices and this permission notice appear in
# all copies of the software and related documentation, and (ii) the names of
# Sam Leffler and Silicon Graphics may not be used in any advertising or
# publicity relating to the software without the specific, prior written
# permission of Sam Leffler and Silicon Graphics.
# 
# THE SOFTWARE IS PROVIDED "AS-IS" AND WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS, IMPLIED OR OTHERWISE, INCLUDING WITHOUT LIMITATION, ANY 
# WARRANTY OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.  
# 
# IN NO EVENT SHALL SAM LEFFLER OR SILICON GRAPHICS BE LIABLE FOR
# ANY SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY KIND,
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER OR NOT ADVISED OF THE POSSIBILITY OF DAMAGE, AND ON ANY THEORY OF 
# LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE 
# OF THIS SOFTWARE.

# This file contains rules to build software with the SCons tool
# (see the http://www.scons.org/ for details on SCons).

from __future__ import print_function
import os

def CheckSizeofInt(context):
    sizeof_int_test = '#include <stdio.h>\nint main() {printf("%d", sizeof(int)); return 0;}\n'
    context.Message('Checking sizeof(int)...')
    result = context.TryRun(sizeof_int_test, '.c')
    if not result[0]:
        context.Result(result[0])
        Exit(1)
    context.Result(result[1])
    return result[1]
def CheckSizeofLong(context):
    sizeof_long_test = '#include <stdio.h>\nint main() {printf("%d", sizeof(long)); return 0;}\n'
    context.Message('Checking sizeof(long)...')
    result = context.TryRun(sizeof_long_test, '.c')
    if not result[0]:
        context.Result(result[0])
        Exit(1)
    context.Result(result[1])
    return result[1]
def CheckTimeWithSysTime(context):
    time_with_sys_time_test = "#include <time.h>\n#include <sys/time.h>\nint main() {return 0;}\n"
    context.Message('Checking if you can safely include both <sys/time.h> and <time.h>...')
    result = context.TryCompile(time_with_sys_time_test, '.c')
    context.Result(result)
    return result
def CheckTmInSysTime(context):
    tm_in_sys_time_test = "#include <sys/time.h>\nstruct tm t;\nint main() {return 0;}\n"
    context.Message("Checking if your <sys/time.h> declares `struct tm'...")
    result = context.TryCompile(tm_in_sys_time_test, '.c')
    context.Result(result)
    return result

def GrokSettings(env):
    settings = {}
    
    settings['CCITT_SUPPORT']                = env['CCITT_SUPPORT']
    settings['CHECK_JPEG_YCBCR_SUBSAMPLING'] = env['CHECK_JPEG_YCBCR_SUBSAMPLING']
    settings['CXX_SUPPORT']                  = env['CXX_SUPPORT']
    settings['DEFAULT_EXTRASAMPLE_AS_ALPHA'] = env['DEFAULT_EXTRASAMPLE_AS_ALPHA']
    settings['HAVE_APPLE_OPENGL_FRAMEWORK']  = env['HAVE_APPLE_OPENGL_FRAMEWORK']
    settings['JPEG_SUPPORT']                 = env['JPEG_SUPPORT']
    settings['LOGLUV_SUPPORT']               = env['LOGLUV_SUPPORT']
    settings['LZW_SUPPORT']                  = env['LZW_SUPPORT']
    settings['MDI_SUPPORT']                  = env['MDI_SUPPORT']
    settings['NEXT_SUPPORT']                 = env['NEXT_SUPPORT']
    settings['OJPEG_SUPPORT']                = env['OJPEG_SUPPORT']
    settings['PACKBITS_SUPPORT']             = env['PACKBITS_SUPPORT']
    settings['PIXARLOG_SUPPORT']             = env['PIXARLOG_SUPPORT']
    settings['STRIPCHOP_DEFAULT']            = env['STRIPCHOP_DEFAULT'] and 'TIFF_STRIPCHOP' or False
    settings['STRIP_SIZE_DEFAULT']           = str(env['STRIP_SIZE_DEFAULT'])
    settings['SUBIFD_SUPPORT']               = env['SUBIFD_SUPPORT']
    settings['THUNDER_SUPPORT']              = env['THUNDER_SUPPORT']
    settings['X_DISPLAY_MISSING']            = env['X_DISPLAY_MISSING']
    settings['ZIP_SUPPORT']                  = env['ZIP_SUPPORT']
    
    settings['HAVE_IEEEFP'] = True
    settings['HAVE_INT16'] = False
    settings['HAVE_INT32'] = False
    settings['HAVE_INT8'] = False
    settings['HOST_BIGENDIAN'] = '0'
    settings['WORDS_BIGENDIAN'] = False # Define to 1 if your processor stores words with the most significant byte first (like Motorola and SPARC, unlike Intel and VAX).
    settings['HOST_FILLORDER'] = 'FILLORDER_LSB2MSB'
    settings['LT_OBJDIR'] = '".libs/"' # Define to the sub-directory in which libtool stores uninstalled libraries.
    settings['NO_MINUS_C_MINUS_O'] = False
    settings['PACKAGE'] = '"tiff"'
    settings['PACKAGE_BUGREPORT'] = '"tiff@lists.maptools.org"'
    settings['PACKAGE_NAME'] = '"LibTIFF Software"'
    settings['PACKAGE_STRING'] = '"LibTIFF Software 3.8.2"'
    settings['PACKAGE_TARNAME'] = '"tiff"'
    settings['PACKAGE_VERSION'] = '"3.8.2"'
    settings['VERSION'] ='"3.8.2"'
    settings['PTHREAD_CREATE_JOINABLE'] = False # Define to necessary symbol if this constant uses a non-standard name on your system.
    settings['STDC_HEADERS'] = True # Define to 1 if you have the ANSI C header files.
    settings['_FILE_OFFSET_BITS'] = False # Number of bits in a file offset, on hosts where this is settable.
    settings['_LARGE_FILES'] = False # Define for large files, on AIX-style hosts.
    settings['const'] = False # Define to empty if `const' does not conform to ANSI C.
    settings['inline'] = False # Define to `__inline__' or `__inline' if that's what the C compiler calls it, or to nothing if 'inline' is not supported under any name.
    
    conf = Configure(env, custom_tests = {'CheckSizeofInt': CheckSizeofInt, 
                                          'CheckSizeofLong': CheckSizeofLong,
                                          'CheckTimeWithSysTime': CheckTimeWithSysTime,
                                          'CheckTmInSysTime': CheckTmInSysTime})
    
    settings['HAVE_ASSERT_H'] = conf.CheckCHeader('assert.h')
    settings['HAVE_DLFCN_H'] = conf.CheckCHeader('dlfcn.h')
    settings['HAVE_FCNTL_H'] = conf.CheckCHeader('fcntl.h')
    settings['HAVE_INTTYPES_H'] = conf.CheckCHeader('inttypes.h')
    settings['HAVE_LIMITS_H'] = conf.CheckCHeader('limits.h')
    settings['HAVE_MALLOC_H'] = conf.CheckCHeader('malloc.h')
    settings['HAVE_MEMORY_H'] = conf.CheckCHeader('memory.h')
    settings['HAVE_SEARCH_H'] = conf.CheckCHeader('search.h')
    settings['HAVE_STDINT_H'] = conf.CheckCHeader('stdint.h')
    settings['HAVE_STDLIB_H'] = conf.CheckCHeader('stdlib.h')
    settings['HAVE_STRINGS_H'] = conf.CheckCHeader('strings.h')
    settings['HAVE_STRING_H'] = conf.CheckCHeader('string.h')
    settings['HAVE_SYS_STAT_H'] = conf.CheckCHeader('sys/stat.h')
    settings['HAVE_SYS_TIME_H'] = conf.CheckCHeader('sys/time.h')
    settings['HAVE_SYS_TYPES_H'] = conf.CheckCHeader('sys/types.h')
    settings['HAVE_UNISTD_H'] = conf.CheckCHeader('unistd.h')
    settings['HAVE_WINDOWS_H'] = conf.CheckCHeader('windows.h')
    
    settings['HAVE_FLOOR'] = conf.CheckFunc('floor')
    settings['HAVE_GETOPT'] = conf.CheckFunc('getopt')
    settings['HAVE_ISASCII'] = conf.CheckFunc('isascii')
    settings['HAVE_LFIND'] = conf.CheckFunc('lfind')
    settings['HAVE_MEMMOVE'] = conf.CheckFunc('memmove')
    settings['HAVE_MEMSET'] = conf.CheckFunc('memset')
    settings['HAVE_MMAP'] = conf.CheckFunc('mmap')
    settings['HAVE_POW'] = conf.CheckFunc('pow')
    settings['HAVE_SQRT'] = conf.CheckFunc('sqrt')
    settings['HAVE_STRCASECMP'] = conf.CheckFunc('strcasecmp')
    settings['HAVE_STRCHR'] = conf.CheckFunc('strchr')
    settings['HAVE_STRRCHR'] = conf.CheckFunc('strrchr')
    settings['HAVE_STRSTR'] = conf.CheckFunc('strstr')
    settings['HAVE_STRTOL'] = conf.CheckFunc('strtol')
    settings['HAVE_STRTOUL'] = conf.CheckFunc('strtoul')
    
    settings['HAVE_LIBC'] = conf.CheckLib('c')
    settings['HAVE_LIBM'] = conf.CheckLib('m')
    
    settings['HAVE_PTHREAD'] = conf.CheckLibWithHeader('pthread', 'pthread.h', 'c')
    
    if settings['JPEG_SUPPORT'] and not conf.CheckLib('jpeg'):
        print("JPEG compression requires IJG JPEG library, which is not present.")
        Exit(1)
    
    if settings['PIXARLOG_SUPPORT'] and not conf.CheckLib('z'):
        print("Pixar log-format algorithm support requires Zlib, which is not present.")
        Exit(1)
    
    if settings['ZIP_SUPPORT'] and not conf.CheckLib('z'):
        print("Deflate compression support requires Zlib, which is not present.")
        Exit(1)
    
    settings['SIZEOF_INT'] = conf.CheckSizeofInt()
    settings['SIZEOF_LONG'] = conf.CheckSizeofLong()
    settings['TIME_WITH_SYS_TIME'] = conf.CheckTimeWithSysTime()
    settings['TM_IN_SYS_TIME'] = conf.CheckTmInSysTime()
    
    if conf.CheckType('off_t', '#include <sys/types.h>\n'):
       settings['off_t'] = False
    else:
       settings['off_t'] = 'long'
    
    if conf.CheckType('size_t', '#include <sys/types.h>\n'):
       settings['size_t'] = False
    else:
       settings['size_t'] = 'unsigned'
    
    env = conf.Finish()
    env['settings'] = settings
    return env

def GenerateConfig(target, source, env):
    settings=env['settings']
    for t in target:
        print(t)
        with open(str(t), 'wt') as f:
            for key in settings.keys():
                if isinstance(settings[key], str):
                    print("#define %s %s" % (key, settings[key]), file=f)
                else:
                    if settings[key]:
                        print("#define %s 1" % (key,), file=f)
                    else:
                        print("/* #undef %s */" % (key,), file=f)
    return 0

# Import globally defined options
#Import([ 'env', 'idir_lib' ])

opts = Variables()
opts.Add(PathVariable('PREFIX',
                      'Directory to install under', 
                      'c:/mingw',
                      PathVariable.PathIsDir))
opts.Add(BoolVariable('CCITT_SUPPORT', 
                      'Support CCITT Group 3 & 4 algorithms.',
                      1))
opts.Add(BoolVariable('CHECK_JPEG_YCBCR_SUBSAMPLING', 
                      'Pick up YCbCr subsampling info from the JPEG data stream to support files '\
                      'lacking the tag (default enabled).',
                      1))
opts.Add(BoolVariable('CXX_SUPPORT', 
                      'Support C++ stream API (requires C++ compiler).',
                      0))
opts.Add(BoolVariable('DEFAULT_EXTRASAMPLE_AS_ALPHA', 
                      'Treat extra sample as alpha (default enabled). The RGBA interface will ' \
                      'treat a fourth sample with no EXTRASAMPLE_ value as being ASSOCALPHA. Many ' \
                      'packages produce RGBA files but don\'t mark the alpha properly.',
                      1))
opts.Add(BoolVariable('HAVE_APPLE_OPENGL_FRAMEWORK', 
                      'Use the Apple OpenGL framework.',
                      0))
opts.Add(BoolVariable('JPEG_SUPPORT',
                      'Support JPEG compression (requires IJG JPEG library).',
                      1))
opts.Add(BoolVariable('LOGLUV_SUPPORT',
                      'Support LogLuv high dynamic range encoding.',
                      1))
opts.Add(BoolVariable('LZW_SUPPORT',
                      'Support LZW algorithm.', 
                      1))
opts.Add(BoolVariable('MDI_SUPPORT', 
                      'Support Microsoft Document Imaging format.', 
                      1))
opts.Add(BoolVariable('NEXT_SUPPORT', 
                      'Support NeXT 2-bit RLE algorithm.',
                      1))
opts.Add(BoolVariable('OJPEG_SUPPORT',
                      'Support Old JPEG compresson (read contrib/ojpeg/README first! Compilation ' \
                      'fails with unpatched IJG JPEG library.',
                      0))
opts.Add(BoolVariable('PACKBITS_SUPPORT', 'Support Macintosh PackBits algorithm.', 1))
opts.Add(BoolVariable('PIXARLOG_SUPPORT', 'Support Pixar log-format algorithm (requires Zlib).', 1))
opts.Add(BoolVariable('STRIPCHOP_DEFAULT',
                      'Support strip chopping (whether or not to convert single-strip uncompressed ' \
                      'images to mutiple strips of specified size to reduce memory usage)',
                      1))
opts.Add('STRIP_SIZE_DEFAULT', 'Default size of the strip in bytes (when strip chopping enabled).', '8192')
opts.Add(BoolVariable('SUBIFD_SUPPORT', 'Enable SubIFD tag (330) support.', 1))
opts.Add(BoolVariable('THUNDER_SUPPORT', 'Support ThunderScan 4-bit RLE algorithm.', 1))
opts.Add(BoolVariable('X_DISPLAY_MISSING', 'Define to 1 if the X Window System is missing or not being used.', 1))
opts.Add(BoolVariable('ZIP_SUPPORT', 'Support Deflate compression.', 1))

env = Environment(ENV=os.environ, variables=opts)
Tool('mingw')(env)
env.Replace(CCFLAGS="-O2 -march=i686")

Help(opts.GenerateHelpText(env))

    
idir_prefix = '$PREFIX'
idir_lib    = '$PREFIX/lib'
idir_bin    = '$PREFIX/bin'
idir_inc    = '$PREFIX/include'
idir_data   = '$PREFIX/share'
Export('env idir_prefix idir_lib idir_bin idir_inc idir_data')


VariantDir('bin', 'obj', duplicate=0)
VariantDir('lib', 'obj', duplicate=0)
VariantDir('obj', '.', duplicate=0)

env = GrokSettings(env)

env.AlwaysBuild(env.Command('tif_config.h', '', GenerateConfig))


SRCS = [
        'tif_aux.c', 
        'tif_close.c', 
        'tif_codec.c', 
        'tif_color.c', 
        'tif_compress.c', 
        'tif_dir.c', 
        'tif_dirinfo.c', 
        'tif_dirread.c', 
        'tif_dirwrite.c', 
        'tif_dumpmode.c', 
        'tif_error.c', 
        'tif_extension.c', 
        'tif_fax3.c', 
        'tif_fax3sm.c', 
        'tif_flush.c', 
        'tif_getimage.c', 
        'tif_jpeg.c', 
        'tif_luv.c', 
        'tif_lzw.c', 
        'tif_next.c', 
        'tif_ojpeg.c', 
        'tif_open.c', 
        'tif_packbits.c', 
        'tif_pixarlog.c', 
        'tif_predict.c', 
        'tif_print.c', 
        'tif_read.c', 
        'tif_strip.c', 
        'tif_swab.c', 
        'tif_thunder.c', 
        'tif_tile.c', 
        #'tif_unix.c',
        'tif_version.c', 
        'tif_warning.c', 
        'tif_write.c', 
        'tif_zip.c' ]

LIBS = []
if env['JPEG_SUPPORT'] or env['OJPEG_SUPPORT']:
    LIBS.append('jpeg')
if env['PIXARLOG_SUPPORT'] or env['ZIP_SUPPORT']:
    LIBS.append('z')

INCS = []

if env['PLATFORM'] in ['posix', 'cygwin', 'darwin', 'irix', 'sunos', 'hpux', 'aix']:
    SRCS.append('tif_unix.c')
elif env['PLATFORM'] in ['win32', 'nt', 'ce']:
    SRCS.append('tif_win32.c')
    env.MergeFlags('-includewindows.h -mwindows')
elif env['PLATFORM'] in ['mac']:
    SRCS.append('tif_apple.c')
elif env['PLATFORM'] in ['riscos']:
    SRCS.append('tif_acorn.h')
#elif env['PLATFORM'] in ['win16']:
#    SRCS.append('tif_win3.c')
#elif env['PLATFORM'] in ['msdos', 'dos']:
#    SRCS.append('tif_msdos.h')
#elif env['PLATFORM'] in ['atari']:
#    SRCS.append('tif_atari.h')
else:
     print("Platform '%s' not supported." % (env['PLATFORM'],))
     Exit(1)

SRCS = ['obj/'+x for x in SRCS]

libtiff = env.StaticLibrary('lib/tiff', SRCS, LIBS=LIBS)
#env.SharedLibrary('bin/tiff', SRCS, LIBS=LIBS)

Default(libtiff)

Alias('install-lib', env.Install(idir_lib, libtiff))
Alias('install-inc', env.Install(idir_inc, ['tiff.h', 'tiffconf.h', 'tiffio.h', 'tiffvers.h', 'tif_config.h']))
env.Alias('install', ['install-lib', 'install-inc'])
```

### Discussion

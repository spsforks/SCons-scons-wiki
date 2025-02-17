

## SConstruct for libjpeg

libjpeg is created by the [Independent JPEG Group](http://www.ijg.org/). Get the library itself [here](http://www.ijg.org/files/jpegsrc.v6b.tar.gz). This is setup to use MinGW by default.  If you want to use another compiler or OS you may need to play with it a bit, but not much. 


### Code


```python
#!python 
import os

env = Environment(ENV=os.environ)
Tool('mingw')(env)
env.Replace(CCFLAGS="-O2 -march=i686")

opts = Variables('jpeg.conf')
opts.Add(PathVariable('PREFIX', 'Directory to install under', 'c:/mingw'))
opts.Update(env)
opts.Save('jpeg.conf', env)

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

Execute(Copy("jconfig.h", "jconfig.vc"))

api = [
    "obj/jcapimin.c", # Application program interface: core routines for compression.
    "obj/jcapistd.c", # Application program interface: standard compression.
    "obj/jdapimin.c", # Application program interface: core routines for decompression.
    "obj/jdapistd.c", # Application program interface: standard decompression.
    "obj/jcomapi.c", # Application program interface routines common to compression and decompression.
    "obj/jcparam.c", # Compression parameter setting helper routines.
    "obj/jctrans.c", # API and library routines for transcoding compression.
    "obj/jdtrans.c", # API and library routines for transcoding decompression.
]

compression = [
    "obj/jcinit.c", # Initialization: determines which other modules to use.
    "obj/jcmaster.c", # Master control: setup and inter-pass sequencing logic.
    "obj/jcmainct.c", # Main buffer controller (preprocessor => JPEG compressor).
    "obj/jcprepct.c", # Preprocessor buffer controller.
    "obj/jccoefct.c", # Buffer controller for DCT coefficient buffer.
    "obj/jccolor.c", # Color space conversion.
    "obj/jcsample.c", # Downsampling.
    "obj/jcdctmgr.c", # DCT manager (DCT implementation selection & control).
    "obj/jfdctint.c", # Forward DCT using slow-but-accurate integer method.
    "obj/jfdctfst.c", # Forward DCT using faster, less accurate integer method.
    "obj/jfdctflt.c", # Forward DCT using floating-point arithmetic.
    "obj/jchuff.c", # Huffman entropy coding for sequential JPEG.
    "obj/jcphuff.c", # Huffman entropy coding for progressive JPEG.
    "obj/jcmarker.c", # JPEG marker writing.
    "obj/jdatadst.c", # Data destination manager for stdio output.
]

decompression = [
    "obj/jdmaster.c", # Master control: determines which other modules to use.
    "obj/jdinput.c", # Input controller: controls input processing modules.
    "obj/jdmainct.c", # Main buffer controller (JPEG decompressor => postprocessor).
    "obj/jdcoefct.c", # Buffer controller for DCT coefficient buffer.
    "obj/jdpostct.c", # Postprocessor buffer controller.
    "obj/jdmarker.c", # JPEG marker reading.
    "obj/jdhuff.c", # Huffman entropy decoding for sequential JPEG.
    "obj/jdphuff.c", # Huffman entropy decoding for progressive JPEG.
    "obj/jddctmgr.c", # IDCT manager (IDCT implementation selection & control).
    "obj/jidctint.c", # Inverse DCT using slow-but-accurate integer method.
    "obj/jidctfst.c", # Inverse DCT using faster, less accurate integer method.
    "obj/jidctflt.c", # Inverse DCT using floating-point arithmetic.
    "obj/jidctred.c", # Inverse DCTs with reduced-size outputs.
    "obj/jdsample.c", # Upsampling.
    "obj/jdcolor.c", # Color space conversion.
    "obj/jdmerge.c", # Merged upsampling/color conversion (faster, lower quality).
    "obj/jquant1.c", # One-pass color quantization using a fixed-spacing colormap.
    "obj/jquant2.c", # Two-pass color quantization using a custom-generated colormap. Also handles one-pass quantization to an externally given map.
    "obj/jdatasrc.c", # Data source manager for stdio input.
]

support = [
    "obj/jerror.c", # Standard error handling routines (application replaceable).
    "obj/jmemmgr.c", # System-independent (more or less) memory management code.
    "obj/jutils.c", # Miscellaneous utility routines.
    "obj/jmemnobs.c", # "No backing store": assumes adequate virtual memory exists.
]

libjpeg = env.StaticLibrary(target='lib/jpeg', source=api+compression+decompression+support)
Default(libjpeg)

cdjpeg = env.Object('obj/cdjpeg.c', LIBS=['jpeg'])
rdswitch = env.Object('obj/rdswitch.c', LIBS=['jpeg'])

cjpeg = env.Program(target='bin/cjpeg', 
                    source=['obj/cjpeg.c', cdjpeg, rdswitch, 
                            'obj/rdbmp.c', 'obj/rdgif.c', 'obj/rdppm.c', 'obj/rdrle.c', 'obj/rdtarga.c'],
                    LIBS=['jpeg'])

djpeg = env.Program(target='bin/djpeg',
                    source=['obj/djpeg.c', cdjpeg, 'obj/rdcolmap.c',
                            'obj/wrbmp.c', 'obj/wrgif.c', 'obj/wrppm.c', 'obj/wrrle.c', 'obj/wrtarga.c'],
                    LIBS=['jpeg'])

jpegtran = env.Program(target='bin/jpegtran',
                       source=['obj/jpegtran.c', cdjpeg, rdswitch, 'obj/transupp.c'],
                       LIBS=['jpeg'])

rdjpgcom = env.Program('bin/rdjpgcom', ['obj/rdjpgcom.c'])
wrjpgcom = env.Program('bin/wrjpgcom', ['obj/wrjpgcom.c'])

env.Alias('install-lib', env.Install(idir_lib, libjpeg))
env.Alias('install-inc', env.Install(idir_inc, ['jpeglib.h', 'jconfig.h', 'jmorecfg.h', 'jerror.h']))
env.Alias('install-bin', env.Install(idir_bin, [cjpeg, djpeg, jpegtran, rdjpgcom, wrjpgcom]))
env.Alias('install', ['install-lib', 'install-inc', 'install-bin'])
```

### Discussion



## SConstruct for SDL_image

The SDL_image homepage is [here](http://www.libsdl.org/projects/SDL_image/). This is setup to use MinGW by default.  If you want to use another compiler or OS you may need to play with it a bit, but not much. Because this is set to use static linking by default, you will need to link to libpng, libtiff, zlib and libjpeg (in that order) for any program built with the resulting library. Just make sure your program's lib list looks like showimage_LIBS and you'll be fine. After installation, the include file resides in "c:/mingw/include/SDL" by default, so use `#include <SDL/SDL_image.h>` in your code. 


### Code


```python
#!python 
import os

env = Environment(ENV=os.environ)
Tool('mingw')(env)
env.Replace(CCFLAGS="-O2 -march=i686")


opts = Variables('SDL_image.conf')

opts.Add(PathVariable('PREFIX', 'Directory to install under', 'c:/mingw', PathVariable.PathIsDir))
opts.Add(BoolVariable('LOAD_JPG', 'support loading JPG images', 1))
opts.Add(BoolVariable('LOAD_PNG', 'support loading PNG images', 1))
opts.Add(BoolVariable('LOAD_TIF', 'support loading TIFF images', 1))
opts.Add(BoolVariable('LOAD_BMP', 'support loading BMP images', 1))
opts.Add(BoolVariable('LOAD_GIF', 'support loading GIF images', 1))
opts.Add(BoolVariable('LOAD_LBM', 'support loading LBM images', 1))
opts.Add(BoolVariable('LOAD_PCX', 'support loading PCX images', 1))
opts.Add(BoolVariable('LOAD_PNM', 'support loading PNM images', 1))
opts.Add(BoolVariable('LOAD_TGA', 'support loading TGA images', 1))
opts.Add(BoolVariable('LOAD_XCF', 'support loading XCF images', 1))
opts.Add(BoolVariable('LOAD_XPM', 'support loading XPM images', 1))
opts.Add(BoolVariable('LOAD_XV', 'support loading XV images', 1))
opts.Add('LOAD_JPG_DYNAMIC', 'dynamically load JPG support', 0)
opts.Add('LOAD_PNG_DYNAMIC', 'dynamically load PNG support', 0)
opts.Add('LOAD_TIF_DYNAMIC', 'dynamically load TIFF support', 0)

opts.Update(env)
opts.Save('SDL_image.conf', env)
Help(opts.GenerateHelpText(env))

if env['LOAD_TIF'] and not env['LOAD_TIF_DYNAMIC']:
   env['LOAD_JPG_DYNAMIC'] = 0

if env['LOAD_JPG']: env.Append(CPPDEFINES={'LOAD_JPG': env['LOAD_JPG'] and 1 or 0})
if env['LOAD_PNG']: env.Append(CPPDEFINES={'LOAD_PNG': env['LOAD_PNG'] and 1 or 0})
if env['LOAD_TIF']: env.Append(CPPDEFINES={'LOAD_TIF': env['LOAD_TIF'] and 1 or 0})
if env['LOAD_BMP']: env.Append(CPPDEFINES={'LOAD_BMP': env['LOAD_BMP'] and 1 or 0})
if env['LOAD_GIF']: env.Append(CPPDEFINES={'LOAD_GIF': env['LOAD_GIF'] and 1 or 0})
if env['LOAD_LBM']: env.Append(CPPDEFINES={'LOAD_LBM': env['LOAD_LBM'] and 1 or 0})
if env['LOAD_PCX']: env.Append(CPPDEFINES={'LOAD_PCX': env['LOAD_PCX'] and 1 or 0})
if env['LOAD_PNM']: env.Append(CPPDEFINES={'LOAD_PNM': env['LOAD_PNM'] and 1 or 0})
if env['LOAD_TGA']: env.Append(CPPDEFINES={'LOAD_TGA': env['LOAD_TGA'] and 1 or 0})
if env['LOAD_XCF']: env.Append(CPPDEFINES={'LOAD_XCF': env['LOAD_XCF'] and 1 or 0})
if env['LOAD_XPM']: env.Append(CPPDEFINES={'LOAD_XPM': env['LOAD_XPM'] and 1 or 0})
if env['LOAD_XV']:  env.Append(CPPDEFINES={'LOAD_XV': env['LOAD_XV'] and 1 or 0})
if env['LOAD_JPG_DYNAMIC']: env.Append(CPPDEFINES={'LOAD_JPG_DYNAMIC': '"$LOAD_JPG_DYNAMIC"'})
if env['LOAD_PNG_DYNAMIC']: env.Append(CPPDEFINES={'LOAD_PNG_DYNAMIC': '"$LOAD_PNG_DYNAMIC"'})
if env['LOAD_TIF_DYNAMIC']: env.Append(CPPDEFINES={'LOAD_TIF_DYNAMIC': '"$LOAD_TIF_DYNAMIC"'})


idir_prefix = '$PREFIX'
idir_lib    = '$PREFIX/lib'
idir_bin    = '$PREFIX/bin'
idir_inc    = '$PREFIX/include'
idir_data   = '$PREFIX/share'
Export('env idir_prefix idir_lib idir_bin idir_inc idir_data')

env.Append(CPPPATH=Dir(idir_inc+"/SDL"))


VariantDir('bin', 'obj', duplicate=0)
VariantDir('lib', 'obj', duplicate=0)
VariantDir('obj', '.', duplicate=0)


libSDL_image_SOURCES = ['IMG.c',
                        'IMG_bmp.c',
                        'IMG_gif.c',
                        'IMG_jpg.c',
                        'IMG_lbm.c',
                        'IMG_pcx.c',
                        'IMG_png.c',
                        'IMG_pnm.c',
                        'IMG_tga.c',
                        'IMG_tif.c',
                        'IMG_xcf.c',
                        'IMG_xpm.c',
                        'IMG_xv.c']

libSDL_image_LIBS = ['SDL',]
if env['LOAD_PNG']:
   libSDL_image_LIBS.append('png')
if env['LOAD_TIF']:
   libSDL_image_LIBS.append('tiff')
if env['LOAD_PNG'] or env['LOAD_TIF']:
   libSDL_image_LIBS.append('z')
if env['LOAD_JPG'] or env['LOAD_TIF']:
   libSDL_image_LIBS.append('jpeg')

libSDL_image = env.StaticLibrary('lib/SDL_image', ['obj/'+x for x in libSDL_image_SOURCES], LIBS=libSDL_image_LIBS)


showimage_SOURCES = ['showimage.c']

showimage_LIBS = ['mingw32', 'SDLmain', libSDL_image]+libSDL_image_LIBS

showimage = env.Program('bin/showimage', ['obj/'+x for x in showimage_SOURCES], LIBS=showimage_LIBS)


Default(libSDL_image)


Alias('install-lib', env.Install(idir_lib, libSDL_image))
Alias('install-inc', env.Install(idir_inc+"/SDL", ['SDL_image.h']))
Alias('install-bin', env.Install(idir_bin, [showimage]))
Alias('install', ['install-lib', 'install-inc', 'install-bin'])
```

### Discussion

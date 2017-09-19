# About

The following tool, cuda (**cuda.py**) is for using the [CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit) by *NVidia*. See the end of the page for an example SConscript for building the _simpleGL_ sample that comes with the SDK and some notes. 


# The tool code

**Note:** code migrated to [scons-contrib](https://github.com/SConsProject/scons-contrib)!

# Sample

The SConscript for building _simpleGL_: 


```
#!python

env = Environment()
env.Tool('cuda')
env.Append(LIBS=['cutil', 'glut', 'GLEW'])

env.Program('simpleGL', ['simpleGL.cpp', 'simpleGL_kernel.cu'])
```

# Notes

The above tool has only been tested on Linux and Mac OS X. If your project doesn't use any of the above paths, you can specify 

```
#!python
env['CUDA_TOOLKIT_PATH'] = path to the CUDA Toolkit
env['CUDA_SDK_PATH'] = path to the CUDA SDK
```

If the tool finds the paths, it sets the above to the path it found. If you want to include CFLAGS for the _nvcc_, set the 

```
#!python
env['NVCCFLAGS'] = flags common to static and shared objects
env['STATICNVCCFLAGS'] = flags for static objects
env['SHAREDNVCCFLAGS'] = flags for shared objects
```
variables. The tool will include automatically the 'cudart' library in LIBS but not _cublas_ nor _cufft_ because you might not need them. Call env.Append as shown in the sample above to add extra libraries after calling `env.Tool('cuda')`. 


## Emitters

> This is an implementation detail, but i'm posting this too here. I'm not sure if this was the best thing to do, but it seems to work. I added two emitters for **.cu** files which modify the results of the _Scons.Defaults.Static/SharedObjectEmitter_ to also add _.linkinfo_ suffixed files as a target because the _nvcc_ compiler builds a **.o/.obj** and a **.linkinfo** from a **.cu** file and i needed to somehow tell to SCons to delete the **.linkinfo** files when _scons -c_ is issued. If you think of a better method for this, please inform me.

After discussions on the usage of the `*.linkinfo` files plus some googling, I came to the conclusion that the `*.linkinfo` files shouldn't be returned from the emitters because they were not used in the build chain: [NVidia DevTalk on linkinfo](https://devtalk.nvidia.com/default/topic/405518/linkinfo-files). - William Blevins

The implementation has been updated to add `*.linkinfo` files as side-effects rather than explicit emitter outputs, so that developers using those object builders do not need to filter the emitter returns.  Clean targets were added to the side-effect files; thus, resolving the original intention of `*.linkinfo` files being returned. - William Blevins

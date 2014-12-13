

# Teaching PDF to understand .lyx files

I have not had the time (nor the knowledge) to convert this to an extension. Feel free to do so and edit this page! 

The technique with add_src_builder could also help in other cases, sometimes asked at the mailing list. License: public domain.  

Notice two things:  

1. The path to the tex files must be available at creation time of Environment, otherwise the default PDF builder claims that he does not understand how to build pdf from tex. There should be a better error message. 
1. add_src_builder does not work like env.PDF.add_src_builder . See below how it's done. 

## Usage


```python
#!python
env = Environment(ENV=dict(PATH='/usr/texbin:/bin:/usr/bin'))  
if env['PLATFORM'] == "darwin":
    env.PrependENVPath( 'PATH', '/Applications/LyX.app/Contents/MacOS')

pdf = env.PDF(source='report.lyx')
```

## Implementation


```python
#!python
import SCons.Script
def namelyxtarget(target, source, env):
    '''The name of the output tex file is the same as the input.'''
    assert len(source) == 1, 'Lyx is single_srouce only.'
    s = str(source[0])
    if s.endswith('.lyx'): 
        target[0] = s[0:-4] +'.tex'
    return target, source
       
env.lyx = SCons.Script.Builder( action = 'lyx --export pdflatex $SOURCE', 
                                suffix = '.tex', src_suffix='.lyx', 
                                single_source=True, # file by file
                                emitter = namelyxtarget )
env.Append(BUILDERS = {'Lyx' : env.lyx})
 
# Teach PDF to understand lyx
env['BUILDERS']['PDF'].add_src_builder(env.lyx)
```
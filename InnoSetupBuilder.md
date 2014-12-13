
A quick hack to build Inno setups using iscc (the Inno Setup preprocessor): 


```python
#!python 
import SCons.Builder;
import os;

def runInno(source,target,env,for_signature):
    INNO_DEFINES=" ".join(['/D'+define for define in env['ISCCDEFINES']]);
    (TARGETDIR,TARGETFILE) = os.path.split(str(target[0]));
    return '%(ISCC)s %(SOURCE)s %(DEFINES)s /O "%(TARGETDIR)s" /F"%(TARGETFILE)s" %(ISCCOPTIONS)s ' % \
        {
            'ISCC':env['ISCC'],
            'ISCCOPTIONS':env['ISCCOPTIONS'],
            'DEFINES':INNO_DEFINES,
            'SOURCE':str(source[0]),
            'TARGETDIR':TARGETDIR,
            'TARGETFILE':TARGETFILE
        }

def generate(env,**kw):
    env['ISCC']='iscc';
    env['ISCCOPTIONS']='/q';
    env['ISCCDEFINES']=[];
    env['BUILDERS']['InnoInstaller'] = SCons.Builder.Builder( generator=runInno,
                                                                                        src_suffix='.iss');

def exists(env):
    return env.WhereIs("iscc");
```
In the SConstruct file: 


```python
#!python 
installer=env.InnoInstaller(target='setup_x64',source='setup_x64.iss',ISCCDEFINES=['APP_NAME="Your App Name"','APP_VERSION="10.4"']);
env.Depends(installer,ALL_THE_DEPENDENCIES); # need to do this manually since there is no dep scanner yet
```
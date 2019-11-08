
Some of our projects contain tar.gz archives of [OpenSource](OpenSource) projects that are used as dependencies. These projects are typically autotools based. This means that as part of the global build, the sequence of untar, configure and make needs to be triggered for each third-party tar.gz file. On this page, we define the first item: untar! 

First we define the unTarBuilder, refering to the [UnTar](UnTar) action, automatically adding the suffix '.tar.gz' to the string you use when invoking the [UnTar](UnTar) builder and using the tarContentsEmitter to create target nodes for all files within  the tar.gz file. 

Similar to Maven in the Java world, I do as much as possible within Python to prevent that we need a whole bunch of tools installed. As much as Python now, and in this case using the tarfile module to extract the tar files. 


```python
unTarBuilder = Builder(action=SCons.Action.Action(UnTar, UnTarString),
                       src_suffix='.tar.gz',
                       emitter=tarContentsEmitter)

thirdPartyEnvironment = Environment()
thirdPartyEnvironment.Append(BUILDERS = {'UnTar' : unTarBuilder})

thirdPartyEnvironment.UnTar(source = 'apr-1.3.3')
```
Let's have a look at the emitter first. I take the first source as the single  tar.gz file. Using the tarfile module, I read the entries in the tar file,  filter out the directories and convert the [TarInfo](TarInfo) objects to File nodes.  I filter out the directories since a Directory seems to have direct  dependencies on their contents. 


```python
def tarContentsEmitter(target, source, env):
    import tarfile
    sourceTar = tarfile.open(source[0].name,'r')
    tarContents = sourceTar.getmembers()
    tarFileContents = filter(lambda tarEntry: tarEntry.isfile(), tarContents)
    newTargets = map(tarInfoToNode, tarFileContents)
    sourceTar.close()
    return (newTargets, source)

def tarInfoToNode(tarInfoObject):
    return File(tarInfoObject.name)
```
Now for the Action. Similar to the emitter, the tarfile Python module is used to extract the contents. 


```python
def UnTar(target, source, env):
    # Code to build "target" from "source" here
    import tarfile
    sourceTar = tarfile.open(source[0].name,'r')
    sourceTar.extractall()
    sourceTar.close()
    return None
    
def UnTarString(target, source, env):
    """ Information string for UnTar """
    return 'Extracting %s' % os.path.basename (str (source[0]))
```
Open issues: 

* the emitter doesn't support multiple source tar.gz files yet. 
* since the emitter filters out the directories, running clean removes only the files. How can I get the clean functionality to also remove the complete folder structure? 
* No error handling in case the tarfile module would throw exceptions. 
Feel free adapt the code to remove some of the open issues. ;-) 

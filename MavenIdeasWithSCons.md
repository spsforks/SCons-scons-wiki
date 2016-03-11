**Using Some Maven Ideas And Best Practices With SCons**

**Table of Contents**

[TOC]

## Abstract

Up to now we used `make` to build most of our projects. However, in our new mid-size project we decided to use `scons` instead. Some requirements which had to be fulfilled are (as you will see, we tried to integrate some of the ideas introduced by the build tool [maven](http://maven.apache.org/)):  
Multimodule Projects
: The project has a hierarchical directory structure containing multiple subprojects, which in turn may have mutliple dependent modules. The build tool should be able to  recursively resolve dependencies between projects and modules in order to build a particular subproject at any level of the hierarchy. 

Short Setup Time
: Especially at early stages of the project numerous subprojects must be created. The development members, located at different subsidiaries, must be able to independently create new subprojects when needed. Thus the build tool should allow subproject creation with little setup effort without specifying the build process in an imperative or declarative way each time. 

Common Directory Structure
: 
A high number of subprojects requires a common directory structure based on best practices as introduced in `maven`. The build tool should support implementation of best practices by configuration of common source code, target, test code, resources ... directories. 


Model-Based Approach
: 
The directory structures of subprojects and modules are self similar. Thus the same logic can be used for builds at any hierarchical level. Consequently the build tool should enable to separate the build logic from the so called [p]roject [o]bject [m]odel (`maven` naming convention). The pom includes the name and version of the subproject, its dependencies and artifacts to build. 


Build Phases
: 
The pom fully specifies a piece of code. Given the pom various build phases like `compile`, `test`, `install`, `site` can be applied to the source code each resulting in a particular artifact. The build tool should be able to interpret and handle a pom to process the source code appropriately. 




## Approach

We integrated the build logic in a `SConstruct`, which is wrapped by a shell script. Thus for each subproject the developers only have to provide its name, version, type and dependencies and then call `sconswrapper compile`. It is very convenient, and it works fine for us. Next I would like to explain, how we use the script and what are the benefits of using it by means of an example. 


### Workflow

The wrapper script mentioned ... 

* checks, whether the current directory contains a `SConscript` (we use the name `pom.scons`, see below), 
* copies `SConstruc` from a dedicated directory to the current directory, 
* executes `scons`, 
* and finally deletes `SConstruct` from the current directory.  
We use it like in the following workflow example: 
Step 1
: 
Create new subproject `helloworld` including the common directory structure. 




```txt
project
|--helloworld
    |--src
       |--main
       |  |--c++ <-- source code goes here 
```

Step 2
: 
Create the corresponding pom for `helloworld` 



```txt
project
|--helloworld
    |--pom.scons <-- project object model
    |--src
       |--main
          |--c++
```

Step 3
: 
The `pom.scons` file is actually a `SConscript`. The following example defines the `Program` `helloworld` at version `0.9`. The `ext` key of the dependency `pthread` is set to `yes`, thus before building the artifact, the existance of the external library `phtread` is checked. The resulting artifact is copied (`exported`) to the common `bin` location. 




```
#!python 
# file: helloworld/pom.scons
# This SConscript contains no build logic but the project object model only. 
import os
import os.path
Import(['env', 'build'])
env = env.Copy()
env['pom']['group'] = ''
env['pom']['name'] = 'helloworld'
env['pom']['version'] = ' 0.9'
env['pom']['artifacts'] = 'Program'
env['pom']['deps'] = [
    {'group':'', 'name':'pthread', 'version':'', 'scopes':['compile'], 'ext':'yes'}] 
env['pom']['exports'] = [
    {'source':'main/helloworld-0.9', 'target':'helloworld', 'type':'bin'}]
targets = build(env)
Return('targets')
```

Step 4
: 
Build and install the program `helloworld`. By default `helloworld` will be copied to `$HOME/local/bin`. If the artifact would be a `SharedLibrary`, it would be copied to `$HOME/local/lib` by default and so on. 




```txt
# cd project/helloworld
# sconswrapper compile install
```

Step 5
: 
Now assume, `helloworld` depends on an internal library called `libhelloworld`. Create new subproject `libhelloworld` including the common directory structure. 




```txt
project
|--helloworld
|   |--pom.scons
|   |--src
|      |--main
|         |--c++
|--libhelloworld
    |--pom.scons
    |--src
       |--main
          |--c++ 
```

Step 6
: 
Create the corresponding pom for `libhelloworld`. 




```
#!python 
# file: libhelloworld/pom.scons
# This SConscript contains no build logic but the project object model only.
import os
import os.path
Import(['env', 'build']) 
env = env.Copy()
env['pom']['group'] = ''
env['pom']['name'] = 'libhelloworld'
env['pom']['version'] = '0.9'
env['pom']['artifacts'] = 'SharedLibrary' 
env['pom']['deps'] = [
    {'group':'', 'name':'pthread', 'version':'', 'scopes':['compile'], 'ext':'yes'}]
env['pom']['exports'] = [
    {'source':'main/libhelloworld- 0.9.so', 'target':'libhelloworld.so', 'type':'lib'}]
targets = build(env)
Return('targets')
```

Step 7
: 
Modify the project object model for `helloworld` by just adding new dependency `helloworld`, which is automatically expanded to `libhelloworld.so` by `scons`. The `ext` key is set to `no`, thus scons does not check the existence of the library before building. 




```
#!python 
# file: helloworld/pom.scons
# This SConscript contains no build logic but the project object model only.
import os
import os.path
Import(['env', 'build'])
env = env.Copy()
env['pom']['group'] = '' 
env['pom']['name'] = 'helloworld'
env['pom']['version'] = '0.9'
env['pom']['artifacts'] = 'Program'
env['pom']['deps'] = [
    {'group':'', 'name':'pthread', 'version':'', 'scopes':['compile'], 'ext':'yes'},
    {'group':'', 'name':'helloworld', 'version':'', 'scopes':['compile'], 'ext':'no'}] # new dependency
env['pom']['exports'] = [
    {'source':'main/helloworld-0.9', 'target':'helloworld', 'type':'bin'}] 
targets = build(env)
Return('targets')
```

Step 8
: 
Now assume, you don't want to build each artifact (`helloworld`, `libhelloworld`) manually, but let scons resolve the dependencies and build them  in the right order. Thus if you call `sconswrapper` at `project` level, `libhelloworld.so` should be built first, `helloworld` should be built next. For that to work simply add another pom for `project`. The artifact type `Meta` means: recursively search for subprojects and build them in the right order. 




```txt
project
|--pom.scons <-- pom for 'project'
|--helloworld
|   |--pom.scons
|   |--src
|      |--main
|         |--c++
|--libhelloworld
    |--pom.scons
    |--src
       |--main
          |--c++
```

```
#!python 
# file: pom.scons
# This SConscript contains no build logic but the project object model only.
import os
import os.path
Import(['env', 'build']) 
env = env.Copy()
env['pom']['group'] = ''
env['pom']['name'] = 'greeting'
env['pom']['version'] = '0.9'
env['pom']['artifacts'] = 'Meta' # artifact type 'Meta' 
env['pom']['deps'] = []
env['pom']['exports'] = []
targets = build(env)
Return('targets')
```

Step 9
: 
Build and install the top level project. As a result `libhelloworld` is built and copied to `$HOME/local/lib`. Next `helloworld` is built and copied to `$HOME/local/bin`.  




```txt
# cd project
# sconswrapper compile install
```

Step 10
: 
Create documentation. For this to work `doxygen` must be in the path. 




```txt
# cd project 
# sconswrapper site
```

Step 11
: 
Clean up. This deletes all created `target` directories. To remove artifacts, created by the current phase only, use `sconswrapper <phase> -c`. 




```txt
# cd project
# sconswrapper clean
```

## Sources

The [sources](https://bitbucket.org/scons/scons/wiki/MavenIdeasWithSCons/sources.zip) used in this Wiki: 
sconswrapper
: 
This is the shell wrapper script calling scons with `SConstruct`. 


SConstruct
: This is the scons script containing all build logic to interpret subproject specific project object models. 

pom.scons.template
: This is a commented template file for project object models. 



## Conclusion

Although it works fine for us, the `SConstruct` is by far not perfect. I am still new to `python` and `scons` and therefore would like to know your opinion on how to do things right. So if it sounds interesting to you or you have any questions or suggestions, please let me know. Any comments would be very much appreciated. 

-- [JakobScheck](JakobScheck) 2007-03-07 10:31:48 

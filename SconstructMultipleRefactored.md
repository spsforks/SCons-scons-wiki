
[SconstructMultiple](SconstructMultiple) has much redundancy in the Sconscripts and some redundancy in the Sconstruct. Some examples: 

* The list of variables to import/export is replicated in all sconscripts and in the sconstruct 
* the build sequence is done in all the sconscripts 
* the set up of the compile flags is done in all the sconscripts 
* etc. 
The new refactored sconstruct/sconscript below simplifies adding a new sub-project tremendously: 

1. cut and paste the sconscript to the new project directory.  
1. add a line **env.jDev.Subproject(project)** at the bottom of the sconstruct with the sub-project's name 
As the project matures, the sconstruct will get more complicated. The Dev class can be extended to handle the new complexity, keeping the sconscripts simple. If the Dev class becomes too large, it can be moved out of the Sconstruct into a separate .py file and/or it can be broken up into smaller classes. The sconscript files on the other hand should remain very simple. In the simple project setup below, the contents don't change at all from sub-project to sub-project. 

Here's the new Sconstruct: 
```python
from SCons.Script.SConscript import SConsEnvironment
import glob

# this is our catch-all Dev class
# it keeps track of all the variables and common functions we need
class Dev:
  mymode = ''
  debugcflags = ''
  releasecflags = ''

  #---
  # sets up the sconscript file for a given sub-project
  def Subproject(self, project):
      SConscript(env.jDev.SPath(project), exports=['project'])

  #sets up the build for a given project
  def Buildit(self, localenv, project):
     buildroot = '../' + env.jDev.mymode
     builddir = buildroot + '/' + project
     targetpath = builddir + '/' + project

     #append the user's additional compile flags
     #assume debugcflags and releasecflags are defined
     if self.mymode == 'debug':
         localenv.Append(CCFLAGS=self.debugcflags)
     else:
         localenv.Append(CCFLAGS=self.releasecflags)

     #specify the build directory
     localenv.VariantDir(builddir, ".", duplicate=0)

     srclst = map(lambda x: builddir + '/' + x, glob.glob('*.cpp'))
     pgm = localenv.Program(targetpath, source=srclst)
     env.Alias('all', pgm)  #note: not localenv

  #---- PRIVATE ----

  #---
  # return the sconscript path to use
  def SPath(self, project):
     return project + '/sconscript'

env = Environment()

# put all .sconsign files in one place
env.SConsignFile()

# we can put variables right into the environment, however
# we must watch out for name clashes.
SConsEnvironment.jDev = Dev()

# get the mode flag from the command line
# default to 'release' if the user didn't specify
env.jDev.mymode = ARGUMENTS.get('mode', 'release')   #holds current mode

# check if the user has been naughty: only 'debug' or 'release' allowed
if not (env.jDev.mymode in ['debug', 'release']):
   print "Error: expected 'debug' or 'release', found: " + env.jDev.mymode
   Exit(1)

# tell the user what we're doing
print '**** Compiling in ' + env.jDev.mymode + ' mode...'

env.jDev.debugcflags = ['-W1', '-GX', '-EHsc', '-D_DEBUG', '/MDd']   #extra compile flags for debug
env.jDev.releasecflags = ['-O2', '-EHsc', '-DNDEBUG', '/MD']         #extra compile flags for release

#make sure the sconscripts can get to the variables
#don't need to export anything but 'env'
Export('env')

#specify all of the sub-projects in the section
env.jDev.Subproject('myprogram')
env.jDev.Subproject('hisprogram')
env.jDev.Subproject('herprogram')
```
The new Sconstruct is more complicated, but it simplifies all the Sconscripts (they are all the same): 
```python
# get environment and project
Import('env', 'project')
localenv = env.Clone()

# call back to jDev to build the project for us
env.jDev.Buildit(localenv, project)
```

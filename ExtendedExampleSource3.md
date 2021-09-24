The `SConstruct` looks like this: 

```python
import os
import fnmatch

##-------------------------------------------------
# Use:
#   scons projectx [mode=debug]
#        - defaults to mode=release
##-------------------------------------------------

#-- lists of projects for various groupings
gFrozenDirProjects = []
gSrcDirProjects = []
gMiscDownloadsDirProjects = []

gDownloadsProjects = []
gMiscDownloadsProjects = []
gNeuralnetsProjects = []
gOtherProjects = []   #unclassified
#taskdefs
#snippets

##-------------------------------------------------
#-- Function definitions here
def GetConscriptPath(d, project):
    return '../' + d + '/' + project + '/sconscript'

def DoSrc(project, mode, group = gOtherProjects):
    gSrcDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('src', project), exports='project')

def DoMiscVC7(project, mode, group = gOtherProjects):
    gSrcDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('miscdownloads', project), exports='project')

def DoMiscVC6(project, mode, group = gOtherProjects):
    gSrcDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('miscdownloads', project), exports='project')

def DoSrcVC7(project, mode, group = gOtherProjects):
    gSrcDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('src', project), exports='project')

def DoSrcVC6(project, mode, group = gOtherProjects):
    gSrcDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('src', project), exports='project')

def DoFrozen(project, mode, group = gOtherProjects):
    gFrozenDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('frozen', project), variant_dir=dev.GetBuildDir(project, mode), exports='project')

def DoFrozenVC7(project, mode, group = gOtherProjects):
    gFrozenDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('frozen', project), exports='project')

def DoFrozenVC6(project, mode, group = gOtherProjects):
    gFrozenDirProjects.append(project)
    group.append(project)
    SConscript(GetConscriptPath('frozen', project), exports='project')

##-------------------------------------------------
#-- Dev Helper Class
class Dev(Environment):
   #-- get build directory
   def GetBuildDir(self, project, mode):
      return os.path.join('\projects', mode, project)

   #-- Get Source files from the source node using patterns as
   def GetSourceFiles(self, patterns=None):
      files = []
      if patterns is None:
         patterns=['*'+self["CXXFILESUFFIX"],'*'+self["CFILESUFFIX"], '*'+self["QT_UISUFFIX"]]
      for file in os.listdir(self.Dir('.').srcnode().abspath):
          for pattern in patterns:
             if fnmatch.fnmatchcase(file, pattern):
                 files.append(file)
      return files

   def SetAliases(self, e, projname, tgt):
       e.Alias(projname, tgt)
       e.Alias(projname.lower(), tgt)

   #-- set up a VC7 project to be built
   def VC7(self, localenv, project, slnname=None, exename=None, exetype=None):
      if slnname is None:  slnname = project
      if exename is None:  exename = project
      if exetype is None:  exetype = 'exe'
      localenv.PrependENVPath('PATH', 'E:/Program Files/Microsoft Visual Studio .NET 2003/Common7/IDE')
      bdir = self.GetBuildDir(project, mode)
      slnpath = slnname + '.sln'
      projpath =  os.path.join(bdir, exename + '.' + exetype)
      localenv.Tool('msvs')
      if mode == 'debug':
         cmd = localenv.Command(projpath, slnpath, 'devenv.exe /rebuild Debug $SOURCE')
      else:
         cmd = localenv.Command(projpath, slnpath, 'devenv.exe /rebuild Release $SOURCE')
      localenv.Clean(cmd, self.GetBuildDir(project, mode))
      return cmd

   #-- set up a VC6 project to be built
   #-- assumes:
   #--      - .dsp is in the source dir
   #--      - build_dir is not used
   #--      - exetype is one of exe, dll, lib
   def VC6(self, localenv, project, dspname=None, exename=None, exetype=None):
      if dspname is None:  dspname = project
      if exename is None:  exename = project
      if exetype is None:  exetype = 'exe'
      localenv.PrependENVPath('PATH', 'E:/Program Files/Microsoft Visual Studio/Common/MSDev98/Bin')
      bdir = self.GetBuildDir(project, mode)
      dsppath = dspname + '.dsp'
      projpath =  os.path.join(bdir, exename + '.' + exetype)
      localenv.Tool('msvc')
      if mode == 'debug':
         cmd = localenv.Command(projpath, dsppath, 'msdev.exe $SOURCE /MAKE "all - Win32 Debug" /NORECURSE /BUILD')
      else:
         cmd = localenv.Command(projpath, dsppath, 'msdev.exe $SOURCE /MAKE "all - Win32 Release" /NORECURSE /BUILD')
      localenv.Clean(cmd, bdir)
      return cmd

   def VC6_dsw(dev, localenv, project, dspname=None, exename=None, exetype=None):
      if dspname is None:  dspname = project
      if exename is None:  exename = project
      if exetype is None:  exetype = 'exe'
      localenv.PrependENVPath('PATH', 'E:/Program Files/Microsoft Visual Studio/Common/MSDev98/Bin')
      bdir = dev.GetBuildDir(project, mode)
      dsppath = dspname + '.dsw'
      projpath =  os.path.join(bdir, exename + '.' + exetype)
      localenv.Tool('msvc')
      if mode == 'debug':
         cmd = localenv.Command(projpath, dsppath, 'msdev.exe $SOURCE /MAKE "all - Win32 Debug" /NORECURSE /BUILD')
      else:
         cmd = localenv.Command(projpath, dsppath, 'msdev.exe $SOURCE /MAKE "all - Win32 Release" /NORECURSE /BUILD')
      localenv.Clean(cmd, bdir)
      return cmd

##-------------------------------------------------
#--
# prevent accidental building of everything;
# - to build everything use 'scons.py .'
Default(None)

##-------------------------------------------------
#- check compilation mode: 'debug' or 'release' only
mode = ARGUMENTS.get('mode', 'release')
if mode not in ['debug', 'release']:
   print "Error: expected 'debug' or 'release', found: " + mode
   Exit(1)

print '**** Compiling in ' + mode + ' mode...'

env = Environment()
dev = Dev()
Export('env', 'dev', 'mode')

#-- frozen projects
#astyle
DoFrozenVC7('ClassesInC', mode, gDownloadsProjects)
#com
DoFrozenVC7('DbDiff', mode, gDownloadsProjects)
#devutils
DoFrozenVC7('ExternalScrollbarListBox', mode, gDownloadsProjects)
DoFrozenVC7('Fave2Xml', mode, gDownloadsProjects)
#gensnippets
DoFrozenVC7('GenWeb', mode)
#genwebcore
DoFrozenVC7('jBackup', mode, gDownloadsProjects)
DoFrozenVC6('jComHeap', mode, gDownloadsProjects)
#jcomheap_test
DoFrozenVC7('jConfigureVC', mode, gDownloadsProjects)
DoFrozenVC7('jContinuousBackup', mode, gDownloadsProjects)
#jdump
DoFrozenVC7('jEnvEditor', mode, gDownloadsProjects)
DoFrozenVC7('jMirror', mode, gDownloadsProjects)
DoFrozenVC7('jPlayer', mode, gDownloadsProjects)
#jplayer - VC6
#jqwiki
DoFrozenVC7('jWebTest', mode, gDownloadsProjects)
#jwiki
DoFrozenVC7('MD5', mode, gDownloadsProjects)
#msdev
#perlvcaddin
DoFrozenVC7('RegDiff', mode, gDownloadsProjects)
DoFrozenVC7('ResumeMaster', mode)
#resumemastercore
DoFrozenVC7('SimpleXml', mode, gDownloadsProjects)
#sourcemonitor
DoFrozenVC7('SpreadSheet', mode, gDownloadsProjects)
#todo: resolve subdir name is 'ut', DoFrozenVC7('utx', mode, gDownloadsProjects)
DoFrozenVC7('W32Chat', mode, gDownloadsProjects)
#winmisc
#xml2tree

#-- miscdownloads
DoMiscVC6('BuildStamp', mode, gMiscDownloadsProjects)
DoMiscVC6('CIncl', mode, gMiscDownloadsProjects)
DoMiscVC7('KillProc', mode, gMiscDownloadsProjects)
DoMiscVC7('LogoffNicely', mode, gMiscDownloadsDirProjects)
DoMiscVC7('WordSearch', mode, gMiscDownloadsDirProjects)
DoMiscVC6('TestFsm', mode, gMiscDownloadsProjects)
DoMiscVC6('TestMsgLoop', mode, gMiscDownloadsProjects)
#OtherUtilities

#-- src projects
DoSrcVC6('CppWiki', mode)
DoSrcVC6('jUtAsserter', mode, gDownloadsProjects)
DoSrcVC6('jWebServer', mode, gDownloadsProjects)

#-- neuralnets
#-- todo:
#jneuralnetcore -- doesn't exist yet
#todo: resolve directory structure DoSrcVC7('jNeuralNets', mode, gNeuralnetsProjects)
DoSrc('pso', mode, gNeuralnetsProjects)


#--todo:
#jWebServer
#jsnippets
#jtaskdefs

#  &lt;!--missing java compiles: utjava, fsmgen, jwiki --&gt;
#  &lt;!--missing cpp  compiles: perlvcaddin, sourcemonitor --&gt;

#-- set up some other aliases for compilation convenience
env.Alias('frozen', gFrozenDirProjects)
env.Alias('src', gSrcDirProjects)
env.Alias('misc', gMiscDownloadsDirProjects)

env.Alias('downloads', gDownloadsProjects)
env.Alias('miscdownloads', gMiscDownloadsProjects)
env.Alias('neuralnets', gNeuralnetsProjects)
env.Alias('other', gOtherProjects)

env.Alias('all', ['downloads','miscdownloads', 'neuralnets', 'other'])
env.Alias('universe', ['all','frozen', 'src', 'misc'])
#-- end of compilation aliases

#-- targets
#todo: need to fill in all of the targets from the old Ant build.xml
#env.Alias('main', ['prepare_main', 'send_main'])

#-- Overall Aliases
env.Alias('prepare_xpsdorg', ['gather_xpsdorgwiki', 'gather_xpsdorghtml', 'convert_xpsdorg'])
env.Alias('prepare_cgi', ['prepare_cgimain', 'prepare_jwikipub', 'prepare_jwikipriv', 'prepare_ubu'])
env.Alias('prepare_html', ['prepare_main', 'prepare_testpages', 'prepare_private', 'prepare_links', 'prepare_snippets', 'prepare_resume', 'prepare_downloads', 'prepare_miscdownloads', 'prepare_taskdefs', 'prepare_neuralnets', 'prepare_articles'])
env.Alias('prepare_all', ['prepare_html', 'prepare_cgi', 'prepare_xpsdorg'])
env.Alias('publish', ['prepare_all', 'send_all'])

env.Alias('send_html', ['send_main', 'send_testpages', 'send_private', 'send_links', 'send_snippets', 'send_resume', 'send_downloads', 'send_miscdownloads', 'send_taskdefs', 'send_neuralnets', 'send_articles'])
env.Alias('send_cgi', ['send_cgimain', 'send_jwikipub', 'send_jwikipriv', 'send_ubu'])
env.Alias('send_all', ['send_html', 'send_cgi', 'send_xpsdorg'])
```
The sconscripts look like this: 
```python
Import('env', 'dev', 'project')
localenv = env.Clone()
tgt = dev.VC7(localenv, project)
localenv.Depends(tgt, dev.GetSourceFiles(['*.cpp', '*.h']))
dev.SetAliases(env, project, tgt)
```
The differences from this sconscript and others is the dev.VC7 line could call dev.VC6 and the Depends() may be more or less complicated. Later these will become much more project-specific and will probably include dependencies on other projects. 

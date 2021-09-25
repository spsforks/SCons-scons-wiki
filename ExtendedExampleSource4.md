See also [SconsProjects](SconsProjects) for lots more real-life SCons examples. 

`SConstruct`: 


```txt
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
   #--      - variant_dir is not used
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
if not (mode in ['debug', 'release']):
   print "Error: expected 'debug' or 'release', found: " + mode
   Exit(1)

print '**** Compiling in ' + mode + ' mode...'

env = Environment()
dev = Dev()
Export('env', 'dev', 'mode')

#put all .sconsign files in one place
env.SConsignFile()

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

# <!--missing java compiles: utjava, fsmgen, jwiki -->
# <!--missing cpp compiles: perlvcaddin, sourcemonitor -->

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

# <target name='compile_all' depends='init,
#         compile_downloads,
#         compile_miscdownloads,
#         compile_snippets,
#         compile_taskdefs,
#         compile_neuralnets'
# />


#-- end of compilation aliases


#-- targets
def GetFiles(dir, includes, excludes=None):
      files = []
      for file in os.listdir(Dir(dir).srcnode().abspath):
          for pattern in includes:
             if fnmatch.fnmatchcase(file, pattern):
                 files.append(file)
      if not excludes is None:
        for file in files:
           for pattern in excludes:
              if fnmatch.fnmatchcase(file, pattern):
                  files.remove(file)
      return files

def InstallFiles(env, dest_dir, src_dir, includes, excludes):
   src = GetFiles(src_dir, includes, excludes)
   #print "x=" + `src`
   dest = env.Dir(dest_dir)
   for f in src:
      env.Install(dest, src_dir + '/' + f)
   return dest

def InstallTree(env, dest_dir, src_dir, includes, excludes):
    destnode = env.Dir(dest_dir)
    dirs = []
    dirs.append(src_dir)
    while len(dirs) > 0:
      currdir = dirs.pop(0)
      currdestdir = dest_dir + currdir[len(src_dir):]
      #print "c=" + currdestdir
      flist = os.listdir(currdir)
      for currfile in flist:
         currpath = currdir + '/' + currfile
         match = 0
         for pattern in includes:
            if fnmatch.fnmatchcase(currfile, pattern):
              match = 1
         if (match == 1):
            for pattern in excludes:
               if fnmatch.fnmatchcase(currfile, pattern):
                  match = 0
            if (match == 1):
               if (os.path.isdir(currpath)):
                  #print "d=" + currpath
                  dirs.append(currpath)
               else:
                  #print "f=" + currpath
                  env.Install(currdestdir, currpath)
      #print "x= len=" + str(len(dirs))
    return destnode

#-- source dirs
arrizza_websrc_root = '/projects/websrc/arrizza'
arrizza_resume_root = '/MyStuff/myresume'
frozen_root = '/projects/frozen'

#-- staging local dirs
arrizza_local_root       = '/projects/staging/arrizza.com'
arrizza_local_html       = arrizza_local_root + '/html'
arrizza_local_cgibin     = arrizza_local_root + '/cgi-bin'
arrizza_local_private    = arrizza_local_html + '/private'
arrizza_local_links      = arrizza_local_html + '/links'
arrizza_local_snippets   = arrizza_local_html + '/snippets'
arrizza_local_taskdefs   = arrizza_local_html + '/taskdefs'
arrizza_local_resume     = arrizza_local_html + '/resume'
arrizza_local_downloads  = arrizza_local_html + '/downloads'
arrizza_local_miscdownloads = arrizza_local_html + '/miscdownloads'
arrizza_local_neuralnets = arrizza_local_html + '/neuralnets'
arrizza_local_articles   = arrizza_local_html + '/articles'
arrizza_local_testpages  = arrizza_local_html + '/testpages'
arrizza_local_jwikipriv  = arrizza_local_cgibin + '/jwikipriv'
arrizza_local_jwikipub   = arrizza_local_cgibin + '/jwikipub'
arrizza_local_jwikitest  = arrizza_local_cgibin + '/jwikitest'
arrizza_local_ubu        = arrizza_local_cgibin + '/ubu'

#------------ MAIN ---------------------
env.Alias('prepare_main', [
     InstallFiles(env,
        dest_dir = arrizza_local_root,
        src_dir  = arrizza_websrc_root + '/main',
        includes = ['*'],
        excludes = ['.svn']),
     InstallFiles(env,
        dest_dir = arrizza_local_html,
        src_dir  = arrizza_websrc_root + '/htmlmain',
        includes = ['*'],
        excludes = ['.svn'])
      ])
env.Alias('main', ['prepare_main', 'send_main'])

#------------ TESTPAGES ---------------------
env.Alias('prepare_testpages', [
     InstallFiles(env,
        dest_dir = arrizza_local_testpages,
        src_dir  = arrizza_websrc_root + '/testpages',
        includes = ['*'],
        excludes = ['.svn'])
      ])
env.Alias('testpages', ['prepare_testpages', 'send_testpages'])

#------------ CGI MAIN ---------------------
env.Alias('prepare_cgimain', [
     InstallFiles(env,
        dest_dir = arrizza_local_cgibin,
        src_dir  = arrizza_websrc_root + '/cgi-bin',
        includes = ['*'],
        excludes = ['.svn'])
      ])
env.Alias('cgimain', ['prepare_cgimain', 'send_cgimain'])

#------------ PRIVATE ---------------------
env.Alias('prepare_private', [
     InstallFiles(env,
        dest_dir = arrizza_local_private,
        src_dir  = arrizza_websrc_root + '/private',
        includes = ['*'],
        excludes = ['.svn'])
      ])
env.Alias('private', ['prepare_private', 'send_private'])

#------------ ARTICLES ---------------------
env.Alias('prepare_articles', [
     InstallFiles(env,
        dest_dir = arrizza_local_articles,
        src_dir  = arrizza_websrc_root + '/articles',
        includes = ['*'],
        excludes = ['.svn'])
      ])
env.Alias('articles', ['prepare_articles', 'send_articles'])

#------------ RESUME ---------------------
env.Alias('prepare_resume', [
     env.InstallAs(arrizza_local_resume + '/johnarrizzawebresume.txt', arrizza_resume_root + '/JohnArrizzawebResume.txt'),
     env.InstallAs(arrizza_local_resume + '/johnarrizzaresume.txt',    arrizza_resume_root + '/JohnArrizzawebResume.txt'),
     env.InstallAs(arrizza_local_resume + '/johnarrizzawebresume.doc', arrizza_resume_root + '/JohnArrizzawebResume.doc'),
     env.InstallAs(arrizza_local_resume + '/johnarrizzaresume.doc',    arrizza_resume_root + '/JohnArrizzawebResume.doc'),
     env.Install(arrizza_local_resume, arrizza_resume_root + '/resume.html'),
     env.Install(arrizza_local_resume, arrizza_resume_root + '/uofccoatofarms.jpg'),
     InstallFiles(env,
        dest_dir = arrizza_local_resume,
        src_dir  = arrizza_websrc_root + '/resume',
        includes = ['*'],
        excludes = ['.svn'])
      ])
env.Alias('resume', ['prepare_resume', 'send_resume'])

#------------ LINKS ---------------------
env.Alias('prepare_links', [
     env.Install(arrizza_local_links, frozen_root + '/fave2xml/links.html'),
      ])
env.Alias('links', ['prepare_links', 'send_links'])

#------------ UBU ---------------------
env.Alias('prepare_ubu', [
     InstallTree(env,
        dest_dir = arrizza_local_ubu,
        src_dir  = arrizza_websrc_root + '/ubu',
        includes = ['*'],
        excludes = ['.svn', '*.pag', '*.log'])
      ])
env.Alias('ubu', ['prepare_ubu', 'send_ubu'])

#------------ jwiki ---------------------
#  locdir: local staging directory
#  srcdir: directory under where extra stuff is held
#  cgifile: filename of the cgifile...
#def gather_jwiki(locdir, srcdir, cgifile):

# <delete dir='${locdir}' />
# <mkdir dir='${locdir}' />
# <!-- copy the base code -->
# <copy todir='${locdir}' preservelastmodified='yes' overwrite='true'>
# <fileset dir='${frozendir}/jqwiki' includes='**/' excludes='db/**'/>
# </copy>
# <!-- overwrite with extra stuff -->
# <copy todir='${locdir}' preservelastmodified='yes' overwrite='true'>
# <fileset dir='${srcdir}' includes='**/' excludes='db/**'/>
# </copy>
# <delete file='${locdir}/qwiki.cgi' />
# <delete file='${locdir}/jqwiki.html' />
# <delete file='${locdir}/jqwiki.cgi' />
# <delete file='${locdir}/jqwiki.cpr' />
# <delete file='${locdir}/jqwiki.PRJ' />
# <delete file='${locdir}/bin/bakit.bat' />
# <delete file='${locdir}/bin/test.bat' />
# <move file='${locdir}/${cgifile}' tofile='${local.cgibin}/${cgifile}' />


#------------ jwiki ---------------------
# <target name='gather_jwikipub' depends='init'>
# <antcall target="gather_jwiki">
# <param name='locdir' value='${local.jwikipub}'/>
# <param name='srcdir' value='${arrizza.websrc}/jwikipub'/>
# <param name='cgifile' value='pub'/>
# </antcall>
# </target>

# env.Alias('prepare_jwikipub', [
#      InstallFiles(env,
#         dest_dir = arrizza_local_articles,
#         src_dir  = arrizza_websrc_root + '/articles',
#         includes = ['*'],
#         excludes = ['.svn'])
#       ])
env.Alias('jwikipub', ['prepare_jwikipub', 'send_jwikipub'])


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
sconscripts haven't changed from the last time. Here's a typical one: 
```txt
Import('env', 'dev', 'project')
localenv = env.Clone()
tgt = dev.VC7(localenv, project)
localenv.Depends(tgt, dev.GetSourceFiles(['*.cpp', '*.h']))
dev.SetAliases(env, project, tgt)
```

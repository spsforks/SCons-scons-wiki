
Here's the SConstruct: 
```txt
from SCons.Script.SConscript import SConsEnvironment 
#import SCons.Script 
import os 
import fnmatch 
import copy 
 
##------------------------------------------------- 
# Use: 
#   scons projectx [mode=debug] 
#        - defaults to mode=release 
##------------------------------------------------- 
 
class Config: 
    #-- source dirs 
    arrizza_websrc_root = '/projects/websrc/arrizza' 
    arrizza_resume_root = '/MyStuff/myresume' 
    frozen_root = '/projects/frozen' 
    taskdefs_root = frozen_root + '/com/arrizza/ant/taskdefs' 
    src_root = '/projects/src' 
    misc_root = '/projects/miscdownloads' 
 
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
 
#-- lists of projects for various groupings 
gFrozenDirProjects = [] 
gSrcDirProjects = [] 
gMiscDownloadsDirProjects = [] 
 
gDownloadsProjects = [] 
gMiscDownloadsProjects = [] 
gNeuralnetsProjects = [] 
gOtherProjects = []   #unclassified 
gNotCompiledProjects = [] 
#taskdefs 
#snippets 
 
 
##------------------------------------------------- 
##-- 
 
#--- 
class HtmlGenerator: 
    def Html(self, f): 
        f.write('<html>\n') 
    def CloseHtml(self, f): 
        f.write('</html>\n') 
    def Body(self, f): 
        f.write('  <body>\n') 
    def CloseBody(self, f): 
        f.write('  </body>\n') 
    def Head(self, f): 
        f.write('  <head>\n') 
    def CloseHead(self, f): 
        f.write('  </head>\n') 
    def ContentHeader(self, f): 
        f.write('    <META http-equiv="Content-Type" content="text/html; charset=iso-8859-1">\n') 
    def H1(self, f, msg): 
        f.write('    <h1>' + msg + '</h1>\n') 
    def H2(self, f, msg): 
        f.write('    <h2>' + msg + '</h2>\n') 
    def ol(self, f): 
        f.write('           <ol>\n') 
    def olclose(self, f): 
        f.write('           </ol>\n') 
    def li(self, f, item): 
        f.write('             <li>' + item + '</li>\n') 
    def Title(self, f, title): 
        if title is None: 
           print "   Title   : n/a" 
        else: 
           print "   Title   : " + title 
           f.write('    <title>' + title + '</title>\n') 
    def Description(self, f, desc): 
        if desc is None: 
           print "   Desc    : n/a" 
        else: 
           print "   Desc    : " + desc 
           f.write('    <META name="description" content="' + desc + '" >\n') 
    def Keywords(self, f, keywords): 
        if keywords is None: 
           print "   Keywords: n/a" 
        else: 
           print "   Keywords: " + keywords 
           f.write('    <META name="keywords" content="' + keywords + '" >\n') 
    def StyleSheet(self, f): 
        f.write('    <style>\n') 
        f.write('       table { margin:0px; cell-spacing:0px; padding:0px;  color:blue }\n') 
        f.write('       td    { margin:0px; cell-spacing:0px; padding:0px;  }\n') 
        f.write('       tr    { margin:0px; cell-spacing:0px; padding:0px;  }\n') 
        f.write('       h1    {}\n') 
        f.write('       a     { margin:0px; cell-spacing:0px; padding:0px;  }\n') 
        f.write('       h2    { font:large; border-top: solid darkblue 3px; }\n') 
        f.write('       h4    { font:large; margin:0px; cell-spacing:0px; padding:0px 0px 0px 8px; background-color:lightblue; border-top: solid darkblue 3px; border-left: solid darkblue 3px; }\n') 
        f.write('       hr    { background-color:lightblue; }\n') 
        f.write('    </style>\n') 
 
#--- 
class HtmlInfo: 
    hgen = HtmlGenerator() 
 
    project = None          # project name 
    title = None            # title of generated html page 
    desc = None             # description of project 
    status = None           # current status 
    keywords = None         # html keywords 
    dest_root = None        # root dir where generated html page will reside 
    htmlpage = None         # file name of generated html page 
    src_root = None         # directory where the notes html page (if any) resides 
    src_htmlpage = None     # file name of notes html page 
    changes = []            # list of strings showing changes done to this project 
    installation = []       # list of strings showing installation steps user needs to do 
    zipfiles=[]             # files to put into the zip file 
    showfiles=[]            # files to display in the _files html page 
 
    def ResetInfo(self): 
      self.project = None 
      self.title = None 
      self.desc = None 
      self.status = None 
      self.keywords = None 
      self.dest_root = None 
      self.htmlpage = None 
      self.src_root = None 
      self.src_htmlpage = None 
      self.changes = [] 
      self.installation = [] 
      self.zipfiles=[] 
      self.showfiles=[] 
 
      #calculated 
      self.dest_htmlpage = None 
      self.dest_filespage = None 
      self.zipfilename = None 
      self.zipfile = None 
 
    def CalcInfo(self): 
      self.dest_htmlpage = self.dest_root + '/' + self.htmlpage 
      self.dest_filespage = self.dest_root + '/_files.html' 
      self.zipfilename = self.project + '.zip' 
      self.zipfile = self.dest_root + '/' + self.zipfilename 
 
    def Html(self, f): 
        self.hgen.Html(f) 
    def CloseHtml(self, f): 
        self.hgen.CloseHtml(f) 
    def Body(self, f): 
        self.hgen.Body(f) 
    def CloseBody(self, f): 
        self.hgen.CloseBody(f) 
 
    def GenHead(self, f): 
        self.hgen.Head(f) 
        self.hgen.ContentHeader(f) 
        self.hgen.Title(f, self.title) 
        self.hgen.Description(f, self.desc) 
        self.hgen.Keywords(f, self.keywords) 
        self.hgen.StyleSheet(f) 
        self.hgen.CloseHead(f) 
 
    def GenBodyTitle(self, f): 
        if self.title is None and self.desc is None: 
          pass 
        elif self.title is None: 
          self.hgen.H1(f, self.desc) 
        elif self.desc is None: 
          self.hgen.H1(f, self.title) 
        else: 
          self.hgen.H1(f, self.title + ' : ' + self.desc) 
 
    def GenChangesOn(self, f): 
        if self.changes is None or len(self.changes) == 0: 
           print "   Change  : n/a" 
        else: 
           self.hgen.H2(f, 'Changes') 
           self.hgen.ol(f) 
           for change in self.changes: 
              print "   Change  : " + str(change) 
              self.hgen.li(f, str(change)) 
           self.hgen.olclose(f) 
 
    def GenInstallationOn(self, f): 
        self.hgen.H2(f, 'Installation') 
        if self.installation is None or len(self.installation) == 0: 
           print "   Install : None." 
           f.write('        None.<br>\n') 
        else: 
           self.hgen.ol(f) 
           for step in self.installation: 
              print "   Install : " + str(step) 
              self.hgen.li(f, str(step)) 
           self.hgen.olclose(f) 
 
    def GenNotesOn(self, f): 
        if not os.path.isfile(self.src_htmlpage): 
           print "   ERROR: source html page " + self.src_htmlpage + ' is not a file.' 
        else: 
           self.hgen.H2(f, 'Notes') 
           g = open(self.src_htmlpage) 
           f.writelines(g.readlines()) 
           g.close() 
 
    def GenSynopsisOn(self, f): 
         f.write('        <table border="1">\n') 
         f.write('           <tr><td><a name="synopsis"></a><h4>Synopsis:</h4></td></tr>\n') 
         for file in self.showfiles: 
            print "   File    : " + str(file) 
            d, filename = os.path.split(str(file)) 
            f.write('           <tr><td><a href="#' + filename + '">' + filename + '</a></td></tr>\n') 
         f.write('        </table><br>\n') 
 
    def GenFileDisplayOn(self, f): 
         f.write('        <table>\n') 
         for file in self.showfiles: 
            d, filename = os.path.split(str(file)) 
            f.write('           <tr><td><table cols="2">\n') 
            f.write('               <tr><td><a name="' + filename + '"></a><h4>' + filename + '</h4></td><td align="left" width="20%"></td></tr>\n') 
            f.write('               <tr><td><a href="#synopsis">Back to Synopsis</a><br></td></tr>\n') 
            f.write('             </table></td></tr>\n') 
            f.write('           <tr><td><pre>\n') 
            g = open(str(file)) 
            f.writelines(g.readlines()) 
            g.close() 
            f.write('           </pre></td></tr>\n') 
         f.write('        </table><br>\n') 
 
class DownloadsHelper(HtmlInfo): 
   mEntriesList = []  # holds all pages for the downloads index page 
   mInstallList = [] 
 
   #public: initialize 
   def Reset(self): 
      self.mInstallList = [] 
      self.ResetInfo() 
 
   def Gen(self, env): 
      self.CalcInfo() 
      self.mInstallList = [] 
      hi = copy.deepcopy(self) 
      self.mInstallList.append(env.PageBuilder(target = self.dest_htmlpage, source = [Value(hi)])) 
      self.mInstallList.append(env.Zip(self.zipfile, self.zipfiles, ZIPNOPATH=1)) 
      self.mInstallList.append(env.FilePageBuilder(target = self.dest_filespage, source = [Value(hi)])) 
      #print "x=appending: " + self.project 
      self.mEntriesList.append([self.project + '/' + self.htmlpage, self.title, self.status, self.desc]) 
 
   def Install(self, env, dest_dir, src_path): 
      self.mInstallList.append(env.Install(dest_dir, src_path)) 
 
   def Alias(self, env): 
      prepalias = env.jAlias('prepare_' + self.project, self.mInstallList, "prepare '" + self.project + "' project page") 
      env.jAlias('prepare_downloads', prepalias, "prepare 'downloads' html page") 
      env.Clean(prepalias, env.Dir(self.dest_root)) 
 
   def GenMainPage(self, env): 
      hix = copy.deepcopy(self.mEntriesList) 
      env.jAlias('prepare_downloads', 
           env.DownloadsBuilder(target = [dev.cfg.arrizza_local_downloads + '/downloads.html'], source = [Value(hix)])) 
      env.Clean('prepare_downloads', env.Dir(dev.cfg.arrizza_local_downloads)) 
 
class MiscDownloadsHelper(HtmlInfo): 
   mEntriesList = []  # holds all pages for the miscdownloads index page 
   mInstallList = [] 
 
   #public: initialize 
   def Reset(self): 
      self.mInstallList = [] 
      self.ResetInfo() 
 
   def Gen(self, env): 
      self.CalcInfo() 
      self.mInstallList = [] 
      hi = copy.deepcopy(self) 
      self.mInstallList.append(env.PageBuilder(target = self.dest_htmlpage, source = [Value(hi)])) 
      self.mInstallList.append(env.Zip(self.zipfile, self.zipfiles, ZIPNOPATH=1)) 
      self.mInstallList.append(env.FilePageBuilder(target = self.dest_filespage, source = [Value(hi)])) 
      #print "x=appending: " + self.project 
      self.mEntriesList.append([self.project + '/' + self.htmlpage, self.title, self.status, self.desc]) 
 
   def Install(self, env, dest_dir, src_path): 
      self.mInstallList.append(env.Install(dest_dir, src_path)) 
 
   def Alias(self, env): 
      prepalias = env.jAlias('prepare_' + self.project, self.mInstallList, "prepare '" + self.project + "' miscdownloads project page") 
      env.jAlias('prepare_miscdownloads', prepalias, "prepare 'miscdownloads' html page") 
      env.Clean(prepalias, env.Dir(self.dest_root)) 
 
   def GenMainPage(self, env): 
      hix = copy.deepcopy(self.mEntriesList) 
      env.jAlias('prepare_miscdownloads', 
               env.MiscDownloadsBuilder(target = [dev.cfg.arrizza_local_miscdownloads + '/miscdownloads.html'], source = [Value(hix)])) 
      env.Clean('prepare_miscdownloads', env.Dir(dev.cfg.arrizza_local_miscdownloads)) 
 
class NeuralnetsHelper(HtmlInfo): 
   mEntriesList = []  # holds all pages for the neuralnets index page 
   mInstallList = [] 
 
   #public: initialize 
   def Reset(self): 
      self.mInstallList = [] 
      self.ResetInfo() 
 
   def Gen(self, env): 
      self.CalcInfo() 
      self.mInstallList = [] 
      hi = copy.deepcopy(self) 
      self.mInstallList.append(env.PageBuilder(target = self.dest_htmlpage, source = [Value(hi)])) 
      self.mInstallList.append(env.Zip(self.zipfile, self.zipfiles, ZIPNOPATH=1)) 
      self.mInstallList.append(env.FilePageBuilder(target = self.dest_filespage, source = [Value(hi)])) 
      #print "x=appending: " + self.project 
      self.mEntriesList.append([self.project + '/' + self.htmlpage, self.title, self.status, self.desc]) 
 
   def Install(self, env, dest_dir, src_path): 
      self.mInstallList.append(env.Install(dest_dir, src_path)) 
 
   def Alias(self, env): 
      prepalias = env.jAlias('prepare_' + self.project, self.mInstallList, "prepare '" + self.project + "' neuralnets project page") 
      env.jAlias('prepare_neuralnets', prepalias, "prepare neuralnets html page") 
      env.Clean(prepalias, env.Dir(self.dest_root)) 
 
   def GenMainPage(self, env): 
      hix = copy.deepcopy(self.mEntriesList) 
      env.jAlias('prepare_neuralnets', 
           env.NeuralnetsBuilder(target = [dev.cfg.arrizza_local_neuralnets + '/neuralnets.html'], source = [Value(hix)])) 
      env.Clean('prepare_neuralnets', env.Dir(dev.cfg.arrizza_local_neuralnets)) 
 
class TaskdefsHelper(HtmlInfo): 
   mEntriesList = []  # holds all pages for the neuralnets index page 
   mInstallList = [] 
 
   #public: initialize 
   def Reset(self): 
      self.mInstallList = [] 
      self.ResetInfo() 
 
   def Gen(self, env): 
      self.CalcInfo() 
      self.mInstallList = [] 
      hi = copy.deepcopy(self) 
      self.mInstallList.append(env.PageBuilder(target = self.dest_htmlpage, source = [Value(hi)])) 
      self.mInstallList.append(env.Zip(self.zipfile, self.zipfiles, ZIPNOPATH=1)) 
      self.mInstallList.append(env.FilePageBuilder(target = self.dest_filespage, source = [Value(hi)])) 
      #print "x=appending: " + self.project 
      self.mEntriesList.append([self.project + '/' + self.htmlpage, self.title, self.status, self.desc]) 
 
   def Install(self, env, dest_dir, src_path): 
      self.mInstallList.append(env.Install(dest_dir, src_path)) 
 
   def Alias(self, env): 
      prepalias = env.jAlias('prepare_' + self.project, self.mInstallList, "prepare '" + self.project + "' taskdefs project page") 
      env.jAlias('prepare_taskdefs', prepalias, "prepare taskdefs page") 
      env.Clean(prepalias, env.Dir(self.dest_root)) 
 
   def GenMainPage(self, env): 
      hix = copy.deepcopy(self.mEntriesList) 
      env.jAlias('prepare_taskdefs', 
           env.TaskdefsBuilder(target = [dev.cfg.arrizza_local_taskdefs + '/taskdefs.html'], source = [Value(hix)])) 
      env.Clean('prepare_taskdefs', env.Dir(dev.cfg.arrizza_local_taskdefs)) 
 
#-------------- 
class FileList: 
  mFileList = {} 
  mDestInstallList = [] 
 
  #public: empty the list 
  def Reset(self): 
      self.mFileList.clear() 
      self.mDestInstallList = [] 
 
  #public: prints the current list 
  def Dump(self): 
     for f in self.mFileList.keys(): 
         print f + '=> ' + self.mFileList[f][0] + '   ' + self.mFileList[f][1] 
 
  #public: add given file to dest_dir 
  def AddFile(self, dest_dir, src_dir, file): 
     self.mFileList[src_dir + '/' + file] = (dest_dir, file) 
 
  #public: add given list of files to dest_dir 
  def AddFiles(self, dest_dir, src_dir, files): 
     for file in files: 
        self.mFileList[src_dir + '/' + file] = (dest_dir, file) 
 
  #public: gets all files from the src_dir directory and adds them to the list 
  #        no sub-directory recursion is done 
  def AddDir(self, dest_dir, src_dir, includes, excludes=None): 
      for file in os.listdir(Dir(src_dir).srcnode().abspath): 
          fqpath = src_dir + '/' + file 
          if (os.path.isdir(fqpath)):  continue   #don't do subdirs 
          if self.Matches(file, includes, excludes): 
             self.mFileList[fqpath] = (dest_dir, file) 
 
  #public: gets all files from the src_dir tree and adds it to the list 
  #        duplicate destinations are possible. See OverwriteFromTree. 
  def AddTree(self, dest_dir, src_dir, includes, excludes): 
      dirs = [] 
      dirs.append(src_dir) 
      while len(dirs) > 0: 
        currdir = dirs.pop(0) 
        currdestdir = dest_dir + currdir[len(src_dir):] 
        for currfile in os.listdir(currdir): 
           currpath = currdir + '/' + currfile 
           if self.Matches(currfile, includes, excludes): 
               if (os.path.isdir(currpath)): 
                   dirs.append(currpath) 
               else: 
                   self.mFileList[currpath] = (currdestdir, currfile) 
 
  #public: gets all files from the src_dir tree and puts them in the list 
  #        if there already is a matching destination file 
  #             it is deleted and a new entry is added with the src_dir 
  #   Using this function is equivalent to copying a directory tree overtop 
  #   of an existing tree. All matching files, would be overwritten 
  def OverwriteFromTree(self, dest_dir, src_dir, includes, excludes): 
      dirs = [] 
      dirs.append(src_dir) 
      while len(dirs) > 0: 
        currdir = dirs.pop(0) 
        currdestdir = dest_dir + currdir[len(src_dir):] 
        for currfile in os.listdir(currdir): 
           currpath = currdir + '/' + currfile 
           if self.Matches(currfile, includes, excludes): 
               if (os.path.isdir(currpath)): 
                   dirs.append(currpath) 
               else: 
                   for v in self.mFileList.keys(): 
                      if self.mFileList[v] == (currdestdir, currfile): 
                          del self.mFileList[v] 
                          break 
                   #it's either a new file or we just deleted the old one and we can create the new one 
                   self.mFileList[currpath] = (currdestdir, currfile) 
 
  #public: take the src file and change its destination directory 
  def Move(self, src_dir, file, dest_dir): 
     self.mFileList[src_dir + '/' + file] = (dest_dir, file) 
 
  #public: returns the current list of files 
  def Get(self): 
     return self.mFileList 
 
  #public: takes the current list of files and Installs them 
  def Install(self, env): 
     for f in self.mFileList.keys(): 
         self.mDestInstallList.append(env.Install(self.mFileList[f][0], f)) 
 
  def InstallFileAs(self, env, dest_path, src_path): 
     self.mDestInstallList.append(env.InstallAs(dest_path, src_path)) 
 
  #public: takes the current list of destination dirs and associates them with a given aliasname 
  #        any additional sub-directories to cleanup can be passed in in cleandirlist 
  def Alias(self, env, aliasname, cleandirlist = None): 
     tmp = env.jAlias(aliasname, self.mDestInstallList) 
     if not cleandirlist is None: 
        env.Clean(tmp, cleandirlist) 
 
  #private function: returns true if file is 
  #   1) matched by a pattern in 'includes' 
  #    -AND- 
  #  2) NOT matched by a pattern in 'excludes' 
  def Matches(self, file, includes, excludes): 
      match = 0 
      for pattern in includes: 
         if fnmatch.fnmatchcase(file, pattern): 
             match = 1 
             break 
      if match == 1 and not excludes is None: 
          for pattern in excludes: 
              if fnmatch.fnmatchcase(file, pattern): 
                  match = 0 
                  break 
      return match 
 
#------------------ 
class SimpleFileList: 
  mFileList = [] 
 
  #public: empty the list 
  def Reset(self): 
      self.mFileList = [] 
 
  #public: prints the current list 
  def Dump(self): 
     for f in self.mFileList: 
         print f 
 
  #public: gets all files from the src_dir tree and adds it to the list 
  #        duplicate destinations are possible. See OverwriteFromTree. 
  def AddTree(self, src_dir, includes = None, excludes = None): 
      dirs = [] 
      dirs.append(src_dir) 
      if includes is None: includes = '*' 
      while len(dirs) > 0: 
        currdir = dirs.pop(0) 
        for currfile in os.listdir(currdir): 
           currpath = currdir + '/' + currfile 
           if self.Matches(currfile, includes, excludes): 
               if (os.path.isdir(currpath)): 
                   dirs.append(currpath) 
               else: 
                   self.mFileList.append(currpath) 
 
  #public: returns the current list of files 
  def Get(self): 
     return self.mFileList 
 
  #private function: returns true if file is 
  #   1) matched by a pattern in 'includes' 
  #    -AND- 
  #  2) NOT matched by a pattern in 'excludes' 
  def Matches(self, file, includes, excludes): 
      match = 0 
      for pattern in includes: 
         if fnmatch.fnmatchcase(file, pattern): 
             match = 1 
             break 
      if match == 1 and not excludes is None: 
          for pattern in excludes: 
              if fnmatch.fnmatchcase(file, pattern): 
                  match = 0 
                  break 
      return match 
 
 
 
##------------------------------------------------- 
#-- Dev Helper Class 
class Dev(Environment): 
    dh = DownloadsHelper() 
    mdh = MiscDownloadsHelper() 
    nnh = NeuralnetsHelper() 
    tdh = TaskdefsHelper() 
    fl = FileList() 
    sfl = SimpleFileList() 
    cfg = Config() 
    mode = 'notset' 
 
    #-- get build directory 
    def GetBuildDir(self, project): 
        return os.path.join('\projects', self.mode, project) 
 
    #-- get sconscript path based on root directory and project name 
    def GetConscriptPath(self, d, project): 
        return '../' + d + '/' + project + '/sconscript' 
 
    def DoIt(self, project, srcgroup, group, dir, srcdir = None): 
        srcgroup.append(project) 
        group.append(project) 
        if srcdir is None: srcdir = project 
        SConscript(self.GetConscriptPath(dir, srcdir), exports='project') 
 
    def DoSrc(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gSrcDirProjects, group, 'src', srcdir) 
 
    def DoMiscVC7(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gSrcDirProjects, group, 'miscdownloads', srcdir) 
 
    def DoMiscVC6(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gSrcDirProjects, group, 'miscdownloads', srcdir) 
 
    def DoSrcVC7(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gSrcDirProjects, group, 'src', srcdir) 
 
    def DoSrcVC6(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gSrcDirProjects, group, 'src', srcdir) 
 
    def DoSrcNotBuilt(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gSrcDirProjects, group, 'src', srcdir) 
 
    def DoFrozen(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gFrozenDirProjects, group, 'frozen', srcdir) 
 
    def DoFrozenVC7(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gFrozenDirProjects, group, 'frozen', srcdir) 
 
    def DoFrozenVC6(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gFrozenDirProjects, group, 'frozen', srcdir) 
 
    def DoFrozenNotBuilt(self, project, group = gOtherProjects, srcdir = None): 
        self.DoIt(project, gFrozenDirProjects, group, 'frozen', srcdir) 
 
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
       e.jAlias(projname, tgt) 
       e.jAlias(projname.lower(), tgt, "compile " + projname) 
 
    #-- set up a VC6 project to be built 
    #-- assumes: 
    #--      - .dsp is in the source dir 
    #--      - build_dir is not used 
    #--      - exetype is one of exe, dll, lib 
    def VC6(self, e, project, dspname=None, exename=None, exetype=None): 
      self.compile_VC6('.dsp', e, project, dspname, exename, exetype) 
 
    #-- set up a VC6 project to be built 
    #-- assumes: 
    #--      - .dsw is in the source dir 
    #--      - build_dir is not used 
    #--      - exetype is one of exe, dll, lib 
    def VC6_dsw(self, e, project, dspname=None, exename=None, exetype=None): 
      self.compile_VC6('.dsw', e, project, dspname, exename, exetype) 
 
    #-- set up a VC7 project to be built 
    def VC7(self, e, project, slnname=None, exename=None, exetype=None, builddir=None): 
      if slnname is None:  slnname = project 
      if exename is None:  exename = project 
      if exetype is None:  exetype = 'exe' 
      self.compile_setpath(e, 'E:/Program Files/Microsoft Visual Studio .NET 2003/Common7/IDE') 
      self.compile_settool(e, 'msvs') 
      if builddir is None: 
        bdir = self.GetBuildDir(project) 
      else: 
        bdir = builddir 
      slnpath = slnname + '.sln' 
      projpath =  os.path.join(bdir, exename + '.' + exetype) 
      if dev.mode == 'debug': 
         type = 'Debug' 
      else: 
         type = 'Release' 
      cmd = e.Command(projpath, slnpath, 'devenv.exe /rebuild ' + type + ' $SOURCE') 
      e.Clean(cmd, bdir) 
      return cmd 
 
    #private: common builder for vc6 
    def compile_VC6(self, suffix, e, project, dspname=None, exename=None, exetype=None, builddir = None): 
      if dspname is None:  dspname = project 
      if exename is None:  exename = project 
      if exetype is None:  exetype = 'exe' 
      self.compile_setpath(e, 'E:/Program Files/Microsoft Visual Studio/Common/MSDev98/Bin') 
      self.compile_settool(e, 'msvc') 
      if builddir is None: 
        bdir = self.GetBuildDir(project) 
      else: 
        bdir = builddir 
      dsppath = dspname + suffix 
      projpath =  os.path.join(bdir, exename + '.' + exetype) 
      if dev.mode == 'debug': 
         type = 'Debug' 
      else: 
         type = 'Release' 
      cmd = e.Command(projpath, dsppath, 'msdev.exe $SOURCE /MAKE "all - Win32 ' + type + '" /NORECURSE /BUILD') 
      e.Clean(cmd, bdir) 
      return cmd 
 
    #private: set path 
    def compile_setpath(self, e, path): 
      e.PrependENVPath('PATH', path) 
 
    #private: set tool 
    def compile_settool(self, e, tool): 
      e.Tool(tool) 
 
##------------------------------------------------- 
#-- 
# prevent accidental building of everything; 
# - to build everything use 'scons.py .' 
Default(None) 
 
##------------------------------------------------- 
#-- helper functions and variables 
#-- ------------------ 
#-- jDataClass holds data for the helper functions 
class jDataClass: 
    mHelpText = {} 
    mHelpTextHead = [] 
    mHelpTextTail = [] 
SConsEnvironment.jData = jDataClass() 
#-- ------------------ 
#-- wraps Alias to put the alias name in the help text 
def jAlias(self, thealias, tgt, helptext=None): 
   self.Alias(thealias, tgt) 
   a = thealias.lower() 
   if helptext is None: 
       if not self.jData.mHelpText.has_key(a): 
          self.jData.mHelpText[a] = '???' 
   else: 
       self.jData.mHelpText[a] = helptext 
SConsEnvironment.jAlias = jAlias 
#-- ------------------ 
#-- adds a line of text to the help heading 
def jHelpHead(self, msg): 
   self.jData.mHelpTextHead.append(msg); 
SConsEnvironment.jHelpHead = jHelpHead 
#-- ------------------ 
#-- adds a line of text to the help footing 
def jHelpFoot(self, msg): 
   self.jData.mHelpTextTail.append(msg); 
SConsEnvironment.jHelpFoot = jHelpFoot 
#-- ------------------ 
#-- generates the help 
def jGenHelp(self): 
   tmp = [] 
   tmp.extend(self.jData.mHelpTextHead) 
   keys = self.jData.mHelpText.keys() 
   keys.sort() 
   maxlen = 0 
   for a in keys: 
      if len(a) > maxlen: maxlen = len(a) 
   for a in keys: 
      s = '   %-*s : %s' % (maxlen, a, self.jData.mHelpText[a]) 
      tmp.append(s) 
   tmp.extend(self.jData.mHelpTextTail) 
   self.Help("\n".join(tmp)) 
SConsEnvironment.jGenHelp = jGenHelp 
#-- ------------------ 
#-- adds upper/lower case of alias names for a target 
def jSetAliases(self, projname, tgt): 
   self.jAlias(projname, tgt) 
   self.jAlias(projname.lower(), tgt, "compile " + projname) 
SConsEnvironment.jSetAliases = jSetAliases 
 
#SConsEnvironment.dev = Dev() 
 
env = Environment() 
env.jHelpHead("First line of Help...") 
env.jHelpFoot("Last line of Help...") 
 
dev = Dev() 
Export('env', 'dev') 
 
##------------------------------------------------- 
#- check compilation mode: 'debug' or 'release' only 
dev.mode = ARGUMENTS.get('mode', 'release') 
if not (dev.mode in ['debug', 'release']): 
   print "Error: expected 'debug' or 'release', found: " + dev.mode 
   Exit(1) 
 
print '**** Compiling in ' + dev.mode + ' mode...' 
 
#put all .sconsign files in one place 
env.SConsignFile() 
 
#--- 
def string_downloadspage(target, source, env): 
    return "Building index page  : '%s'" % target[0] 
 
#--- 
def build_downloadspage(target, source, env): 
    f = open(str(target[0]), 'w') 
    entries = source[0].value 
    hgen = HtmlGenerator() 
    hgen.Html(f) 
    hgen.Head(f) 
    hgen.Title(f, 'Downloads') 
    hgen.ContentHeader(f) 
    hgen.Description(f, 'code samples for utilities in C++, C#, Java and Perl') 
    hgen.Keywords(f, 'astyle, classes in C, DB diff, external scrollbar, fsm generator, continuous backup, configure vcproj,environment editor with undo, website tester, wiki, MD5, perl from a VC addin, mp3 player, regdiff, resume master, signal processing, sourcemonitor, unit testers, w32 chat') 
    hgen.CloseHead(f) 
    hgen.Body(f) 
    hgen.H1(f, 'Downloads') 
    f.write('    This is a set of utilities and other code that I''m currently working on.\n') 
    f.write('    <p>See <a href="../statusdesc.html">here</a> for a description of the statuses</p><p>Any web/html output will work with IE6 with all service packs applied.\n') 
    f.write('     All other browsers, versions, etc. may or may not work. This is especially true\n') 
    f.write('     for XSLT scripts.</p><p>Some code was found on the net and modified. I''ve tried to indicate this\n') 
    f.write('     as best I can, there may be ommissions and apologies.</p>\n') 
    f.write('<p><table border="1" cellpadding="4" cellspacing="0" style="border-style:solid; border-width:thin; margin=0px;">\n') 
    for entry in entries: 
        print "   Download: " + str(entry[1]) 
        f.write('   <tr><td style="background:lightgreen; text-align:left">') 
        f.write('<a href="' + entry[0] + '">' + entry[1] + '</a></td><td>' + entry[2] + '</td><td>' + entry[3] + '</td></tr>\n') 
    f.write('</table></p>\n') 
    f.write('  <p>Contact Information <a href="mailto:admin@arrizza.com">admin@arrizza.com</a></p>\n') 
    hgen.CloseBody(f) 
    hgen.CloseHtml(f) 
    f.close() 
    return 0 
 
#--- 
def string_miscdownloadspage(target, source, env): 
    return "Building index page  : '%s'" % target[0] 
 
#--- 
def build_miscdownloadspage(target, source, env): 
    f = open(str(target[0]), 'w') 
    entries = source[0].value 
    hgen = HtmlGenerator() 
    hgen.Html(f) 
    hgen.Head(f) 
    hgen.Title(f, 'Misc. Downloads') 
    hgen.ContentHeader(f) 
    hgen.Description(f, 'more code samples for utilities in C++, C#, Java and Perl') 
    hgen.Keywords(f, 'astyle, classes in C, DB diff, external scrollbar, fsm generator, continuous backup, configure vcproj,environment editor with undo, website tester, wiki, MD5, perl from a VC addin, mp3 player, regdiff, resume master, signal processing, sourcemonitor, unit testers, w32 chat') 
    hgen.CloseHead(f) 
    hgen.Body(f) 
    hgen.H1(f, 'Misc. Downloads') 
    f.write('    This is a set of utilities and other code that I''ve found on the net or elsewhere.\n') 
    f.write('    I have modified the source... or not.\n') 
    f.write('    <p>I''ve tried to indicate where I found the foce, but I may not have been able to determine its original source.\n') 
    f.write('    Again: there may be ommissions and apologies.</p>\n') 
    f.write('    <p>See <a href="../statusdesc.html">here</a> for a description of the statuses</p>\n') 
    f.write('    <p>Any web/html output will work with IE6 with all service packs applied.\n') 
    f.write('    All other browsers, versions, etc. may or may not work. This is especially true for XSLT scripts.<\p>\n') 
    f.write('<p><table border="1" cellpadding="4" cellspacing="0" style="border-style:solid; border-width:thin; margin=0px;">\n') 
    for entry in entries: 
        print "   Download: " + str(entry[1]) 
        f.write('   <tr><td style="background:lightgreen; text-align:left">') 
        f.write('<a href="' + entry[0] + '">' + entry[1] + '</a></td><td>' + entry[2] + '</td><td>' + entry[3] + '</td></tr>\n') 
    f.write('</table></p>\n') 
    f.write('  <p>Contact Information <a href="mailto:admin@arrizza.com">admin@arrizza.com</a></p>\n') 
    hgen.CloseBody(f) 
    hgen.CloseHtml(f) 
    f.close() 
    return 0 
 
#--- 
def string_neuralnetspage(target, source, env): 
    return "Building index page  : '%s'" % target[0] 
 
#--- 
def build_neuralnetspage(target, source, env): 
    f = open(str(target[0]), 'w') 
    entries = source[0].value 
    hgen = HtmlGenerator() 
    hgen.Html(f) 
    hgen.Head(f) 
    hgen.Title(f, 'Neural Nets') 
    hgen.ContentHeader(f) 
    hgen.Description(f, 'a neural net tic tac toe game') 
    hgen.Keywords(f, 'tic tac toe, neural net, C#') 
    hgen.CloseHead(f) 
    hgen.Body(f) 
    hgen.H1(f, 'Neural Net Samples') 
    f.write('    This is a set of neural net samples. They use TicTacToe as motivation\n') 
    f.write('    for showing how neural nets can be used.\n') 
    f.write('    <p>There are (will be) several versions the game with varying degrees\n') 
    f.write('    of neural net use. The first will simply be TicTacToe without any\n') 
    f.write('    NNs used. This is just to get the GUI and internal software\n') 
    f.write('    architecture correct before adding NN into the mix.\n') 
    f.write('    <p>See <a href="../statusdesc.html">here</a> for a description of the statuses</p>\n') 
    f.write('<p><table border="1" cellpadding="4" cellspacing="0" style="border-style:solid; border-width:thin; margin=0px;">\n') 
    for entry in entries: 
        print "   Download: " + str(entry[1]) 
        f.write('   <tr><td style="background:lightgreen; text-align:left">') 
        f.write('<a href="' + entry[0] + '">' + entry[1] + '</a></td><td>' + entry[2] + '</td><td>' + entry[3] + '</td></tr>\n') 
    f.write('</table></p>\n') 
    f.write('  <p>Contact Information <a href="mailto:admin@arrizza.com">admin@arrizza.com</a></p>\n') 
    hgen.CloseBody(f) 
    hgen.CloseHtml(f) 
    f.close() 
    return 0 
 
#--- 
def string_taskdefspage(target, source, env): 
    return "Building index page  : '%s'" % target[0] 
 
#--- 
def build_taskdefspage(target, source, env): 
    f = open(str(target[0]), 'w') 
    entries = source[0].value 
    hgen = HtmlGenerator() 
    hgen.Html(f) 
    hgen.Head(f) 
    hgen.Title(f, 'Ant Taskdef Downloads') 
    hgen.ContentHeader(f) 
    hgen.Description(f, 'various ANT taskdefs') 
    hgen.Keywords(f, 'Ant, Ant taskdefs, contatenate, csharp, ftpmirror, nunit, regasm, vb6, vbunit, vc6, vc7') 
    hgen.CloseHead(f) 
    hgen.Body(f) 
    hgen.H1(f, 'Ant Taskdef Downloads') 
    f.write('    This is a set of Ant taskdefs I am currently working on.\n') 
    f.write('    <p>See <a href="../statusdesc.html">here</a> for a description of the statuses</p>\n') 
    f.write('<p><table border="1" cellpadding="4" cellspacing="0" style="border-style:solid; border-width:thin; margin=0px;">\n') 
    for entry in entries: 
        print "   Download: " + str(entry[1]) 
        f.write('   <tr><td style="background:lightgreen; text-align:left">') 
        f.write('<a href="' + entry[0] + '">' + entry[1] + '</a></td><td>' + entry[2] + '</td><td>' + entry[3] + '</td></tr>\n') 
    f.write('</table></p>\n') 
    f.write('  <p>Contact Information <a href="mailto:admin@arrizza.com">admin@arrizza.com</a></p>\n') 
    hgen.CloseBody(f) 
    hgen.CloseHtml(f) 
    f.close() 
    return 0 
 
#--- 
def string_mainpage(target, source, env): 
    return "Building project page: %s '%s'" % (source[0].value.title, target[0]) 
#--- 
def build_mainpage(target, source, env): 
    f = open(str(target[0]), 'w') 
    hinfo = source[0].value 
    hinfo.Html(f) 
    hinfo.GenHead(f) 
    hinfo.Body(f) 
    hinfo.GenBodyTitle(f) 
    f.write('        <a href="_files.html">Download Files</a><br>\n') 
    hinfo.GenChangesOn(f) 
    hinfo.GenInstallationOn(f) 
    hinfo.GenNotesOn(f) 
    hinfo.CloseBody(f) 
    hinfo.CloseHtml(f) 
    f.close() 
    return 0 
 
#--- 
def string_filepage(target, source, env): 
    return "Building files page  : %s '%s'" % (source[0].value.title, target[0]) 
#--- 
def build_filepage(target, source, env): 
    f = open(str(target[0]), 'w') 
    hinfo = source[0].value 
    hinfo.Html(f) 
    hinfo.GenHead(f) 
    hinfo.Body(f) 
    hinfo.GenBodyTitle(f) 
    f.write('        <a href="' + hinfo.zipfilename + '">Download ' + hinfo.zipfilename + '</a><br>\n') 
    if hinfo.showfiles is None or len(hinfo.showfiles) == 0: 
       print "Files   : n/a" 
    else: 
       hinfo.GenSynopsisOn(f) 
       hinfo.GenFileDisplayOn(f) 
    hinfo.CloseBody(f) 
    hinfo.CloseHtml(f) 
    f.close() 
    return 0 
 
env.Append(BUILDERS = {'DownloadsBuilder' : Builder(action = Action(build_downloadspage, string_downloadspage))}) 
env.Append(BUILDERS = {'MiscDownloadsBuilder' : Builder(action = Action(build_miscdownloadspage, string_miscdownloadspage))}) 
env.Append(BUILDERS = {'NeuralnetsBuilder' : Builder(action = Action(build_neuralnetspage, string_neuralnetspage))}) 
env.Append(BUILDERS = {'TaskdefsBuilder' : Builder(action = Action(build_taskdefspage, string_taskdefspage))}) 
env.Append(BUILDERS = {'PageBuilder' : Builder(action = Action(build_mainpage, string_mainpage))}) 
env.Append(BUILDERS = {'FilePageBuilder' : Builder(action = Action(build_filepage, string_filepage))}) 
 
 
#-- frozen projects 
dev.DoFrozenNotBuilt('AStyle', gNotCompiledProjects) 
dev.DoFrozenVC7('ClassesInC', gDownloadsProjects) 
#com 
dev.DoFrozenVC7('DbDiff', gDownloadsProjects) 
dev.DoFrozenNotBuilt('DevUtils', gNotCompiledProjects) 
dev.DoFrozenVC7('ExternalScrollbarListBox', gDownloadsProjects) 
dev.DoFrozenVC7('Fave2Xml', gDownloadsProjects) 
#gensnippets 
#dev.DoFrozenVC7('GenWeb') # not needed anymore, not published 
#genwebcore                # not needed anymore, not published 
dev.DoFrozenVC7('jBackup', gDownloadsProjects) 
dev.DoFrozenVC6('jComHeap', gDownloadsProjects) 
#jcomheap_test 
dev.DoFrozenVC7('jConfigureVC', gDownloadsProjects) 
dev.DoFrozenVC7('jContinuousBackup', gDownloadsProjects) 
dev.DoFrozenNotBuilt('jConvert', gNotCompiledProjects) 
dev.DoFrozenNotBuilt('jDump', gNotCompiledProjects) 
dev.DoFrozenVC7('jEnvEditor', gDownloadsProjects) 
dev.DoFrozenNotBuilt('jFtpMirror', gNotCompiledProjects) 
dev.DoFrozenVC7('jMirror', gDownloadsProjects) 
dev.DoFrozenVC7('jPlayer', gDownloadsProjects) 
#jplayer - VC6 
dev.DoFrozenNotBuilt('jQWiki', gNotCompiledProjects) 
dev.DoFrozenVC7('jWebTest', gDownloadsProjects) 
dev.DoFrozenNotBuilt('jWiki', gNotCompiledProjects) 
dev.DoFrozenVC7('MD5', gDownloadsProjects) 
#msdev 
dev.DoFrozenNotBuilt('PerlVCAddin', gNotCompiledProjects) 
dev.DoFrozenVC7('RegDiff', gDownloadsProjects) 
dev.DoFrozenVC7('ResumeMaster') 
#resumemastercore 
dev.DoFrozenVC7('SimpleXml', gDownloadsProjects) 
dev.DoFrozenNotBuilt('SourceMonitor', gNotCompiledProjects) 
dev.DoFrozenVC7('SpreadSheet', gDownloadsProjects) 
dev.DoFrozenVC7('utx', gDownloadsProjects, srcdir='ut') 
#DoFrozenNotBuilt('utcs', gDownloadsProjects, srcdir='ut/utcs') 
dev.DoFrozenNotBuilt('utJava', gNotCompiledProjects, srcdir='ut/utjava') 
dev.DoFrozenNotBuilt('utPerl', gNotCompiledProjects, srcdir='ut/utperl') 
 
dev.DoFrozenVC7('W32Chat', gDownloadsProjects) 
dev.DoFrozenNotBuilt('WinMisc', gNotCompiledProjects) 
dev.DoFrozenNotBuilt('Xml2Tree', gNotCompiledProjects) 
 
#-- miscdownloads 
dev.DoMiscVC6('BuildStamp', gMiscDownloadsProjects) 
dev.DoMiscVC6('CIncl', gMiscDownloadsProjects) 
dev.DoMiscVC7('KillProc', gMiscDownloadsProjects) 
dev.DoMiscVC7('LogoffNicely', gMiscDownloadsDirProjects) 
dev.DoMiscVC7('WordSearch', gMiscDownloadsDirProjects) 
dev.DoMiscVC6('TestFsm', gMiscDownloadsProjects) 
dev.DoMiscVC6('TestMsgLoop', gMiscDownloadsProjects) 
#OtherUtilities 
 
#-- src projects 
dev.DoSrcVC6('CppWiki') 
dev.DoSrcVC6('jUtAsserter', gDownloadsProjects) 
dev.DoSrcVC6('jWebServer', gDownloadsProjects) 
dev.DoSrcNotBuilt('FSMGen', gNotCompiledProjects) 
dev.DoSrcNotBuilt('SignalProcessing', gNotCompiledProjects) 
 
#--todo: 
#jsnippets 
#jtaskdefs 
project = 'taskdefs' 
SConscript('/projects/frozen/com/arrizza/ant/sconscript', exports='project') 
 
#-- neuralnets 
dev.DoSrcVC7('tictactoe', gNeuralnetsProjects, srcdir='jneuralnets') 
dev.DoSrc('pso', gNeuralnetsProjects) 
 
#  <!--missing java compiles: utjava, fsmgen, jwiki --> 
#  <!--missing cpp  compiles: perlvcaddin, sourcemonitor --> 
 
#-- set up some other aliases for compilation convenience 
env.jAlias('compile_frozen', gFrozenDirProjects, 'compile all projects in frozen sub-directory') 
env.jAlias('compile_src', gSrcDirProjects, 'compile all projects in src sub-directory') 
env.jAlias('compile_misc', gMiscDownloadsDirProjects, 'compile all projects in miscdownloads sub-directory') 
 
env.jAlias('compile_downloads', gDownloadsProjects, 'compile all projects downloads group') 
env.jAlias('compile_miscdownloads', gMiscDownloadsProjects, 'compile all projects in miscdownloads group') 
env.jAlias('compile_neuralnets', gNeuralnetsProjects, 'compile all projects in neural nets group') 
env.jAlias('compile_other', gOtherProjects, 'compile all projects in others group') 
 
env.jAlias('compile_all', ['compile_downloads','compile_miscdownloads', 'compile_neuralnets', 'compile_other'], 'compile all projects in all groups') 
#todo: tries to compile non-compilable entities 
#env.jAlias('compile_universe', ['compile_all','compile_frozen', 'compile_src', 'compile_misc']) 
 
#-- end of compilation aliases 
 
#------------ MAIN --------------------- 
dev.fl.Reset() 
dev.fl.AddDir(dest_dir = dev.cfg.arrizza_local_root, 
                   src_dir = dev.cfg.arrizza_websrc_root + '/main', 
                   includes= ['*'], 
                   excludes= ['.svn']) 
dev.fl.AddDir(dest_dir = dev.cfg.arrizza_local_html, 
                   src_dir = dev.cfg.arrizza_websrc_root + '/htmlmain', 
                   includes= ['*'], 
                   excludes= ['.svn']) 
dev.fl.Install(env) 
dev.fl.Alias(env, 'prepare_main') 
env.jAlias('main', ['prepare_main', 'send_main'], 'build web entities in main page') 
 
#------------ TESTPAGES --------------------- 
dev.fl.Reset() 
dev.fl.AddDir(dest_dir = dev.cfg.arrizza_local_testpages, 
                   src_dir = dev.cfg.arrizza_websrc_root + '/testpages', 
                   includes= ['*'], 
                   excludes= ['.svn']) 
dev.fl.Install(env) 
dev.fl.Alias(env, 'prepare_testpages', [dev.cfg.arrizza_local_testpages]) 
env.jAlias('testpages', ['prepare_testpages', 'send_testpages'], 'build web entities in testpages page') 
 
#------------ CGI MAIN --------------------- 
dev.fl.Reset() 
dev.fl.AddDir(dest_dir = dev.cfg.arrizza_local_cgibin, 
                   src_dir = dev.cfg.arrizza_websrc_root + '/cgi-bin', 
                   includes= ['*'], 
                   excludes= ['.svn']) 
dev.fl.Install(env) 
dev.fl.Alias(env, 'prepare_cgimain') 
env.jAlias('cgimain', ['prepare_cgimain', 'send_cgimain'], 'build web entities in cgi main page') 
 
#------------ PRIVATE --------------------- 
dev.fl.Reset() 
dev.fl.AddDir(dest_dir = dev.cfg.arrizza_local_private, 
                   src_dir = dev.cfg.arrizza_websrc_root + '/private', 
                   includes= ['*'], 
                   excludes= ['.svn']) 
dev.fl.Install(env) 
dev.fl.Alias(env, 'prepare_private', [dev.cfg.arrizza_local_private]) 
env.jAlias('private', ['prepare_private', 'send_private'], 'build web entities in private page') 
 
#------------ ARTICLES --------------------- 
dev.fl.Reset() 
dev.fl.AddDir(dest_dir = dev.cfg.arrizza_local_articles, 
                   src_dir = dev.cfg.arrizza_websrc_root + '/articles', 
                   includes= ['*'], 
                   excludes= ['.svn']) 
dev.fl.Install(env) 
dev.fl.Alias(env, 'prepare_articles', [dev.cfg.arrizza_local_articles]) 
env.jAlias('articles', ['prepare_articles', 'send_articles'], 'build web entities in articles page') 
 
#------------ RESUME --------------------- 
dev.fl.Reset() 
dev.fl.AddDir(dest_dir = dev.cfg.arrizza_local_resume, 
                   src_dir = dev.cfg.arrizza_websrc_root + '/resume', 
                   includes= ['*'], 
                   excludes= ['.svn']) 
dev.fl.AddFiles(dev.cfg.arrizza_local_resume, dev.cfg.arrizza_resume_root, ['resume.html', 'uofccoatofarms.jpg']) 
dev.fl.Install(env) 
dev.fl.InstallFileAs(env, dev.cfg.arrizza_local_resume + '/johnarrizzawebresume.txt', dev.cfg.arrizza_resume_root + '/JohnArrizzawebResume.txt') 
dev.fl.InstallFileAs(env, dev.cfg.arrizza_local_resume + '/johnarrizzaresume.txt',    dev.cfg.arrizza_resume_root + '/JohnArrizzawebResume.txt') 
dev.fl.InstallFileAs(env, dev.cfg.arrizza_local_resume + '/johnarrizzawebresume.doc', dev.cfg.arrizza_resume_root + '/JohnArrizzawebResume.doc') 
dev.fl.InstallFileAs(env, dev.cfg.arrizza_local_resume + '/johnarrizzaresume.doc',    dev.cfg.arrizza_resume_root + '/JohnArrizzawebResume.doc') 
dev.fl.Alias(env, 'prepare_resume', [dev.cfg.arrizza_local_resume]) 
env.jAlias('resume', ['prepare_resume', 'send_resume'], 'build web entities in resume page') 
 
#------------ LINKS --------------------- 
dev.fl.Reset() 
dev.fl.AddFile(dest_dir = dev.cfg.arrizza_local_links, 
              src_dir = dev.cfg.frozen_root + '/fave2xml', 
              file    = 'links.html') 
dev.fl.Install(env) 
dev.fl.Alias(env, 'prepare_links', [dev.cfg.arrizza_local_links]) 
env.jAlias('links', ['prepare_links', 'send_links'], 'build web entities in links page') 
 
#------------ UBU --------------------- 
dev.fl.Reset() 
dev.fl.AddTree(dest_dir = dev.cfg.arrizza_local_ubu, 
              src_dir = dev.cfg.arrizza_websrc_root + '/ubu', 
              includes= ['*'], 
              excludes= ['.svn', '*.pag', '*.log']) 
dev.fl.Install(env) 
dev.fl.Alias(env, 'prepare_ubu', cleandirlist = dev.cfg.arrizza_local_ubu) 
env.jAlias('ubu', ['prepare_ubu', 'send_ubu'], 'build web entities in ubu page') 
 
#------------ WIKIs --------------------- 
#helper function for installing wikis 
def jQWikiHelper(dest_dir, websrc, cgifile, aliasname): 
    fl = FileList() 
    fl.AddTree(dest_dir = dest_dir, 
             src_dir = dev.cfg.frozen_root + '/jqwiki', 
             includes = ['*'], 
             excludes = ['.svn', 'sconscript', 'jqwiki.html', 'qwiki.cgi', 'jqwiki.cgi', '*.cpr', 'bakit.bat', 'test.bat']) 
    fl.OverwriteFromTree(dest_dir = dest_dir, 
             src_dir = dev.cfg.arrizza_websrc_root + '/' + websrc, 
             includes = ['*'], 
             excludes = ['.svn']) 
    fl.Move(dev.cfg.arrizza_websrc_root + '/' + websrc, cgifile, dev.cfg.arrizza_local_cgibin) 
    #fl.Dump() 
    fl.Install(env) 
    fl.Alias(env, aliasname, [dest_dir]) 
 
#------------ jWikiPub --------------------- 
jQWikiHelper(dest_dir = dev.cfg.arrizza_local_jwikipub, 
           websrc = 'jwikipub', 
           cgifile = 'pub', 
           aliasname = 'prepare_jwikipub') 
env.jAlias('jwikipub', ['prepare_jwikipub', 'send_jwikipub'], 'build web entities in jwikipub page') 
 
#------------ jWikiPriv --------------------- 
jQWikiHelper(dest_dir = dev.cfg.arrizza_local_jwikipriv, 
           websrc = 'jwikipriv', 
           cgifile = 'priv', 
           aliasname = 'prepare_jwikipriv') 
env.jAlias('jwikipriv', ['prepare_jwikipriv', 'send_jwikipriv'], 'build web entities in jwikipriv page') 
 
#------------ jWikiTest --------------------- 
jQWikiHelper(dest_dir = dev.cfg.arrizza_local_jwikitest, 
           websrc = 'jwikitest', 
           cgifile = 'wikit', 
           aliasname = 'prepare_jwikitest') 
env.jAlias('jwikitest', ['prepare_jwikitest', 'send_jwikitest'], 'build web entities in jwikitest page') 
 
#-- 
dev.dh.GenMainPage(env) 
dev.mdh.GenMainPage(env) 
dev.nnh.GenMainPage(env) 
dev.tdh.GenMainPage(env) 
 
env.jAlias('prepare_html', env.Dir(dev.cfg.arrizza_local_html), 'build web entities in html sub-directory') 
env.Clean('prepare_html', env.Dir(dev.cfg.arrizza_local_html)) 
 
env.jAlias('prepare_cgi', env.Dir(dev.cfg.arrizza_local_cgibin), 'build web entities in cgi-bin sub-directory') 
env.Clean('prepare_cgi', env.Dir(dev.cfg.arrizza_local_cgibin)) 
 
#-- Overall Aliases 
env.jAlias('prepare_xpsdorg', ['gather_xpsdorgwiki', 'gather_xpsdorghtml', 'convert_xpsdorg'], 'build web entities for xpsd.org') 
env.jAlias('prepare_cgi', ['prepare_cgimain', 'prepare_jwikipub', 'prepare_jwikipriv', 'prepare_ubu'], 'build web entities in cgi-bin sub-directory') 
#env.jAlias('prepare_html', ['prepare_main', 'prepare_testpages', 'prepare_private', 'prepare_links', 'prepare_snippets', 'prepare_resume', 'prepare_downloads', 'prepare_miscdownloads', 'prepare_taskdefs', 'prepare_neuralnets', 'prepare_articles']) 
env.jAlias('prepare_html',  ['prepare_main', 'prepare_testpages', 'prepare_private', 'prepare_links',                     'prepare_resume', 'prepare_downloads', 'prepare_miscdownloads', 'prepare_taskdefs', 'prepare_neuralnets', 'prepare_articles'], 'build web entities in html sub-directory') 
#env.jAlias('prepare_all', ['prepare_html', 'prepare_cgi', 'prepare_xpsdorg']) 
env.jAlias('prepare_all',  ['prepare_html', 'prepare_cgi'                   ], 'build all web entities') 
env.jAlias('publish', ['prepare_all', 'send_all'], 'build and send web entities in html sub-directory') 
 
env.jAlias('send_html', ['send_main', 'send_testpages', 'send_private', 'send_links', 'send_snippets', 'send_resume', 'send_downloads', 'send_miscdownloads', 'send_taskdefs', 'send_neuralnets', 'send_articles'], 'send all web entities in html sub-directory') 
env.jAlias('send_cgi', ['send_cgimain', 'send_jwikipub', 'send_jwikipriv', 'send_ubu'], 'send all web entities in cgi-bin sub-directory') 
env.jAlias('send_all', ['send_html', 'send_cgi', 'send_xpsdorg'], 'send all web entities') 
 
#--- this statement must be the last in the file 
env.jGenHelp() 
 
#todo: finish wrapping all Aliases. Use jAlias(). so it does not conflict with existing Alias() in env. 
#todo: move 'dev' into environment env 

Here's a typical sconscript:

Import('env', 'dev', 'project') 
localenv = env.Copy() 
 
tgt = dev.VC6(localenv, project, exetype='lib') 
localenv.Depends(tgt, dev.GetSourceFiles(['*.cpp', '*.h'])) 
dev.SetAliases(env, project, tgt) 
 
#--- set up html page 
dev.dh.Reset() 
dev.dh.project = 'jcomheap' 
dev.dh.status = 'complete' 
dev.dh.title = 'jComHeap' 
dev.dh.desc = 'checks the COM heap for leaks using IMallocSpy' 
dev.dh.keywords = 'COM heap, memory leaks, IMallocSpy' 
dev.dh.dest_root = dev.cfg.arrizza_local_downloads + '/' + dev.dh.project 
dev.dh.htmlpage = 'jcomheap.html' 
dev.dh.src_root = dev.cfg.frozen_root + '/' + dev.dh.project 
dev.dh.src_htmlpage = dev.dh.src_root + '/' + dev.dh.htmlpage 
dev.dh.changes = ['Initial version'] 
dev.dh.installation = [] 
dev.dh.showfiles=[dev.dh.src_root + '/../jComHeap_test/testjcomheap.cpp', 
                  dev.dh.src_root + '/debug.reg', 
                  dev.dh.src_root + '/AllocationMap.cpp', 
                  dev.dh.src_root + '/AllocationMap.h', 
                  dev.dh.src_root + '/Stats.h'] 
dev.dh.zipfiles=[dev.GetBuildDir(dev.dh.project) + '/jcomheap.lib', 
                 dev.dh.src_root + '/jcomheap.sln', 
                 dev.dh.src_root + '/jcomheap.vcproj'] 
dev.dh.zipfiles.extend(dev.dh.showfiles) 
dev.dh.Gen(env) 
dev.dh.Alias(env) 

```
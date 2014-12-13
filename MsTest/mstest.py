
"""
This builder is for running mstest with VS 2005/2008, 
If env['MSTEST_REMOVE_TMP_DIR'] is True, it will also delets all previous temporary mstest directories 
which matche reg. expression: 'username_hostname\s\d{4}-\d{2}-\d{2}\s\d{2}_\d{2}_\d{2}' where username and hostname are real values;
directory like that will be matched and deleted "username_hostname 2000-01-01 10_10_25" 

"""

import os.path
import SCons.Defaults
import SCons.Platform.win32
import SCons.Util
import re
import shutil
import getpass 
import socket
import string
import libxml2
import libxslt

def _detect(env):
    mstest=None
    HLM = SCons.Util.HKEY_LOCAL_MACHINE
    Key = r'Software\Microsoft\VisualStudio\%s\Setup\VS'%env['MSVS_VERSION']
    k=SCons.Util.RegOpenKeyEx(HLM, Key)
    path = SCons.Util.RegQueryValueEx(k, 'EnvironmentDirectory' )
    if path and path[0]:
       path=str(path[0])
       fullpath=os.path.join(path,'mstest.exe')
       if os.path.exists(fullpath):
          mstest=fullpath
    return mstest

def _generateCoverageReport(target, source, env):
   #find coverage report file
   testDir=None
   status=0
   username=getpass.getuser()
   hostname=socket.gethostname().upper()
   reTempDir=re.compile('%s_%s\s\d{4}-\d{2}-\d{2}\s\d{2}_\d{2}_\d{2}'%(username,hostname))
   pathdir=os.path.dirname(target[0].abspath)
   if os.path.exists(pathdir):
      for dir in os.listdir(pathdir):
         outputDir=os.path.join(pathdir,dir)
         if os.path.isdir(outputDir):
            match=reTempDir.match(dir)
            if match:
               testDir=outputDir
               break
   if testDir:
      covReport=os.path.join(testDir,"In",socket.gethostname().upper(),"data.coverage")
      if os.path.exists(covReport):
         out=os.path.join(outputDir,"Out")
         xml=os.path.join(out,"coverage.xml")
         status=env.Execute("\"mstest2xml.exe\" \"%s\" \"%s\" \"%s\""%(out,covReport,xml))
         if status == 0:
            xslfile="coverage.xsl"
            htmlfile="coverage.html"
            styledoc = libxml2.parseFile(xslfile)
            style = libxslt.parseStylesheetDoc(styledoc)
            doc = libxml2.parseFile(xml)
            result = style.applyStylesheet(doc, None)
            style.saveResultToFilename(htmlfile, result, 0)
            style.freeStylesheet()
            doc.freeDoc()
            result.freeDoc()
   return status

def DevMsTestMessage(target, source, env):
    return "Running Mstest %s"%source[0]
def DevMsTest(target, source, env):
   if env['MSTEST_REMOVE_TMP_DIR']:
      username=getpass.getuser()
      hostname=socket.gethostname().upper()
      reTempDir=re.compile('%s_%s\s\d{4}-\d{2}-\d{2}\s\d{2}_\d{2}_\d{2}'%(username,hostname))
      pathdir=os.path.dirname(target[0].abspath)
      if os.path.exists(pathdir):
         for dir in os.listdir(pathdir):
            removeDir=os.path.join(pathdir,dir)
            if os.path.isdir(removeDir):
               match=reTempDir.match(dir)
               if match:
                  print "Removing temporary directory:", removeDir
                  shutil.rmtree(removeDir)
      #Run tests:
      status=env.Execute("\"$MSTEST\" /nologo /testmetadata:%s /resultsfile:%s"%(source[0],target[0]))
      #Jenerate coverage report
      _generateCoverageReport(target, source, env)
      
   return status
def generate(env):
   MsTestAction=SCons.Action.Action(DevMsTest,strfunction=DevMsTestMessage)
   MsTestBuilder=SCons.Builder.Builder(action=MsTestAction, suffix="$MSTEST_RES_SUFFIX")
   env['MSTEST']=_detect(env)
   env['MSTEST_RES_SUFFIX']=".trx"
   env['MSTEST_REMOVE_TMP_DIR']=True
   env['BUILDERS']['MsTest'] = MsTestBuilder

def exists(env):
   return _detect(env)

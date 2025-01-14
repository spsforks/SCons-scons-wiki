
Note: this is just a rough draft - I'll email the users list after I clean it up.... fix: 

               * 'real' URL parsing return values (return None like builder, or target/source like emitter?) use Gary O.'s idea of using a Value node to prevent the url getting munged 
I've cobbled up a quick and dirty lil Source Code module that uses 'wget' to retrieve files from the net. Not finished at the moment, but it might be helpful to others. It's based off the ?[BitKeeper](BitKeeper) tool. You can throw it in your Tools dir, and edit Tools to load it automatically or just do what I did and add: 
```txt
      env.Tool('WGet', toolpath=['./path/to/your/modules/dir'])
```
To your SConstruct file. I've been testing it with a lil wrapper that munges download dir and path name together, but according to Gary O. on the mailing list, using a Value() node would eliminate the need for this. As for usage, In the SConscript files I just have: 


```txt
  GetSourceFile(
    'http://url/to/download/file.tar.gz',
    'path/to/download/to',
    env)
```
[GetSourceFile](GetSourceFile) wrapper: 


```txt
def GetSourceFile(url, output_dir, env):
  '''
  Create a node for a file retrieved via wget.
  This node can be used as a dependency in other rules.
  Hmm - how do we create the node ??
  '''
  # Nab everything after the last slash as the filename
  basefilename = str(url)[str( url).rfind(os.sep) + 1:]
  munged = output_dir + os.sep + basefilename + os.sep + url
  env.SourceCode( munged, env.WGet() )
  return None $
```
Here is the WGet.py file: 


```txt
import os.path
import sys
import popen2
import SCons.Action
import SCons.Builder
import SCons.Util


def generate(env):
  """
  Add a Builder factory function and construction variables for
   WGET'ing to an Environment.
  """

  def WGetDownload(target, source, env):
    ret = []
    for x in target:
      url1 = str(x)
      if 'http:' in url1:
        div = url1.find('http:')
        outn = url1[ :div - 1]
        url = url1[div:]
        url = url.replace('http:/','http://')
      elif 'ftp:' in url1:
        div = url1.find('ftp:')
        outn = url1[ :div - 1]
        url = url1[div:]
        url = url.replace('ftp:/','ftp://')
      basename = str(url)[str( url).rfind(os.sep) + 1:]
      if not os.path.exists( outn):
        cmd = popen2.Popen4('wget -O %s %s' % (outn,url) )
        rc = cmd.wait()
        if rc != 0 :
          print "wget %s returned: %s" % (url, rc)
          print "%s" % cmd.fromchild.read()
          sys.exit()
    return None

  def WGetFactory(env=env):
    """ """
    act = SCons.Action.Action(WGetDownload)
    return SCons.Builder.Builder(action = act, env = env)

  env.WGet = WGetFactory
  env['WGET'] = 'wget'
  env['WGETFLAGS'] = SCons.Util.CLVar('')
  env['WGETCOM'] = '$WGET $WGETFLAGS $TARGET'

def exists(env):
  return env.Detect('wget')
 
```
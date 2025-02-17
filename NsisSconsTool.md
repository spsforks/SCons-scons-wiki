
This is a Tool for SCons that can parse a Nullsoft Scriptable Installation System (NSIS) script (a .nsi file) and determine its dependencies and its actual target name. The following file can be be copied to site-packages/scons/SCons/Tools/ and it will 'just work'. 

**Enhancement note**: This uses glob.glob to find the source files if they have filename glob chars, but if (as is usual) the sources are built by some other builder, you might want to use one of the techniques in [BuildDirGlob](BuildDirGlob) to find them instead, so scons gets all the dependencies correct. 

Feel free to modify and improve as you wish. 

* UPDATE: I have patched this tool to work correctly on Windows 64-bit (with Python 64 bit). If this is useful to you, see here: [http://code.ascend4.org/viewvc/code/trunk/scons/nsis.py?view=log](http://code.ascend4.org/viewvc/code/trunk/scons/nsis.py?view=log). -- [JohnPye](JohnPye) 
* Works for me too! Rather than installing the file in site-packages, I've used it as embedded code in my main trunk/SConstruct and trunk/pygtk/interface/SConscript, which are visible at [https://pse.cheme.cmu.edu/svn-view/ascend/code/trunk/](https://pse.cheme.cmu.edu/svn-view/ascend/code/trunk/), so that I don't have to tell users to mess with their default SCons installation. -- [JohnPye](JohnPye) 
* I have made changes that allow using makensis in linux, and also basic analysis of !include and !ifdef directives (not included in the script below, which does parse File operations).  These changes are provided in a [diff](nsis-changes-for-linux-and-includes.diff).  I have also moved to using env.Glob() instead of glob.glob.  The final script, with those changes applied to the January 2004 shown below, is [here](nsis-with-modifications-for-linux-and-includes.py).  I did not test the script with Windows makensis.exe so there is a possibility some things were broken there.  The only thing I can think of that has possibly been broken, however, is the determination of the SCons install directory in line 146.  To use as a tool without overwriting the SCons install directory, I placed it in a subdirectory of the SConstruct directory called "scons_tools" and used: ```txt
env.Tool("nsis", toolpath=["scons_tools"])
```-- [YitzhakSapir](YitzhakSapir) 
The original script for the tool is provided below. 


```python
#!python
# NSIS Support for SCons
# Written by Mike Elkins, January 2004
# Provided 'as-is', it works for me!


"""
This tool provides SCons support for the Nullsoft Scriptable Install System
a windows installer builder available at http://nsis.sourceforge.net/home


To use it you must copy this file into the scons/SCons/Tools directory or use
the tooldir arg in the Tool function and put a line like 'env.Tool("NSIS")'
into your file. Then you can do 'env.Installer("foobar")' which will read foobar.nsi and
create dependencies on all the files you put into your installer, so that if
anything changes your installer will be rebuilt.  It also makes the target
equal to the filename you specified in foobar.nsi.  Wildcards are handled correctly.

In addition, if you set NSISDEFINES to a dictionary, those variables will be passed
to NSIS.
"""



import SCons.Builder
import SCons.Util
import SCons.Scanner
# NOTE (4 September 2007):  The following import line was part of the original
# code on this wiki page before this date.  It's not used anywhere below and
# therefore unnecessary.  The SCons.Sig module is going away after 0.97.0d20070809,
# so the line should be removed from your copy of this module.  There may be a
# do-nothing SCons.Sig module that generates a warning message checked in, so existing
# configurations won't break and can help point people to the line that needs removing.
#import SCons.Sig
import os.path
import glob


def nsis_parse( sources, keyword, multiple ):
  """
  A function that knows how to read a .nsi file and figure
  out what files are referenced, or find the 'OutFile' line.


  sources is a list of nsi files.
  keyword is the command ('File' or 'OutFile') to look for
  multiple is true if you want all the args as a list, false if you
  just want the first one.
  """
  stuff = []
  for s in sources:
    c = s.get_contents()
    for l in c.split('\n'):
      semi = l.find(';')
      if semi != -1:
        l = l[:semi]
      hash = l.find('#')
      if hash != -1:
        l = l[:hash]
      # Look for the keyword
      l = l.strip()
      spl = l.split(None,1)
      if len(spl) > 1:
        if spl[0].lower() == keyword.lower():
          arg = spl[1]
          if arg.startswith('"') and arg.endswith('"'):
            arg = arg[1:-1]
          if multiple:
            stuff += [ arg ]
          else:
            return arg
  return stuff


def nsis_path( filename, nsisdefines, rootdir ):
  """
  Do environment replacement, and prepend with the SCons root dir if
  necessary
  """
  # We can't do variables defined by NSIS itself (like $INSTDIR),
  # only user supplied ones (like ${FOO})
  varPos = filename.find('${')
  while varPos != -1:
    endpos = filename.find('}',varPos)
    assert endpos != -1
    if filename[varPos+2:endpos] not in nsisdefines:
      raise KeyError ("Could not find %s in NSISDEFINES" % filename[varPos+2:endpos])
    val = nsisdefines[filename[varPos+2:endpos]]
    if type(val) == list:
      if varPos != 0 or endpos+1 != len(filename):
        raise Exception("Can't use lists on variables that aren't complete filenames")
      return val
    filename = filename[:varPos] + val + filename[endpos+1:]
    varPos = filename.find('${')
  return filename


def nsis_scanner( node, env, path ):
  """
  The scanner that looks through the source .nsi files and finds all lines
  that are the 'File' command, fixes the directories etc, and returns them.
  """
  nodes = node.rfile()
  if not node.exists():
    return []
  nodes = []
  source_dir = node.get_dir()
  for include in nsis_parse([node],'file',1):
    exp = nsis_path(include,env['NSISDEFINES'],source_dir)
    if type(exp) != list:
      exp = [exp]
    for p in exp:
      for filename in glob.glob( os.path.abspath(
        os.path.join(str(source_dir),p))):
          # Why absolute path?  Cause it breaks mysteriously without it :(
          nodes.append(filename)
  return nodes


def nsis_emitter( source, target, env ):
  """
  The emitter changes the target name to match what the command actually will
  output, which is the argument to the OutFile command.
  """
  nsp = nsis_parse(source,'outfile',0)
  if not nsp:
    return (target,source)
  x  = (
    nsis_path(nsp,env['NSISDEFINES'],''),
    source)
  return x

def quoteIfSpaced(text):
  if ' ' in text:
    return '"'+text+'"'
  else:
    return text

def toString(item,env):
  if type(item) == list:
    ret = ''
    for i in item:
      if ret:
        ret += ' '
      val = toString(i,env)
      if ' ' in val:
        val = "'"+val+"'"
      ret += val
    return ret
  else:
    # For convienence, handle #s here
    if str(item).startswith('#'):
      item = env.File(item).get_abspath()
    return str(item)

def runNSIS(source,target,env,for_signature):
  ret = env['NSIS']+" "
  if 'NSISFLAGS' in env:
    for flag in env['NSISFLAGS']:
      ret += flag
      ret += ' '
  if 'NSISDEFINES' in env:
    for d in env['NSISDEFINES']:
      ret += '/D'+d
      if env['NSISDEFINES'][d]:
        ret +='='+quoteIfSpaced(toString(env['NSISDEFINES'][d],env))
      ret += ' '
  for s in source:
    ret += quoteIfSpaced(str(s))
  return ret

def generate(env):
  """
  This function adds NSIS support to your environment.
  """
  env['BUILDERS']['Installer'] = SCons.Builder.Builder(generator=runNSIS,
                                 src_suffix='.nsi',
                                 emitter=nsis_emitter)
  env.Append(SCANNERS = SCons.Scanner.Scanner( function = nsis_scanner,
             skeys = ['.nsi']))
  if 'NSISDEFINES' not in env:
    env['NSISDEFINES'] = {}
  env['NSIS'] = find_nsis(env)

def find_nsis(env):
  """
  Try and figure out if NSIS is installed on this machine, and if so,
  where.
  """
  if SCons.Util.can_read_reg:
    # If we can read the registry, get the NSIS command from it
    try:
      k = SCons.Util.RegOpenKeyEx(SCons.Util.hkey_mod.HKEY_LOCAL_MACHINE,
                                  'SOFTWARE\\NSIS')
      val, tok = SCons.Util.RegQueryValueEx(k,None)
      ret = val + os.path.sep + 'makensis.exe'
      if os.path.exists(ret):
        return '"' + ret + '"'
      else:
        return None
    except:
      pass # Couldn't find the key, just act like we can't read the registry
  # Hope it's on the path
  return env.WhereIs('makensis.exe')

def exists(env):
  """
  Is NSIS findable on this machine?
  """
  return find_nsis(env) != None:
```
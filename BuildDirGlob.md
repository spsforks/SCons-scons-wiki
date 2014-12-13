
****This page presents material that is no longer needed but is being kept for historical purposes.  As of version 0.98, [SCons has a Glob function](http://www.scons.org/doc/1.2.0/HTML/scons-user/x489.html) built-in. **** 



---

 

This page shows you how to glob (search files in dir) based on scons Nodes rather than files.  This way you get all the files that _will_ be built as well as the ones that already exist in the filesystem. 

As of this writing, none of these functions recurse into subdirs, but that's not hard either.  Just check each node returned by all_children() and if it's a Dir node, recurse.  Here's a trivial one: 


```python
#!python
def print_all_nodes(dirnode, level=0):
    """Print all the scons nodes that are children of this node, recursively."""
    if type(dirnode)==type(''):
        dirnode=Dir(dirnode)
    dt = type(Dir('.'))
    for f in dirnode.all_children():
        if type(f) == dt:
            print "%s%s: .............."%(level * ' ', str(f))
            print_dir(f, level+2)
        print "%s%s"%(level * ' ', str(f))
```


---

 

* Here is another version of Glob, similar to the one below, except it allows multiple excludes and includes, as well as a directory specification. It also deals directly with SCons Nodes. 
_NOTE: this is the best version available.  The others below are mostly of historical interest._ 


```python
#!python
import fnmatch
import os
def Glob( includes = Split( '*' ), excludes = None, dir = '.'):
   """Similar to glob.glob, except globs SCons nodes, and thus sees
   generated files and files from build directories.  Basically, it sees
   anything SCons knows about.  A key subtlety is that since this function
   operates on generated nodes as well as source nodes on the filesystem,
   it needs to be called after builders that generate files you want to
   include.
   It will return both Dir entries and File entries
   """
   def fn_filter(node):
      fn = os.path.basename(str(node))
      match = False
      for include in includes:
         if fnmatch.fnmatchcase( fn, include ):
            match = True
            break
      if match and excludes is not None:
         for exclude in excludes:
            if fnmatch.fnmatchcase( fn, exclude ):
               match = False
               break
      return match
   def filter_nodes(where):
       children = filter(fn_filter, where.all_children(scan=0))
       nodes = []
       for f in children:
           nodes.append(gen_node(f))
       return nodes
   def gen_node(n):
       """Checks first to see if the node is a file or a dir, then
       creates the appropriate node. [code seems redundant, if the node
       is a node, then shouldn't it just be left as is?
       """
       if type(n) in (type(''), type(u'')):
           path = n
       else:
           path = n.abspath
       if os.path.isdir(path):
           return Dir(n)
       else:
           return File(n)
   here = Dir(dir)
   nodes = filter_nodes(here)
   node_srcs = [n.srcnode() for n in nodes]
   src = here.srcnode()
   if src is not here:
       for s in filter_nodes(src):
           if s not in node_srcs:
               # Probably need to check if this node is a directory
               nodes.append(gen_node(os.path.join(dir,os.path.basename(str(s)))))
   return nodes
```
You can either include this function directly in your SConscript, or place in an external python script to include in any SConscript it's needed. SCons CVS has a better way to do it, but 0.96.1 requires the use of SConscript( 'external_script.py' ) and Import( ) / Export( ) 

I don't take much credit for this. Most credit belongs to John Meinel from the SCons mailinglist. 

* -- [MichaelKoehmstedt](MichaelKoehmstedt) 
If you want to glob for generated files or for source files in a [BuildDir](BuildDir), copy the following function into your project and call Glob instead of glob.glob. 


```python
#!python
def Glob(match):
    """Similar to glob.glob, except globs SCons nodes, and thus sees
    generated files and files from build directories.  Basically, it sees
    anything SCons knows about.  A key subtlety is that since this function
    operates on generated nodes as well as source nodes on the filesystem,
    it needs to be called after builders that generate files you want to
    include."""
    def fn_filter(node):
        fn = str(node)
        return fnmatch.fnmatch(os.path.basename(fn), match)
    here = Dir('.')
    children = here.all_children()
    nodes = map(File, filter(fn_filter, children))
    node_srcs = [n.srcnode() for n in nodes]
    src = here.srcnode()
    if src is not here:
        src_children = map(File, filter(fn_filter, src.all_children()))
        for s in src_children:
            if s not in node_srcs:
                nodes.append(File(os.path.basename(str(s))))
    return nodes
```
Eventually this should go into SCons proper with test cases and documentation. 

**Note**: Glob currently does not support usages such as Glob('src/*.cpp').  Eventually it should split the match string into directories and use the fnmatch module to glob on subdirectories as well. 

(Notes by [chenlee@ustc.edu](mailto:chenlee@ustc.edu) ) Below is the grab function used in my building script: 


```python
#!python
def Glob( pattern = '*.*', dir = '.' ):
    import os, fnmatch
    files = []
    for file in os.listdir( Dir(dir).srcnode().abspath ):
        if fnmatch.fnmatch(file, pattern) :
            files.append( os.path.join( dir, file ) )
    return files
```
Here's another version that has includes and excludes: 


```python
#!python
  def Matches(file, includes, excludes):
      match = False
      for pattern in includes:
         if fnmatch.fnmatchcase(file, pattern):
             match = True
             break
      if match and excludes is not None:
          for pattern in excludes:
              if fnmatch.fnmatchcase(file, pattern):
                  match = False
                  break
      return match
  def AddDir(src_dir, includes, excludes=None):
      files = []
      for file in os.listdir(Dir(src_dir).srcnode().abspath):
          fqpath = src_dir + '/' + file
          if os.path.isdir(fqpath):  continue   #don't include subdirs
          if Matches(file, includes, excludes):
             files.append(file)
      return files
used like so:
   AddDir("c:/mystuff", "*.cpp", excludes=['test*.cpp', '.svn'])
```
And yet another version: SGlob('*.cpp'), SGlob('Test/*.cpp') 


```python
#!python
def SGlob(pattern):
        path = GetBuildPath('SConscript').replace('SConscript', '')
        result = []
        for i in glob.glob(path + pattern):
                result.append(i.replace(path, ''))
        return result
```
**Note:** This Version is kind a dirty, but it searches the sourcedirectory, which makes it usable until there is an offical 'the-SCons-way' Glob. 



---

 

* I have written my own version of the SCons Glob when I couldn't get the above to work properly. I can't guarantee it under all conditions but it seems to work for me and handles a few edge cases I have discovered. [Brad Phelan's SCons Magic Glob](http://xtargets.com/snippets/posts/show/76) I'll update the linked page as I further test the code. 


---

 

* Q: Just a question: Why isn't glob.glob from the stdlib good?  
 A: I haven't proven this, but here's a guess. The latest version of this function claims to scan SCons build nodes. If you used glob.glob then you'd get a list of files that existed before the build. If you use the most up-to-date glob above, you'll probably get a list of files that SCons expects to build in the directory, as well as the files that currently exist. That might be important if you're untarring source files, or checking them out from source control, during the build process.  
 A': Yes, that's exactly right.  Another example: if you have a source-generator, you need to glob against all the files the source-generator will generate, not just the files that exist when the build starts. 
* The glob.glob(mask) results depend on the current directory while SConscripts are supposed to be independent of it.  [There is a call SConscriptChdir(enable) that can disable descending into SConscripts' directories at the time of their harvesting].  Changing to Dir(".").abspath to run glob.glob() could be, in my opinion, dangerous in parallel builds if the latter are implemented as threads.  --[IL](IlguizLatypov) 
* The glob.glob(mask) will produce a list of file paths with inconsistent path separators.  That is, if mask is "dir1/dir2/*.cpp", the result in the win32 build of Python will have paths such as "dir1/dir2\\file.cpp".  --[IL](IlguizLatypov) 
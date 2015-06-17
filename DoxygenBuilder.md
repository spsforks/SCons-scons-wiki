
# Doxygen Builder

The Doxygen builder will generate doxygen docs, given a Doxyfile. It will scan the Doxyfile and determine what directories will be created and what sources are used to generate the docs. This frees you up from writing special code to manage clean up and regeneration of the docs. 

N.B. It seems there was a bug in scons versions before `0.97.0d20070918` which prevented dependencies from working for this builder. See [this email](http://scons.tigris.org/servlets/ReadMsg?list=users&msgNo=12255) to the mailing list for details. 

Russel Winder has started a Bazaar branch on Launchpad to try and acrete all the work found on and from this page into a single good tool. You may want to use this version rather than trying to replicate the various changes needed to reconcile all the variations reported on this page.  If you find any errors or improvements please contribute them back via a pull request rather than posting code to this page.  Thanks. 

The above now appears to have moved to a Mercurial branch on Bitbucket: [https://bitbucket.org/russel/scons_doxygen](https://bitbucket.org/russel/scons_doxygen). 

**Please use the Bazaar Mercurial branch above and not any of the codes below, which are left here just to preserve the historical record.** 


## Usage

Check out the Mercurial repository into `site_scons/site_tools/doxygen`. Then, in your SConstruct file: 


```
#!python
# scons buildfile

# the doxygen package file needs to be in toolpath
env = Environment(tools = ["default", "doxygen"])
env.Doxygen("Doxyfile")
```

## Historical instructions

The original instructions for use are given below. 

Save the following script as file 'doxygen.py' and put its directory in the 'toolpath' list as shown in "Usage" below. 


```
#!python
# vim: set et sw=3 tw=0 fo=awqorc ft=python:
#
# Astxx, the Asterisk C++ API and Utility Library.
# Copyright (C) 2005, 2006  Matthew A. Nicholson
# Copyright (C) 2006  Tim Blechmann
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
import os.path
import glob
from fnmatch import fnmatch

def DoxyfileParse(file_contents):
   """
   Parse a Doxygen source file and return a dictionary of all the values.
   Values will be strings and lists of strings.
   """
   data = {}

   import shlex
   lex = shlex.shlex(instream = file_contents, posix = True)
   lex.wordchars += "*+./-:"
   lex.whitespace = lex.whitespace.replace("\n", "")
   lex.escape = ""

   lineno = lex.lineno
   token = lex.get_token()
   key = token   # the first token should be a key
   last_token = ""
   key_token = False
   next_key = False
   new_data = True

   def append_data(data, key, new_data, token):
      if new_data or len(data[key]) == 0:
         data[key].append(token)
      else:
         data[key][-1] += token

   while token:
      if token in ['\n']:
         if last_token not in ['\\']:
            key_token = True
      elif token in ['\\']:
         pass
      elif key_token:
         key = token
         key_token = False
      else:
         if token == "+=":
            if key not in data:
               data[key] = []
         elif token == "=":
            data[key] = []
         else:
            append_data( data, key, new_data, token )
            new_data = True

      last_token = token
      token = lex.get_token()

      if last_token == '\\' and token != '\n':
         new_data = False
         append_data( data, key, new_data, '\\' )

   # compress lists of len 1 into single strings
   for k, v in data.items():
      if len(v) == 0:
         data.pop(k)

      # items in the following list will be kept as lists and not converted to strings
      if k in ["INPUT", "FILE_PATTERNS", "EXCLUDE_PATTERNS"]:
         continue

      if len(v) == 1:
         data[k] = v[0]

   return data

def DoxySourceScan(node, env, path):
   """
   Doxygen Doxyfile source scanner.  This should scan the Doxygen file and add
   any files used to generate docs to the list of source files.
   """
   default_file_patterns = [
      '*.c', '*.cc', '*.cxx', '*.cpp', '*.c++', '*.java', '*.ii', '*.ixx',
      '*.ipp', '*.i++', '*.inl', '*.h', '*.hh ', '*.hxx', '*.hpp', '*.h++',
      '*.idl', '*.odl', '*.cs', '*.php', '*.php3', '*.inc', '*.m', '*.mm',
      '*.py',
   ]

   default_exclude_patterns = [
      '*~',
   ]

   sources = []

   data = DoxyfileParse(node.get_contents())

   recursive = data.get("RECURSIVE") == "YES"

   file_patterns = data.get("FILE_PATTERNS", default_file_patterns)
   exclude_patterns = data.get("EXCLUDE_PATTERNS", default_exclude_patterns)

   for node in data.get("INPUT", []):
      if os.path.isfile(node):
         sources.append(node)
      elif os.path.isdir(node):
         if recursive:
            for root, dirs, files in os.walk(node):
               for f in files:
                  filename = os.path.join(root, f)

                  pattern_check = any(fnmatch(filename, y) for y in file_patterns)
                  exclude_check = any(fnmatch(filename, y) for y in exclude_patterns)

                  if pattern_check and not exclude_check:
                     sources.append(filename)
         else:
            for pattern in file_patterns:
               sources.extend(glob.glob("/".join([node, pattern])))

   sources = [env.File(path) for path in sources]
   return sources


def DoxySourceScanCheck(node, env):
   """Check if we should scan this file"""
   return os.path.isfile(node.path)

def DoxyEmitter(source, target, env):
   """Doxygen Doxyfile emitter"""
   # possible output formats and their default values and output locations
   output_formats = {
      "HTML": ("YES", "html"),
      "LATEX": ("YES", "latex"),
      "RTF": ("NO", "rtf"),
      "MAN": ("NO", "man"),
      "XML": ("NO", "xml"),
   }

   data = DoxyfileParse(source[0].get_contents())

   targets = []
   out_dir = data.get("OUTPUT_DIRECTORY", ".")

   # add our output locations
   for k, v in output_formats.items():
      if data.get("GENERATE_" + k, v[0]) == "YES":
         targets.append(env.Dir( os.path.join(out_dir, data.get(k + "_OUTPUT", v[1]))) )

   # don't clobber targets
   for node in targets:
      env.Precious(node)

   # set up cleaning stuff
   for node in targets:
      env.Clean(node, node)

   return (targets, source)

def generate(env):
   """
   Add builders and construction variables for the
   Doxygen tool.  This is currently for Doxygen 1.4.6.
   """
   doxyfile_scanner = env.Scanner(
      DoxySourceScan,
      "DoxySourceScan",
      scan_check = DoxySourceScanCheck,
   )

   import SCons.Builder
   doxyfile_builder = SCons.Builder.Builder(
      action = "cd ${SOURCE.dir}  &&  ${DOXYGEN} ${SOURCE.file}",
      emitter = DoxyEmitter,
      target_factory = env.fs.Entry,
      single_source = True,
      source_scanner =  doxyfile_scanner,
   )

   env.Append(BUILDERS = {
      'Doxygen': doxyfile_builder,
   })

   env.AppendUnique(
      DOXYGEN = 'doxygen',
   )

def exists(env):
   """
   Make sure doxygen exists.
   """
   return env.Detect("doxygen")

```

### Note added by Robert Lupton, rhl@astro.princeton.edu

I had to make two changes to make this work. 

1. I had to double the $ in the Action: 

* action = env.Action("cd $${SOURCE.dir} && $${DOXYGEN} $${SOURCE.file}"), 
2. As written, the Builder runs from the top level directory TOP when it scans the doxyfile, but runs doxygen from the source directory. This means that it you set INPUT to e.g. "..", the scanner will set the dependencies to refer to all files found by searching TOP/.. --- which isn't what you want! 

Here's a fix (around line 122): 


```
#!python
#
# We're running in the top-level directory, but the doxygen
# configuration file is in the same directory as node; this means
# that relative pathnames in node must be adjusted before they can
# go onto the sources list
#
conf_dir = os.path.dirname(str(node))

for node in data.get("INPUT", []):
   if not os.path.isabs(node):
      node = os.path.join(conf_dir, node)
```

### Note added by SK

The code above originally had the following initialization of the `action =` argument when creating the Builder: 


```
#!python
action = env.Action("cd ${SOURCE.dir}  &&  ${DOXYGEN} ${SOURCE.file}"),
```
The `env.Action()` call explicitly asks for the string to be evaluated at call time, when the action is created, which is why Robert found it necessary to double the `$` characters. (It probably did work in earlier versions, but variable substitution in construction environment methods has been "cleaned up" in some recent versions, and this may have been a casualty.) 

Since there's nothing special about the action being created (no `strfunction`, for example), it's much simpler to just pass the command-line string to the Builder and let SCons create the Action object. 


```
#!python
action = "cd ${SOURCE.dir}  &&  ${DOXYGEN} ${SOURCE.file}",
```
I updated the code above so that people who cut and paste without reading all the way to the bottom of the page shouldn't have this problem. 

**Additional update 6 March 2007:** There was also a left-over `env.Builder` that had to be changed to the raw form of the call to avoid variable expansion earlier than we want. Code above changed. 


### Note added by Dirk Reiners, dirk@louisiana.edu

I added two (at least for me ;)) important features of doxygen: variable substituion and hierarchical doxygen files. 

Variable substituion allows doxygen to reference variables from the scons environment using $(VARNAME). This is very useful for things like version numbers or for only having certain parts (as defined by scons) included in the documentation without having to mess with doxygen files. 

Hierarchical doxygen files just interpret the @INCLUDE key as an include. 

I also had trouble with files that started with a key, I fixed that. 

The changes are a little longish for putting them in the text, so I attached the changed file [doxygen.py_dr_070226](doxygen.py_dr_070226). Note that I'm a python newbie, so there are probably more elegant ways to do some of the things I did. Feel free to change them. 

Hope it helps. 


### Note added by anonymous

Replace the line `token = env[token[2:-1]]` by `token = env[token[2:token.find(")")]]` to suppress wrong warnings when using environment variables in Doxyfile as path. (Like in "`$(MY_LIBRARY)/include`") 


### Note added by Christoph Boehme, cxb632@bham.ac.uk

Robert Lupton noted that you have to change the source paths if you keep your Doxyfile in a subdirectory and use relative paths. I found that I had to do the same for the target path in the Doxyfile. Therefore, I added the following lines after line 160: 


```
#!python
   if not os.path.isabs(out_dir):
      conf_dir = os.path.dirname(str(source[0]))
      out_dir = os.path.join(conf_dir, out_dir)
```
This is essentially the same code as Robert Lupton's. 


### Adding tagfile to targets and html templates to sources

The following code adds the tagfile to the target list. I added it in line 166: 


```
#!python
   # add the tag file if neccessary:
   tagfile = data.get("GENERATE_TAGFILE", "")
   if tagfile != "":
      if not os.path.isabs(tagfile):
         conf_dir = os.path.dirname(str(source[0]))
         tagfile = os.path.join(conf_dir, tagfile)
      targets.append(env.File(tagfile));
```
To add the html templates from the Doxyfile to the list of sources, you need to apply Robert Lupton's change and add the following snippet in line 137: 


```
#!python
   # Add additional files to the list ouf source files:
   def append_additional_source(option):
      file = data.get(option, "")
      if file != "":
         if not os.path.isabs(file):
            file = os.path.join(conf_dir, file)
         if os.path.isfile(file):
            sources.append(file)

   append_additional_source("HTML_STYLESHEET")
   append_additional_source("HTML_HEADER")
   append_additional_source("HTML_FOOTER")
```
You can easily add dependencies on other output file templates by adding additional calls to append_additional_source(). 

**Addendum 18 July 2007:** I added some code to add tagfiles to the list of sources. Since the tagfiles-option allows for equal-signs in the value, I had to change the parsing code a bit. The new code is found in file [doxygen.py](doxygen.py) . This file also includes the other changes I have made. 


### Note added by Reinderien

I believe that the line 


```
"MAN": ("YES", "man"),
```
should read 


```
"MAN": ("NO", "man"),
```
I was getting unnecessary doxygen runs, and `scons --debug-explain` showed that doxygen.py thinks the man target is on by default when it isn't. 

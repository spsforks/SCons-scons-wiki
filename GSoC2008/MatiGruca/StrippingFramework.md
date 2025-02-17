

# Comments Stripping Framework

NOTE: The Comments Stripping Framework is not yet a part of SCons. The current code is viewable [here](http://scons.tigris.org/source/browse/scons/branches/comments/). Creating Comments Stripping Framework is a part of [my Google Summer of Code project](http://www.scons.org/wiki/GSoC2008/MatiGruca). 

NOTE: This documentation refers to [CommentsRE](http://scons.tigris.org/source/browse/scons/branches/comments/src/engine/SCons/CommentsRE.py)  module and not to `Comments.py` module. Even when I refer to `SCons.Comments` module I really mean `SCons.CommentsRE` module. 

An installation package is also available for download: 

* [scons-csf-01-0.98.5.tar.gz](scons-csf-01-0.98.5.tar.gz) 
* [scons-csf-01-0.98.5.win32.exe](scons-csf-01-0.98.5.win32.exe) 
Comments Stripping Framework is responsible for stripping out comments (or any content not regarded as significant in particular case) and counting checksums only for significant content. 

When the comment is changed in a C program, there is no need to recompile the source code. When the code is changed, there is no need to regenerate the DOXYGEN documentation. 

At the moment CSF is turned on by default and there is no way to turn it off (other than modifying the source code). 


### GenericStripCode() function

`GenericStripCode(filename, patterns)` - this function makes it possible to build your own code stripping functions (i.e. functions that return comments from the files). 

Let's say you need a C-like code stripping function, but with a possibility to strip multiline comments that start with `/@` signs and end with `@/`. 

You can use `GenericStripCode()` function from SCons.CommentsRE module along with two predefined regular expressions (`c_comment` for `/* ... */` comments and `cxx_comment` for one-line `// ...` comments) and a function to create your own multiline regular expressions:  `multiline_comment_regexp()`. 

Sample `SConstruct` file: 


```python
#!python 
from SCons.CommentsRE import GenericStripCode, c_comment, cxx_comment, multiline_comment_regexp

def StripAtCode(filename):
    """Strips source code from file 'filename'.
    Returns traditional C comments ("/* ... */"),
    C++ one-line comments ("// ...") and at-multiline-comments
    ("/@ ... @/")."""

    at_comment = multiline_comment_regexp('/\@', '\@/')
    return GenericStripCode(filename,
                            (c_comment, cxx_comment, at_comment))

# StripAtCode() is a valid stripper now.
# You can add it to your builder using
# add_stripper() method.
```
Predefined wrappers for `GenericStripCode()`: 

* `StripCCode(filename)` - strips the code from the file 'filename' and returns comments. Works for '// ...' and '/* ... */' comments. 
* `StripDCode(filename)` - strips the code from the file 'filename' and returns comments. Works for '// ...', '/* ... */' and '/+ ... +/' comments. 
* `StripHashCode(filename)` - strips the code from the file 'filename' and returns comments. Works for '# ...' one-line comments. 
* `StripFortranCode(filename)` - strips the code from the file 'filename' and returns comments. Works for '! ...' one-line comments. 

### GenericStripComments() function

`GenericStripComments(filename, patterns, quotings = ('"', "'"), comment_first_chars = ('//','/\*'), preprocessor = False)` - this function makes it possible to build your own comments stripping functions (i.e. functions that return code from the files). 

`GenericStripComments()` function returns contents of the `filename` file except of strings that fit regular expressions defined in `patterns` tuple. 

`patterns` may be a string, list or tuple containing regular expression strings ready to be compiled with `re.compile()` function. 

`quotings` is a tuple of characters, each of which marks beginning (and end) of a string. Patterns from the `patterns` argument found between the `quotings` characters won't be stripped. 

`comment_first_chars` is a tuple that defines signs that comments start with. For C-like comments comment_first_chars is equal to `('//', '/\*')`. 

When `preprocessor` is `True` `GenericStripComments()` won't strip whitespaces from the lines that start with `#` sign. 

Let's say you need a C-like comments stripping function, but with a possibility to strip oneline comments that start with `$` sign and end with a new-line. 

You can use `GenericStripComments()` function from `SCons.CommentsRE` module along with two predefined regular expressions (`c_comment` for '/* ... */' comments and `cxx_comment` for one-line '// ...' comments) and a function to create your own multiline regular expressions:  `multiline_comment_regexp()`. 


```python
#!python 
from SCons.CommentsRE import GenericStripComments, c_comment, cxx_comment, oneline_comment_regexp

def StripDollarComments(filename):
    """Strips comments from file 'filename'.
    Returns source code.
    Works for traditional C comments ("/* ... */"),
    C++ one-line comments ("// ...") and dollar-oneline-comments
    ("$ ... ")."""

    dollar_comment = oneline_comment_regexp('\$')
    return GenericStripComments(filename,
                            (c_comment,
                             cxx_comment,
                             dollar_comment),
                             comment_first_chars = ('//', '/\*', '\$'))

# StripDollarComments() is a valid stripper now.
# You can add it to your builder using
# add_stripper() method.
```
Predefined wrappers for `GenericStripComments()`: 

* `StripCComments(filename)` - strips the comments from the file 'filename' and returns source code. Works for '// ...' and '/* ... */' comments. 
* `StripDComments(filename)` - strips the comments from the file 'filename' and returns source code. Works for '// ...', '/* ... */' and '/+ ... +/' comments. 
* `StripHashComments(filename)` -  - strips the comments from the file 'filename' and returns source code. Works for '# ...' one-line comments. 
* `StripFortranComments(filename)` -  - strips the comments from the file 'filename' and returns source code. Works for '! ...' one-line comments. 

### Creating new strippers

Let's say that you want to use your XYZ compiler to compile `hello.xyz` file. XYZ language uses `%` signs as the beginning of the comments (comments end with a new line). You often change and recompile your packages created in XYZ language, so you don't want SCons to rebuild when only comments were changed. 

All you have to do is to create your builder and add stripper to it. You can use `SCons.Comments.GenericStripComments()` function to create the function you need. 

The `SConstruct` file could look like this: 


```python
#!python 
import os
import SCons.Builder
from SCons.Comments import GenericStripComments, oneline_comment_regexp
def StripPercentComments(filename):
    percent_comment = oneline_comment_regexp('\%')
    return GenericStripComments(filename,
                                (percent_comment),
                                 comment_first_chars = ('\%',))

def XYZBuilder(target, source, env):
    os.system("xyz %s" % str(source[0]))

xyz_builder = Builder(action = XYZBuilder)
xyz_builder.add_stripper('.xyz', StripPercentComments)
env = Environment(BUILDERS = { 'XYZ': xyz_builder })
env.XYZ('hello.xyz')
```
In case you need other kind of stripping functions you can use one of the predefined functions or create your own function. Your function should take one argument: a file name to strip comments/code from and return stripped contents of the file. 


The generic substitution builder is an improvement upon the [SubstInFile2](SubstInFile2) builder.  It provides a more generic way of performing substitutions and can be extended with new methods.  This can be used to take *.in files and produce results from them, such as config.h from a config.h.in, an so on.  It provides two common substitution methods, [SubstFile](SubstFile) and [SubstHeader](SubstHeader).  These simply call the [SubstGeneric](SubstGeneric) builder with the desired values. 

This builder has been updated to allow the [SubstHeader](SubstHeader) substitutions to be quoted if desired. 


### The code


```python
#!python 
# File:         subst.py
# Author:       Brian A. Vanderburg II
# Purpose:      A generic SCons file substitution mechanism
# Copyright:    This file is placed in the public domain.
##############################################################################


# Requirements
##############################################################################
import re

from SCons.Script import *
import SCons.Errors


# Helper/core functions
##############################################################################

# Do the substitution
def _subst_file(target, source, env, pattern, replace):
    # Read file
    f = open(source, "rU")
    try:
        contents = f.read()
    finally:
        f.close()

    # Substitute, make sure result is a string
    def subfn(mo):
        value = replace(env, mo)
        if not SCons.Util.is_String(value):
            raise SCons.Errors.UserError("Substitution must be a string.")
        return value

    contents = re.sub(pattern, subfn, contents)

    # Write file
    f = open(target, "wt")
    try:
        f.write(contents)
    finally:
        f.close()

# Determine which keys are used
def _subst_keys(source, pattern):
    # Read file
    f = open(source, "rU")
    try:
        contents = f.read()
    finally:
        f.close()

    # Determine keys
    keys = []
    def subfn(mo):
        key = mo.group("key")
        if key:
            keys.append(key)
        return ""

    re.sub(pattern, subfn, contents)

    return keys

# Get the value of a key as a string, or None if it is not in the environment
def _subst_value(env, key):
    # Why does "if key in env" result in "KeyError: 0:"?
    try:
        env[key]
    except KeyError:
        return None

    # Do a raw substitution so it will not replace tabs/whitespaces with a
    # single space.  This will return a string even if the result really
    # isn't, such as env['HAVE_STRDUP'] = 0
    return env.subst("${%s}" % key, 1)


# Builder related functions
##############################################################################

# Builder action
def _subst_action(target, source, env):
    # Substitute in the files
    pattern = env["SUBST_PATTERN"]
    replace = env["SUBST_REPLACE"]

    for (t, s) in zip(target, source):
        _subst_file(str(t), str(s), env, pattern, replace)

    return 0

# Builder message
def _subst_message(target, source, env):
    items = ["Substituting vars from %s to %s" % (str(s), str(t))
             for (t, s) in zip(target, source)]

    return "\n".join(items)

# Builder dependency emitter
def _subst_emitter(target, source, env):
    pattern = env["SUBST_PATTERN"]
    for (t, s) in zip(target, source):
        # When building, if a variant directory is used and source files
        # are being duplicated, the source file will not be duplicated yet
        # when this is called, so the real source must be used instead of
        # the duplicated source
        path = s.srcnode().abspath

        # Get keys used
        keys = _subst_keys(path, pattern)

        d = dict()
        for key in keys:
            value = _subst_value(env, key)
            if not value is None:
                d[key] = value

        # Only the current target depends on this dictionary
        Depends(t, SCons.Node.Python.Value(d))

    return target, source


# Replace @key@ with the value of that key, and @@ with a single @
##############################################################################

_SubstFile_pattern = "@(?P<key>\w*?)@"
def _SubstFile_replace(env, mo):
    key = mo.group("key")
    if not key:
        return "@"

    value = _subst_value(env, key)
    if value is None:
        raise SCons.Errors.UserError("Error: key %s does not exist" % key)
    return value
    
def SubstFile(env, target, source):
    return env.SubstGeneric(target,
                            source,
                            SUBST_PATTERN=_SubstFile_pattern,
                            SUBST_REPLACE=_SubstFile_replace)


# A substitutor similar to config.h header substitution
# Supported patterns are:
#
# Pattern: #define @key@
# Found:   #define key value
# Missing: /* #define key */
#
# Pattern: #define @key@ default
# Found:   #define key value
# Missing: #define key default
#
# Pattern: #undef @key@
# Found:   #define key value
# Missing: #undef key
#
# The "@" is used so that these defines can be used in addition to
# other defines that you do not desire to be replaced.  Also, each
# key can specify a format to apply some formatting to the returned
# value if used:
#
# str: The returned value will be enclosed in double quotes and escaped
# chr: The returned value will be enclosed in single quotes and escaped
#
# Example:
#
# #define @key:str@ "Default"
#
##############################################################################

# Escape function
_SubstHeader_escape_map = { "\n": "\\n",
                            "\r": "\\r",
                            "\t": "\\t",
                            "\\": "\\\\",
                            "\0": "\\0",
                            "\"": "\\\"",
                            "\'": "\\\'" }
def _SubstHeader_escape(value):
    # TODO: support replacement on all characters that need it
    result = []
    for i in value:
        if i in _SubstHeader_escape_map:
            result.append(_SubstHeader_escape_map[i])
        else:
            result.append(i)

    return "".join(result)

# Format functions
def _SubstHeader_format_chr(value):
    escaped = _SubstHeader_escape(value)

    return "\'%s\'" % escaped[0]

def _SubstHeader_format_str(value):
    escaped = _SubstHeader_escape(value)

    return "\"%s\"" % escaped

_SubstHeader_formats = { "chr": _SubstHeader_format_chr,
                         "str": _SubstHeader_format_str }


# Actual substitution
_SubstHeader_pattern = "(?m)^(?P<space>\\s*?)(?P<type>#define|#undef)\\s+?@(?P<key>\w+?)(:(?P<fmt>\w+?))?@(?P<ending>.*?)$"
def _SubstHeader_replace(env, mo):
    space = mo.group("space")
    type = mo.group("type")
    key = mo.group("key")
    ending = mo.group("ending")
    fmt = mo.group("fmt")

    value = _subst_value(env, key)
    if not value is None:
        if fmt in _SubstHeader_formats:
            value = _SubstHeader_formats[fmt](value)

        # If found it is always #define key value
        return "%s#define %s %s" % (space, key, value)
        
    # Not found
    if type == "#define":
        defval = ending.strip()
        if defval:
            # There is a default value
            return "%s#define %s %s" % (space, key, defval)
        else:
            # There is no default value
            return "%s/* #define %s */" % (space, key)

    # It was #undef
    return "%s#undef %s" % (space, key)
        
def SubstHeader(env, target, source):
    return env.SubstGeneric(target,
                            source,
                            SUBST_PATTERN=_SubstHeader_pattern,
                            SUBST_REPLACE=_SubstHeader_replace)


# Create builders
##############################################################################
def TOOL_SUBST(env):
    # The generic builder
    subst = SCons.Action.Action(_subst_action, _subst_message)
    env["BUILDERS"]["SubstGeneric"] = Builder(action=subst,
                                              emitter=_subst_emitter)

    # Additional ones
    env.AddMethod(SubstFile, "SubstFile")
    env.AddMethod(SubstHeader, "SubstHeader")
```

### SubstFile

The [SubstFile](SubstFile) builder works just like [SubstInFile2](SubstInFile2), replacing any pattern of "@name@" with the value of that environment variable, and any "@@" with a single "@".  If the environment variable does not exist it will result in an error instead of silently replacing it with an empty string. 

SConstruct: 


```txt
import subst

env = Environment()
TOOL_SUBST(env)

env["DISPLAY_NAME"] = "My Application 2009"
env["PREFIX"] = "/usr/local"
env["DESCRIPTION"] = "An application to do something."

env.SubstFile("myapp.desktop", "desktop.in")
```
desktop.in: 


```txt
[Desktop Entry]
Encoding=UTF-8
Name=@DISPLAY_NAME@
Type=Application
Comment=@DESCRIPTION@
TryExec=@PREFIX@/bin/myapp
Exec=@PREFIX@/bin/myapp
Icon=@PREFIX@/share/myapp/pixmaps/mainicon.svg
```
myapp.desktop: 


```txt
[Desktop Entry]
Encoding=UTF-8
Name=My Application 2009
Type=Application
Comment=An application to do something.
TryExec=/usr/local/bin/myapp
Exec=/usr/local/bin/myapp
Icon=/usr/local/share/myapp/pixmaps/mainicon.svg
```

### SubstHeader

This works a little bit different than autotools, but the basic idea is the same.  Certain matches as described in the source file will be replaced with the value from the environment if available.  If not available, then it will be replaced according to the type of define statement.  In addition, the names in the define statement are still surrounded with "@" to control which statements may be substituted or not.  A define statement without "@" around the name will not be substituted. 

SConstruct: 


```txt
import subst

env = Environment()
TOOL_SUBST(env)

env["HAVE_STRDUP"] = 1
env["WITH_WXWIDGETS"] = 1
env["HAVE_MATH_H"] = 1

env.SubstHeader("config.h", "config.h.in")
```
config.h.in: 


```txt
// If you do not use @NAME@ then it will not be a candidate for substitution.  This
// allows regular defines to be placed in a config.h.in type file as well without
// needing to make sure they are not environment variables that would be substituted.
#define COPYRIGHT "Copyright (C) 2009 Foobar"

// This provides a default value if the key is not in the environment.
#define @HAVE_STRDUP@ 0
#define @HAVE_STRCAT@ 0

// If there is no defualt value and it is not in the environment, it will be commented out
#define @WITH_WXWIDGETS@
#define @WITH_OPENGL@

// If #undef is used and the value is not in the environment, it will emit an #undef statement
#undef @HAVE_MATH_H@
#undef @HAVE_STRING_H@
```
config.h.in: 


```txt
// If you do not use @NAME@ then it will not be a candidate for substitution.  This
// allows regular defines to be placed in a config.h.in type file as well without
// needing to make sure they are not environment variables that would be substituted.
#define COPYRIGHT "Copyright (C) 2009 Foobar"

// This provides a default value if the key is not in the environment.
#define HAVE_STRDUP 1
#define HAVE_STRCAT 0

// If there is no defualt value and it is not in the environment, it will be commented out
#define WITH_WXWIDGETS
/* #define WITH_OPENGL */

// If #undef is used and the value is not in the environment, it will emit an #undef statement
#define HAVE_MATH_H 1
#undef HAVE_STRING_H
```

### Custom Substitution

To create a custom substitution, all that is needed is a pattern to match for and a function that will be called to return the substituted value.  The pattern must have a named parameter called "key" which will be used for dependency tracking.  The function will take the environment and the regular expression match object as parameters.  If an there is an error such as a missing variable if it is required, the function should raise a SCons.Errors.[UserError](UserError) 


```python
#!python 
pattern = "#(P<key>\w*?)#"
def replace(env, mo):
    key = mo.group("key")
    if not key:
        return "#"

    # "if key in env: ..." causes a KeyError for some reason instead of "key in env" being False
    # So test like this instead
    try:
        env[key] 
    except KeyError:
        raise SCons.Errors.UserError("Key not found: %s" % key)

    return env.subst("${%s}" % key); 
        
env.SubstGeneric("output", "input.h", SUBST_PATTERN=pattern, SUBST_REPLACE=replace)
```
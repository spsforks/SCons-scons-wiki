**UPDATE: SCons 1.3.0 and later ships with the [Substfile](http://www.scons.org/doc/production/HTML/scons-user.html#b-Substfile) builder which should probably be used instead.**

This is a substitution builder much like the original [SubstInFileBuilder](SubstInFile) builder.  This builder directly uses the environment as the substitution dictionary and emits only the keys a given target uses as dependencies of that target.  The values in the environment to be substituted should either be strings or functions that return to a string.  An environment substitution will occur on the result first before it is replaced in the file.

Example Usage:

```python
#!python
env = Environment()
TOOL_SUBST(env)

def f():
    return "Test"

env['NAME'] = 'John Doe'
env['VERSION'] = '2.10.0'
env['FULLNAME'] = '$NAME $VERSION'
env['FUNCTION'] = f

env.SubstInFile('output', 'input')
```

Sample input file:

```txt
Name: @NAME@
Version: @VERSION@
Fullname: @FULLNAME@
Function: @FUNCTION@
Email: johndoe@@nowhere.com
```

Ouput of that file:

```txt
Name: John Doe
Version: 2.10.0
Fullname: John Doe 2.10.0
Function: Test
Email: johndoe@nowhere.com
```

The builder code:

```python
#!python
# File:         subst.py
# Author:       Brian A. Vanderburg II
# Purpose:      SCons substitution in file mechanism
# Copyright:    This file is placed in the public domain.
# Notice:       Portions of this file are based on the original
#               SubstInFile builder.
########################################################################


# Requirements
########################################################################
import re

from SCons.Script import *
import SCons.Errors


# This will replace any occurance of @keyname@ with the value of the
# key from the environment dictionary.  @@ will produce a single @
########################################################################

_searchre = re.compile('@(.*?)@')

def subst_file(target, source, data):
    # subfunction
    def subfn(mo, data=data):
        key = mo.group(1)
        if key == '':
            return '@'
        return data[key]

    # read file
    f = open(source, 'rU')
    try:
        contents = f.read()
    finally:
        f.close()

    # substitute
    contents = _searchre.sub(subfn, contents)

    # Write file
    f = open(target, 'wt')
    try:
        f.write(contents)
    finally:
        f.close()

def subst_keys(source):
    keys = []

    # subfunction
    def subfn(mo):
        key = mo.group(1)
        if key != '':
            keys.append(key)
        return ''

    # read file
    f = open(source, 'rU')
    try:
        contents = f.read()
    finally:
        f.close()

    # determine keys
    _searchre.sub(subfn, contents)

    return keys

def subst_in_file(target, source, env):
    # What keys do the sources use
    keys = []

    for s in source:
        skeys = subst_keys(str(s))
        for k in skeys:
            if not k in keys:
                keys.append(k)

    # Get these keys from the environment
    d = dict()
    for k in keys:
        try:
            v = env[k]
        except:
            raise SCons.Errors.UserError('SubstInFile key not found in environment: ' + k)

        if callable(v):
            d[k] = env.subst(v())
        elif SCons.Util.is_String(v):
            d[k] = env.subst(v)
        else:
            raise SCons.Errors.UserError('SubstInFile key must be a string or callable: ' + k)

    # Substitute in the files
    for (t, s) in zip(target, source):
        subst_file(str(t), str(s), d)

    return 0


def subst_string(target, source, env):
    items = ['Substituting vars from %s to %s' % (str(s), str(t))
             for (t, s) in zip(target, source)]

    return '\n'.join(items)

def subst_emitter(target, source, env):
    for (t, s) in zip(target, source):
        # Get keys used
        keys = subst_keys(str(s))

        d = dict()
        for k in keys:
            try:
                v = env[k]
            except:
                raise SCons.Errors.UserError('SubstInFile key not found in environment: ' + k)

            if callable(v):
                d[k] = env.subst(v())
            elif SCons.Util.is_String(v):
                d[k] = env.subst(v)

        # Only the current target depends on this dictionary
        Depends(t, SCons.Node.Python.Value(d))

    return target, source

# create builders
def TOOL_SUBST(env):
    subst_in_file_action = SCons.Action.Action(subst_in_file, subst_string)
    env['BUILDERS']['SubstInFile'] = Builder(action=subst_in_file_action,
                                             emitter=subst_emitter)
```


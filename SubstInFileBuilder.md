
UPDATE: SCons 1.3.0 and later ships with [textfile.Substfile](http://scons.org/doc/production/HTML/scons-user/a8588.html#b-Substfile) builder which works like this tool. 

Here's a tool that does substitutions from a dictionary on a file.  This code is freely available for your use. --[GaryOberbrunner](GaryOberbrunner) 

This should work with 0.96.91 or later; earlier versions may or may not work due to the import statement (but the rest should be OK). 


```python
#!python

import re
from SCons.Script import *  # the usual scons stuff you get in a SConscript

def TOOL_SUBST(env):
    """Adds SubstInFile builder, which substitutes the keys->values of SUBST_DICT
    from the source to the target.
    The values of SUBST_DICT first have any construction variables expanded
    (its keys are not expanded).
    If a value of SUBST_DICT is a python callable function, it is called and
    the result is expanded as the value.
    If there's more than one source and more than one target, each target gets
    substituted from the corresponding source.
    """
    env.Append(TOOLS = 'SUBST')
    def do_subst_in_file(targetfile, sourcefile, dict):
        """Replace all instances of the keys of dict with their values.
        For example, if dict is {'%VERSION%': '1.2345', '%BASE%': 'MyProg'},
        then all instances of %VERSION% in the file will be replaced with 1.2345 etc.
        """
        try:
            f = open(sourcefile, 'rb')
            contents = f.read()
            f.close()
        except:
            raise SCons.Errors.UserError, "Can't read source file %s"%sourcefile
        for (k,v) in dict.items():
            contents = re.sub(k, v, contents)
        try:
            f = open(targetfile, 'wb')
            f.write(contents)
            f.close()
        except:
            raise SCons.Errors.UserError, "Can't write target file %s"%targetfile
        return 0 # success

    def subst_in_file(target, source, env):
        if 'SUBST_DICT' not in env:
            raise SCons.Errors.UserError, "SubstInFile requires SUBST_DICT to be set."
        d = dict(env['SUBST_DICT']) # copy it
        for (k,v) in d.items():
            if callable(v):
                d[k] = env.subst(v())
            elif SCons.Util.is_String(v):
                d[k]=env.subst(v)
            else:
                raise SCons.Errors.UserError, "SubstInFile: key %s: %s must be a string or callable"%(k, repr(v))
        for (t,s) in zip(target, source):
            return do_subst_in_file(str(t), str(s), d)

    def subst_in_file_string(target, source, env):
        """This is what gets printed on the console."""
        return '\n'.join(['Substituting vars from %s into %s'%(str(s), str(t))
                          for (t,s) in zip(target, source)])

    def subst_emitter(target, source, env):
        """Add dependency from substituted SUBST_DICT to target.
        Returns original target, source tuple unchanged.
        """
        d = env['SUBST_DICT'].copy() # copy it
        for (k,v) in d.items():
            if callable(v):
                d[k] = env.subst(v())
            elif SCons.Util.is_String(v):
                d[k]=env.subst(v)
        Depends(target, SCons.Node.Python.Value(d))
        return target, source

    subst_action=SCons.Action.Action(subst_in_file, subst_in_file_string)
    env['BUILDERS']['SubstInFile'] = Builder(action=subst_action, emitter=subst_emitter)

```
Here's how to use it: 


```python
#!python
# Load the above tool either by importing it or just including the text in this file
env=Environment(tools=('default', TOOL_SUBST))
# or you could just call TOOL_SUBST(env), same thing.

# This will replace all %FOO% with FooValue in foo.in, creating foo.out.
env.SubstInFile('foo.out', 'foo.in',
                SUBST_DICT={'%FOO%': 'FooValue'})
```
I found I needed to add `varlist=['SUBST_DICT']` as a keyword argument to the subst_action for Scons to regenerate the output file if the SUBST_DICT has changed and the output file already exists.  --[TimPotter](TimPotter) 

Hi Tim; that's what the subst_emitter is supposed to do; I wonder why it didn't work for you?  If you send me a testcase (on [dev@scons.tigris.org](mailto:dev@scons.tigris.org)) I'll look into it.  I'd like to get this into SCons sometime, so I'm interested in improving it. --[GaryOberbrunner](GaryOberbrunner) 

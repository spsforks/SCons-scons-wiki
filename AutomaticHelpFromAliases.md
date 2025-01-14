From Gary Oberbunner's technique, I came up with the following wrapper functions. They can be used to build the help text automatically from all of your Alias() commands: 

```python
from SCons.Script.SConscript import SConsEnvironment

# -- ------------------
# -- jDataClass holds data for the helper functions
class jDataClass:
    mHelpText = {}
    mHelpTextHead = []
    mHelpTextTail = []

SConsEnvironment.jData = jDataClass()
# -- ------------------
# -- wraps Alias to put the alias name in the help text
def jAlias(self, aliasname, tgt, helptext=None):
    thealias = self.Alias(aliasname, tgt)
    lcaliasname = aliasname.lower()
    if helptext is None:
        if not self.jData.mHelpText.has_key(lcaliasname):
            self.jData.mHelpText[lcaliasname] = "???"
    else:
        self.jData.mHelpText[lcaliasname] = helptext
    return thealias

SConsEnvironment.jAlias = jAlias
# -- ------------------
# -- adds a line of text to the help heading
def jHelpHead(self, msg):
    self.jData.mHelpTextHead.append(msg)

SConsEnvironment.jHelpHead = jHelpHead
# -- ------------------
# -- adds a line of text to the help footing
def jHelpFoot(self, msg):
    self.jData.mHelpTextTail.append(msg)

SConsEnvironment.jHelpFoot = jHelpFoot
# -- ------------------
# -- generates the help
def jGenHelp(self):
    tmp = []
    tmp.extend(self.jData.mHelpTextHead)
    keys = self.jData.mHelpText.keys()
    keys.sort()
    maxlen = 0
    for a in keys:
        if len(a) > maxlen:
            maxlen = len(a)
    for a in keys:
        s = " %-*s : %s" % (maxlen, a, self.jData.mHelpText[a])
        tmp.append(s)
    tmp.extend(self.jData.mHelpTextTail)
    self.Help("\n".join(tmp))


SConsEnvironment.jGenHelp = jGenHelp
# -- ------------------
# -- adds upper/lower case of alias names for a target
def jSetAliases(self, projname, tgt):
    self.jAlias(projname, tgt)
    self.jAlias(projname.lower(), tgt, "compile " + projname)

SConsEnvironment.jSetAliases = jSetAliases

# SConsEnvironment.dev = Dev()

env = Environment()
env.jHelpHead("First line of Help...")
env.jHelpFoot("Last line of Help...")

# use jAlias like Alias() except that you can add an optional bit of help text to it
env.jAlias("prepare_downloads", prepalias, "prepare 'downloads' html page")
 
#... other stuff here ...
 
#--- this statement must be the last in the file
env.jGenHelp()
```
when you do scons -h you get the help for all of your aliases automatically: 


```console
scons: Reading SConscript files ...
**** Compiling in debug mode...
scons: done reading SConscript files.
First line of Help...
   prepare_downloads : prepare 'downloads' html page
Last line of Help...
Use scons -H for help about command-line options.
```

# Comment

This is really useful, and I'd vote for such functionality being added to the core `Alias` function. However, what happens if `kAlias` is called twice for the same target, i.e. adding targets to an alias, but the second call doesn't have any help text. Doesn't it overwrite the existing help text? 

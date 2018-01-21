Thoughts on possible improvements for Subst().

# Generally the following are True for Subst #
1. There are few unique strings stored among all Environment()'s created or cloned
1. Most cloned Environments are mostly the same as all (or many others)
1. Subst() is called several orders of magnitude more than there are command lines and/or unique strings
1. The following are potentially the only unique items for most command lines (and are thus not cacheable) [ list from SCons.Environment.reserved_construction_var_names ](http://scons.org/doc/latest/HTML/scons-api/SCons.Environment-module.html#reserved_construction_var_names)
    * CHANGED_SOURCES
    * CHANGED_TARGETS
    * SOURCE
    * SOURCES
    * TARGET
    * TARGETS
    * UNCHANGED_SOURCES
    * UNCHANGED_TARGETS
    * *callable values in Environment's dict.*


# Notes about current implementation #
1. The subst logic is called with a dictionary of local and global values and the string (or list) to be evaluated
1. Most of the time the global dictionary passed is the values from the Environment() being used by the task to build the target (or to evaluate if the target is out of date which requires the command line string to be evaluated). The local dictionary passed may be the TARGET and SOURCE information.
1. The subst logic often involves recursive calls to itself or it's peers (string and list versions of subst)
1. Subst current is composed of two steps
    1. tokenize the string (currently via regex)
    1. recursively evaluate the string
1. Subst can be called in two basic modes
    1. create a command line
    1. create a string for comparing signature  (this drops items between $( and $) )
1. If the evaluated string is a callable, it is called as follows

```
#!python

    callable(target,source,env,for_signature)
```


# Notes about improvement implementation #
1. Tokenize Environment() variables when they are set.
   * Actually tokenize strings (and variables) which will be evaluated by Subst.  (As a user can call (repeatedly) env.Subst("$A $B ${some python logic}..") so ideally we'll tokenize this and store with the original string and other information needed to expand this into a simple string.
1. Scan tokens to identify directly accessed variables. Add these to set which will be checked to invalidate cache when other variables are set. (Including list above)
1. Consider altering strings generated for signatures to exclude SOURCE and TARGET unless they are modified (.abspath,etc ).  This would allow using pre-expanded variables (for example CXXCOM would have everything but TARGET and SOURCE pre expanded, so for signatures this should be a **LOT** faster). Also since the current signature information includes the sources and the targets (and other dependencies), we don't really need them to be in the string used to determine if we need to rebuild.
1. On env.Clone() make shallow copy of environment variables, and then use copy-on-write if the variable changed
1. Handle OverrideEnvironments().. They basically have a "layer" of new variable values which override the existing ones in their "parent" Environment()

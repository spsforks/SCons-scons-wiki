

## Better Error Messages

This is a draft.  Feel free to edit.  If you have questions, please pose them on the mailing list. 

It is believed [#863](/SCons/scons/issues/863), [#1437](/SCons/scons/issues/1437), [#1442](/SCons/scons/issues/1442), [#1871](/SCons/scons/issues/1871) and [#1895](/SCons/scons/issues/1895) are exemplars of this problem. 


### The Problem(s)

There are two ways that a missing Builder can be observed by a user: 

* Attempting to use the Builder by name (_e.g._, `env.BuilderName( ... )`) 
* Refering to a Builder's source suffix (_e.g._, `Program('file.xyz')`) 

Currently, both cases generate opaque error messages (or worse, no error message and appear to work).  The objective is that both cases should generate descriptive error messages. 

Another related difficulty with the current scheme is that full toolchains are not deduced.  That is, if a user adds a Builder that converts `.xyz` to `.c` then it requires extra steps so that SCons will be able to turn this into a `.o`.  And if it's not set up correctly, the error message is opaque about what went wrong. 

A somewhat-related difficulty to the previous point is the use of non-standard suffixes.  A user might wish to use the suffix `.cplusplus` on a C++ file for legacy reasons, yet adding this suffix is painful (or not possible?).  (It should also be possible to remove suffixes.) 


### Analysis

From the user's perspective, SCons should act as if all Builders were present at all times, but only Builders configured into a specific Environment are in play.  That is, SCons should always be able to determine that a Builder should be used (if not always which one), and only generate an error if the required Builder isn't configured. 

This implies that the process of setting up the toolchains should be separate from the actual configuration of a Builder.  The toolchain information (the relationship between source and target suffixes and the Builder name) should always be established, while the Builder itself would only be configured if the circumstances warrant (_i.e._, if the command exists for a default builder or if the Builder is explicitly configured). 


### Implications

The implications are twofold: 

* All `.src --> .tgt` transitions must be known globally to SCons. 
* All Builder names must be known globally to SCons. 
The problem is how to get there from here. 


### Possible Strategy

There's one possible strategy that SCons could employ: 

* SCons should initialize all standard Builder names in a global table. 
* SCons should initialize all `.src --> .tgt` pairs for all standard (_i.e._, provided by SCons) Builders in a global table. 
* User-provided Builders should have their Builder name(s) and `.src --> .tgt` pair(s) added to the global tables. 
* If an Environment gets an `AttributeError`, the global table of Builder names is consulted to determine what type of error message should be generated. 
* If the source-to-target transition is not known in the current Environment, the global table is consulted to determine what type of error message should be generated. 
I'm not sure that this is the best strategy (it seems to have a lot of overhead), but it shows that there is at least one strategy that will deal with the difficulties. 



---

 

Still open: 

* How much overhead is it necessary to induce? 
* How much additional overhead is acceptable? 
* How to get user-created suffixes? 

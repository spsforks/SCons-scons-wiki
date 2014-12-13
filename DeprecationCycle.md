

# Deprecation Cycle

SCons takes backward compatibility very seriously.  Our policy is that an existing feature can only be dropped at a major release (_i.e._, an _X_.0 release).  In addition, such features are required to go through a series of steps before they are removed so that our users have plenty of time to update their SConscripts on their own schedule. 

Because of this commitment, it takes a long time to completely remove a feature.  In general, the decision to drop a feature is made a full major release in advance so that the replacement functionality (if any) can be present at a major release. 

This page describes the steps, but note that this procedure is a guideline, not something cast in concrete.  It's a very strong guideline, but some flexibility is expected. 

Tracking the status of deprecated features will take place in the [DeprecatedFeatures](DeprecatedFeatures) page. 


### 0. The replacement functionality is implemented

In general, if something is removed, there must be another way, hopefully better, of doing the same task.  Functionality may be dropped if we believe it is no longer used and no longer useful, but if we find users (and useful cases) we will rethink whether it should be dropped. 

Usually, the replacement functionality is present for some period of time (at least a minor release cycle) prior to the start of the actual deprecation cycle, to see how it works out in practice.  This is not absolutely required, but it's done whenever possible. 


### 1. Deprecation announced / feature deprecated in manual

The manual is updated to say that the feature will be deprecated and describing how to replace it.  This verbiage should be in place for one or two minor releases (give or take).  See the next step for more information about the timing. 

Starting at this point, release announcements will mention the status of the deprecated feature. 


### 2. Initial deprecation warning

A deprecation warning, off by default, is issued when the feature is used.  It can be enabled by the `--warn=all-deprecated` command line option.  (Presumably, there will also be an option to turn the individual warning on or off, but it wouldn't be particularly useful unless one already knew about it.) 

The idea is that users can check to see if any feature they are using is being deprecated and fix things before the warning becomes more intrusive.  People who distribute their SConscripts would routinely run with `--warn=all-deprecated` so they can be proactive about fielding fixes before their own customers complain. 

The manual now says "is" rather than "will be" deprecated. 

This should be in place for about two minor releases (give or take), more is better. 

Since the message is silent by default, the boundary between this step and the previous step is soft.  In other words, the exact number of releases for each step is flexible and is more a function of the elapsed time involved.  The total time for both steps should be on the order of six months if a minor change is required (change the name of a function), more if code would need to be revamped. 


### 3. Suppressible deprecation warning

The deprecation warning is now on by default.  The message can be suppressed by the `--warn=no-deprecated` command-line option or by an individual option. 

This is often the first time your average user will learn that they have to make changes to their SConscripts.  The theory is that they will usually be the small-scale hobbyist (without a large "tail" of downstream users) so the individual impact will be small.  However, they still may need some time before they can make the changes, so the option exists for them to ignore the warning for now. 

This step should take at least one minor release, at least two is preferred, more is better. 


### 4. Unsuppressible deprecation warning

The deprecation warning is now always on and cannot be suppressed.  Yes, it's rude.  The intent is to be sufficiently rude (without being too offensive) that the necessary code changes will be made before the feature is dropped. 

Normally, this is done for the last minor release before the major release where the feature will be dropped, but if the changes required are "significant" it may occur earlier. 


### 5. Feature dropped

The deprecation warning becomes a fatal error.  Note that the feature is still recognized; it just can't be used any more. 

The documentation still describes the feature (but now says "obsolete" rather than "deprecated") so users can find out what to do to upgrade. 

This step must be done at a major release. 

The announcement for the release identifies that the feature is no longer available.  This is the last status note about the feature. 

Developers can begin to remove the code that supports the feature. 


### 6. Documentation removed

At some later point, often the next major release subsequent to the feature being dropped, the documentation for the feature is removed. 

The error message may be removed, but could remain longer (potentially forever). 

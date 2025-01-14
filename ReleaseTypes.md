

# Release Types

Release numbers are usually of the form _major.minor.micro_ but are occasionally of the form _major.minor.micro.nano_.  Each type of release indicates the kind of changes that the user can expect in that particular release. 

For completeness, this page also describes a checkpoint, even though it's technically not a mainstream release. 


## Major release

A major release is _backwards-unstable_.  That is, the external API can change.  In the usual case, the user-visible change is that features will be deprecated or that deprecated features will be removed, but occasionally there will be true incompatible changes to the API. 

Deprecated features go through five states; the fourth is the only place that must be a major release (it's not backward compatible), while the others are often relegated to minor releases: 

* The man page is altered to say that the feature is deprecated; a replacement feature, if any, is available. 
* A warning is issued when the feature is used in a SConscript, but the feature is still allowed; this warning can be suppressed by a command-line option. 
* A warning is issued when the feature is used in a SConscript, but the feature is still allowed; this warning can <ins>_not_</ins> be suppressed. 
* An error is issued when the feature is used in a SConscript, but the feature is still recognized in order to generate the error. 
* The feature is removed and no longer recognized. 
Extended warranty: Since a major release may cause user SConscripts to be revised, the prior major release will be maintained with bug fixes (but no new features) for a "long" time _(the exact value for "long" needs to be determined, but probably should be in the twelve to twenty-four month range)_ and there will be a way for the two releases to coexist in the same system. 


## Minor release

A minor release is a boundary where it is not possible to revert to a previous minor release without forcing a complete rebuild.  Moving to a new minor release <ins>_may_</ins> cause objects to be rebuilt unnecessarily.  Internal interfaces are changed; a SConscript that depends on an undocumented feature may break. 

_(Comment:  The idea is that internal data structures have changed and an older release won't know how to deal with the new layout.  This could be implemented by recording the release ID in the .sconsign.  If the recorded minor release is higher than the current one, ignore the .sconsign and other cached information and rebuild from scratch.  If the recorded minor release is lower than the current one, the data structures are converted to the extent possible.)_ 

Limited warranty: Since a minor release may require some SConscripts to be tweaked, the prior minor release will be will be maintained with bug fixes (but no new features) for a "short" time _(the exact value for "short" needs to be determined, but probably should be in the six to nine month range: one or two micro releases)_ and there will be a way for the two releases to coexist in the same system. 


## Micro release

A micro release can only add new external and internal APIs; existing APIs are guaranteed to be unchanged.  As long as a SConscript doesn't use any features that are new in later micro releases, the user may freely switch between micro releases. 

Minimal warranty: Since micro releases are interchangeable, the only thing that can happen to a minor release is to have a serious defect that requires a nano release. 


## Nano release

A nano release is an urgent patch that needs to be applied immediately.  If a defect is found that causes major problems, all the releases containing the defect will grow a nano release with the fix.  This is the only time that a four-number release will ever be made, so they are very visible. 

Warranty: A nano release inherits the warranty of the release it patches. 


## Checkpoints

A checkpoint can be considered a beta release; it's a point between mainstream releases that is expected to be stable.  A checkpoint can also be a release candidate for the next mainstream public release. 

No warranty: Problems in a checkpoint will be the highest-priority items for the next checkpoint, but there's no guarantee that any given checkpoint will be retained or have bugs fixed.  In general, the "fix" for a problem in a checkpoint is to upgrade to the next checkpoint. 


## Releases prior to 1.0.0

Prior to the initial public release, development tends to be fast enough that micro releases aren't done.  As a result, the release number is of the form _0.major.minor_, that is, the micro identifier isn't used and a zero is used in the initial position.  Bug fixes are rarely made for a prior release, so nano releases don't occur either. 

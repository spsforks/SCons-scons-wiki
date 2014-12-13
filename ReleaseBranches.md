

# Release Branches

There are three primary branches: the "unstable" or "development" branch, the "stable" or "checkpoint" branch, and the "release" or "production" branch. Each of these is discussed below. 

The driving force of the release process is the [release team](Release_Team), which sets the release dates, selects the features to be present in the release and promotes them to the release branch, cuts and distributes the actual release, and announces the release as appropriate. 

This information is synthesized from a [discussion](ReleaseBranches/Discussion) in scons-dev that started in April 2007.  As of this writing, it is not considered canonical, although informal checkpoints are now being created off the trunk. 

Although the intent of the release stages is sketched, the details of the process still need to be figured out and assigned. Hopefully, this document will be filled out as that takes place. 


## Unstable development branch

This branch is found in `branches/core` in the repository.  It really ought to be named `unstable` but this is the name we have for historical reasons.  It acts as the focus for alpha testing (_i.e._, testing by other developers). 

This is the branch where original development takes place.  Less-permanent forks may be made from this branch for specific features.  A less-permanent fork can be as informal as a checked-out tree on a user's machine where someone is fiddling with a change, or as formal as an actual fork in the repository (typically from some base position on this branch; it would be in `branches/`_feature_). However formal or informal it may be, this branch where most development takes place. It eventually leads to one or more _patches_ being applied to `branches/core`; the complete set of patches for a given feature is called a _development patchset_. 

This branch is where patches mature. Patches are checked in here, where developers can run them through their paces, find and repair problems (which are added to the patchset for this feature), and make sure there are no unexpected side-effects. 

On a frequent basis, the release team reviews all features that haven't been migrated to the checkpoint branch and decides which should be held, which should be promoted, and which should be dropped.  As a rule most features would be promoted pretty much automatically; the features not promoted would be those large and complex enough that they need some seasoning or features that are still showing bugs in the early testing. 

For features being promoted, the feature's patchset is applied to the stable checkpoint branch and the test suite is run to ensure that the branch is still "golden" (see below).  This makes the feature available to the beta community. 

For features being dropped, the feature's patchset is archived (exact method has not yet been determined, but in some way that work on it can continue) and the patchset itself is reverted.  (The exact policy has not yet been determined; the suggestion is that no more than N features can be active on this branch, so "old hoary stuff" would have to be removed before new features could be added.) 

Bug fixes for features already promoted are effectively a special case; they are passed on to the stable checkpoint branch immediately. 

In general, the release where a given patchset will be released is not known in advance, so the unstable branch has no release identifier.  If the current state of the unstable development branch is packaged, it is known solely by its repository revision number (so it has a name like `scons-r1234`). 

Checkins to this branch are not tagged. 


## Stable checkpoint branch

This branch is the "golden thread" for checkpoint releases.  It is expected that anything checked in to this branch is of production quality and passes all regression tests.  As of this writing, the branch does not exist in SVN, but it could easily be created with a name like '`latest`' or '`current`' or '`stable`' or '`checkpoint`' or any number of other names.  It acts as the focus of beta testing (_i.e._, a friendly community of interested users who are willing to download new features and try them out). 

Once a feature is mature and deemed stable enough, it is added to this branch by applying its development patchset as a unit (_i.e._, a single patch operation).  This becomes the initial (and usually only) member of the feature's _checkpoint patchset_. If a problem develops with a feature in this branch, the fix is first checked in to the development branch (and added to the feature's development patchset) and then applied to this branch and added to the feature's checkpoint patchset. 

Features can be removed from this branch if they are deemed too problematical by reverting the patchset. Note that such features remain in the unstable development branch and may be reconsidered at a later time.  Note that this is very different from the production release branch; features release to the general public cannot be removed without an extended period of being deprecated. 

The release team establishes the date for checkpoint releases; in general, it is expected that checkpoints will be released every month or two.  On that date, the patchsets that have accumulated in this branch are packaged to create a _checkpoint_, that is, an intermediate stable point on the way to the next release. Checkpoints are published, but since they are effectively a beta release, the announcement is restricted to a smaller audience. 

A "normal" checkpoint has the features as the prior mainstream release (_i.e._, deprecated features have not yet been removed); it uses the date to identify where it is in the sequence, so it has a name like `scons-1.2.3.d20080521`. 

The last "normal" checkpoint is typically cut a few weeks before a mainstream release date.  At that point, the feature set for the new mainstream release is in place, so no more features are promoted into this branch (bug fixes are accepted).  A week or two before the mainstream release, a special checkpoint is cut; this checkpoint is a _release candidate_ and it is made available for testing; if necessary, additional release candidates are cut. A release candidate with no blocking issues can be promoted to a production release. 

Checkpoints are tagged as `tags/`_x.y.z-dyyyymmdd_ in the repository. 


## Production release branch

This thread is the "golden thread" for mainstream production releases of SCons. It is found in `trunk` in the repository.  It really ought to be called `release` but `trunk` is what we have for historical reasons.  Only official public releases are located here, so that checking out this branch guarantees that one is getting the latest release. 

The release team sets the time for release, coordinating it with the schedule for checkpoint releases.  It also selects the feature set that is intended to be present in the release, and keeps track of the features as they are developed to make sure they land in a (normal) checkpoint in a timely manner. 

To create a new release, the version number in the checkpoint branch is rolled [as appropriate](ReleaseTypes), all of the checkpoint patchsets (including the new version number) are applied to this branch (as a unit?), the branch is packaged and published, and a great sigh of relief is heard. In general, it is expected that production releases will occur two to three times a year. 

It's expected that almost no work will occur in this branch.  In effect, each update to this branch is just copying the current release candidate checkpoint to it (with probably a trivial change that marks it as the production release rather than the checkpoint).  The only time any work will be done on this branch is when it's necessary to add an urgent bug fix. 

In general, no forks are formed off of this branch.  However, if a sufficiently egregious defect is found, it's possible that prior releases may need to be fixed (in addition to the current release).  In that case, a fork is created from the prior release and the patch applied to the fork.  (If an egregious defect is found in the current release, there's no need to fork; it's simply applied to the trunk with a new release number.) 

Releases are tagged as `tags/`_x.y.z_ in the repository. 

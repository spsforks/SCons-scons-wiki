These instructions use outdated workflow based on svnmerge tool.

This flow takes the available changesets in `checkpoint` and brings `release` up to date.  It assumes that `checkpoint` and `release` already exist and have been set up correctly. The `trunk` is the authoritative source for everything that goes in a release; only under exceptional circumstances are changes made to other branches.  The general rule is that a change is made to `trunk`, brought over to `checkpoint` and then merged into `release`. This flow assumes that any needed changesets are already in `checkpoint`; if not, you will need to commit a suitable changeset to `trunk` following your usual development practices, then [cherry-pick the changes](ReleaseHOWTO/TipCherryPick) into `checkpoint` before starting this flow. If you want a checklist you can mark off as you go, cut-n-paste these contents.

**Table of Contents**

[TOC]

!INCLUDE "InitHG.md"

```
$ VERSION=3.2.0.final.0
```
### Check Out Release

!INCLUDE "CheckOutRelease.md" 


### Update Release Values

Verify that `release_level` in [ReleaseConfig](ReleaseConfig) is being set to `final`.

!INCLUDE "UpdateFiles.md"

### Commit Release

Look at the log messages in `commit.txt` and create `log.file` that hits the highlights of the changes that have been incorporated.  Much of the information should already be in `src/Announce.txt`, so it mostly involves copy-n-past from there.  Cut it heavily to one or two lines per feature; the major use of this log is people who are scanning to see where a feature was added, and they will appreciate clarity and brevity.  This is an example of what `log.file` might be like:

```
Rebased the release branch to r54321 of the checkpoint branch.
  -- The blah was updated to do foo
  -- Feature bar was added by John Doe
  -- Various typos
```

Commit the changes using the log message: 

!INCLUDE "Commit.md"

### Build Candidate Packages
!INCLUDE "Bootstrap.md"

### Test the Candidate Packages
This script is kept in the distribution as bin/xxxxxxxxx:
```
$ set -e
$ python runtest.py -a
```
Make a copy of it and edit it based on the description below.

### Regression Test

The first line of the script runs the regression test.  The SCons BuildBot monitors this branch and probably started running regression tests as soon as you checked in the branch.  If so, delete the first line of the script as the Build``Bot is more comprehensive that running the test on a single machine.  You will need to keep an eye on the [BuildBot display](http://buildbot.scons.org/console?branch=release) until all the slaves have finished.

### Package Tests

!INCLUDE "TestCandidates.md"

If any of the tests fail, fix the problem in `trunk` following your usual development practices, [cherry-pick the changes](ReleaseHOWTO/TipCherryPick) into the `checkpoint` branch, and go back to [merge the changeset(s)](ReleaseHOWTO/TipFinalBody) into the `release` branch.

### Tag the Release
!INCLUDE "TagRelease.md"

### Archive Candidate Packages
!INCLUDE "ArchivePackages.md"

 ### Update SourceForge
!INCLUDE "UpdateSourceForge.md" 

### Update scons.org
!INCLUDE "UpdateSConsOrg.md" 

### Update Tigris.org
!INCLUDE "UpdateTigris.md" 

### Announce
!INCLUDE "AnnounceAll.md" 

### Update Trunk to Next Version

**Initialize files for next version** 

!INCLUDE "CheckOutTrunk.md" 

From within the `trunk` directory, edit `ReleaseConfig` and change the assignment of `release_level` to `'post'`. 

!INCLUDE "UpdateFiles.md" 

A release level of `'post'` causes `update-release-info.py` to update `ReleaseConfig` itself to the next minor version and then tweak some other files to set them up for the the beginning of a new version.

**Verify files are correct** Edit files ... [FIXME](ReleaseHOWTO/TipFinalBody)

**Commit changes for next version** Create `log.file` ... [FIXME](ReleaseHOWTO/TipFinalBody) 

!INCLUDE "Commit.md"

**Finalize** Go celebrate; you're all done. 

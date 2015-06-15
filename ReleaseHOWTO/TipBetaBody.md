

<div>
These instructions use outdated workflow based on svnmerge tool. 
</div>
This flow takes the available changesets in `trunk` and brings `checkpoint` up to date.  It assumes that `trunk` and `checkpoint` already exist and have been set up correctly. 

The `trunk` is the authoritative source for everything that goes in a release; only under exceptional circumstances are changes made to other branches.  The general rule is that a change is made to `trunk` and brought over to `checkpoint`. 

This flow assumes that any needed changesets are already in `trunk`; if not, you will need to commit a suitable changeset following your usual development practices. 

If you want a checklist you can mark off as you go, cut-n-paste these contents. 

[[!toc 3]] 

[[!inline pages="../InitHG" quick="yes" raw="yes"]] 
```txt
  $ export RELEASE=3.2.0.beta.yyyymmdd
```

### Send Starting Message

[FIXME](ReleaseHOWTO/TipBetaBody) Send blurb out to release mailing list 


### Check Out Trunk

[[!inline pages="../CheckOutTrunk" quick="yes" raw="yes"]] 


### Check Out Checkpoint

[[!inline pages="../CheckOutCheckpoint" quick="yes" raw="yes"]] 


### Determine Available Changesets

[FIXME](ReleaseHOWTO/TipBetaBody) Use `svnmerge avail --log` instead of dry run. Use `svnmerge` to find out what changesets are available to be merged: 


```txt
  $ cd checkpoint
  $ svnmerge avail --log >../trunk/log.file
  $ cd ../trunk
```

### Edit Configuration Files

The `commit.txt` file created in the previous step has the commit comments for all the applied changesets.  In theory, all of them have been included in the `trunk` files `src/CHANGES.txt`, `stc/RELEASE.txt`, and `src/Announce.txt`, but in practice, some of the information has not been included, so you will have to add it.  At the same time, you want to prepare a `log.file` that will be used as the commit comments. 

**The `log.file` and `src/CHANGES.txt` files** 

Both `log.file` and `src/CHANGES.txt` use similar formats.  Assuming `commit.txt` has three log entries, three from John Doe on two issues and two by Jim Smith on a single issue, `log.file` would look like this: 
```txt
Rebased to trunk revision 54321:

From John Doe:
 - One item that was done by John Doe.
 - Another item that was done by John Doe.

From Jim Smith:
 - Item done by Jim Smith.
```
In theory, the first section of `src/CHANGES.TXT` should already have the corresponding information.  If it does, steal it for `log.file`.  If it doesn't, add it to `src/CHANGES.txt`.  In the end, the items in `src/CHANGES.txt` for John Doe and Jim Smith should have this information: 
```txt
  From John Doe:

    - One item that was done by John Doe with details and examples.

    - Another item that was done by John Doe with details and examples.

  From Jim Smith:

    - Item done by Jim Smith with details and examples.
```
**Verify the `src/RELEASE.txt` file** 

In theory, the entries in `src/RELEASE.txt` should already summarize `src/CHANGES.txt` except that issues are summarized by topic and the names of contributors are collected in a section at the bottom.  In practice, not all of the entries have been transcribed. 


Since this is an announcement, try to edit down the `src/CHANGES.txt` descriptions so that, ideally, each item fits on a single line.  In general, get rid of examples and explanations.  The idea is to pique the reader's interest, not provide full documentation.  Still, use your judgment and feel free to leave in an explanation if it would be too confusing to shorten it. 

Try to reorganize the items so that, within each section, all of the Visual Studio items are listed together, all of the Java items are together, _etc_.  More "important" (or visible) items should appear towards the top of each section. 

It's all right just to delete the description of something that's too difficult to explain and too minor to make much of a difference. 

Whether or not a given item belongs in "`NEW FUNCTIONALITY`" _vs._ "`CHANGED/ENHANCED`" _vs._ "`FIXED`" _vs._ "`IMPROVEMENT`" is a judgment call. 

In the final "Thanks to" paragraph, at a minimum list everyone in the `src/CHANGES.txt` file who contributed to the release, plus anyone else who (in your judgment) merits a mention even if they didn't contribute an actual patch. 

**The `src/Announce.txt` file** 

The `src/Announce.txt` file is the announcement used for production releases.  In theory, it summarizes `src/CHANGES.txt`, but like `src/CHANGES.txt`, entries may not have been transcribed.   Rather than trying to do the summarization all at once in a candidate release, it's better to do it incrementally while the changes to `src/CHANGES.txt` and `src/RELEASE.txt` are fresh in your mind. 

Under the topic "scheduled for next release" add anything that's expected to be a significant change.  To get a feel for what's in play, consult the tracker for issues scheduled for the next next release.  The quickest way of getting that list is to go to the `BugParty` wiki page and click on the "how we're doing" link.  On that report, click on the summary link at the bottom of the column for the next release.  Use the future tense for these items. 

Under the next topic, add any major items that aren't already included.  Use your judgment as to what to add, but if it's not something the user needs to know, don't include it, so things like performance improvements, code cleanup, typos, and minor enhancements don't make the cut. 

[FIXME](ReleaseHOWTO/TipBetaBody) expand this section 


### Confirm Users' Guide is OK

[[!inline pages="../UpdateGuide" quick="yes" raw="yes"]] 


### Commit Trunk

This step is needed only if any `trunk` files were modified.  If nothing was changed, skip to the next step step. 

From within the `trunk` directory: 

Verify that `version_tuple` in `ReleaseConfig` has the correct release number and a release level of `'alpha'`. 

[[!inline pages="../Commit" quick="yes" raw="yes"]] 


### Merge Trunk into Checkpoint

To merge the changes from the trunk into the `checkpoint` branch, run this command from within the `checkpoint` directory: 


```txt
  $ svnmerge merge -b -S $SVN/trunk -f commit.txt
```

### Resolve Conflicts

[[!inline pages="../Resolved" quick="yes" raw="yes"]] 


### Update Release Files

Verify that the `version_tuple` in `ReleaseConfig` says `'beta'` or `'candidate'` as desired. 

From within the `checkpoint` directory: 

[[!inline pages="../UpdateFiles" quick="yes" raw="yes"]] 


### Commit Checkpoint

[FIXME](ReleaseHOWTO/TipBetaBody) 


```txt
  $ svn commit -m"Update checkpoint branch for $VERSION; see CHANGES.txt for details."
```

[[!inline pages="../BuildAndTest" quick="yes" raw="yes"]] [[!inline pages="../Prepare" quick="yes" raw="yes"]] 


### Tag the Release

From within the `checkpoint` directory: 


```txt
  $ svn cp . $SVN/tags/$VERSION
```

### Archive Candidate Packages

[[!inline pages="../ArchivePackates" quick="yes" raw="yes"]] 


### Update SourceForge

[[!inline pages="../UpdateSourceForge" quick="yes" raw="yes"]] 


### Update scons.org

[[!inline pages="../UpdateSConsOrg" quick="yes" raw="yes"]] 


### Update Tigris.org

[[!inline pages="../UpdateTigris" quick="yes" raw="yes"]] 


### Announce

[[!inline pages="../AnnounceCheckpoint" quick="yes" raw="yes"]] 

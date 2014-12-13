

<div>
These instructions use outdated workflow based on svnmerge tool. 
</div>
Cherry-picking is the act of applying only selected changesets to a current branch, rather than taking all possible changesets to bring the branch up-to-date. 

In our case, `trunk` is the authoritative source for everything that goes in a release; only under exceptional circumstances are changes made to `checkpoint` or `trunk`.  The general rule is that a change is made to `trunk` and brought over to `checkpoint`. 

This flow assumes that the needed changesets are already in `trunk`; if not, you will need to commit a suitable changeset to `trunk` following your usual development practices prior to using this flow. 

[[!toc 3]] 

[[!inline pages="../InitSVN" quick="yes" raw="yes"]] 
```txt
  $ VERSION=3.2.0.beta.yyyymmdd
```

### Check Out Checkpoint

[[!inline pages="../CheckOutCheckpoint" quick="yes" raw="yes"]] 


### Determine Revision(s)

You can review the changes available on `trunk` to be integrated into `checkpoint`: 


```txt
  $ svnmerge.py avail --log -S $SVN/trunk
```
You can look at the diff that was applied by this revision: 


```txt
  $ svnmerge.py avail --diff -S $SVN/trunk -r54321
```
Use this information to determine the revision(s) to be applied. 


### Merge Revision(s) from Trunk

After selecting the revision(s), merge them into the `checkpoint` branch. 

From within the `checkpoint` directory: 


```txt
  $ svnmerge.py merge -r54321,54123,53412 -b -S $SVN/trunk -f commit.txt
```

### Resolve Conflicts

[[!inline pages="../Resolved" quick="yes" raw="yes"]] 


### Update Release Values

Verify that `release_tuple` in `ReleaseConfig` has the correct release and says 'beta' or 'candidate' as appropriate, then run the `update-release-info` command: 

[[!inline pages="../UpdateFiles" quick="yes" raw="yes"]] 


### Commit Modified Checkpoint

Prepare a `log.file` that describes the revisions you pulled over.  You can use the `commit.txt` returned by the merge step to help prepare the log file.  Don't just reuse `commit.txt` as it tends to be very verbose and hard to read. 

Here's an example of a reasonable `log.file`: 
```txt
Cherry-picked revisions from trunk because blah blah blah.

From John Doe:
 - One item that was done by John Doe.
 - Another item that was done by John Doe.

From Jim Smith:
 - Item done by Jim Smith.
```
Use your judgment.  If all the revision(s) from John Doe were documentation, and Jim Smith fixed an important bug (and was the actual reason for the cherry-picking), the log message might be like this: 


```txt
Jim Smith fixed the yadda yadda by blah blah, and the issue was
deemed important enough to be brought over into the checkpoint
branch on a expedited schedule toward a micro release.

Also picked up documentation updates from John Doe as they have
no possibility of destabilizing the release.
```
Then commit the result to SVN: 

[[!inline pages="../Commit" quick="yes" raw="yes"]] 

[[!inline pages="../BuildAndTest" quick="yes" raw="yes"]] 




### Determine What and Where to Announce

The sequel describes all the steps for a full-fledged beta or candidate release.  This could be overkill.  For example, if the change is small and has no impact on the way SCons operates (such as a fix to a regression test so that a production release may proceed), there's no reason to publish the checkpoint at all, as publishing the final release will be sufficient. 

There's usually a reason for the choice of changesets to be cherry-picked, and it's important to someone.  At a minimum, those interested parties should be notified.  Other forms of publishing are optional, so use your judgment as to which, if any, of the following steps should be done. 

[[!inline pages="../Prepare" quick="yes" raw="yes"]] 


### Confirm Tests Succeeded

If the [BuildBot display](http://buildbot.scons.org/console?branch=checkpoint) and the test run(s) are OK, then proceed below to publishing the release.  If not, fix the problem in `trunk` following your usual development practices and go back and start again. 


### Tag the Checkpoint

[[!inline pages="../TagRelease" quick="yes" raw="yes"]] 


### Archive Candidate Packages

[[!inline pages="../ArchivePackages" quick="yes" raw="yes"]] 


### Update SourceForge

[[!inline pages="../UpdateSourceForge" quick="yes" raw="yes"]] 


### Update Scons.Org

[[!inline pages="../UpdateSconsOrg" quick="yes" raw="yes"]] 


### Update Tigris.Org

[[!inline pages="../UpdateTigrisOrg" quick="yes" raw="yes"]] 


### Announce

[[!inline pages="../AnnounceCheckpoint" quick="yes" raw="yes"]] 


A final release is prepared and published when FIXME 

If you want a checklist you can mark off as you go, cut-n-paste these contents. 

[[!toc ]] 

[[!inline pages="../InitSVN" quick="yes" raw="yes"]] 
```txt
  $ VERSION=3.2.1.final.0
```

### Check Out Branch

[[!inline pages="../CheckOutNonTip" quick="yes" raw="yes"]] 


### Edit Configuration Files

FIXME 


### Update Release Values

Verify that the `release_level` variable in `ReleaseConfig` is being set to `'final'`. [[!inline pages="../UpdateFiles" quick="yes" raw="yes"]] 


### Confirm Users' Guide is OK

[[!inline pages="../UpdateGuide" quick="yes" raw="yes"]] 


### Commit Branch

Create `log.file` ... FIXME 

[[!inline pages="../Commit" quick="yes" raw="yes"]] 


### Run Regression Tests

The SCons Build``Bot will usually be monitoring this branch, so all you have to do is wait until the [BuildBot display](http://buildbot.scons.org/console) for the commit from the previous step shows that all the regression tests have been run.  On the other hand, if you're feeling bored, you can run the regression tests while you're waiting... ;-) 

[[!inline pages="../RegressionTests" quick="yes" raw="yes"]] 

If the regression tests fail, fix the problem in the branch following your usual development practices and start the flow again. 


### Build Candidate Packages

[[!inline pages="../Bootstrap" quick="yes" raw="yes"]] 


### Test Candidate Packages

[[!inline pages="../TestCandidates" quick="yes" raw="yes"]] 

If any of the candidate packages fail, fix the problem in the branch following your usual development practices and start the flow again. 


### Tag the Release

[[!inline pages="../TagRelease" quick="yes" raw="yes"]] 


### Archive Candidate Packages

[[!inline pages="../ArchivePackages" quick="yes" raw="yes"]] 


### Update SourceForge

[[!inline pages="../UpdateSourceForge" quick="yes" raw="yes"]] 


### Update scons.org

[[!inline pages="../UpdateSConsOrg" quick="yes" raw="yes"]] 


### Update Tigris.org

[[!inline pages="../UpdateTigris" quick="yes" raw="yes"]] 


### Announce

[[!inline pages="../AnnounceAll" quick="yes" raw="yes"]] 

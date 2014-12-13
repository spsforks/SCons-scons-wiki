
An alpha release is a quick-n-dirty way of getting out initial releases for testing.  It can be done at any point, even from a read-only tree, as there's no requirement for committing the branch when the process is completed. 

If you want a checklist you can mark off as you go, cut-n-paste these contents. 

[[!toc ]] 

[[!inline pages="../InitSVN" quick="yes" raw="yes"]] 
```txt
  $ VERSION=3.2.1.alpha.yyyymmdd
```

### Check Out Branch

[[!inline pages="../CheckOutNonTip" quick="yes" raw="yes"]] 


### Update Release Values

Verify that the `release_level` variable in `ReleaseConfig` is being set to `'alpha'`. [[!inline pages="../UpdateFiles" quick="yes" raw="yes"]] 


### Run Regression Tests (Optional)

Since an alpha package is intended to be transient, only useful for a short time, running the regression tests may not be necessary. 

[[!inline pages="../RegressionTests" quick="yes" raw="yes"]] 


### Build Candidate Packages

[[!inline pages="../Bootstrap" quick="yes" raw="yes"]] 


### Test Candidate Packages (Optional)

Since an alpha package is intended to be transient, only useful for a short time, testing the packages may not be necessary. [[!inline pages="../TestCandidates" quick="yes" raw="yes"]] 


### Make Available

TO BE ADDED LATER; if you have some good words for this topic, please edit [ReleaseHOWTO/NonTipAlphaBody](ReleaseHOWTO/NonTipAlphaBody) and put them in. 

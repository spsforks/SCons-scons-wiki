
An alpha release is published from the `trunk`.  It can be done at any point, even from a read-only tree, as there's no requirement for committing `trunk` when the process is completed. 

An alpha release has a very short lifetime; in general, it exists long enough to do some testing and then it is thrown away.  These steps are suggestive, not prescriptive; individual cases may choose among the steps (and even add new ones) to perform their tasks. 

For example, the standard Build``Bot run skips the steps after the regression tests, while the packaging run skips the regression tests and instead does the tests of the candidate packages.  In both cases, the alpha release is immediately discarded. 

Another example might be automatically publishing the packages every day; to keep the run-time reasonable, the testing steps would be skipped. 

[[!toc ]] 

BLAH BLAH BLAH [[!inline pages="../InitSVN" quick="yes" raw="yes"]] 

BLAH BLAH BLAH 
```txt
  $ VERSION=3.2.0-alpha.yyyymmdd
```

### Check Out Trunk

[[!inline pages="../CheckOutTrunk" quick="yes" raw="yes"]] 


### Update Release Values

From within the `trunk` directory: [[!inline pages="../UpdateFiles" quick="yes" raw="yes"]] 


### Run Regression Tests (Optional)

Since an alpha package is intended to be transient, only useful for a short time, running the regression tests may not be necessary. 

[[!inline pages="../RegressionTests" quick="yes" raw="yes"]] 


### Build Candidate Packages

[[!inline pages="../Bootstrap" quick="yes" raw="yes"]] 


### Test Candidate Packages (Optional)

Since an alpha package is intended to be transient, only useful for a short time, testing the packages may not be necessary. [[!inline pages="../TestCandidates" quick="yes" raw="yes"]] 


### Make Available

TO BE ADDED LATER; if you have some good words for this topic, please [FIXME](ReleaseHOWTO/TipAlphaBody) and put them in. 

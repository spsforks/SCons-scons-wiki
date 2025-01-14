### OBSOLETE

### Build Candidate Packages

Provided you have all of the necessary utilities installed, this should be a simple matter of: 


```txt
  $ rm -rf build bootstrap
  $ python bootstrap.py VERSION=$VERSION
```
While you're waiting for the candidate packages to be built, open another shell window and proceed with preparing the test script.  Make sure that $SVN and $VERSION are set up as shell variables as described above. 


### Test

**Prepare test script** 

The script to run the tests is in the source in `bin/fill_me_in`.  Make a copy and edit it according to the instructions below. 


```txt
  # report skipped tests as successful
  export TESTCOMMON_PASS_SKIPS=yes
  set -e       # stop on error
  #
  python runtest.py -a
  python runtest.py -a -p tar-gz
  python runtest.py -a -p zip
  python runtest.py -a -p local-tar-gz
  python runtest.py -a -p local-zip
  python runtest.py -a -p src-tar-gz
  python runtest.py -a -p src-zip
  python runtest.py -a -p rpm
```
The regression suite exercises a wide range of functionality.  There are around a thousand tests in the suite, so each test run can take a while. 

**Regression tests of source tree** 

Normally, the SCons Build``Bot monitors this branch, so it probably started running regression tests as soon as you checked in the changes above.  If your machine is covered by one of the Build``Bot machines (particularly if your machine ``<ins>is</ins>`` one of the Build``Bot machines), you can remove the first `runtest` in the script. 

**Regression tests of candidate packages** 

The build step above not only builds the packages but also _unpacks_ all of them into subdirectories so that you can run the test suite against the packaged goods.  This is intended to catch packaging problems such as not adding a new module to the packaging `MANIFEST` list(s). The `runtest.py` script supports a `-p` option and arguments that run the SCons tests against the different unpacked directories. 

Edit the script to include the tests you want to include.  If you want to be complete, test all of the packages. 

To be quicker but still reasonably thorough, test `tar-gz` and `zip`, one each of `local-` and `src-` (probably do `-tar-gz` for one and `-zip` for the other), and `rpm`. 

For a quick-n-dirty test, just test `tar-gz` or `zip`, and maybe `rpm`. Since all of the different packages use the same lists as input, it's pretty unlikely that the tests will pass on one package and fail for another. 

Once the script is prepared, save it and return to the window creating the packages. 


### Check the Build

The build creates the packages in the `build/dist` subdirectory. If everything built correctly, you should see files that look like the following: 
```txt
  scons-$VERSION-1.noarch.rpm
  scons-$VERSION-1.src.rpm
  scons-$VERSION.linux-x86_64.tar.gz
  scons-$VERSION.linux-x86_64.zip
  scons-$VERSION.tar.gz
  scons-$VERSION.win32.exe
  scons-$VERSION.zip
  scons-doc-$VERSION.tar.gz
  scons-local-$VERSION.tar.gz
  scons-local-$VERSION.zip
  scons-src-$VERSION.tar.gz
  scons-src-$VERSION.zip
```
Note that the `linux-x86_64` strings in some of the file names above may be different, depending on your local system architecture. That doesn't matter; those files don't go public.  Go ahead and remove them. 


### Run Test Script

[FIXME](ReleaseHOWTO/BuildAndTest) 

If the build succeeded, run the test script: 
```txt
  $ sh path/to/copy-of-script
```
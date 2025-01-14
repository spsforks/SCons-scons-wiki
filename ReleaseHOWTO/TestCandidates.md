
The build step above not only builds the packages but also _unpacks_ all of them into subdirectories so that you can run the test suite against the packaged goods.  This is intended to catch packaging problems such as not adding a new module to the packaging `MANIFEST` list(s). The `runtest.py` script supports a `-p` option and arguments that run the SCons tests against the different unpacked directories. 

Edit the script to include the tests you want to include.  If you want to be complete, test all of the packages. 

To be quicker but still reasonably thorough, test `tar-gz` and `zip`, one each of `local-` and `src-` (probably do `-tar-gz` for one and `-zip` for the other), and `rpm`. 

For a quick-n-dirty test, just test `tar-gz` or `zip`, and maybe `rpm`. Since all of the different packages use the same lists as input, it's pretty unlikely that the tests will pass on one package and fail for another. 

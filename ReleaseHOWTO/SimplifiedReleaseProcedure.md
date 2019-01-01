# Current SCons Release Procedure

The procedure has been used for all releases since 2.2.0. 

## Tag Release in Git

* Move work to a release branch. It's currently necessary to do this first as the build will use the branch name when building the REVISION string it substitutes into many of the files.


```
#!bash

   git fetch 
   git checkout -b rel_<NAME> master
```


## Prepare Binaries and Doc

* validate and update all documentation files by calling: 

```txt
   python bin/docs-update-generated.py
   python bin/docs-validate.py
   python bin/docs-create-example-outputs.py
```
* then check all diffs for the files in `docs/generated/*`.

* Commit the auto-generated doc changes to current branch ("Regenerated docs for X.Y.Z release.") 
* update CHANGES.txt (should already be up to date) 
* update Announce.txt (not for checkpoints): add section for this release, important user-visible changes only.  This is really long since it also has old releases.  Is it useful? 
* update RELEASE.txt: this gets its content *replaced* for each release.  New functionality, deprecated functionality, changed functionality, and fixes.  Get this from CHANGES.txt.  Add new contributors to list at end. 
* edit `debian/changelog`. Be careful of formatting here, it gets machine-parsed. 
* NOTE: I think Announce and Release are backwards; Release should be complete release notes for all versions (latest at top) and Announce should be a short blurb of just this release.  FIXME! 
* Commit this to the current branch (normally default branch in hg, unless this release is coming off a branch). 
* update `ReleaseConfig` and run `python bin/update-release-info.py release` (this modifies CHANGES, Release and Announce -- that's why you should commit the above first.) 
* build packages and doc: `python bootstrap.py >& build-XYZ.log` (good idea to save build logfile somewhere) 
* test them: `python runtest.py -a` (Q: aren't there special tests to test the unpacked installers?) 

```txt
You should now have the following in build/dist: 

  scons-$VERSION.tar.gz
  scons-$VERSION.zip
  scons-doc-$VERSION.tar.gz
  scons-local-$VERSION.tar.gz
  scons-local-$VERSION.zip
  scons-src-$VERSION.tar.gz
  scons-src-$VERSION.zip
```


## Upload Software and Doc

* There is now a shell script to do this: `bin/upload-release-files.sh X.Y.Z mysfusername` as long as [SourceForge](SourceForge) and scons.org have your ssh pub key and you're using SSH Agent Forwarding. 
* It uploads all the packages to SF, uploads the doc to scons.org, unpacks it, and updates the doc symlinks.
** You will be prompted for your password numerous times. 
* You may still have to tell SF that the new release dirs exist in its File Manager (it's a bit buggy). 

## Prepare Announcement and announce to all

* Use Announce.txt and/or Release.txt as blurb 
* Update scons.org
  * Update the scons-new-website repo.  

| File   | Changes  |
|---|---|
| versions.py  | update SCONS_PRODUCTION_VERSION, SCONS_PRIOR_VERSION, SCONS_API_VERSIONS  |
| content/releases/release-###.rst | add an announcement |


* Commit the above changes to git and push. 
* Update Sourceforge: 
   * set default downloads for each win/linux/mac etc. appropriately, using the "info" link on the right of each download. 
* Update Tigris: 
   * check out tigris website: `svn checkout http://scons.tigris.org/svn/scons/ scons-tigris --username USERNAME` 
   * Then edit the trunk/www/project-highlights and trunk/www/roadmap.html pages and svn commit.  That will make them live. 
   * Manually add a new Announcement: log in to the site, then upper left Announcements, then in there Add New Announcement. 
   * Add version to issue tracker: Issue Tracker, Configuration, Add/Edit, Add new version. 
* Announce to scons-users and scons-dev 
* Others? 

## After Release

* On GitHub create a pull request from the branch. GitHub will give you a URL when you push and create the branch which will take you to a page to do just this.
* On default branch, run `python bin/update-release-info.py post` to go back to develop mode. 
* Commit those changes after review 
There is more detail on some of the steps here at [http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody](http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody) although that is still based on the old svn system. 

It's OK to do the release-branch creation, commit and tag at the very end, just in case something goes wrong and packages need to be rebuilt. 

# Upload to testpypi #

```
#!bash

twine upload --repository-url https://test.pypi.org/legacy/ dist/scons-*.tar.gz
```

Test via:

```
#!bash

virtualenv venv
. venv/bin/activate
pip install --index-url https://test.pypi.org/simple/ scons==3.0.0.alpha.20170821
scons --version
```

# Upload to Pypi #

```
#!bash

twine upload --repository-url https://test.pypi.org/legacy/ dist/scons-*.tar.gz
```









TODO: 

* do we need both Announce.txt and RELEASE.txt?  Let's optimize for what we really need. 
* research above FIXMEs 
* integrate useful parts of [http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody](http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody) into this page, while keeping it short and to the point. 
* make list of dependencies needed to produce release (e.g. for ubuntu: all doc tools, man2html, rpm)
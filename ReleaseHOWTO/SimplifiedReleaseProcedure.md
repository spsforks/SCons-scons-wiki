

# Simplified Release Procedure for 2012 and later

The procedure has been used for all releases since 2.2.0. 


## Prepare Binaries and Doc

* validate and update all documentation files by calling: ```txt
python bin/docs-update-generated.py
python bin/docs-validate.py
python bin/docs-create-example-outputs.py
```, then check all diffs for the files in `docs/generated/*`. 
* Commit the auto-generated doc changes to current branch ("Regenerated docs for X.Y.Z release.") 
* update CHANGES.txt (should already be up to date) 
* update Announce.txt (not for checkpoints): add section for this release, important user-visible changes only.  This is really long since it also has old releases.  Is it useful? 
* update Release.txt: this gets its content *replaced* for each release.  New functionality, deprecated functionality, changed functionality, and fixes.  Get this from CHANGES.txt.  Add new contributors to list at end. 
* edit `debian/changelog`. Be careful of formatting here, it gets machine-parsed. 
* NOTE: I think Announce and Release are backwards; Release should be complete release notes for all versions (latest at top) and Announce should be a short blurb of just this release.  FIXME! 
* Commit this to the current branch (normally default branch in hg, unless this release is coming off a branch). 
* update `ReleaseConfig` and run `python bin/update-release-info.py release` (this modifies CHANGES, Release and Announce -- that's why you should commit the above first.) 
* build packages and doc: `python bootstrap.py >& build-XYZ.log` (good idea to save build logfile somewhere) 
* test them: `python runtest.py -a` (Q: aren't there special tests to test the unpacked installers?) 
You should now have the following in build/dist: 


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
The .linux-x86_64 ones are not needed and may be deleted; the others all get uploaded to SF. 

* You have to rename the scons-$VERSION.win32.exe to scons-$VERSION-setup.exe; the build SConstruct should be fixed to do this.  (Note that the upload script requires this.) 

## Tag Release in Mercurial

* commit the changes made by update-release-info.py onto a release branch: 

```txt
   hg branch rel_<NAME>
   hg commit (message: final auto updates for x.y.z release)
   hg tag <NAME> (e.g. 2.2.0)
```

## Upload Software and Doc

* There is now a shell script to do this: `bin/upload-release-files.sh X.Y.Z mysfusername` as long as [SourceForge](SourceForge) and scons.org have your ssh pub key and you're using SSH Agent Forwarding. 
* It uploads all the packages to SF, uploads the doc to scons.org, unpacks it, and updates the doc symlinks. 
* You may still have to tell SF that the new release dirs exist in its File Manager (it's a bit buggy). 

## Prepare Announcement and announce to all

* Use Announce.txt and/or Release.txt as blurb 
* Update scons.org.  Much of the hard work is already done by the script.  You just have to manually edit these files in public_html/production: [[!table header="no" class="mointable" data="""
`includes/versions.php`  | update `$latestrelease`, update `$docversions[]` and `$apiversions[]` list 
`index.php`  | add an announcement for the home page  
remove any out-of-date announcements 
`news-raw.xhtml`  | add an announcement to the list (duplicate it from what you just added to `index.php`) 
"""]]

* Commit the above changes to hg and push. 
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

* On default branch, copy all the changes from the release branch back to the default branch.  (XXX: then why do we have the release branch??) 
      * `hg diff -r default:X.Y.Z | patch -p1` 
* On default branch, run `python bin/update-release-info.py post` to go back to develop mode. 
* Commit those changes after review 
There is more detail on some of the steps here at [http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody](http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody) although that is still based on the old svn system. 

It's OK to do the release-branch creation, commit and tag at the very end, just in case something goes wrong and packages need to be rebuilt. 

TODO: 

* do we need both Announce.txt and RELEASE.txt?  Let's optimize for what we really need. 
* research above FIXMEs 
* integrate useful parts of [http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody](http://www.scons.org/wiki/ReleaseHOWTO/TipBetaBody) into this page, while keeping it short and to the point. 
* make list of dependencies needed to produce release (e.g. for ubuntu: all doc tools, man2html, rpm) 
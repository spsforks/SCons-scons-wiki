
# DO NOT EDIT THIS FILE DIRECTLY. See TipFinalBody.md to see organization

# Final Release

**Table of Contents**

[TOC]



### Assumed Setup

These initializations are the conventions that will be used in the rest of this flow. 

The location of the SCons Mercurial archive: 
```txt
  $ export HG=https://bitbucket.org/scons/scons
```

The version string, which should look something like this: 

```
$ export VERSION=3.2.0
```
### Check Out Release


From within your base directory, execute this command: 

```txt
  $ hg clone $HG
  $ hg checkout tip
  $ hg purge
```



### Create Branch for Release

```txt
hg branch rel_$VERSION
```


### Update Release Values

Verify that `release_level` in [ReleaseConfig](ReleaseConfig) is being set to `final`.


```txt
	$ python bin/update-release-info.py release
```


The `ReleaseConfig` file is where the "official" version number ($VERSION), the Python version floors, and other information about the release is recorded.  This command takes the information in `ReleaseConfig` and inserts it in the necessary files. 

### Commit Release

Look at the log messages in `commit.txt` and create `log.file` that hits the highlights of the changes that have been incorporated.  Much of the information should already be in `src/Announce.txt`, so it mostly involves copy-n-past from there.  Cut it heavily to one or two lines per feature; the major use of this log is people who are scanning to see where a feature was added, and they will appreciate clarity and brevity.  This is an example of what `log.file` might be like:

```
Rebased the release branch to r54321 of the checkpoint branch.
  -- The blah was updated to do foo
  -- Feature bar was added by John Doe
  -- Various typos
```

Commit the changes using the log message: 


```txt
  $ hg ci -l log.file
```


### Build Candidate Packages
Provided you have all of the necessary utilities installed, this should be a simple matter of: 


```txt
  $ rm -rf build
  $ python bootstrap.py VERSION=$VERSION
```
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


The build step above not only builds the packages but also _unpacks_ all of them into subdirectories so that you can run the test suite against the packaged goods.  This is intended to catch packaging problems such as not adding a new module to the packaging `MANIFEST` list(s). The `runtest.py` script supports a `-p` option and arguments that run the SCons tests against the different unpacked directories. 

Edit the script to include the tests you want to include.  If you want to be complete, test all of the packages. 

To be quicker but still reasonably thorough, test `tar-gz` and `zip`, one each of `local-` and `src-` (probably do `-tar-gz` for one and `-zip` for the other), and `rpm`. 

For a quick-n-dirty test, just test `tar-gz` or `zip`, and maybe `rpm`. Since all of the different packages use the same lists as input, it's pretty unlikely that the tests will pass on one package and fail for another. 

If any of the tests fail, fix the problem in `trunk` following your usual development practices, [cherry-pick the changes](ReleaseHOWTO/TipCherryPick) into the `checkpoint` branch, and go back to [merge the changeset(s)](ReleaseHOWTO/TipFinalBody) into the `release` branch.

### Tag the Release

Verify that you have VERSION in your shell environment as described in the setup section above, then run this command: 


```txt
  $ hg tag -m "Tagging $VERSION" $VERSION
  $ hg push
```

### Archive Candidate Packages

Verify that you have SVN and VERSION in your shell environment as described in the setup section above, then run the `bin/FillMeIn` script: 

```txt
  set -e   # stop on error
  rm -rf ARCHIVE
  svn co --depth=files $SVN/ARCHIVE
  mkdir ARCHIVE/scons-$VERSION
  cp build/dist/* ARCHIVE/scons-$VERSION
  svn add ARCHIVE/scons-$VERSION
  svn commit -m"Saving copy of $VERSION in archive" ARCHIVE
  rm -rf ARCHIVE
```


### Update SourceForge

**Upload packages** 

Verify that you have SVN and VERSION in your shell environment as described in the setup section above, then run the `bin/scp-sourceforge` script: 

`  $ sh bin/scp-sourceforge sf_username `  
 

**Mark packages with release notes** 

Navigate to the [SourceForge File Manager page for SCons](https://sourceforge.net/project/admin/explorer.php?group_id=30337).  If you're reading this from a printed copy rather than the wiki page and can't click on the link, follow these instructions: 

* Log in to your Source``Forge account 
* Click on `Develop` just under `Forge` in the Source``Forge banner. 
* Under `My Projects`, click on `Develop` next to the SCons project. 
* Click on `Project Admin -> File Manager` 
Open the `scons`, `scons-src`, and `scons-local` directories.  Within each one, open the `$VERSION` folder.  In the `scons/$VERSION` directory, select the `RELEASE.txt` file and mark mark it as the release notes in the popup that appears, then save. 

If this is a final release of the production branch, select `scons-$VERSION.win32.exe` and mark it as the default selection for Windows, then select `scons-$VERSION.tar.gz` and mark it as the default for all other OSes. 

In turn, select each of the files (other than the release notes file itself, which is automatically set) in all three folders (and the folders themselves) and specify that `RELEASE.txt` is to be the release note for that file.  Because of the way the page refreshes after clicking `Save`, it seems to be easier to start at the bottom and work your way up. 

[FIXME: TEST THIS:](ReleaseHOWTO/UpdateSourceForge) You can do multiple releases quickly by opening the File Manager page multiple times in a separate tabs, but if you do, make sure to wait for the page to reload completely in one tab before clicking `Save` in another.  Trying to update multiple releases at once doesn't work, presumably because the session can only handle one update at a time. 

**Hide previous releases** 

* For a checkpoint release, hide all checkpoints in the same series that are older than this checkpoint. 
* For a minor or micro release, hide all the checkpoint releases leading up to this release. 
* For a major release, hide all the checkpoint releases leading up this release AND hide all major and minor releases older than this release. 
For each release name you wish to hide, you have to do the following in `scons`, `scons-local`, and `scons-src`: 

* Click on the gear icon to the left of the package name and select `Cut` from the popup. 
* Click on the gear icon to the left of `old checkpoints` and select `Paste` from the popup. 
**Test downloading** 

Navigate to the [SCons download page](http://sourceforge.net/projects/scons/files/).  If you're reading this from a printed copy rather than the wiki page and can't click on the link, follow these instructions: 

* [FIXME](ReleaseHOWTO/UpdateSourceForge) Add instructions if can't click. 
For each of the `scons`, `scons-src`, and `scons-local` directories: 

* Open the directory. 
* Open the $VERSION folder within the directory. 
* For each package in the folder, click on the link to download it. 
* Verify that the files arrived and look reasonable. 
**Add news item** 

Navigate to the [Project News page](https://sourceforge.net/news/submit.php?group_id=30337).  If you're reading this from a printed copy rather than the wiki page and can't click on the link, follow these instructions: 

* [FIXME](ReleaseHOWTO/UpdateSourceForge) These aren't complete. 
* Go to the `Project Admin -> Feature Settings` page 
* In `Project News`, click `Submit.` 
Once you get to the Project News page: 

* Fill in the `Subject:` box with something like "Release $VERSION now available" 
* Cut-and-paste the blurb you prepared above into the `Details:` box 
* Click `Submit` 
### Update scons.org


### Update the scons.org Web Site

**Apply changes to web site** 

Commit the changes you prepared above: 

```txt
  $ svn commit -m"Changes to publish the SCons $VERSION release"
```

Now you have to go update the site: 

```txt
  $ ssh -l scons manam.pair.com
  $ cd public_html
  $ cp -al production new  # hard-link the whole tree; fast.
  $ (cd new && svn up)     # should be fast here too
  $ rm -rf previous
  $ mv production previous && mv new production
  $ exit
```

Now point your browser to the [SCons home page](http://scons.org/). If anything is amiss, fix it, commit the necessary changes, and update the site. 

**Test downloading** 

* Navigate to the [SCons download page](http://scons.org/download.php). 
* Verify that the opening paragraph makes sense. 
* In the right-hand sidebar, find the download section corresponding to $VERSION. 
* For each file in the section, click on the link to download it. 
* Verify that the files arrived and look reasonable. 
### Update Tigris.org


#### Update project pages

Send the changes you prepared above to Tigris: 

From within the `www` subdirectory of your `trunk` directory: 


  $ svn commit -m"Update project web pages for $VERSION"


Point your browser at [the roadmap page](http://scons.tigris.org/roadmap.html); if anything's amiss, fix it and commit again. 

**Add news item** 

* Log in to your `tigris.org` account 
* Click `Announcements` in the left-hand nav bar 
* Click `Add new announcement` 
* Double-check the date (it's probably already set) 
* Fill in the `Headline` box 
* Fill in the `Body` box with the HTML blurb 
* Click `Add new announcement` 
**Add release name to issue tracker** 

* Click `Issue Tracker` on the left-hand nav bar 
* Click `Configuration options` 
* Click `Add/edit components` 
* Under `scons`, to the far right of `Add ...`, click `Version` 
* At the bottom of the list, to the right of "Add a new version", click `Add` 
* Fill in the `Version:` box with the release ($VERSION) 
* Click the `Add` button 
### Announce

Prepare a blurb by starting with a copy of `src/Announce.txt`.  Edit the file and follow these guidelines: 

* If the "scheduled for the next release" section has no content, cut it. 
* Keep the first "changes since release" section (which should be since the last production release). 
* Cut all of the subsequent "changes since release" sections. 
* Leave the copyright notice at the bottom. 
In general, use your own judgment as to what to keep and what to cut. 

**Post Blurb on Fresh``Meat** 

HOW?  If you know how to do this, [UPDATE THIS INFORMATION](ReleaseHOWTO/AnnounceAll). 

**Send Blurb to Other Interested Parties** 

* Debian maintainer? 
* Fedora maintainer? 
* Ubuntu maintainer? 
* Red``Hat maintainer? 
OTHERS?  Are there other individuals we should notify?  Or other mailing lists?  If you know of any, [UPDATE THIS INFORMATION](ReleaseHOWTO/AnnounceAll). 

See [http://en.wikipedia.org/wiki/Linux_distributions](http://en.wikipedia.org/wiki/Linux_distributions) and [http://en.wikipedia.org/wiki/DistroWatch](http://en.wikipedia.org/wiki/DistroWatch) for candidates to be contacted. 


**Send blurb to SCons mailing lists** 

Send the blurb to each of these mailing lists individually with a title something like "SCons release $VERSION is now available". 

* [announce@scons.tigris.org](mailto:announce@scons.tigris.org) 
* [users@scons.tigris.org](mailto:users@scons.tigris.org) 
* [dev@scons.tigris.org](mailto:dev@scons.tigris.org) 
### Update Trunk to Next Version

**Initialize files for next version** 


From within your base directory, execute this command: 

  $ svn co $SVN/trunk


From within the `trunk` directory, edit `ReleaseConfig` and change the assignment of `release_level` to `'post'`. 


```txt
	$ python bin/update-release-info.py release
```


The `ReleaseConfig` file is where the "official" version number ($VERSION), the Python version floors, and other information about the release is recorded.  This command takes the information in `ReleaseConfig` and inserts it in the necessary files. 

A release level of `'post'` causes `update-release-info.py` to update `ReleaseConfig` itself to the next minor version and then tweak some other files to set them up for the the beginning of a new version.

**Verify files are correct** Edit files ... [FIXME](ReleaseHOWTO/TipFinalBody)

**Commit changes for next version** Create `log.file` ... [FIXME](ReleaseHOWTO/TipFinalBody) 


```txt
  $ hg ci -l log.file
```


**Finalize** Go celebrate; you're all done. 

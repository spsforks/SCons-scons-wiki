**Table of Contents**

[TOC]


# Checkpoint Release HOWTO

Step-by-step instructions for preparing and releasing a new checkpoint release of SCons--that is, release numbered with _X.Y.Z_d_YYYYMMDD_ or _X.Y.Z_r_XXXX_ format, such as 0.97.0.d20070809, 0.97.1r2334, etc. 

If you need to prepare a major release (_X.Y_, such as 0.97), see the [Major_Release_HOWTO](Major_Release_HOWTO). 

If you need to prepare a minor release (_X.Y.Z_, such as 0.97.1), see the [Minor_Release_HOWTO](Minor_Release_HOWTO). 


# Preparation


## Announcement

Summarize the changes listed in the `src/CHANGES.txt` and reorganize them into something like the following template: 


```txt
  A new SCons checkpoint release, 0.XX.0dYYYYMMDD, is now available at the
  SCons download page:

          http://www.scons.org/download.php

  A SCons "checkpoint release" is intended to provide early access to
  new features so they can be tested in the field before being released
  for adoption by other software distributions.

  Note that a checkpoint release is developed using the same test-driven
  development methdology as all SCons releases.  Existing SCons
  functionality should all work as it does in previous releases (except
  for any changes identified in the release notes) and early adopters
  should be able to use a checkpoint release safely for production work
  with existing SConscript files.  If not, it represents not only a bug
  in SCons but also a hole in the regression test suite, and we want to
  hear about it.

  New features may be more lightly tested than in past releases,
  especially as concerns their interaction with all of the other
  functionality in SCons.  We are especially interested in hearing bug
  reports about new functionality.

  We do not recommend that downstream distributions (Debian, Fedora,
  etc.) package a checkpoint release, mainly to avoid confusing the
  "public" release numbering with the long checkpoint release names.

  Here is a summary of the changes since 0.XX:

  NEW FUNCTIONALITY

  - List new features (presumably why a checkpoint is being released)

  DEPRECATED FUNCTIONALITY

  - List anything that's been deprecated since the last release

  CHANGED/ENHANCED EXISTING FUNCTIONALITY

  - List modifications to existing features, where the previous behavior
    wouldn't actually be considered a bug

  FIXES

  - List fixes of outright bugs

  IMPROVEMENTS

  - List improvements that wouldn't be visible to the user in the
    documentation:  performance improvements (describe the circumstances
    under which they would be observed), or major code cleanups

  PACKAGING

  - List changes in the way SCons is packaged and/or released

  DOCUMENTATION

  - List any significant changes to the documentation (not individual
    typo fixes, even if they're mentioned in src/CHANGES.txt to give
    the contributor credit)

  DEVELOPMENT

  - List visible changes in the way SCons is developed

  Thanks to LARRY, MOE and CURLY for their contributions to this release.

          --SK
```
Feel free to edit the opening paragraphs to draw attention to anything special or unusual about the release.  For example, if we specifically want people to test a new feature, or there is a really horrendous problem that this checkpoint fixes, an extra paragraph or two highlighting that would be appropriate. 

Since ths is an announcement, try to edit down the `src/CHANGES.txt` descriptions so that, ideally, each item fits on a single line. In general, get rid of examples and explanations.  The idea is to pique the reader's interest, not provide full documentation.  Still, use your judgment and feel free to leave in an explanation if it would be too confusing to shorten it. 

Try to reorganize the items so that, within each section, all of the Visual Studio items are listed together, all of the Java items are together, etc.  More "important" (or visible) items should appear towards the top of each section. 

It's all right just to delete the description of something that's too difficult to explain and too minor to make much of a difference. 

Whether or not a given item belongs in `NEW FUNCTIONALITY` vs. `CHANGED/ENHANCED` vs. `FIXED` vs. an `IMPROVEMENT` is a judgment call. 

In the final "Thanks to" paragraph, at a minimum list everyone in the `src/CHANGES.txt` file who contributed to the release, plus anyone else who (in your judgment) merits a mention even if they didn't contribute an actual patch. 


## Update version numbers and dates in files

The `src/CHANGES.txt` and `src/RELEASE.txt` files have lines in them that identify the release name and the date. The date stamp should be the same in the two files, and in the format printed by the POSIX `date -R` command. 

You should update these two files by hand and then commit the change: 


```txt
  $ svn diff
  Index: src/CHANGES.txt
  ===================================================================
  --- src/CHANGES.txt     (revision 2520)
  +++ src/CHANGES.txt     (working copy)
  @@ -8,7 +8,7 @@
 
 
 
  -RELEASE 0.XX - XXX
  +RELEASE 0.97.0d20071212 - Wed, 12 Dec 2007 09:29:32 -0600
 
     From John Doe:
 
  Index: src/RELEASE.txt
  ===================================================================
  --- src/RELEASE.txt     (revision 2520)
  +++ src/RELEASE.txt     (working copy)
  @@ -20,7 +20,7 @@



  -RELEASE 0.97.0d200709XX - XXX
  +RELEASE 0.97.0d20071212 - Wed, 12 Dec 2007 09:29:32 -0600

     This is the eighth beta release of SCons.  Please consult the
     CHANGES.txt file for a list of specific changes since last release.
  $ svn commit
  Sending        src/CHANGES.txt
  Sending        src/RELEASE.txt
  Transmitting file data ..
  Committed revision 2523.
  $ 
```

## Build candidate packages

Provided you have all of the necessary utilities installed, this should be a simple matter of: 


```txt
  $ export SVN=http://scons.tigris.org/svn/scons
  $ svn co $SVN/branches/core
  $ cd core
  $ python bootstrap.py CHECKPOINT=d
```
The `CHECKPOINT=d` argument above will cause today's date to be used as the checkpoint identifier. If this checkpoint release should be identified by a revision number, then use `CHECKPOINT=r` instead. 

If you need to re-generate a checkpoint release with a specific string, just supply it as the argument, _including_ the `d` or `r` prefix: `CHECKPOINT=d20070809`. 

This step will create the packages in the `build/dist` subdirectory. If everything built correctly, you should see the following: 


```txt
  scons-0.XX.0dYYYYMMDD-1.noarch.rpm
  scons-0.XX.0dYYYYMMDD-1.src.rpm
  scons-0.97.0dYYYYMMDD.linux-x86_64.tar.gz
  scons-0.97.0dYYYYMMDD.linux-x86_64.zip
  scons-0.XX.0dYYYYMMDD.tar.gz
  scons-0.XX.0dYYYYMMDD.win32.exe
  scons-0.XX.0dYYYYMMDD.zip
  scons-doc-0.97.0dYYYYMMDD.tar.gz
  scons-local-0.XX.0dYYYYMMDD.tar.gz
  scons-local-0.XX.0dYYYYMMDD.zip
  scons-src-0.XX.0dYYYYMMDD.tar.gz
  scons-src-0.XX.0dYYYYMMDD.zip
```
Note that the `linux-x86_64` strings in some of the above file names may be different, depending on your local system architecture. That doesn't matter; those files don't go public. 


## Test candidate packages

The previous build step not only builds the packages but also _unpacks_ all of them into subdirectories so that you can run the test suite against the packaged goods. This is intended to catch packaging problems such as not adding a new module to the packaging `MANIFEST` list(s). The `runtest.py` script supports a `-p` option and arguments that run the SCons tests against the different unpacked directories: 


```txt
  $ python runtest.py -a -p tar-gz
  $ python runtest.py -a -p zip
  $ python runtest.py -a -p local-tar-gz
  $ python runtest.py -a -p local-zip
  $ python runtest.py -a -p src-tar-gz
  $ python runtest.py -a -p src-zip
  $ python runtest.py -a -p rpm
```
If you want to be complete, test all of the packages. 

To be quicker but still reasonably thorough, test `tar-gz` and `zip`, one each of `local-` and `src-` (probably do `-tar-gz` for one and `-zip` for the other), and `rpm`. 

For a quick-and-dirty test, just test `tar-gz` or `zip`, and maybe `rpm`. Since all of the different packages use the same lists as input, it's pretty unlikely that the tests will pass on one package and fail for another. 


## Final User's Guide update

_(TBD -- this will probably be reworked to be part of the build step.)_ 


```txt
  python bin/scons-doc.py --diff
  python bin/scons-doc.py --update
```

```txt
  svn commit
```

# Upload the packages to SourceForge


```txt
  $ ftp upload.sourceforge.net
      .
      .
      .
  Name (upload.sourceforge.net:<your login>): anonymous
  331 Please specify the password.
  Password: <your email>
  ftp> lcd build/dist
  ftp> cd incoming
  ftp> bin
  ftp> put scons-0.XX.0dYYYYMMDD-1.noarch.rpm
  ftp> put scons-0.XX.0dYYYYMMDD-1.src.rpm
  ftp> put scons-0.XX.0dYYYYMMDD.tar.gz
  ftp> put scons-0.XX.0dYYYYMMDD.win32.exe
  ftp> put scons-0.XX.0dYYYYMMDD.zip
  ftp> put scons-local-0.XX.0dYYYYMMDD.tar.gz
  ftp> put scons-local-0.XX.0dYYYYMMDD.zip
  ftp> put scons-src-0.XX.0dYYYYMMDD.tar.gz
  ftp> put scons-src-0.XX.0dYYYYMMDD.zip
  ftp> quit
  221 Goodbye.
```
You can also `put` all of the files with less typing by doing: 


```txt
 ftp> mput *
```
And answering the interactive prompts.  If you do this, note that you should _not_ upload the `scons-0.97.0dYYYYMMDD.linux-x86_64.tar.gz`, `scons-0.97.0dYYYYMMDD.linux-x86_64.zip` and `scons-doc-0.97.0dYYYYMMDD.tar.gz` files, so answer `n` when prompted for those file names. (If you make a mistake and they get uploaded, though, it's not a big deal--Sourceforge will delete them from the directory after an extended timeout period.) 


# Create the new release at the SourceForge project page:


## First, the `scons` package

* Pull down the `Admin` menu and select `File Releases` 
* Package Name: `scons` 
* => Add Release 
* New release name:  0._XX_.0d_YYYYMMDD_ 
* Upload the `RELEASE.txt` file from `build/scons/RELEASE.txt` 
* Upload the `CHANGES.txt` file from `build/scons/CHANGES.txt` 
* **IMPORTANT!** Check the `Preserve my pre-formatted text.` box 
* Click `Submit/Refresh` 
* Scroll down and check the `scons-*` packages you uploaded 
* Click `Add Files and/or Refresh View` 
* Edit the file info (NOTE: you must click `Update/Refresh` for _each_ file; this must be done one at a time): 

File | Architecture | Extension
:--|:--|:--
`scons-0.XX.0dYYYYMMDD-.noarch.rpm` | Any | .rpm
`scons-0.XX.0dYYYYMMDD-.src.rpm` | Any | Source .rpm
`scons-0.XX.0dYYYYMMDD-.tar.gz` | Any | .gz
`scons-0.XX.0dYYYYMMDD-.win32.exe` | i386 | .exe (32-bit Windows)
`scons-0.XX.0dYYYYMMDD-.zip` | Any | .zip


* Check `I'm sure` and click `Send Notice` in the `Email Release Notice` section at the bottom. 

## Then the `scons-local` package

* Pull down the `Admin` menu and select `File Releases` 
* Package Name: `scons-local` 
* => Add Release 
* New release name:  0._XX_.0d_YYYYMMDD_ 
* Upload the `RELEASE.txt` file 
* Upload the `CHANGES.txt` file 
* **IMPORTANT!** Check the `Preserve my pre-formatted text.` box 
* Click `Submit/Refresh` 
* Scroll down and check the `scons-local-*` packages you uploaded 
* Click `Add Files and/or Refresh View` 
* Edit the file info (NOTE: you must click `Update/Refresh` for _each_ file; this must be done one at a time):


File | Architecture | Extension
:--|:--|:--
`scons-local-0.XX.0dYYYYMMDD.tar.gz` | Any | .gz
`scons-local-0.XX.0dYYYYMMDD.zip` | Any | .zip


* Check `I'm sure` and click `Send Notice` in the `Email Release Notice` section at the bottom. 

## Last, the `scons-src` package

* Pull down the `Admin` menu and select `File Releases` 
* Package Name: `scons-src` 
* => Add Release 
* New release name:  0._XX_.0d_YYYYMMDD_ 
* Upload the `RELEASE.txt` file 
* Upload the `CHANGES.txt` file 
* **IMPORTANT!** Check the `Preserve my pre-formatted text.` box 
* Click `Submit/Refresh` 
* Scroll down and check the `scons-local-*` packages you uploaded 
* Click `Add Files and/or Refresh View` 
* Edit the file info (NOTE: you must click `Update/Refresh` for _each_ file; this must be done one at a time): 

File | Architecture | Extension
:--|:--|:--
`scons-src-0.XX.0dYYYYMMDD.tar.gz` | Any | .gz
`scons-src-0.XX.0dYYYYMMDD.zip` | Any | .zip


* Check `I'm sure` and click `Send Notice` in the `Email Release Notice` section at the bottom. 

# Add the new release to the Issue Tracker at tigris.org

* Click `Issue Tracker` on the left-hand nav bar 
* Click `Configuration options` 
* Click `Add/edit components` 
* Under `scons`, to the far right of `Add ...`, click `Version` 
* At the bottom of the list, to the right of "Add a new version", click `Add` 
* Fill in the `Version:` box with 0._XX.0d_YYYYMMDD**' 
* Check `Add this version to '''all''' components.` 
* Click the `Add` button 

# Update the scons.org web site


```txt
  $ svn co $SVN/scons.org
  $ cd scons.org
```
Make the following changes to the following files: 

File | Description
:---|:---
`CHANGES.txt` | copy the new file from `build/scons/CHANGES.txt` in your packaging directory
`includes/templates.php` | update `$latestrelease` to the value `0.XX.0dYYYYMMDD`
`includes/versions.php` | update `$latestrelease` to the value `0.XX.0dYYYYMMDD`<BR>add the new version number to the `$docversions[]` and `$apiversions[]` lists<BR>**IMPORTANT:  shift the index numbers BY HAND!**
`index.php` | add an announcement for the home page<BR>remove any out-of-date announcements
`news-raw.xhtml` | add an announcement to the list (duplicate it from what you just added to `index.php`)
`RELEASE.txt` | copy the new file from `build/scons/RELEASE.txt` in your packaging directory



```txt
  $ mkdir doc/0.XX.0dYYYYMMDD
  $ (cd doc/0.XX.0dYYYYMMDD && tar zxf build/dist/scons-doc-0.XX.0dYYYYMMDD.tar.gz)
  $ svn add doc/0.XX.0dYYYYMMDD
  $ (cd doc && rm -f latest && ln -s 0.XX.0dYYYYMMDD latest)
  $ svn commit
```
Now you have to go update the site: 


```txt
  $ ssh -l scons manam.pair.com
  $ cd public_html
  $ svn co http://scons.tigris.org/svn/scons/scons.org new
  $ rm -rf previous
  $ mv production previous && mv new production)
  $ exit
```
Now point your browser to [http://www.scons.org/](http://www.scons.org/). If anything is amiss, fix it and commit the necessary changes. 


# Update the project pages at tigris.org:


```txt
  $ svn co http://scons.tigris.org/svn/scons/trunk
  $ cd trunk
```

File | Description
:--|:--
`www/project_highlights.html` | Add a short highlight announcement that will appear at the top of all of the `scons.tigris.org` pages.
`www/roadmap.html` | Update the text at the top to reflect that the latest available release is the new checkpoint release.


```txt
  $ svn commit
```
Note that in the typical case of releasing a checkpoint from a branch, you can _not_ update and commit these files from the directory in which you built the packages. These files _must_ be checked in to the `trunk` for them to show up on our `tigris.org` project pages. 


# Test downloading from the SourceForge page


# Test downloading through the web site download page


# Add a news item to the SourceForge project page

* Log in to your [SourceForge](SourceForge) account! 
* Pull down `Project` => `News` 
* Click `Submit` 
* Fill in the `Subject:` box 
* Cut-and-paste the announcement text into the `Details:` box 
* Click `Submit` 

# Add a news item to the tigris.org project page

* Log in to your `tigris.org` account! 
* Click `Announcements` 
* Click `Add new announcement` 
* Double-check the date (it's probably already set) 
* Fill in the `Headline` box 
* Fill in the `Body` box (keep it short) 
* Click `Add new announcement` 

# Announce to the scons-* mailing lists


# Do not announce to external mailing lists!

We don't do this for checkpoint releases. 


# Do not notify freshmeat.net!

We don't do this for checkpoint releases. 


[[!inline pages="../BuildAndTest" quick="yes" raw="yes"]] 

The tests can run a very long time.  While you're waiting, go back to your other shell window and prepare what you can on the assumption that the tests will succeed. 


### Download SCons Home

From within your base directory, run these commands: 


  $ svn co $SVN/scons.org
  $ cd scons.org

The `scons.org` checkout is pretty large.  If you don't want to wait, open another shell window and proceed.  Make sure the new shell is set up with the SVN and VERSION shell variables as described above. 
### Prepare Blurb

Prepare the blurb by starting with a copy of `build/scons/RELEASE.txt`.  It should be pretty much good-to-go, but look over it and see if there are any changes that should be made to make it more suitable as a blurb rather than release notes in a distribution.  In general, use your own judgment as to what to keep and what to cut. 

[FIXME](ReleaseHOWTO/PrepBetaBlurb) HTML copy of blurb by inserting <br/><br/><br/> instead of double blank lines, <br/><br/> instead of single blank lines, and <br/> in front of items in a list.  Not perfect, but more readable. 

[FIXME](ReleaseHOWTO/PrepBetaBlurb) Source of beta and final blurbs are different. 


### Prepare Tigris Announcement

Note that these files <ins>_must_</ins> be checked in to the `trunk` for them to show up on our `tigris.org` project pages; you can <ins>_not_</ins> update and commit these files from the directory in which you built the packages. 

From within the `www` subdirectory of your `trunk` directory, edit these files: 
[[!table header="no" class="mointable" data="""
`project_highlights.html`  | Add a short highlight announcement that will appear at the top of all of the `scons.tigris.org` pages.  Trim the list to remove any entries that are now obsolete.
`roadmap.html`  | Update the text at the top to reflect that this release is now the latest available release.
"""]]


### Prepare scons.org

If you opened another window to do the prep above, move back to the window downloading `scons.org`; it should be done by now.  If you didn't, change back to the `scons.org` subdirectory of your base directory. 

**Web site** 

Make the following changes to the following files: [FIXME](ReleaseHOWTO/UpdateSconsOrg) The destination names aren't `CHANGES.txt` or `RELEASE.txt` and the explanation needs to be tweaked.  And the source for `RELEASE.txt` could be either `RELEASE.txt` or `Announce.txt`. 
[[!table header="no" class="mointable" data="""
`CHANGES.txt`  |  copy the new file from `build/scons/CHANGES.txt` in your packaging directory 
`RELEASE.txt`  |  copy the new file from `build/scons/RELEASE.txt` in your packaging directory 
`includes/versions.php`  |  update `$latestrelease` to the value `$VERSION` [FIXME](ReleaseHOWTO/UpdateSconsOrg)  
add the new version number to the `$docversions[]` list  
add the new version number to the `$apiversions[]` list 
`index.php`  |  add an announcement for the home page  
remove any out-of-date announcements 
`news-raw.xhtml`  |  add an announcement to the list (duplicate it from what you just added to `index.php`) 
"""]]

**Install documentation** 

To unpack the release documentation into where it can be used by the web pages, just run this script: 

[FIXME](ReleaseHOWTO/UpdateSconsOrg) When this script is checked in, it will allow arguments on the command line   
`  $ sh bin/FillMeIn [ $VERSION [ $SVN ] ]`  
 or something similar.  In the meantime, copy the script and run it. 


  mkdir doc/$VERSION
  (cd doc/$VERSION && tar zxf build/dist/scons-doc-$RELEASE.tar.gz)
  svn add doc/$VERSION
  (cd doc && rm -f latest && ln -s $VERSION latest)
  case $VERSION in *.0.final.*)
      # This is a 'final' release on the main branch
      (cd doc && rm -f production && ln -s $VERSION production)
  esac

[FIXME](ReleaseHOWTO/BuildTestPrep) If any of the candidate packages fail, fix the problem in `trunk` following your usual development practices and [go and do another dry run](ReleaseHOWTO/BuildTestPrep). 

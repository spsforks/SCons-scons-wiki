

### Update the scons.org Web Site

**Apply changes to web site** 

Commit the changes you prepared above: 

  $ svn commit -m"Changes to publish the SCons $VERSION release"

Now you have to go update the site: 


  $ ssh -l scons manam.pair.com
  $ cd public_html
  $ cp -al production new  # hard-link the whole tree; fast.
  $ (cd new && svn up)     # should be fast here too
  $ rm -rf previous
  $ mv production previous && mv new production
  $ exit

Now point your browser to the [SCons home page](http://scons.org/). If anything is amiss, fix it, commit the necessary changes, and update the site. 

**Test downloading** 

* Navigate to the [SCons download page](http://scons.org/download.php). 
* Verify that the opening paragraph makes sense. 
* In the right-hand sidebar, find the download section corresponding to $VERSION. 
* For each file in the section, click on the link to download it. 
* Verify that the files arrived and look reasonable. 
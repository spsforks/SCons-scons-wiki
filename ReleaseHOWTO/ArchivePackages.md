
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
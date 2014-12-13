

<div>
These instructions use outdated workflow based on svnmerge tool. 
</div>
This flow sets up a branch for a potential series of point releases. 

[FIXME:](ReleaseHOWTO/NonTipSetupBody) 

* steal comments and examples from [BranchAndMerge](BranchAndMerge) 
* add some setup for `ReleaseConfig` 
* Init``SVN ... 
Initialize...  
 `  $ export SVN=http://scons.tigris.org/svn/scons`  
 `  $ export POINT=3.2.x`  
 

Create point branch...  
 `  $ cd my_working_directory`  
 `  $ svn co $SVN/trunk`  
 `  $ svn cp trunk $SVN/branches/$POINT`  
 `  $ svn commit -m'Added branches/$POINT based on trunk' trunk`  
 I don't know why that last line is needed... 

Set svnmerge base...  
 `  $ svn co $SVN/branches/$POINT working`  
 `  $ (cd working && svnmerge init ../trunk)`  
 `  $ (cd trunk && svnmerge init ../working)`  
 `  $ (cd working && svn commit -m'Set svnmerge base for $POINT')`  
 `  $ (cd trunk && svn commit -m'Set svnmerge base for trunk')`  
 

You can actually do both the "`svnmerge init`" and "`svn commit`" on one branch (in one directory) and then do both on the other branch, but doing it this way makes both of them end up with the same base revision number in the svnmerge property, which is nice and symmetric. 

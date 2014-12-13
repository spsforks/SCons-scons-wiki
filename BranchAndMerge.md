

# SCons Branching and Merging

Since November 2011, SCons switched from Subversion to Mercurial.  Most development is now done on the default mercurial branch; developers commit into their own repositories and submit pull requests to [https://bitbucket.org/scons/scons](https://bitbucket.org/scons/scons).  The remainder of this page is for historical reference only. Please visit [SconsMercurialWorkflows](SconsMercurialWorkflows) instead, for an overview of the branch/merge workflows that are currently in place. 


# Old Subversion Discussion (Historical Only; delete in 2013)

Before release of Subversion 1.6.x we used [svnmerge](http://www.orcaware.com/svn/wiki/Svnmerge.py) process described below to keep track of what changes haven't been merged in each direction. Some of the concepts and steps have been swiped from [svnmerge howto](http://kenkinder.com/subversion-merge-tracking-with-svnmerge/) by Ken Kinder, with liberal help from our Gary Oberbrunner. 

Subversion 1.6 added native merge tracking that can be done now without resorting to svnmerge. Merge tracking via svn is also described below as well as in the excellent [SVN book](http://svnbook.red-bean.com/en/1.5/svn.branchmerge.basicmerging.html). 


<div>
You shouldn't mix the two methods within one branch. For SCons development we use only native merge tracking. The information about svnmerge way is just archived here for historical purpose. 
</div>

## Branches

These are the SCons development branches and their intended uses. 
trunk
: The main development branch for changes to the SCons infrastructure. This branch is the latest-and-greatest checked-in source, where SK checks in most of the stuff he's working on and which gets sent for review to the scons-dev mailing list. This is also where we check in web site changes into the www/ subdirectory for the tigris.org web site. 

checkpoint
: The branch from which we release checkpoints and release candidates. These are considered beta releases to be reviewed by the community. This branch lags patches that the mailing list discussions describe as "checked in to Subversion." This branch's parent is trunk. 

release
: The main code line from which SCons gets released. Once a release candidate in the checkpoint branch has achieved sufficient stability, it is promoted into this branch. This branch's parent is checkpoint. 

branches/*
: Branches for development that will take a longer period of time, such as a major refactoring or a GSoC project.  Branches come and go; what follows is a representative sample. branches/core
: Formerly the branch used for development.  Now only of historical interest. 

branches/sigrefactor
: Development branch for the Big Signature Refactoring that SK has been working on since the last ice age. This branch's parent is branches/core. Now completed; of historical interest. 

branches/testing
: A branch for work on the SCons testing infrastructure. This branch's parent is trunk. Not very active at the moment, because most of that work is just going in right in trunk. 

branches/tools
: The branch intended for people to check in new features to Tool modules. If you want to contribute a change here, go see the step-by-step instructions for doing so. This branch's parent is trunk. 



scons.org
: 
The source for the [SCons home page](http://scons.org) and its subdirectories.  Very large; don't check it out unless you have a lot of space. 



<a name="rebase"></a> 
## Rebasing

The process of updating a branch so that it effectively comes off the parent branch at a later point in time (that is, changing the base of the branch to a new location) is called _rebasing_.  With SVN this requires some initial setup when the branch is created. 


### How to create a branch off the trunk and initialize it for bi-directional merging


#### Using svn-1.5 or newer

This should take place between any branch and its parent to set up to `svn:mergeinfo` to handle the tracking as we go forward. 

* `$ export SVN=http://scons.tigris.org/svn/scons`  
 `$ cd my_working_directory/trunk`  
 `$ svn cp $SVN/trunk $SVN/branches/new_branch`  
 `$ cd ..`  
 `$ svn co $SVN/branches/new_branch`  
 `$ cd new_branch`  
 `$ svn merge $SVN/trunk`  
 `$ cd ../trunk`  
 `$ svn merge $SVN/branches/new_branch`  
 `$ svn commit`  
 `$ cd ../new_branch`  
 `$ svn commit`  
 
You can actually do both the "`svn merge`" and "`svn commit`" on one branch (in one directory) and then do both on the other branch, but doing it this way makes both of them end up with the same revision number in the svn:mergeinfo property, which is nice and symmetric. 

Note that you need to provide your own commit messages. 


### How to merge changes from the trunk to a development branch

This brings a branch in sync with the latest changes that have made it into the trunk for release (usually by being promoted from other branches, we typically don't do work directly on the trunk). 


#### Using svn-1.5 or newer

* `$ export SVN=http://scons.tigris.org/svn/scons`  
 `$ cd my_working_directory/new_branch`  
 `$ svn up`  
 `$ svn merge $SVN/trunk --dry-run`  
 `$ svn merge $SVN/trunk`  
 `$ svn resolved .`  
 `$ svn diff`  
 `$ python runtest.py -a`  
 `$ svn commit`  
 
The "`svn resolved .`" is there because there may be a conflict on the `svn:mergeinfo` property that's attached to the directory to track what changes have or have not already been merged from the trunk. 

Again, note that you have to provide your own commit message. This means that, by default, the commit message after a merge will not contain all log entries for the revisions that were merged. To see those entries, use `svn log -g`. Read the [SVN book](http://svnbook.red-bean.com/en/1.5/svn.branchmerge.advanced.html#svn.branchmerge.advanced.logblame) for more information. 


### How to merge changes from a development branch to the trunk

This promotes the branch changes into the trunk. Note that you should really first make sure that your branch has already merged any changes from the trunk (see previous section) before doing this, or else you're likely to overwrite any work that's already been submitted up. 


#### Using svn-1.5 or newer

* `$ export SVN=http://scons.tigris.org/svn/scons`  
 `$ cd my_working_directory/trunk`  
 `$ svn up`  
 `$ svn merge $SVN/branches/new_branch --dry-run`  
 `$ svn merge $SVN/branches/new_branch`  
 `$ svn resolved .`  
 `$ svn diff`  
 `$ python runtest.py -a`  
 `$ svn commit`  
 
The "`svn resolved .`" is there because there may be a conflict on the `svn:mergeinfo` property that's attached to the directory to track what changes have or have not already been merged from the development branch. 

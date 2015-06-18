**Table of Contents**

[TOC]


# Mercurial Workflow for SCons


## TL;DR

* Clone main repository from [https://bitbucket.org/scons/scons](https://bitbucket.org/scons/scons) 
* Commit to your clone 
* Fork scons repo from Bitbucket UI 
* Mark forked repo as non-publishing in admin interface 
* Check there are no changes in main repository with `hg inc` 
* If there are changes, `hg pull` them and `hg rebase` to put your commits on top 
* Push to your fork with `hg push URL` 
* Go to web interface of you fork and push `Create pull request` button 
(this is workflow v2, instructions below still need to be updated. --anatoly techtonik) 


## Guidelines

* If you have a patch which follows the [submission guidelines (code, doc, test)](http://www.scons.org/guidelines.php) you can submit a [pull request](https://bitbucket.org/scons/scons/pull-requests) at bitbucket. 
* You need to create a free account at Bitbucket to send a pull requests 
* Patches are reviewed and accepted by the release team. 
* For point releases and fixes, apply the patch to the oldest supported release, then merge it to default branch (if necessary) 
* Development is done on default branch; named branches are for maintenance and for some large features. 

## New to Mercurial?

A simple hg tutorial is at [http://mercurial.selenic.com/wiki/Tutorial](http://mercurial.selenic.com/wiki/Tutorial), with more detail at [http://hginit.com/](http://hginit.com/) (Joel Spolsky's longer intro to hg). The definitive guide to Mercurial is, uhh, [The Definitive Guide](http://hgbook.red-bean.com/). 


## Clone SCons repository


```txt
hg clone https://bitbucket.org/scons/scons
```
Now you should have a copy of the sources in the "`scons`" folder. 


## Fork repository on Bitbucket side for creating pull requests

Login to [BitBucket](https://bitbucket.org/), go to [https://bitbucket.org/scons/scons](https://bitbucket.org/scons/scons) and click the "fork" button (a blue arrow). Don't forget to mark repository as **non-publishing**. Non-publishing repositories allow pushing draft changesets (changesets change their status - phase - when you push them upstream and become immutable, pushing to non-publishing repository doesn't change status of commits). 


## Configure Mercurial in local clone

Once you've cloned your fork of the repo, you should add the following as `.hg/hgrc` in the base dir of your clone: 


```txt
[paths]
default = ssh://hg@bitbucket.org/scons/scons
default-push = ssh://hg@bitbucket.org/<my_user>/<my_fork_name>

[ui]
username = your name <email@gmail.com>
```
For this to work correctly, ensure that you added your public SSH key to your [BitBucket](https://bitbucket.org) account as described at [https://bitbucket.org/help/UsingSSH/](https://bitbucket.org/help/UsingSSH/) (look out for the section _Basic setup with a single default identity_). 

Then you can pull updates from the "original" `scons` repository via: 
```txt
hg pull
```
And push to your fork as: 
```txt
hg push
```

## Making changes

With Mercurial we always work with default branch (obviously named "default"). Named branches are not used for bug fixes and even for small feature branches. Make your changes (including doc and tests); when you're happy, commit them, and push: 


```txt
# do some work, and then add/remove files automatically with
hg addremove
# or add files individually with
hg add <single file>

# after adding all new files, commit your changes
hg commit -m "useful comment on checkin purpose"
# push your local commits up to your fork repo
hg push
```
You can inspect your changes with two commands: 
```txt
# show latest 5 changelog entries
hg log --graph -l 5
# show diff of current changes
hg diff
```
Then go to "`bitbucket.org/<my_user>/<my_fork_name>`" and click "Pull request", select the "from" branch "`default`" (or your branch if you created one). Select the "`default`" branch as the "to" branch. Please type reasonably informative subject and description and "submit" the pull. 


## Rebasing changes

Rebasing is needed to place your commits on top of fresh changes from main repository. 
```txt
# first make sure there is new stuff in repository
hg incoming
# if there is, pull it - this doesn't move your code to pulled revision
hg pull
# see the graph of repository history to make sure you're on your latest
# change - revision marked with @
hg log --graph
# rebase and look at graph once more
hg rebase
```

## Working on several "branches" at once

If you need to organize your commits better, because you're actually working on several bugs at the same time, you can use the "`bookmark`" feature of Mercurial. This is pretty close to a "branch" in `git`. Before you start with new bugs, you'll want to mark the current tip revision of "default" as common ancestor, with something like: 


```txt
hg bookmark -f origin
```
. Now you can add bookmarks for your bug or feature "branches" in the same place: 


```txt
hg bookmark bug234
hg bookmark bug987
```
By updating to a bookmark 


```txt
hg update -r bug987
```
you're "switching branches", and all following commits will go onto that current branch. Plus, you can update to your "origin" mark and add a new bookmark at any time. 

You only have to be careful later, when creating a pull request. If you have pushed multiple bookmarks, you'll have several heads on the "default" branch to choose from. Be sure to pick the right commit for your pull request, by checking its revision number. 


## Updating a pull request

After you submitted your pull request, it gets reviewed by other developers. Chances are high that you receive comments or questions about your changes (see also [the Developer Guide intro](DeveloperGuide/Introduction)). In some cases you'll get asked to add or correct things, so you have to update your request. 

For this, update your local "`scons`" copy to the corresponding bookmark, if required. 


```txt
hg update -r <bookmark_name>
```
For the "default" branch, make sure that you're pointing to the last commit of your pull request. Then continue development by adding/changing files and committing them. Finally, push them up to your personal "`scons`" fork with 


```txt
hg push -f
```
Now, go to the original "`scons`" repo page at bitbucket ( [https://bitbucket.org/scons/scons](https://bitbucket.org/scons/scons) ), and make sure that you're logged in. Go to your pull request, and then click "Edit" (right). Bitbucket should pick up your latest changes, and offer you to include their commits into the pull request. 


## Feature branches

Feature branches (named branches) are not usually needed, except for long-term development. If you really think you need one, please contact the developer team via one of the mailing lists first (`scons-users` or `scons-dev@scons.org`), and ask for permission. The rest of the workflow is similar to the descriptions above. 

Once the pull request has been accepted, only if you were working on a feature branch, do the following to mark that branch done.  (Not needed if working on the "default" branch.) 


```txt
hg branches
hg up -C <reasonable_name_for_work_being_done>
hg commit --close-branch -m "Done with this branch"
hg up -C default
hg push
```

## Before working on the next bug/feature

If you have cycled through the sections above, your pull request should now be merged to the "default" branch of the mainline. Before you continue to work on the next bugfix or feature, it's a good idea to update the working copy of your personal fork with the latest commits to `bitbucket.org/scons/scons`. 

So, do a: 


```txt
hg update -C default
hg pull upstream
hg update default
```
, to ensure that your new changes and commits will be as close as possible to the mainline development. Thank you. 

For SCons maintainers' side of the mercurial workflow, see [DeveloperGuide/AcceptingPullRequests](DeveloperGuide/AcceptingPullRequests). 

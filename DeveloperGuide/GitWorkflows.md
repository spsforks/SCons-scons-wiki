# Git Workflow for SCons

## TL;DR

For those who don't want to read the entire page, here is a quick summary:

* Visit main GitHub SCons Page [https://github.com/SConsProject/scons.git](https://github.com/SConsProject/scons.git)
* Fork scons repo from GitHub UI
* `git clone <your repo URL>`
* `git remote add upstream git@github.com:SConsProject/scons.git`
* `git fetch upstream`
* `git checkout -b <your working branch> upstream/master`
* `git config branch.<your working branch>.remote origin`
   * Without the above, git push would try to push your change to the upstream repo
* Do your work 
* git push
* Go to web interface of you fork and push `Create pull request` button


## Guidelines

* If you have a patch which follows the [submission guidelines (code, doc, test)](http://www.scons.org/guidelines.html) you can submit a [pull request](https://github.com/SConsProject/scons/pulls) at GitHub.
* You need to create a free account at GitHub to send a pull requests
* Patches are reviewed and accepted by the release team.
* For point releases and fixes, apply the patch to the oldest supported release, then merge it to default branch (if necessary)
* Development is done on default branch; named branches are for maintenance and for some large features.


## Clone SCons repository


```txt
git clone git@github.com:SConsProject/scons.git
```
Now you should have a copy of the sources in the "`scons`" folder.


## Fork repository on GitHub side for creating pull requests

Login to [GitHub](https://github.com/), go to [https://github.com/SConsProject/scons](https://github.com/SConsProject/scons) and click the "fork" button (a blue arrow).


## Making changes



## Rebasing changes

Feel free to use the Rebase feature to place your commits on top of fresh changes from the main repository, as long as your changes are local only and haven't been pushed to your public repo yet. Otherwise you may confuse the Bitbucket interface, which means that Bitbucket won't be able to update your pull requests automatically anymore. For a git-centered discussion of why "rebase" should only be used in a local context, see also [the drm-next thread](http://lwn.net/Articles/328438/).

```txt
# if there is, pull it - this doesn't move your code to pulled revision
git fetch upstream
# rebase and look at graph once more
git rebase upstream/master
```

## Working on several "branches" at once

Use git branches


## Updating a pull request

After you submitted your pull request, it gets reviewed by other developers. Chances are high that you receive comments or questions about your changes (see also [the Developer Guide intro](DeveloperGuide/Introduction)). In some cases you'll get asked to add or correct things, so you have to update your request.

For this, update your local "`scons`" copy to the corresponding bookmark, if required.



## Feature branches

Feature branches (named branches) are not usually needed, except for long-term development. If you really think you need one, please contact the developer team via one of the mailing lists first (`scons-users` or `scons-dev@scons.org`), and ask for permission. The rest of the workflow is similar to the descriptions above.

Once the pull request has been accepted, only if you were working on a feature branch, do the following to mark that branch done.  (Not needed if working on the "default" branch.)


```txt

```

## Before working on the next bug/feature

If you have cycled through the sections above, your pull request should now be merged to the "master" branch of the mainline. Before you continue to work on the next bugfix or feature, it's a good idea to update the working copy of your personal fork with the latest commits to `https://github.com/SConsProject/scons`.

So, do a:


```txt
git fetch upstream
git checkout -b <new branch name> upstream/master
```
, to ensure that your new changes and commits will be as close as possible to the mainline development. Thank you.

For SCons maintainers' side of the git workflow, see [AcceptingPullRequests](AcceptingPullRequests).

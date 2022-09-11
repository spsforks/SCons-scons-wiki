# Git Workflow for SCons

## TL;DR

For those who don't want to read the entire page, here is a quick summary:

* Visit the main GitHub SCons Page [https://github.com/SCons/scons](https://github.com/SCons/scons)
* Fork the scons repo from GitHub UI - makes a repo in your own account.
* Set up the following plumbing:
```bash
  git clone <your_repo_URL>
  git remote add upstream git@github.com:SCons/scons.git
  git fetch upstream
  git checkout -b <your_working_branchname> upstream/master
  git config branch.<your_working_branchname>.remote origin
```
  Without the above, git push would try to push your change to the upstream repo
* Do your work 
* Add a blurb on your proposed change to `CHANGES.txt`.
* `git push`
* Go to the web interface of your fork and push `Create pull request` button.
* Fill in the template and submit.

## Overview for Github Beginners

To create Pull Requests ("hi, SCons maintainers, I am _Requesting_ you _Pull_ this set of changes into the official mainline"), you need to juggle a few things.  You need a git branch somewhere on github which will be associated with the branch you want to merge to.  Since most of us will not have the rights to do that in the SCons/scons repository, that will usually be a copy ("fork") in your own github account.  And you also need a copy to actually make changes to on your own computer.  So you fork the official repository, then clone your fork to your computer. You work on your own computer to make the changes and push those up to your github fork. Then you can create a PR, which is easy because github remembers your copy of SCons is associated with the official SCons repository.

## Guidelines

* If you have a patch which follows the [submission guidelines](http://www.scons.org/guidelines.html) (code, doc, test) you can submit a [Pull Request ("PR")](https://github.com/SCons/scons/pulls) on GitHub.
* A (free) GitHub account is needed.
* Patches are reviewed and accepted by the release team.
* For point releases and fixes, apply the patch to the oldest supported release, then merge it to default branch (if necessary)
* Development is done on default branch; named branches are for maintenance and for some large features.

## Clone SCons repository

```txt
git clone git@github.com:SCons/scons.git
```
Now you should have a copy of the sources in the "`scons`" folder.

**NOTE** for Windows developers: git will do the right thing in terms of preserving line endings in the git repository for your work. However, to run the SCons test suite against your local branch, which you should do to verify your changes don't break anything, you should run: 
  * `git config --global core.eol lf`. 
  * `git config --global core.autocrlf false`
  * This forces files to checkout with lf rather than the Windows standard crlf line endings and is necessary to ensure that all the tests pass.  Some will fail if their test files are checked out with crlf line endings.
  * `git config --global blame.ignoreRevsFile .git-blame-ignore-revs`
  * This allows specifying that certain commits are to be ignored for git blame purposes. (For example mass reformatting)


## Fork repository on GitHub side for creating pull requests

Login to [GitHub](https://github.com/), go to [https://github.com/SCons/scons](https://github.com/SCons/scons) and click the "fork" button (a blue arrow).


## Making changes

Create a new branch to work in.  When you push this branch to your fork on GitHub, after the first PR you have done, the interface will offer to construct a PR based on the changes present in the branch vs the main branch. This can be changed by fiddling the drop-downs of what to compare, but usually once it gets set, you leave it alone (see the section on Feature Branches).  Use git as needed to track your evolving changes - there's nothing like trying "just one more thing" and then breaking your evolving branch - and you don't remember how to get back!  Later, you can squash your commits together if you wish (the SCons workflow does not require squashing, but the option exists).  

Github will propose the commit message as the message of the PR.  You should usually change this, especially if several commits went into making up the change in which case Github proposes the first message. You want people able to grasp the totality of the change proposal when referring to, or reviewing, a PR.  The convention is that the subject line should be the completion of the sentence "When applied, this change will...", and it's expected to be short; go into more detail in the body.

## Rebasing changes

Feel free to use the Rebase feature to place your commits on top of fresh changes from the main repository, as long as your changes are local only and haven't been pushed to your public repo yet. Otherwise you may confuse the Github interface, which means that Github won't be able to update your pull requests automatically anymore. For a git-centered discussion of why "rebase" should only be used in a local context, see also [the drm-next thread](http://lwn.net/Articles/328438/).

```txt
# grab any changes from upstream - this doesn't change the branch you're working in
git fetch upstream
# rebase and look at graph once more
git rebase upstream/master
```

You also use rebase for commit squashing, if that is your preference (`git rebase --interactive baserevision`).

## Working on several branches at once

git makes branches extremely cheap and easy - they're really just pointers in your git tree.  All changes intending to become Pull Requests should be on a separate branch. To start a new branch, update your view of the master branch from upstream, then branch from that state. The following sequence is one way to start working in a fresh branch named "foo":

```
git fetch upstream
git rebase upstream/master
git checkout -b foo
```


## Updating a pull request

After you submitted your pull request, it gets reviewed by other developers. Chances are high that you receive comments or questions about your changes (see also [the Developer Guide intro](DeveloperGuide/Introduction)). In some cases you'll be asked to add or correct things, so you have to update your request.

For this, update your local "`scons`" copy to the corresponding bookmark, if required.



## Feature branches

Feature branches (named branches) are not usually needed, except for long-term development. If you really think you need one, please contact the developer team via one of the mailing lists first (`scons-users` or `scons-dev@scons.org`), and ask for permission. The rest of the workflow is similar to the descriptions above.

Once the pull request has been accepted, only if you were working on a feature branch, do the following to mark that branch done.  (Not needed if working on the "default" branch.)


```txt

```

## Before working on the next bug/feature

If you have cycled through the sections above, your pull request should now be merged to the "master" branch of the mainline. Before you continue to work on the next bugfix or feature, it's a good idea to update the working copy of your personal fork with the latest commits to `https://github.com/SCons/scons`.

So, do a:


```txt
git fetch upstream
git checkout -b <new branch name> upstream/master
```
, to ensure that your new changes and commits will be as close as possible to the mainline development. Thank you.

For SCons maintainers' side of the git workflow, see [AcceptingPullRequests](AcceptingPullRequests).

## Submitting your Pull Request

Github will offer a template to fill in when you try to submit a PR. 

Please pay attention, it's more than fits on the initial screen, so it needs to be scrolled, and some bits are supposed to be removed.  The commit message in your branch will be the initial summary, but you don't have to keep that exactly, the audience is a little different.  The commit message is backward-looking information, "what was the reason for this change".  The github PR summary is more trying to convince the maintainers why they should accept this change. That's a subtle difference, but you might want to be more verbose in the PR message in some cases. Don't forget to fill in the checklist. Depending on the change, test suite additions or changes may be required, and documentation may need to be updated. 

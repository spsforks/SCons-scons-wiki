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
* Add a blurb on your proposed change to `CHANGES.txt` and `RELEASE.txt`.
* `git push`
* Go to the web interface of your fork and push `Create pull request` button.
* Fill in the template and submit.

## Overview for Github Beginners

Changes to SCons are handled via a "fork and pull" model.
That means you make a fork of the SCons GitHub repository in your own account,
create a "topic" branch for your work, and push your changes to it.
When you are ready to share that work,
you submit a *Pull Request* from your topic branch to the main SCons branch.
A pull request (PR) is a proposal to merge changes from one branch to another.
That triggers discussion over the details of the proposal, and you may
need to iterate on your branch a few times to address review comments.
While the PR is active, it will update automatically when it
sees changes to your topic branch, so there's no further cooordination
work you have to do on it.

Following this workflow can be a little challenging if you've never
used it before, but soon becomes familiar.

The main trick is, you need two copies of the SCons repository:
one in your github account, and one on your computer.

## Guidelines

* If you have a patch which follows the [submission guidelines](http://www.scons.org/guidelines.html) (code, doc, test) you can submit a [Pull Request ("PR")](https://github.com/SCons/scons/pulls) on GitHub.
* A (free) GitHub account is needed.
* Patches are reviewed and accepted by the release team.
* For point releases and fixes, apply the patch to the oldest supported release, then merge it to default branch (if necessary)
* Development is done on default branch; named branches are for maintenance and for occasional large features.

## Fork repository on GitHub for creating pull requests

Login to [GitHub](https://github.com/), go to [https://github.com/SCons/scons](https://github.com/SCons/scons) and click the "fork" button (a blue arrow).

## Clone your SCons fork

Figure out the path to your fork.  Github will tell you this in the web interface,
via the green **Code** button. Pick either the SSH version, or, if you like using
the `gh` command-line utility, you can use that one.
The clone operation will then look like one of these two lines:

```txt
git clone git@github.com:username/scons.git
gh repo clone username/scons
```
Now you should have a copy of the repository in the `scons` folder.

>**NOTE**
for Windows developers: git will do the right thing in terms of preserving line endings in the git repository for your work. However, to run the SCons test suite against your local branch, which you should do to verify your changes don't break anything, some extra setup is suggested:
  * Force files to checkout with lf rather than the Windows standard crlf line endings - necessary to ensure that all the tests pass.  Some will fail if their test files are checked out with crlf line endings.
    * `git config --global core.eol lf`. 
    * `git config --global core.autocrlf false`
  * Specify that certain commits are to be ignored for git blame purposes. (For example mass reformatting)
    * `git config --global blame.ignoreRevsFile .git-blame-ignore-revs`


## Making changes

Create a new topic branch to work in. Make changes. Run appropriate tests. If user-visible behavior changes, add or update documentation for the feature.

You may have to write or modifiy the tests.  If fixing a bug that was not detected by the testsuite, construct a test case that shows the problem and make sure it fails, and then passes with your fix.  Issues reporting bugs are requested to include a reproducer, this might provide a useful starting point for a testcase.


## Rebasing changes

Before submitting the PR, feel free to use git's rebase feature to place your commits on top of fresh changes from the main repository, as long as your changes are local only and haven't been pushed to your public repo yet. If you instead merge from upstream, your commits will be interspersed by date order, and be kind of hard to spot (the GitHub PR interface will end up showing things sensibly, however, so it's not a *problem* to merge instead of rebase, just a visual aid).

```bash
# grab any changes from upstream - this doesn't change the branch you're working in
git fetch upstream
# rebase and look at graph once more
git rebase upstream/master
```

You also use rebase for commit squashing, if that is your preference (`git rebase --interactive baserevision`).

If you rebase after pushing your branch, whether or not it's a PR, you'll end up having to force-push because rebasing rewrites history, and you may end up confusing the GitHub interface if it is a PR already, and things might get harder for reviewers, so this is not suggested. For a git-centered discussion of why "rebase" should only be used in a local context, see [the drm-next thread](http://lwn.net/Articles/328438/).


## Working on several branches at once

git makes branches extremely cheap and easy - they're really just pointers in your git tree.  All changes intending to become Pull Requests should be on a separate branch. To start a new branch, update your view of the master branch from upstream, then branch from that state. The following sequence is one way to start working in a fresh topic branch named "foo", after working on a different branch:

```bash
git checkout master
git fetch upstream
git rebase upstream/master
git checkout -b foo
```

If it's irritating to flip between branches, always cleaning up and committing or stashing everything so you have a clean tree for switching, git provides a "worktree" feature that can be used. Tutorials on git worktrees can be found on the internet.


## Submitting your Pull Request

You submit a PR by first doing a push of your topic branch, to duplicate the local information up to your fork on GitHub. Unless you've configured git to create the linkage automatically, you'll likely get an error like:
```txt
fatal: The current branch Mybranch has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin Mybranch

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.
```

Simply follow that suggestion to complete the push and setup your local branch as a tracking branch. Any future pushes on this branch will use the tracking information and "just work".

When you do push this branch to your fork on GitHub, follow the link in the push message. 

The GitHub web interface will offer to construct a PR based on the changes present in the branch vs the master branch. This can be changed by using drop-down to select what branches to compare, but usually once set, you leave it alone (see the section on Feature Branches).  Use git as needed to track your evolving changes - there's nothing like trying "just one more thing" and then breaking your evolving branch - and you don't remember how to get back!  Later, you can squash your commits together if you wish (the SCons workflow does not require squashing, but the option exists).  

Other than the branches to involve in the PR, the rest of the screen will be an SCons-specific template to fill in. Please pay attention to the template, it's more than fits on the initial screen, so it needs to be scrolled - there's a part you're supposed to remove and some checkboxes to be sure you've followed the necessary steps.  

The main part is the PR description.  Github will propose the commit message as the initial draft. You should usually edit this, especially if several commits went into making up the change, in which case Github proposes only the first commit message. If there's only one initial commit, or you squash-rebase before submitting the PR, this issue is not present. You want readers able to grasp the totality of the change proposal when referring to, or reviewing, a PR.  The convention is that the subject line should be the completion of the sentence "When applied, this change will...", and it's expected to be short; go into more detail in the body.

As a general principle, the PR summary does not have the same exact purpose as the git commit messages: commit messages are more backward-looking, they want to be able to answer questions for people prospecting in the history (a change was made in commit 12345 that changed behavior, what was the reason and details?), which the PR body is information for reviewers.

The commit message is backward-looking information, "what was the reason for this change".  The github PR summary is more trying to convince the maintainers why they should accept this change. That's a subtle difference, but you might want to be more verbose in the PR message in some cases. Don't forget to fill in the checklist. Depending on the change, test suite additions or changes may be required, and documentation may need to be updated. 


## Updating a pull request

After you submit your pull request, it gets reviewed by other developers. Chances are high that you receive comments or questions about your changes (see also [the Developer Guide intro](DevGuide-Introduction)). In some cases you'll be asked to add or correct things, so you have to update your request.  Commit your changes, and do a `git push`. The GitHub PR mechanism will automatically update when it detects pushes to the topic branch.


## Feature branches

Feature branches (non-numbered branches in the main SCons repository, as opposed to branches unique to your own working area) are not usually needed, except for long-term shared development. If you really think you need to create one, please contact the developer team via one of the mailing lists first (`scons-users` or `scons-dev@scons.org`), and ask for permission. The rest of the workflow is similar to the descriptions above.

Once the pull request has been accepted, only if you were working on a feature branch, do the following to mark that branch done:

```txt
TODO
```

## Before working on the next bug/feature

If you have cycled through the sections above, your pull request should now be merged to the "master" branch of the mainline. Before you continue to work on the next bugfix or feature, it's a good idea to update the working copy of your personal fork with the latest commits to `https://github.com/SCons/scons`.

Follow steps like this to ensure that your new changes and commits will be as close as possible to the mainline development (the maintainer who otherwise has to massage things to bring the new PR up to date thanks you!):


```txt
git fetch upstream
git checkout -b <new branch name> upstream/master
```

## For maintainers

For SCons maintainers' side of the git workflow, see [AcceptingPullRequests](AcceptingPullRequests).

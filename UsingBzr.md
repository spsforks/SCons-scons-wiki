

# What is Bazaar ?

Bazaar, like Mercurial and Git, is a distributed version control system (DVCS). DVCSs were created because many free and open source (FOSS) projects found that centralized version control systems (CVCSs), for example Subversion, were not able to support the ways of working required for FOSS projects. In particular the issues of geographic dispersal, unrestricted access, offline but recorded working are not well supported by CVCSs but are by DVCSs. Also, as Bazaar has shown, DVCS is a generalization of CVCS: not only can Bazaar be used as a DVCS, it can be used as a CVCS! 


## What is a DVCS compared to a CVCS ?

With CVCSs, there is a single, central repository for the project, with public read access and controlled and restricted write access. So with a Subversion repository, anyone can checkout the repository, but only those people with write access can use the repository for recording changes. With DVCSs there is no requirement for a central master repository, anyone can have a branch, and all branches have equal status. 

The important concept in DVCS is that of branch, and the feature is very different to that of the same name in Subversion. A Subversion repository is a versioned filestore stored in a database to minimize replication. It is a matter of convention that the directory trunk means the area of main active development and that copies made in the directory branch are branches. Moreover, merging between branches is very poorly supported in Subversion -- yes there is svnmerge and Subversion 1.5 is supposed to integrate this, but it remains a problem. 

With a DVCSs branches and merging are the core and most important features. The use of terms is unfortunately system dependent, so the terms branch and repository mean slightly different things in Bazaar, Mercurial and Git. This is a reflection of the fact that Bazaar, Mercurial and Git handle things differently. This page will probably lean more towards the Bazaar terminology, but that seems reasonable given that it is a Bazaar-focused page. 

A branch is effectively a copy of the project, it comprises a repository and a working tree. Each branch carries with it its own history. This means that all operations other than merging branches are local operations. As a consequence: 

1. Most operations that with Subversion require network connectivity and access to the central repository are handled locally, and can be done disconnected from the network. For example, getting the log, getting annotations, committing, branching, merging from other branches. 
1. Because the branch is local, no special rights are needed: anybody can create a branch, and create commits. Everyone has their own writeable version of the project. 
So how does a project create a master copy that represents the official current state of the project? By convention and application of write controls. Most often this is done by creating a branch on a server that everyone agrees is the master and over which write access is restricted to project committers. So DVCS move the need for convention from branching and merging to determining which is the central master. 

As anyone who has used Subversion knows branching and merging is actually a very big problem. This restricts experimentation, just as much as having to have write permission to the central repository does. Since branching and merging are central to DVCSs, multiple merges work, merging the same thing several times does not destroy things, and tagging and version tracking becomes sensible -- tagging in Subversion is by convention making a copy to the directory tags, tagging in Bazaar is simply providing a label for a given revision. 

Here are some links which go much deeper: 

* some discussion from K. Packard, the main maintainer of X.org: [here](http://keithp.com/blogs/Tyrannical_SCM_selection/), as well as [here](http://keithp.com/blogs/Repository_Formats_Matter/) 
* Linus Torvalds on the advantages of Git, the DVCS he wrote for Linux development, versus Subversion for KDE (long but it makes all the 
points really clearly): [Using Git for KDE](http://lists.kde.org/?l=kde-core-devel&m=118764715705846&w=2) 


## Why using a DVCS ?

Some things which are complicated with Subversion, are much easier with Bazaar: merging, going back into the history (that is at rev 150, you realize that everything from rev 140 is rubbish, and you want to go back: this is tedious to do with Subversion, but not with Bazaar). Basically, most of the reasons we use VCS in the first place are easier with DVCS than CVCS. Considering the different types of people interested in SCons source code: 

- Casual user who wants to use the last development version instead of a release. These people only want read access to the project so any system will do. 

- Casual developers who want to solve a specific problem. Unless these people run their own Subversion repository, they have to use hacky methods to create and maintain patches. Using Bazaar branches and rebasing they have the full power of a VCS and can create patches for submission to the core development team trivially. The core concept here is the notion of a changeset. DVCSs give very good tools for managing changesets in the context of a continuously changing repository. This means you can track changes in the master branch whilst making your own local changes. Also, Bazaar enables things like uncommit if you made a mistake and wants to go back. More generally, going back in history is much easier with a DVCS than a CVCS. 

- Core developers: the ability to use branches for each new feature is extremely useful. It makes it easier to start new things, throw away code, etc... 

The ability to do things locally makes life a lot easier. Commits can be batched to suit network access and not put too much strain on continuous integration. Workflows not really possible with systems such as Subversion become easy with Bazaar. In particular, it is easy to maintain multiple versions of branches at multiple sites, and they can be synchronized trivially. Offline working: how many people work with laptops on trains and planes and want to commit to keep a sane history? 


# Using Bazaar


## Getting Bazaar

Binary distributions of Bazaar are available for all the major platforms: Windows, Mac OS X, Linux, etc. at: [http://bazaar-vcs.org/Download](http://bazaar-vcs.org/Download) 

All the distributions that support packaging provide easy access to Bazaar, you just use the package management tool to do the installation. So anyone using Ubuntu, Debian, Fedora, CentOS/RHEL, SuSE, Gentoo, [MacPorts](MacPorts), Fink, Cygwin, etc. can easily install Bazaar. 

(Bazaar is a Python system that requires version 2.4 or above, so if you don't already have Python installed you will need to do that first. Of course this is SCons so Python may well already be installed :-) The only issue is version number Bazaar definitely requires 2.4 or later.) 

Bazaar is first and foremost a command line system based on using the bzr command. There are GUI systems: Olive-GTK for anyone with GTK installed, and [TortoiseBzr](TortoiseBzr) is under active development (the project may appear to have stalled publicly over the last few months, but there are things happening internally within Canonical, so [TortoiseBzr](TortoiseBzr) is still actively being developed). Also there is an Eclipse plugin for people wanting to use Eclipse. 

It has to be said though that currently GUI tool support for Bazaar (and indeed Mercurial and Git) is not as seasoned as that for Subversion. 


## Basic usage

Russer Winder created a branch of SCons branch/core, that is kept manually as a mirror (it would be nice to get an automatic mirror, plans are afoot). This branch was created using the bzr-svn plugin. This plugin allows Bazaar to use Subversion as a way of storing Bazaar branches. The obvious side-effect is that it is very easy to take Bazaar branches of a Subversion repository, and commits can be made from Bazaar back to the Subversion repository. In effect Bazaar can be used as a Subversion client that allows arbitrary branching for experimentation, offline working, commit batching, etc. So anyone can "checkout" the Subversion repository using Bazaar (if you have the bzr-svn plugin installed): 


```txt
bzr branch svn+http://scons.tigris.org/svn/scons/branches/core
```
Using Bazaar 1.5.0 with bzr-svn 0.4.10 is probably a must here due to "issues" with earlier version. If you follow this route then the first branch will take a while -- you are having to create a complete branch, i.e. a complete history of the whole project (2314 commits as as 2008-05-24 07:23:00+01:00. Actually SCons is small, Emacs has 50,000+ commits! 

Of course the mirror branch helps here since it is already a Bazaar branch and branching a branch is easy and a lot quicker (though the first branch will be a bit slower than subsequent merges since there is a lot of material, about 50MB for SCons, to copy and integrate): 


```txt
bzr branch http://bazaar.launchpad.net/~russel/scons/core
```
This gives you your own personal branch with its own history. 

The commands for Bazaar should be familiar to anyone who has used Subversion. To get the current status 


```txt
bzr status
```
or you can shorten this to: 


```txt
bzr st
```
Will show which files are changed but not yet committed. 


```txt
bzr diff
```
Will show the differences between changed but uncommited files and the version of the last commit. This is also quick and easy in Subversion since Subversion keep a last checkout copy to support exactly this. However if you want to check changes previous to the current one then Subversion has to go back to the repository which means network access. Bazaar carries the entire history with the branch and so all compare operations are local. 

This becomes very important when looking at log and annotation information, the Bazaar commands are very similar to the Subversion commands, but with Bazaar the operation is entirely local whereas with Subversion access to the repository is required. To get the log of the last commit: 


```txt
bzr log -r last:1
```
To get annotation of setup.py: 


```txt
bzr annotate setup.py
```

## More Advanced

For a detailed explanation, the best place to look is the Bazaar documentation at [[http://bazaar-vcs.org/Documentation](http://bazaar-vcs.org/Documentation)]. In particular, the [[http://doc.bazaar-vcs.org/bzr.dev/en/user-guide/index.html](http://doc.bazaar-vcs.org/bzr.dev/en/user-guide/index.html) guide] is easy to read. 


### Checkout vs Branches

It is important to understand the core concepts and terminology of Bazaar to use it effectively: 

* The working tree: is a snapshot of the tree, that is the files tracked by Bazaar at a certain point. 
* The repository: this is where all the informations about the revisions are kept. 
* A branch: this contains the state of the project + the history (contained in a repository). This is a key difference compared to Subversion: with Subversion only the server has this information. With Bazaar (and other DVCS), you will almost always get a branch when you want go get the sources from bzr. In particular, when you make changes and commit, this will be done in your local branch (i.e. nobody else will see your changes). 
* A checkout: with Bazaar it is possible to bind one branch to another branch -- a checkout is a bound branch. Whenever a commit is made to a bound branch the commit is made locally to the repository of the branch and also to the branch that is bound to. Clearly then a checkout is a branch that behaves more like a Subversion checkout -- local actions are immediately reflected non-locally: every time you make a commit, the changes will propagate to the branch to which the local branch is bound. 
Why would you want to get all the history, or commit locally, you may ask? This is extremely useful, because it means that you can work on a new feature or a bug using a branch, and committing to your branch (no need for any rights on the SCons Subversion repository). Once you are done, you can send a patch, or better a merge directive which contain all the revision informations for review. This means that instead of managing big patches, you can work on your machine with a sensible VCS, and once you are done, send the changes for review. 

Operations like log, annotate do not need network access, which means they are really fast. You can also go back to another version really easily, since the information is already directly available. *Technically*, your branch is not less/more important than the one you got from say the project page. Of course, in most cases, you will want to have one repository which is the one from which most people get the sources; but if at some point the main repository changes, nothing prevents you from changing (if you think about one branch for the bleeding edge, one for python 3k, one for python 2.*, it really makes sense to be able to switch between different branches). 

If you are going to make many branches of the same branch, you can, no problem since every branch is self-contained. However for a 40MB repository this can get a bit irritating. So Bazaar has the idea of a shared repository which is a place where many branches that are related can be stored in a space efficient way. Using a shared repository means that branching is very quick indeed since there is no actual copying of repositories. Using a shared repository is probably a good idea if you are going to make a lot of branches for trying different things. Because branching is cheap, having a separate branch for each experiment is a common working practice. If the experiment fails the branch can be deleted. When the experiment succeeds the changeset is merged into your main branch and the experiment branch deleted. Flexibility and control far beyond that provided by Subversion! 

Bazaar also has the concept of a lightweight checkout. The checkout idea presented above which is a branch bound to another branch is often termed a heavyweight checkout. A lightweight checkout is a working tree without its own repository, the repository of the lightweight checkout is the one of the branch checked out. This is as close as you can get to a Subversion checkout: in this case, you do not have any history, and all operations need network access. However this is rarely used as a way of checking out, it is used for doing very lightweight experiments. 


### Revision

Because there is no central server, the notion of a revision is somewhat blurred with DVCSs. Internally, all DVCS use some kind of unique ID based on hash, md5, sha, etc... Bazaar keeps the concept of a simple revision number by default, but this is only a UI detail. You should not be fooled: if two different people start from the same branch at revision 60, then for each commit, the revision will increase, but those revision numbers are only meaningful for that *branch*. In particular, if those two people merge their work together, or commit their changes to the branch they were starting from, the revisions will be changed (e.g. the revision 62 of the first person may become something else once merged with another branch). 

The rationale is that revisions are easier to handle, and in most cases, you do not care about the underlying unique ID, which is a implementation detail. Of course, you can also see the real unique ID if you want to. For more details and examples, just use the command 


```txt
bzr help revisionspec
```

### Committing changes

If you have some changes you want to commit, you simply use the commit command: 


```txt
bzr commit -m "bla bla"
```
or for people still in CVS/Subversion mode: 


```txt
bzr ci -m "bla bla"
```
Now, say you made a mistake (typo in the commit message, etc...), one thing not possible traditionally with Subversion is the ability to uncommit, but this is easy in Bazaar: 


```txt
bzr uncommit
```
This will remove the last commit (only change the repository, that is it won't revert your files). SO now you can correct whatever the problem was and commit. 

The adage appears to be "commit often", and it is easier with Bazaar than with Subversion because of the distributed and hence local nature. 


### Being synchronized with another branch

If you want to get the latest changes from another branch, there are a number of possibilities depending on the situation and goal. 

If your local branch is intended to be just an exact copy of the remote one (that is you just want to follow development you do not do any hacking yourself on this branch), you can use pull: 


```txt
bzr pull REMOTE_BRANCH
```
This will get all the changes from REMOTE_BRANCH. It will not work if you have changes in your local branch which are not in the remote branch -- the two branches have diverged so a simple pull is not possible. If you want to track the remote branch changes in diverged branches, then you use the merge command: 


```txt
bzr merge REMOTE_BRANCH
```
This will merge in all non-conflicting changes and create an interaction for handling all conflicting changes. For more detailed explanation, see this email from one of the Bazaar core developer: [[https://lists.ubuntu.com/archives/bazaar/2007q1/023972.html](https://lists.ubuntu.com/archives/bazaar/2007q1/023972.html) understanding pull vs merge]. 


### But merge is tedious to use ?

If you are coming from Subversion (or CVS), you may be a bit scared by the merge command; merging is so difficult to do in Subversion and CVS, so people tend to avoid it as much as possible. Because DVCS do not have centralized server and branching and merging are central to the whole way of working, people tend to merge each others branches often: this means merge is easy and works well. 

Because a picture is worth 1000 words (reputedly), here is a screenshot of part of the history of one branch of numscons -- a project by David Cournapeau: 

[[/UsingBzr/Screenshot.png]]

Each color in the drawing of the branch history corresponds to another branch. As you can see, merging branches is a regular occurrence. The idea is that there are several local branches, each for one special feature being working on. Since numscons is using another project internally, SCons, David has a branch which keeps track of SCons changes; a branch which is the mainline, a branch for the current version he is working on (0.2 in this case), etc... Also, since he work at different places, he sometimes just copies branches on a USB disk to transfer a branch from one computer to the other. This should convince you that merge is a much more robust feature with Bazaar than it is generally with Subversion. 


### Shared repositories

One design feature specific to bzr is that one branch is one directory, that is you cannot have several branches in the same directories (contrary to git and mercurial). In that sense, it is a bit more similar to subversion model, and is simpler to grasp. Since every branch has all its history, one obvious drawback is that M branches from the same origianl branch takes M times the disk space of the original branch. The solution is to use shared repository: branches shared their common history. 

To create a shared repository, SCONSBZRREP: 


```txt
bar init-repo SCONSBZRREP --rich-root-pack
```
Then, go inside the SCONSBZRREP, and branch from there: 


```txt
cd BZRREP && bzr branch http://bazaar.launchpad.net/~russel/scons/core
```
Of course, if you have already downloaded the branch from launchpad, you can just branch from its original location (using cp will NOT work). Then, just branch as usual 


```txt
bzr branch core mybranch
```
Since a lot is shared between branches, the branch operation is a lot faster, too. 


## bzrtools

bzr functionalities can be expanded through the use of plugins. One set of useful plugins is available through bzrtools, which offer the following facilities: 


### cdiff

cdiff is a colored diff. You just use bzr cdiff instead of bzr diff. 


### shelve

It is current that when working on a branch, you realize you changed separate issues since the last commit. To avoid committing everything at once, you can put away some changes using the shelve command. 

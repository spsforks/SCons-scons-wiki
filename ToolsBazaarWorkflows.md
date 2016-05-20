The following sections try to outline a few workflows for managing external SCons Tools as packages on Launchpad (Bazaar). 


# Basic branching

If you simply want to use an external Tool, or have a look at the sources, issue the command given in the "Branch/Clone" column of the [ToolsIndex](http://scons.org/wiki/ToolsIndex). This will give you a local copy to work with. Example: 


```txt
bzr branch lp:scons-vala vala
```
Patching or extending and then, finally, contributing your code, needs a little more effort... 


# Getting a Launchpad login

We assume that you have initially branched an existing tool, modified it and want to publish your changes. 

* If you don't already have a login at [Launchpad](https://launchpad.net), register there first. A homepage is created for you, and on it you find the [OpenID](https://launchpad.net/+help/openid.html) URL. It has your "Launchpad-login" as last part, after the "`~`". 
* For identification purposes you need to provide a public SSH key to Launchpad. If necessary, [create a new one under your OS of choice](https://help.launchpad.net/YourAccount/CreatingAnSSHKeyPair). Import your key under the entry "`SSH keys`" on your Launchpad homepage. 
* Now you can issue the command "`bzr launchpad-login yournick`" on your local machine. Here, "`yournick`" is your personal "Launchpad-login" as described above. This tells Bazaar to use this nickname for all your following commits/pushes, directed at Launchpad. 
* You should also check your local name (the one that is displayed for commits) with "`bzr whoami`" and change it by "`bzr whoami "John Doe <jdoe@lostmymind.com>"`", respectively. 
* Commit your local changes with "`bzr commit`". 
* Then, push your local branch up to Launchpad with "`bzr push lp:~yournick/toolname/branchname`". Correctly replacing "`yournick`" (your "Launchpad-login"), "`toolname`" (name of the tool) and "`branchname`" (name of your branch), this creates a new branch under your account associated with the tool project. Since Launchpad stores all the different branches in a sort of "matrix", your contribution should show up on your page and on the tool project page along with the original branch. 
* As described on the [Code/Uploading a Branch](https://help.launchpad.net/Code/UploadingABranch) page, you can continue to commit your subsequent changes locally ("`bzr commit`") or publish them again by a push ("`bzr push lp:~yournick/toolname/branchname`"). 
* Eventually, use the "Propose for merging" link (on the Launchpad page of your branch) to get your changes into the "mainline" (also known as "trunk") for the project. 

# Merging, contributing your patched code

The practice currently regarded best, is to branch the current mainline of a Tool,  add your changes, and then propose your branch for a merge via Launchpad. One of the Tool's admins should then merge the user's branch locally, resolve conflicts and finally pushes the result up again. 


# Setting up a project for a new tool

The single steps are: 

* Login in with your user account 
* Go to the main page at [http://launchpad.net](http://launchpad.net) and click on "Register a project" 
* Fill out the details for the first page. Name the project "scons-xyz", where 
"xyz" is the name of your tool. 

* Fill out the second page, and confirm "Create new project" 
* Now you can upload your current version of the tool by 

```txt
bzr push lp:~user/scons-xyz/trunk
```
which pushes it to the automatically created "trunk" series. 


# How to add a downloadable archive to your new project

Select the "trunk" series in the Project's main page 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/click_series_in_overview.png)



"Create a new milestone" and enter a version number 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/create_milestone.png)


Back in the overview page for the "trunk" series, create a new release 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/create_release.png)


Fill out the form for the release and confirm 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/enter_data_and_confirm.png)

Go back to the tool's page on Launchpad, and do a refresh in your browser. Then click on the "trunk" series link. You should see a page like this: 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/trunkseries1.png)

If this has not been done already, link the uploaded branch to this series. Clicking on "Link the branch to this series", select the "trunk" branch... 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/trunkseries2.png)

and get the addition of the series confirmed, after clicking  

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/trunkseries3.png)

Now you can add your TAR archive for download 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/add_file_for_download.png)

... 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/file_was_uploaded.png)

and the archive should get available for download. 

![IMAGE](https://bitbucket.org/scons/scons/wiki/ToolsBazaarWorkflows/release_downloadable.png)


# Additional links

Some helpful links are 

* [https://help.launchpad.net/Projects/Registering](https://help.launchpad.net/Projects/Registering) 
* [https://help.launchpad.net/Projects/SeriesMilestonesReleases](https://help.launchpad.net/Projects/SeriesMilestonesReleases) 
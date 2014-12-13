
**Upload packages** 

Verify that you have SVN and VERSION in your shell environment as described in the setup section above, then run the `bin/scp-sourceforge` script: 

`  $ sh bin/scp-sourceforge sf_username `  
 

**Mark packages with release notes** 

Navigate to the [SourceForge File Manager page for SCons](https://sourceforge.net/project/admin/explorer.php?group_id=30337).  If you're reading this from a printed copy rather than the wiki page and can't click on the link, follow these instructions: 

* Log in to your Source``Forge account 
* Click on `Develop` just under `Forge` in the Source``Forge banner. 
* Under `My Projects`, click on `Develop` next to the SCons project. 
* Click on `Project Admin -> File Manager` 
Open the `scons`, `scons-src`, and `scons-local` directories.  Within each one, open the `$VERSION` folder.  In the `scons/$VERSION` directory, select the `RELEASE.txt` file and mark mark it as the release notes in the popup that appears, then save. 

If this is a final release of the production branch, select `scons-$VERSION.win32.exe` and mark it as the default selection for Windows, then select `scons-$VERSION.tar.gz` and mark it as the default for all other OSes. 

In turn, select each of the files (other than the release notes file itself, which is automatically set) in all three folders (and the folders themselves) and specify that `RELEASE.txt` is to be the release note for that file.  Because of the way the page refreshes after clicking `Save`, it seems to be easier to start at the bottom and work your way up. 

[FIXME: TEST THIS:](ReleaseHOWTO/UpdateSourceForge) You can do multiple releases quickly by opening the File Manager page multiple times in a separate tabs, but if you do, make sure to wait for the page to reload completely in one tab before clicking `Save` in another.  Trying to update multiple releases at once doesn't work, presumably because the session can only handle one update at a time. 

**Hide previous releases** 

* For a checkpoint release, hide all checkpoints in the same series that are older than this checkpoint. 
* For a minor or micro release, hide all the checkpoint releases leading up to this release. 
* For a major release, hide all the checkpoint releases leading up this release AND hide all major and minor releases older than this release. 
For each release name you wish to hide, you have to do the following in `scons`, `scons-local`, and `scons-src`: 

* Click on the gear icon to the left of the package name and select `Cut` from the popup. 
* Click on the gear icon to the left of `old checkpoints` and select `Paste` from the popup. 
**Test downloading** 

Navigate to the [SCons download page](http://sourceforge.net/projects/scons/files/).  If you're reading this from a printed copy rather than the wiki page and can't click on the link, follow these instructions: 

* [FIXME](ReleaseHOWTO/UpdateSourceForge) Add instructions if can't click. 
For each of the `scons`, `scons-src`, and `scons-local` directories: 

* Open the directory. 
* Open the $VERSION folder within the directory. 
* For each package in the folder, click on the link to download it. 
* Verify that the files arrived and look reasonable. 
**Add news item** 

Navigate to the [Project News page](https://sourceforge.net/news/submit.php?group_id=30337).  If you're reading this from a printed copy rather than the wiki page and can't click on the link, follow these instructions: 

* [FIXME](ReleaseHOWTO/UpdateSourceForge) These aren't complete. 
* Go to the `Project Admin -> Feature Settings` page 
* In `Project News`, click `Submit.` 
Once you get to the Project News page: 

* Fill in the `Subject:` box with something like "Release $VERSION now available" 
* Cut-and-paste the blurb you prepared above into the `Details:` box 
* Click `Submit` 
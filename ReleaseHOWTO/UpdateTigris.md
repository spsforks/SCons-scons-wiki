

#### Update project pages

Send the changes you prepared above to Tigris: 

From within the `www` subdirectory of your `trunk` directory: 


  $ svn commit -m"Update project web pages for $VERSION"


Point your browser at [the roadmap page](http://scons.tigris.org/roadmap.html); if anything's amiss, fix it and commit again. 

**Add news item** 

* Log in to your `tigris.org` account 
* Click `Announcements` in the left-hand nav bar 
* Click `Add new announcement` 
* Double-check the date (it's probably already set) 
* Fill in the `Headline` box 
* Fill in the `Body` box with the HTML blurb 
* Click `Add new announcement` 
**Add release name to issue tracker** 

* Click `Issue Tracker` on the left-hand nav bar 
* Click `Configuration options` 
* Click `Add/edit components` 
* Under `scons`, to the far right of `Add ...`, click `Version` 
* At the bottom of the list, to the right of "Add a new version", click `Add` 
* Fill in the `Version:` box with the release ($VERSION) 
* Click the `Add` button 
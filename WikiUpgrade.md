
This page is for bugs and enhancement requests for [this wiki installation](SystemInfo). Feel free to add your wishes and comments. 


## Why Upgrade?


### Missing Features

* different favicon.png 
* install mod_wsgi to run as WSGi application (faster) 

#### Moin info

Greg Noel thinks that the current Moin wiki version (and a link to the Moin``Moin site) should be on the front page (in addition to the change log below).  Something like "_Powered by [MoinMoin](MoinMoin) x.y.z_" or similar.  This uses the Moin``Moin "about" page, which has a lot of information, but no link to the primary location; maybe there's a better one? 

* I've patched wikiconfig.py (there are two of them, BTW) to include version number in the footer along with "Powered by [MoinMoin](MoinMoin)", but the changes didn't come into effect, and I do not know how to restart server. Seems like there is no macro to insert version number either. Are you sure the [ChangeLog](ChangeLog) will be interesting on the [FrontPage](FrontPage)? -- [techtonik](techtonik) 2010-02-17 08:09:57 Badly worded.  "Powered by [MoinMoin](MoinMoin) x.y.z" should be on the front page (not all pages, as it would be in the common footer).  The current version and a link to the Moin``Moin site should be in [the change log below](WikiUpgrade).  Maybe the latter link leads to the page with [information about which is the current version](http://moinmo.in/MoinMoinDownload) (I used the download page, although there might be some other page that provides a better survey, possibly with recommendations as to whether an update is advisable). -- [GregNoel](GregNoel) 2010-02-19 09:07:35 

#### Tools and Builders disambiguation

Wiki lacks [Builder](Builder) and [Tool](Tool) pages with definition of these basic concepts. This should be done to help people put their Contributions into either [ContributedBuilders](ContributedBuilders), [SconsToolbox](SconsToolbox) or [ToolsIndex](ToolsIndex). Even though [SconsToolbox](SconsToolbox) contains a note "Don't put Builders and Tools here.", there is still a lot of *Tool pages there. It should be renamed then. -- [techtonik](techtonik) 2011-02-05 10:02:27 


### Bugs

* [SconsQuickReference](SconsQuickReference) linked from the front page doesn't work as a reference - it is just a wiki search that is confusing 
* The [SyntaxReference](SyntaxReference) page for editing Wiki pages in German does not exist (would be [SyntaxReferenz](SyntaxReferenz)). Is this a configuration/install problem, or do the users really have to roll their own page for each language? 

### Wishes

* Tweak irc log formatter to provide links to bug reports 

## Current modifications to original installation

List of local extensions can be found on [SystemInfo](SystemInfo) page. 


## Wiki ChangeLog

<a name="ChangeLog"></a> Local additions to Moin``Moin: 

* SCons bugs can now be linked directly from this wiki using a macro provided by [GregNoel](GregNoel).  Use <``<Bug(1650)>``> which ends up looking like [[!bug 1650]]; it links directly to the bug page at scons.tigris.org.  Lowercase works too: <``<bug(1650)>``> produces [[!bug 1650]]. 30-May-07 -- [GaryOberbrunner](GaryOberbrunner) 
* Developers should be aware of the [BugScheduleMacro](BugScheduleMacro). -- [GregNoel](GregNoel) 2008-04-11 
* Wiki paths now can be `http://www.scons.org/wiki/FrontPage` (don't have to use the long `/cgi-sys/cgiwrap/scons/moin.cgi` path).  Please report bugs to me.  -- [GaryOberbrunner](GaryOberbrunner) 
* Meaningful paragraph anchors instead of #head-cf83e04bcad3c245dfcd219b1dd87e0de8c70814 <span style="display:none">-- [techtonik](techtonik) 2011-02-18 06:29:25</span> 
Updates to installed version ([newest version here](http://moinmo.in/MoinMoinDownload)): 

* Updated to 1.9.7, 30-mar-13 -- garyo 
   * This was a complete clean install due to the wiki attack in Feb/Mar 2013. 
   * Pages and users were copied over from the old install. 
* Updated to 1.9.5, 20-nov-12 -- techtonik 
   * enabled OpenID support 
   * installed all essential_* underlay pages from [LanguageSetup](LanguageSetup) 
* Updated to 1.8.9, 19-nov-12 -- techtonik 
   * changed default theme to modernized (check your profile to switch to <Default>) 
* Updated to 1.8.8, 18-feb-11 -- techtonik 
* Updated to 1.7.3, 05-feb-11 -- techtonik 
* Updated to 1.6.4 to prepare for 1.7.x upgrade, 04-feb-11 -- techtonik 
* Updated to 1.6.3, 23-apr-08 
* Updated again, to 1.6.1, 11-mar-08 -- [GaryOberbrunner](GaryOberbrunner) 
* Updated this wiki to 1.5.4 to fix some bugs. 12-jul-06 -- [GaryOberbrunner](GaryOberbrunner) 
* Updated this wiki to 1.5.2, now with GUI editor! -- [GaryOberbrunner](GaryOberbrunner) 
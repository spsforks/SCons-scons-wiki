# SCons Developers

This page currently serves as a draft for delegating different SCons responsibilities to different parties.  If you want to volunteer to do something, simply add a task and assign yourself to it. :) 

Hopefully there eventually will be a sizable amount of tasks, and I feel the next step would be to make the list of components more "official" by making them "Categories" on the tigris.org issue tracker.  This way almost anyone can just come in on their lunch break and assign a few bugs to the proper parties. 


## Roles

The following table describes the different roles a contributor the SCons project may have.  [NOTE: Perhaps a role like tigris.org's "observer" would be helpful?] 

Role  | Description  | Responsibilities 
:-----|-------------:|:----------------
Developer | Writes code under his/her control | Checking scons-dev mailing list
 | | Writing code
 | | Submitting to his/her QA contact for testing
QA | Tests code under his/her control | Checking scons-user mailing list to understand user problems
 | | Testing code under his/her control through pre-defined tests and real-world projects using SCons
 | | Submitting patches back to the Developer (optional)
[Release_Team](Release_Team) | Release policy and activities | Participate in setting release schedule
 | | Participate in setting release goals
 | | Rotate actual release duties


## Duties

The following table describes some of the different duties a contributor to the SCons project may have.  One person may have more than one duty; one duty may be shared among several people. 

Duty | Contributor | Responsibilities
:----|------------:|:----------------
Integration Manager | [William Deegan](@bdbaddog) | Monitors and processes pull requests
Release Manager | [William Deegan](@bdbaddog) | Identifies patches to go into next release; when patches have been applied, creates release; coordinates with packagers to distribute release
Webmaster | [William Deegan](@bdbaddog) | Manages the [WebSite](WebSite); point of contact for web provider 
Tigris Tamer | [William Deegan](@bdbaddog) | Deals with administrivia for archive access and issue tracker
SF Tamer | [William Deegan](@bdbaddog) | Deals with residual issues from SourceForge
FAQ Maintainer  | [William Deegan](@bdbaddog)  |  Monitors mailing lists for FAQ worthy material and updates [FrequentlyAskedQuestions](FrequentlyAskedQuestions) 


## Component View of SCons Responsibilities

Components come in two forms: 

* literal: SCons Tool name (e.g., Qt, referring to the Qt Tool) 
* figurative: generic name (e.g. Core, referring to SCons internals) 
Sufficiently large Components can be further divided into Subcomponents, but it is not necessary.

["Affected files" column should be deleted; "Description" and "Notes" should be merged into one column.] 

Components  | Subcomponents  | Description  | Affected Files  | Developers  | QA  | Notes 
------------|----------------|--------------|-----------------|-------------|-----|------
 | | | | | |
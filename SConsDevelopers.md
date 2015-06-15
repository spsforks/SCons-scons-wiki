# SCons Developers

This page currently serves as a draft for delegating different SCons responsibilities to different parties.  If you want to volunteer to do something, simply add a task and assign yourself to it. :) 

Hopefully there eventually will be a sizable amount of tasks, and I feel the next step would be to make the list of components more "official" by making them "Categories" on the tigris.org issue tracker.  This way almost anyone can just come in on their lunch break and assign a few bugs to the proper parties. 


## Roles

The following table describes the different roles a contributor the SCons project may have.  [NOTE: Perhaps a role like tigris.org's "observer" would be helpful?] 

Role  | Description  | Responsibilities 
:-----|-------------:|:----------------
Developer | Writes code under his/her control | Checking scons-dev mailing list, Writing code, Submitting to his/her QA contact for testing
QA | Tests code under his/her control | Checking scons-user mailing list to understand user problems  , Testing code under his/her control through pre-defined tests and real-world projects using SCons, Submitting patches back to the Developer (optional)
[Release_Team](Release_Team) | Release policy and activities | Participate in setting release schedule  , Participate in setting release goals, Rotate actual release duties


## Duties

The following table describes some of the different duties a contributor to the SCons project may have.  One person may have more than one duty; one duty may be shared among several people. 

Duty | Contributor | Responsibilities
:----|------------:|:----------------
Bug Farmer | ? | Ensures that bugs are assigned to someone and that a patch is created (NEED MORE)
Patch Snatcher | ? | Monitors mailing lists for patches; if the patch is not applied in short order, ensures that it is entered in the patch queue
Patch Queue Manager | ? | Tracks patches in the patch queue; determines what additional work is needed and pushes to have that work done; passes accepted patches to integration manager
Integration Manager | [StevenKnight](StevenKnight) | Verifies that the patch passes regression tests; applies patch to trunk
Release Manager | ? | Identifies patches to go into next release; when patches have been applied, creates release; coordinates with packagers to distribute release
Webmaster | [GaryOberbrunner](GaryOberbrunner) | Manages the [WebSite](WebSite); point of contact for web provider (NEED MORE)
Tigris Tamer | [GaryOberbrunner](GaryOberbrunner) | Deals with administrivia for archive access and issue tracker
SF Tamer | ? | Deals with residual issues from SourceForge
FAQ Maintainer  | [SohailSomani](SohailSomani)  |  Monitors mailing lists for FAQ worthy material and updates [FrequentlyAskedQuestions](FrequentlyAskedQuestions) 


## Component View of SCons Responsibilities

Components come in two forms: 

* literal: SCons Tool name (e.g., Qt, referring to the Qt Tool) 
* figurative: generic name (e.g. Core, referring to SCons internals) 
Sufficiently large Components can be further divided into Subcomponents, but it is not necessary.

["Affected files" column should be deleted; "Description" and "Notes" should be merged into one column.] 

Components  | Subcomponents  | Description  | Affected Files  | Developers  | QA  | Notes 
------------|----------------|--------------|-----------------|-------------|-----|------
 | | | | | |


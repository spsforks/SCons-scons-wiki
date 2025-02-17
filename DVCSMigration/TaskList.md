

# SCons DVCS Migration:  Task List

This page is to create a list of tasks for migrating to [Mercurial](http://mercurial.selenic.com/).  The goal is to come up with a reasonably complete set of tasks so we can have a coherent plan when we start the conversion after SCons 2.1 is released.  At some point these probably get turned into Issues in the `tigris.org` database. 

Add tasks.  Fill in descriptions.  Add additional columns.  Volunteer for tasks.  Reorganize the list.  Whatever helps clarify what we need to do. 
[[!table header="no" class="mointable" data="""
 **Task**  |  **Who?**  |  **Description** 
 Choose hosting  |   |  
 HOWTO: Fork SCons to work on private branch  |   |  
 HOWTO: Update your fork from mainline  |   |  
 HOWTO: check in your changes  |   |  
 HOWTO: submit pull request to scons  |   |  
 HOWTO: SCons maintainer - handle pull request  |   |  
 Update tigris.org documentation (link to new HOWTOs)  |   |  
 Update scons.org web site (link to new HOWTOs)  |   |  
 Update wiki with new info (make a pass over for old links etc.)  |   |  
"""]]

Speaking of issues:  although we're going to start by just converting our development and release processes to use Mercurial, a related goal will be to convert our Issues database to whatever our hosting site uses some time after we complete the Mercurial migration (and assuming we pick a hosting site with a decent issue database).  Since the discussion will likely bleed into this area, use the table below to capture ideas about how to handle the issue database migration, so we have a head start when begin to look at that seriously. 
[[!table header="no" class="mointable" data="""
 **Task**  |  **Who?**  |  **Description** 
 Choose hosting  |   |  
 HOWTO: submitting a bug  |   |  
 HOWTO: submitting a patch  |   |  
 HOWTO: submitting a feature request  |   |  
 Update tigris.org documentation (link to new HOWTOs)  |   |  
 Update scons.org web site (link to new HOWTOs)  |   |  
 Update wiki with new info (make a pass over for old links etc.)  |   |  
 Test schema conversion for issues database  |   |  
 Actually convert issues database.  |   |  
 Update bug party scripts  |   |  
"""]]

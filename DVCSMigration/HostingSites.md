

# SCons DVCS Migration:  Hosting Site Selection

We've finished migration of SCons development to [Mercurial](http://mercurial.selenic.com/) in 2012. Here are notes how do we pick a hosting site. 

Options we've discarded: 

* Hosting ourselves.  This is eliminated due to administrative hassle (we want other people to have to worry about that) loss of visibility (we'll get a little more external presence from hosting at a well-known site). 
* `sourceforge.net`:  SCons development was originally hosted at [SourceForge](SourceForge), and our downloads still come from there.  We moved to `tigris.org` because the bug tracker was a real pain to work with.  Reportedly it has not improved since we left.  Lack of migration path to an acceptable bug tracker knocks this out. 
That leaves `code.google.com` and `bitbucket.org` as the two top candidates.  You can propose additional candidates, but to be worth the evaluation effort, any new candidate to be evaluated should have at least one compelling advantage over the othersa. 

Please add additional criteria as new rows in the following tables.  Feel free to fill in the cells with comments and opinions about how each candidate stacks up on each specified criterion.  Note:  this should be where we record the final decisions, and comments/opinions that are relatively "firm" and worth recording long-term.  Take questions that you want to ask or ideas that you just want to kick around to the mailing list. 


### How good is the code hosting?
[[!table header="no" class="mointable" data="""
 `code.google.com`  |  `bitbucket.org` 
 + comment/review code from web  |  + explicit pull requests 
 + patch code from web  |  
 + non-commiters can create patches from web  |  
 + revision/issue autolinking  |  ? 
 + group ownership  |  - single owner, many admins 
"""]]


### How good is the bug tracker?
[[!table header="no" class="mointable" data="""
 `code.google.com 2011`  |  `bitbucket.org 2011` 
 + Python API for creating/updating issues, also issue lists can directly be saved to a local CSV file  |  - no support for import/export of issues (cf. BB-issue 232) 
 - [No API for attachments](http://code.google.com/p/support/issues/detail?id=3213)  |  ? 
 + has a "priority" field and a notion of labels (e.g. for "Easy")  |  - so far, no importance/severity/priority (cf. BB-issue 248) 
 - users need a Google account for creating and commenting on issues  |  + anonymous comments are allowed 
"""]]
[[!table header="no" class="mointable" data="""
 `code.google.com 2014`  |  `bitbucket.org 2014` 
 - <del>Issue API</del> ([deprecated](https://code.google.com/p/support/wiki/IssueTrackerAPI)), issue lists can be saved to a local CSV file  |  + import/export of issues [is now supported](https://confluence.atlassian.com/display/BITBUCKET/Export+or+import+issue+data) 
"""]]

When the time finally comes to pick the actual hosting service, we'll stack up and prioritize the criteria and pick which site wins. 

Is it worth noting that Google Code is focused on the notion of a project with a core team of developers, whereas [BitBucket](BitBucket) is focused on individuals with repositories?  Google Code is fine for projects with a long future, [BitBucket](BitBucket) allows for this and for lots of speculative, potentially short-lived repositories.  Russel Winder 2010-11-22T11:22+00:00. 

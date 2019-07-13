

# SCons Bug Party

The SCons _Bug Party_ was a semi-regular (bi-weekly?) session for examining and prioritizing (or "triaging") open issues.  When it started in March, 2008, we had no triaged issues and 430 untriaged issues (_i.e._, issues with a milestone of `-unspecified-`). Unfortunately the last recorded Bug Party was in May 2011.  This page is retained with interesting information should they be resurrected at a future time.

Since the move to github, it is not as easy to generate a report of the issue status, as that system's issue-tracking is relatively unsophisticated.  We have an "untriaged" lavel which can identify bugs which need that kind of attention, but unfortunately someone has to take the time to add that label, and the number of project participants with rights to do that is quite small, so there's a bottleneck.  Nonetheless, you can follow the link to [untriaged bugs](https://github.com/scons/scons/issues?q=is%3Aissue+is%3Aopen+label%3Auntriaged).


Bug triaging sessions take place on IRC (possibly in future a different interactive chat medium) and should last between sixty and ninety minutes.  All are invited. 


### Responsibilities of Release Team Members

[Release team](ReleaseGroup) members are expected to subscribe to this wiki page (using the "Subscribe" link above) so that they will be automatically notified of any changes.  Not all changes will be reported in the mailing list, but it is expected that "non-routine" changes will be. 

Approximately 4 days before the bug party, a Google [spreadsheet](https://spreadsheets.google.com/ccc?key=0AtofUIe3gu6bdEJtSFQ2RTFlWHZLQmJTSTZlRkpTb2c&hl=en&authkey=CKGv8zU) will be published corresponding to the the agenda below.  Release team members are expected to record their comments and (initial) appraisal in the spreadsheet.  **Write access to the spreadsheets is available by following [these instructions](BugParty/ReadWrite).**  (If you can't access the instructions page, please email [dev@scons.tigris.org](mailto:dev@scons.tigris.org) and ask to be added to the [ReleaseGroup](ReleaseGroup).  It's open to all, as is the bug party itself, but this keeps the noise down a bit.) 

If there is no quorum of comments six hours before the bug party, the meeting is automatically rescheduled one week later.  In this context, a _quorum_ is that "most" of the issues have three or more significant comments attached to them.  (The definition of "most" is flexible, as the number of issues varies so widely.  If there's disagreement about whether "most" of the issues have a quorum, the bug party will be held according to the original schedule.)  Issues that lack a quorum will be bypassed at the bug party. 

People who comment on the issues will be expected to attend the meeting, unless they specifically send mail to the contrary.  People who comment but do not attend must make sure that their comments are particularly understandable or the comments will be ignored. 

The meeting is called and moved to the next week if there's no quorum by five minutes past the start time.  In this context, a quorum is at least three team members who commented on the issues. 


### Agenda

Specific agenda items: 

* Triage issues.  As a rule of thumb, issues are expected to be resolved in two or three minutes on average.  If the discussion of an issue goes past five minutes, it should be moved into email and the issue bypassed until the next meeting.  This agenda item is suspended with about fifteen minutes left in the expected meeting time to allow for the remaining agenda items. 

**ApproveChanges**

The ApproveChanges action for MoinMoin permits the approval of page changes made by untrusted users. Such changes are queued on a separate subpage of each page edited by untrusted users, so if such a user edits FrontPage, the edited version will be saved as a revision of FrontPage/ApprovalQueue. By using the ApproveChanges action, reviewers can approve acceptable changes and incorporate them into the original (parent) page. The ApprovalQueue subpage is never seen by anyone other than reviewers. 

**Table of Contents**

[TOC]


## Finding Queued Changes

Since changes queued for review are typically written to subpages called ApprovalQueue, a search for such pages should yield a list of queued changes pages where changes are waiting to be reviewed. The [ChangesToReview](ChangesToReview) page provides such a search and could therefore be a useful interface for page reviewers. 


## Navigating Queued Changes

Once a queued changes page has been found, the contents of the page will reflect the most recent queued change. However, there may be several queued revisions of the page, and it may be the case that one of these revisions is more appropriate than the others. By using the info action on a queued changes page, the different revisions may be browsed and the most suitable revision displayed. 

When choosing the ApproveChanges action on a particular revision of a page, that particular revision will be the one approved for incorporation into the proper page itself. When choosing the action on the default view of a page (without any revision being specified), the current revision will be the one approved. 

It should be noted that revisions of the queued changes page are independent of each other: unless an untrusted user has saved a page more than once, refining their edits over time, all edits will have been made with only the knowledge of the contents of the parent page. Thus, it can be necessary to approve more than one revision of the queued changes page if all suitable changes are to be incorporated into the parent page. 


## Approving Changes

Choosing the ApproveChanges action on a queued changes page will result in a dialogue being displayed, asking whether the displayed page version should be approved. Approving the version will result in its changes being propagated to the parent page. 


### The Effect of Approving Changes

The effect of approving changes is slightly more sophisticated than just copying the approved version of the page over the parent page. Instead, the action considers which changes were actually made to the original version of the parent page when the untrusted user decided to edit it, and such changes are then applied to the parent page as it is now. 

In the simplest of cases, the queued changes can be applied and the parent page updated without incident. However, it is possible that the following message be shown when choosing the action: 

   * _The affected page has been edited since the queued changes were made._ 
This indicates that the parent page has changed since the untrusted user made their edits, with a possible consequence of this being that their changes no longer fit in with the page as it is now. In many cases, the queued changes made by the untrusted user and the changes made in competition with the queued changes can be reconciled and the parent page updated with both sets of changes intact. Sometimes, however, the changes will conflict with each other and need to be reconciled manually. In this latter case, the page editor will be opened for the editing of the parent page with conflict indicators present in the page text showing the problematic regions where conflicts have arisen. 

Once changes have been approved from a queued changes page, the ApprovalQueue subpage will be deleted and will not appear in any search for queued changes. However, the page revisions will still exist, and approval of other revisions from the queue can still occur. 


## Rejecting Changes

Where no changes present in a queued changes page are of interest, the ApprovalQueue subpage itself can be deleted. This effectively rejects all queued changes. 


## Approving Users

Users who are present in the [ApprovedGroup](ApprovedGroup) do not need to have their edits approved. Thus, to avoid inconveniencing trusted users of a Wiki, such users should be added to this group as soon as possible. 


## Appointing Reviewers

Users who are present in the [PageReviewersGroup](PageReviewersGroup) are allowed to view and approve queued changes. Thus, users who have an editorial capacity in a Wiki should be added to this group so that they can control the final content of each page. 

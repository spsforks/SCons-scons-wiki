
A copy of the scons-dev thread in April 2007 that proposed the three-branch release model, lightly edited.  Quotes from previous messages are in **bold**. 


# Steven Knight

RT members-- 

As I mentioned (off-line), I started working on translating my step-by-step Aegis-based release instructions to Subversion: 

                        * [http://www.scons.org/wiki/Major_Release_HOWTO](http://www.scons.org/wiki/Major_Release_HOWTO)   
 [http://www.scons.org/wiki/Minor_Release_HOWTO](http://www.scons.org/wiki/Minor_Release_HOWTO) 
The question this brings up is how we want to handle Subversion branching for releases.  I can think of three potentially attractive strategies off the top of my head: 

1.  Branch before the release occurs, then release from the branch (and tag the release on the branch, of course).  
  
 This has the advantage of setting up for parallel release development right away.  The branches/0.97 branch would be created immediately and is all set to handle bug fixes for 0.97.1, 0.97.2, etc., while feature develoment can still take place on          other branches off the trunk. 
1.  Release from the trunk, and then branch after the release occurs (and tag the release on the trunk).  
  
 Releases all come from the same branch, but we create the subsidiary _(missing)_  
  
Drawback:  the branch isn't necessarily exactly the same as what you released from.  The packaging code, for example, may need cruft to interact with Subversion differently when building from the branch. 
1.  Release from the trunk, and don't bother with branching (just tag the release on the trunk).  
  
This is sometimes known as a "golden thread" SCM pattern. All development would be done on subsidiary branches, and changes are only merged up when they've been demonstrated to not break anything.  The trunk is always releasable.  Branches can still be cut from the trunk as needed to support parallel release development. 
My moderate preference is for #3, followed by #1, and I'm not a big fan of #2. 

Any strong arguments in favor of one of the above, or some other approach? Something simple to start with is fine.  I think it will be more effective to tweak our policies in response to actual practice, as opposed to starting with some complicated policy that may or may not reflect what will actually work. 

Comments? 


# Greg Noel

On May 18, 2007, at 2:03 PM, Steven Knight wrote: 

**...  how we want to handle Subversion branching for releases.  ...**  
 ** 1.  Branch before the release occurs, ...**  
 ** 2.  Release from the trunk, and then branch after the release ...**  
 ** 3.  Release from the trunk, and don't bother with branching ...** 

1. A simplified description of our current paradigm is a "development" (a.k.a. "unstable") branch, where features are checked in, debugged, tested, and possibly removed.  Once a feature has matured, the changesets for the feature are applied to the trunk (possibly with a little tweaking).  Releases are tagged on the trunk as in the "golden thread" pattern, but since SVN makes no distinction between branches and tags, urgent bug fixes can be applied to the tag and a new release made (or one can create a branch off the tag and release from there, either works). 
Pro: Bleeding-edge development is available to interested users quickly. 

Pro: Mostly-stable checkpoints are available to those who prefer less risk. 

Pro: Branches can be made off the unstable branch for parallel development and later merged back in. 

Pro: The trunk is always releasable. 

Con: Tracking the changesets belonging to features is a maintenance nightmare for the integrator (viz., Steven Knight).  (The integrator might be able to use a clerk for the grunt work, but the responsibility would remain.) 

Con: Features can get in the unstable branch and never mature enough to be applied to the stable branch.  Making sure orphaned features are eventually removed will take discipline. 

Con: There are intrinsic, unresolvable differences between the unstable and stable branches to account for the differences in labeling. 

**My moderate preference is for #3, followed by #1, and I'm not a big fan of #2.** 

I find #4 preferable, but otherwise I agree. 


# Bill Deegan

The release strategy should depend on whether you need to continue patching a release, or not. For example in general when you release a web site (no need to support more than one version out there at a time), you rarely have release branches. However if you ship software where ongoing support is important (packaged software for example), then a branch for each major release stream makes sense. 

(Yup I do CM/release management for a living). For one of my clients we do the following, official releases have a branch, (tag and branch), development builds are released whenever they are stable and have a date stamp (Not tag, though a changelist number is in the version string). Major long term (longer than expected feature releases) are usually on a separate branch which is updated from the development stream on a regular basis. 

So ongoing snapshots from development branch, and then branch for feature releases? Do we have a list of features/bugs for the next release? 

Hope that's helpful. 


# Greg Noel

After thinking about this some more, I'm going take another shot at explaining this suggestion. 

On May 18, 2007, at 7:14 PM, I wrote: 

1. **A simplified description of our current paradigm is a "development" (a.k.a. "unstable") branch, where features are checked in, debugged, tested, and possibly removed.  Once a feature has matured, the patchsets for the feature are applied to the trunk (possibly with a little tweaking).  Releases are tagged on the trunk as in the "golden thread" pattern, but since SVN makes no distinction between branches and tags, urgent bug fixes can be applied to the tag and a new release made (or one can create a branch off the tag and release from there, either works).** 
There are three primary branches: the "unstable" or "development" branch; the "stable" or "checkpoint" branch; and the "release" or "production" branch.  There are also a number of less-permanent branches where original development takes place. 

A less-permanent branch can be as informal as a checked-out tree where someone is fiddling with a change, or as formal as an actual branch from some base position.  However formal or informal it may be, it's where most development takes place.  It eventually leads to a patch, with the full set of changes being bundled into a patchset. 

The unstable branch is where patches mature.  After a patchset is created, it is checked in here, where developers can run it through its paces, find and repair problems, and make sure there are no unexpected side-effects.  If further changes are required, additional patchsets are created and checked in.  (Aside: the applied patchsets are used to identify the point on the unstable branch, so it has a name like scons-p1234.) 

Once a patch is mature and deemed stable enough, it is added to the stable branch by applying all of its patchsets.  Usually, a few patches are applied at the same time to create a checkpoint, that is, an intermediate stable point on the way to the next release. Checkpoints are packaged and published, but since they are effectively a beta, the range of announcement is restricted to  a smaller audience.  (Aside: the date is used to identify a checkpoint, so it has a name like scons-20070521.) 

Some checkpoints are identified as releases.  All of the patches on the stable branch since the last release are applied, the release is packaged and widely published, and a great sigh of relief is heard. (Aside: a normal release is known by a three-number identifier, so it has a name like scons-1.2.3.) 

It may not seem like it, but it's basically what we do now.  If you look back at prior releases, the time between releases with names like 0.9.1 and 0.9.2 is six to eight months, but then there will be a blizzard of releases with names like 0.96.91 and 0.96.92 that are separated by a month or two.  This suggestion formalizes the latter as checkpoints and gives a specific technique for handling the evolution of patches from unstable to production. 

It may seem like a lot of unnecessary mechanism, but as we move through the 1.0 release, it will give a great deal of flexibility, both in how we plan and schedule releases and in how users can sign up for the degree of risk they are willing to undertake when using SCons. 

Oh, Steven, as I was working this through, I thought a lot about how releases should be named.  Are you committed to your scheme, or should I start a thread about naming releases? 


# Sohail Somani

On Fri, 18 May 2007 19:14:33 -0700 Greg Noel wrote:  
 [snip/] 

**Con: Tracking the changesets belonging to features is a maintenance nightmare for the integrator (viz., Steven Knight).  (The integrator might be able to use a clerk for the grunt work, but the responsibility would remain.)** 

There are some ways of handling this: 

* svnmerge.py - Must use when using svn + branching 
* All checkins reference at least one item in bug tracking 
* Use branch-per-fix-slash-feature - In conjunction with svn switch, it should be doable 
**Con: Features can get in the unstable branch and never mature enough to be applied to the stable branch.  Making sure orphaned features are eventually removed will take discipline.** 

So does the branching look like this: 

trunk 

* -> unstable 
   * -> feature1  
 -> feature2  
 -> bug932 
where -> means "branched from?" 

I like this idea and in conjunction with svnmerge, it would be possible to unmerge unwanted changes provided we use branch-per-fix-slash-feature. The only issue as I recall is that svnmerge.py does not handle transitive changes. So you would /always/ have to go through the unstable branch which is sensible imo. 

**SK: My moderate preference is for #3, followed by #1, and I'm not a big fan of #2.  
 GN: I find #4 preferable, but otherwise I agree.** 

I don't really see how #4 is wildly different from #3. Maybe I should go back and read it. 


# Greg Noel

On May 21, 2007, at 8:48 AM, Sohail Somani wrote: 

* **All checkins reference at least one item in bug tracking** 
SCons is less formal in this regard, so I don't think this will fly. A lot of the work done on SCons isn't reflected in the issue tracker, and I don't see that this situation will change much in the near future. 

Yes, requiring all changes to be tracked is good practice, and maybe we will go that way someday, but forcing the creation of an issue just to be able to do a checkin isn't going happen right now. 

* **Use branch-per-fix-slash-feature - In conjunction with svn switch, it should be doable** 
Most development now takes place in local checkouts rather than in branches, but other than that, I believe that it's assumed that we're going in this direction for larger/longer developments. 

**So does the branching look like this:** 

**trunk 

* -> unstable 
   * -> feature1  
 -> feature2  
 -> bug932** 
**where -> means "branched from?"** 

I distrust ASCII art, since I can never get it to look like what I want, but here goes. 


```txt
patch  unstable  stable  release

patchset->|       |        |
patchset->|       |        |
          |       |        |
          |======>|        |
patchset->|       |        |
          |       |        |
          |======>|        |
          |       |=======>|
```
where ===> means "multiple patchsets applied." 

A patch, implemented in one or more patchsets, is first placed in the unstable branch.  As it matures, it is merged first into the stable branch (possibly with other patches) to be part of a checkpoint, and then finally into the release branch as part of a release. 

There may be branches created to develop patches, but once the patch is merged into the unstable branch, it's all merging from that point on; once the three primary branches are forked, the only branching from them is for someplace to work on a patch. 

SVN was supposed to be able to merge patchsets like this from the git-go, but they reneged on that promise, so for now it's an intensely manual process to track the patchsets and do the cross-branch merges.  I understand that SVN is now looking at support for this idea again, so maybe there will be a tool to help with this eventually, but I don't see it in the near future. 

**I don't really see how #4 is wildly different from #3.** 

It wasn't intended to be wildly different.  #3 is what we do now; #4 is a more formal version that makes a sharper distinction (or maybe a clearer hand-off) between the various stages.  And it also allows a bit more flexibility in that patches can be held back from a checkpoint or a release without withdrawing them altogether. 

**Maybe I should go back and read it.** 

I wrote another try at describing #4 last night; that's the one you should go back and read. 


# Gary Oberbrunner

Greg Noel wrote: 

**After thinking about this some more, I'm going take another shot at explaining this suggestion.** 

This is good work.  Let me just take a specific example to see if I understand it. 

I implement a feature, say SubstInFile :-)  I do it mostly in my checked-out area.  When I'm ready, I commit it to the unstable branch (which is currently called "core", yes?).  Let's say it has svn ID r1000.  Other people test it, try it, and submit a few changes; r1010, r1011 and r1012. 

Now when it's matured for a while, we gather up those svn commits and svnmerge.py them to the stable branch (which is currently called "trunk"). This creates rev r1100.  Question: is this done atomically one commit per bug/feature, or as one big rollup with other stuff from unstable->stable at the same time?  In any case, further patches for SubstInFile wend their way from unstable to stable in the same way.  No changes get made to trunk that haven't been made in unstable first and promoted.  (OK, in real life there's the emergency fix applied directly to the trunk and back-ported later, but aside from that.) 

Then when it's time to do a release, SubstInFile is all ready to go in the stable branch, so we just do "svn cp $SVN/trunk $SVN/tags/rel_scons_x.yy.z". Greg: is this what you had in mind, or is there another branch, $SVN/branches/release where we copy all the changesets since last release from the stable branch?  I'm not sure what would be gained by that.  If it's just a stable name for "the current release", we could make a "current_release" tag that always points to the current release.  If it enables a different kind of change tracking, please say more. 

If the above is true, then the main svnmerge hassle is remembering what needs to be merged from unstable to stable.  Keeping a high-level description of each feature/bug and what changesets go into it (and vice versa!!!) so the appropriate merges can be done and we don't lose anything on unstable. svnmerge will tell us what's not been merged, but over time that list will grow long with old hoary stuff that was never quite ready. 

As for patch releases, we decide that unstable r1201, r1202 (for SubstInFile) need to get into a minor fix release.  So we svnmerge them to $SVN/branches/scons_x.yy.zz as well as trunk?  Or we apply them to the trunk and back-port to the branch?  From an svnmerge perspective, it's happy either merging to trunk and thence to the branch, or directly from unstable to the branch.  But we should pick one method & stick to it. 

Side note re: branches and tags, Greg is right that there's no technical difference between a tag and a branch, though there's a large semantic difference.  At my company we typically tag off the trunk, and the rule is "no changes on a tag".  If we need to change something we fix it on the trunk and re-tag (svn rm/svn cp).  And then if a fix release is needed, we just branch from the tag point on the trunk. In the case of scons, there may be transient changes that the build system needs (?Steven?) that never get merged back to the trunk, so those changes could be made directly on the tag branch. 


# Sohail Somani

**Gary: Now when it's matured for a while, we gather up those svn commits and svnmerge.py them to the stable branch (which is currently called "trunk"). This creates rev r1100.  Question: is this done atomically one commit per bug/feature, or as one big rollup with other stuff from unstable->stable at the same time?** 

In the worst case, you have to rollback one unstable->stable and then merge everything but the unwanted feature again. A feature(?) of svnmerge is that you can't easily ignore certain files when doing a merge/rollback. If this is an issue (I think it is) then I would guess unstable->stable should also be done atomically. 


# Bill Baxter

Been lurking here for a long time, but hearing this discussion I'd just like to throw out the idea of using mercurial/bazaar/monotone/darcs/git instead of svn. I can't really say much about them, but the whole mantra of these distributed revision control systems seems to be that handling branches and patches is easier. 

Just wanted to throw it out there to make sure somebody has considered it before you folks spend a lot of effort to move to SVN. 


# Steven Knight

**Greg: Oh, Steven, as I was working this through, I thought a lot about how releases should be named.  Are you committed to your scheme, or should I start a thread about naming releases?** 

Go ahead.  As far as I'm concerned, any of this is open for discussion. 

(I'll tip my hand a little by saying that I've never much cared for the even-number-stable, odd-number-developmental convention.  It's always seemed very arbitrary to me--although, like most naming conventions, it's really a religious argument, and what seems logical and intuitive to me is likely to seem capricious and arbitrary to others...) 


# Steven Knight

**Gary: Side note re: branches and tags, Greg is right that there's no technical difference between a tag and a branch, though there's a large semantic difference.  At my company we typically tag off the trunk, and the rule is "no changes on a tag".  If we need to change something we fix it on the trunk and re-tag (svn rm/svn cp).  And then if a fix release is needed, we just branch from the tag point on the trunk. In the case of scons, there may be transient changes that the build system needs (?Steven?) that never get merged back to the trunk, so those changes could be made directly on the tag branch.** 

I was going to say that "shouldn't happen," but then I realized that it does with respect to the actual version number that will be packaged with the release.  The 0.97 branch 

Other than that, my goal (so far successfully adhered to) has always been to avoid the need to cherry-pick changes by keeping the code itself in sync between branches.  Promoting from a branch to its parent has so far always involved promoting *all* of the accumulated changes on the branch. Using svnmerge.py should at least give us the flexibility to cherry-pick if we need to in the future, but I think we can all stay more sane if we just don't do that unless it's an emergency. 

I think this implies that "main" releases don't get created from branches, and we don't use release branches (when they exist) as vehicles for extended development.  I think this is essentially what Greg's describing, and I agree with his characterization that it's basically the way we've already been doing things. 

Let me see if I can distill this down to some guiding principals: 

* The trunk always stays golden (passes its tests). 
* Main line of releases comes from the trunk. 
* Development takes place on subsidiary branches. 
* Promotions to parent branches take all of the accumulated branch changes. 
* The only time we might release from a branch would be for a critical patch to a release that's already been superceded by later releases.  
  
Example (using the current release naming convention): if 0.97.1 was released with "stable" increments on 0.97, and 0.97.{90,91} had already been released with disruptive features in anticipation of 0.98, and we needed a critical fix on top of 0.97.1, only then (i.e. only as needed) would we branch off 0.97.1 in order to deliver a 0.97.2 with the critical fix.  Graphically: 

```txt
           0.97   0.97.1   0.97.90   0.97.91   0.98
   trunk ---+--------+--------+---------+--------+-----
                      \
                       +-----+-----|
                           0.97.2
```
Rip into the above... 


# Steven Knight

**Sohail: * All checkins reference at least one item in bug tracking** 

**Greg: SCons is less formal in this regard, so I don't think this will fly.  A lot of the work done on SCons isn't reflected in the issue tracker, and I don't see that this situation will change much in the near future.** 

**Yes, requiring all changes to be tracked is good practice, and maybe we will go that way someday, but forcing the creation of an issue just to be able to do a checkin isn't going happen right now.** 

I'm not opposed to this (and I'll doubtless be more effected by it than anyone else).  Are there other compelling reasons not to make this a new policy, as long as we're shaking up the development model? 

Where what we've been doing works and makes sense, sure, let's keep it. But where we can get better, let's not necessarily stick to old patterns just because it's how things currently get done.  Sure, we can still decide "not now," but that's no reason not to at least consider it. 

**Sohail: * Use branch-per-fix-slash-feature - In conjunction with svn switch, it should be doable** 

**Greg: Most development now takes place in local checkouts rather than in branches, but other than that, I believe that it's assumed that we're going in this direction for larger/longer developments.** 

Yes. 


# Greg Noel

On May 21, 2007, at 6:07 PM, Gary Oberbrunner wrote: 

**I implement a feature, say SubstInFile :-)  ... I commit it to the unstable branch (which is currently called "core", yes?).  Let's say it has svn ID r1000.  Other people test it, try it, and submit a few changes; r1010, r1011 and r1012.** 

Yes, what I call the unstable branch is probably closest to branches/core. 

So far, so good.  The patch now has a group of patchsets (a patchgroup? we'll need something to describe it) that implement the change. 

**Now when it's matured for a while, we gather up those svn commits and svnmerge.py them to the stable branch (which is currently called "trunk").  This creates rev r1100.** 

Actually, you use svnmerge.py to gather up the patchgroup; you can then test it, possibly tweak it to fix problems, and then commit it to the stable branch (as r1100 in your example). 

I'm not sure if the trunk (assuming we keep the name) should correspond to the stable branch or the release branch.  I can make a case either way, so it probably depends more on what we feel the external expectation would be if someone checked out that branch. 

**Question: is this done atomically one commit per bug/feature, or as one big rollup with other stuff from unstable->stable at the same time?** 

Personally, I'd prefer one commit of a patchgroup per patch, but I'd also like to require that the tests all pass for every merge.  It will take a long time to test each individual patch, so I can imagine the temptation to only do one commit for a number of patches. 

**In any case, further patches for SubstInFile wend their way from unstable to stable in the same way.  No changes get made to trunk that haven't been made in unstable first and promoted.  ...** 

Yes.  This is how the branches will retain synchronization (in the long term). 

**Then when it's time to do a release, SubstInFile is all ready to go in the stable branch, so we just [create a tag for the release]. Greg: is this what you had in mind, or is there another branch ... where we copy all the changesets since last release from the stable branch?  I'm not sure what would be gained by that.  If it's just a stable name for "the current release", we could make a "current_release" tag that always points to the current release. If it enables a different kind of change tracking, please say more.** 

I'd have a third branch that only contained releases; patches from the stable branch would be rolled up the same way as patches from the unstable branch to the stable branch.  That's why I'd prefer having separate roll-ups for patches to the stable branch: it gives the ability to defer a patch to a later release if need be.  In general, I'd expect all of the patches to be rolled up into the release branch, but this scheme provides the opportunity to decide right up to the last minute.  Since the alternative would be to revert the patch, it seems to be that the little extra hassle is worth the added flexibility. 

It does have the happy side-effect of a fixed label for the current release, which not only makes documenting it easier, but also has benefits for those kind folks who include SCons in their distributions. 

**If the above is true, then the main svnmerge hassle is remembering what needs to be merged ... svnmerge will tell us what's not been merged, but over time that list will grow long with old hoary stuff that was never quite ready.** 

Yeah, I said it would take discipline, but I see it as a part of job for the release committee.  On a regular basis, the patches should be reviewed and a decision made as to whether they should be reverted. (Maybe the reversion is to put them into a separate branch for additional work, or some other way of archiving them.)  An alternative is to require that there will never be more than N active patches under consideration, so "old hoary stuff" would have to be removed before new patches could be added. 

**As for patch releases, ...  So we svnmerge them to [the release tag] as well as trunk?  Or we apply them to the trunk and back-port to the branch?  From an svnmerge perspective, it's happy either merging to trunk and thence to the branch, or directly from unstable to the branch.  But we should pick one method & stick to it.** 

This is as much an issue about version lifetime as it is about branching strategy, since it depends on how long the release will need to stay around.  As soon as I dig my way out of these messages, I'm going to start a thread about that, but basically, "normal" patches are picked up in the next release cycle while "emergency" patches have a special procedure outside the usual rules.  Can you re-raise this point on the new thread?  (But in both cases, I'd expect the patch to be applied unstable --> stable --> release.) 


# Greg Noel

On May 21, 2007, at 6:38 PM, Bill Baxter wrote: 

**Been lurking here for a long time, but hearing this discussion I'd just like to throw out the idea of using mercurial/bazaar/monotone/ darcs/git instead of svn. ...** 

Yeah, wouldn't it be loverly.  I particularly wonder about GIT, which seems to be dealing with the problems SVN reneged on.  In a couple of years, it should be a product that seriously challenges SVN. 

**Just wanted to throw it out there to make sure somebody has considered it before you folks spend a lot of effort to move to SVN.** 

Yep, we looked at them before we moved to SVN.  At the time, none of them had the features and maturity we wanted. 

Also, tigris.org only offers CVS and SVN.  We'd already determined CVS was inadequate, so there wasn't a lot of selection. 


# Greg Noel

This is mostly a "me, too" post, but there are a couple of points I want to raise. 

On May 21, 2007, at 9:35 PM, Steven Knight wrote: 

**... my goal (so far successfully adhered to) has always been to avoid the need to cherry-pick changes by keeping the code itself in sync between branches.  ...  Using svnmerge.py should at least give us the flexibility to cherry-pick if we need to in the future, but I think we can all stay more sane if we just don't do that unless it's an emergency.** 

I concur, but this means that the flow of patches into the unstable branch has to be controlled, and only "promising" patches allowed in.  In general, I'd like to see all of the patches in a checkpoint rolled up into a release, but I think there should be a little more flexibility for patches moving from the unstable branch to the stable branch.  I'd want a patch to stay for a while in the unstable branch for seasoning; if a checkpoint happened to occur just after a patch was added, I'd expect it to be held back for the subsequent checkpoint. 

I see the job of patch management as belonging to the release team. On the one hand, they should nominate the patches to be included in the unstable branch, and, on the other hand, if a patch is held back for more than a couple of checkpoints, they should nominate the patch to be removed for further development outside the unstable branch. 

On the gripping hand, when I get around to describing the release numbering, I'll want to make a case that certain patches will be expected to stay in the unstable branch for a longer time, potentially two or three releases.  These are patches that have implications for forward or backward instability: not only should these be tested for a longer time, but they should also be grouped together so as to minimize disruptions. 

**I think this implies that "main" releases don't get created from branches, and we don't use release branches (when they exist) as vehicles for extended development.  I think this is essentially what Greg's describing, and I agree with his characterization that it's basically the way we've already been doing things.** 

Yes.  One can see in the record of releases that when these guidelines were violated, SCons became less stable. 

**Let me see if I can distill this down to some guiding principals:** 

* **The trunk always stays golden (passes its tests).** 
Uh, the stable branch always stays golden, yes.  (The release branch should also be golden, but that should go without saying.) 

* **Main line of releases comes from the trunk.** 
The main line of releases is pulled up from the stable branch. Usually, it would be the same as a checkpoint (except for labeling). 

* **Development takes place on subsidiary branches.** 
Yes, usually forked from the unstable branch. 

* **Promotions to parent branches take all of the accumulated branch changes.** 
No, let's try not to require this.  I agree that we should try to do this, but if we require it, we're painting ourselves in a corner. 

* **The only time we might release from a branch would be for a critical patch to a release that's already been superceded by later releases.** 
Yes.  In fact, if the bug was far enough back, you might have to branch from several tags and apply the patch in all of them. 


# Greg Noel

On May 21, 2007, at 9:41 PM, Steven Knight wrote: 

**I'm not opposed to this (and I'll doubtless be more effected [_sic_ - "affected"] by it than anyone else).  Are there other compelling reasons not to make this a new policy, as long as we're shaking up the development model?** 

**Where what we've been doing works and makes sense, sure, let's keep it.  But where we can get better, let's not necessarily stick to old patterns just because it's how things currently get done. Sure, we can still decide "not now," but that's no reason not to at least consider it.** 

I worked in a shop that required that every patch had to refer to a bug.  I was on the development side rather than the maintenance side, but I saw how often someone would just make up a bug so they could check in a fix.  For those whose job performance was measured by how many bugs they closed, this was great, but the blizzard of trivial bugs obscured the real, deep bugs that actually needed attention. (It also gave a false impression of how buggy the product was.) 

To my mind, your review process captures the managerial intent of the mandate that every patch has to be for a bug.  If you want to take the time to create an issue for every patch that doesn't already have one, that's fine; as I said, it's good practice and it would provide some help in tracking the progress of the patch into production. 

But I wouldn't want to lose the the very real benefits of having all those eyes on the patch.  That's where I see the trade-off: if the review discussion moves into the bug tracker, fewer eyes will be involved. 

So, bottom line, I'm not adverse to making this a new policy, but I'd like to discuss it in the context of how review issues (and other QA problems) are handled.  And I wouldn't be hard-core about requiring bugs for trivial (or cosmetic) fixes. 


# Peter Amstutz

**Re Bill Baxter on using other than SVN** 

I've been using Bazaar-ng aka 'bzr' ([http://bazaar-vcs.org](http://bazaar-vcs.org)) for about six months now and it's terrific.  Bzr development is directly supported by Canonical which means it has full time developers and has been maturing at a quick pace, and the team is very dedicated to making the revision control system that they want to use, with lots of little convenience features that most other software in this category seems to lack. 

Bzr is also written in Python, so I've been pondering the potential for Scons <--> Bzr integration to support the whole configuration management chain, similar to what Vesta ([http://vestasys.org](http://vestasys.org)) is supposed to do. 


# Peter Amstutz

**Re Steven Knight on guiding principles** 

This sounds good, but I should also point out that unless the diff-merge-test-commit cycle can be fully automated (and I'm still looking for a good way to do that in any version system) the maintainer tends to become a bottleneck.  Also if it requires a lot of outside pressure from contributers to get features merged, most people won't bother and SCons will be the poorer for it. 

I'm not familiar with svnmerge.py, so maybe it fixes the worst of svn's problems, but merging in svn in general is a holy terror.  If you plan on relying on regular branching and merging in SVN, also plan on huge headaches when SVN craps a pile of conflicts all over your working directory.  In my experience, svn works best when most development happens directly on the unstable trunk, you have an automated build-and-test process to catch bad check-ins (and developers who break the build are soundly thrashed) and reserve branching for true diverging branches (like releases) and/or development of large-scale disruptive features.  As with the other poster who mentioned the shop that required every checkin be done in reference to a bug, branching for every single little change is overkill. 

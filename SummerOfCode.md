*A page for collecting central links and information about SCons' participation in the Google Summer of Code.*

**Table of Contents**

[TOC]

# 2007 Post-Mortem

_Note:  The discussion below was post-mortem after 2007.  To get in on what's happening for 2008, see the [starter page for 2008](GSoC2008)._ 


## Plans for Next Year

_These are points that will be merged with the [current checklist](GSoC2007/CheckList) to create the [checklist for next year](GSoC2008/Checklist).  For now, we just need to be sure any new points are listed._ 

* Get [[!bug 123]] and [[!bug 321]] links working. 
* Starter page for mentors. 
* Actively recruit mentors all year long. 
* Revamp proposal page to emphasize process and be less intimidating. 

## Retrospective of This Year

_These are mostly things that didn't go as well as they could._ 

* **Start even earlier.**  Google moved the starting time almost two months earlier.  This caught many organizations flat-footed, including SCons.  We never recovered; we were late starting at almost every milestone.  Our requests for ideas and mentors went out as the application period was opening; that's too late.  Our announcements to students went out after the application period opened and our follow-through with additional announcements was poor; that's "a day late and a dollar short."  We didn't have very many proposals, so we were OK during the evaluation period, but  even then we nearly missed the deadline.  Bottom line: we need to start the campaign for mentors and ideas even earlier, probably around the end of December or sometime in January.  We should have everything ready to go not later than the end of February so that we won't be late at every marker. 
* **More community involvement.**  Greg was really the only one who worked with the students to sharpen their proposals.  There needs to be more than one set of eyes looking at the proposals. 
* **Get the word out.**  We did a <ins>_terrible_</ins> job of broadcasting our name and site to places where students might find it.  We got on the Python Foundation's page of Python-using projects, but that's about it.  
[_Several projects made "public service announcements" hyping their organization on the discussion mailing list.  I don't know if Google considers that "fair use" but we should add it to our list of places for next year._ - JGN] 
* **Proposal page should focus on process.**  The proposal page probably scared off a number of good applicants; it needs to be less intimidating.  Moreover, both students that successfully submitted applications had some confusion about the order to do things, so it should be revamped to emphasize the process, not the proposal.  (On the other hand, it was clear that everyone who followed the instructions produced good proposals, and those that didn't weren't serious.  As a first-level filter, it worked exactly as it should.  The hoops should remain, but they should appear to be less challenging.) 
* **Better presentation of ideas.**  If one understands SCons, the ideas are clear and reasonably succinct.  To someone who doesn't know SCons and is looking for an interesting project, it may not be obvious what is going on.  We need some help in editing the ideas page by someone who's got real experience in communicating technical ideas to people who lack the background in a particular area.  
[_My wife is a technical writer and she tells me that there are specific techniques that can be used, but she's not interested in the job herself, more's the pity._ - JGN] 
* **Find new ideas.**  Subversion has someone whose job is to monitor the mailing list and make sure bugs and patches don't fall through the cracks.  If a bug is reported or a patch is offered, but it isn't picked up by a developer and fixed, his job is to submit the bug or patch to the tracker.  We should do that, too, but we should also have someone (maybe as part of the job description for the bug/patch catcher) who watches for ideas and turns them into enhancement requests.  Ideas that make it into the tracker, whether as bugs or enhancements, are a gold mine. 
* **Three mentors are not enough.**  We need to start a recruitment campaign to find more mentors.  We need to start this immediately and we need to keep working on it throughout the year.  Some people offered ideas for projects; it might be possible to draft them.  Steven should know who provides patches; active patchers might make good mentors. 
* **Mentors didn't put interests in mentors page.**  Only Greg put his interests in the [mentors page](GSoC2007/Mentors).  It's supposed to be a resource for students to find compatible mentors to sponsor them by looking for someone with similar interests.  If there are no interests published, it's not very useful. 
* **Mentoring starter page.**  Steven had problems with what he needed to do as a mentor, so Greg ill-advisedly offered to come up with a page to describe the steps that a mentor should go through.  We need to twist his arm to make sure he writes it while it's still fresh in his mind. 
* **Add community members to mentors@scons.**  Just three people on a mailing list is a cabal, not a representation of the SCons community.  There needs to be someplace where private discussions take place, but there needs to be more representation, both from additional mentors (see above) and from members of the community.  Greg suggested several candidates; nothing was done with them. 
* **Easy links to bugs.**  The ideas page (and possibly other places) should have an easy way to link to bugs at tigris.org.  Greg made a suggestion for a macro to provide the links, but it never went anywhere. 

# 2006 Post-Mortem

_Note:  The discussion below was post-mortem after 2006.  To get in on what's happening for 2007, see the [starter page for 2007](GSoC2007)._ 


## Plans for Next Year

Collect ideas here for how we plan to do better in 2007 (assuming Google does this again, of course). 

* Start earlier.  February or March is not too early. 
   * Mine the other projects for good ideas.  We should start this _now_. 
   * Gather the information about what should be contained in a proposal.  It's currently scattered and needs to be collected in one place.  [2007-02-18: Done, at least a [solid draft](GSoC2007/Proposal) - JGN] 
* Identify mentors right away: 
   * Python had a [web page for mentors and their interests](http://wiki.python.org/moin/SummerOfCode/Mentors) so students could craft their proposals toward the mentor's interests.  It seemed to work well; we should consider it. 
   * Possibly create a mentors@scons mailing list if we have enough.  
(JGN: _We should have a list even if we don't have enough.  My household is not a fan of Hillary Clinton, but to paraphrase her, "It takes a community to mentor a student" and I can imagine that there will be community members who are not mentors yet who should be involved._) 
* **Get ideas written up sooner** and figure out how to write better task suggestions.  This was a weak area last year. 
* Mine for ideas wherever we can: 
   * Ideas from last year. 
   * Requests for enhancements and new features in the issues database. 
   * Defects (bugs) in the issues database. 
   * Advertisements on scons-dev and especially on scons-users. 
   * Advertisements on scons.org and scons.tigris.org 
   * [Projects/companies that use SCons](SconsProjects). 
   * **Where else?**  Update this list if other sources are found so that we won't forget them in future. 
* Be prepared for Google's announcement: 
   * Have the web pages done _before_ the application period so Google can audit them. 
   * Get our application in to Google immediately, so they have plenty of time to look us over and confirm that we are a viable candidate. 
   * Use a name that better says what we do, like "SCons Software Construction Tool" or "SCons Software Build System written in Python" or some such. 
* Advertise our participation to drum up more submissions.  We will be listed on Google's own heavily-advertised web pages, but there are plenty of other places: 
   * Mailing lists (scons-users primarily, but also scons-dev) 
   * www.scons.org and scons.tigris.org 
   * Related third-party sources: 
      * tigris.org 
      * python.org (they mention Python-powered projects in their own SoC pages) 
      * sourceforge.net (although that's a tenuous connection) 
      * [Projects/companies that use SCons](SconsProjects), both web pages and mailing lists. 
   * **Where else?**  Update this list if other sources are found so that we won't forget them in future. 
* Emphasize interactions with students: 
   * Some students did not reply to requests for fixing their applications immediately.  
(Thomas: _Make more complete offers right away so very little will need to be done to fix the applications._) 
   * Discourage students from splitting proposals across multiple areas; they should submit multiple proposals, and if we think they should be combined, we can tell them. 

## Retrospective of This Year

The original [SummerOfCodeIdeas](SummerOfCodeIdeas) page contains the initial kick-start for the 2006 Summer of Code, courtesy of [ThomasNagy](ThomasNagy). 

On balance, we didn't handle 2006 as smoothly as we could have (no reflection on Thomas, without whose initiation we wouldn't have done anything at all). While the experience is still fresh in our minds (especially the mentors), I'd like us to collect ideas about what we didn't do well in 2006: 

* We didn't respond to the initial announcement--indeed, wouldn't have responded at all if Thomas hadn't gotten the ball rolling at the last minute. 
* Responses to most other deadlines tended to be at the last minute (Greg's prompting). 
* Need to make sure mentors know to read their gmail accounts (_cough_ SK _cough_...). 
* It was apparent from the quality of response that there wasn't sufficient direction in the ideas page to lead the students to viable projects. 
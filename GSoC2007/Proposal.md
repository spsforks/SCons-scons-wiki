

# How To Write a Good Proposal

This page outlines what is needed in a proposal that will be acceptable to SCons.  For a source of potential tasks, look at the [ideas page](GSoC2007).  You can also look at the [mentors page](GSoC2007/Mentors) for information about the people who will be doing the evaluations. 


## Requirements

As a student, you must be willing to meet the following requirements, in addition to the [Google eligibility requirements](http://code.google.com/support/bin/topic.py?topic=10730): 

1. **You must not overbook yourself.** Working on your SCons project should be your main activity for the entire summer. 
1. You must be prepared to stay in regular contact with your mentor via email, IRC, or other mutually-agreed method. 
1. You must already know Python and you should have at least cracked open the code and taken a look inside so that you have an understanding of the codebase with which you will be working. 
1. You will be expected to learn how to use the needed developer tools if you don't already know them, including [Subversion](http://subversion.tigris.org) and [QMTest](http://www.codesourcery.com/qmtest/). 
1. You must be willing to discuss what you are doing on the SCons mailing lists.   You will be expected to submit a status report to the developers' mailing list at least weekly.  At a minimum, the status report should contain these three points: 
      * What did you do this week? 
      * What problems are you having (if any)? 
      * What do you plan to do next? 
By far the most important item is the first. Google pays for thirteen weeks, five days a week, eight hours a day.  We can be flexible to some extent to allow for vacations and the like, but if you can't provide us with 520 hours before the completion deadline, save us both some time and don't apply. 


## Ground Rules

You can submit more than one proposal, but it's better to pick something where you feel that you can do a great job, and concentrate on writing one outstanding proposal, with lots of detail about what you plan to accomplish. 

The results must be maintainable and clean.  If you submit a quick hack or something we would have to rewrite from scratch, we will not accept the project as completed, even if the code works as advertised.  We would rather have a maintainable, clean, and incomplete piece of code that we could extend than a complete but unmaintainable piece of code. 

Do your own work.  On the one hand, don't hesitate to ask the community for assistance, but on the other hand, don't expect us to debug your code for you. 

The results must be released under the terms of the [X/MIT Open Source License](http://www.opensource.org/licenses/mit-license.php).  If you are planning to incorporate material from any other source (including translations and transliterations), the source must have a compatible license. 


## The Process

Write a short note to the developers' mailing list (if you aren't already subscribed, you should be) and tell us what you're thinking about doing.  If the response is favorable, go ahead and start preparing the proposal. 

Create a wiki page named GSoC2007/Your****Name (if you don't have a wiki account, you should [create one](UserPreferences)) and put your proposal in it using the template below.  Don't underestimate the value of a good proposal.  Be prepared to spend quite a bit of time on it as it is a major element by which you are judged. Take the time to dot your _i_``'s and cross your _t_``'s and use the correct terminology because you can be sure that you're competing against others who will do so.  And if the proposal is interesting but not complete in some way, be prepared to spend even more time with the mentors to expand and refine the proposal into something we can sponsor. 

The more thoroughly you demonstrate an understanding of SCons and the work entailed by your proposal, the greater the chance that we'll accept it. Your proposal needs to convince us that you understand what needs to be done and that you have the skills to do it.  Don't just repeat what we already have on the ideas page; show some insight into the why and how of the problem. 

You'll have a lot to learn before you can begin coding your project, so plan to spend some time orienting yourself.  And there will need to be some time while others try out your results and report bugs and other problems that will need to be fixed.  Think about this when creating your schedule.  Remember, no project is trivial—all of them represent a significant investment of time and effort. 

Proofread and spellcheck your proposal, then have someone else check it. Yes, this isn't an English contest and not everyone is a native speaker, but if the application is hard to understand, the mentors are less likely to look upon it kindly.  We're primarily an English-speaking team and will expect you to be able to write good code comments, documentation, email messages, and IRC chat in English.  Plus, communication skills are important in distributed development such as you see in open source projects, and this is one of the few chances the mentors will have to evaluate that.  Moreover, it's not uncommon for a better-written proposal to trump a better proposal even in the commercial world, so it's worth making sure that your proposal is the best you can make it. 

Once the proposal has enough information in it to make discussion feasible, drop a note to the developer's mailing list and tell us about it.  Be prepared to defend your proposal, but expect that a number of changes, potentially major, will probably be needed. 

Apply at Google (((REF))) with an abstract of the proposal and include a link to the wiki page above. 


## Proposal Template

A strong proposal will cover the relevant portions of this information: 

* Project Title 
* Contact Information - Name, email, and timezone at a minimum.  Other information, such as a phone number, home page, or IM handle, is at your discretion.  Accepted proposals will be published (by Google) and are potentially visible to spambots, so don't put anything in them that you don't want publicly known.  In particular, consider obscuring your email address so it won't be picked up by spammers. 
* Synopsis - A couple of paragraphs describing what the project will do.  Obviously, conciseness counts, but it should be complete enough to show the full scope of the work.  Use your own words; it's important to show us that you understand what you write and are not just parroting back what you found somewhere else. 
* Benefits to the SCons Community - A good project will be both fun (for you) and generally useful (to users). 
* Project Details - About one to two pages of what the project entails.  In general, you can't be too detailed, but stay focused; a rambling fifteen-page document doesn't help your cause, either.  (If you have an external design document that covers some of these elements, it's sufficient to give the link and then cover the remaining topics in your proposal.)  It should include most of these elements: 
   * Analysis - What the completed project will provide.  Explain to us your take on the problem and how you would solve it.  "This could be implemented with that technique."  "This API will offer that functionality."  If you don't know, say so.  "I need to research these areas."  "I'll need help sorting that out." 
   * Compatibility - SCons takes backward compatibility very seriously, so include a review of existing SCons features that will be affected and explain how your new work will coexist with that functionality. 
   * Techniques - Any unusual approaches, specialized algorithms, or outside tools. If there are interactions between components, a sketch of the anticipated API. 
   * Plan - How will your project integrate into SCons?  Describe what you're going to do and how you think you will do it, and possibly even what you will do if your initial approach does not work. 
   * References - Include academic references, such as links or _brief_ quotes, which back up your ideas. That kind of stuff impresses us.  On the other hand, do **not** include a dozen pages of reference materials; we won't read it.  Summarize.  If the project is related to research already in progress at your school, tell us how you are involved; it allows us to evaluate your approach, as well as giving us the assurance that you are serious about your topic and have already done background work. 
   * Examples - Sometimes the best way to keep the proposal concise is with a short, well-chosen example, usually just a few lines long. 
* Deliverables - It is very important to list quantifiable results here, such as "Implement new feature X" or "Improve Y and Z to do foo" or "Speed up bar by A%".  Deliverables must also include tests and documentation.  The deliverables should be tied to the schedule; on average, a deliverable should be provided every two or three weeks. 
* Project Schedule - How long will the project take? Provide an estimated timeline, so we know what to expect. In general, tests should be one of the first things done, before the start of coding. Please also include other information on your summer plans which might be relevant to planning development. And give yourself some slack to allow for unexpected developments. **This is, arguably, one of the most important sections, so do not overlook it!** 
* Other Proposals - If you submit multiple proposals (either to SCons or to other organizations), tell us about them. If you have a preference for a particular proposal or particular organization, tell us that, too.  It won't affect your ranking, and it will give us a chance to try and get you the project you prefer. 
* Brief Biography - Who are you? What interests you? What makes you the best person to work on this project? 
   * A short resumé or CV is appropriate, but informal is both fine and preferred. 
   * Focus on _relevant_ prior experience that would make you the best choice. 
   * If you know anyone in open source who can vouch for your code quality and/or diligence, use them as a reference. 
   * Include anything else you'd like us to know. 

## Suggestions

The following tips, although not required, will give you the best chance of having your proposal accepted.  Note that the first six points are effectively identical to the advice in the _Writing Your Application_ section of [Google's Advice for Students page](http://code.google.com/p/google-summer-of-code/wiki/AdviceforStudents) (we both started with the same source ;-)). 

1. **Promote your idea** - Describe your idea in detail.  What is its ultimate goal?  What components will it have? How does it benefit the project itself and the SCons community?  How do you plan to achieve completion of your project?  If a specification already exists, what will you do that will go above and beyond expectations? 
1. **Promote yourself** - Convey your passion for the project.  Talk about what makes _you_ stand out from the rest of the crowd.  Talk about your past experiences, what makes you tick. Why are you interested in open source software, and SCons in particular?  What interests do you have, and how do these interests relate to SCons?  There is a basic assumption that people applying for Summer of Code have at least some programming skills already, so rather than a lot of time elaborating on these (though by all means, do tell us what you know), spend time talking about _you_. 
1. **Show enthusiasm** - Summer of Code is a very exciting opportunity, and SCons is an extremely exciting project to work on.  We're not looking for people who want a summer job to pass the time; we're looking for devoted people who are excited about SCons and about open source, who will remain part of our community even after the project is done. 
1. **Tailor your application to the project** - Some people may send applications to more than one project, and copy/paste large parts (or even the entirety) from one application to the next. It is painfully obvious when this is done, and it is a sure-fire way for your application not to be taken seriously. Each application you send should be targeted and tailored for the specific mentoring organization and project to which you are applying. 
1. **Get feedback from the community** - Discussing your idea with some established SCons folks is _highly recommended_.  Try to have your application reviewed by someone before you submit it, whether that be the mentor for a particular project or a person with expertise in a certain area. If your idea duplicates existing efforts or code (and does not provide a very convincing reason for doing so), it will be rejected. Don't be afraid to ask the community for help; we want you to succeed just as much as you do. 
1. **Don't wait until the last minute** - Applications received in the beginning of the submission process will generally be reviewed more thoroughly than those received in the last hours before the interface closes.  Mentors are also more eager to read applications in the beginning and suggest revisions to make your proposal more acceptable. Start preparing your proposal when you first hear of Summer of Code, not a day or two before the deadline.  Start planning your application as soon as possible!  Even start working on the project; if you can offer some preliminary results to show that your project will succeed, your chances of being accepted are improved. 
1. **Be bold** - Do you have a brilliant idea that's not on the ideas page? Great! Don't be afraid to suggest innovative and ambitious approaches to solve hard problems.  Ultimately, we're looking for new major contributors for our projects and a bold proposal makes us think you might be a candidate.  If you know enough about SCons to suggest an interesting project, that lets us know you're serious about us, and in turn, makes us more likely to pick you. 
1. **Be realistic** - Google requires you to _complete_ a project by the deadline; don't be so bold that your proposal can't be finished.  If you think the project as suggested is too large and you can only feasibly complete part of it, make sure your proposal covers a reasonable subset of the functionality (that is, something which is useful without the rest of the project being implemented).  Or consider proposing a prototype that can be extended as time permits.  In general, we'd rather you had time left over at the end that you could spend on polishing (or working on some other task) rather than running out of time. 
1. **Be original** - Many students submit nearly-identical proposals based on recent "hot" papers from academic publications.  Such a proposal is a reasonable thing to suggest (we do want to stay current in our implementation techniques), but if you do make a proposal based on a current hot area, make sure to make another application in an unrelated area, because you'll have plenty of competitors.  It seems counter-intuitive, but the best applications we've received haven't remotely resembled any of the ideas on the ideas page.  Since SCons is a general-purpose tool, there's a lot that can be done, and we don't have the same focus and solid list of objectives that other GSoC projects might have. 
1. **Be sooner** - If you are _already_ a contributor to SCons, your odds improve tremendously.  Contribute in any way you can, but if you can, submit a few patches.  Having a proven track record of code is a great indication that you will deliver some value in a GSoC project.  That way, by the time the selection rolls around, you'll be a known quantity. 

## Acknowledgments

Some of the material above is adapted from writings of the fine folks at [Drupal](http://drupal.org/) and [Adium](http://adiumx.com/), of Josh Berkus of the [PostgreSQL Project](http://postgresql.org/), and of Thiago Macieira of [KDE](http://kde.org/).  We thank them for allowing us to use it. 

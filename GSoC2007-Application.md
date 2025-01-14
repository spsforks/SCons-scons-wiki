

## Mentor Organization Application

_This is a work in progress, of course..._ 

This structure is taken directly from the [2007 Google sign-up form](http://code.google.com/soc/org_signup.html). 

Some points to ponder: 

* The submitter is assumed to be the primary administrator; there's noplace to enter the information separately (as was done in the FAQ questions). 
* For all practical purposes, the application is write-once: there's no way to edit or change it after the application has been submitted (except by submitting a new application and asking that it replace the old one).  In other words, we need to be pretty sure of our replies before submitting it. 
* Some organizations aren't submitting mentors now, preferring to wait until they see the students' applications and putting them together with a mentor at that point.  That might work for a large organization like NetBSD, GNOME, or Plone, but for a small organization like SCons, Google will want to be sure that there are enough mentors to handle the number of students, so including some sample mentors is a good idea. 

### About Your Organization

      1. **What is your Organization's Name?** 
SCons Foundation: Next-Generation Build Tool 

      1. **What is your Organization's Homepage?** 
[http://scons.org/](http://scons.org/) 

      1. **Describe your organization.**  _This information will be used (along with the ideas link and some other information) to create a Google-hosted "about" page, so it should also act as an introduction to SCons._ 
SCons is a cross-platform, next-generation build tool. Unlike most other build tools that invent their own mini-language or wedge a scripting language onto some other configuration file syntax, SCons configuration files are actually Python scripts. The flexibility of Python scripting makes it possible to solve complicated build problems in surprisingly small amounts of maintainable code. Its portability (the only requirement is Python 1.5.2 or later), cross-platform features (extensive support for languages and compilers), and reliability (MD5 file signatures, cache) make it an incomparable tool for build masters in particular, and also for many free software projects. 

SCons has been an active project since its founding in 2001.  SCons now averages about 7000 downloads per month and has active user and development mailing lists with membership of approximately 450 and 150, respectively, and average monthly traffic of 275 and 100 messages, respectively. 

The SCons Foundation was organized in 2003 to hold the copyrights of the SCons source code, and to provide a legal entity for any other organizational necessities (e.g., receiving donations). The Foundation is a Delaware non-profit corporation, but does not currently have 501(c)(3) status. 

      1. **Why is your organization applying to participate in GSoC 2007? What do you hope to gain by participating?** 
We'd like to broaden the appeal of SCons by adding new functionality, improve its code quality, and help SCons continue to advance toward being the best software build tool available. 

      1. **Did your organization participate in GSoC 2005 or 2006? If so, please summarize your involvement and the successes and failures of your student projects. (optional)** 
We participated in GSoC 2006.  We were awarded two slots, but one student was unable to commit to the necessary time before the project started, and we returned the unused slot for use by another participating organization.  The second project was completed successfully and it is in the process of being integrated into the official code base. 

      1. **If your organization has not previously participated in GSoC, have you applied in the past? If so, for what year(s)? (optional)** 
Not applicable. 

      1. **What license does your project use?** 
MIT/X license. 

      1. **URL for your ideas page** 
[http://www.scons.org/wiki/GSoC2007](http://www.scons.org/wiki/GSoC2007) 

      1. **What is the main development mailing list for your organization?** 
[dev@scons.tigris.org](mailto:dev@scons.tigris.org) 

   1. **Where is the main IRC channel for your organization?** 
We don't use IRC regularly for development. The user IRC channel is `#scons` on the OPN network ([irc://irc.freenode.net/scons](irc://irc.freenode.net/scons)). 

   1. **Does your organization have an application template you would like to see students use? If so, please provide it now. (optional)** 

```txt
Short descriptive title here
Student's name here

Full Proposal: http://scons.org/wiki/GSoC2007/YourNameHere

Abstract:

abstract here (two or three paragraphs)

Benefits to the Community:

benefits here

Personal:

contact info here (include timezone)

highlights of relevant experience here
```
   1. **Who will be your backup organization administrator? Please enter their Google Account address. We will email them to confirm, your organization will not become active until they respond. (optional)**  _The backup administrator is not contacted until after the organization has been accepted, as the very last step before listing the organization on their web pages, so the individual must reply <ins>promptly</ins>._ 
Gary Oberbrunner, Gary dot Oberbrunner at gmail dot com. 


### About Your Mentors

      1. **What criteria did you use to select these individuals as mentors? Please be as specific as possible.** 
The mentors are the most active contributors to SCons (of both ideas and code). 

      1. **Who will your mentors be? Please enter their Google Account address separated by commas. If your organization is accepted we will email each mentor to invite them to take part. (optional)**  _What they really want is a <ins>sample</ins> of the mentors so they can assess whether there are a sufficient number of mentors to support the expected students.  Mentors can be added later, if need be, but it will be a hassle._ 
[SguireKnight](SguireKnight) at gmail dot com, Gary dot Oberbrunner at gmail dot com, [GregNoel](GregNoel) at tigris dot org, others to be determined later. 


### About The Program

      1. **What is your plan for dealing with disappearing students?** 
There's a private mailing list for mentors, administrators, and interested community members for discussing issues like this. 

A separate branch will be created for each student project.  We'll expect check-ins of in-progress source code at least weekly to minimize loss of in-progress work. 

The mentor will keep in regular contact with the student (no less than weekly) to make sure they're still working. 

The student must submit a public status report at least weekly to the developers mailing list. 

      1. **What is your plan for dealing with disappearing mentors?** 
We will assign a backup mentor for each project, who will be CC'ed on all email between primary mentor and student.  If the primary mentor is unresponsive, the backup mentor will step in. 

The administrator and the backup administrator will track that these requirements are being satisfied by the mentors.  Any issues will be brought up on the mentors-only mailing list for resolution. 

If that fails, we send Vinny and the boys to start breaking fingers. 

      1. **What steps will you take to encourage students to interact with your project's community before, during and after the program?** 
The students must post their project designs, probably on our wiki.  The students will be expected to announce design updates to the mailing list, to request feedback, and to respond to the feedback in a timely fashion. 

The students' status reports will be publicly available so community members can stay informed of progress.  The students will be required to respond to questions about their status reports in a timely fashion. 

      1. **What will you do to ensure that your accepted students stick with the project after GSoC concludes?** 
We will work to complete integration of the student's code into the main code base and release it to the public as soon as possible after completion. 

We will heavily publicize the authorship of the project, including prominent mention in relevant portions of SCons documentation. 

We will gently discourage others from stepping in to answer mailing list questions and requests about the project, letting the involved student be the visible face for ongoing future support of the feature. 

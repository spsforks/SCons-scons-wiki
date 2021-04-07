
 _ | _ 
:--|:--
SEP | 0000
Title | SCons Enhancement Proposals(SEPs)
Author | Cem Karan
Status | Draft
Type | Process
Post History | [http://scons.tigris.org/ds/viewMessage.do?dsForumId=1268&dsMessageId=2381941](http://scons.tigris.org/ds/viewMessage.do?dsForumId=1268&dsMessageId=2381941)

# SCons Enhancement Proposals



## Author's guide

This is an index of SCons Enhancement Proposals (SEPs).  SEPs are intended to mimic the concept of Python Enhancement Proposals (PEPs, see [PEP 1, PEP Purpose and Guidelines](http://www.python.org/dev/peps/pep-0001/)) so that the SCons community can have a place to comment on ideas as a group.  This page takes the place of [PEP 0, Index of PEPs](http://www.python.org/dev/peps/pep-0000), [PEP 1, PEP Purpose and Guidelines](http://www.python.org/dev/peps/pep-0001), [PEP 9, Sample Plaintext PEP Template](http://www.python.org/dev/peps/pep-0009), and [PEP 12, Sample reStructuredText PEP Template](http://www.python.org/dev/peps/pep-0012), which combined are the index of PEPs, and the format and style guide for PEPs. 

The following steps should serve as a guide as to how to write up a SEP: 

1. Read the SEPs that are currently proposed.  If you find one that is similar or identical to what you wish to propose, read the proposal and any discussion on the page **carefully**.  Oftentimes, seemingly simple modifications to SCons are not so simple.  If enough people propose the same tweak and have that tweak rejected, someone will likely modify the SEP to explain why the tweak won't be accepted. 
1. **Research** your proposal **THOROUGHLY**.  The more accurate and complete information a developer has at hand, the easier it is to create the SEP.  Poor proposals are ambiguous or incomplete.  Good ones tell everyone exactly what is wished for, and what needs to be done to make it happen. 
1. Start a discussion on the [user's](http://www.scons.org/lists.php#users) and [dev's](http://www.scons.org/lists.php#dev) mailing lists to get feedback on your idea.  Keep track of any and all feedback you get.  Others may have already heard your proposal before, and may save you the effort of writing your proposal, only to have it shot down. 
1. Start a wiki page to document all you learn.  At the time of this writing, there isn't a special format for SEPs, but if you read what Python has (see [PEP 1](http://www.python.org/dev/peps/pep-0001), [PEP 9](http://www.python.org/dev/peps/pep-0009), and [PEP 12](http://www.python.org/dev/peps/pep-0012) for ideas) that will get you started.  Keep your page up to date and as complete as possible.  At this stage of the game, you are the person responsible for really driving your SEP forward.  Well-written SEPs are more valuable than poorly-written ones, and more likely to get a good response. 
1. Once your SEP is coming together, add it to the list of draft SEPS below.  Announce that you've added it on the user mailing list.  Developers and other old hands that are interested have already subscribed to this page and will know when changes occur to it. 
Here is a diagram that may help you understand the process: 

![SEP Process](https://github.com/scons/scons/wiki/SEPs/SEP_Process_steps.png)


# SEP index

## Draft

_After_ your proposal has been discussed on the mailing lists, then this is the place where you want to link to it. 

| SEP   | Description |
| ------| ------ |
|[SCons Enhancement Proposals (SEPs)](SEPs) | A proposal for how to write enhancement proposals for SCons|
|[Aggregates Extension](Containers) | A proposal to extend SCons so it understands what containers (e.g., ELF, tar, directories, OS X bundles, and OS X Frameworks) are |
|[MoreSiteSconsDirs](MoreSiteSconsDirs) | A proposal to add more site_scons dirs, with default locations for various OSes. |

## Accepted

After your draft has stabilized, and one of the developers/leaders decides they like it enough, you might find your proposal moved down to here.  If it has, congratulations!  Now you need to do any final polishing to ensure that the developers have all the information they need.  **NOTE** you may **not** make semantic changes to your SEP at this point!  That means that if you proposed a new type of Builder for DocBook, you can't decide that it should also handle LaTeX as well.  SEPs that have been accepted are supposed to be feature complete, requiring only a little bit more polish, not whole new feature enhancements. 


## Deferred

Proposals that are here have been accepted, but no work is being done on them at the moment.  This can for any number of reasons, including lack of time, energy, manpower, etc.  If your SEP has made it here, try to find out why; one good reason is that your proposal is important, but too big.  See if you can _reasonably_ break it up into smaller SEPs.  Note that not all SEPs can be broken up into smaller parts reasonably; discuss the idea of breaking it up on the mailing lists, and see if others agree that that is a good idea. 


## Rejected

Proposals that are here may have been rejected for any number of reasons.  The reasons for rejection will be explained on the SEPs own page.  As the diagram indicates, although a SEP is rejected, it may not be a permanent rejection.  It may have been rejected because the SEP was written poorly, incomplete, etc.  In those circumstances, it is a good idea to keep working on your SEP until it is sufficiently well written that it becomes accepted. 


## Final

Proposals that are here should not be modified.  At most you can correct spelling or grammar mistakes, but should avoid making other changes.  Once a proposal has reached this stage, it means that everyone more or less agrees on what the feature needs to be, that the documentation is sufficient, etc.  SEPs that are at this stage are also referenced in the [issue database](https://github.com/scons/scons/issues).  Note that the issues database is the official way to get an enhancement in; everything you see here is a way for the SCons community to discuss a SEP, but if the SEP isn't put into the database, then it doesn't really exist.  If your SEP makes it down to here, it will be up to you to write up the issue properly and get it into the database. 

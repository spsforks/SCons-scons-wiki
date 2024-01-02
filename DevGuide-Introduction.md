# SCons Developer Guide

## Welcome

to the SCons Developer Guide. It provides pointers to all the material that we offer in various forms: [Wiki](http://www.scons.org/wiki), [webpage](http://www.scons.org), [user guide](http://www.scons.org/doc/production/HTML/scons-user.html), [MAN page](http://www.scons.org/doc/production/HTML/scons-man.html), ...

However, when you start following links and flipping pages for the first time, you'll probably get lost very soon. That's sort of expected, and nothing to be ashamed of. ;)  In the following sections we try to outline the steps and documentation that you need, to simply "get things done". Think of it as a kind of "Quickstart" document...

SCons is a mature project that has been around since 2001, and a lot of thought and development effort has gone into it already. We have a single dedicated mission: developing and providing a replacement for `make` and the GBS `Autotools`. And we have lots of users---individuals, open-source projects, universities and companies---, which rely on SCons' stability and cross-platform capabilities. For the development team it's really important to not let these people down.

That's why we have certain workflows in place, which may look over-engineered at first. But they've stood the test of time, and they help us to develop a very robust and stable tool for our users...and that's the main reason for things being as they are. You can find a rather detailed description here:

* [Developer's Guidelines](http://scons.org/guidelines.html)

So, please try to stick to our rules and be prepared to have a "long breath" when you're about to make larger changes, or during reviews of your pull requests. ;)

If this will be your first contribution to an open-source project ever, you might want to check out a video like Julie Pichon's [I want to help! How to make your first contribution to open-source](http://pyvideo.org/video/2988/i-want-to-help-how-to-make-your-first-contributi) from the [EuroPython 2014 - Berlin](https://ep2014.europython.eu/). It describes the basic steps that most projects out there follow, and SCons is no exception. Beginners can find bugs that are good to start with, in our list of [easy issues to fix](EasyIssuesToFix), or on [OpenHatch.org](http://openhatch.org/projects/SCons).

Finally, if anything is unclear or the descriptions on this page raise further questions, please contact us at our user mailing list. You can write to [scons-users@scons.org](mailto:scons-users@scons.org) straight away, but take into account that it's a moderated list and your post has to get "waved through" each time. So if you want to get a quick answer, or plan to be part of our community on a regular basis, you might want to consider subscribing to the list [http://four.pairlist.net/mailman/listinfo/scons-users](http://four.pairlist.net/mailman/listinfo/scons-users) instead.


## Getting the sources

Your contributions and changes will get processed through _pull requests_, so you'll have to create a personal account on [https://github.com](https://github.com), fork the "default" SCons repository, and then clone your private copy to your computer. The page [GitWorkflows](DevGuide-GitWorkflows) lists these steps in greater detail. It also describes how to push your changes back up to Github, so that you can finally create the pull request.

For a short description of how the source tree is organized you can refer to: [SourceWalkThrough](DevGuide-SourceWalkThrough)

So, you have the sources... now what?


## Working on documentation

The documentation for SCons is basically split in two parts: the main documents for the [user guide](http://www.scons.org/doc/production/HTML/scons-user.html) and [MAN page](http://www.scons.org/doc/production/HTML/scons-man.html) in the `doc` subfolder, and the descriptions of the Tools, Functions, Builders and Construction Variables which appear both in the manpage and in the Appendices A-D of the [user guide](http://www.scons.org/doc/production/HTML/scons-user.html). You can find them in "`*.xml`" files parallel to the Python source files in the `SCons` folder - this locality is intended to make it easier to remember to update docs and code together (roughly, "if you change `Foo.py`, also look at `Foo.xml`").

Check out [DeveloperGuide/Documentation](Documentation) for a full description of the DocBook toolchain that we're using currently.

Make your editorial changes, then validate all the documents as described in the [toolchain documentation](Documentation). Required dependencies for this validation step are the Python bindings for either "`libxml2`" or "`lxml`", so make sure to have one of them installed in your system (since SCons became all Python 3, you'll need lxml as the Python libxml2 binding is no longer supported).

If the validation was successful, you can commit your changes locally, push them to your SCons fork, and then create a pull request - if you have a browser window open on your fork, it should pop up a prompt automatically, and the message from your push should also give you a link you can go to. PLEASE read and follow the instructions in pre-filled screen when you click to create the PR.


## Fixing and developing the core sources

After cloning the sources, you want to run SCons from the local tree directly. Check the [development tree description](https://github.com/scons/scons), which can also be found as `README.rst` at the top level of your source folder, for details.

As you may have read in our [development guidelines](http://www.scons.org/guidelines.html), we do a lot of [testing](TestingMethodology). Before starting to develop new features or fixing bugs, it's a good idea to run the whole test suite once with

```txt
python runtest.py -a
```

This way, you can check that there are no tests failing on your system in the current revision.

If they are all passing (there may be several "No results", depending on which tools are available), you can start with development. Make sure your local "`master`" branch is up to date with the canoncial source on GitHub, create a branch to work in, change sources and add files as required, then commit your changes locally. 

Please help us to improve and extend our regression test suite. For a bugfix add one or more test(s) that break before applying your changes, and pass afterwards. When adding features, try to create end-to-end tests covering the new functionality. The "Testing Howto" at [TestingMethodology](DevGuide-TestingMethodology) explains all the details. Try to write your tests so that they work cross-platform.

Ensure that your source changes are properly documented. Especially when changing and adding features, it is expected that you update comments and the XML files accordingly (see section above).  Edit the file "`CHANGES.txt`" by adding your name and a short note, reflecting your contributions.

Finally, run the full testsuite (`runtest.py`) again, to ensure that your changes didn't break any of the former behaviour (regression test).

If all tests pass, you can commit your changes locally, push them to your personal SCons fork, and then create a pull request.


## Reviews

After you have submitted a pull request, your changes will get reviewed by other developers. Be prepared to receive comments and getting asked questions. Often you'll be asked to update your pull request for seemingly minute details. Please don't take this as an offense, this is part of the quality process we try to adhere to. It doesn't happen only to you, but even to very experienced developers...and we caught several subtle bugs this way already.

We usually wait for comments about a week per pull request (just as a rule of thumb). Once the review phase is over, your commits get merged into the mainline.


## Editing the webpages

Send a mail to our User ML and ask for help.

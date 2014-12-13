

# Howto accept pull requests (for the SCons admin)

You can see the diffs on the bitbucket.org website.  When you do that it will give you the hg commands to pull the user's repo to run tests on. You can then either use hg to push those changes to scons repo on bitbucket, or do it on the website.  If the user was working on the default branch, the following should suffice: 


```txt
hg pull https://bitbucket.org/USER/scons -r 123abc456  # only pull the rev corresponding to the pull request, or you might get other things that user is working on.
hg heads # see what we got
hg merge # with no args, merge merges the user's head into the tip.  It does not commit.
# run tests, make changes as needed, update src/CHANGES.txt
hg commit -m "Merged in USER/scons (pull request #22), fixes #1234 (segfault on startup due to too many unicorns)"
# (note: use exact format of above merge message at least up to the comma -- bitbucket makes various parts into links.)
hg push # that's it -- bitbucket will figure out that this accepts the pull request, you don't need to do anything special.
```
If the user was working on a feature branch, it's a little more complicated. Here's what I did to accept a pull request on the "issue2812" branch.  I started in my clone of the master SCons repo, on the default branch. 


```txt
hg pull https://bitbucket.org/USER/scons # pulls all his branches -- probably could have just pulled issue2812?
hg heads # see what we got
hg merge issue2812 # merge in his branch
# run tests, make any other needed changes here
hg push --new-branch -b default # --new-branch needed here because this push creates issue2812 branch in master repo
# now close the branch:
hg update issue2812
hg ci -m'Closed branch issue2812' --close-branch
hg up default
hg merge issue2812
hg commit -m'Closed branch issue2812'
hg push
```
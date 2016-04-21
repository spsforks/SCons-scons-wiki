

# Notes for Steven

Hi, 

Just a quick note.  As expected, my outbound mail doesn't work, although I have the name of an IT guy who may be able to fix that after I get back from ICU.  They don't get much demand for a submit server; even saying "smart host" didn't get a response. 

Sorry about the bug party.  The procedure was delayed by an emergency preempting the Cath Lab, so I didn't even get started until after 14 o'clock.  Then it ran over two hours as they decided to take an extra long look at a couple of places.  I didn't even get to my room until after 17 o'clock and by the time I was settled in and attached to all the monitoring equipment it was too late. 

As for the schedule, I go in Thursday at 7 o'clock, give or take.  The procedure will take 4-6 hours (although they say four hours is pretty quick and over five is the norm).  Then I go to the ICU, probably for three or four days, then back to my room for about five days.  They tell me I won't remember much of my stay in the ICU as I'll be pretty doped up on meds.  In any event, I'll hope to be back in touch on Monday or Tuesday. 

I got your note about with_traceback() and I was wondering about multiple inheritance.  It could be a bit tricky, but the strict left-to-right depth-first search for attributes might make it feasible, but I haven't thought about it enough to be sure.  It would certainly take some experimentation.  Worth a shot, but if we can't do it, we can still change all of those that don't use with_traceback() and defer the rest for later. 

Sigh.  I see that Bill has screwed up the checkpoint branch and is trying to check in bug fixes to the trunk.  I don't know what part of "no bug fixes in 2.0" he can't understand, but I'll bet he hasn't even noticed that I reverted his patch.  It might be worth bringing branches/pending up to current and applying the patch there; we can pick it up from there later. 

In any event, I'd suggest that we release 2.0 with a "not recommended to install as 2.0.1 will be out in a couple of weeks" note (and not broadcast it widely), then prep and release 2.0.1 with the same fixes as in 1.3.1 (and any subsequents).  I'd suggest releasing 2.0.1 on an expedited schedule: apply the accumulated patches and issue a release candidate immediately after 2.0, then the actual release in a week.  (I'm beginning to think that Python got the release names right (x.y.z.[abcf].p) and that we should think about transitioning to that model.  Maybe 2.0 could also be called 2.0.0.final.0 and we use that scheme henceforth?) 
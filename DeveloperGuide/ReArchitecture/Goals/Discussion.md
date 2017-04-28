A page for issues that are under discussion or are unfinished enough that they need some additional thought and critique before they become a "settled" part of the design. 

This page exists primiarily so we can go back-and-forth on certain contentious topics without interrupting the overall flow of the other documents.  Issues under discussion should have a section here, and the other document should have an appropriate link to the section here as an indication that there's an item under discussion. 

[TOC]

<a name="CPPPATH"></a> 
## O(1) CPPPATH

SK is proposing adding the following as a goal: 

   * Strive for `O(1)` performance on searches of long lists of directories like `$CPPPATH`.  Fallback:  Scale to implicit dependency searches in long directory lists without severe performance degradation.  DISCUSSION:  This must be subject to measurement.  Current builds with long `$CPPPATH` or `$LIBPATH` lists have horrible performance, but it's not clear how much is due to the search vs. the string expansion.  We could achieve `O(1)` searches by having a `PathList` object (or similar) collapse entries into a single dict, but the overhead might outweigh the benefit.  ((JGN: see [1]))) 

[1] (((JGN: Let me try to explain my concern about this scheme.  It has to do with #includes of the form `'dir/file.h'`.  When you are creating this O(1) dict, how deep do you go with the names to be searched?  If you want to look up `'dir/file.h'`, do you use the full name?  Or do you use just `'dir'` and follow the directory chain from there?  If you plan to populate the dict with all possible names in advance, you run the risk of being given something like `/usr/include` with its many hundreds of files.  If you try to fill the dict on demand, you'll want negative caching (_i.e._, remembering which names are <ins>not</ins> in the cache), but then you run afoul of a subsequent operation adding the name to a directory in the path (or worse, a subdirectory of a directory in the path), which you have to figure out how to keep in sync, and probably flush the cache if that happens.  In other words, I see a <ins>lot</ins> of complexity, costing a great deal of setup and overhead that has to be amortized over many calls.  Let me be clear: I'm not saying not to try this, but I see many other things that will probably give more bang for the buck, and you should be very clear on exactly what you want to do <ins>before</ins> you start coding.))) 

(((JGN: I'll also point out that this should <ins>not</ins> be construed as opposition to a per-directory O(1) cache of the names in it.  I think that's a fine idea.  There will have to be some care to keep it synchronized with the actual directory (and there are some other issues to hash out about it, such as whether not-yet-created names live in it), but that's a lot simpler and should be feasible.)))
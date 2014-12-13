
[[!toc ]] 
## Where's the other half?


### Greg Noel

Containers have the property that sometimes they are treated as opaque entities and yet at other times access must be given to their contents.  There are two parts to this problem: Containers that are actually directories and containers that are actually files.  The former is pretty well articulated and some examples (bundles and frameworks) are provided; the latter is barely alluded in the opening paragraph and then ignored.  Probably the most familiar example of a container file is a library, which itself is no more than a special kind of archive.  I believe a solution should address both. 

This suggests that the Container semantics should be able to identify whether it was being accessed as a unit (_e.g._, a copy of a container should copy the its contents intact) or only for one of its contents (_e.g._, a header file in a bundle or a member of an archive).  In turn, this leads to the question of how the container element should be specified; for consistency, I'd suggest using the filesystem separator (rather than specialized syntax such as placing the member name in parentheses, as is done by make). 


### Cem Karan

You're right that both files-as-containers and directories-as-containers need to be addressed, but I don't think a filesystem-like separator is a good idea.  The problem is that if we're also trying to access the contents of file-containers, those containers may have a use for the particular character we're using already.  We could go with an escape mechanism, but that also concerns me.  I think a more general approach would be a list of strings, which, when concatenated together, form the path to the object in question.  This would allow the Container to do any type of necessary concatenation work, including handing off a substring to a sub-Container of a different type (e.g., a tar container uses a different separator mechanism from a Mach-o or ELF container does, but this doesn't matter at the top level) 


## Name


### Greg Noel

Another possible name is "aggregate" which avoids some semantic baggage that "container" might bring along.  It's certainly better than "blob" (which I used because I wasn't fond of "container" and was clearly such a bad choice that it would have to be replaced). 


### Cem Karan

Agreed.  I'll make the change. 


## Subclassing v. delegation


### Greg Noel

Although I'm inclined to agree that delegation is the better model, SCons now mostly uses subclassing as it's more efficient in time and space.  There will probably need to be a side-by-side comparision.  But before that is done, we'll need a better description of the semantics that must be provided. 


### Cem Karan

I'll try to make a list of what I think needs to be put in place as a straw man based on what you mention below. 


## Semantics to be provided


### Greg Noel

Many of the issues seem to collapse to providing signatures of either the container or the member, with the side questions of when or where the member might need to be instantiated (a "read handle" if you will) or overwritten (a "write handle").  And then there's mediating access to members.  Some of this is already done by the Entity class; exploring that might give some insight. 

* Unit 
   * Signature 
   * Copy handle 
   * Write handle 
* Member 
   * Signature 
   * Read handle 
   * Write handle 

### Cem Karan

I just grabbed the latest sources from CVS and didn't see the Entity class in there (grepped for it too).  Can you tell me where to find it? 

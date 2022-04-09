
 _ | _
:--|:--
SEP | 0001
Title | Aggregates Extension
Author | Cem Karan
Status | Draft
Post History| http://scons.tigris.org/ds/viewMessage.do?dsMessageId=2366897&dsForumId=1272
Tracking issue | [#2536](/scons/issues/2536)

Please use the ["Discussion" page](ContainersDiscussion) for discussions about how this SEP should evolve.

After discussing this privately with Greg Noel, I've realized that my original hierarchy of how to handle all kinds of aggregates was needlessly complicated.  Greg suggested that there be some kind of Blob class, with default semantics that can be easily overridden somehow.  The version of the page you see here is due directly to his influence.

## Background

SCons is an excellent tool for building opaque objects, but not so great for building aggregates objects.  A library, media container, object file, etc. are simply opaque things that are created by tools driven by SCons.  Unfortunately, we've reached the point where certain types of aggregates need to be handled by SCons as a part of the build process.  As an example, on OS X, groupings of code and associated resources are stored in specially formatted directories called bundles.  A subclass of this are frameworks, which act like somewhat more intelligent dynamic libraries.  Because these are simply specially formatted directories, any tool can create them (you can create them by hand, if you wish).  This presents both problems and opportunities for SCons; problems, because rebuilding one part of the directory may require modifying other parts as well, opportunities because solving this problem correctly could lead to SCons having the ability to generate installers for all supported platforms, as well as creating bundles/frameworks for OS X.

## Use cases

### Bundles And Frameworks
The main use case I have in mind is for bundles and frameworks under OS X.  The generic problem is that directories don't have the right semantics when building and maintaining such composite objects.

#### Bundles
Bundles are specially formatted directories that are presented to the end user as flat files.  They have an XML file that stores metadata about the bundle, along with various resources (pictures, sound, code, etc.).  There is no single tool that creates bundles; once you're below a particular level in the directory structure, it becomes extremely fluid as to what is in the bundle, and where it happens to be.  For certain kinds of resources, it is even possible to add more resources to the bundle after the bundle has been created (such as localization resources, which will be discovered the next time the bundle is used).  The big reason why this is all so important is because all OS X applications are actually a specialized form of bundle; thus, if anyone wants to use SCons to build full-fledged OS X applications using SCons, it needs to be able to generate bundles.

The Apple developer pages have a [guide for creating and using bundles](https://developer.apple.com/documentation/CoreFoundation/Conceptual/CFBundles/Introduction/Introduction.html).

#### Frameworks
Frameworks are another specialization of bundles, but are more akin to DLLs; the reason that they are stored as bundles is because that allows them to carry their header files and all other resources along in one blob.  It also makes versioning extremely simple; if you make a new version of your code that is not binary compatible with the old version, you can generate a single framework that has both versions of the code within it.  Any application that relies on your framework can ask for whichever version of the library it wants to use.

The Apple developer pages have a [guide to creating and using frameworks](https://developer.apple.com/documentation/MacOSX/Conceptual/BPFrameworks/Frameworks.html);
one chapter gives the [full anatomy](https://developer.apple.com/documentation/MacOSX/Conceptual/BPFrameworks/Concepts/FrameworkAnatomy.html).

#### Discussion
The reason all of this works is because directories can have relative symlinks, and because of the metadata in the XML file within the bundle.  Without these pieces, bundles don't work.

Unfortunately, SCons' current behavior doesn't treat a directory as a target very well; it won't handle updating the XML file, and it won't handle merging old code and new code into a new framework correctly (only certain updates require a new version within the framework, and SCons can't decide which ones on its own).  It's likely this proposal could be extended only slightly to provide extensible semantics for directories, in which case bundles and frameworks would be simple specializations.

### Image Files and Install Files

Another potentially useful application of a container is to build and maintain something like an image file; e.g., a Red Hat RPM file,  a Microsoft installer file, or a Macintosh Installer file.  These files are highly specialized containers that are normally part of the build cycle, although generally a last step of the build cycle.  Being able to make and maintain these types of files would be very useful.

## Problems

In private discussions with Greg Noel, he pointed out that my original hierarchy of how to handle the situation (which was a hierarchy of different container types) was too complicated, that a better solution would be to have a generic Blob class.  For the simple reason that I have fat fingers, and will inevitably type Glob when I mean Blob, I'm going to suggest that this new class be called Aggregate instead. ;)

The Aggregate class will need to solve the following:

 * Providing access to different parts of the aggregate in a uniform manner.
 * Deciding if an aggregate needs updating.
 * Deciding which part of the aggregate needs updating.
 * Deciding how to ''efficiently'' update the aggregate.
 * Others?  I know that I'm missing a bunch here, can someone fill this in?

## Possible solutions

I see two possible solutions:

 * Generic Aggregate class, which is subclassed for specific purposes.
 * Concrete Aggregate class, which uses delegates (see [Delegation pattern](https://en.wikipedia.org/wiki/Delegate_method) for more information) to figure out what needs to be done, and how to do it.

There are advantages and disadvantages to both methods.  Most people know what subclassing is, so they'll be very familiar with it.  The problem is naming conflicts; without very careful adherence to naming conventions, at some point we're going to make a mistake that no-one is going to be happy with.  Delegation is cleaner in this respect.  The other big win for delegates is that since they are completely separate from the rest of SCons, they can be unit tested on their own.  This isn't possible with subclassing.

The next question is how to define the delegates.  The simplest way is to define them within the SConstruct/SConscript files, but might be better to have a function that allows you to specify where a delegate is in relation to the SConstruct/SConscript file.  Again, this allows the delegate to be unit tested without involving the rest of the build system (this can be handy if you have a large build team, and don't want to break what others are doing, etc.)


[Discussion](ContainersDiscussion)

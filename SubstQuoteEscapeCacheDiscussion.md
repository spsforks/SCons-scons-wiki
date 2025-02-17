
# One Lexer or Multiple?


## Greg Noel

I believe there should be a single lexer that's approximately the most-common denominator of the lexers found in shells.  It should recognize only these pieces: 

* Whitespace 
* Words (_i.e._, characters surrounded by other tokens, such as whitespace) 
* Text in single quotes (potentially including double quotes) 
* Text in double quotes (potentially including single quotes) 
* The dollar-dollar sequence as an escape for a single dollar 
* Substitutions (simplistically, `<token>$VAR<token>` or `<token>${...}<token>`) 
* (I can't think of anything else, but I reserve the right to add some later) 
Any additional quoting recognized by the subject shell is passed along as (part of) an uninterpreted word. 

This has the advantage that the input is interpreted identically across all platforms.  It can be documented in detail. 

If there are multiple lexers, it's not possible to determine the lexer at initialization and always use it, as this would not work for cross-platform builds, where one lexer would need to be used for the host platform and one for the build platform.  There would have to be a way to specify different lexers in different contexts (based on the Environment?).  I believe this introduces unnecessary complexity. 


## Jim Randall

That seems reasonable to me.  As long as it actually works, and the things that are quoted at the top level end up effectively quoted at the end in a target appropriate manner.  I do really like that it gives a platform independant view of the world. 

Part of my previous defense of platform specific lexing was that it would at least match what platform-specific tools would expect.   As well, it's was also partially a counsel of despair, as it's hard to imagine a platform independant solution that didn't involve a massive rewrite of the existing macro code.   If such a massive rewrite is on the table, however, then great! 

Either route would be better than the current situation!   As much as I hate spaces in filenames, I appear to be stuck with them for the moment. 

<a name="NewDirection"></a> 
# A Radical New Direction?


## Steven Knight

My initial reaction is that although this is well-thought-out, it's also complex.  It's probably as simple as it can be for something that's trying to maintain all, or most, of the current semantics.  But I think that indicates the real problem. 

Step back a bit:  one of the many half-finished experiments I've tried over the years involved trying to rewrite the current `Subst.py` module along the lines of this design.  I actually took as my starting point the `Itpl` string interpolation module written years ago by Ka-Ping Yee: 

[http://lfw.org/python/Itpl20.py](http://lfw.org/python/Itpl20.py) 

Ping's module works similarly to (my take on) the gist of Greg's proposal, which is to tokenize the input and turn it into a pre-parsed series of typed pieces (in this case, `(type, value)` tuples).  So that's what I tried.  After first determining that `Itpl` wasn't going to do the job for us out of the box, I tried to rewrite it for SCons' semantics.  I ended up with types for `$$`, for `$(` and `$)`, for white space, for variable expansions, for arbitrary `${}` expressions, for callables, etc.  It looked like it was going to be somewhat faster than the current implementation, but...  it was still bloody complicated. 

As a corresponding data point, note that Ping's `Itpl` modules was proposed as the standard string interpolation module for Python ([PEP 215](http://www.python.org/dev/peps/pep-0215/)), but lost out to the current `string.Template` class, apparently in no small part because of the complexity. 

I think this indicates that if we're _really_ going to make significant progress on cleaning up the string substitution mess, it's not going to happen by just coming up with better ways to support everything we do now.  I think the problem is that the current mess of "just growed" semantics is too difficult to support really cleanly and efficiently. 

So...  I've started wondering:  can we do something _radically_ different and better by shedding a whole bunch of the current semantics?  And yes, we'd need to end up finding a new way to support the old interface (backwards compatibility blah blah blah), but we can find ways to make that work.  For the sake of argument, then, throw out _all_ the old assumptions.  What if we try to do something drastically simple, like throw out all of the special cases that make current substitution so complicated (and slow): 

* `$(` `$)` 
  * Find other ways to let people exclude parts of command lines? 
  * Maybe give them some completely different idiom for doing what they use `$(` `$)` for today?  Like a different way to specify build numbers. 
  * Probably just drop the `$(` and `$)` around things like `-I` options, since it's a clever optimization but not crucial. 
* Arbitrary Python expressions in `${}` 
  * This might be tough, because it's what we currently use to tack `-I` options onto the `CPPPATH` values (_e.g._) 
* Executing callables 
  * Would need to catalog what we use these for in our code and find other idioms 
* White space compression 
  * Right now, we take pains to compress white space for command-line signature calculation. 
  * This seems like another "clever" optimization that's technically correct but complicates the logic, and in a way that many users find counter-intuitive.  If they add a space to the command line, why _not_ recompile it because it's different?  That's a simpler, less ambiguous rule than, "When you change a command line, SCons may or may not choose to rebuild depending on whether it thinks the change is significant..." 
* Expand undefined variables as null strings 
  * See SK's discussion below in the context of possible use of the Py3K `string.Formatter` class 
  * This is the primary reason we didn't just use Python variable substitution originally:  `"%(CC)s -o %(TARGET)s %(CCFLAGS)s %(SOURCES)s" % env` generates a `KeyError` if (e.g.) `CCFLAGS` isn't defined in the environment. 
  * Requiring that variables be defined might be acceptable (some people already prefer it) and might allow us to use standard Python formatting (or nearly standard). 
* Others I'm forgetting about right now (it's late...)? 
If we unconstrain ourselves in this way, what would be the simplest possible canonical representation of variables that avoid getting into having to handle a lot of end cases? 

One possible example:  what if _all_ variables were internally represented as lists of atomic strings?  That is, we drop interpretation of quotes from the environment-substitution layer.  To the extent that we'd want make it convenient for users to be able to use quotes to group command-line arguments: 

`    $CC "arg with spaces"` 

The interpretation of the `"arg with spaces"` would be one-time input parsing. 

(((UPDATE:  No, I'm wrong here.  Greg points out below that this is specifiable with: 

`    ['$CC', 'arg with spaces']` 

I'm perfectly content saying that people must specify these as lists of separate arguments, not relying on quoting inside a string.))) 

Or maybe not, so far as the specifics go.  (Like I said, it's getting late, so I'm not feeling terribly coherent.)  My point is, can we simplify this to the point where we don't need type-specific behavior?  And if we did, can we still find ways to support all the necessary functionality that people need, even if it ends up looking rather different from what we currently have. 


## Greg Noel

Hmmm... 

I've never looked at Ka-Ping Yee's code before.  You've mentioned the name, but not exactly what he'd done.  Upon looking at PEP-215 and a preliminary scan of his code, you're right, there are strong similarities to what I'm proposing.  And, in fact, he goes a lot further in many areas.  I'm going to have to digest his code for a while and then see if I can sharpen the proposal. 

Yes, there's complexity, but less, I suspect, than the combined complexity of all the ad-hoc mechanisms we've been using to get the quoting right.  Rather than a fragile edifice of hacks distributed all over the code, I'd rather face up to the inherent complexity in one place and fix it once and for all. 

An aside: it's more than just a `(type, value)` tuple as the token.  Since it's what drives the restringing, it's probably more accurate to categorize it as a `(command, arg, ...)` tuple, where there may be zero or more arguments. 

I definitely want to expose some parts of the tokenization to take care of your `"arg with spaces"` point, but I don't have any good candidates (yet).  My working hypothesis is that we will tokenize a simple string, but we will assume that a list of strings has already been tokenized into components where the whitespace is significant.  That is,   
`    ['$CC', 'arg with spaces']`   
will be treated as you expect.  It seems to be easy to understand and pretty much in line with the way that strings and lists are used today. 

As for the meat of your commentary, going off on a radical new direction, if I had any ideas about simplifying the existing scheme, trust me, you'd have heard about them long since.  You're not old enough to remember the shell wars, when there were a dozen shells, all trying out different quoting rules.  Bourne settled the issue, with a shell that not only was describable as a language, but had ways of dealing with almost all substitution and quoting needs.  If you only look at the surface, substitution and quoting seems simple, but if you read the man page (and look at the implementation), it's <ins>complex</ins>, far more so than you'd think.  Let me go over these PEPs in more detail and see if they can help us. 

It's worth noting that `string.Formatter` (_i.e._, [PEP-3101](http://www.python.org/dev/peps/pep-3101/)) exposes an internal parse of the format string; exactly the kind of thing we'd like to be caching.  Maybe your "radical new direction" is something more like that.  If so, and you can match the surface syntax exactly, the heavy lifting for it is already in C, so it would be very fast.  It's officially a Py3K feature, but there appears to be a pure-Python implementation in the [Python sandbox](http://svn.python.org/view/sandbox/trunk/pep3101/) that could be backported as a compatibility module until our floor is Python 3.0 (or maybe 2.6?). 

Oh, I'll not mention backward compatibility until there's a lot more of a proposal on the table, but let's not forget that we'll have to consider it eventually. 


## Greg Noel

(later) 

After some research, it turns out that I was conflating <ins>three</ins> things, not two: 

* [PEP-215](http://www.python.org/dev/peps/pep-0215/) Ka-Ping Yee's original string interpolation proposal, which required syntax changes to the Python language.  It was rejected, and as far as I can tell from the public discussions on the mailing list, complexity of <ins>implementation</ins> was not much of an issue (complexity of <ins>use</ins> was, however, as it was implicitly invoked when it was stringified, in whatever environment it happened to be at the time). 
* [PEP-292](http://www.python.org/dev/peps/pep-0292/) Barry Warsaw's `string.Template` proposal, which was the one actually accepted.  It requires no syntax changes and is invoked by explicit string methods.  It was also simpler to parse, in that it only recognizes a simple name following the dollar sign (PEP-215 recognizes a syntactic _atom_, including subscripts and the like). 
* [PEP-3101](http://www.python.org/dev/peps/pep-3101/) Talin's `string.Formatter` proposal, which has been accepted as the eventual replacement for `%` formatting.  It's also invoked explicitly via string methods.  Moreover, parsing the string is dirt simple, as all substitutions must be bracketed. 
Based on this new understanding, I've revised my first response above.  And based on Ka-Ping's code, I've created a simple proof of concept that tokenizes strings and lists of strings.  It's inefficient, the output isn't correctly quoted (yet!), and expressions are not optimized, but the internal tokens are pretty close to what is described in the proposal. 

One note: Ka-Ping's code defers the recognition of a syntactic atom to the `tokenize` module.  To be precise, it grabs an internal variable from the module, one that is not part of the public API.  For a quick-and-dirty proof of concept, this is probably OK, but that's a rather expensive module to instantiate just for one variable.  If we use this approach, that variable and its value should be calculated as part of the interpolation module.  Fortunately, the definition of atom hasn't changed since at least 1.5.2, so it should be safe to reproduce. 


## Steven Knight

(later, 26 February 2009 ~09:15 PDT) 

Good points all, and I'm glad you've canvassed and have digested the prior art (more thoroughly than I have, certainly).  Some random thoughts: 

After five whole minutes or so of scanning the PEP, I like the look of `string.Formatter`.  The expansions within the `{}` look like they'd cover most of what we need if we get rid of arbitrary expression evaluation (replacing it with some other way to specify the functionality, of course).  If `string.Formatter` is the wave of the future, I'd be inclined to see if we can just make that how SCons handles string substitution, so that SCons string manipulation just looks like what people will come to learn as "normal" Python string manipulation once Py3K takes over the world.  Yeah, that's a mom-and-apple-pie sentiment and the devils here are in all of the details, but maybe there's a fruitful direction there. 

Note:  if we did try to use stock Py3K `string.Formatter` as the interface for SCons string substitution, the one gotcha I know about is handling undefined variables.  In fact, in the very earliest prototypes of SCons, I did try to use Python string formatting, so that a command string would have been specified and expanded using something like `"%(CC)s -o %(TARGET)s %(CCFLAGS)s %(SOURCE)s" % env`.  There were two mismatches: 

1. You didn't get recursive substitution; this was probably solvable with some code. 
1. You had to define _every_ expected variable or else you'd get `KeyError` exceptions.  I couldn't figure out how to hook the format operator so that you could interpolate a null string for an undefined variable.  (I've been waiting since then for someone to tell me about some way we could do that, some bit of Pythonic magic that I'm still unaware of, but no one ever has...)  At the time, it seemed that forcing definition of all variables was going to be just too darned annoying and make SCons unusable.  After all, Make does it that way, so the behavior is obviously what people would expect, right?.  But maybe it's worth questioning that assumption, too.  Using an undefined variable can be viewed as a lack of rigor in the build configuration, and in fact the whole reason the `AllowSubstExceptions()` interface was added was to give people a way to configure that they _wanted_ SCons to complain when they used an undefined variable.  Methinks now that if we had just bitten the bullet back then and required variables to be defined, there would have been some initial grumbling, everyone would have quickly gotten used to the requirement, and life would be a lot simpler today... 
Anyway, as long as we're going to try to open this can of worms (at least in the context of my "radical new proposal" idea), it's worth considering whether we can simplify the assumptions to the point of just using Py3K string formatting, especially since they seem to be making it more flexible.  Maybe a custom subclass of `string.Formatter` with a few tweaks for expresion evaluation gets us (most of the way) there? 


## Greg Noel

I believe that we need to solve the immediate problem in a more-or-less compatible way (fixing the quoting and escaping may cause some minor inconsistencies, but we can argue that the prior behavior was undefined and we're now defining it ;-) so anyone depending on the undefined behavior is just out of luck), so I'm dividing these comments into two parts: developing a compatible replacement and possible new directions. 


### Current compatibility

I've been working with some examples, and it turns out that putting quoted strings in brackets is not sufficient.  My thought was that a string would be parsed into a list and the list evaluated, but that doesn't carry all the semantics.  Let me try to explain it via an example:   
`    cd "dir with spaces" && command arg1 arg2`   
which would have been equivalent to   
`    ['cd', "dir with spaces", '&&', 'command'. 'arg1', 'arg2']` 

It turns out there's a distinction between "word" tokens and "quoted" tokens.  If we assume that all the strings in the list are treated as quoted, then `&&` would be escaped when it is formatted as a command line.  That would cause the command line to be   
`    cd "dir with spaces" "&&" $CC arg1 arg2`   
which is not the same meaning as the original. 

It gets messier when variables are interpolated in a word context verses a quoted context.  Note that   
`    $SOURCES`   
is not expanded the same as   
`    "$SOURCES"`   
in that the first produces a list of word tokens separated by whitespace (the words may be quoted or not depending on how they are expanded at lower levels) while the second produces one quoted token where the spaces in the expansion are significant. 

I'm still trying to work out a rational set of rules for combining these two modes, but I think I'm getting closer. 


### Radical new direction

One aspect of the can of worms is that expansion will almost certainly require the same distinction between word and quoted interpolations as discussed in the previous section.  That may be possible with a pre-pass to cut the string into quoted and unquoted regions (I'm probably going to do exactly that for the current scheme). 

That said, recursive substitution should be a slam dunk.  There's a specific callback when it wants a variable, so the callback could easily interpolate the variable before returning it. 

Similarly, the same callback could catch an undefined variable and return a null string.  Pretty trivial. 

In any event, if you want to start a page to discuss it (if [RadicalNewInterpolation](RadicalNewInterpolation) suddenly becomes a working link, I'll assume that's it) I'll be glad to contribute.  I don't think there's any hurry, but it would be interesting to mock up a proof of concept (but not until <ins>after</ins> SCons 2.0 is out!). 

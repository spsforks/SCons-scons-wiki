
This is an attempt to understand (and possibly partially untangle) the issues surrounding variable expansion, quoting (of input regions), escaping (of output regions), and caching of environment variables.  Just to be perverse, I'm throwing in semantics for environment variables. 

The original draft is by [Greg Noel](GregNoel), who is the first person in the text. 

I'm maintaining this page elsewhere and sporadically copying it here.  If you have something to say and absolutely must get it in the wiki, please use the [discussion page](SubstQuoteEscapeCache/Discussion). 

xxx Needs to be reorganized; uses of concepts often preceeds their definition and some concepts discussed in scattered places. 


# The Problems

These are issues facing us that keep resurfacing repeatedly in different guises: 

* Values with spaces are not handled correctly. 
   * Values cannot be readily specified as containing significant spaces. 
   * Values containing spaces are not always quoted correctly on command line. 
* Substitution performance sucks. 
* Some environment variables should always provide list-like semantics. 
* (((xxx add more?))) 
There are several aspects that seem to be deeply entwined: 

* **Interpolating** The process of evaluating a `$...` expression within a string and substituting the results of the specified calculation.  The interpolated content may be empty. 
* **Quoting** Identifying parts of a string as _literal_, where the content is to be passed through unchanged. 
* **Escaping**  Rewriting a value such that the semantic content is unchanged when processed by a downstream scanner.  It is likely that there will be different downstream scanners, so there will be multiple escape processors. 
* **Caching**  Minimizing the cost of a calculation by reusing a previously-calculated result when there would be no change. [[note]](SubstQuoteEscapeCache) 
* **Listifying** Really need a better term.  Automatically treating certain environment variables as list-like, _i.e._, as if they were automatically `CLVar`s.  In other words, the equivalent of `property()` for an attribute of an object. 
The desire is to untangle these concepts, make their implementations as independent of each other as possible, and try to speed things up in the process. 

Let's introduce some terminology: 

* **Interpolation depths** An interpolation may be _surface_ (no interpolations done), _shallow_ (one application of interpolation; some special interpolations are not done), _deep_ (recursive evaluation of shallow interpolations), or _bottom_ (all interpolations recursively evaluated). 
* **Token** Technically, a tuple with a _type_ and zero or more associated _values_.  The type has some semantic value.  In our case, one type could be _quoted_ and another type could be _expression_. 
* **Tokenize** Evaluate a string and convert it into a sequence of tokens.  In our context, the result is a surface interpolation. 
* **Whitespace** One or more spaces (or tabs or ...).  In general, consecutive whitespace may be compressed into a single space without loss of meaning.  Whitespace may or may not be a token type, depending on the design requirements. 
* **(((more?)))** 
<a name="cache_note"></a>[note] For us, the shallow interpolation is always safe to cache since it depends solely on the string itself; other interpolation types could also be cached if there is some way to invalidate them if the underlying values change.  It's unlikely that bottom interpolations could be made safe to cache in all cases. 


# The Design

Some general thoughts about an implementation.  Combines several ideas from others.  May even be feasible. 

Note that there is a commonality between the `newCLVar` type and substitution: both must parse a string to see where to break it (quoting) and both must be able to put the string back together on demand (escaping).  The substition processing must also interpolate the results of calculations, but we can save some logic if we can use common code for those aspects. 

On the other hand, the `newCLVar` is frequently examined and manipulated, while the caching/substitution processing will tend to accumulate a lot of values.  Although it's tempting to use the same implementation for both, it may be that separate implementations will make more sense, one optimized for speed and one for space.  Measurements are needed. 

The design is predicated around tokenizing strings.  Converting strings into tokens allows us to separate different types of processing, rather than having it widely scattered and interleaved with other code: Quoting can be concerned with quoting, interpolating with interpolating, and escaping with escaping. 


## Tokenizing

Tokenization breaks a string up into typed pieces.  In general, think `shlex` although it's probably too simple for our uses; maybe a true lexer is closer.  (I'll call it a lexer since my spelling corrector likes the word and doesn't like quoter.)  There may be several tokenizers, or tokenizers may be composed from smaller pieces.  It may be that the only significant difference is the quoting and a common tokenizer can use different lexers to break up the string. 

Tokens pulled out of the string may be of several different types.  Tokens may or may not be separated by whitespace, so the existence of whitespace is significant and we must retain it, so we have a distinct "token" type for it.  Here are some of the types and questions about them: 

* Whitespace.  Adjacent whitespace tokens may be merged.  Leading and trailing whitespace is considered significant and produces a token. 
* An unquoted word.  Let's call it a _word_ token.  The content of word tokens is not escaped when prepared for use. 
* A quoted series of one or more characters.  Let's call it a _quoted_ token.  Is there a distinction between "abc" and 'abc' (_i.e._, are we expected to retain the type of quotes)?  The content of quoted tokens is escaped when prepared for use. 
* An expansion.  It starts with a dollar and continues to the next whitespace or dollar.  (Maybe other terminators?  What about `${...}.dir`?) 
   * Special-case expansions: `$TARGET(S)`, `$SOURCE(S)`, **...** 
   * Simple variable expansions: `$CC`, `$CCFLAGS`, `$XXX`, **...** [1] 
   * Special tokens for `$(` and `$)`?  Any other tokens like these?  Do they create a "container" token? 
   * Expressions: `${expr}` where `expr` is a Python expression. [2] 
   * Special tokens for `$XXX.dir` and the like? 
   * Probably others as well 
* A quoted expansion.  What to do with `"$var"` or `'$var'`?  Is it quoted or expansion?  If the latter, is the expansion considered quoted and not recursively tokenized? [3]  And what to do if `$var` is a list?  Is it one quoted value or a list of quoted values?  I can make a case for either. 
* A quoted composite.  What to do with "The value of CC is $CC"?  Messier than the previous one. [4] 
[1] While researching for this page, I found a <ins>lot</ins> of occurrences of `${VAR}`, particularly if `VAR` begins with an underscore.  They should be treated identically with `$VAR` since we can significantly optimize this case. 

[2] These may be further subdivided into "safe" expressions (evaluations of `_concat` or `_stripixes` for example) and "unsafe" expressions (everything else).  The idea is that safe expressions are ones that have no uncontrolled side-effects and the variables they use can be identified, so we can think about caching their results.  An alternative is to allow `$_func(args)` for cases like that so they can be optimized. 

[3] In the past, I've suggested `$"CC"` as a convention to say that `CC` should be expanded and the result quoted, so if `CC` is `"/My Programs/cl"` the space(s) would be retained correctly.  In other words, the referenced variable (`env['CC']` in this case) is treated as a quoted composite.  Otherwise, we need to recognize a quoted expansion of a single variable as a special case of a quoted composite and process it as described here. 

[4] I've wondered if a quoted composite should be a container type with a list of quoted tokens and epression tokens.  It takes some of the lexer complexity and moves it to the escape processing, but it retains the semantics that it was all quoted. 

A list of strings is tokenized by tokenizing the strings and separating them with a whitespace token. 

To be perfectly safe, an old `CLVar` should be stringified and the string tokenized.  Consider the `CLVar` containing `['-m"A', 'log', 'message"']` which would otherwise fail. 

A `newCLVar` is already quoted, so it's just a matter of transcribing the pieces separated by a whitespace token. 

Anything else should be stringified and made a quoted token (_i.e._, not evaluated further). 


## Interpolating

Substitution takes an expansion token and evaluates it, producing a list of tokens.  If this is a deep substitution, any expansion tokens in the returned list are evaluated recursively. 

xxx more to say here, but that outlines what it does. 

xxx maybe some examples to make it more intuitive?  These are to give flavor, not cast in concrete, and not a complete set. 


### Whitespace

Example: `('whitespace',)` 

Whitespace is compressible (as opposed to literal spaces, which are quoted tokens), so adjacent whitespace tokens produce only one space.  It has no additional information, just the indication of the existance. 


### Word

Example: `('word', "text")` 

A word is just that, an unquoted bit of text, usually surrounded by spaces. 


### Environment variable reference

Example: `('indirect', "key")` 

Contains the key of the variable that is to be interpolated. 


### Special variable reference

Example: `('special', "TARGET")` 

Evaluated every time it's encountered. 


### Inline expression

Example: `('func', refs, value, callable)`   
where `refs` is `('INCPREFIX', 'CPPPATH', 'INCSUFFIX')`   
and `value` is `None`   
and `callable` is a wrapper for `_concat()` 

Despite calling it an inline expression, perhaps it's more accurate to call it an inline cache.  It's used for any expression that can be completely understood by the lexer.  The _refs_ is a list (tuple?) of keys to variables that are used in the expression, the _value_ is the expanded value (or `None` if it needs to be evaluated), and the _callable_ is what will calculate the value (a bound function or a class with a `__call__()` method). 

The idea is that if the value is not `None` and the refs are all unchanged, the value can be used as-is.  Otherwise, the callable is run to get the value, which is tokenized and saved for the next time.  (((It might be simpler if we require that the `callable` return a token list.))) 


### Unsafe expression

Example: `('unsafe', "OPT and '-O' or ''")`   
Example: `('unsafe', "_concat(PRE.strip() + '=', LIST, '', __env__)")` 

An expression that cannot be inlined (_i.e._, cached) and must be evaluated every time it is interpolated.  It's only considered unsafe because the lexer cannot does not understand it completely, so it's possible that today's unsafe expression will become tomorrow's inline expression. 


### Container expressions

Example: `('nonsig', tokenlist)`   
where `tokenlist` is a list of tokens. 

The `nonsig` token captures the semantics of `$( ... $)`, and normally just causes the `tokenlist` to be recursively expanded.  If the expression is being evaluated for a signature, however, it is ignored. 


### Lots more TBD

xxx to be continued 


## Escaping

An escape processor converts a token list into a result to pass to some other scanner.  I'd imagine that there could be a number of different processors, each tailored for a specific type of downstream receiver.  Here are some possibilities: 

* A debugging processor, creates pretty-print, useful for developers. 
* A `newCLVar` processor, does no interpolation, so reproduces surface. 
* A `subprocess` processor, creates a list of strings. 
* A `signature` processor, creates MD5 hash of expanded command line. 
* A `unix` processsor, creates a U<small>NIX</small>-like command line, for display or to pass to a shell. 
* An "echo" processor for printing, like U<small>NIX</small> `echo` command, for `*COMSTR` or equivalent. 
* And lots more... 
Escaping a list of tokens requires examining each token and doing something with it: 

* Consecutive whitespace tokens cause one space to be emitted. 
* A word token is simply copied. 
* A quoted token is processed to see what kind of quoting is required. [1] 
* Expansion tokens are simply copied (or maybe we allow an option for delayed evaluation? hmmm...). 
* And reasonable things for other token types. 
[1] For example, in a U<small>NIX</small>-like system, the token is scanned[2].  If there are no characters requiring quoting, simply copy the token.  If there's no single quote in the token, copy the token surrounded by single quotes.  If there's no double quote in the token, copy the token surrounded by double quotes.  Otherwise, copy the token character-by-character and put a backslash in front of each token requiring quoting. 

[2] All three scans can be done simultaneously in a single `translate()` operation, which is quite efficient. 


## Caching

xxx I had originally considered caching expressions (or expression-like tokens), but I don't think that will work.  References to caching expressions should be converted into how to inline them, instead. 

A cache object (used loosely, implementing it as a tuple or dict might have speed advantages) has these contents: 

* A copy of the text or list being cached (or a hash?) 
* A shallow interpolation.  This can always be cached, since it depends solely on the content of the variable being cached. 
* (Maybe) A "dirty" flag, see below. 
We define these operations on the cache entry: 

* Is-up-to-date-p: Check to see if the source matches the cached source.  If this operation is evaluated a lot and is not trivially cheap, consider a "dirty" flag in the object to cache the results of the test. 
* Crack: Update the cached source and lex it to produce the shallow interpolation. 

# The Implementation

Strategy xxx: 

* Whenever posible, spend time in the lexer to make other operations faster, since we know that can be cached safely. 
* Initially cache only surface interpolation (lexer output).  Write an escape processor that does bottom interpolation and see how fast it can be made.  If that's "fast enough," don't bother with anything else. 
xxx 


## Variables as list-like objects

xxx `env.__setitem__()` is a critical path; it can't be made much longer.  Adding a logic to see if an existing key is a `newCLVar` (or an old `CLVar`?) would make it substantially slower.  We need a hack.  I wonder if turning `_dict` into an object so that we could use `property()` on it would be faster (_i.e._, store the value as an attribute of an object rather than as an item of a dict).  Measure, measure, measure... 

xxx `newCLVar` uses escape processor for stringifying that reproduces surface text. 

The API requires some way of setting up a `newCLVar` object as an Environment item.  (It's not obvious to me that a `newCLVar` item ever needs to be created as a standalone object, so the moral equivalent of `env.CLVar(`_key_`)` may be all that is needed.) 


## Substitution processing

Substitution processing keeps a cache in SubstitutionEnvironment.  This cache is keyed by the same values as the Environment items.  That is, if `env['CC']` is expanded, the result is cached with a key of `'CC'`. 

The cache entry is quite simple; it contains a copy of the Environment item (to see if the value is changed) and a shallow interpolation (a list of tokens which is based solely on the item's value, so it can be safely cached).  As such, using an object may be overkill; a two-element list may be cheaper and faster than using an object, but some measurements should be made to confirm that.  (Also should try with a dict.) 

The API requires some way of tokenizing a value, some way of caching a value based on its key, and some way of evaluating the tokenized value. 


## API

xxx API, try not to overlap with existing names. 

xxx API `crack(`_value_`)` tokenizes value, returns list of tokens. 

xxx API `eval(`_key_`)` caches list of tokens, uses `crack()` to tokenize key's value, returns list of tokens. 

xxx API an ABC for escape processors, with methods that can be overridden? 

xxx API backward compatibility `subst(string)` runs `crack()` then uses escape processor to put it back together. 

xxx API backward compatibility `subst_once(xxx)` maybe just run `crack()` in env being wrapped?  hmmm... 


# Notes

* Should the lexer be platform-specific?  On the one hand, the input strings entered by the user would be familiar, but on the other hand, the same string could be interpreted different ways on different platforms.  I think it was Jim who prefers the former, while I'd prefer implementing a generic lexer that was always the same and documenting it.  [Discussion](SubstQuoteEscapeCache/Discussion) 

# Doodling

A class that expands a token list.  Not terribly efficient.

```
#!python

    class Interp:   
        def __init__(self, env, special):   
            self.env = env   
            self.special = special   
        def calc(self, l):   
            self.buf = []   
            self.interp(l)   
            return ''.join(self.buf)   
        def interp(self, l):   
            for token in l:   
                self.do_[token[0]](self, token)   
        def do_whitespace(self, t):   
            buf = self.buf   
            if len(buf) and buf[-1][-1] != ' ':   
                buf.append(' ')   
        def do_word(self, t):   
            self.buf.append(t[1])   
        def do_nosig(self, t):   
            self.interp(t[1])   
        def do_sig(self, t):   
            pass   
        def do_indir(self, t):   
            self.interp(self.env[t[1]])   
        def do_special(self, t):   
            self.buf.append(self.special[t[1]])   
        def do_concat(self, t):   
            pre = self.env[t[1]]   
            post = self.env[t[3]]   
            first = True   
            for mid in self.env[t[2]]:   
                if first: first = False   
                else:     self.do_whitespace(())   
                self.interp(pre)   
                self.buf.append(mid)   
                self.interp(post)   
    # set up transfer table   
    Interp.do_ = {}   
    for f in dir(Interp):   
        if f.startswith('do_') and f != 'do_':   
            Interp.do_[f[3:]] = getattr(Interp, f) 

```


Some tests: 

```
#!python
 
    env = {}   
    special = {}   
    interp = Interp(env, special)   
    print 'null', interp.calc([   
        ])   
    print 'simple', interp.calc([   
            ('word', 'token'),   
        ])   
    print 'adj', interp.calc([   
            ('word', 'adjacent'),   
            ('word', 'tokens'),   
        ])   
    print 'sep', interp.calc([   
            ('word', 'whitespace-separated'),   
            ('whitespace',),   
            ('word', 'tokens'),   
        ])   
    for tt in ['nosig', 'sig']:   
        # identical except for sig/nosig token   
        print tt, interp.calc([   
                ('word', 'a'),   
                ('whitespace',),   
                ('word', 'line'),   
                ('whitespace',),   
                (tt, [   
                    ('word', 'not'),   
                ]),   
                ('whitespace',),   
                ('word', 'for'),   
                ('whitespace',),   
                ('word', 'sig'),   
            ])   
    #   
    env['CC'] = [('word', 'gcc')]   
    env['SHCC'] = [('indir', 'CC')]   
    env['PREFIX'] = [('word', '-l')]   
    env['LIST'] = ['m', 'c']   
    env['SUFFIX'] = []   
    special['TARGET'] = 'prog'   
    special['SOURCE'] = 'prog.c'   
    print 'compile', interp.calc([   
            ('indir', "SHCC"),   
            ('whitespace',),   
            ('word', '-o'),   
            ('whitespace',),   
            ('special', "TARGET"),   
            ('whitespace',),   
            ('word', '-O'),   
            ('whitespace',),   
            ('special', "SOURCE"),   
            ('whitespace',),   
            ('concat', "PREFIX", "LIST", "SUFFIX"),   
        ]) 

```

# Incorporate later

Is `${VAR}` significantly more expensive than `$VAR`?  If so, we can start with some simple performance improvements there and see what it gets us. 

Compile expressions as a part of lexing and save code so don't have to reparse. 

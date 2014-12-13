

# Preparing Program Sources

For the programmer, changes to source code fall into two categories. First, you have to make the localization functions known to all modules needing message translation. Second, you should identify, adjust and mark all constant strings in your program needing translation. 


## Importing

At the top of modules that have strings to be translated, have the following import: 


```txt
from SCons.i18n import _
```

## Preparing Strings

Before strings can be marked for translations, they sometimes need to be adjusted. Usually preparing a string for translation is done right before marking it, during the marking phase which is described in the next sections. What you have to keep in mind while doing that is the following. 

* Decent English style. 
* Entire sentences. 
* Split at paragraphs. 
* Use format strings instead of string concatenation. 
* Avoid unusual markup and unusual control characters. 
Let's look at some examples of these guidelines. 

Translatable strings should be in good English style. If slang language with abbreviations and shortcuts is used, often translators will not understand the message and will produce very inappropriate translations. 


```txt
"%s: is parameter\n"
```
This is nearly untranslatable: Is the displayed item a parameter or the parameter? 


```txt
"No match"
```
The ambiguity in this message makes it unintelligible: Is the program attempting to set something on fire? Does it mean "The given object does not match the template"? Does it mean "The template does not fit for any of the objects"? 

In both cases, adding more words to the message will help both the translator and the English speaking user. 

Translatable strings should be entire sentences. It is often not possible to translate single verbs or adjectives in a substitutable way. 


```txt
rw = "write" if rw else "read"
print "File %s is %s protected" % (filename, rw)
```
Most translators will not look at the source and will thus only see the string "File %s is %s protected", which is unintelligible. Change this to 


```txt
if rw:
    print "File %s is write protected" % filename
else:
    print "File %s is read protected" % filename
```
This way the translator will not only understand the message, she will also be able to find the appropriate grammatical construction. A French translator for example translates "write protected" like "protected against writing". 

Entire sentences are also important because in many languages, the declination of some word in a sentence depends on the gender or the number (singular/plural) of another part of the sentence. There are usually more interdependencies between words than in English. The consequence is that asking a translator to translate two half-sentences and then combining these two half-sentences through dumb string concatenation will not work, for many languages, even though it would work for English. That's why translators need to handle entire sentences. 

Often sentences don't fit into a single line. If a sentence is output using two subsequent printf statements, like this 


```txt
print "Locale charset \"%s\" is different from\n" % lcharset
print "input file charset \"%s\".\n" % fcharset
```
the translator would have to translate two half sentences, but nothing in the POT file would tell her that the two half sentences belong together. It is necessary to merge the two printf statements so that the translator can handle the entire sentence at once and decide at which place to insert a line break in the translation (if at all): 


```txt
print "Locale charset \"%s\" is different from\n\
input file charset \"%s\".\n" % (lcharset, fcharset)
```
You may now ask: how about two or more adjacent sentences? Like in this case: 


```txt
file.write("Apollo 13 scenario: Stack overflow handling failed.")
file.write("On the next stack overflow we will crash!!!")
```
Should these two statements merged into a single one? I would recommend to merge them if the two sentences are related to each other, because then it makes it easier for the translator to understand and translate both. On the other hand, if one of the two messages is a stereotypic one, occurring in other places as well, you will do a favour to the translator by not merging the two. (Identical messages occurring in several places are combined by pygettext, so the translator has to handle them once only.) 

Translatable strings should be limited to one paragraph; don't let a single message be longer than ten lines. The reason is that when the translatable string changes, the translator is faced with the task of updating the entire translated string. Maybe only a single word will have changed in the English string, but the translator doesn't see that (with the current translation tools), therefore she has to proofread the entire message. 

Hardcoded string concatenation is sometimes used to construct English strings: 


```txt
msg = "Replace " + object1 + " with " + object2 + "?"
```
In order to present to the translator only entire sentences, and also because in some languages the translator might want to swap the order of object1 and object2, it is necessary to change this to use a format string: 


```txt
print "Replace %{object1}s with %{objects2}s?" % {"object1":object1, "object2":object2}
```
Unusual markup or control characters should not be used in translatable strings. Translators will likely not understand the particular meaning of the markup or control characters. 

For example, if you have a convention that ‘|’ delimits the left-hand and right-hand part of some GUI elements, translators will often not understand it without specific comments. It might be better to have the translator translate the left-hand and right-hand part separately. 


## Mark Keywords

All strings requiring translation should be marked in the source code. Marking is done in such a way that each translatable string appears to be the sole argument of some function. There are only a few such possible functions meant for translation, and their names are said to be marking keywords. The marking is attached to strings themselves, rather than to what we do with them. 

This marking operation has two goals. The first goal of marking is for triggering the retrieval of the translation, at run time. The keyword is possibly resolved into a routine able to dynamically return the proper translation, as far as possible or wanted, for the argument string. Most localizable strings are found in executable positions, that is, attached to variables or given as parameters to functions. But this is not universal usage, and some translatable strings appear in structured initializations. See Special cases. 

The second goal of the marking operation is to help pygettext at properly extracting all translatable strings when it scans a set of program sources and produces PO file templates. 

The canonical keyword for marking translatable strings is ‘_’. Use ‘_’ (a simple underline) as a keyword, and write ‘_("Translatable string")’. Further, the coding rule, from GNU standards, wanting that there is a space between the keyword and the opening parenthesis is relaxed, in practice, for this particular usage. So, the textual overhead per translatable string is reduced to only three characters: the underline and the two parentheses. However, This isn't offered officially. 

The marking keywords ‘_’ take the translatable string as sole argument. 

Note also that long strings can be split across lines, into multiple adjacent string tokens. Automatic string concatenation is performed at compile time; pygettext also supports this syntax. 

Later on, the maintenance is relatively easy. If, as a programmer, you add or modify a string, you will have to ask yourself if the new or altered string requires translation, and include it within ‘_()’ if you think it should be translated. For example, ‘"%s"’ is an example of string not requiring translation. But ‘"%s: %d"’ does require translation, because in French, unlike in English, it's customary to put a space before a colon. 


## Marking


### String expansion and translations

_ method wraps the Python module gettext.gettext. 

You can use it like this: 


```txt
title = _("Title")
```
In cases where there is more than one variable, this allows translators to reorder the variables. 

Also, pass the expansion dict into gettext call. If there's a variable expansion error, then module will fall back to the English string. This prevents bad translations from preventing users from using SCons. 

BAD: 
```txt
title = _("Delete file %(filename)s?" % {"filename": self.filename})

title = _("Delete %(count)s file %(filename)s?" % {"count": count, "filename": self.filename})
```
BAD because it expands the variables before calling gettext: 

GOOD: 
```txt
title = _("Delete file %(filename)s?") % {"filename": self.filename}
```
-- 

BAD: 
```txt
title = _("Delete file %s?") % self.filename
```
BAD because it uses %s instead of something like %(filename)s and it doesn't pass in the expansion dict into gettext. 


### Long strings and translations

Long strings (description of things, ...) should be formatted like this: 
```txt
description = _(
    "This is a really long string that is formatted using explicit "
    "whitespace and explicit string delimiters.  It avoids whitespace "
    "problems that can't be seen (extra spaces, carriage returns, ... "
    "without causing parsing problems.\n"
    "\n"
    "You can do multiple paragraphs as well."
)
```
If you need to expand variables in the long string, use the Python string formatting syntax and a dict like this: 
```txt
description = _(
    "This is a long string that you find in %(shortappname)s that "
    "is translated.  Using Python string formatting syntax like this "
    "makes it easier for translators to understand what values are "
    "substituted in.  This paragraph has %(count)d two values.") %
    {"count": 2, "shortappname": "Miro"}
```

## Special cases

In most coding situations, strings are translated where they are coded. Occasionally however, you need to mark strings for translation, but defer actual translation until later. A classic example is: 


```txt
animals = ['mollusk',
           'albatross',
           'rat',
           'penguin',
           'python', ]
# ...
for a in animals:
    print a
```
Here, you want to mark the strings in the animals list as being translatable, but you don’t actually want to translate them until they are printed. 

Here is way you can handle this situation: 


```txt
animals = [N_('mollusk'),
           N_('albatross'),
           N_('rat'),
           N_('penguin'),
           N_('python'), ]

# ...
for a in animals:
    print _(a)
```

## References

[https://develop.participatoryculture.org/trac/democracy/wiki/LocalizedStringsGuide](https://develop.participatoryculture.org/trac/democracy/wiki/LocalizedStringsGuide) 

[http://docs.python.org/library/gettext.html](http://docs.python.org/library/gettext.html) 

[http://www.gnu.org/software/gettext/manual/gettext.html](http://www.gnu.org/software/gettext/manual/gettext.html) 

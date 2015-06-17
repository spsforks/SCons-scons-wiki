**Table of Contents**

[TOC]


## How to create po file?

The translator derives a .po file from the template using the msginit program, then fills out the translations. msginit initializes the translations so, for instance, if we wish to create a Turkish language translation, we'd run 


```txt
msginit --locale=tr --input=scons.pot
```

## How to translate strings?

A sample entry which is in po file would look like 


```txt
#: SConf.py:112
msgid "scons: Configure: creating %s"
msgstr ""
```
The translator will have to edit these, either by hand or with a translation tool like Poedit, or Emacs with its editing mode for .po files. When they are done, the entry will look like this: 


```txt
#: SConf.py:112
msgid "scons: Configure: creating %s"
msgstr "scons: Yapılandırma: %s oluşturuluyor"
```

## How to test translations?

The .po files are compiled into binary .mo files with msgfmt. 


```txt
msgfmt tr.po -o scons.mo
```
To test translated file, compile it into binary .mo and copy it to location which it should be in at system. (On unix-type systems, mo files should be in /usr/share/locale/{lang_code}/LC_MESSAGES or /usr/local/share/{lang_code}/LC_MESSAGES) When you run program, the program will display strings in system language, if there is an .mo file for it. 


## Tips for good translations

* Don't translate literally, translate organically 
  * Being bi- or multi-lingual, you undoubtedly know that the languages you speak have different structures, rhythms, tones, and inflections. Translated messages don't need to be structured the same way as the English ones: take the ideas that are presented and come up with a message that expresses the same thing in a natural way for the target language. It's the difference between creating an equal message and an equivalent message: don't replicate, replace. Even with more structural items in messages, you have creative license to adapt and change if you feel it will be more logical for, or better adapted to, your target audience. 
* Try to keep the same level of formality (or informality) 
  * Each message has a different level of formality or informality. Exactly what level of formality or informality to use for each message in your target language is something you'll have to figure out on your own (or with your team), but [WordPress](WordPress) messages (informational messages in particular) tend to have a politely informal tone in English. Try to accomplish the equivalent in the target language, within your cultural context. 
* Don't use slang or audience-specific terms 
  * Some amount of terminology is to be expected in a blog, but refrain from using colloquialisms that only the "in" crowd will get. If the uninitiated blogger were to install [WordPress](WordPress) in your language, would they know what the term means? Words like pingback, trackback, and feed are exceptions to this rule; they're terminology that are typically difficult to translate, and many translators choose to leave in English. 
* Read other software's localizations in your language 
  * If you get stuck or need direction, try reading through the translations of other popular software tools to get a feel for what terms are commonly used, how formality is addressed, etc. Of course, [WordPress](WordPress) has its own tone and feel, so keep that in mind when you're reading other localizations, but feel free to dig up UI terms and the like to maintain consistency with other software in your language. 

## Can I be a translator?

You need to be truly bilingual -- fluent in both written English and the language(s) you will be translating into. Casual knowledge of either one will make translating difficult for you, or make the localization you create confusing to native speakers. 

You need to be familiar with SCons and Python, as you will sometimes need to read through the SCons code to figure out the best way to translate messages. 


## References

[http://en.wikipedia.org/wiki/GNU_gettext](http://en.wikipedia.org/wiki/GNU_gettext) 

[http://codex.wordpress.org/Translating_WordPress](http://codex.wordpress.org/Translating_WordPress) 

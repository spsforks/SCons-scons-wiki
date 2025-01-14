

# Internationalization of SCons


### Contact Information
[[!table header="no" class="mointable" data="""
 Name  | Tuba Şahin 
 Email  | nestanka {at} gmail.com
 Timezone  | GMT+2 
 Place of Residence  | Mersin / Turkey 
IM  |  *XMPP: nestanka{at}gmail.com *IRC: [nestanka@irc.freenode.org](mailto:nestanka@irc.freenode.org) 
"""]]


## Abstract

SCons is widely used installation system by the programmers all over the world. The programmers usually know a second language especially english as it is universal. But SCons is not used only by the programmer. It is also used by the users. In addition to this, the users encounter with the messages of SCons more than the programmers. The users may not know english. For that reason, internationalization of scons will increase the usebility of SCons and will help it to spread larger area. 

With this project, I'll implement i18n support to SCons. So translators will be able to translate SCons their own languages easily and users will be able to use SCons with their system locale. Besides, i'll do first translation of SCons and translate it into my native language Turkish within my project. 


## Detailed Description


### Analysis

I think, the main expected results of i18n are creating translatable codes smoothly, translating string catalogs easily and providing multi-language translation infrastructure. Because of these expectations i'll use gettext library. 

Gettext is an easy-to-use l10n library. Developers can use gettext with a lot of programming languages and mark their messages with only a few extra characters. With these feature, gettext satisfies our first expectation. 

Gettext tools use simple text files as string catalog. So translators can translate string catalogs at various platforms easily (translators can use vi, kwrite, kbabel, various web systems etc.). With these feature, gettext satisfies our second expectation. 

Gettext use locale variables (from different sources) to specify user language and use catalog of this language. So no need extra effort for programmer for multi-language translation.  

Additionally, gettext is a widely used l10n library so most of programming language developers consider gettext. I don't think, new versions of programming languages will do big changes about usage of gettext and we will be able to adapt our codes to new versions easily. 

At start, all strings are needed marking with gettext marks. This is a demanding job at first time. But then if developers code with these marks, this job is simpliest part of localization. 

distutils library cant compile and install po files directly. So we have to add our own function to compile po files or add new dependencies (like van.potomo, babel etc.) for installation process. I think, writing our own functions is the simpliest way to compile po files.   

After coding jobs completed, documents are necessary. Documents should be clear and cover all message and string types and illustrate all possible situations for translators. 


### Backward Compatibility

If gettext library can not find the translated text it uses original text. Thus, I don't think that marking the messages with gettext will not create a problem about backward compatibility. 


### Special Techniques

I think Gettext library is suitable for all translation processes. 


### Plan


#### sample works in bonding period

I'll do sample works to illustrate what i will do within project, like modify a module, mark strings in this module and translate it. So we can realize our problems with my mentor and try to solve them before project time start. 


#### setting up the infrastructure to provide translations

I'll use gettext library. So gettext library should be imported all modules which will use translated texts. I'll add these imports and needed gettext variables to provide infrastracture that needed for marking messages. 


#### marking all the messages that needs to be translated

Some of strings doesn't need to be translated. Because some strings can not be seen by users or hardcoded variables about program. I'll find the strings that users encounter and need to be translate and mark them with gettext marks.   


#### writing tests for all i18n supported modules

After completed the marking of each module, I'll write unittest for module to check print outs and find out for possible errors or deficiencies. I'll use two different translation for testing. (Turkish translation and pseudo-translation) With Turkish translation, i can test a real situation and i can test possible extreme situations with the help pseudo-translation. 


#### translating SCons into Turkish

I'll translate SCons into my native language during my project. I'll translate each module after completed the marking strings and use this translation for testing.  


#### writing "how-to" documents about translation

I'll write two different document about i18n and l10n. 

One of them will be for developers. This documents will illustrate how to mark strings to make them translatable. This document will cover various string and message types like %-style strings, advanced string formatting, joined strings etc. 

And the other document will be for translators. This document will define and explain string catalog files and illustrate all posible situations like plural words, joined strings, strings including "%s" etc. 


#### modify setup script to install locale files

We have to add a function to setup script to compile po files as i mentioned in analysis section. This will be a simple function which uses msgfmt to compile po files. And after compile po files, we will be able to install them to locale folder like the other data files. 


#### fixing bugs from SCons issue list

I'll try to fix some bugs from SCons issue list. I will give priority to bug which related with my project if there any. Otherwise, I will be interested in "Clean up code and start using [PyChecker](PyChecker) (or similar tool)" #1970 bug firstly. 


##### Clean up code and start using PyChecker (or similar tool)

There is some tools and examples with [PyChecker](PyChecker) in issue tracker and svn. I'll check these and compare with other similar tools. I'll check code with selected tool and fix problems which tool reported. I didnt make a decision about details so i dont know time and process exactly but i think all job will take 1 or 2 week.  


## Scope of Work


### Deliverables

* Implement i18n Support 
* a. translatable modules (all modules will be translatable at the end of seventh week) 
* b. unittests for all modules (I'll write unittest of each module after completed the marking of each module) 
* c. fixed setup script to install locale files 
* Documents 
* a. How to mark strings which will be translated (For developers) (in eighth week) 
* b. How to translate SCons using translation files (For translators) (in nineth week) 
* Turkish translation of SCons (I'll translate each module into Turkish after completed the marking of each module) 
* Fixed bugs from SCons issue list 

### Schedule


#### Bonding period (20 April - 23 May)

I'll contact with my mentor about details of project and read documents of libraries which I'll use in project. I'll do a sample work in last week of bonding period. 


#### First week (23 May)

This week I have my final exams for that reason it may be diffucult for me to work. 


#### Second week (30 May)

I'll start to define the functions that print messages which users encounter and modify them relating to i18n if needed. Because of this week is my first week, different situations may slow me down. So I'll aim to complete half of this job in this week. 


#### Third week (6 June)

I'll define the functions that print messages which users encounter and modify them relating to i18n if needed. At the end of third week, i will have completed setting up the infrastructure to provide translations. 


#### Third week - Fifth week (13 June - 27 June)

I'll start marking strings. This job will continue ~2 weeks. For my skecthy count, there is ~200 python file in src folder except *Tests files. I plan to complete marking in two weeks. 


#### Fifth week - Seventh week (27 June - 18 July)

I'll start translating and testing. This job will continue ~2-3 weeks. For my skecthy count, there is ~200 python file in src folder except *Tests files. I plan to complete ~66 modules each week (~33% per week) 

I'll have completed ~33% of this job at midterm. 

I'll translate all marked strings into Turkish (and create a pseudo-translation) After translation completed, i'll check print outs of file with these two translation file. Since these two job are closely related, i have to do these jobs simultaneously. 


#### Seventh week (11 July)

I'll fix setup script to install locale files in this week after completed the other job. 


#### Eighth week (18 July)

I'll start writing how-to document for developers. 


#### Nineth week (25 July)

I'll complete developer document at this week. And I'll start writing how-to document for translators. I want documents to cover all situations. So i will check all string catalogs while writing developer document. And then I'll write explanations for all situations stated in developer document at translator document. 


#### Tenth week (1 August)

I'll complete translator document at tenth week. I'll start to work on bugs which mentioned plan section. If i complete those bugs, I'll check up-to-date issue list and try to fix bugs which i can solve. To fix the bug which mentioned in plan section will take ~1-2 weeks. 


#### Final (17 August)

I'll try to complete to fixing all bugs that i start to work on before final. 


## Availibility

There are my final exams between 18-29 May. This overlaps with first week of project timeline. And i help a project in my university voluntarily. I'll continue to help this project in summer. I am collecting data from web for this project so it doesn't effect my works so much as it is an easy job. Except these, i will be completely free for work all summer. 


## Biography

I use opensource softwares for about one year. And I contribute different opensource projects. Iam in Pardus Q&A team, and I translated some programs for KDE Turkey. I'm a student of English Linguistics Department in Mersin, Turkey. I am working for the Computational Linguistics in my university. I am programing with Python at intermediate level on linux. 

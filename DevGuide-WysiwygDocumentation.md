# WYSIWYG Editing for SCons Documentation


## Editing single chapters

The DocBook source files for the User Guide have been set up in a way, such that you can either load the whole document ("`main.xml`"), or a single chapter file like "`libraries.xml`" for example. 

The latter option is to be preferred, since it doesn't require as much CPU and memory for rendering the documents live. 


## Insertion of DTD entities

After adding a new Tool, Builder or something like this, you'll have to update the list of generated entities by calling 


```txt
  python bin/docs-update-generated.py
```
Only after this step will you be able to insert and use the newly added entities in all the single chapters and the global document "`main.xml`". 


## Configurations for visual editing

Configuration sets for two visual XML editors have been prepared. These are _**XmlMind_** and _**Syntext Serna**_, both offering good WYSIWYG like editing. Other, more text-oriented solutions like Editix or Quanta may be used with success too (check [the list of DocBook Authoring tools](http://wiki.docbook.org/topic/DocBookAuthoringTools) for an exhaustive list). 

Finally, I also found [Howto create a visual Docbook Editor in 10 Minutes](http://relation.to/Bloggers/HowToCreateAVisualDocBookEditorIn10Minutes), a short description about how to use the VPE/JBOSS plugin of Eclipse to preview XML documents. But I did not follow this route any further...any volunteers out there? 


### XMLMind editor
Homepage
: [https://www.xmlmind.com/xmleditor](https://www.xmlmind.com/xmleditor) 


Tested versions
: Professional Edition 5.8.1 

(current release is 9.5.0, it might be useful if someone tested a more recent version)

This editor comes also in a free version, containing all the basic features that you'll need for editing DocBook documents. Unfortunately, the Personal Edition doesn't support user-defined target namespaces. So you'll have to invest a few bucks, but it's definitely worth the money in my opinion. 

Copy the contents of the "`xmlmind`" folder in the archive to your user's XXE config directory. This is located at 

* "`$HOME/.xxe4/`" on Linux. 
* "`$HOME/Library/Application Support/XMLmind/XMLEditor4/`" on the Mac. 
* `%APPDATA%\XMLmind\XMLEditor4\` on Windows 2000, XP, Vista. 

for the versions of XXE with a major version number of 4. Later versions with a different major number use the same pattern, so for 9.x:

* "`$HOME/.xxe9/`" on Linux, 
* "`$HOME/Library/Application Support/XMLmind/XMLEditor9/`" on the Mac and 
* `%APPDATA%\XMLmind\XMLEditor9\` on Windows 2000, XP, Vista. 

After a restart of the program, the SCons DTD is picked up automatically, and you can even select it when inserting new Books, Articles,... whatever. 

![xmlmind Screenshot](https://github.com/SCons/scons/wiki/DeveloperGuide/WysiwygDocumentation/colortest.png)

### Syntext Serna Free
Homepage
: [https://github.com/pantonov/serna-free](https://github.com/pantonov/serna-free)

Tested version
: 4.4.0 


This is a good alternative to the [XmlMind](XmlMind) editor, however its "Insert tag" philosophy didn't convince me that much. But your mileage may vary... After Serna was bought by another company, the free version won't get developed any further unfortunately (and the free version doesn't really indicate a version any longer). But it's still okay for basic writing stuff as in the SCons docs, so give it a spin. 

Copy the prepared "`scons`" addon folder to the "`plugins`" directory of your _**Serna**_ installation. Depending on where and how you installed the program, you might need root access for this step. 


![Serna Screenshot](https://github.com/SCons/scons/wiki/DeveloperGuide/WysiwygDocumentation/serna3.png)

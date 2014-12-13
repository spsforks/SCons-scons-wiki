

### Create a CSV File for Uploading

* You'll need to have run a query at Issuezilla to get the issues you want to include in the spreadsheet.  The [BugParty](BugParty) page probably contains the query you want; if not, a wide range of queries can be constructed using the [BugScheduleMacro](BugScheduleMacro) or the (undocumented) TempBugHack macro (put the macro instantiation in a page to run it; it can be in a preview page if you don't plan to keep it).  If those don't cover it, you can [construct a query at Issuezilla](http://scons.tigris.org/issues/query.cgi) the hard way. 
* On the Issuezilla "Issue list" page that's the result of the query, select the "Format as XML" button. 
* On the "Format as XML" page, tick the "Download as file" radio button, change the filename if you wish, and select the "Generate XML" button to download the file to your computer. 
* On your computer, run `bin/xmlagenda.py` from the SCons distribution.  It has one optional parameter, the filename to be converted; the default is `issues.xml` if no parameter is present.  This will create `editlist.csv` in the current directory. 
* If you want to keep the CSV file, rename it or it will be overwritten the next time you do this.  It needs to end in `.csv` but otherwise there are no naming restrictions. 


# BugSchedule Macro

The `BugSchedule` macro is an extension to the SCons wiki.  It creates a link to the SCons issues database which will do a query for specific kinds of issues. 


## Usage

To use it, just put the macro in your wiki page with the parameters you want: 

`             <<BugSchedule(who, text)>>` 

It takes two arguments: 

* who
: Either a Tigris.org account name, `@ALL`, `@ALL=`_accountname_, `@TRIAGE`, or `@TRIAGE=`_milestone_.  If it is missing, `@ALL` is assumed 

text
: The text that will be highlighted for the link.  If it is missing, a best guess for some reasonable text is made. 



## Examples

# Python3 compatibility was added with SCons 3.0.0.
## Keeping below for historical reference.

Discussion of our transition from Python 2.x towards 3.x (via 2.7 preferrably). 


# Problems

...that we might encounter, or issues we have to care about. 


# Ideas

...for the basic workflow and implementation details 

It might make sense to select Python 3.3 (or higher) as target versions for the transition, because Unicode support (see next section) has reached a pretty mature state in it. 


# Unicode


## Resources

* Python2 Unicode HOWTO ( [http://docs.python.org/2/howto/unicode.html](http://docs.python.org/2/howto/unicode.html) ) 
* Python3 Unicode HOWTO ( [http://docs.python.org/py3k/howto/unicode.html](http://docs.python.org/py3k/howto/unicode.html) ) 

## Known issues

* unicode paths break SCons (#589) 
* [ListAction](ListAction) doesn't handle Unicode strings (#1098) 
* scons sometimes fails to run when windows keymap != ASCII (#1662) 
* SCons cannot work with files containing UTF-8 encoded Unicode (#2741) 
* printing of Value nodes while debugging the DAG (#2910) 

## Things to check

* Where do we write to or read from files? Ensure that these places get rewritten to use the functionality of the new io module. 
* Where is data printed to the screen? 
* Where are the types str and unicode explicitly used in the code? 
* Are there places where an implicit coercion between str and unicode might happen (in either direction)? Candidates for this are: the "+" operator, format specifiers in strings like "A string: %s" and the print() function in general. 
* Do we have places where we explicitly use encode() /decode()? 

## What the user needs

* support for encoding specifications within SConstruct/SConscript files (coding directive) and in scanned files as well 
* options to override and explicitly specify the input and/or output encoding to use 
* options to override the strategy for encoding errors (strict/replace/ignore) for input and output respectively 

# Internationalization/Localization

Should we care about this at the same time (during transformation 2.x to 3.x)? If yes, what is our plan for attack? 

Issue number in the bug tracker is #318, by the way. 

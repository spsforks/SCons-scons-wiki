
# Subst() rewrite proposal

This is a proposal for a rewrite of the Subst logic in SCons. 


## Current issues

Issues with the current engine include: 

1. The processing of {} symbols are not handled correctly. The engine incorrectly handle statements such as: 
```
"${Foo(${Boo})}"
```
1. Escape handling has issues. This might not be as simple to deal with, but the current logic is much worse than it should be. 
1. Non string types are not handled well. This is very much so for recursive substitution calls in which the escape handling gets invoked. For example: 

```
#!python 
env['FOO']=['Hello','world']
env['CPPDEFINES']"$FOO"
print env.subst("$_CPPDEFINES") 
 
```

we would like to see: 

```txt
/DHello /Dworld
 
```

but we get: 

```txt
/DHello world
```

Which is incorrect. In other cases depending how the substitute path is set you may get 

```txt
"/DHello world"
```

which is also incorrect 
4.Current api's like subst_list() don't work correctly or act in strange ways. For example the subst_list() api will always return a list with one list of items, not a list of items. (This is the difference of getting ["hello", "world"]("hello", "world") vs ["hello", "world"]) 

1. caching logic is not well defined. This leads to a lot of other code in SCons trying to cache certain values that it thinks should be ok to cache. This increases memory usage and makes it difficult to correct "clear" the cache or reevaluate when it might make sense to do so. 
1. There some internal cases in which the user can hit bugs in the subst() engine in which internal classes that should work in cases of "adding" two string objects with the "+" operator should work but don't for some reason, do a bug in [UserString](UserString) or the class the sub-classes from it. 
1. Certain action may be cumbersome to say in certain cases. For example: 

```
#!python 
env['Boo']="$somestuff"+env.Literal("${leave alone})+"$otherstuff"
```

it would be nice to be able to say in certain cases: 

```python
#!python 
env['Boo']="$somestuff${Literal('${leave alone}')}$otherstuff"
```

This allows a clearer understanding of what is needed that depending on special "hidden" string objects types that handle this, and might be corrupted with a str() call 

## Suggested improvements to the "string" grammar

To help improve the syntax used when defining what to substitute I suggest that we allow for this syntax: 
$$
: resolves to $ 

$var
: resolves the value of var 

${expression}
: evaluates the expression based on values defined the Environment object, or a dictionary object provided. If the value is a list or non string type the value will have a string conversion applied to it 

$( value $)
: 
allows the **value** to not be processed by the signature function. In our case this means a certain "raw" mode will process return this value differently 


${IGNORE('value')
: long form of the $( $) syntax 

${LITERAL('value')
: another way to say env.Literal('value'), but embedded in the string. 

${APPEND('expression')}
: evaluate the expression and returning a list of raw types (for example Node objects might be returned), appending the values to the parent container, given that it is not a string type(wording??) This allows for the expression to result in a list to be expanded in place correctly. For example: 

```
#!python 
env.Append(MYPATH=['path1', 'path2 with space'])
env.Replace(CPPPATH=['path0',"$[MYPATH]"])
```

would result in the expected 

```txt
/Ipath0 /Ipath1 /I"path2 with space"
```


not in the current 

```txt
/Ipath0 /Ipath1 path2 with spaces
```

${APPENDUNIQUE('expression',move=True)}, ${PREPENDUNIQUE('expression',move=True)}, ${PREPEND('expression')}
: Like append, but with the different logic. In the case unique, the optional move can be set to control how the order will be handled. It defaults to True ( False might be better if I have my logic backwards) which says if the value already exists, move the value to the end ( or start) of the collection. If False it would not add the value so the existing value would be used. 

$['expression']
: short hand for the Append Unique case, as this is generally what we want with path and flags, ie we only want one case and ordering of paths matter in that we want what we depend on to move to the end of the list. (I have found this logic is generally useful for large build on posix system for values such as LIBPATH and LIBS when resolving a tree of values with the substitute engine)  



## API


### Functions

In package SCons.Subst 

[SubstString](SubstString)(input,subst_mode,use_cache,**dict):: 
input
: the value to be substituted, the value could be a string or collection of strings 

subst_mode
: 
special rules to apply. A bit field of value such s SIG (remove values in **$( $)** ), WHITESPACE (keep white space). ( what else??) 


use_cache
: controls if the value is cached or fully reevaluated.  

dict
: this is the environment object or dictionary of values in which the expressions in a ${} like statement would evaluate within. 

Returns
: This function returns a string object, or internal object sub-classed from a Python str type. 



### Classes

**class SubstStrBase(str):** 

* This class is internal class that allows the construction of different types of string classes that have special behavior. The most common use will be to have string class that preserve the state of the string from modification or holding a set of string values ( Like a C++ rope implementation) to preserve different behaviors on different segments of the sting during substitution processing. 
**class Literal(SubstStrBase):** 

* This call holds and prevent the value of the string to be modified during a substitution call. 
**class Ignore(SubstStrBase):** 

* This string holds a values that depending on the substitution mode will return an empty string or the resolved value of the string. 
**class SubstStr(SubstStrBase):** 

* This class holds the values of different types string as a list. This allow a value to correctly behave as a string while holding on to certain properties that preserve certain behaviors. For example a "$foo" + Literal("$world") would result in a string of value "$foo$world". After a subst() call we might get a value of "hello $world". The SubstStr object will allow a second call to subst() to preserve the $world value, as the object would hold a list of a ["hello ",Literal("$world")] 
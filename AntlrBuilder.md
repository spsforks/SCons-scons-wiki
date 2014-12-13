
**Note**: the following is for ANTLR v2, not for ANTLR v3. It also assumes that you don't use the 'exportVocab' keyword in the 'options' block for your Lexer. It also can not be used if you want to create a shared library containing your lexer/parser, as the list of sources returned by the tool includes header files and text files, which G++ will refuse to package in a shared library. Tested Oct 2007 with 'cantlr' deb package on Ubuntu 7.04. 

For a given antlr grammar (`t.g`): 


```cplusplus
#!cplusplus 
header {

#include <iostream>

ANTLR_USING_NAMESPACE(std)
ANTLR_USING_NAMESPACE(antlr)

}

options {
  language="Cpp";
}

class IntAndIDLexer extends Lexer;

INT        : ('0'..'9')+ ;
ID             : ('a'..'z')+ ;
COMMA      : ',' ;
NEWLINE    : '\n' ;

class SeriesParser extends Parser;

series     : element (COMMA! element)* NEWLINE;
element    : INT | ID;

//class SeriesTreeParser extends TreeParser;
//series: (INT | ID)+;
```
The following builder will build a static library for the parser for this grammar and link it with a main.cpp. Note that I am assuming C++ output here. 


```python
#!python 
import os
import re

antlr_res={};

def make_re(classtype):
        return re.compile('^class\\s+(\\S+)\\s+extends\\s+'+classtype,re.MULTILINE);

def append_re(res,classtype,fn):
        res[classtype]=[make_re(classtype),fn];

def lexer_append(target,classname):
        target_append(target,classname);
        target.append(classname+'TokenTypes'+'.hpp');
        target.append(classname+'TokenTypes'+'.txt');

def target_append(target,classname):
        target.append(classname+'.hpp');
        target.append(classname+'.cpp');        

append_re(antlr_res,'Lexer',lexer_append);
append_re(antlr_res,'Parser',target_append);
append_re(antlr_res,'TreeParser',target_append);

def antlr_emitter(target,source,env):
        target=[];
        for src in source:
                contents = src.get_contents();
                for type_re in antlr_res:
                        found = antlr_res[type_re][0].findall(contents);
                        for classname in found:
                                antlr_res[type_re][1](target,classname);
        return (target,source);

b = Builder(action="java antlr.Tool $SOURCE",src_suffix='.g',emitter=antlr_emitter)
env = Environment();
env.Append(BUILDERS={'antlr':b}); # NEED TO APPEND!
env.Append(ENV={'CLASSPATH':os.environ['CLASSPATH']});
antlr_sources=env.antlr(source='t.g')

lantlr=env.StaticLibrary(target='tparser',source=antlr_sources);
prog=env.Program(source=['main.cpp'],LIBS=['tparser','antlr'],LIBPATH='.');
```
And the output: 


```txt
antlr $ scons -Q
java antlr.Tool t.g
ANTLR Parser Generator   Version 2.7.4   1989-2004 jGuru.com
g++ -c -o IntAndIDLexer.o IntAndIDLexer.cpp
g++ -c -o SeriesParser.o SeriesParser.cpp
ar r libtparser.a IntAndIDLexer.hpp IntAndIDLexer.o IntAndIDLexerTokenTypes.hpp IntAndIDLexerTokenTypes.txt SeriesParser.hpp SeriesParser.o
ranlib libtparser.a
ar: creating libtparser.a
g++ -c -o main.o main.cpp
g++ -o main main.o -L. -ltparser -lantlr
```
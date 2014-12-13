
CXXFile() builds a lexer from a lex file, typically ending with '.ll'. 
```txt
## Beginning of script
CXXFile( target='lex.yy.cpp', source='parser.ll' );
```
The result will be a C++ file named 'lex.yy.cpp' which you can then compile and link with your project. 


Builder() creates a Builder object for the specified action. In general, you should only need to add a new Builder object when you want to build a new type of file or other external target. A Builder object is a callable that encapsulates information about how to execute actions to create a target Node (file) from source Nodes (files), and how to create those dependencies for tracking.  

Generally the Builder ([SCons User Guide](http://scons.org/doc/HTML/scons-user/book1.html) Chapter 19) should have a action or a generator (SCons User Guide Chapter 19.5.) parameter.  

For a detailed parameter description look into the man pages [scons-man.html](http://www.scons.org/doc/HTML/scons-man.html) Chapter _Builder Objects_ 

Examples for custom builder could be find at [CustomBuilders](CustomBuilders) 

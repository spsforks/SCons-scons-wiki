
Use the [SideEffect() method](SideEffect) and specify the same dummy file for each target that shouldn't be built in parallel.  Even if the file doesn't exist, SCons will prevent the simultaneous execution of commands that affect the dummy file. 

_This answer should be expanded with at least two specific examples: one demonstrating preventing different commands in parallel, and one demonstrating how a builder would prevent parallel execution with itself._ 

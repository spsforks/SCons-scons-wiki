
I have no idea how to do this, so here is a page ready for the experts to fill in the details. 

Lets say I need to make a custom version of ld, or gcc, and want it to be done as part of a source build: 

tree example: 
```txt
         project/
         project/compiler/
         project/application
```
An executable in project/compiler needs to be created before anything in project/application is compiled. In addition, this executable needs to be used for Builders in project/application. 

Can scons do this ? [Yes.] 

The first step is to have scons compile the ld, or compiler.  Then you would create a new Environment and configure it to use your compiler or linker, export this new Environment for use to compile the rest of the project. 

See for more information: [UsingCodeGenerators](UsingCodeGenerators) 

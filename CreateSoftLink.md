
This page explains how to correctly create symbolic links. 

Creating symbolic links is required when you create a shared library. You'll need to set up a link from the _soname_ to the real name. 

Assume the files in your project are 

* some_code.c 
* sconstruct 
* backend/some_code.c 
* backend/sconstruct 
Assume somehow you have built _backend/liba.so.0.0.1_. Then you wish to create two soft links in directory _backend_, named _liba.so.0_ pointing to _liba.so.0.0.1_, and _liba.so_ pointing to _liba.so.0.0.1_. For some reason (e.g., different compiling option between the folders), you  use _sconstruct_ and _backend\sconstruct_ separately to compile different folders. 

Here is a solution. 

In _sconstruct_: 

* env.SConscript('backend/sconstruct') 
In _backend/sconstruct_: 

* env.Command('liba.so', 'liba.so.0.0.1', 'ln -s **${SOURCE.file}** $TARGET') 
* env.Command('liba.so.0', 'liba.so.0.0.1', 'ln -s **${SOURCE.file}** $TARGET') 


## Gch Builder

The Gch Builder provides a similar interface for precompiled headers on gcc like the PCH builder for msvc. Dependencies of shared objects and static objects are autogenerated. 

Limitations: 

* different gch's for shared objects and static objects are required, thus there are two builders Gch and GchSh 
* mixing Gch and GchSh for the same header file is not possible, since gcc seems to look only for one gch 
      * TIP: GCC supports multiple precompiled headers (with different compiler options) by putting them in a folder named "headername.gch" with different names. The builder could use this to create a pch for each set of options used... 

### Explanation and additional usage instructions

This way we check if an object file depends on the original header from which precompiled header was generated. To use modified tool with build dirs you modify the build environment in `SConscript` like this: 


```python
#!python
env.Prepend(CPPPATH=['.'])
```
which will ensure that the compiler looks for (precompiled) header in a build dir **before** the source dir. I'm not sure if this can be automated somehow. 

[Code in github](https://gist.github.com/1321295) 


## Usage

See comments on top of the file 

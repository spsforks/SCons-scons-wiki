
This documents intents to describe the current shortcomings of Fortran support (as scons 0.97.0d20071212), as well as the possible remedies. Some user cases which break 


# Some user cases which currently break

With the current system, scons "guarantees" that every fortran dialect (F77, F90, F95, as well as a default one, FORTRAN are currently supported) is supported as long as one fortran tool define one dialect, or one fortran compiler is given during the environment construct. Concretely 


```python
env = Environment()
env.Program('hello.f90')
```
will "work" even if only a f77 compiler is found by scons. "works" and not works because if for example, g77 is the found compiler, scons will use it as a fallback if no f90 compiler is found; but g77 will not recognize the `.f90` file as a fortran source file, but as a link script input, which is certainly not what the user expects. Worse, g77 does not return status error in this case, leading scons to continue after the compilation. Link will fail with obscure error(s). 


```python
env = Environment(F77 = fancycompiler)
env.Program('hello.f90')
```
Will also works, and scons will compile hello.f90 with the F77 compiler if F90 (or FORTRAN) is not defined by a tool. Again, this is unlikely to work. 

Another problem is related to the documentation: according to scons manual, the user can expect to find many construction variables related to fortran. `FORTRAN`, `FORTRANCOM`, etc... are supposed to represent the default fortran compiler, and as such, the user should expect it if any fortran compiler is found. This is not the case: those variables are never defined, except in rare cases. Other dialects (F77\*, F90\*, etc...) are not defined either. So if you want to check whether the F77 compiler is set: 


```python
env = Environment()
assert not env['F77'] == ''
```
This will not work, even when a F77 compiler is found by scons. 

The core problem is that because scons wants to guarantee that all dialects are internally usable when at least one tool define one dialect, a lot of magic is happening. This magic was necessary in "old times" when scons did not support different dialects; now, this gives a lot of complexity, to support a feature which is not that useful, and actually leads to obscure bugs. 


# How to improve the situation ?

What we propose is to remove the magic, and to be much more explicit. For example, assuming only one fortran tool is used, it would define explicitly the dialects it supports. For example, in the case of g77, FORTRAN and F77 only would be defined. This means that files with suffixes .f90 of .f95 would not be recognized; we believe that this is a much better behavior. 


## What would break ?

The goal is to make things working out of the box. In particular, using: 


```python
env = Environment()
env.Program('hello.f')
env.Program('hello2.f90')
```
Will work as long as a f90 compiler is found. It would not work on platforms with only f77 compiler available, but those could not work anyway with current scons. 

Another case which would break: 


```python
env = Environment(F77 = fancycompiler)
env.Program('hello.f90')
```
This works with current scons on some platforms where the compiler frontend is "smart" (sun fortran compiler, for example): F90 is not defined, but scons uses F77 as a fallback for `.f90` source files. If the compiler is smart enough to see this is F90 source code, the F77 compiler may call internally the F90 compiler. f77 on solaris does this (> is the shell prompt) 


```console
> f77 -c hello.f90
NOTICE: Invoking ../opt/sun/sunstudio12/bin/f90 -f77 -ftrap=%none hello.f90
```
IOW: scons wo F90 compiler uses F77 as a fallback, and then solaris f77 is smart enough to actually call f90 ! What we suggest is to define F90 if a f90 tool is available, such as scons does call F90, and thus less magic is involved. But if an F90 compiler is found by scons through the tool search mechanism, it will anyway define F90, and call directly the f90 compiler. So this would break only if you forced scons not to look for an F90 compiler. 


## What would be fixed

As every tool explicitly define its dialects, the following variables will always be defined: 

  * FORTRAN\* -> any fortran compiler should define thoses. The last included compiler wins (e.g. tools = ['f77', 'f90'] in Environment would cause FORTRAN to be defined as f90). 
  * Any compiler supporting one dialect would define the corresponding compiler (g77 would define F77, f90 would define F90, etc...). 

Also, we will fix the fortran tools, in particular: 

  * correct flag handling for pic code (-KPIC, -fpic, etc...) 
  * support newer compilers (gfortran) 
  * eventually: support mixing C and Fortran code, using a scheme similar to autoconf. 

## How to migrate

We intend to make it possible to use the same sconscript for both old scons and new scons, but this may require changing your scons script. 

  * In most cases, the changes are handled at the tool level. If the fortran tools you are using can be found by scons, you won't have to change anything. 
  * If you need to support several dialects, just define the corresponding variables to the desired compiler. For example, if you want to support F77 and F90, and your compiler is not available as a scons tool, just define F77 and F90 to your compiler. If you need different compiler flags, you will have to define the corresponding F77FLAGS and F90FLAGS. 

# Unsolved questions


## source file suffix

Depending on the fortran compilers, different suffix are recognized. For example, scons currently define F77 source files suffix with .f77. But this is not recognized by g77, for example. This should be defined at the tool level to be really useful, or more precisely, it should be possible for a fortran tool to define itself which suffix to use for what dialect: 

  * g77 and gfortran will not recognize .f77, but sun compiler, even when invoked as f77, will 
  * g77 will not recognize .f90 but gfortran will 
It looks like .f77 is not often used. NETLIB sources use .f, and neither g77 or gfortran recognize .f77. Should .f should be recognized as a F77 or FORTRAN ? 


## Fortran 77?

Since Fortran 90 and better are supersets of Fortran 77, should Fortran 77 compilers be deprecated?  Especially with the continued strong development and acceptance of gfortran? 

This would mean one set of FORTRAN* environment variables. 


## Explicit is better than implicit

Because of several different Fortran 90 and better compilers, I would like to be able to use an explicit list of compilers. 

I am very new to SCons and have started to apply it to a project that is mostly `*.f` files, but needs to be compiled with a Fortran 90 or better compiler.  On Windows, the project uses [Lahey](http://www.lahey.com/) and I have been using [Portland Group](http://pgroup.com) on Linux.  Currently there are two different build systems for the different platforms and that is why I was hoping to use SCons. 

In order to work with SCons I am only compiling the part that can be compiled with 'g77'. 

Would something like the following work?  Choose and set all of the `FORTRAN*` env variables based on the first Tool found. I am not sure of the Lahey fortran command name and I am not sure that SCons doesn't already do something like this. 
```python
Tool(['ifort', 'lhf', 'pgf90', 'gfortran'])(env)
```
Of course, SCons would have to be extended to support Lahey and Portland Group to easily work with my current project. 

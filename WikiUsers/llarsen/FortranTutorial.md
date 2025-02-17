

# SCons Fortran Tutorial

SCons is an interesting alternative to make for compiling Fortran projects. I recently started to look into using scons to build some of my Fortran code, but ran into several difficulties. Most of these difficulties were a result of lack of documentation related to compiling Fortran using SCons. I figured I would write a tutorial based on my experience in order to make the process easier for others that may choose to use SCons to build Fortran projects. It is assumed that SCons is already installed. For instructions on installing SCons (as well as compiling c code) see [this tutorial](SconsTutorial1). 


## The Fortran Code

The Fortran program used for this tutorial, was comprised of a simple module named `TestMod.f90` and a program file called `main.f90`. The module has a function that adds two real values, and the main program calls this function and prints the result. The Fortran source files are shown below: 

`TestMod.f90` 
```txt
module TestMod
contains
  function Add(val1, val2) result(sum1)
    real val1, val2
    sum1 = val1 + val2
  end function 
end module
```
`main.f90` 
```txt
Program AddTest
  use TestMod
  real reslt
  reslt = Add(5.4,3.2)
  write(*,*) "5.4 + 3.2 = ", reslt
end Program
```
These two file should be placed in the same directory. 


## The SConstruct File

The first step in building a program using SCons is to make a file named SConstruct. This file is a python script that can be edited in a text editor. It is different from a standard python script in that some SCons classes and methods used for building projects are already imported. You can of course import other python modules in the SConstruct script, but the basic classes and methods that you use to build a program are already available. You don't execute the SConstruct file directly. Instead you run the scons script (which is located in the Python installations `Scripts` directory) inside the folder where the SConstruct file is located. This is analogous to running make in the folder that a makefile is located. Often the Fortran source files are located in this same folder as the SConstruct file, although you can indicate other locations for the source files in the SConstruct script.  


## Building a Fortran Program in One Step

In SCons, there is a class called `Environment` that contains all of the methods used to compile and build a Program. When compiling Fortran programs using SCons, it is necessary to initialize an `Environment` object with information about which Fortran version will be used to compile Fortran source files. Compilers such as gfortran, g77, ifort, and sunf77 are supported (I am not sure what others). The gfortran compiler was used for this tutorial, and have not been tested with other Fortran compilers. 

Often, code is compiled in a compile step, followed by a link step. gfortran can be called both to compile the Fortran source files (into object files - or files that end in .o), and to link the object files into an executable. With gfortran, a program can be built in a single LINK step. gfortran will automatically cause the individual files to be compiled. However, when the files are implicitly compiled in a link single step, there is little control over the compile options for the individual source files. To compile the Fortran program in a single step create an SConstruct file in the same folder as the Fortran source files above and add the following text: 

SConstruct 
```txt
# Comment lines start with the # symbol
# The following sets up an Compile Environment Object with gfortran as the linker.
env = Environment(LINK='gfortran')
# The next line of code is an array of the source files names used in the program.
sources = ['TestMod.f90','main.f90']
# The next line is the actual code that links the executable. env.Program is generates an executable.
objs = env.Program('test.exe', sources)
```
Just as in the [c tutorial](SconsTutorial1), `env.Program` takes the name of an executable to product (`test.exe` in this case) followed by an array of source files to compile and link (in this case `TestMod.f90` and `main.f90`). For your case the array of files may be longer. To run the script, you will need to have a command window (or terminal window) open, and navigate the the folder the contains the SConstruct file and the Fortran source files. You will need the `Scripts` folder under the Python directory in your path, or you will need to type the fill path to the scons script file (scons.bat on windows). When you run the scons script in this directory, the following output should appear: 


```txt
> scons.bat
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gfortran -o test.exe TestMod.f90 main.f90
scons: done building targets.
```
There should also be a `test.exe` file in the folder which you can now run. 

You can add additional flags to the link call by passing a `LINKFLAGS` value to the `Environment`. For example, replacing the `Environment` initialization above with the following adds a '-g' (debug mode) flag to link command: 

SConstruct 
```txt
# Add LINKFLAGS='-g' to add a the -g option to the gfortran linker call.
env = Environment(LINK='gfortran',LINKFLAGS='-g')
sources = ['TestMod.f90','main.f90']
objs = env.Program('test.exe', sources)
```
Output: 
```txt
> scons.bat
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gfortran -o test.exe -g TestMod.f90 main.f90
scons: done building targets.
```

## Configuring the Fortran Compiler

While the build SConstruct method outlined about may work, often it is better to have a compile step followed by a link step. In the example above, a compile step is not called because the Fortran compiler was not configured in the environment - only the linker was configured. SCons allows you to configure FORTRAN 77, and Fortran 90/95 independently. SCons assumes by default that FORTRAN 77 files with have the extension .f77, Fortran 90 file will have the extension .f90, and that Fortran 95 files will have the extension .f95 (the extensions can be changed). If the compiler is not specified for any of these, then SCons will indicate an error if you try to run an explicit compile command for a file with the associated extension. If the compiler IS configured, then calling `env.Program` causes a compile step to precede the link step automatically. Since the source files above have the extension .f90 we will configure the Fortran 90 compiler options by passing an `F90=gfortran` value when we initialize the `Environment`. We will also set `F90FLAGS='-g'` to cause the files to be compiled in debug mode. You can also configure the F77 and F95 compilers if you have source files that end in .f77 or .f95. Alternatively, you can modify the list of extensions supported by, for example, the F90 compiler by passing `F90SUFFIXES=['.f77','.f90','.f95']` when initializing the `Environment` object. We also have to pass the `tools` parameter and indicate that 'gfortran' is included. You can also include 'default' in the tools list, which I thinks means that you can compile c and c++ files as well as gfortran files. 

SConstruct 
```txt
# Configure the f90 compiler
env = Environment(tools=['default','gfortran'],F90='gfortran',LINK='gfortran',LINKFLAGS='-g',F90FLAGS='-g')
sources = Split('TestMod.f90 main.f90')
objs = env.Program('test.exe',sources)
```
When you run the scons script, the following output results: 
```txt
> scons.bat
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gfortran -o TestMod.o -c -g TestMod.f90
gfortran -o main.o -c -g main.f90
gfortran -o test.exe -g TestMod.o main.o
scons: done building targets.
```
Note that first a compile step is called that generates an object (<source file>.o) file. Finally a link step occurs that automatically contains the '<source file>.o' files. The extra compile step occurred because we configured the F90 compiler, so SCons recognized what to do with the '.f90' files before the link step occurred. 


## Explicit Compile Followed by a Link Step

SCons include a method that that is used to explicitly compile a source file to an object file. That command is `env.Object`. The `env.Object` call receives a list of source files, and returns the files that were generated as a list. The files generated in the compile step include both object files (<source file>.o) as well as module files (<source file>.mod). For modules, an object file AND and module file is created. However, when we call the link step, ONLY the object file should be passed to the link command. This means that the list passed back from the `env.Object` call must be filtered to remove any module files before sending the list onto the `env.Program` command. 

The list of files that is passed back from `env.Object` is not a list of strings. The files are objects of the class `'SCons.Node.FS.Entry'`. Note that I determined this by printing  the type of one of the items in the list returned by `env.Object` below. I also determined that this object has a method called `get_suffix()` by calling dir on the object and printing the result. If you are not familiar with Python list comprehension statements, then the method I use to filter the module files out of the list may not make sense. I will explain it following the SConstruct file given below: 

SConstruct 
```txt
env = Environment(tools=['default','gfortran'],F90='gfortran',LINK='gfortran',LINKFLAGS='-g',F90FLAGS='-g')
sources = ['TestMod.f90','main.f90']
objs = env.Object(sources)
# Print the kind of object in the list that comes back from env.Object
print "Object list item type: " + type(objs[0])
# To see the methods supported by SCons.Node.FS.Entry objects uncomment the following
#print dir(objs[0])
# Get rid of the .mod names from the list using a list comprehension filter
objs2 = [obj for obj in objs if obj.get_suffix() == ".o"]
env.Program("filtermod2step.exe",objs2)
```
When `env.Object` is executed, it returns a list containing the files `['TestMod.o', 'TestMod.mod','main.o']`. The file `'TestMod.mod'` needs to be removed from this list before passing the list on to `env.Program` to build the executable. 

The statement `objs = [obj for obj in objs if obj.get_suffix() == ".o"]` is what is referred to as a list comprehension statement in Python. A list comprehension is used to take one list and make a new one. An if statement can be included to filter items. In this case each item in the list `objs` is checked to see if it ends with the suffix '.o'. If not it is not included in the new list objs2. For more info on python list comprehensions, read the 'list comprehensions' section on [this page](http://docs.python.org/howto/functional.html#generator-expressions-and-list-comprehensions). The list comprehension statement is equivalent to: 
```txt
objs2 = []
for obj in objs:
  if obj.get_suffix() == ".o":
    objs2.append(obj)
```
When the scons script is run, the following output is given: 
```txt
> scons.bat
scons: Reading SConscript files ...
Object list item type: <class 'SCons.Node.FS.Entry'>
scons: done reading SConscript files.
scons: Building targets ...
gfortran -o TestMod.o -c -g TestMod.f90
gfortran -o main.o -c -g main.f90
gfortran -o filtermod2step.exe -g main.o TestMod.o
scons: done building targets.
```
Note that in this case, `TestMod.f90` and `main.f90` are each compiled to object files individually. The list of object file is passed to the link step `env.Program`. The link step then links together the object files into an executable. 


## Building a Library

For large projects that share code, sometimes the shared code is compiled into a library that is linked into both projects. SCons can be used to generate static libraries by using the `env.Library` command. The `env.Program` command can link to one or more libraries indicated by the `LIBS` parameter. A `LIBPATH` parameter tells scons where to look for the library files. This can be a single path string, or an array of path strings. Relative paths may be used. The follow SConstruct file causes a library called `TestMod.a`, that contains the `TestMod` object file, to be created. This library is then linked to the `main` object file: 

SConstruct 
```txt
env = Environment(tools=['default','gfortran'],F90='gfortran',LINK='gfortran',LINKFLAGS='-g',F90FLAGS='-g')
sources = ['TestMod.f90']
env.Library('TestMod',sources)
env.Program('test.exe','main.f90',LIBS=['TestMod'],LIBPATH='.')
```
The output is as follows: 
```txt
> scons.bat
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gfortran -o TestMod.o -c -g TestMod.f90
ar rc libTestMod.a TestMod.o
ranlib libTestMod.a
gfortran -o main.o -c -g main.f90
gfortran -o test.exe -g main.o -L. -lTestMod
scons: done building targets.
```

## Share Libraries

Sometimes a shared library (such as a *.dll on windows, or a *.so on Linux) is preferred for shared source file. The `env.ShareLibrary` command can be used to create a shared library. The process is essentially the same as above with the exception that `env.ShareLibrary` is used in place of `env.Library`: 

SConstruct 
```txt
env = Environment(tools=['default','gfortran'],F90='gfortran',LINK='gfortran',LINKFLAGS='-g',F90FLAGS='-g')
sources = ['TestMod.f90']
env.SharedLibrary('TestMod',sources)
env.Program('test.exe','main.f90',LIBS=['TestMod'],LIBPATH='.')
```
Output 
```txt
> scons.bat
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gfortran -o TestMod.o -c -g TestMod.f90
gfortran -g -shared -o TestMod.dll TestMod.o -Wl,--out-implib,libTestMod.a
Creating library file: libTestMod.a
gfortran -o main.o -c -g main.f90
gfortran -o test.exe -g main.o -L. -lTestMod
scons: done building targets.
```
On windows, this creates a `libTestMod.a` file as well as the `TestMod.dll` file. It then links the `test.exe` to the `TestMod.dll` file. 

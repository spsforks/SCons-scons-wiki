[TOC]


# Available D compilers

The D Programming language main website is [here](https://dlang.org/).

The D programming language has (currently) three compilers and associated runtime systems:

- DMD 
- LDC
- GDC

DMD is the reference compiler. The front-end is written in D – so you have to bootstrap to build from source. Builds are made for Windows, macOS, and various Linux distributions, e.g. Debian, Ubuntu, Fedora, RHEL, CentOS – see [here](https://dlang.org/download.html) for downloads. It is packaged in Homebrew, Arch, Gentoo, and Chocolatey. Due to licensing issues associated with the backend, it has not been package by Debian or Fedora. This licensing issue has recently been resolved, so it is anticipated that DMD will soon be available in Debian and Fedora. There is though a DMD Debian repository called [D-Apt](http://d-apt.sourceforge.net/).

[LDC](https://wiki.dlang.org/LDC) is an LLVM-based version of the D compiler and runtime system. The D frontend code of DMD is put together with a LLVM backend to create the system. Distributions are made for Windows, macOS, and various Linux distributions. LDC is packaged by Homebrew, Debian, Ubuntu, Fedora, Arch, and Gentoo.

[GDC](https://gdcproject.org/) is a GCC-based version of the D compiler and runtime system. The D frontend code of DMD is put together with a GCC backend to create the system. It is not formally part of the GCC Suite, but there is some hope that it will be. GDC is packaged by Debian, Ubuntu, and Arch, but not by Fedora.

# Some general thoughts

DMD generally has the fastest compilation, and so many use it for development. It is also the reference compiler and so is generally the furthest ahead in dealing with D language features. The backend does not produce the most efficient code, even with optimisation on.

LDC has relatively slow compilation times compared to DMD, but generates very fast optimised code. Many people use LDC rather than DMD for their production builds, and indeed deal with the slower compilation during development. LDC is the D compiler to choose for mixed D/C++/C systems compiled with Clang.

GDC, like, LDC has relatively slow compilation times compared to DMD, but generates very fast optimised code. Many people use GDC rather than DMD for their production builds, and indeed deal with the slower compilation during development. GDC is quite a long way behind the latest D definition though. GDC is the D compiler to choose for mixed D/C++/C systems compiled with the GCC Suite.

# Support for D in SCons

D is supported integrally by SCons 'out of the box': C, C++, Fortran, and D are peer languages in the SCons system. The `Object`, `Program`, `Library`, and `SharedLibrary` builders are able to deal with D source code, i.e. files ending with a .d extension. This is the case for pure D language projects and mixed C/C++/D projects.

By default the search order for a D compiler is DMD, LDC, GDC.

There are also compiler-specific tools to enable a project to restrict the choice of D compiler; the tools are dmd, ldc, and gdc. (No surprise in the naming then.) These tools are for the compiler only, you still need a link tool in order to link compiled objects. SCons usually builds programs by compiling each file to create an object file, and then link all the object together to create an executable.

Unlike C and C++, D is a module/package based system: in D each file is a module, and packages comprise modules. D also has some whole program reflection features, often used by test frameworks. D has built in unit testing features. Whilst useful they are fairly basic, which leads to having frameworks build over the builtin features to give a truly powerful test framework. Doing whole program reflection means doing whole source compilation at once. This is not somethng normally supported by SCons. The dmd, ldc, and gdc tools though provide a new builder `ProgramAllAtOnce` which compiles all the source files in a single compile/link execution. This is not always fast for large monolithic codes, so there is a growing thought that per-package builds should be supported, which is not the case as yet.

# Notice of any incompatibilities

The biggest difficulty is that DMD, LDC, and GDC support different versions of D. it is important to check the language version in use for a project so as to determine which compilers are "in play".
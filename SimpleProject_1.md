I have 3 groups of files, all reside in the same directory: 
```
group1: file1.cc file2.cc file3.cc 
group2: file4.cc file5.cc file6.cc 
group3: file7.cc 
```
and then I have main.cc 

I want to compile 

* group1 with "-g" 
* group2 same as group1 and in addition with "-Wall" 
* group3 same as group2 and in addition with "-fprofile-arcs -ftest-coverage" 

My Sconstruct looks like this: 


```
flags = '-g'
fsharp = flags + ' -Wall'
fprof  = fsharp + ' -fprofile-arcs -ftest-coverage'

base = Environment(CCFLAGS = flags)
sharp = base.Clone(CCFLAGS = fsharp)
prof  = sharp.Clone(CCFLAGS = fprof)

prfList = Split("""
            file7.cc
""")

myList = Split("""
            file4.cc
            file5.cc
            file6.cc
""")

list = Split("""
            file1.cc
            file2.cc
            file3.cc
""")

prof.Library('my1', prfList)
sharp.Library('my2', myList)
base.Library('my3', list)

#Library('my',['my1','my2','my3'])
# this does NOT work ...???

sharp.Program('main.cc', LIBS=['my1','my2','my3','my1','my2','my3'], LIBPATH='.') 
```
Because I can't build a library from libraries, I have to specify my sublibraries twice, since there are dependencies between them. Does anybody know a better way to achieve this ...??? 

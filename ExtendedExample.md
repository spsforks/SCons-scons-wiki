
This is a kind of 'diary' of my experiences converting my Ant-based build system into scons. You'll see that it is a combination of emails from the mailing list and some extra notes and bits of code that I tried. 

John Arrizza 

---

I am (still) new to scons. I've tried it on a couple of small projects and it seems to work well. 

However, I'd like to roll it out in a bigger way and I'm stuck. I'd like to get some feedback from you all on how you'd proceed. I'd like to use it for my home setup which has some interesting twists and turns and so may pose a nice challenge for the scons gurus. 

The basic scenario is that I have a whole bunch of little projects (50 or so?) and I use those to populate my web site (www.arrizza.com). I am currently running on Win2K, using Ant with some home-brew  taskdefs, some helper exe's, scripts, etc. It's become a bit of a mess and I'd like to clean it up into something much more straightforward by using scons. 

The directory structure looks like: 
```txt
   \projects\src\project1
   \projects\src\project2
   ...
   \projects\src\projectn  (~20 projects)
   \projects\frozen\project1 (~20 projects.)
   \projects\neuralnets\project1 (~5 projects)
   \projects\debug\project1 (etc.)
   \projects\release\project1 (etc.)
   \projects\web\arrizza\html\  (etc.)
   \projects\web\arrizza\cgi-bin\ (etc.)
```
* The `\projects\web\arrizza` is a staging area where I collect all of the information prior to FTP'ing (via an Ant taskdef) to my web site. I've been working on a python based ftpmirror that will only send new/changed files. 
* All of the projects under `\projects\frozen` are compiled and put in the staging area. 
* Some -- not all -- of the projecs in `\projects\src` are compiled and put in the staging area. 
* some projects don't have a compile step, there are just some files that get put in the staging area. 
* there are some dependencies between the projects (e.g. unit testers are used by many projects) but generally they are isolated. 
* I have projects written in in C# or C++ (VC7 or VC6 or gcc) or Java (jikes). Most projects are compiled in one and only one language but there are some (e.g. a cross-platform unit tester) that I compile in multiple languages. 
* I have an xml file contains information that is used to create and generate zip files, the html page, etc. for a downloads area. I wrote a C# app to do all of this work. I'd like to replace it with some python code. 
The public interface to this build system (i.e. what I can call from or do from the command line with Ant) is something like: 

* compile (release mode) any given project 
* compile various groups of projects (see for example [http://www.arrizza.com/downloads/downloads.html](http://www.arrizza.com/downloads/downloads.html) as one of these groups) 
* compile all 
* prepare a particular part of the staging area (e.g. put my resume in the `html\resume` directory) 
* prepare all of the staging area 
* send a particular part of the staging area (e.g. send an updated resume to my website) 
* send all of the staging area to the website 
* do it all, i.e. compile all, prepare all, send all 
Given all that, how would you lay out the the scons files, what builders would I need, etc. to get this to work similar to the way I have the Ant system now? 

---

 I have source in several directories: 
```txt
   projects\src\projectn (etc.)
   projects\frozen\projectn  (etc.)
```
I want the target directory to be either debug or release (siblings of the source root directories): 
```txt
   projects\debug\project
   projects\release\project
```
* 1 Should I have one sconscript file at the root (i.e. `\projects\sconscript`) and then one in each project, or is it better to put it all into one file at the root? 1 I would like to name projectx on the command line and have scons "know" where projectx resides. That way I can move projectx from one source root directory to another without having to change the command line to build projectx. How do I do this? 


---

 _1) Should I have one sconscript file at the root (i.e. `\projects\sconscript`) and then one in each project, or is it better to put it all into one file at the root?_ 

I'd go with separate SConscripts in each project.  Modularity is your friend. 

_2) I would like to name projectx on the command line and have scons "know" where projectx resides. That way I can move projectx from one source root directory to another without having to change the command line to build projectx. How do I do this?_ 

Use the Alias() function to map the arguments you'd like people to specify on the command line to the underlying targets (subdirectories and/or individual files) that should be built for that argument. 

---

 Main sconstruct file has a list of Alias()'s with each project I care about. If I ever move a project, I change the Alias for it in one place -- done. I'll start setting this up... 

My next question: 

Once I have all of this set up, how do I group the Alias()'s into a few different groups? e.g. I need a command to compile all of the 'download' projects, another to compile all of the 'neuralnet' projects, etc. I'd also like a 'compile all'. 

In make these are psuedo targets, in scons the right way to do this is to use ?? 

---

 _In make these are psuedo targets, in scons the right way to do this is to use ??_ 

Aliases again.  Aliases can "contain" other aliases. 
```python
a = Alias('A')
b = Alias('B')
all = Alias([a, b])
```


---

 As Gary mentioned, use Aliases. You can also use the Alias call on the same alias multiple times... so your SConstruct could look like: 
```python
...
Alias('neuralnet1','neurelnet1.exe')
Alias('neuralnet','neuralnet1')
...
Alias('neuralnet1','neurelnet2.exe')
Alias('neuralnet','neuralnet2')
...
Alias('neuralnet1','neurelnet3.exe')
Alias('neuralnet','neuralnet3')
...
Alias('neuralnet1','neurelnet4.exe')
Alias('neuralnet','neuralnet4')
```
Is equivalent to, 
```python
...
Alias('neuralnet1','neurelnet1.exe')
...
Alias('neuralnet1','neurelnet2.exe')
...
Alias('neuralnet1','neurelnet3.exe')
...
Alias('neuralnet1','neurelnet4.exe')
Alias('neuralnet',['neurelnet1','neurelnet2','neurelnet3','neuralnet4'])
```
The order you add tasks into the Alias is the order they will be executed. 



---

 In response to the emails, I tried the following. It did not work. 

Sconscruct 
```python
env = Environment()
env.Alias('cppwiki', 'src/cppwiki')
env.Alias('pso', 'src/pso/sconscript')
```
Sconscript 
```python
import sys

print("In pso\sconscript")
env = Environment(tools=['mingw'])
project = 'pso'
builddir = buildroot + '/' + project
targetpath = builddir + '/' + project
VariantDir('#' + builddir, "#.", duplicate=0)
env.Program(targetpath, source=Split(map(lambda x: '#' + builddir + '/' + x, glob.glob('*.cpp'))))
```
Calling 'scons pso' just says that the target is up to date 
```cmd
D:\projects>scons  pso
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: `pso' is up to date.
scons: done building targets.
D:\projects>
```
Made things simpler: 
```python
env = Environment()

Export('env')
env.Alias('cppwiki', 'src/cppwiki/sconscript')
env.Alias('pso', 'src/pso/sconscript')
```
pso/sconscript 
```python
import sys
Import('env')
print("In pso/sconscript")
project = 'pso'
```
Still no joy. Using SConscript works: 
```python
env = Environment()

Export('env')
env.Alias('cppwiki', 'src/cppwiki/sconscript')
env.Alias('pso', 'src/pso/sconscript')
SConscript('src/pso/sconscript')
SConscript('src/cppwiki/sconscript')
```
but now builds both projects, no matter what I put on the command line. 

---

 Well it didn't really "build" both projects. It just read the sconscript files, which caused the 'print' function to execute, which made it look like a compile was happening. 

---

 Here's a response to an email I sent out. 
```python
env = Environment()
Export('env')
env.Alias('cppwiki', 'src/cppwiki/sconscript')
env.Alias('pso', 'src/pso/sconscript')
```
The Alias calls should not list the SConscript files, they should list whatever *targets* (files and/or subdirectories) you want built for the alias.  So if you want the aliases to build all of the targets underneath the subdirectories in which those SConscript files live, you should list those subdirectories: 
```python
env.Alias('cppwiki', 'src/cppwiki')
env.Alias('pso', 'src/pso')
SConscript('src/cppwiki/sconscript')
SConscript('src/pso')
```
You still need the SConscript() calls to tell SCons to read up and execute the SConscript files. 

_But I get this output no matter what's on the command line. So it looks like the SConscript() command is calling the sconscript not just a declaration. That is the conscript file is executed immediately when the SConscript() statement is seen._ 

It's actually not executed immediately, but it is executed.  That's what the SConscript() call does; it says, "Here's a subsidiary configuration file, you need to read it and execute it so you have the right picture of the dependencies before you process the targets on the command line." 

_How do I "hook up" the command line to the Alias to the sconscript file? In other words, I need to declare that whenever I type 'pso' on the command line, there is a mapping from that to a real directory (via the Alias)_ 

Right, to a directory, not an SConscript file. 

_and there is a mapping from the directory name to the invocation of the correct sconscript file (via ???)._ 

No, SConscript files just get read up to establish the global picture of the dependencies.  You don't need to map specific names to specific SConscript files. 

_But those are only declarations. I also need a way to say, ok, for this invocation of scons, I need to compile a target, e.g. pso, and no others._ 

That's what you specify on the command line.  They can be files, or directories (in which case everything under the directory is built) or Aliases (which expand to files or directories). 

---

 Based on the above email and more reading of the manual, here is the latest sconstruct: 
```python
env = Environment()
Export('env')
env.Alias('cppwiki', 'src/cppwiki')
env.Alias('pso', 'src/pso')
SConscript('src/pso/sconscript')
SConscript('src/cppwiki/sconscript')
```
and sconscripts (only one, the other is similar): 
```python
Import('env')
print("In pso/sconscript")
project = 'pso'

env.Program(target = 'pso', source = ['acs-tsp2003.cpp', 'solution.cpp', 'utilities.cpp'])
```
**Current Status** 

It currently builds one or the other target based on the command line, and 'scons .' builds both. 

**Notes** 

* the sconscript files are read and, since they are python, they are 'executed'. However, that does not cause a build to actually occur. 
* the Program() causes the build to occur but only if the command line target (through an Alias() if it exists) matches the "target=" parameter to the Program() call. 
**Questions (more or less priority order)** 

* the Program() is defaulting to VC7 (i.e. 2003 .Net), I need to force a different compiler in each case (gcc for pso, VC6 for cppwiki). How do I do that? _Create different construction environments, possibly from a common ancestor using env.Clone(), and then call env.Tool(tool) on each environment with different values of tool_ 
* how do I specify an alternate build directory? e.g. `\projects\debug\pso` Read about env.VariantDir
* how do I specify debug vs release? _Leanid: I use the same env.VariantDir and add Release or Debug into path, I set it by using ARGUMENTS.get('mode', 'Release') and invoking "scons mode=Debug", also I put this value in env[MODE](MODE) and alter compiler flags based on this setting._ 
* there is a .dsp available for cppwiki. I believe I can use that. How do I do it? 

_Leanid: I have written wrappers for `Program, `SharedLibrary` ,`StaticLibrary` and use something like this inside. Now "scons dsp=yes" build dsp files_
```python
class Dev(Environment):
    def _devBuildDsp(self, buildtype, target, source, duplicate=0):
        # Split source in group
        ...
        buildtarget = self.Program(target, src["Source"], duplicate=duplicate)
        self.MSVSProject(
            target=target + self["MSVSPROJECTSUFFIX"],
            srcs=src["Source"],
            incs=src["Header"],
            localincs=src["Local Headers"],
            resources=src["Resource"],
            misc=src["Other"],
            buildtarget=buildtarget,
            variant=self["MODE"],
        )

    def DevProgram(self, target=None, source=None, pattern=None, duplicate=0):
        if ARGUMENTS.get("dsp", "no") == "yes":
            self._devBuildDsp("exec", target, source, duplicate=duplicate)
        else:
            self.Program(target, source, duplicate=duplicate)
```
* why are all the sconscript files being read when I only specify one on the command line? Is there a workaround? _SCons, by default, reads everything so that it can build a full dependency tree. This is good. If you are clever then you can do things like if env['BUILD_PSO']: SConscript('src/pso/sconscript'); to only read the SConscripts of the targets you're interested in, but be careful._ 
* some of my projects require me to build with more than one compiler. How do I do that? _See the answer to your first question :-)_ 
* do I have to name each and every .cpp? _Try import glob; Program('pso', glob.glob('*.cpp'))_ 
      * _Leanid: glob will not work with VariantDir set. I use next function:_ 

```python
class Dev(Environment):
    def DevGetSourceFiles(self, patterns=None):
        files = []

        if patterns is None:
            patterns = [
                "*" + self["CXXFILESUFFIX"],
                "*" + self["CFILESUFFIX"],
                "*" + self["QT_UISUFFIX"],
            ]
        for file in os.listdir(self.Dir(".").srcnode().abspath):
            for pattern in patterns:
                if fnmatch.fnmatchcase(file, pattern):
                    files.append(file)
        return files
```
* how do I add other compile and link parameters? _Use env.Append(CCFLAGS = ['-g', '-O2']) and similar._ 


---

 Made some further changes based on comments above and another email: 

I find it's simpler to do most of the work in the SConstruct: in SConstruct: 
```python
mode = ARGUMENTS['mode']
# also set up tools according to mode here
variant_dir = os.path.join('#Build', mode, 'projectx')
SConscript('projectx/SConscript', variant_dir=build_dir, ...)
```
then the projectx/SConscript doesn't have to know about the mode at all.  And your build dir can go wherever you like, just set up the build_dir arg properly.  The SConscripts can just look like this: 
```python
foo = Project(...)
Alias('projectx', foo)
bar = OtherThing(...)
Alias('projectx', bar)  # add each target to the projectx alias
```
If all your targets (and only those) are under '.' (the current build dir), you could just do 
```python
Alias('projectx', '.')
```
instead.  Of course only the final targets need to be added to the Alias; everything else needed by those will automatically built as needed. 

---

 The current code is here [ExtendedExampleSource1](ExtendedExampleSource1) 

**Current Status** 

It currently builds one or the other target based on the command line, e.g. 'scons pso mode=debug', and 'scons .' builds everything. 

**Todo** 

   * finish setting up the correct Tool() for each project or should I use the .dsp builder? 
   * finish adding appropriate compile & link parms to each project; Look into having a centralized list of parms 
   * figure out which tool to use for C# or use something to run devenv against the .sln 
   * disallow command lines like 'scons pso mode=fred' this causes a \projects\fred\pso\... tree to be created. mode should be 'debug' or 'release' only. 
   * decide whether to prevent reading of sconscripts based on command line arguments 
   * add remaining projects; add more Alias()s for groups, e.g. neuralnet, downloads, miscdownloads, etc. use Ant file to group them 
   * try multiple variant compiles with jUtAsserter 
   * Check out Leonid's Dev() class rather than just glob.glob 
**Questions** 

   * heh. no questions. just work. 


---

 The current code is here [ExtendedExampleSource2](ExtendedExampleSource2) 

**Current Status** 

   * Added Leonid's Dev() class rather than using glob.glob. Seems to have simplified the sconscripts a bit 
   * I disallowed command lines like 'scons pso mode=fred' this causes a \projects\fred\pso\... tree to be created. mode must be 'debug' or 'release' only. 
**Todo** 

   * finish setting up the correct Tool() for each project or should I use the .dsp builder? 
   * No builtin tool for C#, see if I can use Erling's C# Tool. 
   * finish adding appropriate compile & link parms to each project; Look into having a centralized list of parms 
   * decide whether to prevent reading of sconscripts based on command line arguments 
   * add remaining projects; add more Alias()s for groups, e.g. neuralnet, downloads, miscdownloads, etc. use Ant file to group them 
   * try multiple variant compiles with jUtAsserter 
**Questions** 

   * more work 


---

 Just tried MSVSProject(). Compiled ok but did not generate any files. Read the Manpage, looked at Leonid's Dev() class again, still no joy... Hmmm. 

---

 The current code is here [ExtendedExampleSource3](ExtendedExampleSource3) 

In general, the sconstruct has become the repository for all the helper functions the sconscripts need and also it has become the driver/coordinator of the sconscripts. I wanted it this way to ensure that I can move projects from one directory tree to another with very little effort. I think this is the right direction: 

   * sconscripts hold as little information as possible except for project-specific stuff 
   * everything else in the sconstruct 
I'm working on getting the Install() to start building a staging area where the website files will eventually reside. When that staging area is complete, I will then need to find a way to transfer it to my website server. 

**Current Status** 

   * gave up on MSCSProject() for now. set up a Command() for building sln's and dsp's. Used Depends() to make the target depend on source files (.cpps, .h's etc.) not just the project file (.dsp, .sln) 
   * added almost all Alias() and projects that I want to use 
**Todo** 

   * some projects have multiple dsp's or have directory structures that don't fit into the current setup (e.g. jUtAsserter). need to finish adding the rest of them to the sconstruct and adding sconscripts for them. 
   * decide whether to prevent reading of sconscripts based on command line arguments 
   * need to finish the remaining Alias()es 
   * started working on understanding Install() 
**Questions** 

   * I have some files that get "installed" by just a straight copy from a source directory to the staging area 
   * I also need to see if I can use ftp to transfer the staging area to the remote server 


---

 The current code is here [ExtendedExampleSource4](ExtendedExampleSource4) 

The Install() works nicely with either targets (e.g. Program(), etc.) or with existing files (e.g. File(), Dir()). 

I created three helper functions that might be useful to others: 

      * [GetFiles](GetFiles)(dir, includes, excludes=None) returns a list of files in 'dir' that matches the patterns in 'includes' and doesn't match the patterns in 'excludes'. see [InstallFiles](InstallFiles)() for an example of how to use it. 
      * [InstallFiles](InstallFiles)(env, dest_dir, src_dir, includes, excludes) returns a Node of the dest_dir to use in an Alias(). It gets all of the files in 'src_dir' that matches the patterns in 'includes' and doesn't match the patterns in 'excludes' and adds an Install() for each one in the given 'env'. It's used something like this: 

```python
env.Alias('prepare_main', [
     InstallFiles(env,
        dest_dir = arrizza_local_root,
        src_dir  = arrizza_websrc_root + '/main',
        includes = ['*'],
        excludes = ['.svn']),
     InstallFiles(env,
        dest_dir = arrizza_local_html,
        src_dir  = arrizza_websrc_root + '/htmlmain',
        includes = ['*'],
        excludes = ['.svn'])
      ])
```
Now 'scons prepare_main' will copy all files from the directories in .../main and in .../htmlmain and put them in their respective destination directories held in the variables 'arrizza_local_root' and 'arrizza_local_html'. All the files in the source directories are copied expect those that match the .svn (this is from the [SubVersion](SubVersion) version control, see [http://www.tigris.org](http://www.tigris.org)). 

      * [InstallTree](InstallTree)(env, dest_dir, src_dir, includes, excludes) is similar to [InstallFiles](InstallFiles)() except that it traverses the entire directory tree. 
**Current Status** 

   * finished most of the Installs() I need 
   * started using SConsignFile() 
**Todo** 

   * some remaining Installs require a complete tree to be moved over, then a few files deleted, a few files overwritten, etc. need to work out how to do that. 
   * some projects have multiple dsp's or have directory structures that don't fit into the current setup (e.g. jUtAsserter). need to finish adding the rest of them to the sconstruct and adding sconscripts for them. 
   * decide whether to prevent reading of sconscripts based on command line arguments 
   * need to finish the remaining Alias()es 
   * I also need to see if I can use ftp to transfer the staging area to the remote server 
   * Need to look into Zip() 


---

 It seems that there a few categories of soncs commands: 

   * commands that return Nodes, e.g. Dir(), File(), Alias(), Depends(), etc.  These commands are used to create, organize or otherwise manipulate Nodes. 
   * commands that have a file-system side-effect, e.g. Program(), Install(), [InstallAs](InstallAs)(), Command(), etc. These commands take a Node and do something with them, OR do something and return a Node to indicate what it did. They effect files and directories on the file-system. More precisely, they effect the file-system if they are part of the final target Node list. 
   * commands used for admin/bookkeeping purposes, e.g. SConscript(), SConsignFile(), Export(), Import(), etc. These commands provide "glue" between the various bits of the build system. 
hmmm. more categories to come as I learn about them... 

---

 The current code is here [ExtendedExampleSource5](ExtendedExampleSource5) 

Lots of changes occurred since I updated here last. I have done the following: 

   * modified Zip() to optionally prevent the directory from being put into the zip path 
   * generated HTML files from sconscript calls 
   * found out about Value() too late to use it. Value(s) returns a node, the "source" is the string 's' and, best of all, it creates a dependency against it. In other words, if you change the string parameter in Value(s), it will cause a re-build to occur. Perfect for generating HTML files! 
   * created a bunch of wrapper functions to help spew out the files and the matching index pages. see [http://www.arrizza.com/miscdownloads/miscdownloads.html](http://www.arrizza.com/miscdownloads/miscdownloads.html) for an example of the index page. This page sets up a table that contains hrefs to a bunch of project pages. Each project page contains a main page, a zip file, and a page that lists source code. 
   * sconstruct is roughly 1200 lines and the individual sconscripts have become more complex. However the structure is pretty simple and the sconscripts are more or less independent of where they're located in the directory structure. This means I can move projects around if I want to with very little change to the build system. 
To do: 

   * finish doing the snippets page and projects [http://www.arrizza.com/snippets/snippets.html](http://www.arrizza.com/snippets/snippets.html) . This is a bit more complicated index than the others but should be still fairly straightforward. 
   * start working on sending the files from the staging area to the actual website 
   * tighten up some of the dependencies. It's still relatively loosely defined what gets built and what doesn't when a target is named 
   * extract out some of the HTML generating code into it's own .py 

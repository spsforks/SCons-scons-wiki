**Table of Contents**

[TOC]

Looking around on the Internet, a lot of places can be found where people complain about SCons being horrendously slow, up to the point that it's unusable (for them). One of the most prominent ones seems to be a series of blog articles by Eric Melski: 
* [http://blog.melski.net/2011/05/23/why-is-scons-so-slow/](http://blog.melski.net/2011/05/23/why-is-scons-so-slow/) 
* [http://www.electric-cloud.com/blog/2010/03/08/how-scalable-is-scons/](http://www.electric-cloud.com/blog/2010/03/08/how-scalable-is-scons/) 
* [http://www.electric-cloud.com/blog/2010/07/21/a-second-look-at-scons-performance/](http://www.electric-cloud.com/blog/2010/07/21/a-second-look-at-scons-performance/) 
* [http://www.electric-cloud.com/blog/2010/08/11/the-last-word-on-scons-performance/](http://www.electric-cloud.com/blog/2010/08/11/the-last-word-on-scons-performance/) 
* [http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/](http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/) 
Another, often linked and cited, comparison that makes SCons look extremely bad is: 

* [http://gamesfromwithin.com/the-quest-for-the-perfect-build-system](http://gamesfromwithin.com/the-quest-for-the-perfect-build-system) 
* [http://gamesfromwithin.com/the-quest-for-the-perfect-build-system-part-2](http://gamesfromwithin.com/the-quest-for-the-perfect-build-system-part-2) 
* [http://gamesfromwithin.com/bad-news-for-scons-fans](http://gamesfromwithin.com/bad-news-for-scons-fans) 
Several users jump on the same train, e.g.: 

* [http://softwareswirl.blogspot.de/2009/08/benchmarking-build-systems.html](http://softwareswirl.blogspot.de/2009/08/benchmarking-build-systems.html) 
Finally, there is the very detailed wonderbuild benchmark at: 

* [http://www.retropaganda.info/~bohan/work/psycle/branches/bohan/wonderbuild/benchmarks/time.xml](http://www.retropaganda.info/~bohan/work/psycle/branches/bohan/wonderbuild/benchmarks/time.xml) 
On the other hand, in our mailing lists we don't very often hear from desperate users that need help speeding up their builds. 

So what's true? Does SCons get slow on large builds? And exactly when does this happen and why? 

In order to possibly answer some of these questions, I started my own investigations. This meant running a lot of SCons builds under various conditions and recording and evaluating the results. 


# Reviewing the Taskmaster

In this first part of my investigations, I concentrated on busting the myth that SCons' Taskmaster would show quadratic time complexity behaviour. My basic approach for this was to double up the number of C/CPP files for a given benchmark project, and then compare the profiling output. I assumed that a badly designed Taskmaster would lead to a large increase of running time for the "tasking" parts. 


## Repositories

All the results of the following discussion can be downloaded as `hg` (Mercurial) repo from [http://www.bitbucket.org/dirkbaechle/scons_testresults](http://www.bitbucket.org/dirkbaechle/scons_testresults). In separate folders you can find the raw result data and the scripts that were used to run the examples. Look out for `README.rst` or `overview.rst` files, they contain some additional info about how things work and what the single subdirectories contain. 

Additionally, I created a separate SCons testsuite which is available at [http://www.bitbucket.org/dirkbaechle/scons_testsuite](http://www.bitbucket.org/dirkbaechle/scons_testsuite). It comprises several real-life projects, control scripts, and the supporting `sconstest` package for running all the timings and profilings. 

A warning: Both repos are rather large, so be prepared for some download time! 


## Linear scaling

This section presents results for SCons' "linear scaling" behaviour while running on a single core. With this I mean: "What happens when the number of source files gets doubled up in each step?" 


### Used machine

For all the tests and speedup comparisons in this section, I used the following machine setup 

* 2 Intel(R) Core(TM)2 Duo CPU E8300  @ 2.83GHz 
* 2 GB RAM 
* Ubuntu Linux 12.04.02 LTS (x86-64) 
* make 3.81 
* gcc 4.6.3 
* python 2.7.3 

### The genscons.pl script

This is the original script as used by Eric Melski in his comparison of SCons and make. I additionally downloaded the stable release of SCons v1.2.0 and installed it, just to be sure that I get as close to his setup as possible. 

The full set of results can be found in the `scons120_vs_make` folder of the `scons_testresults` repo. 

For a better comparison, here is the original result data by Eric Melski first (as published via `pastebin`). 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/melski.png) 

I ran my own series of builds as "clean build" (from scratch), "update" and as "implicit-deps-unchanged update" (for SCons only, with the command-line options `--max-drift=1 --implicit-deps-unchanged`). While doing so, the project sizes ranged from 2500 up to 16500 C files. 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/scons120.png) 

The measured times don't show a dramatic quadratic increase as claimed. You'll certainly notice that the X axis is scaled differently. That's because I couldn't reach any higher number of C files without my machine starting to swap memory. At the maximum of 16500 C files, SCons required about 1GB of RAM for a clean build, and the update runs as well. The rest of my total 2GB was taken by the OS, which makes me wonder how Eric Melski was able to reach those high numbers of files. By letting the machine swap freely? This would explain the increase of build times, starting at about 20000 C files in his data. 

Another thing is, that if a quadratic behaviour for the whole process can be seen, I'd expect at least one module or function to show `O(n**2)` behaviour or worse. I mean, if there were a design flaw to be found, it shouldn't affect the whole program/framework but only a part of it, like a module or a single function. This bug would then grow exponentially over the number of files, and drag the overall performance of SCons down. 

So I did a full profiling run with `cProfile.py` for the two project sizes `d` (8500 files) and `e` (16500 files). You'll find the complete results in the repo, with all the timings, memory consumption and `pstats` files. Here are the profiling results for an update run: 

[melski_update_d.svg](melski_update_d.svg) 

[melski_update_e.svg](melski_update_e.svg) 

which don't show any significant difference or increase for the percentage of runtime in each function. 

As my later experiments showed (see the section "Continued analysis" below), the number of files was still too small for the actual effects to kick in and create a clearly visible bump. 


### Switching to a more recent SCons version

A comparison of the ancient v1.2.0 with the recent v2.3.0 release (see the folder `scons230_vs_make/genscons` in the `scons_testresults` repo) didn't show any large differences in runtime behaviour. So for the remaining tests, I decided to switch to a current revision from latest development. 

I picked revision `#0c9c8aff8f46` of the SCons trunk. This means we talk about the stable 2.3.0 release, plus some additional patches towards 2.3.1 (right after replacing the documentation toolchain). 


### The generate_libs.py script

This is the script that was used by Noel Llopis in his "Quest for Performance" series. I downloaded it from the website, and disabled all other competitors except SCons and make. 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/scons230_qperf.png) 

The project sizes were 5000, 10000, 12500 and 15000 CPP files. All the results can be found in the `scons230_vs_make/questfperf/run_original` folder. 


### Wonderbuild

Then I ran the example script from the wonderbuild benchmark with the same numbers of source files. 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/scons230_wbuild.png) 

Find the full set of results in the `scons230_vs_make/wonderbuild/run_original` folder. 


### Patched sources

As for the Melski series, both of these additional benchmarks don't show a strictly quadratic scaling (I'm still investigating where the "hook" in the wonderbuild results for a clean build comes from). However, the differences between the times for make and SCons are rather large. 

The main reason for this is that the source files are actually empty, such that the compiler doesn't have anything to do. So the displayed times give a clue about the administrative overhead that each build system needs. But if I compile about 10000 CPP files, I certainly don't expect build times of 2 or 3 minutes. 

The CPP and header sources in all the three benchmarks above look something like: 


```txt
////////
Header:
////////

#ifndef class_0_h_
#define class_0_h_

class class_0 {
public:
    class_0();
    ~class_0();
};
#endif

////////
Source:
////////

#include "class_0.h"
<several other includes>

class_0::class_0() {}
class_0::~class_0() {}

```
I tried to get a more realistic comparison, by throwing in some functions that are actually doing stuff and use the STL to some extent: 


```txt
////////
Header:
////////

#ifndef class_0_h_
#define class_0_h_

#include <string>
#include <vector>
class class_0
{
public:
    class_0();
    ~class_0();
    class_0(const class_0 &elem);
    class_0 &operator=(const class_0 &elem);

    void addData(const std::string &value);
    void clear();
private:
    std::vector<std::string> data;
};

#endif

////////
Source:
////////

#include "class_0.h"
<several other includes>
using namespace std;

class_0::class_0()
{}

class_0::~class_0()
{}

class_0::class_0(const class_0 &elem)
{
  data = elem.data;
}

class_0 &class_0::operator=(const class_0 &elem)
{
  if (&elem == this)
  {
    return *this;
  }

  data = elem.data;

  return *this;
}

void class_0::clear()
{
  data.clear();
}

void class_0::addData(const string &value)
{
  data.push_back(value);
}
```
With these patched classes I ran another series for the "Quest for performance" and the "wonderbuild" benchmarks. 

Here are the results of the "Quest for performance" script:   

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/scons230_qperfp.png) 

and the "wonderbuild" setup: 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/scons230_wbuildp.png) 

. The full set of results can be found in the `run_patched` folder of `scons230_vs_make/questfperf` and `scons230_vs_make/wonderbuild`, respectively. 

The graphs show how make and SCons times converge when the build steps have some actual load. 


## Parallel builds

By a lucky coincidence, I could get access to two different multi-core machines for a week. So I seized the chance, wrote some scripts, and ran a full series of SCons/make builds with the parallel "-j" option enabled. My goal was to find out whether SCons has any scaling problems when building things in parallel. 


### Machines

The first of the machines was a quad-core 

* 4 Intel(R) Core(TM) i5 CPU 650 @ 3.20GHz 
* 4 GB RAM 
* SLES11 SP2, 32bit 
* Kernel 3.0.13-0.27-pae 
and the other had eight cores 

* 8 Intel(R) Xeon(R) CPU X3460  @ 2.80GHz 
* 4 GB RAM 
* SLES10 SP3, 32bit 
* Kernel 2.6.16.60-0.54.5-bigsmp 

### Results

You can find all results and speedup graphs in the `scons230_vs_make/parallel` folder and its subdirectories. Please read the `README/overview.rst` files for getting a better overview. 

In general the results show that the parallel speedups for SCons and make are on par, following are two example graphs. The first was run on the quad core machine and shows the "Quest for performance" results to the left, and the "wonderbuild" speedup to the right: 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/speedup_quad.png) 

I repeated the same experiment on the octa core machine, but let the number of threads range between 1 and 12 (again the "wonderbuild" graph is to the right): 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/speedup_octa.png) 

As an example of what's actually behind these graphs, here's the full array of single runs from `-j1` to `-j12` for the wonderbuild benchmark on the octa core system: 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/parallel_wbuild_1_12.png) 


# Testsuite and `fastcpp` Tool

So far, we've seen that SCons doesn't perform that bad and with that I mean "It seems to scale pretty well.". To me this indicates that our Taskmaster is doing a good job (despite common belief) and we don't have a more general problem in our source code where quadratic, or higher, complexity goes havoc. Still the update times could probably be a little smaller, which raises the questions 

* For what is the overhead of time used in SCons? 
* Are there any places for improvement? 
I searched the Internet and collected some [OpenSource](OpenSource) projects that use SCons as their build system. Adding the benchmarks above, I compiled a small testsuite for timing and profiling different revisions. This made it easier to tell whether code changes actually improve the performance and in which parts. 

You can find the resulting little test framework at 

* [http://www.bitbucket.org/dirkbaechle/scons_testsuite](http://www.bitbucket.org/dirkbaechle/scons_testsuite) 
If you're interested enough to give it a go, please consult its `README.rst` file in the top-level folder to understand how things work.  

Disclaimer: It's currently not in a state of "running everywhere", but especially crafted for my very own Ubuntu Linux machine. So, if you try to start the examples on your own, be prepared to run into some pitfalls. You might have to adapt the controlling scripts, or even need to patch the software packages themselves...including the installation of special packages as prerequisites.  


## Results

With this testsuite I profiled the `#0c9c8aff8f46` revision of SCons v2.3.0 mentioned above, in order to have some figures for reference. I won't go into full detail about all the different profiling and results graphs, just check the `testresults/default` folder for yourself. 

In general, the running time of SCons is distributed over a lot of different modules and functions, making it difficult to identify a single place that is suited for optimization. However, by cycling through patching the source code and rerunning the tests I found two places where a lot of time gets spent on the wrong things in my opinion. At least this is where we could spare a few cycles, especially for large projects with a lot of C/CPP files: 

1. The prefixes and suffixes for programs, objects and libraries in the default C/CPP builders are set as variables. For example the `Program` Builder in `src/engine/SCons/Tool/__init__.py`, ll. 196, uses:

```
#!python
prefix = '$PROGPREFIX',
suffix = '$PROGSUFFIX',
src_suffix = '$OBJSUFFIX',
```

This means that they have to get substituted every time a corresponding target gets built. 
1. Somewhat related to this is the flexibility that we offer when specifiying C/CPP source files. By adding a large list of different scanners for file suffixes,
```
#!python
CSuffixes = [".c", ".C", ".cxx", ".cpp", ".c++", ".cc",
             ".h", ".H", ".hxx", ".hpp", ".hh",
             ".F", ".fpp", ".FPP",
             ".m", ".mm",
             ".S", ".spp", ".SPP", ".sx"]
 
```
, `src/engine/SCons/Tool/__init__.py`, ll. 64, we have to check against them for each source file we encounter. When a user knows that he only has CPP files to process, there is simply no need to check for FORTRAN... 
So my ideas for improvements were: 

1. Set suffixes to fixed strings for each OS in a special "fast C/CPP"-Tool. 
1. In the same manner, restrict the number of possible source file suffixes to a customizable extension, like ".cpp". 
These observations have led to the development of another external Tool called "fastcpp". It's listed in the [ToolsIndex](ToolsIndex) and can be loaded on top of a normal C/CPP building environment. 

But mind the warning: It's still in a very experimental state and probably not ready for production work! 

The following picture shows the update times of SCons with the `fastcpp` tool, against make: 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/fastcpp_update.png) 

and a comparison of SCons updates with/without the new builder: 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/fastcpp_compare_update.png) 

All the results and scripts for the `fastcpp` builder can be found in the folder  `scons_testresults/scons230_trace/fastcpp`. 


# Continued speed analysis

Led by Eric Melski's remarks in his latest article 

* [http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/](http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/) 
, I was finally able to reproduce his results on a larger machine with 8GB RAM. The following graphs and figures are all based on a simplified version of the benchmark, where the actual compiler and linker calls are replaced by the "echo" command. This means faster runtimes for the program and the benchmarks, while still showing the same basic behaviour. 

Here are the result graphs for my machine, using CPython (left) and [PyPy](PyPy) (right): 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/cpython_pypy.png) 

I checked both Python interpreters because I found some notices on the Internet that [PyPy](PyPy) wouldn't suffer from the same memory `realloc` problems as CPython. This turned out to be partly true, and [PyPy](PyPy) obviously has a somewhat lesser runtime increase...but it's still there. 

I also found this thread 

* [https://mail.python.org/pipermail//portland/2011-August/001132.html](https://mail.python.org/pipermail//portland/2011-August/001132.html) 
, and tried disabling the [GarbageCollector](GarbageCollector) for a full SCons run. But this didn't help at all and made runtimes even worse... 

As Eric found out during his profilings, SCons would spend a lot of time in system call related methods like `waitpid` and `fork`. So I started to have a close look at the internals, by traceing the whole run with `strace`. The results (see folders `scons230_trace/strace` and `strace_orig_logs` in the `scons_testresults` repo) seemed to hint at problems with either the `realloc` of CPython's memory allocation, or the futex management in the Kernel. While comparing the running times of single system calls as recorded by strace, the two methods `mremap` and `set_robust_list` increased their runtime linearly during a build (while the memory usage went up). 

The following image displays the difference in accumulated time for two single compile commands (first, second) over the number of required syscalls. While the "first" graph was captured at the start of the build (within the first ten targets), the "second" evaluation is close to the end:  

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/strace_cpython.png) 

It shows how the time needed for a single compile increases, throughout the build of the full project. So I patched the SCons sources, such that no shell/process would be spawned but only the target files got created by `touch`ing them in Python directly. 


```txt
# HG changeset patch
# Parent d53323337b3accbe3b88280fd0597580a1b5e894
diff -r d53323337b3a -r 1fc40f790145 src/engine/SCons/Action.py
--- a/src/engine/SCons/Action.py        Sun Jan 05 13:27:10 2014 +0100
+++ b/src/engine/SCons/Action.py        Thu Jan 09 09:16:10 2014 +0100
@@ -801,17 +801,22 @@
             source = executor.get_all_sources()
         cmd_list, ignore, silent = self.process(target, list(map(rfile, source)), env, executor)

+        for t in target:
+            tf = open(str(t),"w")
+            tf.write("\n")
+            tf.close()
+
         # Use len() to filter out any "command" that's zero-length.
-        for cmd_line in filter(len, cmd_list):
-            # Escape the command line for the interpreter we are using.
-            cmd_line = escape_list(cmd_line, escape)
-            result = spawn(shell, escape, cmd_line[0], cmd_line, ENV)
-            if not ignore and result:
-                msg = "Error %s" % result
-                return SCons.Errors.BuildError(errstr=msg,
-                                               status=result,
-                                               action=self,
-                                               command=cmd_line)
+        #for cmd_line in filter(len, cmd_list):
+        #    # Escape the command line for the interpreter we are using.
+        #    cmd_line = escape_list(cmd_line, escape)
+        #    result = spawn(shell, escape, cmd_line[0], cmd_line, ENV)
+        #    if not ignore and result:
+        #        msg = "Error %s" % result
+        #        return SCons.Errors.BuildError(errstr=msg,
+        #                                       status=result,
+        #                                       action=self,
+        #                                       command=cmd_line)
         return 0

     def get_presig(self, target, source, env, executor=None):
```
Then I ran the full benchmark again, with the following results (again CPython to the left, and [PyPy](PyPy) on the right side): 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/cpython_pypy_touch.png) 

In comparison to the results above, these curves clearly show how a large overhead gets introduced by spawning shells and waiting for the processes to finish. SCons itself (finding/processing tasks, keeping track of build signatures, scanning of implicit dependencies) appears to scale just fine. 

Inspired by Trevor Highland and his comment in [http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/](http://blog.melski.net/2013/12/11/update-scons-is-still-really-slow/), I wrote this little Python script that spawns single processes in quick succession. By allocating more and more memory at the same time, the runtimes for the single process calls seem to grow. 


```txt
import os
import sys

perc='%'

def main():
    cycles = 25000
    append = True
    if len(sys.argv) > 1:
        cycles = int(sys.argv[1])
    if len(sys.argv) > 2:
        append = False

    print "Starting %d cycles..." % cycles
    m_list = []
    cnt = 0
    for i in xrange(cycles):
        cnt += 1
        args = ['echo', '%d/%d (%.2f%s)' % (cnt, cycles, float(cnt)*100.0/float(cycles), perc)]
        os.spawnvpe(os.P_WAIT, args[0], args, os.environ)
        signature ='A'*20000
        if append:
            m_list.append(signature)

    print "Done."

if __name__ == "__main__":
    main()

```
I then rewrote this to a C program, again trying to mimic SCons' basic process of repeatedly building targets and then collecting build infos in memory: 


```txt
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAXCYCLES 32000
#define SIGLEN 20000

int main(int argc, char **argv)
{
    int cnt = 0;
    int cycles = MAXCYCLES;
    char echo_arg[100];
    pid_t child_pid;
    int child_status;


    if (argc > 1) {
        cycles = atoi(argv[1]);
        if (cycles > MAXCYCLES) {
            cycles = MAXCYCLES;
            printf("Warning: setting number of cycles to internal maximum of %d!", MAXCYCLES);
        }
    }

    printf("Starting %d cycles...\n", cycles);
    char *m_list[MAXCYCLES];
    for (; cnt < cycles; ++cnt) {
        sprintf(echo_arg, "%d/%d (%.2f%%)", cnt, cycles, ((double) cnt)*100.0/((double) cycles));

        printf("%s\n", echo_arg);
        child_pid = fork();
        if (child_pid == 0) {
            /* This is done by the child process. */
            execlp("echo", echo_arg, NULL);

            /* If execvp returns, it must have failed. */
            printf("Unknown command\n");
            exit(0);
        } else {
           /* This is run by the parent.  Wait for the child
              to terminate. */
           while (wait(&child_status) != child_pid)
               ;

        }
        m_list[cnt] = malloc(SIGLEN*sizeof(char));
        strcpy(m_list[cnt], echo_arg);
    }

    printf("Done.\n");
}
```
It should be compilable with: 


```txt
gcc -o spawn_test spawn_test.c
```
The running times for the latter C program on my machine, as measured with `/usr/bin/time`, are: 


```txt
cycles | elapsed time
---------------------

 2000  | 0:01.69
 4000  | 0:04.04
 8000  | 0:10.72
16000  | 0:32.51
32000  | 1:46.85
```
So, while the number of cycles (spawned processes) doubles in each step, the running time doesn't scale linearly with it.  

I asked about this problem on the `kernel-dev` mailing list and `glibc-help`. The Kernel list didn't deliver any answers (it was the wrong forum in hindsight), but some of the glibc users gave very helpful advice and insight in the following threads: 

* [https://sourceware.org/ml/libc-help/2014-01/msg00038.html](https://sourceware.org/ml/libc-help/2014-01/msg00038.html) spawning (exec*/wait) shows non-constant time if memory grows 
* [https://sourceware.org/ml/libc-help/2014-03/msg00015.html](https://sourceware.org/ml/libc-help/2014-03/msg00015.html) Memory consumption of iconv 

# The stubprocess.py wrapper

Many thanks go to Tzvetan Mikov, who volunteered and found the place in the code where `fork` does its bad things: 

* "It is happening in the kernel: fork() needs to duplicate all page table entries of the parent process,  so by definition its cost is proportional to the size of the address space. I don't think there is a big mystery there, unless I am missing something (which I might very well be) - it needs to do some amount of work for every 4K page of address space. You can examine kernel/fork.c:dup_mmap() and mm/memory.c:copy_page_range() in the kernel source (e.g. at [http://lxr.free-electrons.com/source/kernel/fork.c](http://lxr.free-electrons.com/source/kernel/fork.c) )" 
In parallel, the Parts team around Jason Kenny (Intel, Paris) reported to have experienced similar performance problems: 

* [http://two.pairlist.net/pipermail/scons-dev/2014-April/001260.html](http://two.pairlist.net/pipermail/scons-dev/2014-April/001260.html) 
* [http://two.pairlist.net/pipermail/scons-dev/2014-April/001263.html](http://two.pairlist.net/pipermail/scons-dev/2014-April/001263.html) 
They wrote a wrapper module (big thanks to its author Eugene Leskinen!) that is able to redefine the default subprocess.call() method. Under Posix systems it then uses the more lightweight posix_spawn() to create a new shell process. An option that is not directly available in the current implementations of the standard subprocess Python module. 

This extension provides a significant speedup, because the slow `fork` is out of the way. Here are the runtimes (see also folder `scons230_trace/stubprocess` in the `scons_testresults` repo) for a clean build, compared to make: 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/compare_clean_make.png) 

and compared to the default spawn method: 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/compare_clean.png) 

We also compared the runtimes between SCons and make, for the patched sources (using STL to make up for more realistic CPP files) of the "Quest for performance" example from above (see the folder `scons230_trace/stubprocess_patched` in the `scons_testresults` repo): 

![](https://bytebucket.org/scons/scons/wiki/WhySconsIsNotSlow/stubprocess_patched.png) 

One can see how build times are only about 20% higher than for make, and if your CPP sources happen to be a "little more complicated" (driving the compile time for each source further up) you should be on the safe side...  

Our current plans ( see [http://scons.org/wiki/Roadmap](http://scons.org/wiki/Roadmap) ) include to integrate this wrapper to the next release 2.4 of SCons. 

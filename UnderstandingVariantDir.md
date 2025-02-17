Okay, I have been trying to beat SCons into submission several times and I kept staring at ``VariantDir`` and how it should affect me.  I *think* I understand it as well as the malfunction most people have with it.  `VariantDir()` *is* somewhat crappily named, but only somewhat.  It does what the developers say it does, but they tend to explain the rare use case of multiple build types rather than the common use case of a pristine source tree off in la la land.  So, we present: 

**Table of Contents**

[TOC]

_Comment by [GregNoel](GregNoel): First, there's too much detail, so much so that the (extremely valid) points get lost.  Second, any attempt to explain VariantDir that doesn't contrast it with Repository is flawed, because that's *exactly* what delivers "a pristine source tree off in la la land."  Third, ``VariantDir`` is badly conflated with the [SCons build model](UsingVariantDir), so that should be discussed here as well.  Please contact me directly for more detailed suggestions._ 


# Andy's 3 Step Guide To ``VariantDir()``


## Step 1: ``VariantDir()`` isn't the droid you're looking for

If your use case is "Get SCons to quit putting !@#$ in the same directory as my SConscript file and put it over <ins>there</ins> instead."  You want the variant_dir argument to SConscript().  Stop here. 


## Step 2: ``VariantDir()`` might be the droid you're looking for

If your use case is "I have this external source tree that I can't pull directly under my SCons directories and can't put an SConscript in it, but I still need to build it without putting SCons droppings all over it."  You probably want `VariantDir()`.  To me, this is the most common case because it resembles the pristine "source" directory that people familiar with GNU want. 


## Step 3: ``VariantDir()`` is definitely the droid you're looking for

If your use case is "I need multiple types of builds and targets built simultaneously."  You almost certainly want ``VariantDir()``.  I won't cover this case here as this is what the main developers cover at length in their descriptions.  I couldn't possibly explain this as well as they do since I don't really use it yet. 


# Examples:


## Step 1: ``VariantDir()`` isn't the droid you're looking for

Let's look at a fairly simple example of an sconstruct.  What is in the sconscript isn't so relevant, yet.  Here is what things look like: 


```console
[nds@localhost unix]$ pwd
/home/nds/lwip-scons/contrib/ports/unix
[nds@localhost unix]$ ls -alR
.:
total 16
drwxr-xr-x  3 nds nds 4096 Apr 12 22:34 .
drwxr-xr-x 11 nds nds 4096 Apr 12 17:55 ..
drwxr-xr-x  2 nds nds 4096 Apr 12 21:58 bfs
-rw-r--r--  1 nds nds  580 Apr 12 22:34 sconstruct
./bfs:
total 12
drwxr-xr-x 2 nds nds 4096 Apr 12 21:58 .
drwxr-xr-x 3 nds nds 4096 Apr 12 22:34 ..
-rw-r--r-- 1 nds nds 1328 Apr 12 21:56 sconscript
```
sconstruct 
```python
import SCons

rootEnv = Environment(
    BUILDROOT="BUILD",
    ENV={"PATH": [".", "/bin", "/usr/bin", "/opt/bin", "/usr/local/bin"]},
)
liblwip4Env = rootEnv.Clone()
env = liblwip4Env
Export("env")
liblwip4 = liblwip4Env.SConscript("bfs/sconscript", exports="env")
# liblwip4 = liblwip4Env.SConscript(
#     "bfs/sconscript", variant_dir="$BUILDROOT/LIBLWIP4", exports="env"
# )
```
And here's what happens when we run that sconstruct: 


```console
[nds@localhost unix]$ scons -Q
<Lots of compiler output elided>
[nds@localhost unix]$ pwd
/home/nds/lwip-scons/contrib/ports/unix
[nds@localhost unix]$ ls -alR
.:
total 40
drwxr-xr-x  3 nds nds  4096 Apr 12 22:38 .
drwxr-xr-x 11 nds nds  4096 Apr 12 17:55 ..
drwxr-xr-x  5 nds nds  4096 Apr 12 22:38 bfs
-rw-r--r--  1 nds nds 21445 Apr 12 22:38 .sconsign.dblite
-rw-r--r--  1 nds nds   580 Apr 12 22:34 sconstruct
./bfs:
total 152
drwxr-xr-x 5 nds nds   4096 Apr 12 22:38 .
drwxr-xr-x 3 nds nds   4096 Apr 12 22:38 ..
drwxr-xr-x 2 nds nds   4096 Apr 12 22:38 API
drwxr-xr-x 3 nds nds   4096 Apr 12 22:38 CORE
-rw-r--r-- 1 nds nds 123160 Apr 12 22:38 liblwip4.a
drwxr-xr-x 2 nds nds   4096 Apr 12 22:38 NETIF
-rw-r--r-- 1 nds nds   1328 Apr 12 21:56 sconscript
./bfs/API:
total 136
drwxr-xr-x 2 nds nds  4096 Apr 12 22:38 .
drwxr-xr-x 5 nds nds  4096 Apr 12 22:38 ..
-rw-r--r-- 2 nds nds 15393 Apr 12 17:55 api_lib.c
-rw-r--r-- 1 nds nds  6192 Apr 12 22:38 api_lib.o
-rw-r--r-- 2 nds nds 18548 Apr 12 17:55 api_msg.c
-rw-r--r-- 1 nds nds  6836 Apr 12 22:38 api_msg.o
-rw-r--r-- 2 nds nds  2612 Apr 12 17:55 err.c
-rw-r--r-- 1 nds nds   647 Apr 12 22:38 err.o
-rw-r--r-- 2 nds nds 40205 Apr 12 17:55 sockets.c
-rw-r--r-- 1 nds nds 11160 Apr 12 22:38 sockets.o
-rw-r--r-- 2 nds nds  8782 Apr 12 17:55 tcpip.c
-rw-r--r-- 1 nds nds  3876 Apr 12 22:38 tcpip.o
<other directories elided>
```
Lots of stuff gets dumped under the bfs directory because that is where the sconscript is located and executed.  If that's what you want, great!  However, if you want your scons droppings to go elsewhere, you need to add the "variant_dir" flag to your SConscript call in your sconstruct like so: 


```console
[nds@localhost unix]$ pwd
/home/nds/lwip-scons/contrib/ports/unix
[nds@localhost unix]$ ls -alR
.:
total 16
drwxr-xr-x  3 nds nds 4096 Apr 12 22:46 .
drwxr-xr-x 11 nds nds 4096 Apr 12 17:55 ..
drwxr-xr-x  2 nds nds 4096 Apr 12 22:45 bfs
-rw-r--r--  1 nds nds  579 Apr 12 22:46 sconstruct
./bfs:
total 12
drwxr-xr-x 2 nds nds 4096 Apr 12 22:45 .
drwxr-xr-x 3 nds nds 4096 Apr 12 22:46 ..
-rw-r--r-- 1 nds nds 1328 Apr 12 21:56 sconscript
```
sconstruct 
```python
import SCons

rootEnv = Environment(
    BUILDROOT="BUILD",
    ENV={"PATH": [".", "/bin", "/usr/bin", "/opt/bin", "/usr/local/bin"]},
)
liblwip4Env = rootEnv.Clone()
env = liblwip4Env
Export("env")
# liblwip4 = liblwip4Env.SConscript("bfs/sconscript", exports="env")
liblwip4 = liblwip4Env.SConscript(
    "bfs/sconscript", variant_dir="$BUILDROOT/LIBLWIP4", exports="env"
)
```
And upon running that sconstruct: 


```console
[nds@localhost unix]$ scons -Q
<Lots of compiler output elided>
[nds@localhost unix]$ ls -alR
.:
total 44
drwxr-xr-x  4 nds nds  4096 Apr 12 22:48 .
drwxr-xr-x 11 nds nds  4096 Apr 12 17:55 ..
drwxr-xr-x  2 nds nds  4096 Apr 12 22:45 bfs
drwxr-xr-x  3 nds nds  4096 Apr 12 22:48 BUILD
-rw-r--r--  1 nds nds 21833 Apr 12 22:48 .sconsign.dblite
-rw-r--r--  1 nds nds   579 Apr 12 22:46 sconstruct
./bfs:
total 12
drwxr-xr-x 2 nds nds 4096 Apr 12 22:45 .
drwxr-xr-x 4 nds nds 4096 Apr 12 22:48 ..
-rw-r--r-- 2 nds nds 1328 Apr 12 21:56 sconscript
./BUILD:
total 12
drwxr-xr-x 3 nds nds 4096 Apr 12 22:48 .
drwxr-xr-x 4 nds nds 4096 Apr 12 22:48 ..
drwxr-xr-x 5 nds nds 4096 Apr 12 22:48 LIBLWIP4
./BUILD/LIBLWIP4:
total 152
drwxr-xr-x 5 nds nds   4096 Apr 12 22:48 .
drwxr-xr-x 3 nds nds   4096 Apr 12 22:48 ..
drwxr-xr-x 2 nds nds   4096 Apr 12 22:48 API
drwxr-xr-x 3 nds nds   4096 Apr 12 22:48 CORE
-rw-r--r-- 1 nds nds 123300 Apr 12 22:48 liblwip4.a
drwxr-xr-x 2 nds nds   4096 Apr 12 22:48 NETIF
-rw-r--r-- 2 nds nds   1328 Apr 12 21:56 sconscript
./BUILD/LIBLWIP4/API:
total 136
drwxr-xr-x 2 nds nds  4096 Apr 12 22:48 .
drwxr-xr-x 5 nds nds  4096 Apr 12 22:48 ..
-rw-r--r-- 2 nds nds 15393 Apr 12 17:55 api_lib.c
-rw-r--r-- 1 nds nds  6192 Apr 12 22:48 api_lib.o
-rw-r--r-- 2 nds nds 18548 Apr 12 17:55 api_msg.c
-rw-r--r-- 1 nds nds  6836 Apr 12 22:48 api_msg.o
-rw-r--r-- 2 nds nds  2612 Apr 12 17:55 err.c
-rw-r--r-- 1 nds nds   647 Apr 12 22:48 err.o
-rw-r--r-- 2 nds nds 40205 Apr 12 17:55 sockets.c
-rw-r--r-- 1 nds nds 11168 Apr 12 22:48 sockets.o
-rw-r--r-- 2 nds nds  8782 Apr 12 17:55 tcpip.c
-rw-r--r-- 1 nds nds  3888 Apr 12 22:48 tcpip.o
<other directory listings removed>
```
Hey, Presto!  All of the files got placed under the subdirectory BUILD/LIBLWIP4 just like we specified. Congratulations, if all you wanted was to make scons generate files away from your sconscript file and its directory, you're done. If not, read on ... 


## Step 2: ``VariantDir()`` might be the droid you're looking for

"Hey!", you say.  "Where did all those files come from?  We don't have anything to create those."  This is where ``VariantDir()`` comes in. This time we're going to focus on the sconscript down in the bfs subdirectory. For these examples, I'm going to leave the variant_dir in place in the sconstruct as I don't want files going all over my nice, clean areas with sconstruct and sconscript. So, let's take a look at that sconscript, shall we: 


```console
[nds@localhost unix]$ pwd
/home/nds/lwip-scons/contrib/ports/unix
```
bfs/sconscript 
```python
Import(["env"])
# Should be called SourcePrefixMap or something ...
VariantDir("CORE/", "/home/nds/lwip-scons/lwip/src/core/")
VariantDir("API/", "/home/nds/lwip-scons/lwip/src/api/")
VariantDir("NETIF/", "/home/nds/lwip-scons/lwip/src/netif/")
env.Replace(
    CPPPATH=[
        "/home/nds/lwip-scons/lwip/src/include",
        "/home/nds/lwip-scons/lwip/src/include/ipv4",
        # FIXME: This path is to include arch/cc.h.
        "/home/nds/lwip/contrib/ports/unix/include",
        # FIXME: This path is to grab lwipopts.h
        "/home/nds/lwip/contrib/ports/unix/proj/unix_bsd_echoserver",
    ]
)
# In "core" subdir
coreFiles = [
    "CORE/mem.c",
    "CORE/memp.c",
    "CORE/netif.c",
    "CORE/pbuf.c",
    "CORE/raw.c",
    "CORE/stats.c",
    "CORE/sys.c",
    "CORE/tcp.c",
    "CORE/tcp_in.c",
    "CORE/tcp_out.c",
    "CORE/udp.c",
    "CORE/dhcp.c",
]
# In "core/ipv4" subdir
core4Files = [
    "CORE/ipv4/icmp.c",
    "CORE/ipv4/igmp.c",
    "CORE/ipv4/ip_addr.c",
    "CORE/ipv4/ip.c",
    "CORE/ipv4/ip_frag.c",
]
# In "api" subdir
apiFiles = [
    "API/api_lib.c",
    "API/api_msg.c",
    "API/tcpip.c",
    "API/err.c",
    "API/sockets.c",
]
# In "netif" subdir
netifFiles = ["NETIF/loopif.c", "NETIF/etharp.c", "NETIF/slipif.c"]
liblwip4 = env.StaticLibrary("lwip4", [coreFiles, core4Files, apiFiles, netifFiles])
Return("liblwip4")
```
Whoa!  What the ... ?!?!  *3* ``VariantDir()``'s?  Capital letters in directories that don't exist?!?!  Source files that appear from nowhere?  What is going on? 

What is happening is that ``VariantDir()`` is being used to pull files from an area outside of the direct control of scons and build those files under the control of scons.  If you can add an sconscript to the source directory, you really shouldn't be playing with ``VariantDir()``.  In this instance, the lwip library is outside of our control and cannot be saddled with an sconscript, yet is sufficiently dependent that we have to rebuild it with the local application.  This is a prime example for ``VariantDir()``. 

In my opinion, right here is the crux of the ``VariantDir()`` misunderstandings.  ``VariantDir()`` does *two* separate things of which one isn't explained very often.  I have chosen to use capital letters to highlight the fact that there are two things occurring simultaneously. 


### A) ``VariantDir()```` sets up a prefix to original directory substitution for target files

This is the task which isn't discussed very explicitly.  The line: 
```python
VariantDir("CORE/", "/home/nds/lwip-scons/lwip/src/core/")
```
sets up a mapping such that references to targets named "CORE/foo.c" (prefix/file) get filled out to "/home/nds/lwip-scons/lwip/src/core/foo.c" (original directory/file).  Here is the key: 

THE PREFIX HAS NO MEANING OR RELATION TO THE MAPPING OTHER THAN AS A PURE VARIABLE SUBSTITUTION. 

we could have set up a line: 


```python
VariantDir("BELCH/", "/home/nds/lwip-scons/lwip/src/core/")
```
at which point "BELCH/foo.c" would get filled out to "/home/nds/lwip-scons/lwip/src/core/foo.c".  So, what changes would we have to make to the sconscript file if we used "BELCH" as the prefix?  We would have to use: 


```python
# In "core" subdir
coreFiles = ["BELCH/mem.c", "BELCH/memp.c", "BELCH/netif.c", "BELCH/pbuf.c", "BELCH/raw.c",
             "BELCH/stats.c", "BELCH/sys.c", "BELCH/tcp.c", "BELCH/tcp_in.c", "BELCH/tcp_out.c",
             "BELCH/udp.c", "BELCH/dhcp.c"]
# In "core/ipv4" subdir
core4Files = ["BELCH/ipv4/icmp.c",  "BELCH/ipv4/igmp.c",  "BELCH/ipv4/ip_addr.c",
              "BELCH/ipv4/ip.c",  "BELCH/ipv4/ip_frag.c"]
```

### B) ``VariantDir()`` copies the external files from the source directory into the working area.

In doing so, ``VariantDir()`` has to put those files into the working area somewhere so that it can avoid name collisions.  It does so by setting the build directory equivalent to prefix name. 

*This* is the fact that everybody focuses on and gives ``VariantDir()`` its' name.  Going back to the original sconscript, let's take a look at the organization of the build directory after scons gets through running: 


```console
[nds@localhost unix]$ pwd
/home/nds/lwip-scons/contrib/ports/unix
```
bfs/sconscript  
```python
Import(["env"])

# Should be called SourcePrefixMap or something ...
VariantDir("CORE/", "/home/nds/lwip-scons/lwip/src/core/")
VariantDir("API/", "/home/nds/lwip-scons/lwip/src/api/")
VariantDir("NETIF/", "/home/nds/lwip-scons/lwip/src/netif/")

env.Replace(
    CPPPATH=[
        "/home/nds/lwip-scons/lwip/src/include",
        "/home/nds/lwip-scons/lwip/src/include/ipv4",
        # FIXME: This path is to include arch/cc.h.
        "/home/nds/lwip/contrib/ports/unix/include",
        # FIXME: This path is to grab lwipopts.h
        "/home/nds/lwip/contrib/ports/unix/proj/unix_bsd_echoserver",
    ]
)

# In "core" subdir
coreFiles = [
    "CORE/mem.c",
    "CORE/memp.c",
    "CORE/netif.c",
    "CORE/pbuf.c",
    "CORE/raw.c",
    "CORE/stats.c",
    "CORE/sys.c",
    "CORE/tcp.c",
    "CORE/tcp_in.c",
    "CORE/tcp_out.c",
    "CORE/udp.c",
    "CORE/dhcp.c",
]

# In "core/ipv4" subdir
core4Files = [
    "CORE/ipv4/icmp.c",
    "CORE/ipv4/igmp.c",
    "CORE/ipv4/ip_addr.c",
    "CORE/ipv4/ip.c",
    "CORE/ipv4/ip_frag.c",
]

# In "api" subdir
apiFiles = [
    "API/api_lib.c",
    "API/api_msg.c",
    "API/tcpip.c",
    "API/err.c",
    "API/sockets.c",
]

# In "netif" subdir
netifFiles = ["NETIF/loopif.c", "NETIF/etharp.c", "NETIF/slipif.c"]

liblwip4 = env.StaticLibrary("lwip4", [coreFiles, core4Files, apiFiles, netifFiles])
Return("liblwip4")
```

```console
[nds@localhost unix]$ scons -Q
<Lots of compiler output elided>
[nds@localhost unix]$ ls -alR
.:
total 44
drwxr-xr-x  4 nds nds  4096 Apr 12 23:37 .
drwxr-xr-x 11 nds nds  4096 Apr 12 17:55 ..
drwxr-xr-x  2 nds nds  4096 Apr 12 22:45 bfs
drwxr-xr-x  3 nds nds  4096 Apr 12 23:37 BUILD
-rw-r--r--  1 nds nds 21833 Apr 12 23:37 .sconsign.dblite
-rw-r--r--  1 nds nds   579 Apr 12 22:46 sconstruct

./bfs:
total 12
drwxr-xr-x 2 nds nds 4096 Apr 12 22:45 .
drwxr-xr-x 4 nds nds 4096 Apr 12 23:37 ..
-rw-r--r-- 2 nds nds 1328 Apr 12 21:56 sconscript

./BUILD:
total 12
drwxr-xr-x 3 nds nds 4096 Apr 12 23:37 .
drwxr-xr-x 4 nds nds 4096 Apr 12 23:37 ..
drwxr-xr-x 5 nds nds 4096 Apr 12 23:37 LIBLWIP4

./BUILD/LIBLWIP4:
total 152
drwxr-xr-x 5 nds nds   4096 Apr 12 23:37 .
drwxr-xr-x 3 nds nds   4096 Apr 12 23:37 ..
drwxr-xr-x 2 nds nds   4096 Apr 12 23:37 API
drwxr-xr-x 3 nds nds   4096 Apr 12 23:37 CORE
-rw-r--r-- 1 nds nds 123300 Apr 12 23:37 liblwip4.a
drwxr-xr-x 2 nds nds   4096 Apr 12 23:37 NETIF
-rw-r--r-- 2 nds nds   1328 Apr 12 21:56 sconscript

./BUILD/LIBLWIP4/API:
total 136
drwxr-xr-x 2 nds nds  4096 Apr 12 23:37 .
drwxr-xr-x 5 nds nds  4096 Apr 12 23:37 ..
-rw-r--r-- 2 nds nds 15393 Apr 12 17:55 api_lib.c
-rw-r--r-- 1 nds nds  6192 Apr 12 23:37 api_lib.o
<further listing truncated>

./BUILD/LIBLWIP4/CORE:
total 392
drwxr-xr-x 3 nds nds  4096 Apr 12 23:37 .
drwxr-xr-x 5 nds nds  4096 Apr 12 23:37 ..
-rw-r--r-- 2 nds nds 55149 Apr 12 17:55 dhcp.c
-rw-r--r-- 1 nds nds   648 Apr 12 23:37 dhcp.o
drwxr-xr-x 2 nds nds  4096 Apr 12 23:37 ipv4
<further listing truncated>

./BUILD/LIBLWIP4/CORE/ipv4:
total 104
drwxr-xr-x 2 nds nds  4096 Apr 12 23:37 .
drwxr-xr-x 3 nds nds  4096 Apr 12 23:37 ..
-rw-r--r-- 2 nds nds  6268 Apr 12 17:55 icmp.c
-rw-r--r-- 1 nds nds  3248 Apr 12 23:37 icmp.o
<further listing truncated>

./BUILD/LIBLWIP4/NETIF:
total 76
drwxr-xr-x 2 nds nds  4096 Apr 12 23:37 .
drwxr-xr-x 5 nds nds  4096 Apr 12 23:37 ..
-rw-r--r-- 2 nds nds 33201 Apr 12 17:55 etharp.c
-rw-r--r-- 1 nds nds  8252 Apr 12 23:37 etharp.o
<further listing truncated>
```
scons has created the directories API, CORE, and NETIF underneath the working directory (BUILD/LIBLWIP4).  It has then copied the .c files from the full pathname to populate those directories.  Finally, it compiled the copied .c files into the .o files for use building the library. 

So, to examine the relationship between everything, let's look at what would happen if we changed CORE to BELCH: 


```console
[nds@localhost unix]$ pwd
/home/nds/lwip-scons/contrib/ports/unix
```
bfs/sconscript 
```python
Import(["env"])

# Should be called SourcePrefixMap or something ...
VariantDir("BELCH/", "/home/nds/lwip-scons/lwip/src/core/")
VariantDir("API/", "/home/nds/lwip-scons/lwip/src/api/")
VariantDir("NETIF/", "/home/nds/lwip-scons/lwip/src/netif/")

env.Replace(
    CPPPATH=[
        "/home/nds/lwip-scons/lwip/src/include",
        "/home/nds/lwip-scons/lwip/src/include/ipv4",
        # FIXME: This path is to include arch/cc.h.
        "/home/nds/lwip/contrib/ports/unix/include",
        # FIXME: This path is to grab lwipopts.h
        "/home/nds/lwip/contrib/ports/unix/proj/unix_bsd_echoserver",
    ]
)

# In "core" subdir
coreFiles = [
    "BELCH/mem.c",
    "BELCH/memp.c",
    "BELCH/netif.c",
    "BELCH/pbuf.c",
    "BELCH/raw.c",
    "BELCH/stats.c",
    "BELCH/sys.c",
    "BELCH/tcp.c",
    "BELCH/tcp_in.c",
    "BELCH/tcp_out.c",
    "BELCH/udp.c",
    "BELCH/dhcp.c",
]

# In "core/ipv4" subdir
core4Files = [
    "BELCH/ipv4/icmp.c",
    "BELCH/ipv4/igmp.c",
    "BELCH/ipv4/ip_addr.c",
    "BELCH/ipv4/ip.c",
    "BELCH/ipv4/ip_frag.c",
]

# In "api" subdir
apiFiles = [
    "API/api_lib.c",
    "API/api_msg.c",
    "API/tcpip.c",
    "API/err.c",
    "API/sockets.c",
]

# In "netif" subdir
netifFiles = ["NETIF/loopif.c", "NETIF/etharp.c", "NETIF/slipif.c"]

liblwip4 = env.StaticLibrary("lwip4", [coreFiles, core4Files, apiFiles, netifFiles])
Return("liblwip4")
```

```console
[nds@localhost unix]$ scons -Q
<Lots of compiler output elided>
[nds@localhost unix]$ ls -alR
.:
total 44
drwxr-xr-x  4 nds nds  4096 Apr 12 23:43 .
drwxr-xr-x 11 nds nds  4096 Apr 12 17:55 ..
drwxr-xr-x  2 nds nds  4096 Apr 12 23:42 bfs
drwxr-xr-x  3 nds nds  4096 Apr 12 23:43 BUILD
-rw-r--r--  1 nds nds 21852 Apr 12 23:43 .sconsign.dblite
-rw-r--r--  1 nds nds   579 Apr 12 22:46 sconstruct

./bfs:
total 12
drwxr-xr-x 2 nds nds 4096 Apr 12 23:42 .
drwxr-xr-x 4 nds nds 4096 Apr 12 23:43 ..
-rw-r--r-- 2 nds nds 1346 Apr 12 23:42 sconscript

./BUILD:
total 12
drwxr-xr-x 3 nds nds 4096 Apr 12 23:43 .
drwxr-xr-x 4 nds nds 4096 Apr 12 23:43 ..
drwxr-xr-x 5 nds nds 4096 Apr 12 23:43 LIBLWIP4

./BUILD/LIBLWIP4:
total 152
drwxr-xr-x 5 nds nds   4096 Apr 12 23:43 .
drwxr-xr-x 3 nds nds   4096 Apr 12 23:43 ..
drwxr-xr-x 2 nds nds   4096 Apr 12 23:43 API
drwxr-xr-x 3 nds nds   4096 Apr 12 23:43 BELCH
-rw-r--r-- 1 nds nds 123312 Apr 12 23:43 liblwip4.a
drwxr-xr-x 2 nds nds   4096 Apr 12 23:43 NETIF
-rw-r--r-- 2 nds nds   1346 Apr 12 23:42 sconscript

./BUILD/LIBLWIP4/API:
total 136
drwxr-xr-x 2 nds nds  4096 Apr 12 23:43 .
drwxr-xr-x 5 nds nds  4096 Apr 12 23:43 ..
-rw-r--r-- 2 nds nds 15393 Apr 12 17:55 api_lib.c
-rw-r--r-- 1 nds nds  6192 Apr 12 23:43 api_lib.o
<further listing truncated>

./BUILD/LIBLWIP4/BELCH:
total 392
drwxr-xr-x 3 nds nds  4096 Apr 12 23:43 .
drwxr-xr-x 5 nds nds  4096 Apr 12 23:43 ..
-rw-r--r-- 2 nds nds 55149 Apr 12 17:55 dhcp.c
-rw-r--r-- 1 nds nds   648 Apr 12 23:43 dhcp.o
drwxr-xr-x 2 nds nds  4096 Apr 12 23:43 ipv4
<further listing truncated>

./BUILD/LIBLWIP4/BELCH/ipv4:
total 104
drwxr-xr-x 2 nds nds  4096 Apr 12 23:43 .
drwxr-xr-x 3 nds nds  4096 Apr 12 23:43 ..
-rw-r--r-- 2 nds nds  6268 Apr 12 17:55 icmp.c
-rw-r--r-- 1 nds nds  3252 Apr 12 23:43 icmp.o
<further listing truncated>

./BUILD/LIBLWIP4/NETIF:
total 76
drwxr-xr-x 2 nds nds  4096 Apr 12 23:43 .
drwxr-xr-x 5 nds nds  4096 Apr 12 23:43 ..
-rw-r--r-- 2 nds nds 33201 Apr 12 17:55 etharp.c
-rw-r--r-- 1 nds nds  8252 Apr 12 23:43 etharp.o
<further listing truncated>
```
This time scons pulls the files from "/home/nds/lwip-scons/lwip/src/core/" and deposits them into BUILD/LIBLWIP4/BELCH.  Even though the name of the "build directory" has changed, everything still compiles just fine.  This is the usage that receives the most attention and leads to ... 


## Step 3: ``VariantDir()`` is definitely the droid you're looking for

If your use case is: "I need multiple types of builds and targets built simultaneously."  You almost certainly want ``VariantDir()``.  In that case, I suggest starting with the [UsingVariantDir](UsingVariantDir) entry.  The main developers explain this case far better than I ever could. 

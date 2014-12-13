

## Goal

The goal is to get SCons to track dependencies and the need to build RPMs all in one SConstruct instead of relying on external SConscripts. This is due to the fact that the build of the repository is a simple matter of globbing a set of *.spec files.  The creation process is as follows: 
```txt
    .spec ==> .src.rpm ==> .rpm
```
Since SCons doesn't support this out-of-the-box, we need to create some custom Builders and setup to get this working. 

To see the full unedited source, you can view and comment directly within here: [/FullScript](RpmHoncho/FullScript) 


## .spec ==> .src.rpm

To create a source rpm out of a spec file we need to know a few things: 

   1. The sources that go to create a source rpm. 
   1. The target that is produced. 

### SourceRPM Sources

A source rpm is really just a compressed CPIO package with some extra header.  The sources that comprise of a source RPM include the .spec file, files mentioned in "Source:" tags, and files mentioned in "Patch:" tags.  These tags are found in the specfile, so we build a scanner to get this information.  In my situation, some of the files are tarballs and are not checked into SVN.  Therefore, I use an env.Repository() to point to a cache_dir where I download the appropriate tarballs into. 

_I do this because [BuildDir](BuildDir)() does not really duplicate anything generated from this Scanner. I have no clue why._ 

The code looks like this: 


```python
#!python 
def specfile_scan(node, env, path, *args):
    sources = env.current.sources
    srccache = os.path.join(env.cache_dir, os.path.dirname(str(node)))
    # mkdir -p
    try:
        os.mkdir(srccache)
    except OSError:
        pass
    for k,v in sources.items():
        if v.startswith('http') or v.startswith('ftp'):
            urlgrab(v, os.path.join(srccache, k))
        else:
            shutil.copy(os.path.join(os.path.dirname(str(node)), k),srccache)
    return sources.keys()

specscan = Scanner(function = specfile_scan,
                   skeys = ['.spec'])

...

env.cache_dir = '/data/pyvault-build/sources'
env.Repository(env.cache_dir)
```
env.current is a small Class that contains information parsed out of the specfile by an external utility. This is done outside of any Builder() step. _But this part of my SConstruct is probably messed up._ 


### SourceRPM Target

The target is pretty easy to identify. Building of a source rpm is always of the format: "name-version-release.src.rpm", which is readily available in the env.current Class that was created before the Builder is executed: 

_I had to prepend the build_dir (which I define explicitly) to get things to work. Not sure what's wrong here._ 


```python
#!python 
def srpm_targets(target, source, env):
    targets = env.current.srcrpm
    targets = [os.path.join(env['build_dir'], t) for t in targets]
    return targets, source
```

### SourceRPM Builder

We wrap this all up by creating a custom builder based on the Target. The Scanner part is [AutoMagically](AutoMagically) called when  SCons encounters a .spec file. 


```python
#!python 
macros = """--define='_sourcedir %_topdir/sources/%name' \
            --define='_srcrpmdir %_topdir/srpms' """
srpmbld = Builder(action = "rpmbuild %s --nodeps -bs $SOURCE" % macros,
                  suffix = '.src.rpm',
                  src_suffix = '.spec',
                  emitter = srpm_targets,
                  single_source = True,
          )
```

## .src.rpm ==> .rpm

Setting this up is pretty cake-like since there's only one source. But, there are multiple targets. The difficulty is taken care of prior to invoking the Builder() stuff by using an external utility as discussed above. 


### RPM Source

Always whatever is supplied to the custom builder.  Should end in .src.rpm. 


### RPM Target

Computed by using an external utility, then wrapped: 


```python
#!python 
def rpm_targets(target, source, env):
    targets = [os.path.join(env['build_dir'], t) for t in env.current.packages]
    return env.current.packages, source
```
_Again: needed to prepend build_dir. Dunno why..._ 


### RPM Builder


```python
#!python 
# this could be "rpmbuild --rebuild", or mach. This is what I am working with now.
rpmbld = Builder(action = "mock --no-clean --resultdir=$build_dir -r $chroot $SOURCE",
                 suffix = '.rpm',
                 src_suffix = '.src.rpm',
                 emitter = rpm_targets,
                 single_source = True,
                 src_builder = srpmbld,
```
I put in `src_builder` because I wanted to see if making this a [MultiStageBuilder](MultiStageBuilder) would make any difference. _XXX: So far it has not made a difference._ 


## Failed Experiment

So far, with my script, I've only had SCons exhibit the following behavior, either: 

   1. Always executing the .spec => .src.rpm => .rpm build chain, or 
   1. Never executing it. 
There's one thing I tried to see if it would help. I created a `MakeSpec` builder that bridged the multistage into a .spec ==> .rpm step: 


```python
#!python 

def buildit(target, source, env):
    env.MakeSRPM(source[0])
    env.MakeRPM(os.path.join(env['build_dir'],env.current.srcrpm[0]))

specbld = Builder(action = buildit,
                 suffix = '.rpm',
                 src_suffix = '.spec',
                 emitter = rpm_targets,
                 single_source = True,
                )
```
But, it complained loudly since I just reused the `rpm_targets` found in the `MakeRPM` builder.  So, I need to bail on this and use the original global function called buildit() that wraps multiple builders... 

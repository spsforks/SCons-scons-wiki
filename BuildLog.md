
Sometimes you want to write the SCons output to a file as well as see it on the screen.  The following Bourne shell command will do just that: 

```bash
scons 2>&1 | tee build.log
```
The `2>&1` bit (which sends stderr to the same place as stdout) only works in Bourne shells (sh, bash) and not csh or tcsh. If you are using csh or tcsh, use the following command: 

```csh
scons >&| tee build.log
```
Since the above command is a fair amount of typing, you can set up a function for it: 

```bash
build() {
    scons $* 2>&1 | tee build.log
}
```

When you start using the 'build' command instead of 'scons', it doesn't matter if errors go flying by.  You can just look in the log! 

If you want to set this up in the SConstruct file rather than on the command line: 

```python
import sys
import os
sys.stdout = os.popen("tee build.log", "w")
sys.stderr = sys.stdout
```

---

As an alternative, Timothee Besset posted some code on the scons users mailing list on sept. 30, 2004 to do this within scons: 

Here are some snippets [Note: this was updated to Python 3 syntax]:
```python
# need an Environment and a matching buffered_spawn API .. encapsulate
class idBuffering:
    def buffered_spawn(self, sh, escape, cmd, args, env):
        stderr = StringIO.StringIO()
        stdout = StringIO.StringIO()
        command_string = ""
        for i in args:
            if len(command_string):
                command_string += " "
            command_string += i
        try:
            retval = self.env["PSPAWN"](sh, escape, cmd, args, env, stdout, stderr)
        except OSError as x:
            if x.errno != 10:
                raise x
            print("OSError ignored on command: %s" % command_string)
            retval = 0
        print(command_string)
        sys.stdout.write(stdout.getvalue())
        sys.stderr.write(stderr.getvalue())
        return retval


# get a clean error output when running multiple jobs
def SetupBufferedOutput(env):
    buf = idBuffering()
    buf.env = env
    env["SPAWN"] = buf.buffered_spawn

```
Timothee's original message is at [http://scons.tigris.org/servlets/ReadMsg?list=users&msgNo=1784](http://scons.tigris.org/servlets/ReadMsg?list=users&msgNo=1784) 

Timothee, hope you don't mind my posting this.  -- Gary Oberbrunner 


### Using subprocess

My issue was not writing to a log file and the screen, but not getting output at all under buildbot. If I ran SCons from buildbot it captured no output from tools  which SCons invoked.  I tried idBuffering above but it did not work for me. The implementation of PSPAWN was a little scary.  Since I'm using Python 2.5 I tried subprocess, it worked.  This is on Windows. 

Is there some other way to get around this issue with buildbot?  Seems like everyone would want to see the output of tools launched by SCons in the log file, but I  did not find anything on this problem. 

This routine is surely incomplete but is working for us.  Should it catch OSError like idBuffering does? 


```python
import subprocess


def echospawn(sh, escape, cmd, args, env):
    """Spawn which echos stdout/stderr from the child."""

    # convert env from unicode strings
    asciienv = {}
    for key, value in env.iteritems():
        asciienv[key] = str(value)

    p = subprocess.Popen(
        args,
        env=asciienv,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True,
    )
    (stdout, stderr) = p.communicate()
    
    # Does this screw up the relative order of the two?
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return p.returncode


env["SPAWN"] = echospawn
```
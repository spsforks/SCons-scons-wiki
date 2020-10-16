# ParseDepends
`ParseDepends` allows parsing dependency files, primarily intended for compiler-generated ones, and lets SCons establish the listed dependencies.  

## Why would I do that?
As a rule of thumb, never use it unless you have to. SCons has scanners to extract implicit dependencies, and usually that's all you need. However, sometimes the built-in scanners cannot work out some dependencies - such as when they can't be established until the preprocessor runs. SCons does not run the preprocessor as part of its scanning. Consider the following example: `hello.c`: 

```cpp
#define FOO_HEADER "foo.h"

#include FOO_HEADER

int main() {
        return FOO;
}
```
foo.h:

```cpp
#define FOO 42
```

SConstruct: 

```python
Program('hello.c')
```

```console
$ scons --tree=prune
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gcc -o hello.o -c hello.c
gcc -o hello hello.o
+-.
  +-SConstruct
  +-hello
  | +-hello.o
  | | +-hello.c
  | | +-/bin/gcc
  | +-/bin/gcc
  +-hello.c
  +-[hello.o]
scons: done building targets.
```

As the dependency tree reveals, SCons does not know about `foo.h` and does not rebuild `hello.o` when `foo.h` changes.  If the compiler is able to extract implicit dependencies and output those as Make rules, SCons can parse these files and properly set up the dependencies. 

However, if we had a record of this dependency in a file, we could feed this to SCons:

```python
ParseDepends("hello.d")
Program("hello.c")
```

Where `hello.d` looks like this:
```make
hello: hello.c /usr/include/stdc-predef.h foo.h
```

Then things would look better:

```console
$ scons --tree=prune
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
gcc -o hello hello.o
+-.
  +-SConstruct
  +-foo.h
  +-hello
  | +-hello.o
  | | +-hello.c
  | | +-/bin/gcc
  | +-hello.c
  | +-/usr/include/stdc-predef.h
  | +-foo.h
  | +-/bin/gcc
  +-hello.c
  +-[hello.o]
scons: done building targets.
```

But how do we get these dependencies set up?

## Generate dependency files as a side effect

Here is an example of how to let gcc generate a dependency file while compiling the object file:

```python 
Program("hello.c", CCFLAGS="-MD -MF hello.d")
ParseDepends("hello.d")
SideEffect("hello.d", "hello.o")
```

GCC generates a dependency file that looks like the following:

```console
hello.o: hello.c foo.h
```

There is one problem with this approach: Read the [full story here DEAD LINK](http://scons.tigris.org/servlets/ReadMsg?listName=dev&msgNo=709). TL;DR `ParseDepends` does not read the file in the first pass, leading to unnecessary rebuilds in the second pass. The reason is, that the signature changes as new dependencies are added (`foo.h` in the example above). 

## Generate dependency files in advance
If you want to extract the dependencies (and call `ParseDepends`) before building the object files, the only viable solution is to use a multi-stage builder with a source scanner: 

```python 
def parsedep(node, env, path):
    print "ParseDepends(%s)" % str(node)
    ParseDepends(str(node))
    return []


def parsecheck(node, env):
    return node.exists()


depscan = Scanner(function=parsedep, skeys=[".d"], scan_check=parsecheck)

depbuild = Builder(
    action="$CC -M -MF $TARGET $CCFLAGS -c $SOURCE", suffix=".d", src_suffix=".c"
)

depparse = Builder(
    action=Copy("$TARGET", "$SOURCE"),
    suffix=".dep",
    src_builder=depbuild,
    source_scanner=depscan,
)

env = Environment(BUILDERS={"ExtractDependencies": depparse})

dep = env.ExtractDependencies("hello.c")

obj = env.Object("hello.c")
env.Requires(obj, dep)
env.Program(obj)
```

Some notes:

* The scanner needs to be called when the file exists 
    * **scan_check** ensures the node exists before calling the scanner 
    * A **target_scanner** in depbuild does not work (it's called _before_ the `.d` file exists) 
* The Copy action is useless, the depparse builder exists only to execute a **source_scanner** 
* The dependency file must be generated before the object, therefore the order-only prerequisite 

## Links

* Mailing List: [compiler-generated `.d` files and MD5 signatures](http://scons.tigris.org/servlets/ReadMsg?listName=dev&msgNo=709) 
* Mailing List: [`ParseDepends` questions DEAD LINK](http://scons.tigris.org/servlets/ReadMsg?listName=dev&msgNo=5359)
* Documentation Issue [1984](https://github.com/SCons/scons/issues/1984)

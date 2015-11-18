**How to statically link the c++ runtime libraries (and statically link libgcc) in a sconsy way ?**

As of scons 2.0.1 adding LINKFLAGS="--static" to Program() seems to work.

Example:

```txt
Program("test.cxx",
        LIBS = ["boost_unit_test_framework"],
        LIBPATH = ["/usr/lib", "/usr/local/lib"],
        LINKFLAGS="--static")
```

---


```python
#!python

env = Environment();

static = env.Command('libstdc++.a', None, Action('ln -s `g++ -print-file-name=libstdc++.a` $TARGET'));
lib = env.StaticLibrary(target='mylib', source='mylib.cpp', LIBPATH='.', LINKFLAGS='-static-libgcc', LIBS=[static]);

env.Program(target='myprog', source='main.cpp', LIBS=[static,lib], LINKFLAGS='-static-libgcc', LIBPATH='.');
```

Warning: this first recipe wont work with scons 0.96.1 or lower.


---

```python
#!python

env = Environment(
    # LINKCOM needs to be specifed here because of the special handling when
    # linking against the static libgcc and stdc++
    LINKCOM = "$LINK -o $TARGET $SOURCES $_LIBDIRFLAGS $_LIBFLAGS $LINKFLAGS",

    LINKFLAGS = "-static-libgcc -ldl -Xlinker -B -Xlinker static -lstdc++")

prog = env.Program(target='myprog',source='main.cpp');
```


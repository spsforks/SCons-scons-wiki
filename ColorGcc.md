**How to use the colorgcc wrapper to colorize the output of compilers ?**

To be able to use [colorgcc](https://schlueters.de/colorgcc.html) with SCons you need an environment that includes $PATH, $TERM, and $HOME.


```txt
env = Environment(ENV = {'PATH' : os.environ['PATH'],
                         'TERM' : os.environ['TERM'],
                         'HOME' : os.environ['HOME']})
```

* $PATH needs to include the path to where your symbolic links named gcc, g++, cxx, cc, all pointing to the colorgcc wrapper, are located.
* $TERM is used by colorgcc to check if the terminal is smart enough to handle colors.
* $HOME is used by colorgcc to find your .colorgccrc file including customizations.


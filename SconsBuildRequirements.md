

# Build requirements for packaging SCons


## Python

To build SCons you need to have Python version 2.7 or later installed, as well as its developer package named `python-dev` under Debian. You'll also need the setuptools, named `python-setuptools`. 


## Full builds, including all docs

However, if you want to build the docs as well, it will be more complicated. You'll need some extra packages: 

You need to have the Python binding for either `libxml2` or `lxml` installed. For rendering PDF documents, you'll need a program like `fop`, `xep` or `jw` available in your system-wide `$PATH`. Creating the EPUB output files of the [UserGuide](UserGuide) and the MAN page, both depend on the Ghostscript executable `gs` for creating the front cover image.  `fop` requires Java but is easily installed via `apt-get` on Debian/Ubuntu.  `jw` is available for Debian/Ubuntu as part of the `docbook-utils` package.  You'll also need `epydoc` in the `python-epydoc` package. 

See also [DeveloperGuide/Documentation](DeveloperGuide/Documentation) for further details. 


## Master script

In the SCons source tree you can also find the script `bin/scons_dev_master.py`, which can be used to setup your current environment for special development tasks. Calling it with: 


```txt
python bin/scons_dev_master.py build
```
should automatically install the required packages, as mentioned above. 


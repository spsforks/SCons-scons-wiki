# Build Requirements for running SCons

There is no building required to run scons: you can just run directly from the source tree, and scons intentionally does not depend on anything that isn't in the Python Standard Library.

# Build Requirements for packaging SCons

## Python

To build SCons for packaging you need to have Python version 2.7.* or version 3.5.0 or later installed, as well as its developer package named `python-dev` under Debian. You'll also need the setuptools, named `python-setuptools`. 


## Full builds, including all docs

If you want to build the docs as well, it will be more complicated. You'll need some extra packages: 

You need to have the Python binding for either `libxml2` and `libxslt` or for `lxml` installed. For rendering PDF documents, you'll need a program like `fop`, `xep` or `jw` available in your system-wide `$PATH`. Creating the EPUB output files of the [UserGuide](UserGuide) and the MAN page, both depend on the Ghostscript executable `gs` for creating the front cover image.  `fop` requires Java but is easily installed via `apt-get` on Debian/Ubuntu.  `jw` is available for Debian/Ubuntu as part of the `docbook-utils` package.  You'll also need `epydoc` in the `python-epydoc` package. 

See also [DeveloperGuide/Documentation](DeveloperGuide/Documentation) for further details. 

Note: the docs do not currently build under Python 3. Check the progress of [Issue 3300](https://github.com/SCons/scons/issues/3300) for progress.  Also note there is no supported Python 3.x binding for `libxslt`.


## Master script

In the SCons source tree you can also find the script `bin/scons_dev_master.py`, which can be used to setup your current environment for special development tasks. Calling it with: 


```txt
python bin/scons_dev_master.py build
```
should automatically install the required packages, as mentioned above. The script is kept up to date on a best-effort basis, but might be a bit out of date on a recent version of Ubuntu.


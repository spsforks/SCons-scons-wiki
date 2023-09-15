# Build Requirements for running SCons

You don't need to build or package SCons to run it. You can just run directly from the source tree, and scons intentionally does not depend on anything that isn't in the Python Standard Library.

# Build Requirements for packaging SCons

## Python

To build SCons for packaging you need to have Python version 3.6.0 or later installed


## Full builds, including all docs

If you want to build the docs as well, it will be more complicated. You'll need some extra packages: 

Use the script `bin/scons_dev_master.py docs building testing` to install the required system packages.
The script is kept up to date on a best-effort basis, but might be a bit out of date on a recent version of Ubuntu.

Then we advise you create a python virtualenv and install the python packages via pip

`pip install -U -r requirements-dev.txt`

`pip install -U -r requirements-pkg.txt`

See also [DeveloperGuide/Documentation](DeveloperGuide/Documentation) for further details. 


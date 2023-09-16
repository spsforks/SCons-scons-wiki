# Requirements for running SCons

You don't need to build or package SCons to run it. You can just run directly from the source tree, and scons intentionally does not depend on anything that isn't in the Python Standard Library.
```console
python somepath/scons/scripts/scons.py
```

# Requirements for Working on SCons

If you are intending to work on changes to SCons code, you'll want to run the tests (including any new ones you may be developing). For that, 
a few packages are useful: `psutil`, `ninja` and `lxml`.  These are captured in `requirements-dev.txt`.

The tests are set up to run through a lot of features, but they skip tests which require external programs to operate, if those are not found on the system. It usually isn't necessary to worry about these unless they're actually in the area you are working on, then you'll need to find how to install those for your development system.

# Requirements for Packaging SCons

Packaging additionally requires the Python package `build`.

> **Note**: for the current setup (last updated in 2023), the documentation build is required to complete the wheel package, because the generated manpages (`scons.1`, `sconsign.1`, `scons-time.1`) are added to the package. This *may* be a temporary situation, but for now, please assume the following section always applies.

## Full builds, including all docs

If you want to build the docs as well, it will be more complicated. You'll need some extra Python packages, which are captured in `requirements-pkg.txt`, and some system packages.

We advise creating a Python virtualenv and using that to create your work environment.  If not familiar with this, there is a simple walkthrough available for three different system types in [the Cookbook](https://scons-cookbook.readthedocs.io/en/latest/#setting-up-a-python-virtualenv-for-scons). You don't need to install the `scons` package in this instance, since you'll be working directly with the code in your working tree. With this virtualenv activated:

```console
pip install -r requirements-pkg.txt
```

It may be convenient to have the `scons` command available, referring to the working source tree, to reduce typing the path to the `scons.py` driver program. To accomplish that, while in the top of that tree:

```console
pip install --editable .
```

Building the documentation makes use of a lot of additional software that may not by default be installed on your system. 
For Ubunto/Debian systems, use the script `bin/scons_dev_master.py docs building testing` to install the required system packages.
This script is kept up to date on a best-effort basis, but might be a bit out of date on the most recent systems.
For other systems, examine that script, and use the native packaging tools - package names should have some relationship,
but will likely differ a bit.  The doc build is not currently supported on Windows.

See also [DeveloperGuide/Documentation](DeveloperGuide/Documentation) for further details. 


# SCons Source Tree Walkthrough
Here's a quick introduction to the structure of the SCons repository.

When you first check out SCons, the main directories you will see are:

|           |                                            |
|-----------|--------------------------------------------|
| SCons     | the sources                                |
| doc       | the documentation (man pages, guides, etc) |
| scripts   |the things your would run from a cmdline    |
| test      | the test suite (end to end tests)          |
| testing   | the testing framework                      |

The `SCons` directory is the one you probably care about. It is organized like this:

* `SCons`: the root of the SCons python module hierarchy
  * `*.py`: the python modules
  * `*Tests.py`: unit tests, discovered automatically; see [TestingMethodology](TestingMethodology)
  * `*.xml`: documentation files that are kept close to the implementation (these are folded in to the contents of `doc` when documentation is built)
  * `Tool`: Tool modules, e.g. cc.py, msvc.py, latex.py...
  * `Scanner`: Scanner modules for dependency scanning
  * `Node`: the Node object, the central filesystem abstraction for building the dependency graph
  * `Script`: `Main.py` in here has the main loop that parses SCons options and reads the `SConstruct`; it's what's called from the "scons" script

Some key files in `SCons`:

* ```Environment.py```: SCons Environment class: the user way to communicate dependencies and construction information to the SCons engine
* ```Node/FS.py```: File() and Dir() nodes are defined here

After working with the source tree for a while, there may be two additional directories of interest:

|           |                                                 |
|-----------|-------------------------------------------------|
| build     | where the documentation build goes              |
| bootstrap | localized scons distribution used for packaging |

This page is intended to track the various features that are, or will be, deprecated, and their progress through our [DeprecationCycle](DeprecationCycle).  The idea is to have a place to track movement of these through the cycle so that, within the guidelines of the Cycle, we can be reasonably timely about shedding older features that may be slowing down or complicating the code base. 

In the table below, a '?' indicates an estimated or unknown value and a '??' indicates a projected future time.  The most recently announced are at the top. 

Note that Python version support is handled a bit differently.  While there is a small component that is an "active" SCons feature - bytecode strings for certain scenarios - mostly the Python version isn't really part of SCons.  Since old versions restrict the syntax that can be used, SCons is now tracking more closely to the versions of cPython supported by upstream and is not using the long deprecation sequence for this.

TODO:  Go through old release notes and/or mailing list archives to nail down "Announced." 

Stage       | Description
:-----------|:-----------
Repl    |  Replacement released
Annuc   |  Announcement
Hidden  |  Hidden Warning, off by default, can be turned on
Suppr   |  Suppressible Warning, on by default, can be turned off
Mand    |  Mandatory Warning, always on
Fatal   |  Fatal Error, feature no longer available
Removed |  Check removed, may cause Python error


 **Feature**  |  **Description / Notes**  |  **Repl**  |  **Annuc**  |  **Hidden**  |  **Suppr**  |  **Mand**  |  **Fatal**  |  **Removed**
:-----|:------|:---|:---|:----|:----|:----|:----|:----|
 Python 3.5  |  Drop support for Python 3.5  |  N/A  |  4.2  |  N/A  |  N/A  |  N/A  |  N/A  |  never 
 `--cache-<option>`  |  Convert to `--cache=<option>`  |  2.1??  |  2.1??  |  2.1??  |  ??  |  ??  |  3.0??  |  3.2?? 
 `${,UN}CHANGED_SOURCES` `${,UN}CHANGED_TARGETS` reserved variables  |  Deprecate the user's ability to set them  |  N/A  |  1.2  |  Warning message (and assignment suppressed) as one of the reserved construction variable names |||||
 `Options/*.py` modules  |  Stub modules, restored when 0.98.1 removed them and broke released configurations  |  0.98.3  |  TODO  |   |  1.2  |  2.0  |  2.1??  |  3.0?? 
 `*Option` names  |  Replaced by `*Variable` names  |  0.98.1  |  TODO  |   |  1.2  |  2.0  |  2.1??  |  3.0?? 
 `env.BuildDir()`  |  Replaced by `env.VariantDir()`  |  0.98.0  |  TODO  |   |  2.0  |  2.1??  |  3.0??  |  3.1.2
 `build_dir` option  |  Replaced by `variant_dir`  |  0.98.0  |  TODO  |   |  2.0  |  2.1??  |  3.0??  |  3.1.2
 `env.Copy()`  |  Replaced by `env.Clone()`  |  0.98.0  |  TODO  |   |  0.98.0  |  2.0  |  2.1??  |  3.1.2
 `env.SourceSignatures()` and `env.TargetSignature()`  |  Replaced by `env.Decider()`; eliminating these would speed up a critical code path!  |  0.98.0  |  TODO  |   |  0.98.0  |  2.0  |  2.1??  |  3.1.2
 `--debug=dtree` option  |  Replaced by `--tree=derived`  |  0.98.0  |  TODO  |   |  0.98.0  |  2.0  |  2.1??  |  3.1.2
 `--debug=stree` option  |  Replaced by `--tree=all,status`  |  0.98.0  |  TODO  |   |  0.98.0  |  2.0  |  2.1??  |  3.1.2
 `--debug=tree` option  |  Replaced by `--tree=all`  |  0.98.0  |  TODO  |   |  0.98.0  |  2.0  |  2.1??  |  3.1.2
 `Sig` module  |  Stub module to maintain backwards compatibility from before the Signature Refactoring  |  0.97.x  |  TODO  |   |  0.98.0  |  2.0  |  2.1??  |  ?? 
 `scanner` Builder keyword  |  Replaced by separate `target_scanner` and `source_scanner` keywords  |  0.96.90  |  TODO  |   |  0.96.90  |  2.0  |  2.1??  |  3.1.2
 `overrides` Builder keyword  |  Replaced by use of keyword arguments in Builder creation  |  0.95  |  TODO  |   |  0.95  |  2.0  |  2.1??  |  3.1.2
 `--debug=nomemoizer` option  |  No longer has any effect  |  0.96.94  |  TODO  |   |  0.96.94  |  2.0  |  2.1??  | 3.1.2
 `File.win32` attribute  |  Replaced by `.windows`  |  0.96.92  |  TODO  |  none  |  2.1??  |  ??  |  ??  |  ?? 
 `$WIN32*` construction variables  |  Replaced by `$WINDOWS*` construction variables  |  0.96.92  |  TODO  |  none  |  2.1??  |  ??  |  ??  |  4.2
 `$PDFCOM` construction variable  |  Replaced by `$DVIPDFCOM`  |  0.14  |  TODO  |  none  |  2.1??  |  ??  |  ??  |  4.2
 `Taskmaster.Task.` `needs_execute()`  |  internal method; may be used by user-defined subclasses |  should always be overridden - now an abstract method || |  ?  |  2.0  |  2.1??  |  ??  |  4.0
 `Scanner.Scanner` class  |  TBD:  unused internal class; may be used by user code  |  ?  |  ?  |  ?  |  ?  |  ?  |  ?  |  ?
 `Scanner.Selector` class  |  TBD:  unused internal class; may be used by user code  |  ?  |  ?  |  ?  |  ?  |  ?  |  ?  |  ?
 `qt` tool | Drop old qt3-only tool | qt4/qt4 contrib | 4.3 | 4.3  |  ?  |  ?  |  ?  |  ?  |  ?


CAUTION: Only try this step if you have the toolchain for building the documentation.  The packages needed are discussed [here](DevGuide-Documentation).  It's quite a list. 

The following steps verify that the user guide sources (some of which are generated from other files) are up to date. 

[FIXME](ReleaseHOWTO/UpdateGuide) _(This will probably be reworked to be part of the build step.)_ 


```txt
  $ python bin/scons-doc.py --diff
  $ python bin/scons-doc.py --update
```
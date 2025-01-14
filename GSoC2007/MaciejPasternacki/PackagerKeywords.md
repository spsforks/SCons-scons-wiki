

# Packaging software supported keywords

This page describes which general keywords are recognized by various flavours pf software packaging software.  These are fields that are of general use; idiosyncratic fields (like dependency information in system packagers) are left out. 


## SCons packaging extension

Philipp Scholl's Google Summer of Code 2006 project (see [PhilippSchollProposal](PhilippSchollProposal)) 

Source: [https://teco62pc.teco.edu/projects/Scholl_SummerOfCode/wiki/PackageMetaData](https://teco62pc.teco.edu/projects/Scholl_SummerOfCode/wiki/PackageMetaData) 

* Project name 
* Version 
* Package version (RPM release, .deb revision) 
* Summary (possibly in different languages) 
* Description (possibly in different languages) 
* License 
* License text 
* Source URL 
* Architecture 
* URL 
* Vendor 
* Changelog 

## RPM

RPM package manager for managing binary software packages in Linux distribution, originally designed for Red Had Linux. 

Source: [http://www.rpm.org/max-rpm/s1-rpm-inside-tags.html](http://www.rpm.org/max-rpm/s1-rpm-inside-tags.html) 

* Name 
* Summary 
* Epoch (number that's more important than version when calculating 
which package is newer) 

* Version 
* Release (version of package) 
* Copyright/License (synonyms) 
* Group (for organizing software within distribution) 
* Icon 
* Vendor 
* URL 
* Packager (person that packaged software) 
* Description 

## Dpkg

Debian's package manager for `.deb` files. 

Source: [http://www.debian.org/doc/debian-policy/ch-controlfields.html#s-controlfieldslist](http://www.debian.org/doc/debian-policy/ch-controlfields.html#s-controlfieldslist) 

* Source (source package's name) 
* Package (binary package's name) 
* Maintainer 
* Uploaders (co-maintainers) 
* Changed-By (usually same as Maintainer) 
* Section (like RPM's Group) 
* Priority (how important the package is for system) 
* Architecture 
* Essential 
* Version (epoch:upstream_version-debian_revision) 
* Description 
* Distribution (which Debian lines package supports) 
* Date (of last change) 
* Urgency 
* Changes (changelog) 

## ASDF

Common Lisp's Another System Definition Facility. 

Source: [http://constantly.at/lisp/asdf/](http://constantly.at/lisp/asdf/) 

* Name 
* Description 
* Version 
* Author 
* Licence 

## Distutils

Python's standard packaging extension. 

Source: [http://docs.python.org/dist/module-distutils.core.html](http://docs.python.org/dist/module-distutils.core.html), PEP-314 at [http://www.python.org/dev/peps/pep-0314/](http://www.python.org/dev/peps/pep-0314/) 

* Name 
* Version 
* Description 
* Long description 
* Author 
* Author email (separate from author) 
* Maintainer (if left out, same as author) 
* Maintainer email 
* URL 
* Download URL 
* Classifiers (categories to which package belongs) 
* License 
* Keywords 
* Platforms 
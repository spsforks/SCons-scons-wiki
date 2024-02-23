The following env variables can affect the command line and created files for these

* `SHLIBVERSION`
* `SONAME`
* `SOVERSION`
* `APPLELINK_NO_CURRENT_VERSION`    (applelink only)
* `APPLELINK_CURRENT_VERSION`       (applelink only)
* `APPLELINK_COMPATIBILITY_VERSION` (applelink only)

In most cases the linker will create a file named as

`${SHLIBPREFIX}lib_name${SHLIBSUFFIX}.${SHLIBVERSION}`

Which will have a soname baked into it as one of the

* `${SONAME}`
* `${SHLIBPREFIX}lib_name${SHLIBSUFFIX}.${SOVERSION}`
* (for applelink only)
   * `${SHLIBPREFIX}lib_name${major version only from SHLIBVERSION}${SHLIBSUFFIX}`
   * `-Wl,-compatibility_version,%s`
   * `-Wl,-current_version,%s`
   
For **applelink** the version has to follow these rules to verify that the version # is valid.

* For version # = X[.Y[.Z]]
* where X 0-65535
* where Y either not specified or 0-255
* where Z either not specified or 0-255


   
For most platforms this will lead to a series of symlinks eventually pointing to the actual shared library (or loadable module file).

(This info it stored in a list of tuples stored in `target[0].attributes.shliblinks` this is currently done in the emitter)
1. `${SHLIBPREFIX}lib_name${SHLIBSUFFIX} -> ${SHLIBPREFIX}lib_name${SHLIBSUFFIX}.${SHLIBVERSION}`
1. `${SHLIBPREFIX}lib_name${SHLIBSUFFIX}.${SOVERSION} -> ${SHLIBPREFIX}lib_name${SHLIBSUFFIX}.${SHLIBVERSION}`

For **openbsd** the following rules for symlinks apply

   * OpenBSD uses x.y shared library versioning numbering convention and doesn't use symlinks to backwards-compatible libraries


The current code provides the following hooks a compiler can use to customize:

```        
        'VersionedShLibSuffix': _versioned_lib_suffix,
        'VersionedLdModSuffix': _versioned_lib_suffix,
        'VersionedShLibSymlinks': _versioned_shlib_symlinks,
        'VersionedLdModSymlinks': _versioned_ldmod_symlinks,
        'VersionedShLibName': _versioned_shlib_name,
        'VersionedLdModName': _versioned_ldmod_name,
        'VersionedShLibSoname': _versioned_shlib_soname,
        'VersionedLdModSoname': _versioned_ldmod_soname,
```


# Thoughts on new implementation

so if I define 
```py
env['SONAME']='$GenSONAME'
```
And then if the user sets `SONAME` directly that works. `GenSONAME` is a function which uses any values of  `SHLIBVERSION`, `SOVERSION`, (or if user implemented any values it wants) fairly straightforward t generated shared library name from variables as well. and get rid of all the levels of indirection.

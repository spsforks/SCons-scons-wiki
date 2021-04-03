Sometimes targets are made by a sequence of builders, some of which may be implicit. For example:

```python
Program(target="foo", source="foo.c")
```

tells SCons that you want to make `foo` (or `foo.exe`) from the source file `foo.c`. But to get there, the object file `foo.o` (or `foo.obj`) needs to be built first, and SCons chains builders to get there. The object file in this instance is an intermediate target. You have the choice to mention this target youself or not, for example you can do:

```python
fooobj = Object(target="foo", source="foo.c")
Program(target="foo", source=fooobj)
```

but if SCons can infer that relationship, there is no need to be so explicit, and trying to be can often lead to less portable builds (for example, mentioning the intermediate file as `foo.o` means it only works on systems where the object-file suffix is `.o`). So it is actually usually preferred to let SCons figure it out.

SCons treats implicit intermediate targets very similarly to explicitly mentioned targets - they are built if needed or fetched from a repository if an up to date copy is found there, are reported on when built (or fetched) if settings don't disable printing, are stored in or fetched from a CacheDir if one is enabled, are recorded in the dependency information in the sconsign database, and are cleaned by the SCons clean mode (-c).  For those familiar with the "make" tool this is different behavior: in "make", if an intermediate target file is created in order to update a different target file, the intermediate target is deleted after it is no longer needed. SCons leaves the file around, as it might be useful later: there might not be any need to rebuild a given intermediate target on a later build if it exists and is up to date.

Unlike SCons, make provides a way to fine-tune this behavior, through the `.INTERMEDIATE` and `.SECONDARY` special targets. SCons issue [#583](/SCons/scons/issues/583) asks for this kind of control to be provided in SCons as well. It turns out this is not easy to implement, requiring at least these four things to happen:

* New functions (perhaps `Intermediate` and `Secondary`) to mark Nodes appropriately.
* The logic to delete an intermediate target when the need for it is done.
* The logic to figure out if a target is up-to-date even if intermediate or secondary targets are missing.
* The logic to rebuild missing intermediate targets if a downstream target needs them.

An additional issue is that the handling of implicit intermediate targets can easily violate the least-surprise principle.  Consider a case where two different targets are built which have a source file in common, but the two builds use different sets of build options, each in their own environment. The SConscripts never mention the intermediate object file, but SCons will still try to put them into the dependency tree, and then fail with the infamous error:
```
scons: *** Two environments with different actions were specified for the same target: foo.o
```
Because of the above-mentioned characteristics - basically that implied intermediate targets are still first-class targets - SCons cannot disambiguate `foo.o` of env1 from `foo.o` of env2, and it just gives up with a fatal error.  Using variant directories can be a solution to this, as they provides a form of namespace isolation, but it's still surprising to users when they run into a conflict on a target they never even listed (and without a particularly useful error message to show where the problem occurred), and arguably forces more complexity where it might not be necessary.

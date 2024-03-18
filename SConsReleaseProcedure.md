# Current SCons Release Procedure

The procedure has been used for all releases since 4.3.0. 

## Tag Release in Git

* Move work to a release branch. It's currently necessary to do this first as the build will use the branch name when building the REVISION string it substitutes into many of the files.


```bash
git fetch 
git checkout -b rel_<NAME> master
git clean -xfd
```


## Prepare Binaries and Doc

- [ ] Validate and update all documentation files by calling: 

```bash
python bin/docs-update-generated.py
python bin/docs-validate.py
python bin/docs-create-example-outputs.py
```

- [ ] Check if there's anything specific to this version in `doc/man/scons.xml` that should be updated.. For example, support for a particular Python version may be deprecated or dropped in this SCons release. In particular, look for the sequence **`requires Python`**. It's worth rerunning the `docs-validate.py` script if a change was made here.
- [ ] Commit the auto-generated doc changes to current branch ("Regenerated docs for X.Y.Z release.") 
- [ ] Update CHANGES.txt (should already be up to date) 
- [ ] Update RELEASE.txt (should already be up to date) 
- [ ] Update ReleaseConfig
- [ ] Commit 
- [ ] Update `default_version` in SConstruct
- [ ] Build packages and doc: `python scripts/scons.py >& build-XYZ.log` (good idea to save build logfile somewhere) 

```txt
You should now have the following in build/dist: 

SCons-$VERSION-py3-none-any.whl
SCons-$VERSION.tar.gz
SCons-$VERSION.zip
scons-doc-$VERSION.tar.gz
scons-local-$VERSION.tar.gz
scons-local-$VERSION.zip

```
- [ ] Commit the above changes to git and push. 
- [ ] Tag and push tag

## Upload Software and Doc
- [ ] Run `bin/upload-release-files.sh X.Y.Z mysfusername`

* There is now a shell script to do this: `bin/upload-release-files.sh X.Y.Z mysfusername` as long as [SourceForge](SourceForge) and scons.org have your ssh pub key and you're using SSH Agent Forwarding. 
* It uploads all the packages to SF, uploads the doc to scons.org, unpacks it, and updates the doc symlinks.
  * You will be prompted for your password numerous times. 
* You may still have to tell SF that the new release dirs exist in its File Manager (it's a bit buggy). 

## Prepare Announcement and announce to all

* Use RELEASE.txt as blurb 



## Update website

| File   | Changes  |
|---|---|
| versions.py  | update SCONS_PRODUCTION_VERSION, SCONS_PRIOR_VERSION, SCONS_API_VERSIONS  |
| content/documentation/documentation.md | Update the version for each type of documentation |
| content/releases/release-###.rst | add an announcement |


- [ ] Commit the above changes to git and push. 
- [ ] Tag and push tag

```
git tag #.#.#
git push --tags
```

- [ ] Update Sourceforge: 
- [ ] set default downloads for each win/linux/mac etc. appropriately, using the "info" link on the right of each download. 
  - NOTE: it will take a minute or two for these changes to affect the README and default downloads you've just set.
- [ ] Announce to scons-users and scons-dev python list


- [ ] Upload to testpypi #

```bash
python setup.py bdist_wheel
python setup.py sdist --format=gztar
# If you have a ~/.pypirc
twine upload -r pypitest build/dist/SCons-*.{tar.gz,whl}
# else this will prompt you for your pypi or test pypi username/password
twine upload --repository-url https://test.pypi.org/legacy/ build/dist/SCons-*.{tar.gz,whl}
```

- [ ] Test package:

```bash
# Be sure to do this on both windows and non-windows systems
virtualenv venv
. venv/bin/activate
pip install --index-url https://test.pypi.org/simple/ scons==3.0.0.alpha.20170821
scons --version
```

- [ ] Upload to Pypi #

```bash
twine upload  build/dist/SCons-*.tar.gz build/dist/SCons*.whl
```

## After Release

- [ ] On GitHub create a pull request from the branch. GitHub will give you a URL when you push and create the branch which will take you to a page to do just this.
- [ ] On Github create a release with RELEASE.txt using [Github New Release Page](https://github.com/SCons/scons/releases/new)
- [ ] On master branch, run `python bin/update-release-info.py post` to go back to develop mode. 
- [ ] Commit those changes after review 

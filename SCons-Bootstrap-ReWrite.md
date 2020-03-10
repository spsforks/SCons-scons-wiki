# Here's what SCons' internal build should do:
1. build docs (if enabled)
2. build API docs (if docs enabled and api docs enabled)
3. build wheel and sdist_gztar
4. build scons-local zip and tgz package
5. expand packages so runtest.py can run against them? (is this still needed)


# Files to be generated
* scons-$VERSION.tar.gz 
* scons-$VERSION.zip 
* scons-local-$VERSION.tar.gz
* scons-local-$VERSION.zip
* scons-src-$VERSION.tar.gz
* scons-src-$VERSION.zip
* scons-doc-$VERSION.tar.gz
* Announce.txt 
* CHANGES.txt 
* RELEASE.txt
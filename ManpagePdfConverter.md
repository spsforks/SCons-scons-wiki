Using [OpenJade](http://openjade.sourceforge.net/), [doclifter](http://catb.org/~esr/doclifter/) and Jade Wrapper you can export the SCons manpage as a handy, indexed PDF file.

```bash
# This script was written for Ubuntu 6.10 and assumes the following packages:
# docbook-utils
# doclifter
# sudo apt-get install docbook-utils doclifter 

gunzip -c /usr/share/man/man1/scons.1.gz | doclifter > scons.sgml 

# Uncomment this line if you want to check the sgml before processing it #gedit scons.sgml 

docbook2pdf scons.sgml 

# You could use this if you don't have the docbook2pdf script #jw -f docbook -b pdf scons.sgml 

rm scons.sgml
```

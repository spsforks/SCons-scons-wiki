

# Model programs and their Automake files

In order to concentrate on actually used features and on practical usage of Automake compatibility layer, I chose a few programs that currently use Automake, in order to make it possible to build them using SCons. 

Since SCons lacks any Gettext support and adding it is non-trivial and not in scope of this project, as far as my project is concerned, if any of referenced programs uses Gettext, support for it will not be included in SConsified version. 

Additional suggestions for model programs, both simple and (more important) complex, are welcome. 


## Simple projects


### AMHello

Canonical 'Hello, World' example included with Automake as an example.  Minimal project, a must-have. 

No own home or project page. 
Browse sources
: 
[http://cvs.savannah.gnu.org/viewvc/automake/doc/amhello/?root=automake](http://cvs.savannah.gnu.org/viewvc/automake/doc/amhello/?root=automake) 


`configure.ac` file
: 
[configure.ac](http://cvs.savannah.gnu.org/viewvc/automake/doc/amhello/configure.ac?root=automake&view=markup) 


`Makefile.am` files
: 
      * [Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/doc/amhello/Makefile.am?root=automake&view=markup) 
      * [src/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/doc/amhello/src/Makefile.am?root=automake&view=markup) 



#### SConstruct

Low-level API: 
```python
#!python 
proj = Project('amhello', '1.0', header='config.h')
proj.Distribute('configure.ac', 'Makefile.am', 'src/Makefile.am')
proj.AutoInstall(Program('src/hello', 'src/main.c'))
```

### GNU cpio

Simple C program, referenced as an example throughout Automake manual, multiple directories, Texinfo documentation, library, header files. 
Home page
: 
[http://www.gnu.org/software/cpio/](http://www.gnu.org/software/cpio/) 


Project page
: 
[http://savannah.nongnu.org/projects/cpio](http://savannah.nongnu.org/projects/cpio) 


Browse sources
: 
[http://cvs.savannah.gnu.org/viewvc/cpio/?root=cpio](http://cvs.savannah.gnu.org/viewvc/cpio/?root=cpio) 


`configure.ac` file
: 
[configure.ac](http://cvs.savannah.gnu.org/viewvc/cpio/configure.ac?root=cpio&view=markup) 


`Makefile.am` files
: 
      * [Makefile.am](http://cvs.savannah.gnu.org/viewvc/cpio/Makefile.am?root=cpio&view=markup) 
      * [doc/Makefile.am](http://cvs.savannah.gnu.org/viewvc/cpio/doc/Makefile.am?root=cpio&view=markup) 
      * [headers/Makefile.am](http://cvs.savannah.gnu.org/viewvc/cpio/headers/Makefile.am?root=cpio&view=markup) 
      * [lib/Makefile.am](http://cvs.savannah.gnu.org/viewvc/cpio/lib/Makefile.am?root=cpio&view=markup) 
      * [src/Makefile.am](http://cvs.savannah.gnu.org/viewvc/cpio/src/Makefile.am?root=cpio&view=markup) 
      * [tests/Makefile.am](http://cvs.savannah.gnu.org/viewvc/cpio/tests/Makefile.am?root=cpio&view=markup) 



### Automake

Not a very complicated program, written in Perl (project not based on C language), non-trivial installation. 
Home page
: 
[http://www.gnu.org/software/automake/](http://www.gnu.org/software/automake/) 


Project page
: 
[http://savannah.nongnu.org/projects/automake](http://savannah.nongnu.org/projects/automake) 


Browse sources
: 
[http://cvs.savannah.gnu.org/viewvc/automake/?root=automake](http://cvs.savannah.gnu.org/viewvc/automake/?root=automake) 


`configure.ac` file
: 
[configure.ac](http://cvs.savannah.gnu.org/viewvc/automake/configure.ac?root=automake&view=markup) 


`Makefile.am` files
: 
   * [Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/Makefile.am?root=automake&view=markup) 
   * [doc/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/doc/Makefile.am?root=automake&view=markup) 
   * [lib/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/lib/Makefile.am?root=automake&view=markup) 
   * [lib/Automake/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/lib/Automake/Makefile.am?root=automake&view=markup) 
   * [lib/Automake/tests/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/lib/Automake/tests/Makefile.am?root=automake&view=markup) 
   * [lib/am/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/lib/am/Makefile.am?root=automake&view=markup) 
   * [m4/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/m4/Makefile.am?root=automake&view=markup) 
   * [tests/Makefile.am](http://cvs.savannah.gnu.org/viewvc/automake/tests/Makefile.am?root=automake&view=markup) 



### Fetchmail

Simple, C-based program.  Unique feature to test is Lex and Yacc usage. 
Home page
: 
[http://fetchmail.berlios.de/](http://fetchmail.berlios.de/) 


Project page
: 
[http://developer.berlios.de/projects/fetchmail/](http://developer.berlios.de/projects/fetchmail/) 


Browse sources
: 
[http://mknod.org/svn/fetchmail/trunk/](http://mknod.org/svn/fetchmail/trunk/) 


`configure.ac` file
: 
[configure.ac](http://mknod.org/svn/fetchmail/trunk/configure.ac) 


`Makefile.am` files
: 
   * [Makefile.am](http://mknod.org/svn/fetchmail/trunk/Makefile.am) 
   * [m4/Makefile.am](http://mknod.org/svn/fetchmail/trunk/m4/Makefile.am) 


SConstruct file: [GSoC2007/MaciejPasternacki/ModelPrograms/FetchmailSConstruct](GSoC2007/MaciejPasternacki/ModelPrograms/FetchmailSConstruct) 


## Complex projects


### Nix

Complex, C++-based programs.  Lots of subdirectories.  Non-trivial installation. 
Home page
: 
[http://nix.cs.uu.nl/](http://nix.cs.uu.nl/) 


Browse sources
: 
[https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/) 


`configure.ac` file
: 
[configure.ac](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/configure.ac) 


`Makefile.am` files
: 
   * [Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/Makefile.am) 
   * [corepkgs/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/corepkgs/Makefile.am) 
   * [corepkgs/buildenv/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/corepkgs/buildenv/Makefile.am) 
   * [corepkgs/channels/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/corepkgs/channels/Makefile.am) 
   * [corepkgs/nar/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/corepkgs/nar/Makefile.am) 
   * [doc/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/doc/Makefile.am) 
   * [doc/manual/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/doc/manual/Makefile.am) 
   * [externals/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/externals/Makefile.am) 
   * [misc/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/misc/Makefile.am) 
   * [misc/emacs/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/misc/emacs/Makefile.am) 
   * [scripts/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/scripts/Makefile.am) 
   * [src/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/Makefile.am) 
   * [src/bin2c/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/bin2c/Makefile.am) 
   * [src/boost/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/boost/Makefile.am) 
   * [src/boost/format/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/boost/format/Makefile.am) 
   * [src/bsdiff-4.3/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/bsdiff-4.3/Makefile.am) 
   * [src/libexpr/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/libexpr/Makefile.am) 
   * [src/libmain/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/libmain/Makefile.am) 
   * [src/libstore/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/libstore/Makefile.am) 
   * [src/libutil/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/libutil/Makefile.am) 
   * [src/nix-env/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/nix-env/Makefile.am) 
   * [src/nix-hash/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/nix-hash/Makefile.am) 
   * [src/nix-instantiate/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/nix-instantiate/Makefile.am) 
   * [src/nix-log2xml/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/nix-log2xml/Makefile.am) 
   * [src/nix-setuid-helper/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/nix-setuid-helper/Makefile.am) 
   * [src/nix-store/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/nix-store/Makefile.am) 
   * [src/nix-worker/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/src/nix-worker/Makefile.am) 
   * [tests/Makefile.am](https://svn.cs.uu.nl:12443/repos/trace/nix/trunk/tests/Makefile.am) 



### Gnucash

Complex GUI program, mixes Guile Scheme and C (SWIG bindings), and maybe some Perl. 

I'm not sure if I will manage to actually convert it, since it uses libtool, which is very tightly integrated with Autotools and libtool support is out of immediate scope of this project.  Even if I won't, usage patterns from Gnucash should be beneficial to the project. 
Home page
: 
[http://www.gnucash.org/](http://www.gnucash.org/) 


Browse sources
: 
[http://svn.gnucash.org/trac/browser/gnucash/trunk](http://svn.gnucash.org/trac/browser/gnucash/trunk) 


`configure.ac` file
: 
[configure.in](http://svn.gnucash.org/trac/browser/gnucash/trunk/configure.in) 


`Makefile.am` files
: 
   * [Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/Makefile.am) 
   * [accounts/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/Makefile.am) 
   * [accounts/C/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/C/Makefile.am) 
   * [accounts/da/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/da/Makefile.am) 
   * [accounts/de_AT/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/de_AT/Makefile.am) 
   * [accounts/de_CH/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/de_CH/Makefile.am) 
   * [accounts/de_DE/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/de_DE/Makefile.am) 
   * [accounts/el_GR/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/el_GR/Makefile.am) 
   * [accounts/en_GB/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/en_GB/Makefile.am) 
   * [accounts/es_ES/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/es_ES/Makefile.am) 
   * [accounts/fr_CA/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/fr_CA/Makefile.am) 
   * [accounts/fr_CH/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/fr_CH/Makefile.am) 
   * [accounts/fr_FR/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/fr_FR/Makefile.am) 
   * [accounts/hu_HU/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/hu_HU/Makefile.am) 
   * [accounts/it/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/it/Makefile.am) 
   * [accounts/nb/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/nb/Makefile.am) 
   * [accounts/pt_BR/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/pt_BR/Makefile.am) 
   * [accounts/pt_PT/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/pt_PT/Makefile.am) 
   * [accounts/sk/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/sk/Makefile.am) 
   * [accounts/tr_TR/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/accounts/tr_TR/Makefile.am) 
   * [checks/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/checks/Makefile.am) 
   * [doc/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/doc/Makefile.am) 
   * [doc/examples/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/doc/examples/Makefile.am) 
   * [intl-scm/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/intl-scm/Makefile.am) 
   * [lib/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/Makefile.am) 
   * [lib/glib28/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/glib28/Makefile.am) 
   * [lib/guile-www/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/guile-www/Makefile.am) 
   * [lib/libc/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/libc/Makefile.am) 
   * [lib/libqof/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/libqof/Makefile.am) 
   * [lib/libqof/backend/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/libqof/backend/Makefile.am) 
   * [lib/libqof/backend/file/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/libqof/backend/file/Makefile.am) 
   * [lib/libqof/qof/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/libqof/qof/Makefile.am) 
   * [lib/srfi/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/lib/srfi/Makefile.am) 
   * [m4/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/m4/Makefile.am) 
   * [packaging/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/packaging/Makefile.am) 
   * [packaging/win32/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/packaging/win32/Makefile.am) 
   * [src/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/Makefile.am) 
   * [src/app-utils/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/app-utils/Makefile.am) 
   * [src/app-utils/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/app-utils/test/Makefile.am) 
   * [src/backend/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/backend/Makefile.am) 
   * [src/backend/file/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/backend/file/Makefile.am) 
   * [src/backend/file/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/backend/file/test/Makefile.am) 
   * [src/backend/file/test/test-files/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/backend/file/test/test-files/Makefile.am) 
   * [src/backend/file/test/test-files/xml2/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/backend/file/test/test-files/xml2/Makefile.am) 
   * [src/backend/postgres/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/backend/postgres/Makefile.am) 
   * [src/backend/postgres/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/backend/postgres/test/Makefile.am) 
   * [src/bin/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/bin/Makefile.am) 
   * [src/bin/overrides/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/bin/overrides/Makefile.am) 
   * [src/bin/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/bin/test/Makefile.am) 
   * [src/business/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/Makefile.am) 
   * [src/business/business-core/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-core/Makefile.am) 
   * [src/business/business-core/file/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-core/file/Makefile.am) 
   * [src/business/business-core/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-core/test/Makefile.am) 
   * [src/business/business-gnome/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-gnome/Makefile.am) 
   * [src/business/business-gnome/glade/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-gnome/glade/Makefile.am) 
   * [src/business/business-gnome/schemas/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-gnome/schemas/Makefile.am) 
   * [src/business/business-gnome/ui/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-gnome/ui/Makefile.am) 
   * [src/business/business-ledger/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-ledger/Makefile.am) 
   * [src/business/business-reports/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-reports/Makefile.am) 
   * [src/business/business-utils/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/business-utils/Makefile.am) 
   * [src/business/dialog-tax-table/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/business/dialog-tax-table/Makefile.am) 
   * [src/calculation/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/calculation/Makefile.am) 
   * [src/calculation/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/calculation/test/Makefile.am) 
   * [src/core-utils/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/core-utils/Makefile.am) 
   * [src/doc/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/doc/Makefile.am) 
   * [src/doc/design/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/doc/design/Makefile.am) 
   * [src/doc/xml/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/doc/xml/Makefile.am) 
   * [src/engine/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/engine/Makefile.am) 
   * [src/engine/test-core/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/engine/test-core/Makefile.am) 
   * [src/engine/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/engine/test/Makefile.am) 
   * [src/experimental/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/experimental/Makefile.am) 
   * [src/experimental/cbb/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/experimental/cbb/Makefile.am) 
   * [src/experimental/cbb/cbb-engine/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/experimental/cbb/cbb-engine/Makefile.am) 
   * [src/experimental/cgi-bin/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/experimental/cgi-bin/Makefile.am) 
   * [src/experimental/gg/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/experimental/gg/Makefile.am) 
   * [src/experimental/ofx/explore/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/experimental/ofx/explore/Makefile.am) 
   * [src/gnc-module/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnc-module/Makefile.am) 
   * [src/gnc-module/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnc-module/test/Makefile.am) 
   * [src/gnc-module/test/misc-mods/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnc-module/test/misc-mods/Makefile.am) 
   * [src/gnc-module/test/mod-bar/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnc-module/test/mod-bar/Makefile.am) 
   * [src/gnc-module/test/mod-baz/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnc-module/test/mod-baz/Makefile.am) 
   * [src/gnc-module/test/mod-foo/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnc-module/test/mod-foo/Makefile.am) 
   * [src/gnome-search/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome-search/Makefile.am) 
   * [src/gnome-utils/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome-utils/Makefile.am) 
   * [src/gnome-utils/glade/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome-utils/glade/Makefile.am) 
   * [src/gnome-utils/schemas/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome-utils/schemas/Makefile.am) 
   * [src/gnome-utils/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome-utils/test/Makefile.am) 
   * [src/gnome-utils/ui/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome-utils/ui/Makefile.am) 
   * [src/gnome/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome/Makefile.am) 
   * [src/gnome/glade/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome/glade/Makefile.am) 
   * [src/gnome/schemas/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome/schemas/Makefile.am) 
   * [src/gnome/ui/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/gnome/ui/Makefile.am) 
   * [src/import-export/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/Makefile.am) 
   * [src/import-export/binary-import/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/binary-import/Makefile.am) 
   * [src/import-export/binary-import/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/binary-import/test/Makefile.am) 
   * [src/import-export/hbci/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/hbci/Makefile.am) 
   * [src/import-export/hbci/glade/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/hbci/glade/Makefile.am) 
   * [src/import-export/hbci/schemas/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/hbci/schemas/Makefile.am) 
   * [src/import-export/hbci/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/hbci/test/Makefile.am) 
   * [src/import-export/log-replay/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/log-replay/Makefile.am) 
   * [src/import-export/ofx/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/ofx/Makefile.am) 
   * [src/import-export/ofx/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/ofx/test/Makefile.am) 
   * [src/import-export/qif-import/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/qif-import/Makefile.am) 
   * [src/import-export/qif-import/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/qif-import/test/Makefile.am) 
   * [src/import-export/qif-io-core/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/qif-io-core/Makefile.am) 
   * [src/import-export/qif-io-core/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/qif-io-core/test/Makefile.am) 
   * [src/import-export/qif/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/qif/Makefile.am) 
   * [src/import-export/qif/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/qif/test/Makefile.am) 
   * [src/import-export/schemas/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/schemas/Makefile.am) 
   * [src/import-export/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/import-export/test/Makefile.am) 
   * [src/optional/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/optional/Makefile.am) 
   * [src/optional/xsl/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/optional/xsl/Makefile.am) 
   * [src/pixmaps/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/pixmaps/Makefile.am) 
   * [src/quotes/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/quotes/Makefile.am) 
   * [src/register/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/register/Makefile.am) 
   * [src/register/ledger-core/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/register/ledger-core/Makefile.am) 
   * [src/register/ledger-core/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/register/ledger-core/test/Makefile.am) 
   * [src/register/register-core/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/register/register-core/Makefile.am) 
   * [src/register/register-core/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/register/register-core/test/Makefile.am) 
   * [src/register/register-gnome/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/register/register-gnome/Makefile.am) 
   * [src/register/register-gnome/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/register/register-gnome/test/Makefile.am) 
   * [src/report/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/Makefile.am) 
   * [src/report/locale-specific/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/locale-specific/Makefile.am) 
   * [src/report/locale-specific/us/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/locale-specific/us/Makefile.am) 
   * [src/report/locale-specific/us/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/locale-specific/us/test/Makefile.am) 
   * [src/report/report-gnome/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/report-gnome/Makefile.am) 
   * [src/report/report-gnome/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/report-gnome/test/Makefile.am) 
   * [src/report/report-system/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/report-system/Makefile.am) 
   * [src/report/report-system/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/report-system/test/Makefile.am) 
   * [src/report/standard-reports/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/standard-reports/Makefile.am) 
   * [src/report/standard-reports/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/standard-reports/test/Makefile.am) 
   * [src/report/stylesheets/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/stylesheets/Makefile.am) 
   * [src/report/stylesheets/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/stylesheets/test/Makefile.am) 
   * [src/report/utility-reports/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/utility-reports/Makefile.am) 
   * [src/report/utility-reports/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/report/utility-reports/test/Makefile.am) 
   * [src/scm/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/scm/Makefile.am) 
   * [src/scm/gnumeric/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/scm/gnumeric/Makefile.am) 
   * [src/tax/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/tax/Makefile.am) 
   * [src/tax/us/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/tax/us/Makefile.am) 
   * [src/tax/us/test/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/tax/us/test/Makefile.am) 
   * [src/test-core/Makefile.am](http://svn.gnucash.org/trac/browser/gnucash/trunk/src/test-core/Makefile.am) 



### GRUB Legacy

Complex program; lots of documentation; conditional build; many custom build rules. 
Home page
: 
[http://www.gnu.org/software/grub/grub-legacy.en.html](http://www.gnu.org/software/grub/grub-legacy.en.html) 


Browse sources
: 
[http://cvs.savannah.gnu.org/viewvc/grub/?root=grub](http://cvs.savannah.gnu.org/viewvc/grub/?root=grub) 


`configure.ac` file
: 
[configure.ac](http://cvs.savannah.gnu.org/viewvc/grub/configure.ac?root=grub&view=markup) 


`Makefile.am` files
: 
   * [Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/Makefile.am?root=grub&view=markup) 
   * [lib/Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/lib/Makefile.am?root=grub&view=markup) 
   * [grub/Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/grub/Makefile.am?root=grub&view=markup) 
   * [stage1/Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/stage1/Makefile.am?root=grub&view=markup) 
   * [stage2/Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/stage2/Makefile.am?root=grub&view=markup) 
   * [netboot/Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/netboot/Makefile.am?root=grub&view=markup) 
   * [util/Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/util/Makefile.am?root=grub&view=markup) 
   * [docs/Makefile.am](http://cvs.savannah.gnu.org/viewvc/grub/docs/Makefile.am?root=grub&view=markup) 



### Irssi

Complex program and complex build process (generated Makefile.am files!).  C with embedded Perl.  Heavy usage of conditional build. 
Home page
: 
[http://www.irssi.org/](http://www.irssi.org/) 


Browse sources
: 
[http://svn.irssi.org/repos/irssi/trunk/](http://svn.irssi.org/repos/irssi/trunk/) 


`configure.ac` file
: 
[configure.in](http://svn.irssi.org/repos/irssi/trunk/configure.in) 


`Makefile.am` files
: 
   * [Makefile.am](http://svn.irssi.org/repos/irssi/trunk/Makefile.am) 
   * [docs/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/docs/Makefile.am) 
   * [docs/help/in/Makefile.am.gen](http://svn.irssi.org/repos/irssi/trunk/docs/help/in/Makefile.am.gen) 
   * [docs/help/Makefile.am.gen](http://svn.irssi.org/repos/irssi/trunk/docs/help/Makefile.am.gen) 
   * [scripts/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/scripts/Makefile.am) 
   * [scripts/examples/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/scripts/examples/Makefile.am) 
   * [servertest/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/servertest/Makefile.am) 
   * [src/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/Makefile.am) 
   * [src/lib-config/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/lib-config/Makefile.am) 
   * [src/lib-popt/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/lib-popt/Makefile.am) 
   * [src/perl/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/perl/Makefile.am) 
   * [src/fe-common/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/fe-common/Makefile.am) 
   * [src/fe-common/irc/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/fe-common/irc/Makefile.am) 
   * [src/fe-common/irc/dcc/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/fe-common/irc/dcc/Makefile.am) 
   * [src/fe-common/irc/notifylist/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/fe-common/irc/notifylist/Makefile.am) 
   * [src/fe-common/core/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/fe-common/core/Makefile.am) 
   * [src/irc/flood/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/irc/flood/Makefile.am) 
   * [src/irc/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/irc/Makefile.am) 
   * [src/irc/proxy/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/irc/proxy/Makefile.am) 
   * [src/irc/core/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/irc/core/Makefile.am) 
   * [src/irc/dcc/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/irc/dcc/Makefile.am) 
   * [src/irc/bot/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/irc/bot/Makefile.am) 
   * [src/irc/notifylist/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/irc/notifylist/Makefile.am) 
   * [src/core/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/core/Makefile.am) 
   * [src/fe-text/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/fe-text/Makefile.am) 
   * [src/fe-none/Makefile.am](http://svn.irssi.org/repos/irssi/trunk/src/fe-none/Makefile.am) 
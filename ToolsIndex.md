# Introduction

SCons core provides tools implemented as Python modules.  This is fine for tools that are part of the SCons distribution, but for contributed tools supported separately from the SCons code repository, using modules is not the best architecture.  Fortunately, SCons allows for tools to be implemented as Python packages (i.e. directories with a file `__init__.py`).  This allows for tools to be managed as packages in distributed version control system (DVCS) branches and repositories -- a Python package is a directory and directories not files are the top-level thing managed by a DVCS (which is why it is easier to deal with packages rather than modules using a DVCS). 

To manage tools that are not part of SCons core, or provide enhancements for core tools independently, a DVCS (e.g. Mercurial, Git, Bazaar) repository (branch in Bazaar) should be created and the directory should contain a file `__init__.py` so that it is a package in the Python sense. The tool can then be installed by cloning (branching in Bazaar) the repository into the `site_scons/site_tools` directory. 

No matter which DVCS and hosting site is used for a given tool, it should be indexed on this page:  this page is the central index of all contributed tools.  The index works best where there is a wiki page explaining the tool linked to by the entry in the first column of the tool list. 


# Install and usage

Installing an external Tool requires you to clone (branch in Bazaar) the contents of the package's folder to 

1. `/path_to_your_project/site_scons/site_tools/foo`, if you need the `foo` Tool in one project only, or 

2. `~/.scons/site_scons/site_tools/foo`, for a personal installation of `foo` that can be used by you for all your projects (SCons 2.1 and later). 

In SCons 2.1 and later, the following paths are tried in order to detect SCons specific settings, like the `site_scons/site_tools` folder:

| OS (Platform)    | Paths         |
|-----------------:|:--------------|
| Windows<br> (win32/cygwin)      | `$ALLUSERSPROFILE\Application Data\scons`<br> `$USERPROFILE\Local Settings\Applicatio Data\scons`<br> `$APPDATA\scons`<br> `~\.scons` |
| MacOS X (darwin) | `/Library/Application Support/SCons`<br> `/opt/local/share/scons`<br> `/sw/share/scons`<br> `~/Library/Application Support/SCons`<br> `~/.scons` |
| Solaris (sunos)  | `/opt/sfw/scons`<br> `/usr/share/scons`<br> `~/.scons` |
| Linux/HPUX/... (other) | `/usr/share/scons`<br> `~/.scons` |

(see also sect. 18.7 [http://scons.org/doc/production/HTML/scons-user/ch18s07.html](http://scons.org/doc/production/HTML/scons-user/ch18s07.html) in the User's Guide). 

This makes the tool available but it must be included explicitly in a SCons build by creating an Environment with a `tools` entry since only named tools from the SCons core are initialized automatically when SCons runs. Example: 


```python
# Create environment and init Tool foo
env = Environment(tools=['foo'])

# Use the builder, provided by the Tool foo
env.Foo(Glob('*.foo'))
```

# Have a pick (the actual index)

The index of Tools maintained outside of SCons repository. If the Name column is a link, follow it for more details.

**Name**  | **DVCS**  | **Location**  | **Branch/Clone command** |
---------:|:----------|--------------:|:-------------------------|
Chapel  | Mercurial  | <https://bitbucket.org/russel/scons_chapel>  | `hg clone https://bitbucket.org/russel/scons_chapel chapel`
[C#](CsharpBuilder)  | Git  | <https://github.com/SCons/scons-contrib/tree/master/sconscontrib/SCons/Tool/csharp>  | `git clone https://github.com/SCons/scons-contrib`
[CPython](CPythonTool)  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_cpython>  | `hg clone https://bitbucket.org/dirkbaechle/scons_cpython cpython`
D [1]  |   |   |  
[Docbook](DocbookTool)  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_docbook>  | `hg clone https://bitbucket.org/dirkbaechle/scons_docbook docbook`
Doxyfile  | Git  | <https://github.com/ptomulik/scons-tool-doxyfile>  | `git clone https://github.com/ptomulik/scons-tool-doxyfile` 
[Doxygen](DoxygenBuilder)  | Mercurial  | <https://bitbucket.org/russel/scons_doxygen>  | `hg clone https://bitbucket.org/russel/scons_doxygen doxygen`
dvipdfm  | Git  | <https://github.com/ptomulik/scons-tool-dvipdfm>  | `git clone https://github.com/ptomulik/scons-tool-dvipdfm dvipdfm` | 
[Eiffel](EiffelStudioTool)  | Bazaar  | <https://launchpad.net/scons-eiffel>  | `bzr branch lp:scons-eiffel eiffel` 
Erlang  | Mercurial  | <https://bitbucket.org/russel/scons_erlang>  | `hg clone https://bitbucket.org/russel/scons_erlang erlang` | 
fastcpp  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_fastcpp>  | `hg clone https://bitbucket.org/dirkbaechle/scons_fastcpp fastcpp`
GccCov  | Git  | <https://github.com/ptomulik/scons-tool-gcccov>  | `git clone https://github.com/ptomulik/scons-tool-gcccov gcccov` | 
Gnuplot  | Git  | <https://github.com/ptomulik/scons-tool-gnuplot>  | `git clone https://github.com/ptomulik/scons-tool-gnuplot gnuplot`
Go  | Git  | <http://github.com/alberts/goscons/tree/master/goscons/>  | `git clone git://github.com/alberts/goscons.git`
[GObject (gob2)](Gob2Tool)  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_gob2>  | `hg clone https://bitbucket.org/dirkbaechle/scons_gob2 gob2`
[Haskell](GhcBuilder)  | Mercurial  | <https://bitbucket.org/russel/scons_haskell>  | `hg clone https://bitbucket.org/russel/scons_haskell haskell`
Jinja2  | Git  | <https://github.com/hgomersall/scons-jinja>  | `git clone https://github.com/hgomersall/scons-jinja jinja`
Matlab (Mex)  | Git  | <https://github.com/marcecj/scons_matlab>  | `git clone https://github.com/marcecj/scons_matlab matlab`
[MFObject](MFObject)  | Bazaar  | <https://code.launchpad.net/~asomers/sconsaddons/mfobject>  | `bzr branch lp:~asomers/sconsaddons/mfobject`
[OCaml](OcamlBuilder)  | Mercurial  | <https://bitbucket.org/russel/scons_ocaml>  | `hg clone https://bitbucket.org/russel/scons_ocaml ocaml`
Perl | Mercurial  | <https://bitbucket.org/carandraug/scons-perl5>  | `hg clone https://bitbucket.org/carandraug/scons-perl5 scons-perl5`
pkg-config | Git  | <https://github.com/manuelnaranjo/scons-pkg-config>  | `git clone https://github.com/manuelnaranjo/scons-pkg-config pkg-config`
[Protocol Buffers](ProtocBuilder)  | Mercurial  | <https://bitbucket.org/russel/scons_protobuf>  | `hg clone https://bitbucket.org/russel/scons_protobuf protoc`
[Qt4](Qt4Tool)  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_qt4>  | `hg clone https://bitbucket.org/dirkbaechle/scons_qt4 qt4`
[Qt5](Qt5Tool)  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_qt5>  | `hg clone https://bitbucket.org/dirkbaechle/scons_qt5 qt5`
[reST (docutils)](ReStructuredTextBuilder)  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_rest>  | `hg clone https://bitbucket.org/dirkbaechle/scons_rest rest`
[RightNow](RightNow)  | Bazaar  | <https://code.launchpad.net/~asomers/sconsaddons/rightnow>  | `bzr branch lp:~asomers/sconsaddons/rightnow`
SIP  | Mercurial  | <https://bitbucket.org/dirkbaechle/scons_sip>  | `hg clone https://bitbucket.org/dirkbaechle/scons_sip sip`
Sphinx  | Mercurial  | <http://bitbucket.org/zondo/sphinx-scons/overview>  | `hg clone https://bitbucket.org/zondo/sphinx-scons`
[sphinx4scons](sphinx4scons)  | Mercurial  | <https://bitbucket.org/wingbrant/sphinx4scons/>  | `hg clone https://bitbucket.org/wingbrant/sphinx4scons`
[Vala](ValaBuilder)  | Mercurial  | <https://bitbucket.org/russel/scons_vala>  | `hg clone https://bitbucket.org/russel/scons_vala vala`
[Watcom](Watcom)  | Git  | <https://bitbucket.org/cr1901/scons-wat>  | `git clone https://bitbucket.org/cr1901/scons-wat watcom`
Xcode | Mercurial | <https://bitbucket.org/al45tair/scons-xcode> | `hg clone https://bitbucket.org/al45tair/scons-xcode xcode`
X10  | Mercurial  | <https://bitbucket.org/russel/scons_x10>  | `hg clone https://bitbucket.org/russel/scons_x10 x10`
Wayland | git | <https://git.sr.ht/~sircmpwn/scons-wayland-scanner> | `git clone https://git.sr.ht/~sircmpwn/scons-wayland-scanner wayland-scanner`



[1]: The D tool is no longer developed outside of the SCons source tree (as it once was) to enable correct integration between D, C++ and C in multi-language systems.  D tool development now happens in [a clone of the SCons repository specifically for developing the D tool](https://bitbucket.org/russel/scons_d_tooling). 

# Workflows

If you simply want to use the Tools above, or have a look at the sources, issue the command given in the **Branch/Clone** column. This will give you a local copy to work with. 

Patching or extending and then, finally, contributing your code, needs a little more effort.  For each DVCS, the following sections try to outline the required steps. 


## Mercurial/BitBucket

If you just want to create a read-only copy of the tool then just use "hg clone . . . ".   If you are wanting to get involved in development of the tool then you will need a writeable clone. 

* You will need to create a [BitBucket](https://bitbucket.org/) account if you haven't already got one.  Navigate to [BitBucket](https://bitbucket.org/) and create an account and then login.  If you already have an account then just login. 
* In order to be able to push to your repository, you need to upload SSH keys to [BitBucket](https://bitbucket.org/).  Your Account Settings page has a section for SSH keys. 
* If you are cloning an existing  tool then use the [BitBucket](https://bitbucket.org/) "fork" button on the existing tool repository.  At the time of writing (2011-08-13T10:50+01:00) the icon is a blue arrow pointing up and right. 
* If you are creating a new tool then create the repository on [BitBucket](https://bitbucket.org/). 
* Now you clone your [BitBucket](https://bitbucket.org/) repository to your local machines in an appropriate place. 
* When you make changes locally remember to push them up to [BitBucket](https://bitbucket.org/) when they are ready for publishing. 
* If you have cloned a pre-existing repository remember to issue pull requests when you think you have a change that should be merged into the mainline. 

## Bazaar/Launchpad

We assume that you have initially branched an existing tool, modified it and want to publish your changes. 

* If you don't already have a login at [Launchpad](https://launchpad.net), register there first. A homepage is created for you, and on it you find the [OpenID](https://launchpad.net/+help/openid.html) URL. It has your _Launchpad-login_ as last part, after the `~`. 
* For identification purposes you need to provide a public SSH key to Launchpad. If necessary, [create a new one under your OS of choice](https://help.launchpad.net/YourAccount/CreatingAnSSHKeyPair). Import your key under the entry **SSH keys** on your Launchpad homepage. 
* Now you can issue the command `bzr launchpad-login yournick` on your local machine. Here, `yournick` is your personal _Launchpad-login_ as described above. This tells Bazaar to use this nickname for all your following commits/pushes, directed at Launchpad. 
* You should also check your local name (the one that is displayed for commits) with `bzr whoami` and change it by `bzr whoami "John Doe <jdoe@lostmymind.com>"`, respectively. 
* Commit your local changes with `bzr commit`. 
* Then, push your local branch up to Launchpad with `bzr push lp:~yournick/toolname/branchname`. Correctly replacing `yournick` (your _Launchpad-login_), `toolname` (name of the tool) and `branchname` (name of your branch), this creates a new branch under your account associated with the tool project. Since Launchpad stores all the different branches in a sort of "matrix", your contribution should show up on your page and on the tool project page along with the original branch. 
* As described on the [Code/Uploading a Branch](https://help.launchpad.net/Code/UploadingABranch) page, you can continue to commit your subsequent changes locally `bzr commit` or publish them again by a push `bzr push lp:~yournick/toolname/branchname`. 
* Eventually, use the "Propose for merging" link (on the Launchpad page of your branch) to get your changes into the _mainline_ (also known as _trunk_). 
Please also regard the special page [ToolsBazaarWorkflows](ToolsBazaarWorkflows), it contains more info about 

* proper merging, 
* how to setup a new project for a Tool and 
* adding a downloadable Tarball to your release 
In many ways all branches for a given tool are equal; all branches are effectively forks of the tool.  The mainline is the one agreed to be the mainline and is the one to be indexed above. 

For more detailed infos about Bazaar and DVCS in general, you should also visit the [UsingBzr](http://scons.org/wiki/UsingBzr) page.

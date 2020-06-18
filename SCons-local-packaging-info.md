Here's the current tree/file layout for existing scons-local packaging.

`scons-local`
`├── scons-3.1.1.bat`
`├── scons-LICENSE`
`├── scons-README`
`├── scons-configure-cache.py`
`├── scons-local-3.1.1`
`│   ├── SCons`
`│   │   ├── Action.py`
`│   │   ├── Builder.py`
`│   │   ├── CacheDir.py`
`│   │   ├── Conftest.py`
`│   │   ├── Debug.py`
`│   │   ├── Defaults.py`
`│   │   ├── Environment.py`
`│   │   ├── Errors.py`
`│   │   ├── Executor.py`
`│   │   ├── Job.py`
`│   │   ├── Memoize.py`
`│   │   ├── Node`
`│   │   │   ├── Alias.py`
`│   │   │   ├── FS.py`
`│   │   │   ├── Python.py`
`│   │   │   └── __init__.py`
`│   │   ├── PathList.py`
`│   │   ├── Platform`
`│   │   │   ├── __init__.py`
`│   │   │   ├── aix.py`
`│   │   │   ├── cygwin.py`
`│   │   │   ├── darwin.py`
`│   │   │   ├── hpux.py`
`│   │   │   ├── irix.py`
`│   │   │   ├── mingw.py`
`│   │   │   ├── os2.py`
`│   │   │   ├── posix.py`
`│   │   │   ├── sunos.py`
`│   │   │   ├── virtualenv.py`
`│   │   │   └── win32.py`
`│   │   ├── SConf.py`
`│   │   ├── SConsign.py`
`│   │   ├── Scanner`
`│   │   │   ├── C.py`
`│   │   │   ├── D.py`
`│   │   │   ├── Dir.py`
`│   │   │   ├── Fortran.py`
`│   │   │   ├── IDL.py`
`│   │   │   ├── LaTeX.py`
`│   │   │   ├── Prog.py`
`│   │   │   ├── RC.py`
`│   │   │   ├── SWIG.py`
`│   │   │   └── __init__.py`
`│   │   ├── Script`
`│   │   │   ├── Interactive.py`
`│   │   │   ├── Main.py`
`│   │   │   ├── SConsOptions.py`
`│   │   │   ├── SConscript.py`
`│   │   │   └── __init__.py`
`│   │   ├── Subst.py`
`│   │   ├── Taskmaster.py`
`│   │   ├── Tool`
`│   │   │   ├── 386asm.py`
`│   │   │   ├── DCommon.py`
`│   │   │   ├── FortranCommon.py`
`│   │   │   ├── GettextCommon.py`
`│   │   │   ├── JavaCommon.py`
`│   │   │   ├── MSCommon`
`│   │   │   │   ├── __init__.py`
`│   │   │   │   ├── arch.py`
`│   │   │   │   ├── common.py`
`│   │   │   │   ├── netframework.py`
`│   │   │   │   ├── sdk.py`
`│   │   │   │   ├── vc.py`
`│   │   │   │   └── vs.py`
`│   │   │   ├── PharLapCommon.py`
`│   │   │   ├── __init__.py`
`│   │   │   ├── aixc++.py`
`│   │   │   ├── aixcc.py`
`│   │   │   ├── aixcxx.py`
`│   │   │   ├── aixf77.py`
`│   │   │   ├── aixlink.py`
`│   │   │   ├── applelink.py`
`│   │   │   ├── ar.py`
`│   │   │   ├── as.py`
`│   │   │   ├── bcc32.py`
`│   │   │   ├── c++.py`
`│   │   │   ├── cc.py`
`│   │   │   ├── clang.py`
`│   │   │   ├── clangCommon`
`│   │   │   │   └── __init__.py`
`│   │   │   ├── clangxx.py`
`│   │   │   ├── cvf.py`
`│   │   │   ├── cxx.py`
`│   │   │   ├── cyglink.py`
`│   │   │   ├── default.py`
`│   │   │   ├── dmd.py`
`│   │   │   ├── docbook`
`│   │   │   │   └── __init__.py`
`│   │   │   ├── dvi.py`
`│   │   │   ├── dvipdf.py`
`│   │   │   ├── dvips.py`
`│   │   │   ├── f03.py`
`│   │   │   ├── f08.py`
`│   │   │   ├── f77.py`
`│   │   │   ├── f90.py`
`│   │   │   ├── f95.py`
`│   │   │   ├── filesystem.py`
`│   │   │   ├── fortran.py`
`│   │   │   ├── g++.py`
`│   │   │   ├── g77.py`
`│   │   │   ├── gas.py`
`│   │   │   ├── gcc.py`
`│   │   │   ├── gdc.py`
`│   │   │   ├── gettext_tool.py`
`│   │   │   ├── gfortran.py`
`│   │   │   ├── gnulink.py`
`│   │   │   ├── gs.py`
`│   │   │   ├── gxx.py`
`│   │   │   ├── hpc++.py`
`│   │   │   ├── hpcc.py`
`│   │   │   ├── hpcxx.py`
`│   │   │   ├── hplink.py`
`│   │   │   ├── icc.py`
`│   │   │   ├── icl.py`
`│   │   │   ├── ifl.py`
`│   │   │   ├── ifort.py`
`│   │   │   ├── ilink.py`
`│   │   │   ├── ilink32.py`
`│   │   │   ├── install.py`
`│   │   │   ├── intelc.py`
`│   │   │   ├── ipkg.py`
`│   │   │   ├── jar.py`
`│   │   │   ├── javac.py`
`│   │   │   ├── javah.py`
`│   │   │   ├── latex.py`
`│   │   │   ├── ldc.py`
`│   │   │   ├── lex.py`
`│   │   │   ├── link.py`
`│   │   │   ├── linkloc.py`
`│   │   │   ├── m4.py`
`│   │   │   ├── masm.py`
`│   │   │   ├── midl.py`
`│   │   │   ├── mingw.py`
`│   │   │   ├── msgfmt.py`
`│   │   │   ├── msginit.py`
`│   │   │   ├── msgmerge.py`
`│   │   │   ├── mslib.py`
`│   │   │   ├── mslink.py`
`│   │   │   ├── mssdk.py`
`│   │   │   ├── msvc.py`
`│   │   │   ├── msvs.py`
`│   │   │   ├── mwcc.py`
`│   │   │   ├── mwld.py`
`│   │   │   ├── nasm.py`
`│   │   │   ├── packaging`
`│   │   │   │   ├── __init__.py`
`│   │   │   │   ├── ipk.py`
`│   │   │   │   ├── msi.py`
`│   │   │   │   ├── rpm.py`
`│   │   │   │   ├── src_tarbz2.py`
`│   │   │   │   ├── src_targz.py`
`│   │   │   │   ├── src_tarxz.py`
`│   │   │   │   ├── src_zip.py`
`│   │   │   │   ├── tarbz2.py`
`│   │   │   │   ├── targz.py`
`│   │   │   │   ├── tarxz.py`
`│   │   │   │   └── zip.py`
`│   │   │   ├── pdf.py`
`│   │   │   ├── pdflatex.py`
`│   │   │   ├── pdftex.py`
`│   │   │   ├── qt.py`
`│   │   │   ├── rmic.py`
`│   │   │   ├── rpcgen.py`
`│   │   │   ├── rpm.py`
`│   │   │   ├── rpmutils.py`
`│   │   │   ├── sgiar.py`
`│   │   │   ├── sgic++.py`
`│   │   │   ├── sgicc.py`
`│   │   │   ├── sgicxx.py`
`│   │   │   ├── sgilink.py`
`│   │   │   ├── sunar.py`
`│   │   │   ├── sunc++.py`
`│   │   │   ├── suncc.py`
`│   │   │   ├── suncxx.py`
`│   │   │   ├── sunf77.py`
`│   │   │   ├── sunf90.py`
`│   │   │   ├── sunf95.py`
`│   │   │   ├── sunlink.py`
`│   │   │   ├── swig.py`
`│   │   │   ├── tar.py`
`│   │   │   ├── tex.py`
`│   │   │   ├── textfile.py`
`│   │   │   ├── tlib.py`
`│   │   │   ├── wix.py`
`│   │   │   ├── xgettext.py`
`│   │   │   ├── yacc.py`
`│   │   │   └── zip.py`
`│   │   ├── Util.py`
`│   │   ├── Variables`
`│   │   │   ├── BoolVariable.py`
`│   │   │   ├── EnumVariable.py`
`│   │   │   ├── ListVariable.py`
`│   │   │   ├── PackageVariable.py`
`│   │   │   ├── PathVariable.py`
`│   │   │   └── __init__.py`
`│   │   ├── Warnings.py`
`│   │   ├── __init__.py`
`│   │   ├── __main__.py`
`│   │   ├── compat`
`│   │   │   ├── __init__.py`
`│   │   │   └── _scons_dbm.py`
`│   │   ├── cpp.py`
`│   │   ├── dblite.py`
`│   │   └── exitfuncs.py`
`│   └── scons-3.1.1-py2.7.egg-info`
`├── scons-time.py`
`├── scons.bat`
`├── scons.py`
`└── sconsign.py`

`13 directories, 203 files`

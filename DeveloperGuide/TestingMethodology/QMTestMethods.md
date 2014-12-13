
These are the classes in the test infrastructure and their methods. Each class described below is located in a module by the same name:  
 `    from TestCmd import TestCmd`  
 If a class is derived from another class, the superclass is given in parenthesis. 

xxx At the moment, only limited documentation is present; basically, this is just something I can search when I need a particular function.  In time, descriptions will be added for each method.  There may be methods missing that need to be added and there may be internal routines present that need to be removed.  TLC is needed until this becomes actual documentation.  This is intended to be "quick-look" documentation and detailed documentation (including the vaunted examples) would be linked from the description. 


### TestCmd

Access to test directory. Create pathnames within the test directory. Write (and read) test files. Run a command and capture stdout and stderr. Miscellaneous operating system and file system operations. Succeed, fail, and skip test. 

Initialize and tear down. 
TestCmd.__init__(self, description = None, program = None, interpreter = None, workdir = None, subdir = None, verbose = None, match = None, combine = 0, universal_newlines = 1)
: 

TestCmd.description_set(self, description)
: 

TestCmd.program_set(self, program)
:  String or list of strings.  The command to be tested and its arguments. 

TestCmd.interpreter_set(self, interpreter)
: String or list of strings.  If the command to be tested is a script, the interpreter and any arguments. 

TestCmd.workdir_set(self, path)
: 
Creates a temporary working directory.  if `path` is `None` or `''` a unique name is created. 


cnt = TestCmd.subdir(self, *subdirs)
: Create subdirectories under the current working directory.  Errors are ignored; the return value is the number of subdirectories actually created. 

TestCmd.verbose_set(self, verbose)
: 

TestCmd.preserve(self, *conditions)
: 
If the test terminates due to one of the `conditions`, preserve the temporary test directory.  The `conditions` can be any or all of 'pass_test', 'fail_test', or 'no_result'; no `conditions` preserves the directory for all cases. 


TestCmd.cleanup(self, condition = None)
: 


Skip, fail, succeed.  One of these must be executed to terminate the test run. 
TestCmd.no_result(self, condition = 1, function = None, skip = 0)
: 
Reports NO RESULT from the test if the `condition` is true.  If the test is failing, runs `function` with no arguments to clean up.  The first `skip` stack frames are not displayed; set it to a large number to suppress the display completely. 


TestCmd.fail_test(self, condition = 1, function = None, skip = 0)
: 
Fails the test if the `condition` is true.  If the test is failing, runs `function` with no arguments to clean up.  The first `skip` stack frames are not displayed; set it to a large number to suppress the display completely. 


TestCmd.pass_test(self, condition = 1, function = None)
: 
Passes the test if the `condition` is true.  If the test is succeeding, runs `function` with no arguments. 



Workspace.  The `canonicalize()` and `workpath()` methods appear to be equivalent; I don't know why both exist. 
TestCmd.canonicalize(self, path)
: 
Returns the full path within the working directory.  The `path` argument may either be a string or a list of strings representing path elements. 


TestCmd.workpath(self, *args)
: Returns the full path within the working directory.  The arguments are strings of path elements. 

TestCmd.write(self, file, content, mode = 'wb')
: 
Write `content` (a string) to the workspace file. 


TestCmd.read(self, file, mode = 'rb')
: Return the content of the workspace file. 


Run command. 
cmd_list = TestCmd.command_args(self, program = None, interpreter = None, arguments = None)
: 
Constructs a command list.  If `program` or `interpreter` are not specified, the corresponding default is used. 


popen = TestCmd.start(self, program = None, interpreter = None, arguments = None, universal_newlines = None, **kw)
: 

TestCmd.finish(self, popen, **kw)
: 

TestCmd.run(self, program = None, interpreter = None, arguments = None, chdir = None, stdin = None, universal_newlines = None)
: 


Test results. 
content = TestCmd.stdout(self, run = None)
: 
Return the standard output from the specified `run`.  If `run` is `None`, the latest run is returned. 


content = TestCmd.stderr(self, run = None)
: 
Return the standard error from the specified `run`.  If `run` is `None`, the latest run is returned. 


bool = TestCmd.match(self, lines, matches)
: 
Either `match_exact` or `match_re` depending on the `match` argument when the class was initialized. 


bool = TestCmd.match_exact(self, lines, matches)
: 
Returns true if `lines` and `matches` are the same and false otherwise.  Both `lines` and `matches` can be either a string or a list of strings. 


bool = TestCmd.match_re(self, lines, res)
: 
Returns true if `lines` matches the regular expressions in `res`.  Both `lines` and `res` can be either a string or a list of strings. 


bool = TestCmd.match_re_dotall(self, lines, res)
: 
Same as match_re except that the regular expressions are compiled with `re.DOTALL`. 


module.diff_re(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
: 
A quick-and-dirty line-by-line diff.  Both `a` and `b` must be lists of strings; lines in `a` are compared with regular expressions in `b`.  The keyword arguments are all ignored. 



Miscellaneous. 
path = TestCmd.where_is(self, file, path=None, pathext=None)
: 

path = TestCmd.tempdir(self, path=None)
: 
Creates a temporary directory and arranges to remove it when the test completes.  A `path` of `None` causes a unique directory to be created.  Note that the path is not canonicalized. 


TestCmd.chmod(self, path, mode)
: 

TestCmd.symlink(self, target, link)
: 

TestCmd.touch(self, path, mtime=None)
: 

TestCmd.unlink(self, file)
: 

TestCmd.sleep(self, seconds = default_sleep_seconds)
: 

TestCmd.rmdir(self, dir)
: 

TestCmd.readable(self, top, read=1)
: 

TestCmd.writable(self, top, write=1)
: 

TestCmd.executable(self, top, execute=1)
: 



### TestCommon(TestCmd)

Extension of `TestCmd`. 

Module variables. 
module.python_executable
: 

module.exe_suffix
: 

module.obj_suffix
: 

module.shobj_prefix
: 

module.shobj_suffix
: 

module.lib_prefix
: 

module.lib_suffix
: 

module.dll_prefix
: 

module.dll_suffix
: 


Uncategorized. 
TestCommon.__init__(self, **kw)
: 

TestCommon.banner(self, s, width=None)
: 

TestCommon.diff(self, a, b, name, *args, **kw)
: 

TestCommon.skip_test(self, message="Skipping test.\n")
: Print the message.  If TESTCOMMON_PASS_SKIPS is set in the (shell) environment, pass the test, otherwise say no result. 


File status. 
TestCommon.must_exist(self, *files)
: Fail test if file(s) do not exist. 

TestCommon.must_not_exist(self, *files)
: Fail test if file(s) exist. 

TestCommon.must_be_writable(self, *files)
: Fail test if file(s) do not exist or cannot be written. 

TestCommon.must_not_be_writable(self, *files)
: Fail test if file(s) do not exist or can be written. 


File contents. 
TestCommon.must_match(self, file, expect, mode = 'rb')
: 
Ensure that the `file` contents exactly match the `expect` parameter. 


TestCommon.must_contain(self, file, required, mode = 'rb')
: 
Ensure that the `file` contains the `required` text somewhere within it. 


TestCommon.must_contain_all_lines(self, output, lines, title=None, find=None)
: 
Ensure that all of the `lines` (a list of strings) appear in `output`.  The `title` appears above any failure output.  The `find` function returns true if the lie (second arg) is in the output (first arg). 


TestCommon.must_contain_any_line(self, output, lines, title=None, find=None)
: 
Ensure that `output` contains at least one of the `lines` specified.  The `ti tle` appears above any failure output.  The `find` function returns true if the lie (second arg) is in the output (first arg). 


TestCommon.must_contain_lines(self, lines, output, title=None)
: Deprecated. 

TestCommon.must_not_contain_any_line(self, output, lines, title=None, find=None)
: 

TestCommon.must_not_contain_lines(self, lines, output, title=None)
: 


Overrides. 
popen = TestCommon.start(self, program = None, interpreter = None, arguments = None, universal_newlines = None, **kw)
: 

TestCommon.finish(self, popen, stdout = None, stderr = '', status = 0, **kw)
: 

TestCommon.run(self, options = None, arguments = None, stdout = None, stderr = '', status = 0, **kw)
: 



### TestSCons(TestCommon)

Specialized routines with SCons-specific knowledge for running `SConstruct`s. 

Module variables and functions. 
module.default_version
: 

module.copyright_years
: 

module.SConsVersion
: 

module.machine
: 

module.python
: = python_executable 

module._python_
: = '"' + python_executable + '"' 

module._exe
: = exe_suffix 

module._obj
: = obj_suffix 

module._shobj
: = shobj_suffix 

module.shobj_
: = shobj_prefix 

module._lib
: = lib_suffix 

module.lib_
: = lib_prefix 

module._dll
: = dll_suffix 

module.dll_
: = dll_prefix 

module.re_escape(str)
: 

module.python_version_string()
: 

module.python_minor_version_string()
: 

module.unsupported_python_version(version=sys.version_info)
: 

module.deprecated_python_version(version=sys.version_info)
: 

module.deprecated_python_expr
: 


Uncategorized. 
TestSCons.scons_version
: = SConsVersion 

TestSCons.get_python_version(self)
: 
Deprecated, use `module.python_minor_version_string()`. 


TestSCons.__init__(self, **kw)
: 

TestSCons.Environment(self, ENV=None, *args, **kw)
: 

TestSCons.detect(self, var, prog=None, ENV=None, norm=None)
: 

TestSCons.detect_tool(self, tool, prog=None, ENV=None)
: 

TestSCons.where_is(self, prog, path=None)
: 

TestSCons.wrap_stdout(self, build_str = "", read_str = "", error = 0, cleaning = 0)
: 

TestSCons.up_to_date(self, options = None, arguments = None, read_str = "", **kw)
: 

TestSCons.not_up_to_date(self, options = None, arguments = None, **kw)
: 

msg = TestSCons.diff_substr(self, expect, actual, prelen=20, postlen=40)
: 
Return a string displaying the first mismatched character between two strings (`expect` and `actual`) that are known to be different. 


TestSCons.python_file_line(self, file, line)
: 

TestSCons.normalize_pdf(self, s)
: 

paths = TestSCons.paths(self, patterns)
: 
Expand a list of `patterns` into a list of matching pathnames. 


TestSCons.wait_for(self, fname, timeout=10.0, popen=None)
: 
Wait up to `timeout` seconds for `fname` to exist.  If `popen` is given, terminate it by closing the standard input. 


TestSCons.get_alt_cpp_suffix(self)
: Return altername C++ suffix based on whether the filesystem is case sensitive. 

TestSCons.checkLogAndStdout(self, checks, results, cached, logfile, sconf_dir, sconstruct, doCheckLog=1, doCheckStdout=1)
: 


Java. 
TestSCons.java_ENV(self, version=None)
: 

TestSCons.java_where_includes(self,version=None)
: 

TestSCons.java_where_java_home(self,version=None)
: 

TestSCons.java_where_jar(self, version=None)
: 

TestSCons.java_where_java(self, version=None)
: 

TestSCons.java_where_javac(self, version=None)
: 

TestSCons.java_where_javah(self, version=None)
: 

TestSCons.java_where_rmic(self, version=None)
: 


Qt. 
TestSCons.Qt_dummy_installation(self, dir='qt')
: 

TestSCons.Qt_create_SConstruct(self, place)
: 


SWIG. 
TestSCons.get_platform_python_info(self)
: 
Skips test if there is no '`python`' in the path.  Returns pathname of Python executable, pathname of Python include directory (for `CPPPATH`), pathname of Python library directory (for `LIBPATH`), and the library name (for `LIBS`). 




### TestSConsign(TestSCons)
TestSConsign.__init__(self, *args, **kw)
: 

TestSConsign.script_path(self, script)
: 

TestSConsign.set_sconsign(self, sconsign)
: 

TestSConsign.run_sconsign(self, *args, **kw)
: 



### TestSConsMSVS(TestSCons)
TestSConsMSVS.msvs_versions(self)
: 

TestSConsMSVS.vcproj_sys_path(self, fname)
: 

TestSConsMSVS.msvs_substitute(self, input, msvs_ver, subdir=None, sconscript=None, python=None, project_guid=None)
: 

TestSConsMSVS.get_msvs_executable(self, version)
: 



### TestRuntest(TestCommon)
TestRuntest.__init__(self, **kw)
: 

TestRuntest.write_fake_scons_source_tree(self)
: 

TestRuntest.write_failing_test(self, name)
: 

TestRuntest.write_no_result_test(self, name)
: 

TestRuntest.write_passing_test(self, name)
: 



### TestSCons_time(TestCommon)
TestSCons_time.__init__(self, **kw)
: 

TestSCons_time.archive_split(self, path)
: 

TestSCons_time.fake_logfile(self, logfile_name, index=0)
: 

TestSCons_time.profile_data(self, profile_name, python_name, call, body)
: 

TestSCons_time.tempdir_re(self, *args)
: 

TestSCons_time.write_fake_aegis_py(self, name)
: 

TestSCons_time.write_fake_scons_py(self)
: 

TestSCons_time.write_fake_svn_py(self, name)
: 

TestSCons_time.write_sample_directory(self, archive, dir, files)
: 

TestSCons_time.write_sample_tarfile(self, archive, dir, files)
: 

TestSCons_time.write_sample_zipfile(self, archive, dir, files)
: 

TestSCons_time.write_sample_project(self, archive, dir=None)
: 


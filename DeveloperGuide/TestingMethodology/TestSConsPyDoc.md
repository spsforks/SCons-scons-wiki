
```
#!text

Help on module TestSCons:

NAME
    TestSCons

FILE
    /Users/bdbaddog/devel/scons/hg/scons/QMTest/TestSCons.py

DESCRIPTION
    TestSCons.py:  a testing framework for the SCons software construction
    tool.
    
    A TestSCons environment object is created via the usual invocation:
    
        test = TestSCons()
    
    TestScons is a subclass of TestCommon, which in turn is a subclass
    of TestCmd), and hence has available all of the methods and attributes
    from those classes, as well as any overridden or additional methods or
    attributes defined in this subclass.

CLASSES
    __builtin__.object
        TestCmd.TestCmd
            TestCommon.TestCommon
                TestSCons
    
    class TestCmd(__builtin__.object)
     |  Class TestCmd
     |  
     |  Methods defined here:
     |  
     |  __del__(self)
     |  
     |  __init__(self, description=None, program=None, interpreter=None, workdir=None, subdir=None, verbose=None, match=None, match_stdout=None, match_stderr=None, diff=None, diff_stdout=None, diff_stderr=None, combine=0, universal_newlines=1, timeout=None)
     |  
     |  __repr__(self)
     |  
     |  banner(self, s, width=None)
     |  
     |  canonicalize(self, path)
     |  
     |  chmod(self, path, mode)
     |      Changes permissions on the specified file or directory
     |      path name.
     |  
     |  cleanup(self, condition=None)
     |      Removes any temporary working directories for the specified
     |      TestCmd environment.  If the environment variable PRESERVE was
     |      set when the TestCmd environment was created, temporary working
     |      directories are not removed.  If any of the environment variables
     |      PRESERVE_PASS, PRESERVE_FAIL, or PRESERVE_NO_RESULT were set
     |      when the TestCmd environment was created, then temporary working
     |      directories are not removed if the test passed, failed, or had
     |      no result, respectively.  Temporary working directories are also
     |      preserved for conditions specified via the preserve method.
     |      
     |      Typically, this method is not called directly, but is used when
     |      the script exits to clean up temporary working directories as
     |      appropriate for the exit status.
     |  
     |  command_args(self, program=None, interpreter=None, arguments=None)
     |  
     |  description_set(self, description)
     |      Set the description of the functionality being tested.
     |  
     |  diff(self, a, b, name=None, diff_function=None, *args, **kw)
     |  
     |  diff_stderr(self, a, b, *args, **kw)
     |      Compare actual and expected file contents.
     |  
     |  diff_stdout(self, a, b, *args, **kw)
     |      Compare actual and expected file contents.
     |  
     |  dir_fixture(self, srcdir, dstdir=None)
     |      Copies the contents of the specified folder srcdir from
     |      the directory of the called  script, to the current
     |      working directory.
     |      The srcdir name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The dstdir is
     |      assumed to be under the temporary working directory, it gets
     |      created automatically, if it does not already exist.
     |  
     |  executable(self, top, execute=1)
     |      Make the specified directory tree executable (execute == 1)
     |      or not (execute == None).
     |      
     |      This method has no effect on Windows systems, which use a
     |      completely different mechanism to control file executability.
     |  
     |  fail_test(self, condition=1, function=None, skip=0, message=None)
     |      Cause the test to fail.
     |  
     |  file_fixture(self, srcfile, dstfile=None)
     |      Copies the file srcfile from the directory of
     |      the called script, to the current working directory.
     |      The dstfile is assumed to be under the temporary working
     |      directory unless it is an absolute path name.
     |      If dstfile is specified its target directory gets created
     |      automatically, if it does not already exist.
     |  
     |  finish(self, popen=None, **kw)
     |      Finishes and waits for the process being run under control of
     |      the specified popen argument, recording the exit status,
     |      standard output and error output.
     |  
     |  interpreter_set(self, interpreter)
     |      Set the program to be used to interpret the program
     |      under test as a script.
     |  
     |  match(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  match_stderr(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  match_stdout(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  no_result(self, condition=1, function=None, skip=0)
     |      Report that the test could not be run.
     |  
     |  parse_path(self, path, suppress_current=False)
     |      Return a list with the single path components of path.
     |  
     |  pass_test(self, condition=1, function=None)
     |      Cause the test to pass.
     |  
     |  preserve(self, *conditions)
     |      Arrange for the temporary working directories for the
     |      specified TestCmd environment to be preserved for one or more
     |      conditions.  If no conditions are specified, arranges for
     |      the temporary working directories to be preserved for all
     |      conditions.
     |  
     |  program_set(self, program)
     |      Set the executable program or script to be tested.
     |  
     |  read(self, file, mode='rb')
     |      Reads and returns the contents of the specified file name.
     |      The file name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The file is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.  The I/O mode for the file may
     |      be specified; it must begin with an 'r'.  The default is
     |      'rb' (binary read).
     |  
     |  readable(self, top, read=1)
     |      Make the specified directory tree readable (read == 1)
     |      or not (read == None).
     |      
     |      This method has no effect on Windows systems, which use a
     |      completely different mechanism to control file readability.
     |  
     |  rmdir(self, dir)
     |      Removes the specified dir name.
     |      The dir name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The dir is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.
     |      The dir must be empty.
     |  
     |  run(self, program=None, interpreter=None, arguments=None, chdir=None, stdin=None, universal_newlines=None, timeout=<TestCmd.null object>)
     |      Runs a test of the program or script for the test
     |      environment.  Standard output and error output are saved for
     |      future retrieval via the stdout() and stderr() methods.
     |      
     |      The specified program will have the original directory
     |      prepended unless it is enclosed in a [list].
     |  
     |  set_diff_function(self, diff=<TestCmd.null object>, stdout=<TestCmd.null object>, stderr=<TestCmd.null object>)
     |      Sets the specified diff functions.
     |  
     |  set_match_function(self, match=<TestCmd.null object>, stdout=<TestCmd.null object>, stderr=<TestCmd.null object>)
     |      Sets the specified match functions.
     |  
     |  set_timeout(self, timeout)
     |  
     |  sleep(self, seconds=1)
     |      Sleeps at least the specified number of seconds.  If no
     |      number is specified, sleeps at least the minimum number of
     |      seconds necessary to advance file time stamps on the current
     |      system.  Sleeping more seconds is all right.
     |  
     |  start(self, program=None, interpreter=None, arguments=None, universal_newlines=None, timeout=<TestCmd.null object>, **kw)
     |      Starts a program or script for the test environment.
     |      
     |      The specified program will have the original directory
     |      prepended unless it is enclosed in a [list].
     |  
     |  stderr(self, run=None)
     |      Returns the error output from the specified run number.
     |      If there is no specified run number, then returns the error
     |      output of the last run.  If the run number is less than zero,
     |      then returns the error output from that many runs back from the
     |      current run.
     |  
     |  stdout(self, run=None)
     |      Returns the standard output from the specified run number.
     |      If there is no specified run number, then returns the standard
     |      output of the last run.  If the run number is less than zero,
     |      then returns the standard output from that many runs back from
     |      the current run.
     |  
     |  subdir(self, *subdirs)
     |      Create new subdirectories under the temporary working
     |      directory, one for each argument.  An argument may be a list,
     |      in which case the list elements are concatenated using the
     |      os.path.join() method.  Subdirectories multiple levels deep
     |      must be created using a separate argument for each level:
     |      
     |              test.subdir('sub', ['sub', 'dir'], ['sub', 'dir', 'ectory'])
     |      
     |      Returns the number of subdirectories actually created.
     |  
     |  symlink(self, target, link)
     |      Creates a symlink to the specified target.
     |      The link name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The link is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name. The target is *not* assumed to be
     |      under the temporary working directory.
     |  
     |  tempdir(self, path=None)
     |      Creates a temporary directory.
     |      A unique directory name is generated if no path name is specified.
     |      The directory is created, and will be removed when the TestCmd
     |      object is destroyed.
     |  
     |  touch(self, path, mtime=None)
     |      Updates the modification time on the specified file or
     |      directory path name.  The default is to update to the
     |      current time if no explicit modification time is specified.
     |  
     |  unlink(self, file)
     |      Unlinks the specified file name.
     |      The file name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The file is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.
     |  
     |  verbose_set(self, verbose)
     |      Set the verbose level.
     |  
     |  where_is(self, file, path=None, pathext=None)
     |      Find an executable file.
     |  
     |  workdir_set(self, path)
     |      Creates a temporary working directory with the specified
     |      path name.  If the path is a null string (''), a unique
     |      directory name is created.
     |  
     |  workpath(self, *args)
     |      Returns the absolute path name to a subdirectory or file
     |      within the current temporary working directory.  Concatenates
     |      the temporary working directory name with the specified
     |      arguments using the os.path.join() method.
     |  
     |  writable(self, top, write=1)
     |      Make the specified directory tree writable (write == 1)
     |      or not (write == None).
     |  
     |  write(self, file, content, mode='wb')
     |      Writes the specified content text (second argument) to the
     |      specified file name (first argument).  The file name may be
     |      a list, in which case the elements are concatenated with the
     |      os.path.join() method.  The file is created under the temporary
     |      working directory.  Any subdirectories in the path must already
     |      exist.  The I/O mode for the file may be specified; it must
     |      begin with a 'w'.  The default is 'wb' (binary write).
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  context_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      Compare two sequences of lines; generate the delta as a context diff.
     |      
     |      Context diffs are a compact way of showing line changes and a few
     |      lines of context.  The number of context lines is set by 'n' which
     |      defaults to three.
     |      
     |      By default, the diff control lines (those with *** or ---) are
     |      created with a trailing newline.  This is helpful so that inputs
     |      created from file.readlines() result in diffs that are suitable for
     |      file.writelines() since both the inputs and outputs have trailing
     |      newlines.
     |      
     |      For inputs that do not have trailing newlines, set the lineterm
     |      argument to "" so that the output will be uniformly newline free.
     |      
     |      The context diff format normally has a header for filenames and
     |      modification times.  Any or all of these may be specified using
     |      strings for 'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
     |      The modification times are normally expressed in the ISO 8601 format.
     |      If not specified, the strings default to blanks.
     |      
     |      Example:
     |      
     |      >>> print ''.join(context_diff('one\ntwo\nthree\nfour\n'.splitlines(1),
     |      ...       'zero\none\ntree\nfour\n'.splitlines(1), 'Original', 'Current')),
     |      *** Original
     |      --- Current
     |      ***************
     |      *** 1,4 ****
     |        one
     |      ! two
     |      ! three
     |        four
     |      --- 1,4 ----
     |      + zero
     |        one
     |      ! tree
     |        four
     |  
     |  diff_re(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      A simple "diff" of two sets of lines when the expected lines
     |      are regular expressions.  This is a really dumb thing that
     |      just compares each line in turn, so it doesn't look for
     |      chunks of matching lines and the like--but at least it lets
     |      you know exactly which line first didn't compare correctl...
     |  
     |  escape(arg)
     |      escape shell special characters
     |  
     |  match_caseinsensitive(lines=None, matches=None)
     |  
     |  match_exact(lines=None, matches=None)
     |  
     |  match_re(lines=None, res=None)
     |  
     |  match_re_dotall(lines=None, res=None)
     |  
     |  simple_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      A function with the same calling signature as difflib.context_diff
     |      (diff -c) and difflib.unified_diff (diff -u) but which prints
     |      output like the simple, unadorned 'diff" command.
     |  
     |  unified_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      Compare two sequences of lines; generate the delta as a unified diff.
     |      
     |      Unified diffs are a compact way of showing line changes and a few
     |      lines of context.  The number of context lines is set by 'n' which
     |      defaults to three.
     |      
     |      By default, the diff control lines (those with ---, +++, or @@) are
     |      created with a trailing newline.  This is helpful so that inputs
     |      created from file.readlines() result in diffs that are suitable for
     |      file.writelines() since both the inputs and outputs have trailing
     |      newlines.
     |      
     |      For inputs that do not have trailing newlines, set the lineterm
     |      argument to "" so that the output will be uniformly newline free.
     |      
     |      The unidiff format normally has a header for filenames and modification
     |      times.  Any or all of these may be specified using strings for
     |      'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
     |      The modification times are normally expressed in the ISO 8601 format.
     |      
     |      Example:
     |      
     |      >>> for line in unified_diff('one two three four'.split(),
     |      ...             'zero one tree four'.split(), 'Original', 'Current',
     |      ...             '2005-01-26 23:30:50', '2010-04-02 10:20:52',
     |      ...             lineterm=''):
     |      ...     print line                  # doctest: +NORMALIZE_WHITESPACE
     |      --- Original        2005-01-26 23:30:50
     |      +++ Current         2010-04-02 10:20:52
     |      @@ -1,4 +1,4 @@
     |      +zero
     |       one
     |      -two
     |      -three
     |      +tree
     |       four
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  banner_char = '='
     |  
     |  banner_width = 80
    
    class TestCommon(TestCmd.TestCmd)
     |  Method resolution order:
     |      TestCommon
     |      TestCmd.TestCmd
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, **kw)
     |      Initialize a new TestCommon instance.  This involves just
     |      calling the base class initialization, and then changing directory
     |      to the workdir.
     |  
     |  finish(self, popen, stdout=None, stderr='', status=0, **kw)
     |      Finishes and waits for the process being run under control of
     |      the specified popen argument.  Additional arguments are similar
     |      to those of the run() method:
     |      
     |              stdout  The expected standard output from
     |                      the command.  A value of None means
     |                      don't test standard output.
     |      
     |              stderr  The expected error output from
     |                      the command.  A value of None means
     |                      don't test error output.
     |      
     |              status  The expected exit status from the
     |                      command.  A value of None means don't
     |                      test exit status.
     |  
     |  must_be_writable(self, *files)
     |      Ensures that the specified file(s) exist and are writable.
     |      An individual file can be specified as a list of directory names,
     |      in which case the pathname will be constructed by concatenating
     |      them.  Exits FAILED if any of the files does not exist or is
     |      not writable.
     |  
     |  must_contain(self, file, required, mode='rb', find=None)
     |      Ensures that the specified file contains the required text.
     |  
     |  must_contain_all(self, output, input, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains all of the specified input as a block (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_contain_all_lines(self, output, lines, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains all of the specified lines (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_contain_any_line(self, output, lines, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains at least one of the specified lines (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_contain_exactly_lines(self, output, expect, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains all of the lines in the expected string (second argument)
     |      with none left over.
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.  The function must return the index
     |      of the found line in the output, or None if the line is not found.
     |  
     |  must_contain_lines(self, lines, output, title=None, find=None)
     |  
     |  must_exist(self, *files)
     |      Ensures that the specified file(s) must exist.  An individual
     |      file be specified as a list of directory names, in which case the
     |      pathname will be constructed by concatenating them.  Exits FAILED
     |      if any of the files does not exist.
     |  
     |  must_exist_one_of(self, files)
     |      Ensures that at least one of the specified file(s) exists.
     |      The filenames can be given as a list, where each entry may be
     |      a single path string, or a tuple of folder names and the final
     |      filename that get concatenated.
     |      Supports wildcard names like 'foo-1.2.3-*.rpm'.
     |      Exits FAILED if none of the files exists.
     |  
     |  must_match(self, file, expect, mode='rb', match=None)
     |      Matches the contents of the specified file (first argument)
     |      against the expected contents (second argument).  The expected
     |      contents are a list of lines or a string which will be split
     |      on newlines.
     |  
     |  must_not_be_writable(self, *files)
     |      Ensures that the specified file(s) exist and are not writable.
     |      An individual file can be specified as a list of directory names,
     |      in which case the pathname will be constructed by concatenating
     |      them.  Exits FAILED if any of the files does not exist or is
     |      writable.
     |  
     |  must_not_contain(self, file, banned, mode='rb', find=None)
     |      Ensures that the specified file doesn't contain the banned text.
     |  
     |  must_not_contain_any_line(self, output, lines, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      does not contain any of the specified lines (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_not_contain_lines(self, lines, output, title=None, find=None)
     |  
     |  must_not_exist(self, *files)
     |      Ensures that the specified file(s) must not exist.
     |      An individual file be specified as a list of directory names, in
     |      which case the pathname will be constructed by concatenating them.
     |      Exits FAILED if any of the files exists.
     |  
     |  must_not_exist_any_of(self, files)
     |      Ensures that none of the specified file(s) exists.
     |      The filenames can be given as a list, where each entry may be
     |      a single path string, or a tuple of folder names and the final
     |      filename that get concatenated.
     |      Supports wildcard names like 'foo-1.2.3-*.rpm'.
     |      Exits FAILED if any of the files exists.
     |  
     |  options_arguments(self, options, arguments)
     |      Merges the "options" keyword argument with the arguments.
     |  
     |  run(self, options=None, arguments=None, stdout=None, stderr='', status=0, **kw)
     |      Runs the program under test, checking that the test succeeded.
     |      
     |      The parameters are the same as the base TestCmd.run() method,
     |      with the addition of:
     |      
     |              options Extra options that get appended to the beginning
     |                      of the arguments.
     |      
     |              stdout  The expected standard output from
     |                      the command.  A value of None means
     |                      don't test standard output.
     |      
     |              stderr  The expected error output from
     |                      the command.  A value of None means
     |                      don't test error output.
     |      
     |              status  The expected exit status from the
     |                      command.  A value of None means don't
     |                      test exit status.
     |      
     |      By default, this expects a successful exit (status = 0), does
     |      not test standard output (stdout = None), and expects that error
     |      output is empty (stderr = "").
     |  
     |  skip_test(self, message='Skipping test.\n')
     |      Skips a test.
     |      
     |      Proper test-skipping behavior is dependent on the external
     |      TESTCOMMON_PASS_SKIPS environment variable.  If set, we treat
     |      the skip as a PASS (exit 0), and otherwise treat it as NO RESULT.
     |      In either case, we print the specified message as an indication
     |      that the substance of the test was skipped.
     |      
     |      (This was originally added to support development under Aegis.
     |      Technically, skipping a test is a NO RESULT, but Aegis would
     |      treat that as a test failure and prevent the change from going to
     |      the next step.  Since we ddn't want to force anyone using Aegis
     |      to have to install absolutely every tool used by the tests, we
     |      would actually report to Aegis that a skipped test has PASSED
     |      so that the workflow isn't held up.)
     |  
     |  start(self, program=None, interpreter=None, options=None, arguments=None, universal_newlines=None, **kw)
     |      Starts a program or script for the test environment, handling
     |      any exceptions.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from TestCmd.TestCmd:
     |  
     |  __del__(self)
     |  
     |  __repr__(self)
     |  
     |  banner(self, s, width=None)
     |  
     |  canonicalize(self, path)
     |  
     |  chmod(self, path, mode)
     |      Changes permissions on the specified file or directory
     |      path name.
     |  
     |  cleanup(self, condition=None)
     |      Removes any temporary working directories for the specified
     |      TestCmd environment.  If the environment variable PRESERVE was
     |      set when the TestCmd environment was created, temporary working
     |      directories are not removed.  If any of the environment variables
     |      PRESERVE_PASS, PRESERVE_FAIL, or PRESERVE_NO_RESULT were set
     |      when the TestCmd environment was created, then temporary working
     |      directories are not removed if the test passed, failed, or had
     |      no result, respectively.  Temporary working directories are also
     |      preserved for conditions specified via the preserve method.
     |      
     |      Typically, this method is not called directly, but is used when
     |      the script exits to clean up temporary working directories as
     |      appropriate for the exit status.
     |  
     |  command_args(self, program=None, interpreter=None, arguments=None)
     |  
     |  description_set(self, description)
     |      Set the description of the functionality being tested.
     |  
     |  diff(self, a, b, name=None, diff_function=None, *args, **kw)
     |  
     |  diff_stderr(self, a, b, *args, **kw)
     |      Compare actual and expected file contents.
     |  
     |  diff_stdout(self, a, b, *args, **kw)
     |      Compare actual and expected file contents.
     |  
     |  dir_fixture(self, srcdir, dstdir=None)
     |      Copies the contents of the specified folder srcdir from
     |      the directory of the called  script, to the current
     |      working directory.
     |      The srcdir name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The dstdir is
     |      assumed to be under the temporary working directory, it gets
     |      created automatically, if it does not already exist.
     |  
     |  executable(self, top, execute=1)
     |      Make the specified directory tree executable (execute == 1)
     |      or not (execute == None).
     |      
     |      This method has no effect on Windows systems, which use a
     |      completely different mechanism to control file executability.
     |  
     |  fail_test(self, condition=1, function=None, skip=0, message=None)
     |      Cause the test to fail.
     |  
     |  file_fixture(self, srcfile, dstfile=None)
     |      Copies the file srcfile from the directory of
     |      the called script, to the current working directory.
     |      The dstfile is assumed to be under the temporary working
     |      directory unless it is an absolute path name.
     |      If dstfile is specified its target directory gets created
     |      automatically, if it does not already exist.
     |  
     |  interpreter_set(self, interpreter)
     |      Set the program to be used to interpret the program
     |      under test as a script.
     |  
     |  match(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  match_stderr(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  match_stdout(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  no_result(self, condition=1, function=None, skip=0)
     |      Report that the test could not be run.
     |  
     |  parse_path(self, path, suppress_current=False)
     |      Return a list with the single path components of path.
     |  
     |  pass_test(self, condition=1, function=None)
     |      Cause the test to pass.
     |  
     |  preserve(self, *conditions)
     |      Arrange for the temporary working directories for the
     |      specified TestCmd environment to be preserved for one or more
     |      conditions.  If no conditions are specified, arranges for
     |      the temporary working directories to be preserved for all
     |      conditions.
     |  
     |  program_set(self, program)
     |      Set the executable program or script to be tested.
     |  
     |  read(self, file, mode='rb')
     |      Reads and returns the contents of the specified file name.
     |      The file name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The file is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.  The I/O mode for the file may
     |      be specified; it must begin with an 'r'.  The default is
     |      'rb' (binary read).
     |  
     |  readable(self, top, read=1)
     |      Make the specified directory tree readable (read == 1)
     |      or not (read == None).
     |      
     |      This method has no effect on Windows systems, which use a
     |      completely different mechanism to control file readability.
     |  
     |  rmdir(self, dir)
     |      Removes the specified dir name.
     |      The dir name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The dir is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.
     |      The dir must be empty.
     |  
     |  set_diff_function(self, diff=<TestCmd.null object>, stdout=<TestCmd.null object>, stderr=<TestCmd.null object>)
     |      Sets the specified diff functions.
     |  
     |  set_match_function(self, match=<TestCmd.null object>, stdout=<TestCmd.null object>, stderr=<TestCmd.null object>)
     |      Sets the specified match functions.
     |  
     |  set_timeout(self, timeout)
     |  
     |  sleep(self, seconds=1)
     |      Sleeps at least the specified number of seconds.  If no
     |      number is specified, sleeps at least the minimum number of
     |      seconds necessary to advance file time stamps on the current
     |      system.  Sleeping more seconds is all right.
     |  
     |  stderr(self, run=None)
     |      Returns the error output from the specified run number.
     |      If there is no specified run number, then returns the error
     |      output of the last run.  If the run number is less than zero,
     |      then returns the error output from that many runs back from the
     |      current run.
     |  
     |  stdout(self, run=None)
     |      Returns the standard output from the specified run number.
     |      If there is no specified run number, then returns the standard
     |      output of the last run.  If the run number is less than zero,
     |      then returns the standard output from that many runs back from
     |      the current run.
     |  
     |  subdir(self, *subdirs)
     |      Create new subdirectories under the temporary working
     |      directory, one for each argument.  An argument may be a list,
     |      in which case the list elements are concatenated using the
     |      os.path.join() method.  Subdirectories multiple levels deep
     |      must be created using a separate argument for each level:
     |      
     |              test.subdir('sub', ['sub', 'dir'], ['sub', 'dir', 'ectory'])
     |      
     |      Returns the number of subdirectories actually created.
     |  
     |  symlink(self, target, link)
     |      Creates a symlink to the specified target.
     |      The link name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The link is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name. The target is *not* assumed to be
     |      under the temporary working directory.
     |  
     |  tempdir(self, path=None)
     |      Creates a temporary directory.
     |      A unique directory name is generated if no path name is specified.
     |      The directory is created, and will be removed when the TestCmd
     |      object is destroyed.
     |  
     |  touch(self, path, mtime=None)
     |      Updates the modification time on the specified file or
     |      directory path name.  The default is to update to the
     |      current time if no explicit modification time is specified.
     |  
     |  unlink(self, file)
     |      Unlinks the specified file name.
     |      The file name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The file is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.
     |  
     |  verbose_set(self, verbose)
     |      Set the verbose level.
     |  
     |  where_is(self, file, path=None, pathext=None)
     |      Find an executable file.
     |  
     |  workdir_set(self, path)
     |      Creates a temporary working directory with the specified
     |      path name.  If the path is a null string (''), a unique
     |      directory name is created.
     |  
     |  workpath(self, *args)
     |      Returns the absolute path name to a subdirectory or file
     |      within the current temporary working directory.  Concatenates
     |      the temporary working directory name with the specified
     |      arguments using the os.path.join() method.
     |  
     |  writable(self, top, write=1)
     |      Make the specified directory tree writable (write == 1)
     |      or not (write == None).
     |  
     |  write(self, file, content, mode='wb')
     |      Writes the specified content text (second argument) to the
     |      specified file name (first argument).  The file name may be
     |      a list, in which case the elements are concatenated with the
     |      os.path.join() method.  The file is created under the temporary
     |      working directory.  Any subdirectories in the path must already
     |      exist.  The I/O mode for the file may be specified; it must
     |      begin with a 'w'.  The default is 'wb' (binary write).
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from TestCmd.TestCmd:
     |  
     |  context_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      Compare two sequences of lines; generate the delta as a context diff.
     |      
     |      Context diffs are a compact way of showing line changes and a few
     |      lines of context.  The number of context lines is set by 'n' which
     |      defaults to three.
     |      
     |      By default, the diff control lines (those with *** or ---) are
     |      created with a trailing newline.  This is helpful so that inputs
     |      created from file.readlines() result in diffs that are suitable for
     |      file.writelines() since both the inputs and outputs have trailing
     |      newlines.
     |      
     |      For inputs that do not have trailing newlines, set the lineterm
     |      argument to "" so that the output will be uniformly newline free.
     |      
     |      The context diff format normally has a header for filenames and
     |      modification times.  Any or all of these may be specified using
     |      strings for 'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
     |      The modification times are normally expressed in the ISO 8601 format.
     |      If not specified, the strings default to blanks.
     |      
     |      Example:
     |      
     |      >>> print ''.join(context_diff('one\ntwo\nthree\nfour\n'.splitlines(1),
     |      ...       'zero\none\ntree\nfour\n'.splitlines(1), 'Original', 'Current')),
     |      *** Original
     |      --- Current
     |      ***************
     |      *** 1,4 ****
     |        one
     |      ! two
     |      ! three
     |        four
     |      --- 1,4 ----
     |      + zero
     |        one
     |      ! tree
     |        four
     |  
     |  diff_re(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      A simple "diff" of two sets of lines when the expected lines
     |      are regular expressions.  This is a really dumb thing that
     |      just compares each line in turn, so it doesn't look for
     |      chunks of matching lines and the like--but at least it lets
     |      you know exactly which line first didn't compare correctl...
     |  
     |  escape(arg)
     |      escape shell special characters
     |  
     |  match_caseinsensitive(lines=None, matches=None)
     |  
     |  match_exact(lines=None, matches=None)
     |  
     |  match_re(lines=None, res=None)
     |  
     |  match_re_dotall(lines=None, res=None)
     |  
     |  simple_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      A function with the same calling signature as difflib.context_diff
     |      (diff -c) and difflib.unified_diff (diff -u) but which prints
     |      output like the simple, unadorned 'diff" command.
     |  
     |  unified_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      Compare two sequences of lines; generate the delta as a unified diff.
     |      
     |      Unified diffs are a compact way of showing line changes and a few
     |      lines of context.  The number of context lines is set by 'n' which
     |      defaults to three.
     |      
     |      By default, the diff control lines (those with ---, +++, or @@) are
     |      created with a trailing newline.  This is helpful so that inputs
     |      created from file.readlines() result in diffs that are suitable for
     |      file.writelines() since both the inputs and outputs have trailing
     |      newlines.
     |      
     |      For inputs that do not have trailing newlines, set the lineterm
     |      argument to "" so that the output will be uniformly newline free.
     |      
     |      The unidiff format normally has a header for filenames and modification
     |      times.  Any or all of these may be specified using strings for
     |      'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
     |      The modification times are normally expressed in the ISO 8601 format.
     |      
     |      Example:
     |      
     |      >>> for line in unified_diff('one two three four'.split(),
     |      ...             'zero one tree four'.split(), 'Original', 'Current',
     |      ...             '2005-01-26 23:30:50', '2010-04-02 10:20:52',
     |      ...             lineterm=''):
     |      ...     print line                  # doctest: +NORMALIZE_WHITESPACE
     |      --- Original        2005-01-26 23:30:50
     |      +++ Current         2010-04-02 10:20:52
     |      @@ -1,4 +1,4 @@
     |      +zero
     |       one
     |      -two
     |      -three
     |      +tree
     |       four
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from TestCmd.TestCmd:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from TestCmd.TestCmd:
     |  
     |  banner_char = '='
     |  
     |  banner_width = 80
    
    class TestSCons(TestCommon.TestCommon)
     |  Class for testing SCons.
     |  
     |  This provides a common place for initializing SCons tests,
     |  eliminating the need to begin every test with the same repeated
     |  initializations.
     |  
     |  Method resolution order:
     |      TestSCons
     |      TestCommon.TestCommon
     |      TestCmd.TestCmd
     |      __builtin__.object
     |  
     |  Methods defined here:
     |  
     |  Environment(self, ENV=None, *args, **kw)
     |      Return a construction Environment that optionally overrides
     |      the default external environment with the specified ENV.
     |  
     |  Qt_create_SConstruct(self, place)
     |  
     |  Qt_dummy_installation(self, dir='qt')
     |  
     |  __init__(self, **kw)
     |      Initialize an SCons testing object.
     |      
     |      If they're not overridden by keyword arguments, this
     |      initializes the object with the following default values:
     |      
     |              program = 'scons' if it exists,
     |                        else 'scons.py'
     |              interpreter = 'python'
     |              match = match_exact
     |              workdir = ''
     |      
     |      The workdir value means that, by default, a temporary workspace
     |      directory is created for a TestSCons environment.  In addition,
     |      this method changes directory (chdir) to the workspace directory,
     |      so an explicit "chdir = '.'" on all of the run() method calls
     |      is not necessary.
     |  
     |  checkLogAndStdout(self, checks, results, cached, logfile, sconf_dir, sconstruct, doCheckLog=1, doCheckStdout=1)
     |  
     |  deprecated_fatal(self, warn, msg)
     |      Determines if the warning has turned into a fatal error.  If so,
     |      passes the test, as any remaining runs are now moot.
     |      
     |      This method expects a SConscript to be present that will causes
     |      the warning.  The method writes a SConstruct that calls the
     |      SConsscript and looks to see what type of result occurs.
     |      
     |      The pattern that matches the warning is returned.
     |      
     |      TODO: Actually detect that it's now an error.  We don't have any
     |      cases yet, so there's no way to test it.
     |  
     |  deprecated_warning(self, warn, msg)
     |      Verifies the expected behavior occurs for deprecation warnings.
     |      This method expects a SConscript to be present that will causes
     |      the warning.  The method writes a SConstruct and exercises various
     |      combinations of command-line options and SetOption parameters to
     |      validate that it performs correctly.
     |      
     |      The pattern that matches the warning is returned.
     |  
     |  deprecated_wrap(self, msg)
     |      Calculate the pattern that matches a deprecation warning.
     |  
     |  detect(self, var, prog=None, ENV=None, norm=None)
     |      Detect a program named 'prog' by first checking the construction
     |      variable named 'var' and finally searching the path used by
     |      SCons. If either method fails to detect the program, then false
     |      is returned, otherwise the full path to prog is returned. If
     |      prog is None, then the value of the environment variable will be
     |      used as prog.
     |  
     |  detect_tool(self, tool, prog=None, ENV=None)
     |      Given a tool (i.e., tool specification that would be passed
     |      to the "tools=" parameter of Environment()) and a program that
     |      corresponds to that tool, return true if and only if we can find
     |      that tool using Environment.Detect().
     |      
     |      By default, prog is set to the value passed into the tools parameter.
     |  
     |  diff_substr(self, expect, actual, prelen=20, postlen=40)
     |  
     |  gccFortranLibs(self)
     |      Test which gcc Fortran startup libraries are required.
     |      This should probably move into SCons itself, but is kind of hacky.
     |  
     |  get_alt_cpp_suffix(self)
     |      Many CXX tests have this same logic.
     |      They all needed to determine if the current os supports
     |      files with .C and .c as different files or not
     |      in which case they are instructed to use .cpp instead of .C
     |  
     |  get_platform_python_info(self)
     |      Returns a path to a Python executable suitable for testing on
     |      this platform and its associated include path, library path,
     |      and library name.
     |  
     |  get_python_version(self)
     |      Returns the Python version (just so everyone doesn't have to
     |      hand-code slicing the right number of characters).
     |  
     |  java_ENV(self, version=None)
     |      Initialize with a default external environment that uses a local
     |      Java SDK in preference to whatever's found in the default PATH.
     |  
     |  java_get_class_files(self, dir)
     |  
     |  java_where_includes(self, version=None)
     |      Return java include paths compiling java jni code
     |  
     |  java_where_jar(self, version=None)
     |  
     |  java_where_java(self, version=None)
     |      Return a path to the java executable.
     |  
     |  java_where_java_home(self, version=None)
     |  
     |  java_where_javac(self, version=None)
     |      Return a path to the javac compiler.
     |  
     |  java_where_javah(self, version=None)
     |  
     |  java_where_rmic(self, version=None)
     |  
     |  normalize_pdf(self, s)
     |  
     |  normalize_ps(self, s)
     |  
     |  not_up_to_date(self, arguments='.', **kw)
     |      Asserts that none of the targets listed in arguments is
     |      up to date, but does not make any assumptions on other targets.
     |      This function is most useful in conjunction with the -n option.
     |  
     |  option_not_yet_implemented(self, option, arguments=None, **kw)
     |      Verifies expected behavior for options that are not yet implemented:
     |      a warning message, and exit status 1.
     |  
     |  paths(self, patterns)
     |  
     |  python_file_line(self, file, line)
     |      Returns a Python error line for output comparisons.
     |      
     |      The exec of the traceback line gives us the correct format for
     |      this version of Python.  Before 2.5, this yielded:
     |      
     |          File "<string>", line 1, ?
     |      
     |      Python 2.5 changed this to:
     |      
     |          File "<string>", line 1, <module>
     |      
     |      We stick the requested file name and line number in the right
     |      places, abstracting out the version difference.
     |  
     |  run(self, *args, **kw)
     |      Set up SCONSFLAGS for every command so test scripts don't need
     |      to worry about unexpected warnings in their output.
     |  
     |  skip_if_not_msvc(self, check_platform=True)
     |      Check whether we are on a Windows platform and skip the
     |      test if not. This check can be omitted by setting
     |      check_platform to False.
     |      Then, for a win32 platform, additionally check
     |      whether we have a MSVC toolchain installed
     |      in the system, and skip the test if none can be
     |      found (=MinGW is the only compiler available).
     |  
     |  start(self, *args, **kw)
     |      Starts SCons in the test environment.
     |      
     |      This method exists to tell Test{Cmd,Common} that we're going to
     |      use standard input without forcing every .start() call in the
     |      individual tests to do so explicitly.
     |  
     |  up_to_date(self, arguments='.', read_str='', **kw)
     |  
     |  wait_for(self, fname, timeout=20.0, popen=None)
     |      Waits for the specified file name to exist.
     |  
     |  where_is(self, prog, path=None)
     |      Given a program, search for it in the specified external PATH,
     |      or in the actual external PATH if none is specified.
     |  
     |  wrap_stdout(self, build_str='', read_str='', error=0, cleaning=0)
     |      Wraps standard output string(s) in the normal
     |      "Reading ... done" and "Building ... done" strings
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  CF = 3
     |  
     |  CR = 1
     |  
     |  Configure_lib = 'm'
     |  
     |  NCF = 2
     |  
     |  NCR = 0
     |  
     |  javac_is_gcj = False
     |  
     |  scons_version = '2.4.2.alpha.yyyymmdd'
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from TestCommon.TestCommon:
     |  
     |  finish(self, popen, stdout=None, stderr='', status=0, **kw)
     |      Finishes and waits for the process being run under control of
     |      the specified popen argument.  Additional arguments are similar
     |      to those of the run() method:
     |      
     |              stdout  The expected standard output from
     |                      the command.  A value of None means
     |                      don't test standard output.
     |      
     |              stderr  The expected error output from
     |                      the command.  A value of None means
     |                      don't test error output.
     |      
     |              status  The expected exit status from the
     |                      command.  A value of None means don't
     |                      test exit status.
     |  
     |  must_be_writable(self, *files)
     |      Ensures that the specified file(s) exist and are writable.
     |      An individual file can be specified as a list of directory names,
     |      in which case the pathname will be constructed by concatenating
     |      them.  Exits FAILED if any of the files does not exist or is
     |      not writable.
     |  
     |  must_contain(self, file, required, mode='rb', find=None)
     |      Ensures that the specified file contains the required text.
     |  
     |  must_contain_all(self, output, input, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains all of the specified input as a block (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_contain_all_lines(self, output, lines, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains all of the specified lines (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_contain_any_line(self, output, lines, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains at least one of the specified lines (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_contain_exactly_lines(self, output, expect, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      contains all of the lines in the expected string (second argument)
     |      with none left over.
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.  The function must return the index
     |      of the found line in the output, or None if the line is not found.
     |  
     |  must_contain_lines(self, lines, output, title=None, find=None)
     |  
     |  must_exist(self, *files)
     |      Ensures that the specified file(s) must exist.  An individual
     |      file be specified as a list of directory names, in which case the
     |      pathname will be constructed by concatenating them.  Exits FAILED
     |      if any of the files does not exist.
     |  
     |  must_exist_one_of(self, files)
     |      Ensures that at least one of the specified file(s) exists.
     |      The filenames can be given as a list, where each entry may be
     |      a single path string, or a tuple of folder names and the final
     |      filename that get concatenated.
     |      Supports wildcard names like 'foo-1.2.3-*.rpm'.
     |      Exits FAILED if none of the files exists.
     |  
     |  must_match(self, file, expect, mode='rb', match=None)
     |      Matches the contents of the specified file (first argument)
     |      against the expected contents (second argument).  The expected
     |      contents are a list of lines or a string which will be split
     |      on newlines.
     |  
     |  must_not_be_writable(self, *files)
     |      Ensures that the specified file(s) exist and are not writable.
     |      An individual file can be specified as a list of directory names,
     |      in which case the pathname will be constructed by concatenating
     |      them.  Exits FAILED if any of the files does not exist or is
     |      writable.
     |  
     |  must_not_contain(self, file, banned, mode='rb', find=None)
     |      Ensures that the specified file doesn't contain the banned text.
     |  
     |  must_not_contain_any_line(self, output, lines, title=None, find=None)
     |      Ensures that the specified output string (first argument)
     |      does not contain any of the specified lines (second argument).
     |      
     |      An optional third argument can be used to describe the type
     |      of output being searched, and only shows up in failure output.
     |      
     |      An optional fourth argument can be used to supply a different
     |      function, of the form "find(line, output), to use when searching
     |      for lines in the output.
     |  
     |  must_not_contain_lines(self, lines, output, title=None, find=None)
     |  
     |  must_not_exist(self, *files)
     |      Ensures that the specified file(s) must not exist.
     |      An individual file be specified as a list of directory names, in
     |      which case the pathname will be constructed by concatenating them.
     |      Exits FAILED if any of the files exists.
     |  
     |  must_not_exist_any_of(self, files)
     |      Ensures that none of the specified file(s) exists.
     |      The filenames can be given as a list, where each entry may be
     |      a single path string, or a tuple of folder names and the final
     |      filename that get concatenated.
     |      Supports wildcard names like 'foo-1.2.3-*.rpm'.
     |      Exits FAILED if any of the files exists.
     |  
     |  options_arguments(self, options, arguments)
     |      Merges the "options" keyword argument with the arguments.
     |  
     |  skip_test(self, message='Skipping test.\n')
     |      Skips a test.
     |      
     |      Proper test-skipping behavior is dependent on the external
     |      TESTCOMMON_PASS_SKIPS environment variable.  If set, we treat
     |      the skip as a PASS (exit 0), and otherwise treat it as NO RESULT.
     |      In either case, we print the specified message as an indication
     |      that the substance of the test was skipped.
     |      
     |      (This was originally added to support development under Aegis.
     |      Technically, skipping a test is a NO RESULT, but Aegis would
     |      treat that as a test failure and prevent the change from going to
     |      the next step.  Since we ddn't want to force anyone using Aegis
     |      to have to install absolutely every tool used by the tests, we
     |      would actually report to Aegis that a skipped test has PASSED
     |      so that the workflow isn't held up.)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from TestCmd.TestCmd:
     |  
     |  __del__(self)
     |  
     |  __repr__(self)
     |  
     |  banner(self, s, width=None)
     |  
     |  canonicalize(self, path)
     |  
     |  chmod(self, path, mode)
     |      Changes permissions on the specified file or directory
     |      path name.
     |  
     |  cleanup(self, condition=None)
     |      Removes any temporary working directories for the specified
     |      TestCmd environment.  If the environment variable PRESERVE was
     |      set when the TestCmd environment was created, temporary working
     |      directories are not removed.  If any of the environment variables
     |      PRESERVE_PASS, PRESERVE_FAIL, or PRESERVE_NO_RESULT were set
     |      when the TestCmd environment was created, then temporary working
     |      directories are not removed if the test passed, failed, or had
     |      no result, respectively.  Temporary working directories are also
     |      preserved for conditions specified via the preserve method.
     |      
     |      Typically, this method is not called directly, but is used when
     |      the script exits to clean up temporary working directories as
     |      appropriate for the exit status.
     |  
     |  command_args(self, program=None, interpreter=None, arguments=None)
     |  
     |  description_set(self, description)
     |      Set the description of the functionality being tested.
     |  
     |  diff(self, a, b, name=None, diff_function=None, *args, **kw)
     |  
     |  diff_stderr(self, a, b, *args, **kw)
     |      Compare actual and expected file contents.
     |  
     |  diff_stdout(self, a, b, *args, **kw)
     |      Compare actual and expected file contents.
     |  
     |  dir_fixture(self, srcdir, dstdir=None)
     |      Copies the contents of the specified folder srcdir from
     |      the directory of the called  script, to the current
     |      working directory.
     |      The srcdir name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The dstdir is
     |      assumed to be under the temporary working directory, it gets
     |      created automatically, if it does not already exist.
     |  
     |  executable(self, top, execute=1)
     |      Make the specified directory tree executable (execute == 1)
     |      or not (execute == None).
     |      
     |      This method has no effect on Windows systems, which use a
     |      completely different mechanism to control file executability.
     |  
     |  fail_test(self, condition=1, function=None, skip=0, message=None)
     |      Cause the test to fail.
     |  
     |  file_fixture(self, srcfile, dstfile=None)
     |      Copies the file srcfile from the directory of
     |      the called script, to the current working directory.
     |      The dstfile is assumed to be under the temporary working
     |      directory unless it is an absolute path name.
     |      If dstfile is specified its target directory gets created
     |      automatically, if it does not already exist.
     |  
     |  interpreter_set(self, interpreter)
     |      Set the program to be used to interpret the program
     |      under test as a script.
     |  
     |  match(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  match_stderr(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  match_stdout(self, lines, matches)
     |      Compare actual and expected file contents.
     |  
     |  no_result(self, condition=1, function=None, skip=0)
     |      Report that the test could not be run.
     |  
     |  parse_path(self, path, suppress_current=False)
     |      Return a list with the single path components of path.
     |  
     |  pass_test(self, condition=1, function=None)
     |      Cause the test to pass.
     |  
     |  preserve(self, *conditions)
     |      Arrange for the temporary working directories for the
     |      specified TestCmd environment to be preserved for one or more
     |      conditions.  If no conditions are specified, arranges for
     |      the temporary working directories to be preserved for all
     |      conditions.
     |  
     |  program_set(self, program)
     |      Set the executable program or script to be tested.
     |  
     |  read(self, file, mode='rb')
     |      Reads and returns the contents of the specified file name.
     |      The file name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The file is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.  The I/O mode for the file may
     |      be specified; it must begin with an 'r'.  The default is
     |      'rb' (binary read).
     |  
     |  readable(self, top, read=1)
     |      Make the specified directory tree readable (read == 1)
     |      or not (read == None).
     |      
     |      This method has no effect on Windows systems, which use a
     |      completely different mechanism to control file readability.
     |  
     |  rmdir(self, dir)
     |      Removes the specified dir name.
     |      The dir name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The dir is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.
     |      The dir must be empty.
     |  
     |  set_diff_function(self, diff=<TestCmd.null object>, stdout=<TestCmd.null object>, stderr=<TestCmd.null object>)
     |      Sets the specified diff functions.
     |  
     |  set_match_function(self, match=<TestCmd.null object>, stdout=<TestCmd.null object>, stderr=<TestCmd.null object>)
     |      Sets the specified match functions.
     |  
     |  set_timeout(self, timeout)
     |  
     |  sleep(self, seconds=1)
     |      Sleeps at least the specified number of seconds.  If no
     |      number is specified, sleeps at least the minimum number of
     |      seconds necessary to advance file time stamps on the current
     |      system.  Sleeping more seconds is all right.
     |  
     |  stderr(self, run=None)
     |      Returns the error output from the specified run number.
     |      If there is no specified run number, then returns the error
     |      output of the last run.  If the run number is less than zero,
     |      then returns the error output from that many runs back from the
     |      current run.
     |  
     |  stdout(self, run=None)
     |      Returns the standard output from the specified run number.
     |      If there is no specified run number, then returns the standard
     |      output of the last run.  If the run number is less than zero,
     |      then returns the standard output from that many runs back from
     |      the current run.
     |  
     |  subdir(self, *subdirs)
     |      Create new subdirectories under the temporary working
     |      directory, one for each argument.  An argument may be a list,
     |      in which case the list elements are concatenated using the
     |      os.path.join() method.  Subdirectories multiple levels deep
     |      must be created using a separate argument for each level:
     |      
     |              test.subdir('sub', ['sub', 'dir'], ['sub', 'dir', 'ectory'])
     |      
     |      Returns the number of subdirectories actually created.
     |  
     |  symlink(self, target, link)
     |      Creates a symlink to the specified target.
     |      The link name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The link is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name. The target is *not* assumed to be
     |      under the temporary working directory.
     |  
     |  tempdir(self, path=None)
     |      Creates a temporary directory.
     |      A unique directory name is generated if no path name is specified.
     |      The directory is created, and will be removed when the TestCmd
     |      object is destroyed.
     |  
     |  touch(self, path, mtime=None)
     |      Updates the modification time on the specified file or
     |      directory path name.  The default is to update to the
     |      current time if no explicit modification time is specified.
     |  
     |  unlink(self, file)
     |      Unlinks the specified file name.
     |      The file name may be a list, in which case the elements are
     |      concatenated with the os.path.join() method.  The file is
     |      assumed to be under the temporary working directory unless it
     |      is an absolute path name.
     |  
     |  verbose_set(self, verbose)
     |      Set the verbose level.
     |  
     |  workdir_set(self, path)
     |      Creates a temporary working directory with the specified
     |      path name.  If the path is a null string (''), a unique
     |      directory name is created.
     |  
     |  workpath(self, *args)
     |      Returns the absolute path name to a subdirectory or file
     |      within the current temporary working directory.  Concatenates
     |      the temporary working directory name with the specified
     |      arguments using the os.path.join() method.
     |  
     |  writable(self, top, write=1)
     |      Make the specified directory tree writable (write == 1)
     |      or not (write == None).
     |  
     |  write(self, file, content, mode='wb')
     |      Writes the specified content text (second argument) to the
     |      specified file name (first argument).  The file name may be
     |      a list, in which case the elements are concatenated with the
     |      os.path.join() method.  The file is created under the temporary
     |      working directory.  Any subdirectories in the path must already
     |      exist.  The I/O mode for the file may be specified; it must
     |      begin with a 'w'.  The default is 'wb' (binary write).
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from TestCmd.TestCmd:
     |  
     |  context_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      Compare two sequences of lines; generate the delta as a context diff.
     |      
     |      Context diffs are a compact way of showing line changes and a few
     |      lines of context.  The number of context lines is set by 'n' which
     |      defaults to three.
     |      
     |      By default, the diff control lines (those with *** or ---) are
     |      created with a trailing newline.  This is helpful so that inputs
     |      created from file.readlines() result in diffs that are suitable for
     |      file.writelines() since both the inputs and outputs have trailing
     |      newlines.
     |      
     |      For inputs that do not have trailing newlines, set the lineterm
     |      argument to "" so that the output will be uniformly newline free.
     |      
     |      The context diff format normally has a header for filenames and
     |      modification times.  Any or all of these may be specified using
     |      strings for 'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
     |      The modification times are normally expressed in the ISO 8601 format.
     |      If not specified, the strings default to blanks.
     |      
     |      Example:
     |      
     |      >>> print ''.join(context_diff('one\ntwo\nthree\nfour\n'.splitlines(1),
     |      ...       'zero\none\ntree\nfour\n'.splitlines(1), 'Original', 'Current')),
     |      *** Original
     |      --- Current
     |      ***************
     |      *** 1,4 ****
     |        one
     |      ! two
     |      ! three
     |        four
     |      --- 1,4 ----
     |      + zero
     |        one
     |      ! tree
     |        four
     |  
     |  diff_re(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      A simple "diff" of two sets of lines when the expected lines
     |      are regular expressions.  This is a really dumb thing that
     |      just compares each line in turn, so it doesn't look for
     |      chunks of matching lines and the like--but at least it lets
     |      you know exactly which line first didn't compare correctl...
     |  
     |  escape(arg)
     |      escape shell special characters
     |  
     |  match_caseinsensitive(lines=None, matches=None)
     |  
     |  match_exact(lines=None, matches=None)
     |  
     |  match_re(lines=None, res=None)
     |  
     |  match_re_dotall(lines=None, res=None)
     |  
     |  simple_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      A function with the same calling signature as difflib.context_diff
     |      (diff -c) and difflib.unified_diff (diff -u) but which prints
     |      output like the simple, unadorned 'diff" command.
     |  
     |  unified_diff(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
     |      Compare two sequences of lines; generate the delta as a unified diff.
     |      
     |      Unified diffs are a compact way of showing line changes and a few
     |      lines of context.  The number of context lines is set by 'n' which
     |      defaults to three.
     |      
     |      By default, the diff control lines (those with ---, +++, or @@) are
     |      created with a trailing newline.  This is helpful so that inputs
     |      created from file.readlines() result in diffs that are suitable for
     |      file.writelines() since both the inputs and outputs have trailing
     |      newlines.
     |      
     |      For inputs that do not have trailing newlines, set the lineterm
     |      argument to "" so that the output will be uniformly newline free.
     |      
     |      The unidiff format normally has a header for filenames and modification
     |      times.  Any or all of these may be specified using strings for
     |      'fromfile', 'tofile', 'fromfiledate', and 'tofiledate'.
     |      The modification times are normally expressed in the ISO 8601 format.
     |      
     |      Example:
     |      
     |      >>> for line in unified_diff('one two three four'.split(),
     |      ...             'zero one tree four'.split(), 'Original', 'Current',
     |      ...             '2005-01-26 23:30:50', '2010-04-02 10:20:52',
     |      ...             lineterm=''):
     |      ...     print line                  # doctest: +NORMALIZE_WHITESPACE
     |      --- Original        2005-01-26 23:30:50
     |      +++ Current         2010-04-02 10:20:52
     |      @@ -1,4 +1,4 @@
     |      +zero
     |       one
     |      -two
     |      -three
     |      +tree
     |       four
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from TestCmd.TestCmd:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from TestCmd.TestCmd:
     |  
     |  banner_char = '='
     |  
     |  banner_width = 80

FUNCTIONS
    diff_re(a, b, fromfile='', tofile='', fromfiledate='', tofiledate='', n=3, lineterm='\n')
        A simple "diff" of two sets of lines when the expected lines
        are regular expressions.  This is a really dumb thing that
        just compares each line in turn, so it doesn't look for
        chunks of matching lines and the like--but at least it lets
        you know exactly which line first didn't compare correctl...
    
    fail_test(self=None, condition=1, function=None, skip=0, message=None)
        Cause the test to fail.
        
        By default, the fail_test() method reports that the test FAILED
        and exits with a status of 1.  If a condition argument is supplied,
        the test fails only if the condition is true.
    
    match_caseinsensitive(lines=None, matches=None)
    
    match_exact(lines=None, matches=None)
    
    match_re(lines=None, res=None)
    
    match_re_dotall(lines=None, res=None)
    
    no_result(self=None, condition=1, function=None, skip=0)
        Causes a test to exit with no valid result.
        
        By default, the no_result() method reports NO RESULT for the test
        and exits with a status of 2.  If a condition argument is supplied,
        the test fails only if the condition is true.
    
    pass_test(self=None, condition=1, function=None)
        Causes a test to pass.
        
        By default, the pass_test() method reports PASSED for the test
        and exits with a status of 0.  If a condition argument is supplied,
        the test passes only if the condition is true.

DATA
    __all__ = ['diff_re', 'fail_test', 'no_result', 'pass_test', 'match_ex...
    __revision__ = '__FILE__ __REVISION__ __DATE__ __DEVELOPER__'
    _dll = '.dylib'
    _exe = ''
    _lib = '.a'
    _obj = '.o'
    _python_ = '/usr/bin/python'
    _shobj = '.os'
    dll_ = 'lib'
    dll_prefix = 'lib'
    dll_suffix = '.dylib'
    exe_suffix = ''
    lib_ = 'lib'
    lib_prefix = 'lib'
    lib_suffix = '.a'
    machine = 'x86_64'
    obj_suffix = '.o'
    python = '/usr/bin/python'
    shobj_ = ''
    shobj_prefix = ''
    shobj_suffix = '.os'



```

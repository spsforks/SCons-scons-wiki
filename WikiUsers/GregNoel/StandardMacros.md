

# Standard Macros


## Priority List
[[!table header="no" class="mointable" data="""
**Priority list of macros to implement** |||
**Macro**  | **Assigned_to**  | **Description** 
AC_CHECK_HEADERS  | testing  | Check a list of headers and generate a HAVE_ definition for each one present 
open  |   |  
open  |   |  
open  |   |  
open  |   |  
open  |   |  
open  |   |  
open  |   |  
open  |   |  
open  |   |  
"""]]


## Triage List

The `autoconf` macros are in the table (except for the obsolete ones).  Most `automake` macros have been included, but they need to be validated. 
[[!table header="no" class="mointable" data="""
**Breakout of macros by type and implementation status** ||||
**Category**  | **Unimplemented**  | **Implemented**  | **Unneeded** 
Initialization  | AC_INIT  
 AC_CONFIG_SRCDIR  
 AM_INIT_AUTOMAKE  
 AM_ENABLE_MULTILIB  
 AC_PREREQ  
 AC_COPYRIGHT  
 AC_REVISION  
 AC_PREFIX_DEFAULT  
 AC_PREFIX_PROGRAM  
 AC_CONFIG_AUX_DIR  
  |   |  
Output  | AC_CONFIG_COMMANDS  
 AC_CONFIG_COMMANDS_PRE  
 AC_CONFIG_COMMANDS_POST  
 AC_CONFIG_FILES  
 AC_CONFIG_HEADERS  
 AC_CONFIG_LINKS  
 AC_CONFIG_SUBDIRS  
 AC_OUTPUT  
  |   |  
Variable substitution  | AC_DEFINE  
 AC_DEFINE_UNQUOTED  
 AC_SUBST  
 AC_SUBST_FILE  
 AC_ARG_VAR  
  |   |  AC_PROG_MAKE_SET  

Autoheader  | AH_VERBATIM  
 AH_TEMPLATE  
 AH_TOP  
 AH_BOTTOM  
  |   |  
Programs  |  AC_CHECK_PROG  
 AC_CHECK_PROGS  
 AC_CHECK_TOOL  
 AC_CHECK_TOOLS  
 AC_PATH_PROG  
 AC_PATH_PROGS  
 AC_PATH_TOOL  
 AC_PROG_AWK  
 AC_PROG_EGREP  
 AC_PROG_FGREP  
 AC_PROG_INSTALL  
 AC_PROG_LEX  
 AC_PROG_YACC  
 AC_PROG_RANLIB  
 AC_PROG_LN_S  
 AM_GNU_GETTEXT  
 AM_PATH_PYTHON  
 AM_PATH_LISPDIR  
 AM_PROG_LISP  
 AM_PROG_AS  
 AM_PROG_LEX  
 AM_PROG_GCJ  
  |   |  
Files  | AC_CHECK_FILE  
 AC_CHECK_FILES  
  |   |  
Libraries  | AC_CHECK_LIB  
 AC_SEARCH_LIBS  
 AM_WITH_MALLOC  
 AM_WITH_REGEX  
  |   |  
Functions  | AC_CHECK_FUNCS  
  AC_LIBOBJ  
 AC_LIBSOURCE  
  AC_LIBSOURCES  
 AC_CONFIG_LIBOBJ_DIR  
 AC_REPLACE_FUNCS  
 AC_REPLACE_FNMATCH  
 AC_FUNC_ALLOCA  
 AC_FUNC_CHOWN  
 AC_FUNC_CLOSEDIR_VOID  
 AC_FUNC_ERROR_AT_LINE  
 AC_FUNC_FNMATCH  
 AC_FUNC_FNMATCH_GNU  
 AC_FUNC_FORK  
 AC_FUNC_FSEEKO  
 AC_FUNC_GETGROUPS  
  AC_FUNC_GETLOADAVG  
 AC_FUNC_GETMNTENT  
 AC_FUNC_GETPGRP  
 AC_FUNC_LSTAT_FOLLOWS_SLASHED_SYMLINK  
 AC_FUNC_MALLOC  
 AC_FUNC_MEMCMP  
 AC_FUNC_MBRTOWC  
 AC_FUNC_MKTIME  
 AC_FUNC_MMAP  
 AC_FUNC_OBSTACK  
 AC_FUNC_REALLOC  
 AC_FUNC_SELECT_ARGTYPES  
 AC_FUNC_SETPGRP  
  AC_FUNC_SETVBUF_REVERSED  
 AC_FUNC_STAT  
 AC_FUNC_LSTAT  
 AC_FUNC_STRCOLL  
 AC_FUNC_STRERROR_R  
 AC_FUNC_STRFTIME  
 AC_FUNC_STRNLEN  
 AC_FUNC_STRTOD  
 AC_FUNC_UTIME_NULL  
 AC_FUNC_VPRINTF  
  | AC_CHECK_FUNC  
  |  
Headers  | AC_CHECK_HEADERS  
 AC_HEADER_DIRENT  
 AC_HEADER_MAJOR  
 AC_HEADER_STAT  
 AC_HEADER_STDBOOL  
 AC_HEADER_STDC  
 AC_HEADER_SYS_WAIT  
 AC_HEADER_TIME  
 AC_HEADER_TIOCGWINSZ  
  | AC_CHECK_HEADER  
  |  
Declarations  | AC_CHECK_DECL  
 AC_CHECK_DECLS  
  |   |  
Structures  | AC_CHECK_MEMBER  
 AC_CHECK_MEMBERS  
 AC_STRUCT_ST_BLKSIZE  
 AC_STRUCT_ST_BLOCKS  
 AC_STRUCT_ST_RDEV  
 AC_STRUCT_TM  
 AC_STRUCT_TIMEZONE  
  |   |  
Types  | AC_CHECK_TYPES  
 AC_TYPE_GETGROUPS  
 AC_TYPE_MBSTATE_T  
 AC_TYPE_MODE_T  
 AC_TYPE_OFF_T  
 AC_TYPE_PID_T  
 AC_TYPE_SIGNAL  
 AC_TYPE_SIZE_T  
 AC_TYPE_UID_T  
  | AC_CHECK_TYPE  
  |  
Preprocess  | AC_PROG_CPP  
 AC_PROG_CXXCPP  
  |   |  
C  | AC_PROG_CC  
 AC_PROG_CC_C_O  
 AM_PROG_CC_C_O  
 AC_C_BACKSLASH_A  
 AC_C_BIGENDIAN  
 AC_C_CONST  
 AC_C_VOLATILE  
 AC_C_INLINE  
 AC_C_CHAR_UNSIGNED  
 AC_C_LONG_DOUBLE  
 AC_C_STRINGIZE  
 AC_C_PROTOTYPES  
 AM_C_PROTOTYPES  
 AC_PROG_GCC_TRADITIONAL  
  |   |  
C++  | AC_PROG_CXX  
  |   |  
FORTRAN  | AC_PROG_F77  
 AC_PROG_F77_C_O  
 AC_F77_LIBRARY_LDFLAGS  
 AC_F77_DUMMY_MAIN  
 AC_F77_MAIN  
 AC_F77_WRAPPERS  
 AC_F77_FUNC  
  |   |  
Try run  | AC_LANG  
 AC_LANG_PUSH  
 AC_LANG_POP  
 AC_LANG_CONFTEST  
 AC_LANG_SOURCE  
 AC_LANG_PROGRAM  
 AC_LANG_CALL  
 AC_LANG_FUNC_LINK_TRY  
 AC_PREPROC_IFELSE  
 AC_EGREP_HEADERS  
 AC_EGREP_CPP  
  |  AC_COMPILE_IFELSE  
 AC_LINK_IFELSE  
 AC_RUN_IFELSE  
 |  
System  | AC_CHECK_SIZEOF  
 AC_PATH_X  
 AC_PATH_XTRA  
 AC_SYS_INTERPRETER  
 AC_SYS_LARGEFILE  
 AC_SYS_LONG_FILE_NAMES  
 AC_SYS_POSIX_TERMIOS  
  |   |  
UNIX variants  | AC_AIX  
 AC_GNU_SOURCE  
 AC_ISC_POSIX  
 AC_MINIX  
  |   |  
Cross-  
 compile  | AC_CANONICAL_BUILD  
 AC_CANONICAL_HOST  
 AC_CANONICAL_TARGET  
 AC_ARG_PROGRAM  
  |   |  
User options and help  | AC_ARG_WITH/AC_WITH  
 AC_ARG_ENABLE/AC_ENABLE  
 AC_HELP_STRING  
  |   |  
Testing (Autotest)  | AC_CONFIG_TESTDIR  
 AT_INIT  
 AT_TESTED  
 AT_SETUP  
 AT_KEYWORDS  
 AT_CLEANUP  
 AT_DATA  
 AT_CHECK  
  |   |  
Messages  | AC_MSG_NOTICE  
 AC_MSG_ERROR  
 AC_MSG_FAILURE  
 AC_MSG_WARN  
 AC_DIAGNOSE  
 AC_WARNING  
 AC_FATAL  
  | AC_MSG_CHECKING  
 AC_MSG_RESULT  
 |  
Others  | AC_CACHE_VAL  
 AC_CACHE_CHECK  
 AC_CACHE_LOAD  
 AC_CACHE_SAVE  
 AC_REQUIRE  
 AC_REQUIRE_CPP  
 AC_BEFORE  
 AM_CONDITIONAL  
  |   |  
"""]]

xx 

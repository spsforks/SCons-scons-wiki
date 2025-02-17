

# SConstruct file for Fetchmail

Ommited distributing Autotools-related stuff; other obvious missing feature is distributing whole directories -- this is still missing and may be not supported at all in favour of listing specific files.  There are also some shortcuts in Autoconf counterparts since replicating Autoconf tests is out of my project's scope. 


```python
#!python 
# -*- Python -*-

################################################################################
#### Options
####

opts = Options()
opts.Add(BoolOption('FORCE_TRIO', 'Set to 1 to force Trio', 0))

################################################################################
#### Configuration
####

env = Environment(tools=['default', 'project', 'substitute'],
                  options=opts, YACCFLAGS='-y -d')
env.Replace(AWK=env.Detect(['mawk', 'gawk', 'nawk', 'awk']))
env.Append(CPPPATH=['#', '#/libesmtp/'])

conf = env.Configure(header='config.h')

## AC_HEADER_STDC
conf.header['STDC_HEADERS'] = 1

## AC_HEADER_TIME
conf.header['HAVE_SYS_TIME_H'] = 1
conf.header['TIME_WITH_SYS_TIME'] = 1
conf.header['PID_DIR'] = "/var/run"

## AC_CHECK_HEADERS
for header in ['string.h', ## AC_HEADER_STDC
               'unistd.h', 'termios.h', 'termio.h', 'sgtty.h',
               'sys/itimer.h', 'fcntl.h', 'sys/fcntl.h', 'memory.h', 'sys/wait.h',
               'arpa/inet.h', 'arpa/nameser.h', 'netinet/in.h', 'net/socket.h',
               'sys/select.h', 'sys/socket.h', 'sys/time.h', 'langinfo.h',
               'resolv.h']:
    conf.CheckHeader(header)

### AC_TYPE_SIGNAL -> #define RETSIGTYPE
if conf.TryCompile("""
#include <sys/types.h>
#include <signal.h>

int
main ()
{
return *(signal (0, 0)) (0) == 1;
  ;
  return 0;
}
""", ".c"):
    conf.header.Definition('RETSIGTYPE', 'int', verbatim=True)
else:
    conf.header.Definition('RETSIGTYPE', 'void', verbatim=True)

### AC_CHECK_LIBS
if not conf.CheckFunc('getaddrinfo'):
    conf.CheckLib(['inet6'], 'getaddrinfo')

if not conf.CheckFunc('res_search'):
    # symbol search b0rken
    # conf.CheckLib('resolv', 'res_search', header='#include <resolv.h>')
    if conf.CheckLib('resolv'):
        conf.header['HAVE_RES_SEARCH'] = 1

### AC_CHECK_FUNCS
for func in ['tcsetattr', 'stty', 'setsid', 'geteuid', 'seteuid',
             'strerror', 'syslog', 'snprintf', 'vprintf', 'vsnprintf', 'vsyslog',
             'atexit', 'inet_aton', 'strftime', 'setrlimit', 'socketpair',
             'sigprocmask', 'sigaction', 'strdup', 'setlocale', 'getnameinfo']:
    conf.CheckFunc(func)

## AC_CHECK_FUN + AC_LIBSOURCE + AC_ADD_sth
conf.CheckFunc('MD5Init', add_libobj='md5c.c')

### AC_REPLACE_FUNCS (Like `AC_CHECK_FUNCS', but uses
### `AC_LIBOBJ(FUNCTION)' as ACTION-IF-NOT-FOUND.)
for func in ['strstr', 'strcasecmp', 'memmove', 'stpcpy',
             'strlcpy', 'strlcat', 'strsignal']:
    conf.CheckFunc(func, add_libobj=True)

NEED_TRIO = env['FORCE_TRIO']
if not ( conf.header['HAVE_VPRINTF'] and conf.header['HAVE_VSNPRINTF'] ):
    NEED_TRIO = True

env = conf.Finish()

################################################################################
#### Project
####

proj = env.Project('fetchmail', '6.4.0', 'fetchmail-devel@lists.berlios.de',
                   header='config.h', DIST_TYPE='src_tarbz2')

## DISTDOCS
proj.Distribute(Split("""
    BUGS OLDNEWS design-notes.html esrs-design-notes.html todo.html
    fetchmail-features.html README.SSL README.NTLM README.packaging
    fetchmail-FAQ.book fetchmail-FAQ.html fetchmail-SA-2005-01.txt
    fetchmail-SA-2005-02.txt fetchmail-SA-2005-03.txt"""))

proj.Distribute(
    env.Command('FAQ', ['fetchmail-FAQ.html', 'dist-tools/html2txt'],
                'AWK=$AWK $SHELL ${SOURCES[1]} ${SOURCES[0]} >$TARGET || { rm -f $TARGET ; exit 1 ; }'))
proj.Distribute(
    env.Command('FEATURES', ['fetchmail-features.html', 'dist-tools/html2txt'],
                'AWK=$AWK $SHELL ${SOURCES[1]} ${SOURCES[0]} >$TARGET || { rm -f $TARGET ; exit 1 ; }'))
proj.Distribute(
    env.Command('NOTES', ['design-notes.html', 'esrs-design-notes.html', 'dist-tools/html2txt'],
                """echo "This file contains two articles reformatted from HTML." > $TARGET \
                && echo "------------------------------------------------------" >> $TARGET \
                && echo "" >> $TARGET \
                && AWK=$AWK $SHELL ${SOURCES[2]} ${SOURCES[0]} >>$TARGET \
                && AWK=$AWK $SHELL ${SOURCES[2]} ${SOURCES[1]} >>$TARGET \
                || { rm -f $TARGET ; exit 1 ; }"""))
proj.Distribute(
    env.Command('fetchmail-man.html', ['fetchmail.man', 'dist-tools/manServer.pl'],
                """env - PATH=$PATH ${SOURCES[1]} ${SOURCES[0]} >$TARGET \
                || { rm -f $TARGET ; exit 1 ; }"""))
proj.Distribute(
    env.Command("fetchmail-FAQ.pdf", ['fetchmail-FAQ.html', 'fetchmail-FAQ.book', 'bighand.png'],
                """$AWK '/^[ \t]*<h1/ {sec++; } {if (sec < 2 || sec > 3) print $$0;}' <${SOURCES[0]} >fetchmail-FAQ-print.html
                htmldoc --logoimage ${SOURCES[2]} --batch ${SOURCES[1]}
                rm -f fetchmail-FAQ-print.html"""))

## TRIO
trio = env.Library('trio', ['trio/triostr.c', 'trio/trio.c', 'trio/trionan.c'])
trio_regression = env.Program('regression', 'trio/regression.c', LIBS=[trio, 'm'])
proj.Attach(trio, trio_regression)

if NEED_TRIO:
    env.Append(LIBS=[trio, 'm'])
    proj.Test(trio_regression)

## EXTRA_DIST
proj.Distribute(Split("""
fetchmail.spec ucs/README.svn trio/CHANGES trio/README strlcpy.3
bighand.png m4-local/ac-archive-license.txt
m4-local/ac_ma_search_package.m4 m4-local/autobuild.m4 t.smoke t.rc
dist-tools/manServer.pl dist-tools/html2txt"""))

env.Command('fetchmail.spec', 'specgen.sh',
            "$SHELL $SOURCE ${PROJECT['VERSION']} > $TARGET")

proj.Distribute(
    env.Command('TODO', ['todo.html', 'dist-tools/html2txt'],
                'AWK=$AWK $SHELL ${SOURCES[1]} ${SOURCE} >$TARGET || { rm -f $TARGET ; exit 1 ; }'))

env.Append(LIBS=env.Library('libfm.a',
                            ['xmalloc.c', 'base64.c', 'rfc822.c', 'report.c', 'rfc2047e.c',
                             'servport.c', 'smbdes.c', 'smbencrypt.c', 'smbmd4.c', 'smbutil.c',
                             'libesmtp/gethostbyname.c']))

proj.AutoInstall(env.Program('fetchmail', Split("""
    socket.c getpass.c pop3.c imap.c etrn.c odmr.c fetchmail.c env.c
    idle.c options.c daemon.c driver.c transact.c sink.c smtp.c uid.c
    mxget.c md5ify.c cram.c kerberos.c gssapi.c opie.c rpa.c
    interface.c netrc.c unmime.c conf.c checkalias.c lock.c
    rcfile_l.l rcfile_y.y
    ucs/norm_charmap.c libesmtp/getaddrinfo.c KAME/getnameinfo.c""")))
Depends('rcfile_l.o', 'rcfile_y.c')

# Checking for Python is useless
import sys
proj.AutoInstall(
    env.Command(
        'fetchmailconf', (),
        """( echo '#! /bin/sh' && echo 'exec $PYTHON $PYTHONDIR/fetchmailconf.py "$$@"' ) >$TARGET || { rm -f $TARGET ; exit 1; }""",
        PYTHON=sys.executable,
        PYTHONDIR=proj['DIR'].python),
    instal='bin', executable=True)
proj.AutoInstall('fetchmailconf.py', install='python')
proj.AutoInstall('fetchmail.man', install='man1')

lsm_name = '%s-%s.lsm' % (proj['NAME'], proj['VERSION'])
proj.Attach(
    env.Alias('lsm', env.Command(lsm_name, proj.Substitute('genlsm.sh.in'),
                                 "$SHELL $SOURCE >$TARGET")))
env.Depends(lsm_name, env.Alias('dist-fetchmail'))

proj.Test('t.smoke',
          ['t.rc',
           env.Program('rfc822.c', CFLAGS='-DMAIN', OBJPREFIX='rfc822_'),
           env.Program('unmime.c',  CFLAGS='-DSTANDALONE', OBJPREFIX='unmime_'),
           env.Program(['netrc.c', 'xmalloc.c', 'report.c'], CFLAGS='-DSTANDALONE', OBJPREFIX='netrc_'),
           env.Program('rfc2047e.c',  CFLAGS='-DTEST', OBJPREFIX='rfc2047e_'),
           env.Program('mxget.c', CFLAGS='-DSTANDALONE', OBJPREFIX='mxget_')
           ],

          environment = {
              'srcdir' : env.File('t.rc').dir,
              'LC_ALL' : 'C',
              'TZ' : 'UTC'
              })
```

****Use a level-one header for the topic and a level-two header for each comment in the topic.  The anchor before the top-level header is in case someone wishes to refer to the topic externally; it should be a valid URI identifier.****[[!toc 1]] 

<a name="target_option"></a> 
# The --target Option


## J.T. Conklin

The proposal uses --target to specify the cross development target.  This is different than the GBS which uses --build to specify the build machine, --host to build the cross target, and --target to specify the target of the tool being built.  For example, 

* `configure --build=i686-linux --host=powerpc-linux --target=arm-linux` 
would be used for a package that is built on a i686-linux machine, will ultimately run on a powerpc-linux machine, and will generate code for an arm-linux.  Outside of cross development tools, the --target option is rarely used in the GBS. 


## Greg Noel

Note that the `--build` option is unnecessary for SCons; there's no need to generate a script to be run elsewhere as build machine is the one where the code is already being run.  And I agree that `--target` is confusing the way that GNU uses it.  My concern is that using a different set of defaults than the GNU model will cause those transitioning from `configure` to be not only confused but also annoyed, and would potentially cost us a user. 

That said, I would prefer that if only one of `--target` or `--host` is specified is that both be defaulted from it; that is, if you want a cross-development tool, you <ins>_must_</ins> specify both.  Since you are the first developer with major configure-fu to be interested in the topic, do you think changing the rules would be too confusing? 

As an aside, I would still allow `--build` to be used on the command line, but I would require that it be "compatible" (for some definition of compatible) with the current machine.  It would not be generally useful, but there might be an odd case where some aspect of the machine was not determinable by polling the Python characteristics.  I can't imagine what the aspect might be, but at this point, I want to make sure I'm not excluding any possibilities. 


## J.T. Conklin

Even in the GBS, the `--build` option is rarely explicitly specified.  I will try to find a use case where it's needed to see whether the same case would apply to SCons.  The existence of _build_ as a concept is important, as we will likely need separate variables for build, host, and target (and maybe broken apart variables like build_cpu, host_os, and target_vendor like found in the GBS).  One of the more common bugs found in configure scripts are conditionals that refer to the wrong variable. 

I have to think about more about your question about the default behavior. 


## Greg Noel

It doesn't surprise me that the use of the `--build` option is rare; `autoconf` does a remarkably good job of creating a portable shell script.  It's so portable that it's common to distribute the generated `configure` script as part of the project, just in case the user doesn't have `autoconf` installed (or, more accuraely, the right macro set).  (But you already knew that, I'm sure.)  On the other hand, I can (just barely) imagine a case where you might need to generate a `configure` script with a non-standard set of macros if you were, say, planning to run it on a DOS-based platform.  (Yes, I know, `autoconf` doesn't run there; that's why I can just barely imagine it.) 

Although I agree that having it possible to refer to the build, host, and target platforms individually is important, I am not convinced that they all need to be exposed in the same Environment.  My proposal is that the IAPAT have the information for <ins>one</ins> platform (and therefore, any Environments derived from it would as well).  If you need access to both the build platform information and the host platform information, create two IAPATs.  (For generating cross-compilers, note that the target platform is usually just passed to the build, but it would be possible to create an IAPAT for the target and cherry-pick attributes, if desired.) 

That's why the default IAPAT is for the `--host` machine.  The theory is that most builds could be cross-compiled simply by specifying that machine; the major (only?) exception is when a program must be built locally in order to generate sources.  In that case, an IAPAT (and derived Environments) for the local machine must be used; in all other cases, cross-compilation Just Works. 

This puts me at odds with the vs_revamp folks, who want to create a complete set of build and host variables in an Environment; my attempts to disuade them were for naught.  I couldn't seem to convince them that you don't need to know what the build machine is; either the cross-compiler runs on it (in which case the Environment variables are already set up correctly to do the build) or it doesn't (in which case the problem isn't in the SConscript).  In other words, I'm not aware of a use case where knowledge of the build platform is needed to select or run the cross-compiler.  Are you?  (Knowledge that the build is a cross-compile, yes, in order to select the right name for the cross-compiler and maybe some options, but not detailed knowledge of what the build platform is.) 

<a name="feature_test_use_cases"></a> <a name="interrogate_test_results"></a> 
# Feature Test Use Cases (1)

Original topic separated into three sections. 


## J.T. Conklin

Greg asked me to note some of the use cases / problem spots encountered with SCons' current configuration mechanism that we encountered when converting XORP from the GBS to SCons. 

One major problem is that the feature test results are not kept by the configuration infrastructure, so the user's SConscript must introduce variables in their SConscript to track these themselves.  So a test for a header file <quux.h> that depends on <foo.h> and <bar.h>, but those latter headers may or may not be present on a given system, ends up looking like this: 

* ```txt
have_foo_h = conf.CheckHeader('foo.h')
have_bar_h = conf.CheckHeader('bar.h')

prereq = []
if have_foo_h:
    prereq.append('foo.h')
if have_bar_h:
    prereq.append('bar.h')
have_quux_h = conf.CheckHeader(prereq + [ 'quux.h' ])
```

## Greg Noel

I believe this issue is already handled by the design I'm proposing.  Each "header" is a separate object (and looks enough like a File that it can be used as a dependency, if desired) and the "contents" of the header can be introspected.  Thus, the value of a boolean variable can be determined mearly by referring to it:   
`    hdr.Declare('HAVE_FOO_H', 'Can use functions in foo')`   
`    hdr.vars.HAVE_FOO_H = iapat.CheckHeader('foo.h')`   
`    if hdr.vars.HAVE_FOO_H: ...`   
If the usage is common enough (and there are no technical considerations against it), it's possible that the header namespace can be incorporated directly in the header object, so it would be `hdr.HAVE_FOO_H` instead of the way in the example. 

Note that the intent here is that `CheckHeader()`, _et.al._, return a _delayed-action object_ rather than an actual truth value.  Using the object in a header would naturally form a DAG that the standard evaluation mechanisms would optimize, only evaluating a given condition once, and <ins>_not_</ins> evaluating it in subsequent runs if there's no need.  In this case, evaluating the object in a bool context would cause the test to be performed, if it hadn't already. 

<a name="reusing_context"></a> 
# Feature Test Use Cases (2)


## J.T. Conklin

The GBS maintains the state of previous tests and makes them available, so the above would look something like: 

* ```txt
AC_CHECK_HEADERS(foo.h bar.h)
AC_CHECK_HEADERS(quux.h, [], [], [
#ifdef HAVE_FOO_H
#include <foo.h>
#endif
#ifdef HAVE_BAR_H
#include <bar.h>
#endif
])
```

## Greg Noel

This is reusing the context determined by prior tests in subsequent tests.  As I understand it, a `configure` script does this by accumulating a set of `-D` and `-U` parameters that are used in the command line of the test compiles.  (If a `config.h` is not generated, these options are propagated into `CFLAGS` so the build will use them as well.) 

Yes, I'd planned to do this, although I have to admit I hadn't given it much thought.  Maybe the simplest way would be for `CheckHeader()` to be a method of the header object, so to have any previously-evaluated header values in scope, you'd use something like this:   
`    hdr.vars.HAVE_QUUX_H = hdr.CheckHeader('quux.h')`   
or maybe just like this (assuming standard naming conventions):   
`    hdr.CheckHeader('quux.h')`   
This method would generate a command line that included all of the currently-defined values and automatically add the variable for this header.  There's a tension here, as things like libraries need to be accumulated at the `IAPAT` level (_e.g._, the `LIBS` variable); these are some things that will need to be worked out. 

The other part of this point is the ability to specify a different prefix for the test function (or maybe a whole new body?).  I have to admit I thought that was already part of `CheckHeader()`, _et.al._, but a quick peek at the man page disabused me of that idea.  Yes, it's something that should be possible, maybe with keyword arguments to allow the specification of the prefix, body, and suffix independently:   
`    hdr.CheckHeader('quux.h', prefix = '''`   
`        #ifdef HAVE_FOO_H`   
`        #include <foo.h>`   
`        #endif`   
`        #ifdef HAVE_BAR_H`   
`        #include <bar.h>`   
`        #endif`   
`     '''`   
You'd probably need some rule about stripping leading blanks (similar to what is done for Python doc strings). 

(I'm glad you mentioned this last point; it could have easily fallen through the cracks.) 

<a name="devault_include_prefix"></a> 
# Feature Test Use Cases (3)


## J.T. Conklin

If checking for <foo.h> and <bar.h> will be common for all tests, you can even set the default boilerplate "includes" which simplifies things even further. 

* ```txt
AC_DEFAULT_INCLUDES([
#ifdef HAVE_FOO_H
#include <foo.h>
#endif
#ifdef HAVE_BAR_H
#include <bar.h>
#endif
])

AC_CHECK_HEADERS(foo.h bar.h quux.h)
```
This starts showing clear benefits once there is more than one feature test that uses the same boilerplate. 


## Greg Noel

This issue is the ability to specify the default prefix/body/suffix "globally" (probably per-header).  I can see reason for it, but I also see that it could cause failures a long way from the cause.  I suspect `configure` does it that way because it's irritatingly hard to create and use variables in M4, so maybe the solution for SCons is to use Python variables and simply always specify the prefix/body/suffix:   
`    hdrPrefix = '''`   
`        #ifdef HAVE_FOO_H`   
`        #include <foo.h>`   
`        #endif`   
`        #ifdef HAVE_BAR_H`   
`        #include <bar.h>`   
`        #endif`   
`    '''`   
`    hdr.CheckHeader('foo.h', prefix=hdrPrefix)`   
`    hdr.CheckHeader('bar.h', prefix=hdrPrefix)`   
`    hdr.CheckHeader('quux.h', prefix=hdrPrefix)` 

I'm not wedded to this position and can certainly see both sides, so this point needs more discussion. 

<a name="typedefs"></a> 
# Feature Test Use Cases (?)


## Greg Noel

In your message to the mailing lists, you said something to the effect that typedefs couldn't be used by this sort of machinery.  I didn't understand that point; could you clarify? 

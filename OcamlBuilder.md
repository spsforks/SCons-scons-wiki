# O'Caml Builder

[O'Caml](http://www.ocaml.org/) is statically-typed mixed paradigm programming language. Its toolchain functions somewhat differently from that of [gcc](http://gcc.gnu.org/), and it's currently unsupported by [SCons](http://www.scons.org/). Since I'd like to use [SCons](http://www.scons.org/) to build an [O'Caml](http://www.ocaml.org/) project, I'm adding the necessary code.

_Please note_ that I'm a novice when it comes to SCons, so if you can improve something on this page, please do!

Russel Winder has created a Bazaar branch of a SCons OCaml tool based on this code.  It can be found at [https://bitbucket.org/russel/scons_ocaml](https://bitbucket.org/russel/scons_ocaml)


## Tools

Let's have a closer look at the tools provided by the [O'Caml](http://www.ocaml.org/) distribution:

Tool           | Description
--------------:|:----------------------------------------------------------------
**ocaml**      | a interactive bytecode interpreter
**ocamlc**     | a bytecode compiler
**ocamlopt**   | a native code compiler
**ocamlfind**  | an environment querying tool
**ocamldep**   | a utility for determining build dependencies
**ocamldoc**   | a utility for generating documentation embedded in source code
**ocamlmktop** | Building custom toplevel systems
**ocamlyacc**  | Ocaml Yacc
**ocamllex**   | Ocaml Lex
**ocamlmklib** | generate libraries with mixed C / Caml code


## Extensions

Extension | Description
---------:|:---------------------------
**.ml**   | a source file
**.mli**  | a module interface file
**.cmi**  | a compiled interface
**.cmo**  | a bytecode compiled object
**.cma**  | a bytecode library
**.cmx**  | a native compiled object
**.cmxa** | a native library
**.mll**  | Ocaml Lex file
**.mly**  | Ocaml Yacc file

**ocamlc** generates **.cmi** files from **.mli** files, and **.cmo** files from **.ml** files

**ocamlopt** generates **.cmi** files from **.mli** files and **.cmx** and **.o** files from **.ml** files

## Scanners

O'Caml modules are opened using the syntax:

`open ModuleName`

_The above is O’Caml’s equivalent to Python’s `from ModuleName import *`. The scanner below won’t find dependencies on modules that aren’t `open`’ed, such as just using the module name. For instance, to use the `map` function from the `List` module, you just say `List.map`, and you don’t need to mention `List` anywhere else. You’ll need to use the `ocamldep` command to get the dependencies, in general._

Here's a scanner:


```python
#!python
# use re.MULTILINE flag, so '^' matches at the beginning of the
# string and at the beginning of each line, i.e. after each newline.
# Matching of '$' is similary affected.
open_re = re.compile('^open\\s+(\\S+)$', re.MULTILINE)
def scan_ml_for_deps(node):
  contents = node.get_contents()
  found = open_re.findall(contents)
  return map(str.lower, found)
# Bytecode
def mlfile_scan_bytecode(node, env, path):
  found = scan_ml_for_deps(node)
  bytecode_objects = map(lambda x: x + '.cmo', found)
  return bytecode_objects
mlscan_bytecode = Scanner(function = mlfile_scan_bytecode, skeys = ['.ml'])
```

## Ocaml Tool

This tool provides four builders:

* OcamlObject
* OcamlLibrary
* OcamlProgram
* OcamlPack

which works like Object, Library and Program. You can customize command line options and choose between a bytecode executable, a native one or a toplevel (interactive loop).

OcamlPack is used for packing several object into one (see option -pack of ocamlc).

Ocaml Tool file:


```python
#!python
# Ocaml Tool
# version: 0.2 (12/30/2005)
#
# TODO:
# - testing
# - make it portable (currently only tested on Unix)
# - Lex and Yacc builders
import os
def read_command(cmd):
        """
        Execute the command cmd and return output
        """
        return os.popen(cmd).readlines()
def when_code(env, bytecode, native, toplevel=None):
        """
        Return value depending on output code kind wanted
        """
        if toplevel == None:
                toplevel = bytecode
        if env['OCAML_CODE'] == 'bytecode':
                r = bytecode
        elif env['OCAML_CODE'] == 'native':
                r = native
        elif env['OCAML_CODE'] == 'toplevel':
                r = toplevel
        else:
                print "$OCAML_CODE must be either 'toplevel', 'bytecode' or 'native'"
                env.Exit(1)
        return r
def obj_suffix(env):
        return when_code(env, '.cmo', '.cmx')
def lib_suffix(env):
        return when_code(env, '.cma', '.cmxa')
def set_suffix(f, suffix):
        b, e = os.path.splitext(str(f))
        return b+suffix
def obj_of_src(f, env):
        return set_suffix(f, obj_suffix(env))
def iface_of_src(f):
        return set_suffix(f, '.cmi')
def comp(env):
        """
        Choose a compiler depending on environment variables
        """
        return when_code(env, '$OCAMLC', '$OCAMLOPT', '$OCAMLMKTOP')
def flags(env, t=''):
        """
        Generate flags depending on environment variables
        """
        s = when_code(env, '$OCAMLC_FLAGS', '$OCAMLOPT_FLAGS', '$OCAMLMKTOP_FLAGS')
        if env['OCAML_DEBUG']:
                s += when_code(env, ' -g', '')
        if env['OCAML_PROFILE']:
                s += when_code(env, '', ' -p')
        if env['OCAML_PP']:
                s += ' -pp %s' % env['OCAML_PP']
        if t == 'lib':
                s += ' -a'
        elif t == 'obj':
                s += ' -c'
        elif t == 'pack':
                s += ' -pack'
        return s
def is_installed(exe):
        """
        Return True if an executable is found in path
        """
        path = os.environ['PATH'].split(':')
        for p in path:
                if os.path.exists( os.path.join(p, exe) ):
                        return True
        return False
def norm_suffix(f, suffix):
        """
        Add a suffix if not present
        """
        p = str(f)
        e = p[-len(suffix):]
        if e != suffix:
                p = p + suffix
        return p
def norm_suffix_list(files, suffix):
        return map(lambda x: norm_suffix(x, suffix), files)
def find_packages(env):
        """
        Use ocamlfind to retrieve libraries paths from package names
        """
        packs = env.Split(env['OCAML_PACKS'])
        if not is_installed(env['OCAMLFIND']):
                if len(packs):
                        print "Warning: ocamlfind not found, ignoring ocaml packages"
                return ""
        s = "%s query %%s -separator ' ' %s" % (
                env['OCAMLFIND'], " ".join( packs)
        )
        i = read_command(s % '-i-format')
        l = read_command(s % '-l-format')
        code = when_code(env, 'byte', 'native')
        a = read_command(s % '-predicates %s -a-format' % code)
        r = " %s %s %s " % ( l[0][:-1], i[0][:-1], a[0][:-1] )
        return r
def cleaner(files, env, lib=False):
        files = map(str, files)
        r = []
        for f in files:
                r.append(obj_of_src(f, env))
                r.append(iface_of_src(f))
                if env['OCAML_CODE'] == 'native':
                        r.append(set_suffix(f, '.o'))
                        if lib:
                                r.append(set_suffix(f, '.a'))
        return r
def scanner(node, env, path):
        objs = norm_suffix_list(env['OCAML_OBJS'], obj_suffix(env))
        libs = norm_suffix_list(env['OCAML_LIBS'], lib_suffix(env))
        return libs+objs
prog_scanner = lib_scanner = obj_scanner = pack_scanner = scanner
def lib_emitter(target, source, env):
        t = norm_suffix(str(target[0]), lib_suffix(env))
        env.Clean(t, cleaner(source, env, lib=True))
        return (t, source)
def obj_emitter(target, source, env):
        t = norm_suffix(str(target[0]), obj_suffix(env))
        env.Clean(t, cleaner(source+[t], env))
        return (t, source)
def pack_emitter(target, source, env):
        t = norm_suffix(str(target[0]), obj_suffix(env))
        s = norm_suffix_list(source, obj_suffix(env))
        env.Clean(t, cleaner(source+[t], env))
        return (t, source)
def prog_emitter(target, source, env):
        env.Clean(target, cleaner(source, env))
        return (target, source)
def command_gen(source, target, env, comp, flags):
        """
        Generate command
        """
        target = str(target[0])
        objs = norm_suffix_list(env['OCAML_OBJS'], obj_suffix(env))
        objs = " ".join( objs )
        libs = norm_suffix_list(env['OCAML_LIBS'], lib_suffix(env))
        libs = " ".join( libs )
        inc = map(lambda x:'-I '+x, env['OCAML_PATH'])
        inc = " ".join(inc) + find_packages(env)
        s = ("%s %s -o %s %s %s %s $SOURCES" %
                        (comp, flags, target, inc, libs, objs)
        )
        return s
def obj_gen(source, target, env, for_signature):
        return command_gen( source, target, env, comp(env), flags(env, 'obj'))
def pack_gen(source, target, env, for_signature):
        return command_gen(source, target, env, comp(env), flags(env, 'pack'))
def lib_gen(source, target, env, for_signature):
        return command_gen( source, target, env, comp(env), flags(env, 'lib'))
def prog_gen(source, target, env, for_signature):
        return command_gen(source, target, env, comp(env), flags(env))
def generate(env):
        """
        Add Builders and construction variables for Ocaml to an Environment.
        """
        prog_scan = env.Scanner(prog_scanner)
        lib_scan = env.Scanner(lib_scanner)
        obj_scan = env.Scanner(obj_scanner)
        pack_scan = env.Scanner(pack_scanner)
        env.Append(BUILDERS = {
                'OcamlObject': env.Builder(
                        generator=obj_gen,
                        emitter=obj_emitter,
                        source_scanner=obj_scan
                ),
                # Pack several object into one object file
                'OcamlPack': env.Builder(
                        generator=pack_gen,
                        emitter=pack_emitter,
                        source_scanner=pack_scan
                ),
                'OcamlLibrary': env.Builder(
                        generator=lib_gen,
                        emitter=lib_emitter,
                        source_scanner=lib_scan
                ),
                'OcamlProgram': env.Builder(
                        generator=prog_gen,
                        emitter=prog_emitter,
                        source_scanner=prog_scan
                )
        })
        env.AppendUnique(
                OCAMLC='ocamlc',
                OCAMLOPT='ocamlopt',
                OCAMLMKTOP='ocamlmktop',
                OCAMLFIND='ocamlfind',
                #OCAMLDEP='ocamldep',           # not used
                OCAML_PP='',                    # not needed by default
                OCAML_DEBUG=0,
                OCAML_PROFILE=0,
                OCAMLC_FLAGS='',
                OCAMLOPT_FLAGS='',
                OCAMLMKTOP_FLAGS='',
                OCAML_LIBS=[],
                OCAML_OBJS=[],
                OCAML_PACKS=[],
                OCAML_PATH=[],
                OCAML_CODE=''                   # bytecode, toplevel or native
        )
def exists(env):
        return env.Detect('ocaml')
```


# Example

There are three files: lib.ml, object.ml and prog.ml, we want to build the executable _prog_.

The dependencies are:

* prog: object.cmx lib.cmxa prog.ml
* object.cmx: object.ml lib.cmxa
* lib.cmxa: lib.ml

```txt
(* lib.ml *)
print_endline "lib.ml"
```

```txt
(* object.ml *)
open Lib;;
print_endline "object.ml"
```

```txt
(* prog.ml *)
open Graph.Builder;;
open Object;;
print_endline "hello ocaml world !";;
```

The SConstruct file:


```python
#!python
# SConstruct
import ocaml
env = Environment(
        OCAML_PACKS="ocamlgraph",
        OCAML_CODE='native',       # could be 'bytecode'
        OCAML_DEBUG=0,
        OCAML_PROFILE=0
)

env.Tool('ocaml', '.')
o = env.OcamlObject('object', 'object.ml')
l = env.OcamlLibrary('lib', 'lib.ml')
env.OcamlProgram('prog', 'prog.ml', OCAML_LIBS=l, OCAML_OBJS=o)
```

This is the building process:


```
$ ls
lib.ml  object.ml  ocaml.py  ocaml.pyc  prog.ml  SConstruct
$ scons prog
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
ocamlopt -a -o lib.cmxa -ccopt -L/usr/lib/ocaml/3.08.3/ocamlgraph -I /usr/lib/ocaml/3.08.3/ocamlgraph lib.ml
ocamlopt -c -o object.cmx -ccopt -L/usr/lib/ocaml/3.08.3/ocamlgraph -I /usr/lib/ocaml/3.08.3/ocamlgraph object.ml
ocamlopt -o prog -ccopt -L/usr/lib/ocaml/3.08.3/ocamlgraph -I /usr/lib/ocaml/3.08.3/ocamlgraph lib.cmxa object.cmx prog.ml
scons: done building targets.

$ ls
lib.a    lib.cmxa  object.cmi  object.o   prog      prog.ml
lib.cmi  lib.ml    object.cmx  ocaml.py   prog.cmi  prog.o
lib.cmx  lib.o     object.ml   ocaml.pyc  prog.cmx  SConstruct

$ scons -c
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Cleaning targets ...
Removed lib.cmxa
Removed lib.cmx
Removed lib.cmi
Removed lib.o
Removed lib.a
Removed object.cmx
Removed object.cmi
Removed object.o
Removed prog
Removed prog.cmx
Removed prog.cmi
Removed prog.o
scons: done cleaning targets.
$ ./prog
lib.ml
object.ml
hello ocaml world !
```


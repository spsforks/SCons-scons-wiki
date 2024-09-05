# Introduction

This aims to demonstrate basic usage of a cluster management software
from within SCons.  It provides guidance on how to structure your
sources and targets so that SCons natively understands the dependency
tree and can run jobs through a cluster management software like
[slurm](https://slurm.schedmd.com/documentation.html) or Grid Engine.
An example would be using SCons to drive a numerical experiment where
you need to build some executable, run the executable under a wide
variety of inputs, and then generate figures or tables from the results.

# Assumptions

This recipe makes the following assumptions:

1.  You are already familiar with SCons and the usage of
    [Command](https://scons.org/doc/production/HTML/scons-user.html#chap-builders-commands)
2.  You are familiar with the cluster management tool you are using and,
    in particular, understand how to dispatch jobs
3.  You have build steps that would benefit from running on a cluster

This recipe uses slurm, but the principles should be applicable to any
other cluster management tool.

# Preliminary Steps

The first step is to ensure all of your source and target names are
deterministic.  It is common for cluster management tools to create
files such as `<some deterministic tag>-<incrementing job id>.out` where
the first tag is easy to predict, but the incrementing job id is only
know _after_ a job is submitted to the cluster.  This does not work well
with SCons' dependency tracker.  Instead, you should make liberal use of
your cluster management tool's redirection flags to rename the file.
This will ensure SCons is able to determine when a dependency is out of
date and relaunch jobs accordingly.

# Setting up the Build

Let's take the following steps as the high-level description of what the
build needs to accomplish:

1.  Run some task locally on a single host
2.  Run a long running job on a single host of the cluster
3.  Distribute many jobs across an arbitrary number of hosts on the
    cluster

Each step is described in the following sections.  The full working
examples are provided at the end of this recipe.

## Running a Job Locally

Running a job on the local host uses the standard SCons utilities to
define a target.  This could be from a Builder, Command, AddMethod, or
any other means to create the target from the sources.

```python
table = env.Command("example-table.txt", "generate-table.py",
                    action="python $SOURCE -o $TARGET $N",
                    varlist=("N",), N=N)
```

## Running a Single Job

The next step is to send a single job to the cluster.  In principle,
this would be a long running or, perhaps, a job that needs additional
resources available from a cluster host.  The key detail is to use the
single job submission command (`srun` for slurm, `qrsh` or `qlogin` for
Grid Engine, etc.).

```python
stem = File("table")
tables = env.Command([f"{stem.name}.{_:05d}.txt" for _ in range(N)],
                     ["split-tables.py" + table,
                     action="srun python ${SOURCES[0]} -s $stem",
                     varlist=("stem",), stem=stem)
```

Notice a few key details in this recipe.  First, the file names are
deterministic and are passed to `env.Command`.  This is critical to
allow SCons to know what file will be generated so it can track any
downstream dependencies and what potentially needs to be cleaned.
Second, the stem of the generated files is declared as a `File` so it is
available as the stem of the targets and to get the correct path when
variable substitution occurs for the action string.

## Running Multiple Jobs

The last step is distributing a collection of jobs to the cluster.  This
is primarily targeting array jobs where each gets the same job
submission but some logic handles the adjustments based on the job's
specific id in the array.

```python
action = ["sbatch", "--wait", f"--array=0-{N-1}", "--output=/dev/null",
          f"--wrap='python ${{SOURCES[0]}} {stem.name}.`printf %05d $$SLURM_ARRAY_TASK_ID`.txt'"
          ]
pngs = env.Command([str(Path(_.name).with_suffix(".png)) for _ in tables],
                   ["imshow.py"] + tables, action=" ".join(action))
```

Notice a few key details in this recipe.  First, as before, the targets
have predictable names that are passed to SCons.  Second, the `--wait`
flag tells slurm to wait for all of the jobs to complete before
returning.  This allows SCons to pause and wait for all of the targets
to be generated (or a failure) before it tries to build any
dependencies.  Third, the output is specifically redirected to
`/dev/null` to prevent the creation of unpredictable files.  If you want
outputs from the jobs, explicitly log them to a predictable file name.

Also note the use of `--wrap` in this action.  In this context, it tells
`sbatch` to wrap it's argument in a simple shell shell script for
submission.  This allows the command to gain access to the jobs task id
via `$SLURM_ARRAY_TASK_ID`.  Alternatively, you could provide a script
that handles obtaining the task id and running the
appropriate job.  The key point is each task in the array uses the same
command line and arguments.

# Full Examples

The following are the full files used in the above snippets demonstrating full use.

## SConstruct

```python
#!/usr/bin/env python

import os
from pathlib import Path

env = Environment(ENV=os.environ)

N = 100
"""A nominal size we will need multiple times"""

# Do the big long preprocessing step that has to be done locally before
# we can do other work.
table = env.Command("example-table.txt", "generate-table.py",
                    action="python $SOURCE -o $TARGET $N",
                    varlist=("N",), N=N,
                    )

# Now run some potentially long running task that depends on the
# previous step, but must be run on a single host.  This can be
# dispatched using srun.
stem = File("table")
tables = env.Command([f"{stem.name}.{_:05d}.txt" for _ in range(N)],
                     ["split-tables.py"] + table,
                     action="srun python ${SOURCES[0]} -s $stem ${SOURCES[1]}",
                     varlist=("stem",), stem=stem,
                     )

# Now we do something with our results from above.  This is the
# embarrassingly parallel portion that can be distributed across the
# hosts using sbatch.  Note, this still requires the user to know a sane
# set of flags to sbatch to get the array jobs right.  This includes
# using `--wrap` to gain access to `$SLURM_ARRAY_TASK_ID` across the
# jobs.  The logic to grab the task ID could potentially be in the
# script submitted to `sbatch` instead.
action = ["sbatch", "--wait", f"--array=0-{N-1}", "--output=/dev/null",
          "--wrap='python ${{SOURCES[0]}} {stem.name}.`printf %05d $$SLURM_ARRAY_TASK_ID`.txt'",
          ]
pngs = env.Command([str(Path(_.name).with_suffix(".png")) for _ in tables],
                   ["imshow.py"] + tables, action=" ".join(action)
                   )
```

## generate-tables.py

```python
#!/usr/bin/env python
#
#SBATCH -o /dev/null

import argparse

import numpy

parser = argparse.ArgumentParser(description="""
Generate a table of values that can be used to demonstrate the
processing pipeline.  This generates N tables with y rows and x columns
with a random variable in the range [vmin, vmax) for the colormap.  The
tables will need to be split into individual tables by a later
processing stage.
""")
parser.add_argument("N", type=int, help="the number of tables to generate")
parser.add_argument("seed", nargs="?", type=int, default=42,
                    help="the seed for the random number generator")
parser.add_argument("-x", type=int, default=32,
                    help="the width (columns) of each table: %(default)s")
parser.add_argument("-y", type=int, default=16,
                    help="the height (rows) of each table: %(default)s")
parser.add_argument("-m", "--vmin", type=float, default=0.0,
                    help="the minimum value: %(default)s")
parser.add_argument("-M", "--vmax", type=float, default=1.0,
                    help="the maximum value: %(default)s")
parser.add_argument("-o", "--output", type=argparse.FileType("w"),
                    default="-", help="the output file")
args = parser.parse_args()

xx, yy = numpy.meshgrid(numpy.arange(1, args.x + 1),
                        numpy.arange(1, args.y + 1),
                        indexing="ij")

rng = numpy.random.default_rng(seed=args.seed)
zz = rng.random(numpy.prod(xx.shape) * args.N)

tt = numpy.hstack([numpy.ones(xx.flatten().shape) * _
                   for _ in range(args.N)])

numpy.savetxt(args.output, numpy.vstack((tt.flatten(),
                                         numpy.tile(xx.flatten(), args.N),
                                         numpy.tile(yy.flatten(), args.N),
                                         zz.flatten())).T)
```

## split-tables.py

```python
#!/usrbin/env python
#
#SBATCH -o /dev/null

import argparse

import numpy

parser = argparse.ArgumentParser(description="""
Generate a single table for easier parsing later.  This is a stand in
for files that could be generated by a process on a single host that
generates multiple outputs.
""")
parser.add_argument("table", help="the full input table")
parser.add_argument("-s", "--stem", default="table", help="output stem")
args = parser.parse_args()

table = numpy.loadtxt(args.table)
for count, frame in enumerate(numpy.unique(table[:, 0])):
    with open(f"{args.stem}.{count:05d}.txt", "w") as _:
        print(table[:, 3].min(), table[:, 3].max(), numpy.nan, numpy.nan,
              file=_)
        numpy.savetxt(_, table[table[:, 0] == frame])
```

## imshow.py

```python
#!/usr/bin/env python
#

import argparse
import pathlib

import numpy

from matplotlib import pyplot

parser = argparse.ArgumentParser(description="""
Generate an image plot of a table.
""")
parser.add_argument("table", help="the individual table to plot")
parser.add_argument("-s", "--show", action="store_true",
                    help="show the figure instead of saving")
args = parser.parse_args()

table = numpy.loadtxt(args.table)

fig, axs = pyplot.subplots(1, 1, layout="constrained")

img = axs.imshow(table[1:, 3].reshape((len(numpy.unique(table[1:, 2])),
                                       len(numpy.unique(table[1:, 1])),
                                       )),
                 vmin=table[0, 0], vmax=table[0, 1])
cbr = fig.colorbar(img, ax=axs)

axs.set_xlabel("$x$")
axs.set_ylabel("$y$")
cbr.set_label("$z$")

if args.show:
    pyplot.show()
else:
    print(args.table)
    fig.savefig(pathlib.Path(args.table).with_suffix(".png"))
```

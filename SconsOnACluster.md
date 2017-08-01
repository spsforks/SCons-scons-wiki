# Using SCons on a cluster of parallel machines #
Usually machines like this are used in batch mode, where a large job is submitted and executed some time later.
To make your software work, all the machines need to be able to see a shared file system etc.
There are several pieces of software for doing this. One of them is [slurm](https://slurm.schedmd.com/).
SCons can be made to execute a job on a cluster by using the slurm command srun. This allocates the command to a free CPU in the cluster and runs it, and then returns control to scons. To make this work with scons all that is needed is to prefix the action you would normally run in the scons builder with "srun -n1".# SCons on a cluster #
SCons can be useful for controlling high performance computing workflows on a cluster.
# slurm #
Slurm is a tool for managing computation jobs on a cluster of high performance computers.
Usually slurm is used to submit jobs in batch mode.
To use slurm with scons, prefix the command you want scons to run with the srun command in the builder
i.e. srun computationallyexpensivejob infile outfile
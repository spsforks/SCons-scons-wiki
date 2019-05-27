# Using SCons on a cluster of parallel machines #
Usually machines like this are used in batch mode, where a large job is submitted and executed some time later.
To make your software work, all the machines need to be able to see a shared file system etc.
There are several pieces of software for doing this. One of them is [slurm](https://slurm.schedmd.com/).
## Slurm
To use slurm with SCons, prefix the command you want SCons to run with the srun command in a custom builder
i.e. srun computationallyexpensivejob infile outfile
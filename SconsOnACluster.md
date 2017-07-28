# SCons on a cluster #
SCons can be useful for controlling high performance computing workflows on a cluster.
# slurm #
Slurm is a tool for managing computation jobs on a cluster of high performance computers.
Usually slurm is used to submit jobs in batch mode.
To use slurm with scons, prefix the command you want scons to run with the srun command in the builder
i.e. srun computationallyexpensivejob infile outfile
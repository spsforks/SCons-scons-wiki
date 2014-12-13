

### How to limit the cache size (by abusing Progress())

The cache for derived files currently will grow indefinitely, which can cause problem for automated builds, or if the build generates very large files. It is however possible to attach a cleanup function to Progress(), which gets called every a few steps during the build. 

In the scenario from which the following example stems, object files are generated with varying compile time and sizes, and be able to cache large Fortran code with compile time on the order of several minutes is critically important. Therefore, a predictor is needed to estimate the time penalty for removing a file from the cache, and resulting in a rebuild. In this simple example, the rebuilt time is considered as proportional to the derived file size, and the likelihood of rebuilding decays exponentially. Therefore, the weight for each file is calculated as size * exp(-age * log(2) / half_time), and the file with the smallest weights are removed first. 

Scanning through the cache directory, if done at every step of the build, can have a large impact for a large build. This is avoided using Progress()' ninterval, and the cache directory is allowed to grow beyond the limit for few steps into the build. 


```txt
import os, sys, glob, time, math

class cache_progress:
    # The default is 1 GB cache and 12 hours half life
    def __init__(self, path = None, limit = 1073741824,
                 half_life = 43200):
        self.path = path
        self.limit = limit
        self.exponent_scale = math.log(2) / half_life
    def __call__(self, node, *args, **kw):
        self.delete(self.file_list())
    def delete(self, file):
        if len(file) == 0:
            return
        # Utter something
        sys.stderr.write(
            'Purging `%s\' (%d %s) from cache\n' %
            ('\', `'.join(file), len(file),
             len(file) > 1 and 'files' or 'file'))
        map(os.remove, file)
    def file_list(self):
        if self.path == None:
            # Nothing to do
            return []
        # Gather a list of (filename, (size, atime)) within the
        # cache directory
        file_stat = [
            (x, os.stat(x)[6:8]) for x in
            glob.glob(os.path.join(self.path, '*', '*'))]
        if file_stat == []:
            # Nothing to do
            return []
        # Weight the cache files by size (assumed to be roughly
        # proportional to the recompilation time) times an exponential
        # decay since the ctime, and return a list with the entries
        # (filename, size, weight).
        current_time = time.time()
        file_stat = [
            (x[0], x[1][0],
             x[1][0] * math.exp(self.exponent_scale *
                                (x[1][1] - current_time))),
            for x in file_stat]
        # Sort by highest weight (most sensible to keep) first
        file_stat.sort(key=lambda x: x[2], reverse=True)
        # Search for the first entry where the storage limit is
        # reached
        sum, mark = 0, None
        for i,x in enumerate(file_stat):
            sum += x[1]
            if sum > self.limit:
                mark = i
                break
        if mark == None:
            return []
        else:
            return [x[0] for x in file_stat[mark:]]
```
Example how to attach it into SConstruct: 


```txt
# Obtain the environment
env = Environment()
# Enable SCons cache
cache_directory = str(env.Dir(os.path.join('#', 'cache')))
env.CacheDir(cache_directory)
# Simple cache pruning, attached to SCons' progress callback. Trim the
# cache directory to a size not larger than cache_limit.
cache_limit = float(ARGUMENTS.get('cache_limit', '1024')) * 1048576
progress = cache_progress(cache_directory, cache_limit)
Progress(progress, interval = 8)
```
To further improve upon the behavior, it can be useful to scale the weight for different file types (e.g. to lower the weight for executables, which result in large files, but is much faster to generate than object files). 

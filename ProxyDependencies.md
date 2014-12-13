
Commands that have lots of input and output nodes can be very taxing on scons. For example: 


```txt
in = [...] # lots of nodes
out = [...] # lots of nodes

act = 'somecommand $SOURCES'

env.Command(out, in, act)
```
scons processes this as if each element in `out` depends on the entire set of `in`. Depending on how big `in` and `out`, you can really slow down the dependency verification process, as it takes time proportional to `len(in) * len(out)`. 

You can use a trick to make things better, but you need md5sum 


```txt
in = [...] # lots of nodes
out = [...] # lots of nodes

act = 'somecommand $MYSOURCES'

mnode = env.Command('sum.md5', in, 'md5sum $SOURCES > $TARGET')

env.Command(out, mnode, act, MYSOURCES = in)
```
This makes every node in `out` only depend on `mnode`, which in turn depends on each node in `in`. This can reduce the dependency processing significantly, as `mnode` only has to be verified once, and everything in `out` essentially recycles that work. 

The dependencyes between `out` and `in` are preserved. If something in `in` changes, then the contents of `mnode` change, because it is generated using md5sum, and thus `out` nodes will get rebuilt. 

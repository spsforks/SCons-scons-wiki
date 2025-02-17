
The `File` and `Dir` functions return File and Dir Nodes, respectively. Nodes are Python objects which have several user-visible attributes and methods that are often useful: 

* `path` - The build path of the given file or directory. This path is relative to the top-level directory (where the SConstruct file is found). The build path is the same as the source path if `variant_dir` is not being used. 
* `abspath` - The absolute build path of the given file or directory. 
* `srcnode()` - returns another File or Dir object representing the source path of the given File or Dir. 
See also [File()](File()). 

```python
# Get the current build dir's path, relative to top.
Dir(".").path
# Current dir's absolute path
Dir(".").abspath
# Next line is always '.', because it is the top dir's path relative to itself.
Dir("#.").path
File("foo.c").srcnode().path  # source path of the given source file.

# Builders return a list of File objects (a NodeList)
foo = env.Program("foo.c")
print("foo will be built in %s" % foo[0].path)
```

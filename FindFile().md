
Searches for a named file in the path specified by dirs. The file argument may be a list of file names or a single string file name. The dir argument may be a list of dir paths or a single string dir path. In addition to searching for files that exist in the filesytem, this function also searches for derived files that have not yet been built. 

The function returns a File object if the file is found, or None if not found. 

Although it is legal to provide a list of file names, it appears that the function will always return None in this case. 


```txt
foo = env.FindFile(’foo’, [’dir1’, ’dir2’])
```
See also [File()](File()), [Dir()](Dir()). 

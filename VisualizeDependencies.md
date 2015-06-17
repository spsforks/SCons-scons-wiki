
# Analyzing source trees, based on dependency graphs


## Tools

While trying to get a deeper understanding for the source of SCons, I actually wanted to see the classes and their dependencies. Googling around I found these two tools that could produce DOT graph files for class or import dependencies from Python source trees: 

* [http://furius.ca/snakefood](http://furius.ca/snakefood): Creates module import dependency graphs. Use the Mercurial command "hg clone [https://hg.furius.ca/public/snakefood](https://hg.furius.ca/public/snakefood)" for a checkout of the current sources. 
* [http://www.logilab.org/project/pylint](http://www.logilab.org/project/pylint): As part of pylint it analyzes class dependencies. 

## Commands

Having both applications installed, I called 


```txt
sfood -i . | sfood-graph > scons_import.dot
```

```txt
pyreverse -p scons -k .
```
with the SCons source directory as current folder. 

Unfortunately, the resulting graphs were pretty large and visualizing them via the _dot_ tool did not help. PNG, PS or SVG output, the images got too large and the layout of the nodes and edges left a lot to desire. 


## dottoxml.py

Then I remembered the yEd Graph Editor ([http://www.yworks.com/en/products_yed_about.html](http://www.yworks.com/en/products_yed_about.html)), a great application that can layout and handle even very large datasets...if you find a way to get the data inside. Since it does not import DOT files (yet), I wrote the little converter script dottoxml.py ([http://www.mydarc.de/dl9obn/programming/python/dottoxml](http://www.mydarc.de/dl9obn/programming/python/dottoxml)) that outputs yEd's native file format Graphml (XML). 

Now looking at complicated DOT graphs is a snap...have a try! 


## Examples

The following files were created with the sources for `SCons 1.2.0.d20090223` and `Waf 1.5.8`, they are all available in two versions: 

1. The nodes contain not only the class names, but also methods/attributes ("_fc" suffix) and 
1. class names only (no special suffix). 
Graphml files (XML) with dependencies that can be read directly by yEd: 

* SCons classes/packages [scons_graphml.zip](scons_graphml.zip) 
* Waf classes/packages [waf_graphml.zip](waf_graphml.zip) 
The original DOT files: 

* SCons classes/packages [scons_dot.zip](scons_dot.zip) 
* Waf classes/packages [waf_dot.zip](waf_dot.zip) 

## Screenshots


### SCons classes

[[!img /home/dirk/programming/python/tohh/structure/dots/classes_scons.png] [[!img /home/dirk/programming/python/tohh/structure/dots/classes_scons_close1.png] 

[[!img /home/dirk/programming/python/tohh/structure/dots/classes_scons_close2.png] 


### Waf classes

[[!img /home/dirk/programming/python/tohh/structure/dots/classes_waf.png] 

[[!img /home/dirk/programming/python/tohh/structure/dots/classes_waf_close1.png] 


### SCons packages

[[!img /home/dirk/programming/python/tohh/structure/dots/packages_scons.png] 


### Waf packages

[[!img /home/dirk/programming/python/tohh/structure/dots/packages_waf.png] 

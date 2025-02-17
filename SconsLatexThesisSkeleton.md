

# SCons Build Environment for LaTeX Theses

It is hard enough to write a thesis. And whoever has done some work using _larger_ documents knows that it is well worth investing some effort into structure. This thesis skeleton tries to help in adding structure without adding a significant work overhead. 

* structured directory hierarchy 
* figures for the document go into separate directories for the different chapter LaTeX sources 
* build automation using SCons 
* automatic generation of dependent/needed image files: 
      * generation of `pdflatex` compatible output file formats from EPS figures 
      * generation of `latex` compatible output file format from PDF/PNG/JPG figures 
      * generation of EPS and PDF output from GNUplot input files 
      * automatically finds image files for individual chapters to process 
* choice of DVI or PDF build target: `scons` or `scons dvi` 
* "Easy as" cleaning of build junk: `scons -c` (or `scons -c dvi`) 
For ease of maintainability go to the main documentation of this skeleton on Guy's wiki:   
 [http://www.kloss-familie.de/moin/TidBits/SconsLatexThesisSkeleton](http://www.kloss-familie.de/moin/TidBits/SconsLatexThesisSkeleton) 

A bit more on the background has been blogged about [here](http://www.kloss-familie.de/blog/article.php?story=20070806062236152) with further updates to the whole matter [here](http://www.kloss-familie.de/blog/article.php?story=20090528022145172). 

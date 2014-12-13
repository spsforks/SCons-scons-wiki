
Here is a spot to discuss LaTeX/TeX build tool issues. 

What commands, packages that create files are supported?: 

* \bibliography 
* \makeindex, makeidx 
* \tableofcontents 
* \listoftables 
* \listoffigures 
* \makeglossary, glossary 
* \makeglossaries, glossaries 
* \makenomenclature, nomenclature 
* beamer document class 
* bibunits 
I see several spots of immediate interest to get working (these have been dealt with): 

1. integrate index patch ([bug](http://sourceforge.net/tracker/index.php?func=detail&aid=1457764&group_id=30337&atid=398973)) 
1. improved bibtex 
   1. add output files to emitter 
   1. include check for "bibliography" in the scanner 
1. bibunit support 
1. test [BuildDir](BuildDir) with the TeX builders 

# A minimal Latex SConstruct file


```txt
import os
env=Environment()
# Look in standard directory ~/texmf for .sty files
env['ENV']['TEXMFHOME'] = os.path.join(os.environ['HOME'],'texmf')
env.PDF('main.tex')
```
This SConstruct file is appropriate to a setting where an author maintains personal styles and fonts in a user local directory ~/texmf.  In a collaborative setting, _TEXMFHOME_ should not be set to a user-relative path. 


# A skeletal thesis file

Dr Nicola Talbot from the University of East Anglia provides a wealth of tips and tutorials concerning LaTeX on his [Latex Related Information](http://theoval.sys.uea.ac.uk/~nlct/latex/) web site.  For a simple yet realistic initial test, you might try the skeletal thesis file he recommends in _Using LaTeX to Write a PhD Thesis_: 


```txt
\documentclass[a4paper]{report}
\begin{document}
\title{A Sample PhD Thesis}
\author{A. N. Other}
\date{July 2004}
\maketitle
\pagenumbering{roman}
\tableofcontents
\listoffigures
\listoftables
\chapter*{Acknowledgements}
\begin{abstract}
\end{abstract}
\pagenumbering{arabic}
\chapter{Introduction}
\label{ch:intro}
\chapter{Technical Introduction}
\label{ch:techintro}
\chapter{Method}
\label{ch:method}
\chapter{Results}
\label{ch:results}
\chapter{Conclusions}
\label{ch:conc}
\bibliographystyle{plain}
\bibliography{thesis}
\end{document}
```

# Troubleshooting

Attempting to process the thesis skeleton file above with the simple Scons script above, I received the following error: 


```txt
  scons: *** While building `['thesis-skel.pdf']' from `['thesis-skel.tex']':
  Don't know how to build from a source file with suffix `.tex'.
  Expected a suffix in this list: ['.dvi', '.ps'].
```
The text of the error suggests that Scons does not have the necessary build logic, when in fact the problem was that my system did not have TeX fully installed. 

On my Fedora Core 4 Linux system, I installed all the tetex packages from the package system manually with the command: 

* sudo yum install tetex tetex-doc tetex-latex tetex-fonts tetex-dvips tetex.afm tetex.xdvi 
Note: the download for tetex-doc was 50MB and probably isn't necessary to run the TeX/LaTeX builders. 

Once TeX was fully installed, the build proceeded with much verbosity and generated a 12-page PDF output consisting of front-matter, content, and back-matter pages with appropriate page numbering, formatting and titles with mostly empty page contents. 

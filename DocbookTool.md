

# The SCons Docbook tool

This tool tries to make working with Docbook in SCons a little easier. It provides several toolchains for creating different output formats, like HTML or PDF. Contained in the package is a distribution of the Docbook XSL stylesheets as of version 1.76.1. As long as you don't specify your own stylesheets for customization (see Selecting stylesheet), these official versions are picked as default...which should reduce the inevitable setup hassles for you. 

Implicit dependencies to images and XIncludes are detected automatically if you meet the HTML requirements (see Requirements). The additional stylesheet `utils/xmldepend.xsl` by Paul [DuBois](DuBois) is used for this purpose. 

Note, that there is no support for XML catalog resolving offered! This tool calls the XSLT processors and PDF renderers with the stylesheets you specified, that's it. The rest lies in your hands and you still have to know what you're doing when resolving names via a catalog.  


## Install

Installing it requires you to copy (or, even better: checkout) the contents of the package's `docbook` folder to 

* "`/path_to_your_project/site_scons/site_tools/docbook`", if you need the Docbook Tool in one project only, or 
* "`~/.scons/site_scons/site_tools/docbook`", for a system-wide installation under your current login. 
For more infos about this, please refer to  

* the SCons User's Guide, chap. 19.7 "Where to put your custom Builders and Tools" and 
* the SCons Tools Wiki page at [http://scons.org/wiki/ToolsIndex](http://scons.org/wiki/ToolsIndex). 

## How to activate

For activating the tool "docbook", you have to add its name to the Environment constructor, like this 


```txt
env = Environment(tools=['docbook'])
```
On its startup, the Docbook tool tries to find a required `xsltproc` processor, and a PDF renderer, e.g. `fop`. So make sure that these are added to your system's environment `PATH` and can be called directly, without specifying their full path. 


## Requirements

For the most basic processing of Docbook to HTML, you need to have installed 

* the Python `lxml` binding to `libxml2`, or 
* the direct Python bindings for `libxml2/libxslt`, or 
* a standalone XSLT processor, currently detected are `xsltproc`, `saxon`, `saxon-xslt` and `xalan`. 
Rendering to PDF requires you to have one of the applications `fop`, `xep` or `jw` installed. 


## Processing documents

Creating a HTML or PDF document is very simple and straightforward. Say 


```txt
env = Environment(tools=['docbook'])
env.DocbookHtml('manual.html', 'manual.xml')
env.DocbookPdf('manual.pdf', 'manual.xml')
```
to get both outputs from your XML source `manual.xml`. As a shortcut, you can give the stem of the filenames alone, like this: 


```txt
env = Environment(tools=['docbook'])
env.DocbookHtml('manual')
env.DocbookPdf('manual')
```
and get the same result. Target and source lists are also supported: 


```txt
env = Environment(tools=['docbook'])
env.DocbookHtml(['manual.html','reference.html'], ['manual.xml','reference.xml'])
```
or even 


```txt
env = Environment(tools=['docbook'])
env.DocbookHtml(['manual','reference'])
```
Important: Whenever you leave out the list of sources, you may not specify a file extension! The Tool uses the given names as file stems, and adds the suffixes for target and source files accordingly. 

The rules given above are valid for the Builders `DocbookHtml`, `DocbookPdf`,  `DocbookSlidePdf` and `DocbookXInclude`. For the `DocbookMan` transformation you can specify a target name, but the actual output names are automatically set from the `refname` entries in your XML source. 

Please refer to the section Chunked output for more infos about the other Builders. 


## Selecting your own stylesheet

If you want to use a specific XSL file, you can set the additional `xsl` parameter to your Builder call as follows: 


```txt
env.DocbookHtml('other.html', 'manual.xml', xsl='html.xsl')
```
Since this may get tedious if you always use the same local naming for your customized XSL files, e.g. `html.xsl` for HTML and `pdf.xsl` for PDF output, a set of variables for setting the default XSL name is provided. These are: 


```txt
DOCBOOK_DEFAULT_XSL_HTML        
DOCBOOK_DEFAULT_XSL_HTMLCHUNKED        
DOCBOOK_DEFAULT_XSL_HTMLHELP        
DOCBOOK_DEFAULT_XSL_PDF        
DOCBOOK_DEFAULT_XSL_MAN        
DOCBOOK_DEFAULT_XSL_SLIDESPDF        
DOCBOOK_DEFAULT_XSL_SLIDESHTML        
```
and you can set them when constructing your environment: 


```txt
env = Environment(tools=['docbook'],
                  DOCBOOK_DEFAULT_XSL_HTML='html.xsl',
                  DOCBOOK_DEFAULT_XSL_PDF='pdf.xsl')
env.DocbookHtml('manual') # now uses html.xsl
```

## Chunked output

The Builders `DocbookHtmlChunked`, `DocbookHtmlhelp` and `DocbookSlidesHtml` are special, in that: 

* they create a large set of files, where the exact names and their number depend on the content of the source file, and 
* the main target is always named `index.html`, i.e. the output name for the XSL transformation is not picked up by the stylesheets. 
As a result, there is simply no use in specifying a target HTML name.  So the basic syntax for these builders is: 


```txt
env = Environment(tools=['docbook'])
env.DocbookHtmlhelp('manual')
```
Only if you use the `root.filename` (`titlefoil.html` for slides) parameter in your own stylesheets you have to give the new target name. This ensures that the dependencies get correct, especially for the cleanup via "`scons -c`": 


```txt
env = Environment(tools=['docbook'])
env.DocbookHtmlhelp('mymanual.html','manual', xsl='htmlhelp.xsl')
```
Some basic support for the `base.dir` is added (this has not been properly tested with variant dirs, yet!). You can add the `base_dir` keyword to your Builder call, and the given prefix gets prepended to all the created filenames: 


```txt
env = Environment(tools=['docbook'])
env.DocbookHtmlhelp('manual', xsl='htmlhelp.xsl', base_dir='output/')
```
Make sure that you don't forget the trailing slash for the base folder, else your files get renamed only!  


## All builders

A simple list of all builders currently available: 
DocbookHtml
: Single HTML file. 

DocbookHtmlChunked
: 
Chunked HTML files, with support for the `base.dir` parameter. The `chunkfast.xsl` file (requires "EXSLT") is used as the default stylesheet. 


DocbookHtmlhelp
: 
Htmlhelp files, with support for `base.dir`. 


DocbookPdf
: PDF output. 

DocbookMan
: Man pages. 

DocbookSlidesPdf
: Slides in PDF format. 

DocbookSlidesHtml
: 
Slides in HTML format, with support for `base.dir`. 


DocbookXInclude
: Can be used to resolve XIncludes in a preprocessing step. 



## Need more?

This work is still in a very basic state and hasn't been tested well with things like variant dirs, yet. Unicode problems and poor performance with large input files may occur. There will definitely arise the need for adding features, or a variable. Let us know if you can think of a nice improvement or have worked on a bugfix/patch with success. Enter your issues at the Launchpad bug tracker for the Docbook Tool, or write to the User General Discussion list of SCons at `users@scons.tigris.org`. 

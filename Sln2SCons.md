
A python script to convert Microsoft Visual Studio 2005 solution files (*.sln) and the associated project files (*.vcproj) into a set of SCons files (SConstruct and SConscript) can be found at: [http://www.alfersoft.com.ar/blog/2008/05/23/converting-visual-studio-solutions-to-scons/](http://www.alfersoft.com.ar/blog/2008/05/23/converting-visual-studio-solutions-to-scons/) 

The class Sln2SCons does all the work, parses the sln and vcproj files and generates a main SConstruct and one SConscript for every project in the solution. 

Here is the direct link to the Google Code project: [http://code.google.com/p/sln2scons/](http://code.google.com/p/sln2scons/) 

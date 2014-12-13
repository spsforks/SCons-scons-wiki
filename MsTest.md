

## Integrating mstest and coverage reporting in 3rd party Build system with scons


#### (Tested with VS 2005 only)

I have added mstest.py as new patch, there is a plan to add it to 1.0. But I also added generation of coverage report from mstest run (if coverage was enabled). It does involve running special converter utility and use of external XML python module. So it can not be added in base scons package. I decided to describe steps here. 

What will it do? 

* Runs mstest 
* If you configured coverage in your xxx.testrunconfig scons will convert result to .xml file and then generate short .html report by using .xsl. 
Why? 

* You don't want to use TFS to build your .Net projects, you are using some other build system like [CruiseControl](CruiseControl), [Parabuild](http://www.viewtier.com/)etc. 
* You want to have Unit Tests and Coverage result presented in your build system 
How to do it? 

* Install: libxml2 and libxslt. It developed by: [http://xmlsoft.org/python.html](http://xmlsoft.org/python.html) you can download Windows installer from: [http://users.skynet.be/sbi/libxml-python/](http://users.skynet.be/sbi/libxml-python/)  You will need both modules libxml2 and libxslt 
* Download [Microsoft.VisualStudio.Coverage.Analysis.dll](Microsoft.VisualStudio.Coverage.Analysis.dll), [coverage.xsl](coverage.xsl), [mstest2xml.exe](mstest2xml.exe) from this page attachments and put it to your system. Also download , [mstest.py](mstest.py). Note: you might need to modify lines: 55, 56, 58,59 to make scons find these files you just downloaded on your system 
* Add mstest.py as tool 
* After you run mstest builder, something like: MsTest("TestResults/unittest.trx","mytests.vsmdi"), and your mytests.vcmdi has coverage enabled, it will generate data.coverage binary file somewhere in In directory  TestResults/username_host 2008-04-10 09_01_43/In/host/. 
* Then scons will look for that file in TestResults/username_host 2008-04-10 09_01_43/In/host/data.coverage  You might need to adjust it 
* mstest.py will run **mstest2xml.exe out covReport xml**, where: **out **location of Out directory, like  TestResults/username_host 2008-04-10 09_01_43/Out, **covReport **full path to data.coverage file and **xml **location of xml file 
* Then mstest builder will convert generated XML file to html by using coverage.xsl. So from 10 Mb xml file you get small html report like this: This is the coverage report 

# Assembly coverage
[[!table header="no" class="mointable" data="""
Assembly  | Blocks not covered  | % blocks not covered 
my1.dll  | 2419               of               4008  | 60.3542914171657 
my2.dll  | 125               of               146  | 85.6164383561644 
my3.dll  | 56               of               74  | 75.6756756756757 
my4.dll  | 105               of               384  | 27.34375 
my5.dll  | 401               of               463  | 86.6090712742981 
my6.dll  | 1605               of               3934  | 40.7981698017285 
my7.dll  | 287               of               458  | 62.6637554585153 
"""]]

If you want to modify mstest2xml.exe, there is .Net code for it, also it depends on Microsoft.[VisualStudio](VisualStudio).Coverage.Analysis.dll, so add it as reference: 


```txt
using System;
using System.Collections.Generic;
using Microsoft.VisualStudio.CodeCoverage;

namespace mstest2xml
{
    class Program
    {
        static void Main(string[] args)
        {
            String CoveragePath = args[0];
            // Create a coverage info object from the file
            CoverageInfoManager.SymPath = CoveragePath;

            CoverageInfoManager.ExePath = CoveragePath;

            CoverageInfo ci = CoverageInfoManager.CreateInfoFromFile(args[1]);
            // Ask for the DataSet
            // The parameter must be null
            CoverageDS data = ci.BuildDataSet(null);

            // Write to XML
            data.WriteXml(args[2]);
        }
    }
}
```
Note: for reference I used next article as source for ideas and instructions:  [joc'c bLog](http://blogs.msdn.com/ms_joc/articles/495996.aspx) 

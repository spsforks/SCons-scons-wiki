
PyuicBuilder is simple builder to generate Python files for [PyQt](http://www.riverbankcomputing.co.uk) from Qt .ui sources. The .ui files are typically created in [QtDesigner](http://qt.nokia.com/doc/qt4-designer.html). 


```txt
# Builder for PyQt pyuic4
# Based on this: http://osdir.com/ml/programming.tools.scons.user/2003-08/msg00126.html
# and a tip from Sergey Popov on freenode.net #scons

import os
env = Environment(ENV = os.environ )

uic_builder_py = Builder(
        action = 'pyuic4 $SOURCE -o $TARGET',
    suffix = '.py',
        src_suffix = '.ui',
        single_source = True)

env.Append( BUILDERS = { 'FormPy': uic_builder_py } )

env.FormPy(source=Glob('*.ui'))
```
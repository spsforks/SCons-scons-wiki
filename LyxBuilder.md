
# Teaching PDF to understand .lyx files

Note that this builder has been added to the SCons "contrib" repo at https://bitbucket.org/scons/scons-contrib , as of 2016-12-07! Get your latest copy from there... 

## Usage


```python
#!python
env = Environment(tools=['default','pdftex','pdflatex','lyx'])
env.PDF(source='test.lyx')

```

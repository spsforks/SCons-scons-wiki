
You have a big hierarchical tree of projects. If someone accidentally enters: 
```txt
scons
```
it will build every project in that tree. If you want to ensure that they meant to build everything, add this to the SConstruct file: 
```python
#!python
#prevent accidental building of everything
Default(None)
```
If someone does want to build every project, they must do so explicitly by: 
```txt
scons .
```
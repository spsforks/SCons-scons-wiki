Suppose you have a big hierarchical tree of projects. If someone accidentally enters: 

```console
scons
```
it will build every project in that tree. If you want to ensure that they meant to build everything, add this to the SConstruct file: 

```python
# prevent accidental building of everything
Default(None)
```
If someone does want to build every project, they must do so explicitly by: 
```console
scons .
```

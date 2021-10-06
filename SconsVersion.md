**How to retrieve the version of SCons from your script ?**

Ah! We don't really have a defined, public interface for this. We should have. In the meantime, you can use:

```python
import SCons
print SCons.__version__
```
(Where, of course, you can do whatever you like with the `SCons.__version__` string, not just print it.)

If you are looking to ensure a certain version of SCons, use:
[`EnureSConsVersion`](http://www.scons.org/doc/production/HTML/scons-user.html#f-EnsureSConsVersion)

For example, using `EnsureSConsVersion(0, 96, 93)` will exit SCons with an appropriate error message if the version of SCons is not at least 0.96.93


Credits: [StevenKnight](StevenKnight), [TaybinRutkin](TaybinRutkin)



The ARGUMENTS dictionary contains the command line arguments you passed in, for example: 
```txt
C:\projects> scons.py myproject release=1
```
The value retrieved from the dictionary is a string. Here's an example: 
```txt
if ARGUMENTS.get('release', '0') == '1':
  print "*** Release build..."
  buildroot = 'release'
else:
  print "*** Debug build..."
  buildroot = 'debug'
```


---

 If the command line is : 
```txt
C:\projects> scons.py myproject -c
```
The output is: 
```txt
*** Debug build...
```


---

 If the command line is : 
```txt
C:\projects> scons.py myproject -c release=0
```
The output is: 
```txt
*** Debug build...
```


---

 If the command line is : 
```txt
C:\projects> scons.py myproject -c release=1
```
The output is: 
```txt
*** Release build...
```
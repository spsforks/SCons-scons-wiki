

# Memory Reduction War Stories


## Episode 4: Light-weight classes with __slots__

SCons creates a lot of instances of various classes when conducting large software builds. Some of those objects only have few attributes so the overhead that every instance carries accounts for a large amount of memory. Chris AtLee proposed the application of [slotted classes in SCons](http://scons.tigris.org/servlets/ReadMsg?listName=users&msgNo=11883). Jean Brouwers, the author of asizeof, gives a good [motivation for using classes with slots](http://mail.python.org/pipermail/python-list/2004-May/261985.html). 


### __slots__ properties

* Introduced with Python 2.2 
      * Cannot be weakly referenced (needs Python 2.3) 
* Instance attributes to be set must have a slot assigned, otherwise an `AttributeError` is thrown 
      * Might have a `__dict__` slot to overcome this problem (needs Python 2.3) 
* Can't be pickled automatically, `__setstate__` and `__getstate__` must be specified 
* Existing methods can't be overridden 

### Picking a class

Choosing a class for assigning slots can be eased by evaluating which type of instances take up most of the memory. The following chart was generated with the `HtmlStats` facility of the Heapmonitor while making an up-to-check of Ardour. 

[[!img timespace.png] 


### Executor

The Executor objects are interesting due to the large number of instances in memory intensive builds. Furthermore, the classes are easily converted to slotted classes due to the small number of attributes. The only needed change concerns method assignments. This problem can be circumvented creating a slot for the method and initializing the slot to the actual method. 
[[!table header="no" class="mointable" data="""
 Hello World (Clean Build)  |  Executor.Executor   |  Executor.Null 
 Instance #                 |  4                   |  4             
 Original size (average)    |  906 Byte            |  1006 Byte     
 Original size (min)        |  856 Byte            |   944 Byte     
 Original size (max)        |  1.02 KB             |   1.16 KB      
 Slot class size (average)  |  676 Byte             |   924 Byte     
 Slot class size (min)      |  608 Byte             |   840 Byte     
 Slot class size (max)      |  880 Byte             |  1.15 KB     
"""]]
[[!table header="no" class="mointable" data="""
 Ardour (Up-to-date check)  |  Executor.Executor   |  Executor.Null 
 Instance #                 |  1348                |  2135          
 Original size (average)    |  856 Byte            |  944 Byte      
 Original size (total)      |  1.12 MB (4%)        |  1.92 MB (7%)  
 Slot class size (average)  |  681 Byte             |   840 Byte     
 Slot class size (total)    |  897.14 KB (3.08%)    |  1.71 MB (6%) 
"""]]

[slot_executor.patch](slot_executor.patch) 


### Node objects

Depending on the project, Node objects take between 60-90% of the memory observable with the Heapmonitor. This makes them the perfect candidates for memory reduction.  


### Node Attrs

An `Attrs` instance is stored in each Node object. It serves as a dictionary to store additional information - presumably by Tools. Turning this into a slotted class is easy but only allows a very minor memory reduction. Moreover, `Attrs` should still be used as a general purpose dictionary so I attached a `__dict__` slot.  

[slot_attrs.patch](slot_attrs.patch) 


### NodeInfo, BuildInfo and SConsign

Every Node object has a `BuildInfo` and `NodeInfo` structure attached to it. This takes a considerable amount of space in the Node object. Trying to turn these objects into slotted classes is more involved, though. The pickling must be done manually and the sconsign format differs. It is possible to use existing sconsign databases.  However, once the sconsign database was emitted using slot classes, it cannot be used anymore from older versions of SCons. 
[[!table header="no" class="mointable" data="""
 Hello World (Clean Build)  |  Node.FS.Entry      |  Node.FS.File  |  SConsign.DB 
 Instance #                 |  2                   |  3              |  2           
 Original size (average)    |  5.75 KB             |  4.81 KB        |  1.02 KB     
 Slot class size (average)  |  4.99 KB             |  4.46 KB        |   916 B      
"""]]
[[!table header="no" class="mointable" data="""
 Ardour (Up-to-date check)  |  Node.FS.Entry      |  Node.FS.File  |  SConsign.DB 
 Instance #                 |  2238                   |  1393        |  69           
 Original size (average)    |  7.72 KB             |  5.88 KB        |  8.06 KB     
 Slot class size (average)  |  7.26 KB             |  5.46 KB        |  6.68 KB      
"""]]

[slot_sconsign.patch](slot_sconsign.patch) 


## Results

The previous results look promising but do not provide an overview about the whole memory consumption and execution time impact. 
[[!table header="no" class="mointable" data="""
                   |  Ardour up-to-date check memory  |  Ardour up-to-date check runtime 
 Classic           |  60.34 MB    |  43.7s 
 `Executor` slotted  |  58.60 MB    |  43.7s 
 `*Info` slotted  |  56.94 MB  |  45.1s 
 All patches applied  |  55.14 MB  |  45.2s 
"""]]

All tests were run on 32bit Linux with Python 2.5.2 and the Heapmonitor Branch of SCons based on version 0.98.5. 

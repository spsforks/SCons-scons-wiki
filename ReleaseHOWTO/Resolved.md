
[FIXME](ReleaseHOWTO/Resolved) This segment is overkill for anyone who actually uses SVN.  Cut it or drop it. 

A conflict occurs when SVN tries to apply changes from the archive that overlap with other changes made locally.  These are rare but can happen when cherry-picking applies changes out of order.  In general, the correct approach is to use the text from the archive rather than the local version, but use your judgment when making the changes as there will be some cases where the original text (or even a merger of the two texts) is the correct choice as SVN is not always accurate when marking the conflicted regions. 

**Finding conflicts** 

To determine if there're conflicts, run this command: 
```txt
  $ svn status
  ?      test/example.py.r4941
  ?      test/example.py.mine
  ?      test/example.py.r4649
  C      test/example.py
  ?      src/engine/SCons/CoreFile.py.r4941
  ?      src/engine/SCons/CoreFile.py.mine
  ?      src/engine/SCons/CoreFile.py.r4649
  C      src/engine/SCons/CoreFile.py
  $
```
Lines that begin with "`C`" identify a file that's conflicted.  There are also a number of related files provided by SVN that can be used in the process of resolution, identified by lines that begin with "`?`".  This is a simple resolution, so we won't use them. 

**Removing Conflicts** 

To remove the conflicts from a file, follow these steps: 

* Locate a conflict marker in the text.  The center of each conflicted region is marked with "`=======`" so searching for a line with only that on it will get you to the right place. 
* The start of the region is marked with "`<<<<<<< .mine`" and contains the local text.  Delete this text as well as the start and center markers. 
* The end of the region is marked with something that looks like "`>>>>>>> .r54321`" and contains the text from the SVN archive.  Delete the end marker. 
* Repeat until there are no more conflict markers. 
To see how your updated file compares with the archive, run this command: 
```txt
  $ svn diff test/example.py
```
If the changes aren't satisfactory, repeat the editing step. 

Once the editing is done, use this command to tell SVN that the conflict has been resolved: 
```txt
  $ svn resolved test/example.py
```
As a side-effect, resolving the conflict will remove the related files provided by SVN. 

Repeat this section for each conflicted file. 

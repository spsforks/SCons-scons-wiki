

## Persist Data Between Runs

[[!bug 1678]] is about being able to keep `--srcdir` command-line options between runs.  Since I see a need to keep configuration information between runs as well, I view fixing that bug as a prerequisite for future configuration work, so I'm providing as much insight as I can to make it easier to do.  And once a generic facility is in place, there's other information that could be kept between runs as well. 

I'm going to make a very concrete description of one way this might work.  Be clear that it's not the only way, and it may not be the best way.  And I'm not wed to any of the names; they are made up purely to make it easier to describe the process. 


### Working Top

The top of the working directory is identified by a file which we'll call `.scons.top`, although `.sconfigure` might be a more attractive name.  (This is where `.sconsign` is currently created, so one option would be to merge them.)  The `.scons.top` file is the place where all values are kept that should survive between runs. 

For purposes of discussion, we'll assume it's a text file, but it could just as well be XML or binary.  The `.scons.top` file is created even if it is empty; it's purpose is to identify the top of the tree reliably even if other markers (liks a `SConstruct`) are missing. 

There's an internal API for putting stuff in the file; some aspects of the API may be exposed to the public, probably indirectly. 


### Top Calculation

Here are the conditions that can affect what needs to be done.  (Presumably something very similar to this scheme is already done to determine the location of the `.sconsign` file, but I wanted to make it explicit.)  **OUCH: Steven has pointed out that the `SConstruct` file may be in SCCS or RCS, so the search needs to include the default `SourceCode()` lookup as well.** 
[[!table header="no" class="mointable" data="""
**Name** | **Condition**
||
top | `.scons.top` is present in current directory
cur | A _SConstruct flavor_ (`SConstruct`, `Sconstruct`, or `sconstruct` file) is found in the current directory
src | `--srcdir` options are present on command line
up | one of the `--up` options is present
"""]]

Here are the actions that must be taken based upon the state of the contitions.  If a condition must be true, its column is marked with a '+'; if false, with a '-'; if don't care, with an 'x'.  The action column describes what to do.  A letter in parenthesis indicates a common action that is used in more than one place. 
[[!table header="no" class="mointable" data="""
t  
o  
p | c  
u  
r | s  
r  
c | u  
p | **Action**
|||||
+ | x | + | x | Error "extraneous --srcdir options present"
+ | x | - | x | (A) process `.scons.top` and proceed normally
- | + | x | x | (B) create `.scons.top` and proceed normally
- | - | - | + | Scan up. If `.scons.top`, use (A); if SConstruct flavor, use (B); otherwise error "SConstruct not found when scanning up"
- | - | + | - | (C) If SConstruct flavor via `--srcdir`, use (B); otherwise error "SConscript not found"
- | - | - | - | (GNU compatibility) set `--srcdir=..` and use (C)
- | - | + | + | Damifino; needs a decision: is this more 'src' or 'up'?
"""]]

Action (B) to create a `.scons.top` file uses the primitive operation below to place a `SourceDir(`_dirname_`)` line in the file for each `--srcdir` command-line option. 

Action (A) to process the `.scons.top` file executes it in a special context where the _persistence names_ (see below) like `SourceDir` are defined.  (Other schemes are possible; remember I'm not wedded to this one.)  The `SourceDir` method causes its parameter to be treated as if it were present on the command line as a `--srcdir` option. 


### Primitive Operations

There are two primitive operations: one to accumulate the file content and one to flush the file contents to disk if the new content differs. 

There's an internal primitive that is handed pieces of text to add to the `.scons.top` file, which it keeps in a buffer.  It's likely that it will be that dirt simple, but it's possible that it may need to keep track of several buffers so they can be written in the correct order. 

When the `scons` command is terminated normally, the second primitive compares the buffer(s) against the file contents and overwrites the file contents if there's a difference. 


### Extensions

To extend persistence to other values, add a method to the persistence names.  When run, this method should produce the effects requested by its arguments and then reinsert itself with the same arguments in the `.scons.top` file. 

Possible extensions include cached configuration values to avoid recalculations and external variant build directories with pre-configured parameters. 

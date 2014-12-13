
[Russel Winder](RusselWinder) may provide more insight into optimal plugin scheme following information from [ToolsIndex](ToolsIndex). 

I thought about using Abstract Base Classes as described here [http://www.doughellmann.com/PyMOTW/abc/](http://www.doughellmann.com/PyMOTW/abc/) but there can be alternative (or more simple solutions). Trac component system is nice, but IMO not documented good enough for plugin writers, and it may be an overkill for our purposes, especially for debugging (like with any observers that are dynamically inserted). -- [techtonik](techtonik) 2010-05-06 14:15:58 

**Russel Winder** 

Given the invitation above B) 

The principle question is, what is a _plugin_.  Currently SCons has just infrastructure and tools.  Currently all infrastructure and most tools are provided as part of the core SCons.  Although the core tools are realized using Python modules, SCons allows for tools to be realized as Python packages as well.  This means that tools can be developed (though not currently tested :-( ) separately from the SCons core.  So if _plugin_ means a SCons tool then SCons already has a plugin capability.  The API is not flexible and possible needs a rethink, but it is there.  If however, _plugin_ should mean more than a SCons tool, the core infrastructure of SCons would need a rework (I guess). 

I guess we could address this by asking "For what do we need plugins with SCons?".  Supporting new languages is handled by the tool idea, so that is covered already.  What other things might plugins be developed to do?  If we can enumerate a few exemplars, it might give us an idea of what the API should look like. 

[Russel Winder](RusselWinder) 2010-05-07T07:04:47BST 

_NB Its a pity [MoinMoin](MoinMoin) doesn't implement ISO8601 for its timestamps :-( _ 

   * It is a problem of Python standard library - [http://bugs.python.org/issue7584](http://bugs.python.org/issue7584)  -- [techtonik](techtonik) 2010-05-08 16:15:23 Thanks for adding this, a useful link.  [Russel Winder](RusselWinder) 2010-05-08T17:58:00BST 

A page for specific goals of the Rearchitecture, both design goals and implementation goals. 

(Consider this the requirements specification, although we're calling it "Goals" because everything here won't be a hard-and-fast requirement.) 

[[!toc 4]] 


# Performance

Performance is divided into two general categories: 

   * _Big-O_ for functionality that must be executed and whose performance is limited by the algorithmic complexity of the underlying problem to be solved. 
   * _Caching_ for functionality whose cost can be amortized over multiple calls by remembering the result of previous calculations. 
When features are considered, they should be evaluated by these criteria: 

   * Any feature that slows down performance from its goal can potentially be sacrificed and should be **explicitly** considered for whether or not to keep it. 
   * Any feature we decide to keep that **does** slow down performance should have its impact on evaluation time documented. 
Performance criteria will have specific regression tests to monitor that the performance stays in bounds. 


## Big-O

   * Strive for `O(nodes)` performance when evaluating builds for up-to-dateness and scheduling them.  Fallback possibilities include redefining this to `O(nodes + arcs)` if arc processing is non-negligible, or `O(nodes + arcs) + overhead` if overhead isn't constant. 
   * Strive for `O(sources + targets)` performance when determining whether a given build is up-to-date.  Note that we'll do `O(nodes)` of up-to-date evaluations so the `(sources + targets)` should properly be migrated into the previous performance criteria, but it's probably simpler to focus on them separately. 
   * [/Discussion#O(1) CPPPATH](DeveloperGuide/ReArchitecture/Goals/Discussion) 
   * _OTHERS..._ 

## Caching

   * Strive for at most one `os.stat()` call of any file (per location[1]) before building, and at most one `os.stat()` call of any file after building. 
   * Strive for at most one MD5 checksum of the contents of an `Entity` before building, and at most one MD5 checksum of the contents after building. 
   * _OTHERS..._ 
[1] A file may be found in more than one location: an optional build directory, a working directory, and any number of repositories.  The goal is at most one `os.stat()` call in each of the possible locations. 


## Startup

   * Explicitly support saving state between runs to minimize startup time. 

# Design

   * Be relatively unconstrained by the current SCons design and implementation.  Within that, refer to the current SCons feature set as a reference list of what we have to design for, or explicitly exclude). 
   * Be unafraid of re-using design (or even code, when we get to that point) from other projects. 
   * AFTER the design is "complete," be able to figure out a reasonably incremental transition to the new design, probably in some subsystem-by-subsystem fashion. 

# Architecture

   * Avoid (over)use of inheritance.  That led to much of the current rat's nest. 

# Transition

   * Any feature we discard must have some documented transition plan: 
         * Transparently support old and new implementations. 
         * Follow the [DeprecationCycle](DeprecationCycle) to a new implementation. 
         * Support side-by-side old and new implementations (for example, maybe a new-steyle `Environment` with better performance but perhaps restricted functionality--similar in concept to Python classic classes and new-style classes, although nwe-style classes didn't actually scale back functionality...). 
         * Documenting the requirement to change configuration. 

# APIs

   * Clear distinction between the "external API" and "internal API": 
         * External API is immutable and must be maintained for backwards compatibility or put through the [DeprecationCycle](DeprecationCycle). 
         * Internal API is mutable and can change at will out from under the users.  (In practice, since it's all Python and nothing prevents users from reaching in to internal APIs they shouldn't, we may still exercise judgment and put an internal API through the [DeprecationCycle](DeprecationCycle) to avoid hassle for important customers.  But that should be decided on a case-by-case basis, and we are "within our rights" to break use of internal APIs.) 

# Testing


## Unit Testing

   * All modules will be thoroughly unit tested to defined APIs.  This should help with the architecture, as designing for unit testability is a proven useful technique on other projects for architectural consistency. 

## System Testing

   * End-to-end system tests define supported behaviors of user-hardened interfaces. 
         * If it's in a system test, it's by definition user-visible behavior and must be maintained for backwards compatibility, or explicitly put through the [DeprecationCycle](DeprecationCycle). 
         * If it's user-visible behavior that's not in a system test, put it in a system test. 

## Performance Testing

   * As indicated above, performance criteria will have specific regression tests to monitor that the performance stays in bounds. 
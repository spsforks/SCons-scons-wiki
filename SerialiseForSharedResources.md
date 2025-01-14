

# Serialise for shared resources

Some tasks are best executed in series, either because they share resources which are more efficiently utilised in series or they share unique resources which cannot be accesed simultaniously. 

A simple solution is to only invoke _scons_ without _-j N_, unless N = 1. 

However, in a build consisting of a mixture of tasks that can be executed in parallel and tasks that need to be serialised, requiring all the tasks that can be run in parallel to execute in series is non optimal. 

The solution for the tasks that you know share resources is to tell scons that they create the same dummy file as a side effect. Scons will avoid executing only these tasks in parallel to avoid simultaneous acess to this dummy file. 


## Example

```py
env.BuilderUsingSharedResource(source="x1.in", target="x1.out")
env.BuilderUsingSharedResource(source="x2.in", target="x2.out")
env.AnyOtherBuilder(source="x3.in", target="x3.out")

env.SideEffect("dummyfile", "x1.out")
env.SideEffect("dummyfile", "x2.out")
```
In this case when the script is invoked with scons -j 2 we should expect only x3.out to be created in parellel, the other two tasks should be completely serialised. 

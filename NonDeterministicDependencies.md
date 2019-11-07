# Non Deterministic Dependencies

This problem arises when a builder can create more than one target, and the number of targets cannot be known until that builder is executed. Other builders may be required to process each of those targets, and other builders may then be dependent on all of those results. 

The solution is to have the non deterministic builder create a file listing it's targets, and have a dependant builder use a scanner to read that file to find the dependancies, process them and use them as sources. 

The stand alone example below shows how to make such a dynamic builder so that scons can build the whole tree despite not knowing the number of processes when scons is invoked. 

The example behaves correctly when intermediate files are deleted. 

```python
def PartMakerFunc(target, source, env):
#a builder that makes a result requiring a number of subsequent operations not known when scons is called
        targets = ["%d.out" % i for i in range(3)]
        open(target[0].get_path(),'w').write('\n'.join(targets))

def DynamicFunc(target, source, env):
#a builder that depends on a variable number of sources not known when scons is called
        sourceFiles = [f for f in source[0].get_text_contents().split('\n') if len(f)]

        f = open(target[0].get_path(),'w')
        for sf in sourceFiles:
                f.writelines(open(sf).readlines() + ["\n\n"])
        f.close()

def DynamicScannerFunc(node,env,path):
#a scanner that can scan the variable results of PartMaker identifying it's parts
#and performing an operation on each, in this case a simple copy
        sourceFiles = [f for f in node.get_text_contents().split('\n') if len(f)]
        result = []
        for f in sourceFiles:
                env.Command(f,node,Copy("$TARGET","$SOURCE"))
                result.append(env.File(f))
        return result


env = Environment()

#make the builders
env['BUILDERS']['Dynamic'] = Builder(action=Action(DynamicFunc),source_scanner=Scanner(DynamicScannerFunc))
env['BUILDERS']['PartMaker'] = Builder(action=Action(PartMakerFunc))

#Create a variable number of parts
env.PartMaker("parts.txt","x.txt")
#Process that variable number of parts, using a operation for each process and an operation dependant on each part process
env.Dynamic("result.txt","parts.txt")
#Perform an operation that depends on the result
env.Command("final.txt","result.txt",Copy("$TARGET","$SOURCE"))
```
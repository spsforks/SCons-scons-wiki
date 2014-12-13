
Our project uses RPC protocol and "rpcgen" utility to generate .c and .h sources from RPC protocol source files (.x extension). 

The problem with "rpcgen" utility is how it generates the "#include" statements. Namely, "rpcgen" will pick include path from its source file (.x) path. THerefore, i've wrote several actions, which does directory change, .x -> [.c|.h] code generation with "rpcgen" and then change directory back: 


```python
#!python 
def rpc_xdr_action( target, source, env ):
        source_dir  = os.path.dirname( str(source[0]) )
        source_file = os.path.basename( str(source[0]) )

        target_file = os.path.abspath( str(target[0]) )

        cwd = os.getcwd()

        os.chdir( source_dir )
        os.system( "rpcgen -c -o " + target_file + " " + source_file )
        os.chdir( cwd )

def rpc_client_action( target, source, env ):
        source_dir  = os.path.dirname( str(source[0]) )
        source_file = os.path.basename( str(source[0]) )

        target_file = os.path.abspath( str(target[0]) )

        cwd = os.getcwd()

        os.chdir( source_dir )
        os.system( "rpcgen -l -o " + target_file + " " + source_file )
        os.chdir( cwd )

def rpc_header_action( target, source, env ):
        source_dir  = os.path.dirname( str(source[0]) )
        source_file = os.path.basename( str(source[0]) )

        target_file = os.path.abspath( str(target[0]) )

        cwd = os.getcwd()

        os.chdir( source_dir )
        os.system( "rpcgen -h -o " + target_file + " " + source_file )
        os.chdir( cwd )


rpcxdr = Builder( action = rpc_xdr_action,
                  suffix = ".c",
                  src_suffix = ".x" )

env.Append(BUILDERS = {'RPCXDRBuilder' : rpcxdr})

rpcclnt = Builder( action = rpc_client_action,
                   suffix = ".c",
                   src_suffix = ".x" )

env.Append(BUILDERS = {'RPCCLNTBuilder' : rpcclnt})

rpchdr = Builder( action = rpc_header_action,
                  suffix = ".h",
                  src_suffix = ".x" )

env.Append(BUILDERS = {'RPCHDRBuilder' : rpchdr})
```
Request1: How to actually use the RPC builders. 

Request2: Please include an rpcgen tool in the standarc scons distribution. 

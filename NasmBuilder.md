
**IMPORTANT NOTE: OUTDATED 

               * Recent versions of scons (>=0.08) know about nasm, so it is very likely that this item is not useful for nasm anymore However, the code can be applied to other tools** 
Here is an example of a nasm files builder ([nasm](http://octium.net/nasm/?page=home) is the netwide assembler): 

` nasm_builder = Builder(name='Nasm', action='nasm -f elf -o $TARGET $SOURCE', src_suffix='.nasm') ` ` nasm_env = Environment(BUILDERS = [nasm_builder]) # BUILDERS now takes a dictionary, not an array, this must be outdated` ` nasm_files = 'unix/snapvector unix/ftol' ` ` nasm_objs = [ nasm_env.Nasm(target=x+'.o', source=x+'.nasm') for x in nasm_files.split() ] ` 

... 

` env.Program(target='spam', source = source_list + nasm_objs)` 

This was inspired by [this thread on scons-users](http://sourceforge.net/mailarchive/message.php?msg_id=1178608) 

The construction of nasm_objs requires Python 2.0 or newer. 

You can also note that instead of doing 

`nasm_files = [ 'unix/snapvector', 'unix/ftol' ] ` 

I did 

`nasm_files = 'unix/snapvector unix/ftol' ` `nasm_list = nasm_files.split()` 

that's just a handy trick when the lists of files are pretty long to write 

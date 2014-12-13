

## Rationale

Qt's uic tool has the ability to embed binary images into a c++ source file. Trolltech call this an 'image collection'. While porting to scons the build system of a project that used this uic feature I developed a quick and dirty builder to do the job. I hope someone finds this useful. 


## The Builder


```txt
def embed_images( target, source, env ) :
        output_file_str = str(target[0])
        input_files = [ str(src_item) for src_item in source ]
        input_files_str = ' '.join( input_files )
        cmd_str = '%s -embed %s %s -o %s'%(env['QT_UIC'], env['project'], input_files_str, output_file_str)

        os.system( cmd_str )

def embed_images_message( target, source, env ) :
        print "Embedding images into", str(target[0])
        for item in source :
                print "\t", str(item), "..."

bld = Builder( action = Action(embed_images, embed_images_message),
                                suffix = '.cxx',
                                src_suffix = '' )
```

### Notes

Note that the builder function relies on two variables being set in the current environment: QT_UIC (the location of the uic tool) and 'project'. 'project' should have the same value you used when using uic in your original Makefile, as explained on uic manpage: 
```txt
       Generate image collection:
            uic  [options] -embed <project> <image1> <image2> <image3> ...
               <project>:       project name
               <image[1..n]>:   image files
```
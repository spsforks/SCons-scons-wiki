

# Bash Completion for SCons

Bash completion makes using SCons much easier:  hitting tab after an incomplete word will present a list of possible options if there is more than one completion or complete the rest of the word if there is only one completion.  Completion is context sensitive, if there is a - at the beginning of the word then only command line options will be completed, if there is no - at the beginning of the word then SCons will be run in silent, dry-run, debug mode in order to ascertain what possible targets are available. 

To use this script you can: 

1. Append this to your personal Bash completion configuration, usually ~/.bash_completion. 
1. Add this file inthe directory /etc/bash_completion.d (if you have super-user privileges. 
1. Create a personal ~/bash_completion.d directory, put the file in there and then ensure you have appropriate code in ~/.bash_completion.  I have the code:```txt
# -*- mode:shell-script -*-
for file in bash_completion.d/*
do
    [[ ${file##*/} != @(*~|*.bak|*.swp|\#*\#|*.dpkg*|.rpm*) ]] &&
        [ \( -f $file -o -h $file \) -a -r $file ] &&
        . $file
done
```
My webpage about this is at [here](http://www.russel.org.uk/sconsBashCompletion.html). If you see any problems with this script do email [me](mailto:russel@russel.org.uk). 

Russel Winder, 2010-04-22 16:24+01:00
```txt
# -*- mode:shell-script -*-

# Programmable completion for the scons command under bash.

# This file draws heavily on the rake and subversion files that come as standard with Bash 3.

#  Author : Russel Winder
#  Version : 2008-07-19T18:36:29+01:00
#  Licence : GPL

_scons()
{
    local cur prev sconsf i

    COMPREPLY=()
    cur=${COMP_WORDS[COMP_CWORD]}
    prev=${COMP_WORDS[COMP_CWORD-1]}
    sconsf="SConstruct"

    if [[ "$prev" == "-f" ]]; then
        _filedir
        return 0
    fi

    if [[ "$cur" == *=* ]]; then
        prev=${cur/=*/}
        cur=${cur/*=/}
        if [[ "$prev" == "--file=" || "$prev" == "--makefile=" || "$prev" == "--sconstruct=" ]]; then
            _filedir -o nospace
            return 0
        fi
    fi

    if [[ "$cur" == -* ]]; then
        COMPREPLY=( $( compgen -W '-b -m -S -t --no-keep-going --stop --touch\
            -c --clean --remove -C '--directory='\
            --cache-disable --no-cache --cache-force --cache-populate --cache-show\
            '--config=' -d -D '--debug=' '--diskcheck=' '--duplicate='\
           -f '--file=' '--makefile=' '--sconstruct='\
           -h --help -H --help-options -i --ignore-errors\
           -I '--include=' --implicit-cache --implicit-deps-changed --implicit-deps-unchanged\
           -j '--jobs=' -l --keepgoing '--max-drift='\
           -n --no-exec --just-print --dry-run --recon\
           '--profile=' -q --question -Q --random -s --silent --quiet\
           '--taskmastertrace=' '--tree=' -u --up --search-up -u -v --version\
           '--warn=' '--warning=' -Y '--repository=''\
            -- $cur ))
    else

        for (( i=0; i < ${#COMP_WORDS[@]}; i++)); do
            case "${COMP_WORDS[i]}" in
            -f)
                eval sconsf=${COMP_WORDS[i+1]}
                break
                ;;
            --file=*|--makefile=* | --sconstruct=*)
                eval sconsf=${COMP_WORDS[i]/*=/}
                break
                ;;
            esac
        done

        [ ! -f $sconsf ] && return 0

        COMPREPLY=( $( scons -s -n -f "$sconsf" --tree=all . | \
            awk -F '+' '{ print substr ( $2 , 2 , length ( $2 ) - 1 ) }' | \
            command grep "^$cur" ))

    fi
}
complete -F _scons $filenames scons
```
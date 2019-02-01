#!/usr/bin/gawk
BEGIN{
    f=""
}
{
    if(f != FILENAME){
        f=FILENAME;
        print "reading",f
    } 
    if(match($0, /from .* import (.*)/,arr)&&!match($0, /Behavior/)){
        print "\t",arr[1];
        }
}

#In command line (for now)
#gawk 'BEGIN{f=""}{if(f != FILENAME){f=FILENAME; print "reading",f} if(match($0, /from .* import (.*)/,arr)){print "\t",arr[1];}}' behaviors/behavior*/src/behavior*/*.py > regexes/outputAwkTest.txt

#For use count of each 
#gawk 'BEGIN{f=""}{if(match($0, /from .* import (.*)/,arr)){print "\t",arr[1];}}' behaviors/behavior*/src/behavior*/*.py|sort|uniq -c|sort -n > regexes/outputUniq.txt


# ---
# UNUSED (KEEP UNTIL ANSWER FOUND)
# ---


#BEGIN {
#    f="";
#    regex = "from (?!flexbe_core).* import (.*)";
#}
#{
#    if(f != FILENAME){
#    f=FILENAME; print "reading",f
#    }
#    if (match($0,regex)) {
#        capture = substr($0,RSTART,RLENGTH);
#    }
#    print capture;
#}   
#
#Filenames
#~/flexbe_behaviors/behaviors/behavior_*


##!/usr/bin/env bash
#filename="$1";
#re="from (?!flexbe_core).* import (.*)\n";
#while read -r line;
#do
#	name=$line;
#	if [[$name=~ $re]]; then
#		echo ${BASH_REMATCH[1]};
#	fi
#done < "$filename"

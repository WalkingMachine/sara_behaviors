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
END{

}

#In command line (for now)
#gawk -f regexes/getDependenciesState.gawk  behaviors/behavior*/src/behavior*/*.py > regexes/outputAwkTest.txt

#For no-underscores (_)
#gawk -f regexes/getDependenciesState.gawk  behaviors/behavior*/src/behavior*/*.py| sed "s/_//" > regexes/outputSedTest.txt

#For use count of each 
#gawk 'BEGIN{f=""}{if(match($0, /from .* import (.*)/,arr)){print "\t",arr[1];}}' behaviors/behavior*/src/behavior*/*.py|sort|uniq -c|sort -n > regexes/outputUniq.txt

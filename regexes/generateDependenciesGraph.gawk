#!/usr/bin/gawk

# To generate with sorted entries
# gawk -f regexes/generateDependenciesGraph.gawk  behaviors/behavior_action_*/src/behavior_*/*.py&& sort -u regexes/graphs/dependenceGraph.plantuml

function basename(file) {
    sub(".*/", "", file);
    sub(".py","", file);
    sub("_?((sm)|(SM))","", file);
    return file;
}
function writeF(str){

    sub("_?((sm)|(SM))","", str);
    return system("echo \""str"\">>regexes/graphs/dependenceGraph.plantuml")
}

BEGIN{
    f=""
    umlFileName="regexes/graphs/dependenceGraph";
    file=umlFileName".plantuml";
    system("echo \"\" >"file);
    # system("echo \"@startuml\n \" >"file);
}
{
    if(f != FILENAME){
        f=FILENAME;
        print "reading",f
        class = basename(FILENAME);
    #NeedTo Ignore case and remove "_"
#    writeF("node" class"\n")
    }
    if(match($0, /from .* import (.*)/,arr)&&!match($0, /Behavior/)){
        print "\t",arr[1];
        writeF(arr[1]" -> "class"");
    }
}
END{
#    system("sort -u "file" >"file);
#    system("echo '@startuml\n node SaraSay\n' | cat - "file" > temp && mv temp todo.txt")
#    system("sed -i '1s/^/\@startuml\n node SaraSay\n/' "file);
#    system("cat regexes/graphs/dependenceGraph.plantuml"); 
#    system("echo '@startuml\n node SaraSay' >/tmp/tempUml.txt");
#    system("cat regexes/graphs/dependenceGraph.plantuml >>/tmp/tempUml.txt");
#    system("awk 'BEGIN{print \\\"@startuml\n node SaraSay\\\"}{print}' "file" > "file);
#    system("cp /tmp/tempUml.txt "file)
    # writeF("@enduml");
    # system("sort "file" > "file);
    # system("plantuml -tsvg "file);
    # system("eog "umlFileName".svg");
}

#In command line (for now)
#gawk -f regexes/getDependenciesState.gawk  behaviors/behavior*/src/behavior*/*.py > regexes/outputAwkTest.txt

#For no-underscores (_)
#gawk -f regexes/getDependenciesState.gawk  behaviors/behavior*/src/behavior*/*.py| sed "s/_//" > regexes/outputSedTest.txt

#For use count of each 
#gawk 'BEGIN{f=""}{if(match($0, /from .* import (.*)/,arr)){print "\t",arr[1];}}' behaviors/behavior*/src/behavior*/*.py|sort|uniq -c|sort -n > regexes/outputUniq.txt

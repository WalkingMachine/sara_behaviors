NR==1{
    lowerCased = tolower($1)
    print "\
<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n    \
\n\
<behavior name=\""$1"\">\n\
\n\
    <executable package_path=\"sara_flexbe_behaviors."lowerCased"_sm\" class=\""$0"SM\" />\n";
}

NR==2{
    date=strftime("%a %b %d %Y");
    print"\
    <tagstring>"$0"</tagstring>\n\
    <author>Raphaël Duchaîne</author>\n\
    <date>"date"</date>\n";
}

NR==3{
    print"\
    <description>\n\
    "$0"\n\
    </description>\n\
\n\
\n\
    <!-- Contained Behaviors -->\n\
\n\
    <!-- Available Parameters -->\n\
\n\
</behavior>\n";
}

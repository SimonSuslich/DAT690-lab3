Lab 3 peer review group 111
Reviewing group number: 125
Submitting group number: 111

Section 1: Core functionality
Does the application run? 
    yes
Does the application display the complete map of tram lines? 
    yes
Is it possible to query shortest path between any two points? 
    yes
Does the application deal with changes correctly? 
    Yes, displays along with path
Does the application show current traffic information? 
    yes
Does the application correctly handle invalid input? 
    yes

Section 2: Code quality

Make comments on the overall code quality of the submission, including whether:
code from lab 2 has been properly reused (i.e. in an efficient way without boilerplate code)
    
    Yes, no visible repetition boiler plate code.

the dijkstra() function has been implemented and used as intended: there is just one definition of the function itself, and different distances are obtained by just changing the cost function
    
    Yes, just one definition of dijkstra and upon calling it in shortest_path in tramviz.py, it uses the new specialized cost functions specialized_transition_time and specialized_geo_distance.

You may add any other comments about code quality you wish, for example suggestions for code optimization and good practices of object-oriented programming.
    
    Might not be the most efficient way to loop through all paths to find the bestt, takes a little while to load. Otherwise good.

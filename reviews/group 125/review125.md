Group 125

Section 1: Core functionality
Does the application run? (yes/no)
    Yes
Does the application display the complete map of tram lines? (yes/no)
    Yes
Is it possible to query shortest path between any two points? (yes/no)
    Yes
Does the application deal with changes correctly? (yes/no)
    Yes
Does the application show current traffic information? (yes/no)
    Yes
Does the application correctly handle invalid input? (yes/no)
    Yes

Section 2: Code quality
Make comments on the overall code quality of the submission, including whether:
code from lab 2 has been properly reused (i.e. in an efficient way without boilerplate code)

    Code from lab 2 has been efficiently reused. Using WeightedGraph to display specialized tram graph and dijkstra to calculate distance and time.

the dijkstra() function has been implemented and used as intended: there is just one definition of the function itself, and different distances are obtained by just changing the cost function
    
    Only one instance of dijkstra and used cost functions efficiently to calculate transition time and transition distance.

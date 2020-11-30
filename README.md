# pythonProject
this is for 95888 Project

Project Draft Plan
Shaily Shah, Anna Tan, Claire Skinner, Shrivatsan Ragavan

Basic Concept: 
Create a python program that allows students to view their major core course requirements and list of electives. Also, allows students to search for a Heinz course and provide them with the course information and the prerequisites for that course. Users have the option of adding the searched course to their schedule. Once the user finishes adding all the courses they want added to their draft schedule. The program will summarize the courses added by the student to their schedule.

Overall objective:
View user’s core courses and list of electives for their major. Create a searchable database that contains all Heinz graduate level courses and allows the user to view the description and the prerequisites for a particular course. Create a schedule for the user depending on what courses the user wants to add to the schedule. 

Basic Use Cases: 
Ask the user for their major. Provide an output of the core classes and list of electives for the user’s major. The user is prompted to enter a word or course ID. The input is searched through the dictionary and the program outputs the course description, its prerequisites, and units. The user is prompted if they want to add the searched course to their schedule after every search. The user keeps entering a word/course ID until it quits the loop. Once the user quits the loop, the program will output a schedule based on the courses chosen by the user. 

Data Sources
API: Heinz api - course catalog and the courses description/prerequisites; https://api.heinz.cmu.edu/courses_api/course_list/ 
Data Table: grab list of electives according to the user’s major
MSPPM -https://www.heinz.cmu.edu/heinz-shared/_files/img/student-handbooks/msppm-2020-2021-student-handbook.pdf
MISM - https://www.heinz.cmu.edu/heinz-shared/_files/img/student-handbooks/mism-2019-2020-student-handbook.pdf

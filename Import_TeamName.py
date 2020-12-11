#Import TeamName: Shrivatsan Ragavan, Shaily Shah, Claire Skinner, Anna Tan

#Main program

import requests
from bs4 import BeautifulSoup
import sys
import time
from lxml import html
import PyPDF2
import urllib.request
import pandas as pd
import re

"""
Displays list of majors for user to choose from (checks for valid number)
"""
def grabNumber():
    print('Majors')
    print('-'*40)
    programs=['Information Systems Management (MISM)','Business Intelligence & Data Analytics (BIDA)','Public Policy & Management (MSPPM)','Public Policy & Data Analytics (MSPPM-DA)']
    for i in range(len(programs)):
        print('{:<3}{:<20}'.format(i+1,programs[i]))
    major=-1
    #get major choice
    while major not in range(1,len(programs)+1):
        print('\nType an integer from 1 to %d'%len(programs))
        try:
            major=int(input('Type your major (in number): '))
        except Exception as e:
            print('Error: Wrong input. Please type an integer')
    return major

"""
Given the users choice of major, print major core courses
"""
def coreClasses(major):
    mismCoreClasses = list()
    mismBidaCoreClasses = list()
    msppmCoreClasses = list()
    msppmDACoreClasses = list()
    #MISM
    if(major == 1):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/information-systems-management-master/12-month')
        soup = BeautifulSoup(page.content, 'html.parser')
        mismCore = soup.find(id='825899-accordion')
        coreCourses = mismCore.find(class_= 'user-markup')
        count = 0
        #fix weird char
        for classes in coreCourses.find_all('li'):
            mismCoreClasses.append(classes.text.replace('\xa0', ' '))
        #display
        for course in mismCoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return mismCoreClasses    
    #MISM-BIDA
    if(major == 2):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/information-systems-management-master/bida-12month')
        soup = BeautifulSoup(page.content, 'html.parser')
        mismBidaCore = soup.find(id='99728-accordion')
        coreCourses = mismBidaCore.find(class_= 'user-markup')
        count = 0
        #fix weird char
        for classes in coreCourses.find_all('li'):
            mismBidaCoreClasses.append(classes.text.replace('\xa0', ' '))
        #display
        for course in mismBidaCoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return mismBidaCoreClasses    
    #MSPPM
    if(major == 3):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/public-policy-management-master/pittsburgh-two-year')
        soup = BeautifulSoup(page.content, 'html.parser')
        msppmCore = soup.find(id='675743-accordion')
        coreCourses = msppmCore.find(class_= 'user-markup')
        count = 0
        #fix weird char
        for classes in coreCourses.find_all('li'):
            msppmCoreClasses.append(classes.text.replace('\xa0', ' '))
        #display
        for course in msppmCoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return msppmCoreClasses    
    #MSPPM-DA
    if(major == 4):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/public-policy-management-master/data-analytics')
        soup = BeautifulSoup(page.content, 'html.parser')
        msppmDACore = soup.find(id='43546-accordion')
        coreCourses = msppmDACore.find(class_= 'user-markup')
        count = 0
        #fix weird char
        for classes in coreCourses.find_all('li'):
            msppmDACoreClasses.append(classes.text.replace('\xa0', ' '))
        #display
        for course in msppmDACoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return msppmDACoreClasses


"""
Read the text file generated from make_dict.py to a dictionary
"""  
def read_dict():
    course_dict={}
    #check if have textfile
    try:
        f=open('course_dict.txt')
    except Exception as e:
        print('Haven\'t generated local dictionary')
        try:
            import make_dict.py #import if don't have textfile
        except Exception as e:
            pass
        f=open('course_dict.txt')
    #create dict    
    lines=f.readlines()
    for line in lines:
        line=line.split('=')
        val=line[1]
        val=val.strip('{')
        val=val.strip('}')
        val=val.split('$')
        vals={}
        for item in val:
            item=item.split(':')
            if len(item)>1:
                vals[item[0]]=item[1]
                if item[0]=='Units':
                    vals[item[0]]=int(vals[item[0]])
        course_dict[line[0]]=vals
    return course_dict


"""
Return list of MSPPM electives
"""    
def electiveMsppm():
    #Download pdf file from url
    electives=pd.DataFrame({'Code':[],'Course':[],'Units':[]})
    url='https://www.heinz.cmu.edu/heinz-shared/_files/img/student-handbooks/msppm-2020-2021-student-handbook.pdf'
    urllib.request.urlretrieve(url,url.split('/')[-1])

    pdfFileObj=open(url.split('/')[-1],'rb')
    pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
    
    #Parsing the pages of the pdf with the electives and using RegEx to extract elective info
    for j in range(7,9):
        pageObj=pdfReader.getPage(j)
        pagetext=pageObj.extractText().replace("\n"," ")
        
        #Creating separate lists for 6 and 12 unit electives
        six_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+, 6 units',pagetext)
        twelve_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+, 12 units',pagetext)
        
        #Taking the contents of the lists and populating the final dataframe
        for i in six_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-9],'Units':6},ignore_index=True)

        for i in twelve_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-10],'Units':12},ignore_index=True)
    return electives

"""
Return list of MSIM electives
"""  
def electiveMism():
    #Download pdf file from url
    electives=pd.DataFrame({'Code':[],'Course':[],'Units':[]})
    url='https://www.heinz.cmu.edu/heinz-shared/_files/img/student-handbooks/mism-2020-2021-student-handbook.pdf'
    urllib.request.urlretrieve(url,url.split('/')[-1])

    pdfFileObj=open(url.split('/')[-1],'rb')
    pdfReader=PyPDF2.PdfFileReader(pdfFileObj)

    #Parsing the pages of the pdf with the electives and using RegEx to extract elective 
    for j in range(4,6):
        pageObj=pdfReader.getPage(j)
        pagetext=pageObj.extractText().replace("\n"," ")
        
        #Creating separate lists for 6 and 12 unit electives
        six_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+ 6 units',pagetext)
        twelve_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+ 12 units',pagetext)

        #Taking the contents of the lists and populating the final dataframe
        for i in six_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-8].strip(),'Units':6},ignore_index=True)

        for i in twelve_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-9].strip(),'Units':12},ignore_index=True)
    return electives

"""
Course search funct (takes in course number and course dictionary and
outputs the title, units, and description)
""" 
def search(course_dict,course_num):
    query = course_dict[course_num]
    print('Course Title:', query['Title'])
    print('Course Number:', course_num)
    print('Units:',query['Units'])
    print('Description:',query['Description'])

"""
Driver function for adding/dropping courses - takes in course dictionary, takes
user through process of adding/dropping
""" 
def addDropCourse(course_dict,maxcred=54):
    units=0
    courses=[]
    value =input('Would you like to Add or Drop (A/D) a course, type quit when finished: ')
    while value.lower()!='quit':
        #adding
        if value.upper()=='A' or value.upper() == 'ADD':
            add = str(input('\nSearch for a course number to add XX-XXX (type DONE when finished): '))
            while add.upper()!='DONE' and units<=maxcred:
                #check if quit
                if add.upper()=='DONE':
                    break
                #check valid course
                elif add not in course_dict.keys():
                    print('Invalid course number! Try again')
                #check under max credits
                elif units+course_dict[add]['Units']>maxcred:
                    print('Adding this course would exceed your maximum units.')
                    break
                #check if already added
                elif add in courses:
                    print('You already have this class on your schedule. ')
                #display course details and ask if want to add
                else:
                    search(course_dict, add)
                    adding=input('\nDo you want to add this class to your schedule? Y/N: ')
                    while adding.upper() not in ['Y','N']:
                            print('Invalid input - Please try again')
                            adding = str(input('\nDo you want to add this class from your schedule? Y/N: '))
                    #if Y add, if N do nothing
                    if adding.upper()=='Y' or 'Y' in adding.upper():
                        units+=course_dict[add]['Units']
                        courses.append(add)
                        print('Course added successfully')
                        print('*Current courses in planned schedule: '+str(courses))
                        print('*Current units in planned schedule: '+str(units)+'/%d'%maxcred)

                add = str(input('\nSearch for another course number to add XX-XXX (type DONE when finished): '))
        #dropping
        if value.upper()=='D' or value.upper() == 'DROP':
            print('*Current courses in planned schedule: '+str(courses))
            print('*Current units in planned schedule: '+str(units)+'/%d'%maxcred)
            #check if courses to drop
            if len(courses) != 0:
                drop = str(input('\nSearch for a course number to drop XX-XXX (type DONE when finished): '))
                while drop.upper()!='DONE':
                    #check if quit
                    if drop.upper()=='DONE':
                        break
                    #check if valid course to drop
                    elif drop not in course_dict.keys():
                        print('Invalid course number! Try again')
                    #check if really want to drop
                    elif drop in courses:
                        dropping = str(input('Do you want to drop this class from your schedule? Y/N: '))
                        while dropping.upper() not in ['Y','N']:
                            print('Invalid input - Please try again')
                            dropping = str(input('Do you want to drop this class from your schedule? Y/N: '))
                        #if Y drop, if N do nothing
                        if dropping.upper()=='Y' or 'Y' in dropping.upper():
                            courses.remove(drop)
                            print('Course dropped successfully')
                            units-=course_dict[drop]['Units']
                            print('*Current courses in planned schedule: '+str(courses))
                            print('*Current units in planned schedule: '+str(units)+'/%d'%maxcred)
                    #if course not in schedule
                    else:
                        print('You don\'t have this class in your schedule.')
                    drop = str(input('\nSearch for a course number to drop XX-XXX (type DONE when finished): '))
            else:
                print('There are no courses in your schedule to drop.')
        value = input('Would you like to Add or Drop (A/D) a course, type quit when finished: ')

    courses.sort()
    return courses,units,maxcred


def main():
    #get major
    major = grabNumber()
    
    #display major core and electives
    print('\nMajor Core Classes:')
    print('-------------------')
    coreClasses(major)
    print()
    print('Major Elective Classes:')
    print('-----------------------')
    if (major == 1 or major == 2):
        elective_list=electiveMism()
        print(elective_list)
    if (major == 3 or major == 4):
        elective_list=electiveMsppm()
        print(elective_list)

    ##create course dictionary 
    course_dict=read_dict()

    #add/drop courses
    schedule,units,maxcred = addDropCourse(course_dict)
            
    #create schedule file
    time.sleep(0.5)
    print('generating schedule')
    for i in range(10):
        time.sleep(0.02)
        print('.')
        
    with open('schedule.csv','w') as f:
        f.write('Course Number,Title,Units\n')
        for c in schedule:
            d=course_dict[c]
            f.write('%s,%s,%d \n'%(c,d['Title'],d['Units']))
        f.write(' ,total units, %d/%d\n'%(units,maxcred))

if __name__ == '__main__':
    main()
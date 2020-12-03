#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 17:01:34 2020

@name: shaily shah
@andrewID: shailys
"""
import requests
from bs4 import BeautifulSoup
import sys
import time
from lxml import html
import PyPDF2
import urllib.request
import pandas as pd
import re


def grabNumber():
    print('Majors')
    print('-'*40)
    programs=['Information Systems Management (MISM)','Business Intelligence & Data Analytics (BIDA)','Public Policy & Management (MSPPM)','Public Policy & Data Analytics (MSPPM-DA)']
    for i in range(len(programs)):
        print('{:<3}{:<20}'.format(i+1,programs[i]))
    major=-1
    while major not in range(1,len(programs)+1):
        print('\nType an integer from 1 to %d'%len(programs))
        try:
            major=int(input('Type your major (in number): '))
        except Exception as e:
            print('Error: Wrong input. Please type an integer')
    return major


def coreClasses(major):
    mismCoreClasses = list()
    mismBidaCoreClasses = list()
    msppmCoreClasses = list()
    msppmDACoreClasses = list()
    if(major == 1):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/information-systems-management-master/12-month')
        soup = BeautifulSoup(page.content, 'html.parser')
        mismCore = soup.find(id='825899-accordion')
        coreCourses = mismCore.find(class_= 'user-markup')
        count = 0
        for classes in coreCourses.find_all('li'):
            mismCoreClasses.append(classes.text.replace('\xa0', ' '))
        for course in mismCoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return mismCoreClasses
    if(major == 2):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/information-systems-management-master/bida-12month')
        soup = BeautifulSoup(page.content, 'html.parser')
        mismBidaCore = soup.find(id='99728-accordion')
        coreCourses = mismBidaCore.find(class_= 'user-markup')
        count = 0
        for classes in coreCourses.find_all('li'):
            mismBidaCoreClasses.append(classes.text.replace('\xa0', ' '))
        for course in mismBidaCoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return mismBidaCoreClasses
    if(major == 3):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/public-policy-management-master/pittsburgh-two-year')
        soup = BeautifulSoup(page.content, 'html.parser')
        msppmCore = soup.find(id='675743-accordion')
        coreCourses = msppmCore.find(class_= 'user-markup')
        count = 0
        for classes in coreCourses.find_all('li'):
            msppmCoreClasses.append(classes.text.replace('\xa0', ' '))
        for course in msppmCoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return msppmCoreClasses
    if(major == 4):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/public-policy-management-master/data-analytics')
        soup = BeautifulSoup(page.content, 'html.parser')
        msppmDACore = soup.find(id='43546-accordion')
        coreCourses = msppmDACore.find(class_= 'user-markup')
        count = 0
        for classes in coreCourses.find_all('li'):
            msppmDACoreClasses.append(classes.text.replace('\xa0', ' '))
        for course in msppmDACoreClasses:
            count += 1
            print('%2d. %s' % (count, course))
        return msppmDACoreClasses


def read_dict():
    course_dict={}
    f=open('course_dict.txt')
    for line in f.readlines():
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


def electiveMsppm():

    """
    Snippet to download pdf file from url
    """
    electives=pd.DataFrame({'Code':[],'Course':[],'Units':[]})
    url='https://www.heinz.cmu.edu/heinz-shared/_files/img/student-handbooks/msppm-2020-2021-student-handbook.pdf'
    urllib.request.urlretrieve(url,url.split('/')[-1])

    pdfFileObj=open(url.split('/')[-1],'rb')
    pdfReader=PyPDF2.PdfFileReader(pdfFileObj)

    #print(pdfReader.numPages)
    """
    Parsing the pages of the pdf with the electives and using RegEx to extract elective info
    """

    for j in range(7,9):
        pageObj=pdfReader.getPage(j)

        pagetext=pageObj.extractText().replace("\n"," ")

        """
        Creating separate lists for 6 and 12 unit electives
        """
        six_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+, 6 units',pagetext)
        twelve_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+, 12 units',pagetext)

        """
        Taking the contents of the lists and populating the final dataframe
        """
        for i in six_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-9],'Units':6},ignore_index=True)

        for i in twelve_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-10],'Units':12},ignore_index=True)
    return electives

def electiveMism():

    """
    Snippet to download pdf file from url
    """
    electives=pd.DataFrame({'Code':[],'Course':[],'Units':[]})
    url='https://www.heinz.cmu.edu/heinz-shared/_files/img/student-handbooks/mism-2020-2021-student-handbook.pdf'
    urllib.request.urlretrieve(url,url.split('/')[-1])

    pdfFileObj=open(url.split('/')[-1],'rb')
    pdfReader=PyPDF2.PdfFileReader(pdfFileObj)

    #print(pdfReader.numPages)
    """
    Parsing the pages of the pdf with the electives and using RegEx to extract elective info
    """
    for j in range(4,6):
        pageObj=pdfReader.getPage(j)

        pagetext=pageObj.extractText().replace("\n"," ")

        """
        Creating separate lists for 6 and 12 unit electives
        """

        six_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+ 6 units',pagetext)
        twelve_unit_Master=re.findall('9[0-9] - [0-9][0-9][0-9] \D+ 12 units',pagetext)

        """
        Taking the contents of the lists and populating the final dataframe
        """
        for i in six_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-8].strip(),'Units':6},ignore_index=True)

        for i in twelve_unit_Master:
            code=str(re.findall('9[0-9] - [0-9][0-9][0-9]',i)).replace(" ","")
            electives=electives.append({'Code': code[2:-2], 'Course':i[9:-9].strip(),'Units':12},ignore_index=True)
    return electives


#course search funct (takes in course number and course dictionary and
# outputs the title, units, and description)
def search(course_dict,course_num):
    query = course_dict[course_num]
    print('Course Title:', query['Title'])
    print('Course Number:', course_num)
    print('Units:',query['Units'])
    print('Description:',query['Description'])


def addDropCourse(course_dict,maxcred=54):
    units=0
    courses=[]
    add=input('Would you like to Add or Drop (A/D) a course, type quit when finished: ')
    while add.lower()!='quit':
        if add.upper()=='A' or 'A' in add.upper():
            while add.upper()!='DONE' and units<=maxcred:
                add = str(input('\nSearch for a course number to add XX-XXX (type DONE when finished): '))
                if add.upper()=='DONE':
                    break
                elif add not in course_dict.keys():
                    print('Invalid course number! Try again')
                elif add in courses:
                    print('current courses: '+str(courses))
                    print('You already have this class on your schedule. ')
                    drop=str(input('\nDo you want to drop this class? '))
                    if drop.upper()=='Y' or 'Y' in drop.upper():
                        courses.remove(add)
                elif units+course_dict[add]['Units']>maxcred:
                    print('Adding this course would exceed your maximum units.')
                else:
                    search(course_dict, add)
                    adding=input('\nDo you want to add this class to your schedule? Y/N ')
                    while adding.upper() not in ['Y','N']:
                        if adding.upper()=='Y':
                            units+=course_dict[add]['Units']
                            courses.append(add)
                            print('current courses: '+str(courses))
                            print('current units: '+str(units)+'/%d'%maxcred)
                        adding=input('Do you want to add this class to your schedule? Y/N ')
                    if adding.upper()=='Y':
                        units+=course_dict[add]['Units']
                        courses.append(add)
                        print('current courses: '+str(courses))
                        print('current units: '+str(units)+'/%d'%maxcred)
        if add.upper()=='D' or 'D' in add.upper():
            print('current courses: '+str(courses))
            print('current units: '+str(units)+'/%d'%maxcred)
            while add.upper()!='DONE':
                add = str(input('\nSearch for a course number to drop XX-XXX (type DONE when finished): '))
                if add.upper()=='DONE':
                    break
                elif add not in course_dict.keys():
                    print('Invalid course number! Try again')
                elif add in courses:
                    drop=str(input('\nDo you want to drop this class from your schedule? '))
                    if drop.upper()=='Y' or 'Y' in drop.upper():
                        courses.remove(add)
                    print('current courses: '+str(courses))
                    print('current units: '+str(units)+'/%d'%maxcred)
                else:
                    print('You don\'t have this class on your schedule.')
        add=input('Would you like to Add or Drop (A/D) a course, type quit when finished: ')


    courses.sort()
    return courses,units,maxcred




def main():
    major = grabNumber()
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

    ##creates dictionary with api calling 
    course_dict=read_dict()
    

    #creates schedule by calling addcourse function
    schedule,units,maxcred = addDropCourse(course_dict)
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

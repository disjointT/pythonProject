import sys
import requests
from bs4 import BeautifulSoup


##########************************************
def program():
    link='https://www.heinz.cmu.edu/programs/'
    page =\
    requests.get(link)
    #find programs names
    soup = BeautifulSoup(page.content, 'html.parser')
    programs1=soup.find(id="js-programs")
    programs=programs1.get_text()
    programs=programs.split('Program')
    programs=[x.split(')')[0] for x in programs]
    programs=[x for x in programs if 'Overview' not in x and '(' in x]
    programs=[x+')' for x in programs if len(x)>7]

    hyperlinks=[]
    #find links
    for program in programs:
        content=programs1.find(title=program)
        hplink='https://www.heinz.cmu.edu'+content['href']
        hyperlinks.append(hplink)
    return programs,hplink
############***********************************

def grabNumber():
    print('Majors:')
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
    print('Major: %s'%programs[major-1])
    return major

def addCourse(course_dict,maxcred=54):
    add=input('Do you wanna add a class? (Y/N): ')
    units=0
    courses=[]
    print(courses)
    if add.upper()=='Y' or 'Y' in add.upper():
        while add.upper()!='DONE' and units<=maxcred:
            add=input('\nType course number  (type DONE when finished):')
            if add.upper()=='DONE':
                break
            elif add not in course_dict.keys():
                print('Invalid course number! Try again')
            elif add in courses:
                print('current courses: '+str(courses))
                print('You already have this class on your schedule. ')
            elif units+course_dict[add]['units']>maxcred:
                print('Adding this course would exceed your maximum units.')
            else:
                units+=course_dict[add]['units']
                courses.append(add)
                print('current courses: '+str(courses))
                print('current units: '+str(units)+'/%d'%maxcred)
    courses.sort()
    return courses,units

###> Shailey's code:
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
        for classes in coreCourses.find_all('li'):
            mismCoreClasses.append(classes.text.replace('\xa0', ' '))
        print(mismCoreClasses)
        return mismCoreClasses
    if(major == 2):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/information-systems-management-master/bida-12month')
        soup = BeautifulSoup(page.content, 'html.parser')
        mismBidaCore = soup.find(id='99728-accordion')
        coreCourses = mismBidaCore.find(class_= 'user-markup')
        for classes in coreCourses.find_all('li'):
            mismBidaCoreClasses.append(classes.text.replace('\xa0', ' '))
        print(mismBidaCoreClasses)
        return mismBidaCoreClasses
    if(major == 3):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/public-policy-management-master/pittsburgh-two-year')
        soup = BeautifulSoup(page.content, 'html.parser')
        msppmCore = soup.find(id='675743-accordion')
        coreCourses = msppmCore.find(class_= 'user-markup')
        for classes in coreCourses.find_all('li'):
            msppmCoreClasses.append(classes.text.replace('\xa0', ' '))
        print(msppmCoreClasses)
        return msppmCoreClasses
    if(major == 4):
        page =\
        requests.get('https://www.heinz.cmu.edu/programs/public-policy-management-master/data-analytics')
        soup = BeautifulSoup(page.content, 'html.parser')
        msppmDACore = soup.find(id='43546-accordion')
        coreCourses = msppmDACore.find(class_= 'user-markup')
        for classes in coreCourses.find_all('li'):
            msppmDACoreClasses.append(classes.text.replace('\xa0', ' '))
        print(msppmDACoreClasses)
        return msppmDACoreClasses
   ##<<


def main():
    programs,hplink=program()
    major=grabNumber()
    print('Core:')
    core=coreClasses(major)
    #test cases
    #course_dict={'1':{'title':'abc','units':32,'description':""},'2':{'title':' df','units':22,'description':' '},'3':{'title':' d','units':2,'description':' '},'4':{'title':' d','units':12,'description':' '}}
    #addCourse(course_dict)

if __name__ == '__main__':
    main()

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


###> Shaily's code:
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

def main():
    programs,hplink=program()
    major=grabNumber()
    print('Major Core Classes:')
    print('-------------------')
    core=coreClasses(major)

if __name__ == '__main__':
    main()

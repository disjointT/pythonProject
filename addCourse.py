import sys


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

def main():
    #test cases
    course_dict={'1':{'title':'abc','units':32,'description':""},'2':{'title':' df','units':22,'description':' '},'3':{'title':' d','units':2,'description':' '},'4':{'title':' d','units':12,'description':' '}}
    addCourse(course_dict)

if __name__ == '__main__':
    main()

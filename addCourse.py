import sys
import time

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


def addCourse(course_dict,maxcred=54):
    add=input('Do you wanna add a class? (Y/N): ')
    units=0
    courses=[]
    print(courses)
    if add.upper()=='Y' or 'Y' in add.upper():
        while add.upper()!='DONE' and units<=maxcred:
            add=input('\nType course number XX-XXX (type DONE when finished):')
            if add.upper()=='DONE':
                break
            elif add not in course_dict.keys():
                print('Invalid course number! Try again')
            elif add in courses:
                print('current courses: '+str(courses))
                print('You already have this class on your schedule. ')
            elif units+course_dict[add]['Units']>maxcred:
                print('Adding this course would exceed your maximum units.')
            else:
                print(course_dict[add])
                adding=input('\nDo you want to add this class? Y/N ')
                while adding.upper() not in ['Y','N']:
                    if adding.upper()=='Y':
                        units+=course_dict[add]['Units']
                        courses.append(add)
                        print('current courses: '+str(courses))
                        print('current units: '+str(units)+'/%d'%maxcred)
                    adding=input('Do you want to add this class? Y/N ')
                if adding.upper()=='Y':
                    units+=course_dict[add]['Units']
                    courses.append(add)
                    print('current courses: '+str(courses))
                    print('current units: '+str(units)+'/%d'%maxcred)

    courses.sort()
    return courses,units,maxcred

def main():
    schedule,units,maxcred=addCourse(course_dict)
    time.sleep(0.5)
    print('generating schedule')
    for i in range(10):
        time.sleep(0.02)
        print('.')
    with open('schedule.csv','w') as f:
        f.write(' ,total units, %d/%d\n'%(units,maxcred))
        f.write('Course Number,Title,Units\n')
        for c in schedule:
            d=course_dict[c]
            f.write('%s,%s,%d \n'%(c,d['Title'],d['Units']))


if __name__ == '__main__':
    main()

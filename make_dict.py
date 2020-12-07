import requests
from lxml import html
#get course data from main list
url = 'https://api.heinz.cmu.edu/courses_api/course_list/'
print('Grabbing data from %s'%url)
page = requests.get(url)
tree = html.fromstring(page.content)

#pull out needed fields
course_numbers = tree.xpath('//*[@class="clickable-row"]/td[1]/a/text()')
course_names = tree.xpath('//*[@class="clickable-row"]/td[2]/text()')

course_units = tree.xpath('//*[@class="clickable-row"]/td[3]/text()')
course_units = list(map(int, course_units)) #make ints in case math later

#get course details using new urls
course_descr = []
counter=0
total=len(course_numbers)
for num in course_numbers:
    counter+=1
    if counter%10==0:
        print('Generating %d %% of data'%(counter/total*100))
    url = 'https://api.heinz.cmu.edu/courses_api/course_detail/' + num
    page = requests.get(url)
    tree = html.fromstring(page.content)
    whole_text = tree.xpath('//*[@id="container-fluid"]/div/div[2]/p/text()')
    #description is entry after first blank entry
    descr = whole_text[whole_text.index(' ')+1]
    #Remove weird char
    descr = descr.replace('\xa0','')
    descr = descr.replace('\r\n','')
    #add to descr list
    course_descr.append(descr)

#create searchable dictionary (keys: (name, num) & values: (units, descr))
zipped = list(zip(course_names, course_units, course_descr))
values = list(map(lambda x:{'Title': x[0], 'Units': x[1], 'Description': x[2]},
                    zipped))
course_dict = dict(zip(course_numbers,values))
with open('course_dict.txt','w') as f:
    for x in course_dict.keys():
        f.write('%s={'%x)
        vals=course_dict[x]
        for atr in vals.keys():
            val=vals[atr]
            #fix this issue on course 95-758
            if isinstance(val,str) and len(val)>3 and val[-1]==':':
                ind=val.rfind('.')
                val=val[:ind+1]
            f.write('%s:%s$'%(atr,val))
        f.write('}\n')
    print('course_dict.txt created')

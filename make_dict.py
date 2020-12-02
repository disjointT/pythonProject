import requests
from lxml import html
#get course data from main list
url = 'https://api.heinz.cmu.edu/courses_api/course_list/'
print(url)
page = requests.get(url)
tree = html.fromstring(page.content)

#pull out needed fields
course_numbers = tree.xpath('//*[@class="clickable-row"]/td[1]/a/text()')
print('yes')
course_names = tree.xpath('//*[@class="clickable-row"]/td[2]/text()')

course_units = tree.xpath('//*[@class="clickable-row"]/td[3]/text()')
course_units = list(map(int, course_units)) #make ints in case math later
print('yes')

#get course details using new urls
course_descr = []
print(len(course_numbers))
for num in course_numbers:
    print(num)
    url = 'https://api.heinz.cmu.edu/courses_api/course_detail/' + num
    page = requests.get(url)
    tree = html.fromstring(page.content)
    whole_text = tree.xpath('//*[@id="container-fluid"]/div/div[2]/p/text()')
    #description is entry after first blank entry
    descr = whole_text[whole_text.index(' ')+1]
    #Remove weird char
    descr = descr.replace('\xa0','')
    #add to descr list
    course_descr.append(descr)

print('yes')

#create searchable dictionary (keys: (name, num) & values: (units, descr))
zipped = list(zip(course_names, course_units, course_descr))
values = list(map(lambda x:{'Title': x[0], 'Units': x[1], 'Description': x[2]},
                    zipped))
course_dict = dict(zip(course_numbers,values))
with open('course_dict.txt','w') as f:
    for x in course_dict.keys():
        f.write('%s={'%x)
        vals=course_dict[x]
        for val in vals.keys():
            f.write('%s:%s$'%(val,vals[val]))
        f.write('}\n')
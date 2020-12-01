import requests
from lxml import html

#get course data from main list
url = 'https://api.heinz.cmu.edu/courses_api/course_list/'
page = requests.get(url)
tree = html.fromstring(page.content)

#pull out needed fields
course_numbers = tree.xpath('//*[@class="clickable-row"]/td[1]/a/text()')

course_names = tree.xpath('//*[@class="clickable-row"]/td[2]/text()')

course_units = tree.xpath('//*[@class="clickable-row"]/td[3]/text()')
course_units = list(map(int, course_units)) #make ints in case math later

#get course details using new urls
course_descr = []
for num in course_numbers:
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
    
#create searchable dictionary (keys: (name, num) & values: (units, descr))
zipped = list(zip(course_names, course_units, course_descr))
values = list(map(lambda x:{'Title': x[0], 'Units': x[1], 'Description': x[2]},
                    zipped))

course_dict = dict(zip(course_numbers,values))
   
#course search funct (takes in course number and course dictionary and 
# outputs the title, units, and description)
def search(course_dict,course_num):
    query = course_dict[course_num]
    print('Course Title:', query['Title'])
    print('Course Number:', course_num)
    print('Units:',query['Units'])
    print('Description:',query['Description'])

#example
#search(course_dict,'91-809')

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 16:50:39 2020

@author: Shrivatsan Ragavan
"""



def electiveMsppm():
    import PyPDF2
    import urllib.request
    import pandas as pd
    import re
    
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
    import PyPDF2
    import urllib.request
    import pandas as pd
    import re
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

def main():
   
 #  elective_list=pd.Dataframe({'Code':[],'Course':[],'Units':[]})
   choice=int(input("(1) MSPPM \n (2) MISM \n Select Program Number:"))
   if choice==1:
       elective_list=electiveMsppm()
       print(elective_list)
   elif choice==2:
       elective_list=electiveMism()
       print(elective_list)
   else:
       print("Invalid Choice")
       

if __name__=='__main__':
    main()      
   
 
            
            
                             
             
            
                             
from docx.api import Document
from flashtext import KeywordProcessor
import sys
import re

def main():
    try:
        keyword_number = int(input("Enter number of keywords: "))
    except ValueError:
        sys.exit('Not int')
    keyword_list = get_keywords(keyword_number)
    new_doc = word_document()
    formatted_doc = format(new_doc)
    exact_match_parse(formatted_doc, keyword_list)

def get_keywords(s): #creates a list of keywords for future use
    number = int(s)
    keyword_list = []
    while number > 0:
        keyword_list.append(input("Enter keyword: "))
        number-=1
    return keyword_list

def word_document(): #this takes the docx file and returns it as txt
    new_doc = open('temp.txt', 'w')
    document = Document('paysafecard.docx') #this specifically is a local file, change if you want to test with different one
    for i in document.paragraphs:
        new_doc.write(i.text + "\n")
    return 'temp.txt'
    
def format(new_doc): #this cleans up the .txt, removing html tags, punctuation, and citation numbers with regex
    with open(new_doc, 'r') as original_file, open('formatted_temp.txt', 'w') as formatted_file:
        for line in original_file.readlines():
            clean = re.compile('<.*?>')
            line = re.sub(clean,'', line)
            line = re.sub("[,.?]",'', line)
            line = re.sub("\[[0-9]\]", '', line)
            formatted_file.write(line)
    return 'formatted_temp.txt'

def exact_match_parse(formatted_file, keyword_list): #this will parse the formatted txt for exact matches
    keyword_count = {}
    formatted_document = open(formatted_file, 'r').read()
    keyword_processor = KeywordProcessor()
    for i in keyword_list:
        keyword_processor.add_keyword(i)
    kw_found = keyword_processor.extract_keywords(formatted_document)
    for i in kw_found:
        if i not in keyword_count:
            keyword_count.update({i: 1})
        elif i in keyword_count:
            keyword_count[i] += 1
    for i in keyword_count:
        print(f'Keyword "{i}" is {keyword_count[i]} times in text')

if __name__ == "__main__":
    main()


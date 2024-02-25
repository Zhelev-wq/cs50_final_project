from docx.api import Document
from flashtext import KeywordProcessor
import sys

def main():
    """try:
        keyword_number = int(input("Enter number of keywords: "))
    except ValueError:
        sys.exit('Not int')
    keyword_list = get_keywords(keyword_number)
    for i in keyword_list:
        print(f"Keyword {i['keyword']} is present {i['number']} times in the text")"""
    new_doc = word_document()
    with open('new_doc.txt', 'w') as file:
        for i in new_doc:
            file.write(i + "\n")

def get_keywords(s):
    number = int(s)
    keyword_list = []
    while number > 0:
        keyword = input("Enter keyword: ")
        keyword_list.append({'keyword': keyword, 'number': 0})
        number-=1
    return keyword_list

def word_document():
    new_doc = []
    document = Document('paysafecard.docx')
    for i in document.paragraphs:
        new_doc.append(i.text)
    return new_doc
     
def parse():
    ...

if __name__ == "__main__":
    main()


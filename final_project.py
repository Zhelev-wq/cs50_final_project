from docx.api import Document
from flashtext import KeywordProcessor
import sys

def main():
    """try:
        keyword_number = int(input("Enter number of keywords: "))
    except ValueError:
        sys.exit('Not int')
    keyword_list = get_keywords(keyword_number)"""
    new_doc = word_document()
    print(new_doc)

def get_keywords(s):
    """this function takes an int as an argument, 
    which represents the number of KW you want to enter"""
    number = int(s)
    """empty list which will hold the KW after they are input by the user"""
    keyword_list = []
    """this loop takes user input for each keyword, 
    adding them to a list in the order in which they're entered,
    after every entry the int is reduced by 1 until it reaches 0"""
    while number > 0:
        keyword_list.append(input("Enter keyword: "))
        number-=1
    """the fuction returns the list of keywords sorted into key:value pairs"""
    return keyword_list

def word_document():
    """empty list to hold paragraph elements"""
    new_doc = []
    """this loads the .docx file using the python-docx module"""
    document = Document('paysafecard.docx')
    """loop that itterates over each paragraph element, 
    coverts it to standard text,
    then adds it to the empty list"""
    for i in document.paragraphs:
        new_doc.append(i.text)
    """this returns the list of paragraphs, 
    with each paragraph being a separate list index """
    return new_doc
     
def format_and_parse(keyword_dict, new_doc):
    ...

if __name__ == "__main__":
    main()


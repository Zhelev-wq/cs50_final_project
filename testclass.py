from flashtext import KeywordProcessor
from docx import Document
from tabulate import tabulate
import sys
import re


class Keyword:
    def __init__(self, keyword, exact_match=0, partial_match=0) -> None:
        self.keyword = keyword
        self.exact_match = exact_match
        self.partial_match = partial_match
        
    def __str__(self):
        return str([self.keyword, self.exact_match, self.partial_match])
    
    def validate_argv(): #validates if the passed argument is a docx file and if the command is correct
        if len(sys.argv)>2:
            sys.exit("Too many command-line arguments")
        elif len(sys.argv)<2:
            sys.exit("Too for command-line arguments")
        elif sys.argv[1][-5:] != '.docx':
            sys.exit("File not .docx extension")
        else:
            return sys.argv[1]
    
    def get_keywords_manually(s: int): #enters a list of keywords, which are then passed to __init__
        number = int(s)
        keyword_list = []
        while number > 0:
            keyword = input("Enter keyword: ")
            keyword_list.append(keyword)
            number-=1
        return keyword_list
    
    def get_keywords_from_list(list_file): #txt file which passed and every line is extracted as a keyword
        keyword_list = []
        with open(list_file) as file:
            file = file.readlines()
            for line in file:
                keyword_list.append(line.strip())
        return keyword_list
    
    def pass_keywords_to_class(keyword_list): #this creates the variable that stores the class instances as list entries
        KW = [] 
        for keyword in keyword_list:
            KW.append(Keyword(keyword))
        return KW
    
    def word_document(doc): # this takes the docx file and returns a txt
        new_doc = open('temp.txt', 'w')
        document = Document(doc)
        for i in document.paragraphs:
            new_doc.write(i.text + "\n")
        return 'temp.txt'
    
    def format(new_doc): #this cleans up the .txt, removing html tags, punctuation, and citation numbers with regex
        with open(new_doc, 'r') as original_file, open('formatted_temp.txt', 'w') as formatted_file:
            for line in original_file.readlines():
                clean = re.compile('<.*?>')
                line = re.sub(clean,'', line)
                line = re.sub("[,.?:']",'', line)
                line = re.sub("\[[0-9]\]", '', line)
                formatted_file.write(line)
        return 'formatted_temp.txt'

    def exact_match_parse(formatted_file, KW): #
        formatted_document = open(formatted_file, 'r').read()
        keyword_processor = KeywordProcessor()
        for i in KW:
            keyword_processor.add_keyword(i.keyword)
        kw_found = keyword_processor.extract_keywords(formatted_document)
        for i in KW:
            i.exact_match += kw_found.count(i.keyword)

    def partial_match_parse(formatted_file, keyword_list, KW):
        kw_patterns = []
        for keyword in keyword_list:
            separated_kw = keyword.split(" ")
            kw_patterns.append('(?: |(?:(?: \w* )(?:\w* )?))'.join(separated_kw))
        with open(formatted_file, 'r') as file:
            file = file.read()
            for number, pattern in enumerate(kw_patterns):
                matches = re.findall(pattern, file, re.IGNORECASE)
                matches = [x.lower() for x in matches]                
                for match in matches:
                    if match in keyword_list:
                        continue
                    else:
                        KW[number].partial_match +=1

def main():
    doc_name = Keyword.validate_argv()

    while True:
        choice = int(input("1.Manual keyword entry \n2.Provide .txt file \nChoice: "))
        if choice == 1:
            keyword_list = Keyword.get_keywords_manually(int(input("How many keywords: ")))
            break
        elif choice == 2:
            keyword_list = Keyword.get_keywords_from_list(input("Enter file name: "))
            break
        else:
            continue

    KW = Keyword.pass_keywords_to_class(keyword_list)
    new_doc = Keyword.word_document(doc_name)
    formatted_doc = Keyword.format(new_doc)
    Keyword.exact_match_parse(formatted_doc, KW)
    Keyword.partial_match_parse(formatted_doc, keyword_list, KW)
    table_visualization =[['Keyword', 'Exact Matches', 'Partial Matches', 'Total Matches']]
    for i in KW:
        table_visualization.append([i.keyword, i.exact_match, i.partial_match, i.exact_match + i.partial_match])
    print(tabulate(table_visualization, headers="firstrow", tablefmt="grid"))


if __name__ == "__main__":
    main()


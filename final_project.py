from docx.api import Document
from flashtext import KeywordProcessor
import sys
import re
from tabulate import tabulate

def main():
    doc = validate_argv()
    try:
        keyword_number = int(input("Enter number of keywords: "))
    except ValueError:
        sys.exit('Not int')
    keyword_list = get_keywords(keyword_number)
    new_doc = word_document(doc)
    formatted_doc = format(new_doc)
    table_visualization = [['Keyword', 'Exact Matches', 'Partial Matches']]
    exact = exact_match_parse(formatted_doc, keyword_list) #list of dictionaries {KW:number}
    partial = partial_match_parse(formatted_doc, keyword_list) #list of partial keyword matches (number only)
    
    for count, i in enumerate(exact):
        complete_list = [i, exact[i], partial[count]]
        table_visualization.append(complete_list)
    
    print(tabulate(table_visualization, headers="firstrow", tablefmt="grid"))    

def validate_argv(): #validates if the passed argument is a docx file and if the command is correct
    if len(sys.argv)>2:
        sys.exit("Too many command-line arguments")
    elif len(sys.argv)<2:
        sys.exit("Too for command-line arguments")
    elif sys.argv[1][-5:] != '.docx':
        sys.exit("File not .docx extension")
    else:
        return sys.argv[1]

def get_keywords(s): #creates a list of keywords for future use
    number = int(s)
    keyword_list = []
    while number > 0:
        keyword_list.append(input("Enter keyword: "))
        number-=1
    return keyword_list

def word_document(doc): #this takes the docx file and returns it as txt
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
            line = re.sub("[,.?]",'', line)
            line = re.sub("\[[0-9]\]", '', line)
            formatted_file.write(line)
    return 'formatted_temp.txt'

def exact_match_parse(formatted_file, keyword_list): #this will parse the formatted txt for exact matches
    keyword_count = {}
    for i in keyword_list:
        keyword_count.update({i: 0})
    
    formatted_document = open(formatted_file, 'r').read()
    keyword_processor = KeywordProcessor()
    for i in keyword_list:
        keyword_processor.add_keyword(i)
    
    kw_found = keyword_processor.extract_keywords(formatted_document)

    for i in kw_found:
        keyword_count[i] += 1
    return keyword_count

def partial_match_parse(formatted_file, keyword_list): 
    #this will parse the formatted document for partial KW matches. If the KW is an exact match, 
    #it will not be counted towards partial
    kw_patterns = []
    for keyword in keyword_list:
        separated_kw = keyword.split(" ")
        kw_patterns.append('(?: |(?:(?: \w* )(?:\w* )?))'.join(separated_kw))

    partial_matches = []
    
    with open(formatted_file, 'r') as file:
        file = file.read()
        for pattern in kw_patterns:
            matches = re.findall(pattern, file, re.IGNORECASE)
            for match in matches:
                if match.lower() in keyword_list:
                    matches.remove(match)
            partial_matches.append(len(matches))
    return partial_matches    

if __name__ == "__main__":
    main()
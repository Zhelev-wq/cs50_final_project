from flashtext import KeywordProcessor
import re

keywords = ['online casinos that accept paysafecard',
'best online casinos paysafecard',
'online casino with paysafecard',
'best online casinos that accept paysafecard',
'paysafecard casino sites']
keyword_count = {}

"""this removes html tags and punctuation from the file"""
with open('new_doc.txt', 'r') as original_file, open('test_file2.txt', 'w') as formatted_file:
    for line in original_file.readlines():
        clean = re.compile('<.*?>')
        line = re.sub(clean,'', line)
        line = re.sub("[,.?]",'', line)
        line = re.sub("\[[0-9]\]", ' ', line)
        formatted_file.write(line)

formatted_document = open('test_file2.txt', 'r').read()
keyword_processor = KeywordProcessor()
for i in keywords:
    keyword_processor.add_keyword(i)
kw_found = keyword_processor.extract_keywords(formatted_document)
for i in kw_found:
    if i not in keyword_count:
        keyword_count.update({i: 1})
    elif i in keyword_count:
        keyword_count[i] += 1
    
for i in keyword_count:
    print(f'Keyword "{i}" is {keyword_count[i]} times in text')

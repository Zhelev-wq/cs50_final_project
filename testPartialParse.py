import re

keywords_list = ['online casinos that accept paysafecard',
'best online casinos paysafecard',
'online casino with paysafecard',
'best online casinos that accept paysafecard',
'paysafecard casino sites']

# the pattern ( |(( \w* )(\w* )?)) takes one white space, or one word, or one word followed by a second word

keyword = 'The best online casinos with paysafecard are around the corner. Jone of the best online casinos offering paysafecard now.'

"""pattern = r'best(?: |(?:(?: \w* )(?:\w* )?))online(?: |(?:(?: \w* )(?:\w* )?))casinos(?: |(?:(?: \w* )(?:\w* )?))paysafecard'
if partial_match := re.findall(pattern, keyword):
    print('yes')
    print(partial_match)
else:
    print('no')"""

"""kw_patterns = []
with open('kw_patterns.txt', 'w') as file:
    for keyword in keywords_list:
        separated_kw = keyword.split(" ")
        kw_patterns.append('(?: |(?:(?: \w* )(?:\w* )?))'.join(separated_kw))
    for keyword in kw_patterns:  
        file.write(keyword + '\n')"""


partial_matches = []
with open('formatted_temp.txt', 'r') as file:
    file = file.read()
    matches = re.findall('best(?: |(?:(?: \w* )(?:\w* )?))online(?: |(?:(?: \w* )(?:\w* )?))casinos(?: |(?:(?: \w* )(?:\w* )?))paysafecard', file, re.IGNORECASE)
    for i in matches:
        if i.lower() in keywords_list:
            continue
        else:
            partial_matches.append(i)
print(len(partial_matches))
for i in partial_matches:
    print(i)
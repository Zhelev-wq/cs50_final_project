import re

keywords_list = ['online casinos that accept paysafecard',
'best online casinos paysafecard',
'online casino with paysafecard',
'best online casinos that accept paysafecard',
'paysafecard casino sites']

keyword_dict = {}

for i in keywords_list:
    keyword_dict.update({i:'0'})

for count, i in enumerate(keyword_dict):
    keyword_dict[i] = [keyword_dict[i], keywords_list[count]]

print(keyword_dict)
#print(len(keyword_dict.keys()))
#print(len(keyword_dict.values()))
# the pattern ( |(( \w* )(\w* )?)) takes one white space, or one word, or one word followed by a second word

"""keyword = 'The best online casinos with paysafecard are around the corner. Jone of the best online casinos offering paysafecard now.'


kw_patterns = ['online(?: |(?:(?: \w* )(?:\w* )?))casinos(?: |(?:(?: \w* )(?:\w* )?))that(?: |(?:(?: \w* )(?:\w* )?))accept(?: |(?:(?: \w* )(?:\w* )?))paysafecard',
'best(?: |(?:(?: \w* )(?:\w* )?))online(?: |(?:(?: \w* )(?:\w* )?))casinos(?: |(?:(?: \w* )(?:\w* )?))paysafecard',
'online(?: |(?:(?: \w* )(?:\w* )?))casino(?: |(?:(?: \w* )(?:\w* )?))with(?: |(?:(?: \w* )(?:\w* )?))paysafecard',
'best(?: |(?:(?: \w* )(?:\w* )?))online(?: |(?:(?: \w* )(?:\w* )?))casinos(?: |(?:(?: \w* )(?:\w* )?))that(?: |(?:(?: \w* )(?:\w* )?))accept(?: |(?:(?: \w* )(?:\w* )?))paysafecard',
'paysafecard(?: |(?:(?: \w* )(?:\w* )?))casino(?: |(?:(?: \w* )(?:\w* )?))sites'
]

with open('kw_patterns.txt', 'w') as file:
    for keyword in keywords_list:
        separated_kw = keyword.split(" ")
        kw_patterns.append('(?: |(?:(?: \w* )(?:\w* )?))'.join(separated_kw))
    for keyword in kw_patterns:  
        file.write(keyword + '\n')


partial_matches = []
with open('formatted_temp.txt', 'r') as file:
    file = file.read()
    for pattern in kw_patterns:
        matches = re.findall(pattern, file, re.IGNORECASE)
        for match in matches:
            count = []
            if match.lower() in keywords_list:
                matches.remove(match)
            
        partial_matches.append({
            keywords_list[kw_patterns.index(pattern)]:len(matches)
            })

for i in partial_matches:
    print(i)
for i in kw_patterns:
    print(keywords_list[kw_patterns.index(i)])"""

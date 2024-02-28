import re

keywords_list = ['online casinos that accept paysafecard',
'best online casinos paysafecard',
'online casino with paysafecard',
'best online casinos that accept paysafecard',
'paysafecard casino sites']

# the pattern ( |(( \w* )(\w* )?)) takes one white space, or one word, or one word followed by a second word

keyword = 'best online casinos with paysafecard'

pattern = 'best online casinos( |(( \w* )(\w* )?))paysafecard'
if partial_match := re.search(pattern, keyword):
    print('yes')
else:
    print('no')

kw_patterns = []
for keyword in keywords_list:
    separated_kw = keyword.split(" ")
    kw_patterns.append('( |(( \w* )(\w* )?))'.join(separated_kw))

for i in kw_patterns:
    print(i)
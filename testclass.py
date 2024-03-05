class Keyword:
    def __init__(self, keyword, exact_match, partial_match) -> None:
        self.keyword = keyword
        self.exact_match = exact_match
        self.partial_match = partial_match
    def keyword_form(self):
        return [self.keyword, self.exact_match, self.partial_match]

keywords = ['online casinos that accept paysafecard',
'best online casinos paysafecard',
'online casino with paysafecard',
'best online casinos that accept paysafecard',
'paysafecard casino sites']

x = x.keyword()
print(x)
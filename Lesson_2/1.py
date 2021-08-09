import requests
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

url = 'http://127.0.0.1:5000/'

response = requests.get(url)
html = response.text

soup = bs(html, 'html.parser')
print()

tag_a = soup.find('a')
# print(tag_a)

parent_a = tag_a.parent.parent  # findParent()
# print(parent_a)

# children = parent_a.children
#
# pprint(list(children))

children = parent_a.findChildren(recursive=False)
# pprint(list(children))

# tag = children[0]
# while tag.nextSibling is not None:
#     pprint(tag)
#     tag = tag.nextSibling
#
#
# print('The end')

# elements = soup.find('div',attrs={'id':'d2'})
# print(elements)

# elements = soup.find_all('p',attrs={'class':['red', 'left']})
# print(elements)

elem = soup.find(text='Шестой параграф')
print(elem.parent)


import requests
from bs4 import BeautifulSoup
import tqdm
import sys

def get_content(target):
    try:
        req = requests.get(url = target)
    except Exception as e:
        print('丢了一章')
        print(e)
        return -1
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html,'html.parser')
    texts = bf.find('div',id='content')
    content = texts.text.strip().split('\xa0'*4)
    return content

seach_url = 'https://www.xsbiquge.com/search.php?keyword='

def seach(book_name):
    try:
        req = requests.get(seach_url + book_name)
    except Exception as e:
        print(e)
        return -1
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html,'html.parser')
    result_items = bf.find_all('div',class_ = 'result-game-item')
    results = {}
    for result_item in result_items:
        result_book_index_url = result_item.find('a').get('href')
        result_book_name = result_item.find('a',class_ = 'result-game-item-title-link')
        result_book_name = result_book_name.get('title')
        results[result_book_name] = result_book_index_url
    return results



server = 'https://www.xsbiquge.com/'
##index = 'https://www.xsbiquge.com/87_87254/' 测试
##index = 'https://www.xsbiquge.com/87_87249/' 测试用例

if len(sys.argv) <= 1:
    print('缺少参数\n\t需要index(目录url)和book_name(书名)')
    sys.exit(1)
else:
    #index = sys.argv[1]
    #book_name = sys.argv[2] + '.txt'
    results = seach(sys.argv[1])

loop = 1
book_list = []

for key in results.keys():
    print(loop)
    print('\t')
    print(key)
    print(results[key])
    print('\n')
    book_list.append(key)
    loop = loop + 1
try:
    answer = int(input('input a number of list'))
except ValueError:
    sys.exit(-2)

book_name = book_list[answer - 1]
index = results[book_name]

def main(index,book_name):
    f = open('SB/' + book_name + '.txt','w+',encoding = 'utf-8')
    r = requests.get(index)
    r.encoding = r.apparent_encoding
    html = r.text
    bf = BeautifulSoup(html,'html.parser')
    chapters = bf.find('div',id = 'list')
    chapters = chapters.find_all('a')
    print(chapters)
    for chapter in tqdm.tqdm(chapters):
        chapter_name = chapter.string)
        url = server + chapter.get('href')
        content = get_content(url)
        f.write('##')
        f.write(chapter_name)
        f.write('\n  ')
        f.write('\n  '.join(content))
        f.write('\n')
    f.close()
main(index,book_name)
print('ok')
sys.exit(0)

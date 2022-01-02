# import sys
# from urllib.request import urlopen
#
# f = urlopen('https://www.hanbit.co.kr/store/books/full_book_list.html')
# encoding = f.info().get_content_charset(failobj="utf-8")
#
# print('encoding:', encoding, file=sys.stderr)
#
# text = f.read().decode(encoding)
# print(text)
# f = open('dp.html', 'w')
# f2 = open('dp.txt', 'w')
# f.write(text)
# f2.write(text)
# f.close()
# f2.close()

# p59

import re
from html import unescape

# 이전 절에서 다운로드한 파일을 열고 html이라는 변수에 저장
with open('dp.html') as f:
    html = f.read()

# re.findall() 을 사용해 도서 하나에 해당하는 HTML을 추출

for partial_html in re.findall(r'<td class="left"><a.*?</td>', html, re.DOTALL):
    # 도서의 URL을 추출
    url = re.search(r'<a href="(.*?)">', partial_html).group(1)
    url = 'http://hanbit.co.kr' + url

    # 태그를 제거해서 도서의 제목을 추출

    title = re.sub(r'<.*?>', '', partial_html)
    title = unescape(title)

    print('url:', url)
    print('title:', title)
    print('---')
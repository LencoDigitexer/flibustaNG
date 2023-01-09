from lxml import html
import requests

page = requests.get('http://flibusta.is/b/91828')
tree = html.fromstring(page.content)
fb2 = tree.xpath('//*[@id="main"]/div[3]/a[2]/@href')
epub = tree.xpath('//*[@id="main"]/div[3]/a[3]/@href')
mobi = tree.xpath('//*[@id="main"]/div[3]/a[4]/@href')
pdf = tree.xpath('//*[@id="main"]/div[3]/a[5]/@href')
image = tree.xpath('//*[@id="main"]/img/@src')
p = tree.xpath('//*[@id="main"]/p/text()')
print('fb2: ', str(fb2[0]))
print('epub: ', epub)
print('mobi: ', mobi)
print('pdf: ', pdf)
print(image)
print(p)
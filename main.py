from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import os

requestUrl = 'https://nhentai.net/g/100000/'

# nHentaiId
nHentaiIdMatch = re.search('/g/([0-9]*)/', requestUrl)
if nHentaiIdMatch is None:
    print('abort')
    exit(1)
nHentaiId = nHentaiIdMatch.group(1)

# get site html
r = requests.get(requestUrl)
soup = BeautifulSoup(r.text, 'html.parser')

# print(soup.prettify())

# get gallery id
coverSourceUrl = soup.find(id='cover').img['data-src']

galleryIdMatch = re.search('/galleries/([0-9]*)/', coverSourceUrl)
if galleryIdMatch is None:
    print('abort')
    exit(1)
galleryId = galleryIdMatch.group(1)

# get pageCount
pageCount = len(soup.find(id='thumbnail-container').find('div', class_='thumbs').contents)

# extract image urls using the pageCount and the gallery id
imgBaseUrl = "https://i.nhentai.net/galleries/{}/{}.jpg"

imgUrlList = []
for i in range(1, pageCount + 1):
    imgUrlList.append(imgBaseUrl.format(galleryId, i))

for imgUrl in imgUrlList:
    print(imgUrl)

# download images into directory

baseDir = '/home/tam/PycharmProjects/pythonProject/saves'
print('base directory: {}'.format(baseDir))
newDir = os.path.join(baseDir, nHentaiId)
print('creating new directory named {}'.format(galleryId))
try:
    print('attempting to create dir {}'.format(baseDir))
    if not os.path.exists(baseDir):
        print('creating dir {}...'.format(baseDir))
        os.mkdir(baseDir)
    else:
        print('dir {} already exists', baseDir)

    print('creating dir {}...'.format(newDir))
    os.mkdir(newDir)
except OSError:
    print("dir creation failed")

# pretend to be normal user
# opener=urllib.request.build_opener()
# opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
# urllib.request.install_opener(opener)

for imgUrl in imgUrlList:
    filename = os.path.join(newDir, imgUrl.split('/')[-1])
    print('writing {} to {}'.format(imgUrl, filename))
    urllib.request.urlretrieve(imgUrl, filename)

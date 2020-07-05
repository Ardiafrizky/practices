import os
import bs4, json
import requests, clint
from pprint import pprint

imgLinks = []
apikey = 'mZk1ErtcfG7if0dxrNhei5XbaZpKg9V9'

def searchImg(url,location):
    pages = 0
    for p in range((qty//24)+1):
        pages += 1
    for page in range(startingPage,startingPage+pages):
        url += ('&page='+str(page))
        req = requests.get(url,stream=True)
        if req.status_code == 200:
            theJson = json.loads(req.text)
            for data in theJson['data']:
                imgLinks.append(data['path'])
                if len(imgLinks) >= qty:
                    break
        else:
            print(url+' can not be accessed (check your username)')
    
    for i in range(qty):
        imgReq = requests.get(imgLinks[i],stream=True)
        if imgReq.status_code == 200:
            imgPath = 'C:\\Users\\MSI PS42\\Downloads\\Wallpaper\\Wallhaven\\Users\\'+user+location
            if not os.path.exists(imgPath):
                os.makedirs(imgPath)
            print('\n'+str(i+1)+') '+imgLinks[i])
            with open(imgPath+'\\'+imgLinks[i].split('/')[-1],'wb') as file:
                length = int(imgReq.headers.get('content-length'))
                for chunk in clint.textui.progress.bar(imgReq.iter_content(chunk_size=1024), expected_size=(length/1024)+1):
                    if chunk:
                        file.write(chunk)
                        file.flush()
            print('file downloaded')
        else:
            print(imgLinks[i]+' not downloaded')

print('''
Insert (1) if you want to search by user's uploads
Insert (2) if you want to search by user's collection
''')
searchBy = input('Your Input: ')

if searchBy == '1':
    user = input('User Name: ')
    qty = int(input('Quantity: '))
    startingPage = int(input('Starting Page: '))
    url = 'https://wallhaven.cc/api/v1/search?apikey='+apikey+'&q=@'+user+'&categories=111'
    searchImg(url,'\\Uploads')
elif searchBy == '2':
    user = input('User Name: ')
    qty = int(input('Quantity: '))
    startingPage = int(input('Starting Page: '))
    collectionsUrl = 'https://wallhaven.cc/api/v1/collections/'+user
    getColl = requests.get(collectionsUrl,stream=True)
    collections = json.loads(getColl.text)
    if len(collections['data']) == 0:
        print('This user has no collection')
    else:
        print('\nCollections: ')
        for i in range(len(collections['data'])):
            print(' '+str(i+1)+') '+collections['data'][i]['label']+'('+str(collections['data'][i]['count'])+')')
        key = input('\nInsert the Collection number: ')
        key = collections['data'][int(key)-1]['id']
        url = 'https://wallhaven.cc/api/v1/collections/'+user+'/'+str(key)+'?categories=111&apikey='+apikey
        searchImg(url,'\\Collections\\'+collections['data'][i]['label']) 
else:
    print("Input (1) or (2) only ...")

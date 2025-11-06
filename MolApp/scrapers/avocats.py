import sys
import requests 
import pandas as pd 
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')


def url_access(url):
     response = requests.get(url)
     response.encoding = response.apparent_encoding
     html = response.content.decode("utf-8")
     return BeautifulSoup(html, 'html5lib')
     
def url_exists(url):
    try: 
        response = requests.get(url, allow_redirects=True)
        if response.status_code >= 200 :
            return True
        else:
            return False
    except requests.ConnectionError:
        print(f"Erreur de connexion : l'URL {url} est inaccessible.")
        return False
   
    except requests.RequestException as e:
        print(f"Une erreur s'est produite : {e}")
        return False

    

def clean_txt(ch):
    while ch.find('\n')!=-1:
        ch=ch.replace('\n',' ')
    while ch.find('  ')!=-1:
        ch=ch.replace('  ',' ')
    return ch

def data_extract(tr,dic):
    cols=tr.find_all('div', class_='one-column')
    nb=-1
    keys=list(dic.keys())
    for col in cols: 
        champ=col.find_all('li', class_='block1')
        for li in champ:
            nb+=1
            label= keys[nb]
            dic[label].append(li.find('span',class_='data_ann').text)


def avocat_scrap(url,ch,intervalle):
    while True:      
        url=input("Entrer l'URL de la page: ")
        if url_exists(url)== True:
            break
        else: 
            print("URL non valide")

    dic={
        'الاسم':[],
        'اللقب':[],
        'الجدول':[],
        'الفرع':[],
        'الولاية':[],
        'المدينة':[],
        'الترقيم البريدي':[],  
        'الهاتف القار':[],
        'الفاكس':[],
        'العنوان':[],
        'البريد الالكتروني':[],
        
    }

    listpage=[]
    numpage=[]
    deb='0'
    fin='0'
    while True:
        ch=ch.strip()
        if ch.lower()=='toutes':
            break
        elif ch.lower()=='actuelle':
            break 
        elif ch.lower()=='personnaliser':
            while True: 
                intr=intervalle.replace(' ','')
                test=True
                for i in intr:
                    if i.isalpha() and i!= '-' and i!=',':
                        test=False
                if test: 
                    break 
            if intr.isnumeric():
                deb=intr
            elif intr.find('-')!=-1 and intr.find(',')!=-1:
                for i in intr.split(','):
                    if '-' in i :
                        listpage.append(i.split('-'))
                    else:
                        listpage.append(i)
            elif intr.find('-')!= -1:
                deb=intr.split('-')[0]
                fin=intr.split('-')[1]
            elif intr.find(',')!= -1 :
                numpage=intr.split(',')       
            break
        else:
            print("Erreur : veuillez entrer 'toutes' ou 'actuelle' ou 'personnaliser'")

    if url.find('/annuaire-')==-1:
        url_base=url+"/annuaire-"
    else:
        i=url.find('/annuaire-')
        url_base=url[:i+10]

    if ch.lower()=='toutes':
        npage=1
        while True: 
            url_scrap=url_base+str(npage)
            soup=url_access(url_scrap)
            body=soup.body 
            info='info_'
            n=1
            while 1: 
                tr=body.tbody.find('tr',id=info+str(n))
                data_extract(tr,dic)
                n+=1
                if body.tbody.find('tr',id=info+str(n)) == None :
                    break 
            pagination=body.find('div', class_='pagination')
            next_page = pagination.find('a', string=str(npage + 1))
            if next_page is None:
                break
            npage += 1
    elif ch.lower()=='actuelle': 
        url_scrap=url
        soup=url_access(url_scrap)
        body=soup.body 
        info='info_'
        n=1
        while 1: 
            tr=body.tbody.find('tr',id=info+str(n))
            data_extract(tr,dic)
            n+=1
            if body.tbody.find('tr',id=info+str(n)) == None :
                break 
            
    elif deb!='0' and fin=='0'and ch.lower()=='personnaliser':
        url_scrap=url_base+str(deb)
        soup=url_access(url_scrap)
        body=soup.body 
        info='info_'
        n=1
        while 1: 
            tr=body.tbody.find('tr',id=info+str(n))
            data_extract(tr,dic)
            n+=1
            if body.tbody.find('tr',id=info+str(n)) == None :
                break 
    elif deb!='0' and fin!='0' and ch.lower()=='personnaliser':
        for i in range(int(deb),int (fin)+1):
            url_scrap=url_base+str(i)
            soup=url_access(url_scrap)
            body=soup.body 
            info='info_'
            n=1
            while 1: 
                tr=body.tbody.find('tr',id=info+str(n))
                data_extract(tr,dic)
                n+=1
                pagination=body.find('div', class_='pagination')
                if body.tbody.find('tr',id=info+str(n)) == None or (pagination.find('span', class_='inactive')!=None and pagination.find('span',class_='active').text != '1') :
                    break 

    elif listpage != [] and ch.lower()=='personnaliser':
        for i in listpage: 
            if isinstance(i, list):
                for j in range(int(i[0]), int(i[1])+1):
                    url_scrap=url_base + str(j)
                    soup=url_access(url_scrap)
                    body=soup.body 
                    info='info_'
                    n=1
                    while 1: 
                        tr=body.tbody.find('tr',id=info+str(n))
                        data_extract(tr,dic)
                        n+=1
                        pagination=body.find('div', class_='pagination')
                        if body.tbody.find('tr',id=info+str(n)) == None  or (pagination.find('span', class_='inactive')!=None and pagination.find('span',class_='active').text != '1'):
                            break 
            else: 
                url_scrap=url_base + i
                soup=url_access(url_scrap)
                body=soup.body 
                info='info_'
                n=1
                while 1: 
                    tr=body.tbody.find('tr',id=info+str(n))
                    data_extract(tr,dic)
                    n+=1
                    pagination=body.find('div', class_='pagination')
                    if body.tbody.find('tr',id=info+str(n)) == None  or (pagination.find('span', class_='inactive')!=None and pagination.find('span',class_='active').text != '1'):
                        break 

    elif numpage != [] and ch.lower()=='personnaliser':
        for i in numpage:
            url_scrap=url_base + i
            soup=url_access(url_scrap)
            body=soup.body 
            info='info_'
            n=1
            while 1: 
                tr=body.tbody.find('tr',id=info+str(n))
                data_extract(tr,dic)
                n+=1
                pagination=body.find('div', class_='pagination')
                if body.tbody.find('tr',id=info+str(n)) == None  or (pagination.find('span', class_='inactive')!=None and pagination.find('span',class_='active').text != '1'):
                    break 
    return dic




import sys
import requests 

from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


sys.stdout.reconfigure(encoding='utf-8')


def url_access(url):
     response = requests.get(url,headers=headers)
     response.encoding = response.apparent_encoding
     html = response.content.decode("utf-8")
     time.sleep(5)
     return BeautifulSoup(html, 'html5lib')


def url_exists(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code >= 200 and response.status_code < 300:
            return True
        else:
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

def data_extract(div,dic):
    cont=div.find('div',class_='contact-info')
    nometat=cont.h4.text 
    ind=nometat.find(' | ')
    dic['Nom Prénom'].append(nometat[:ind])
    dic['État'].append(nometat[ind+3:])
    for j in cont.find_all('p'):
        if j.find('i', class_='fas fa-map-pin') is not None:
            if j.text !='':
                dic['Adresse'].append(j.text)
            else:
                dic['Adresse'].append('Non disponible')
        if j.find('i', class_='fas fa-envelope') is not None:
            if j.text !='':
                dic['E-mail'].append(j.text)
            else:
                dic['E-mail'].append('Non disponible')
        if j.find('i', class_='fas fa-phone-alt') is not None:
            if j.find('a').text !='':
                num=j.find('a').text
                dic['Num Tel'].append( num )
            else: 
                dic['Num Tel'].append('Non disponible')
        if j.find('i', class_='fas fa-fax') is not None: 
            if j.find('i', class_='fas fa-fax').text !='':
                fax=j.find('i', class_='fas fa-fax').text
                dic['Fax'].append(fax)
            else:
                dic['Fax'].append('Non disponible')
        if j.find('i',class_='fas fa-id-card') is not None:
           bold= j.find_all('b')
           if bold[0]!='':
               dic["Année d'adhésion"].append(bold[0].text)
           else:
               dic["Année d'adhésion"].append('Non disponible') 
           if bold[1]!='':
               dic['Conseil Régional'].append(bold[1].text)
           else:
                dic['Conseil Régional'].append('Non disponible')

def experts_scrap(url,ch,intervalle):

    dic={
        'Nom Prénom':[],
        'État':[],
        'Adresse':[],
        'E-mail':[],
        'Num Tel':[],
        'Fax':[],
        "Année d'adhésion":[],
        'Conseil Régional':[]
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


    if url.find('/page/')==-1:
        url_base=url + '/page/'
    else: 
        i=url.find('/page/')
        url_base=url[:i+6]

    if ch.lower()=='toutes':
        i= url_base.find('/page/')-1
        url_base=url_base[:i-1]
        for c in 'abcdefghijklmnopqrstuvwxyz':
            url_scrap=url_base + c +'/page/1/'
            while True:
                soup=url_access(url_scrap)
                body= soup.body
                for div in body.find_all('div', class_='contact-card'):
                    data_extract(div,dic)
                pagination = soup.body.find('ul', class_='page-numbers')
                if pagination:
                    next_page = pagination.find('a', class_='next page-numbers')
                    if next_page:
                        url_scrap = next_page['href']
                    else:
                        break
                else:
                    break

    elif ch.lower() =='actuelle':
        url_scrap=url
        soup=url_access(url_scrap)
        container= soup.body
        for div in container.find_all('div', class_='contact-card'):
            data_extract(div,dic)

    elif deb!='0' and fin=='0'and ch.lower()=='personnaliser':
        url_scrap=url_base + deb +'/'
        soup=url_access(url_scrap)
        body= soup.body
        for div in body.find_all('div', class_='contact-card'):
            data_extract(div,dic)

    elif deb!='0' and fin!='0' and ch.lower()=='personnaliser':
        for i in range(int(deb),int(fin)+1):
            url_scrap=url_base + str(i)+'/'
            soup=url_access(url_scrap)
            body= soup.body
            for div in body.find_all('div', class_='contact-card'):
                data_extract(div,dic)
            pagination=body.find('ul', class_='page-numbers')
            next=pagination.find('a', class_='next page-numbers')
            if next == None :
                break 
    elif listpage != [] and ch.lower()=='personnaliser':
        for i in listpage: 
            if isinstance(i, list):
                for j in range(int(deb),int(fin)+1):
                    url_scrap=url_base + str(j)+'/'
                    soup=url_access(url_scrap)
                    body= soup.body
                    for div in body.find_all('div', class_='contact-card'):
                        data_extract(div,dic)
                    pagination=body.find('ul', class_='page-numbers')
                    next=pagination.find('a', class_='next page-numbers')
                    if next == None :
                        break 
            else:
                url_scrap=url_base + i +'/'
                soup=url_access(url_scrap)
                body= soup.body
                for div in body.find_all('div', class_='contact-card'):
                    data_extract(div,dic)

    elif numpage != [] and ch.lower()=='personnaliser':
        for i in numpage:
            url_scrap=url_base +i +'/'
            soup=url_access(url_scrap)
            body= soup.body
            for div in body.find_all('div', class_='contact-card'):
                data_extract(div,dic)

    return dic 

import sys
import requests 
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'

    }

def url_access(url):
     response = requests.get(url, headers=headers,allow_redirects=True)
     response.encoding = response.apparent_encoding
     
     html = response.content.decode("utf-8")
     return BeautifulSoup(html, 'html5lib')

     
def clean_txt(ch):
    while ch.find('\n')!=-1:
        ch=ch.replace('\n',' ')
    while ch.find('  ')!=-1:
        ch=ch.replace('  ',' ')
    return 

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

def data_extract(url, dic):
    soup1 = url_access(url)
    nom = soup1.find('div', {'data-name': "entity_field_post_title"})
    dic['Nom Prénom'].append(nom.text.strip() if nom else 'Non disponible')
    fct = soup1.find('div', {'data-name': "entity_field_directory_category"})
    dic['Fonction'].append(fct.text.strip() if fct else 'Non disponible')
    adresse = 'Non disponible'
    gouvernorat = 'Non disponible'
    phone = 'Non disponible'
    fax = 'Non disponible'
    email = 'Non disponible'
    for i in soup1.find_all('div', {'data-name': 'column'}):
        if i.find('div', {'data-name': 'entity_field_location_address'}):
            adresse = i.find('div', {'data-name': 'entity_field_location_address'}).text.strip()
        if i.find('div', {'data-name': 'entity_field_location_location'}):
            gouvernorat = i.find('div', {'data-name': 'entity_field_location_location'}).text.strip()
        if i.find('div', {'data-name': 'entity_field_field_phone'}):
            phone = i.find('div', {'data-name': 'entity_field_field_phone'}).text.strip()
        if i.find('div', {'data-name': 'entity_field_field_fax'}):
            fax = i.find('div', {'data-name': 'entity_field_field_fax'}).text.strip()
        if i.find('div', {'data-name': 'entity_field_field_email'}):
            email = i.find('div', {'data-name': 'entity_field_field_email'}).text.strip()

    dic['Adresse'].append(adresse)
    dic['Gouvenorat'].append(gouvernorat)
    dic['Num Tel'].append(phone)
    dic['Fax'].append(fax)
    dic['E-mail'].append(email)



def url_create(num, url):
    if 'page' not in url:
        url_base = f"{url}?_page={num}"
    else:
        url_base = url.split('?_page=')[0] + f"?_page={num}"
    return url_base


def comptab_scrap(url,ch,intervalle):

    soup=url_access(url)


    dic={
        'Nom Prénom':[],
        'Fonction':[],
        'Adresse':[],
        'Gouvenorat':[],
        'Num Tel':[],
        'Fax':[],
        'E-mail':[]
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





    if ch.lower()=='toutes':
        url_scrap=url_create(1,url)
        while True:
            soup=url_access(url_scrap)
            for elt in soup.body.find_all('div',class_="dw-panel drts-view-entity-container"):
                url_fiche=elt.a['href']
                data_extract(url_fiche,dic)
            pagination=soup.body.find('div', class_='drts-pagination drts-bs-btn-group drts-bs-nav-item drts-bs-mr-2 drts-bs-mb-2 drts-bs-mb-sm-0 drts-view-nav-item drts-view-nav-item-name-pagination')
            next=pagination.find('i',class_='fas fa-angle-double-right')
            if next.parent['href']!='#': 
                url_scrap=next.parent['href']
            else:
                break
    elif ch.lower()=='actuelle':
        url_scrap=url
        soup=url_access(url_scrap)
        for elt in soup.body.find_all('div',class_="dw-panel drts-view-entity-container"):
            url_fiche=elt.a['href']
            data_extract(url_fiche,dic)
        
    elif deb!='0' and fin=='0'and ch.lower()=='personnaliser':
        url_scrap=url_create(int(deb),url)
        soup=url_access(url_scrap)
        for elt in soup.body.find_all('div',class_="dw-panel drts-view-entity-container"):
            url_fiche=elt.a['href']
            data_extract(url_fiche,dic)
        
    elif deb!='0' and fin!='0' and ch.lower()=='personnaliser':
        for i in range(int(deb),int(fin)+1):
            url_scrap=url_create(i,url)
            soup=url_access(url_scrap)
            for elt in soup.body.find_all('div',class_="dw-panel drts-view-entity-container"):
                url_fiche=elt.a['href']
                data_extract(url_fiche, dic)

    elif listpage != [] and ch.lower()=='personnaliser':
        for i in listpage: 
            if isinstance(i, list):
                for j in range(int(i[0]), int(i[1])+1):
                    url_scrap=url_create(j,url)
                    soup=url_access(url_scrap)
                    for elt in soup.body.find_all('div',class_="dw-panel drts-view-entity-container"):
                        url_fiche=elt.a['href']
                        data_extract(url_fiche,dic)
            
            else: 
                url_scrap=url_create(i,url)
                soup=url_access(url_scrap)
                for elt in soup.body.find_all('div',class_="dw-panel drts-view-entity-container"):
                        url_fiche=elt.a['href']
                        data_extract(url_fiche,dic)

    elif numpage != [] and ch.lower()=='personnaliser':
        for i in numpage:
            url_scrap=url_create(i,url)
            soup=url_access(url_scrap)
            for elt in soup.body.find_all('div',class_="dw-panel drts-view-entity-container"):
                        url_fiche=elt.a['href']
                        data_extract(url_fiche,dic)
    return dic 
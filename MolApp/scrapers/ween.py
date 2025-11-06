import sys
import requests 
from bs4 import BeautifulSoup


sys.stdout.reconfigure(encoding='utf-8')


def url_access(url):
     response = requests.get(url)
     response.encoding = response.apparent_encoding
     
     html = response.content.decode("utf-8")
     return BeautifulSoup(html, 'html5lib')
     
def clean_txt(ch):
    while ch.find('\n')!=-1:
        ch=ch.replace('\n',' ')
    while ch.find('  ')!=-1:
        ch=ch.replace('  ',' ')
    return ch
    

def fiche_extract(url,dic):
    soup2=url_access(url)
    texte=soup2.find('div', class_="text-info")
    dic['Nom'].append(texte.h1.text.strip()) 
    if texte.p!= None:
        dic['Adresse'].append(texte.p.text.strip())
    else: 
        dic['Adresse'].append('Non disponible')
    if texte.li.text!=None:
        dic['Num Tel'].append(clean_txt(texte.li.text.strip()))
    else: 
        dic['Num Tel'].append('Non disponible')
    if soup2.find('div',class_="aprop-empty")!=None:
        desc=soup2.find('div',class_="aprop-empty").text.strip()
        dic['Description'].append(desc)
    else: 
        dic['Description'].append('Non disponible')


def weenscrap(url,ch,intervalle): 
    dic={
        'Nom':[],
        'Type':[],
        'Description':[],
        'Adresse':[],
        'Num Tel':[]
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


    if url.find('&page=')==-1:
        url_base=url+"&page="
    else:
        i=url.find('&page=')
        url_base=url[:i+6]



    if ch.lower()=='toutes':
        url_scrap=url_base+'1'
        while True:
            soup1=url_access(url_scrap)
            body1=soup1.body
            for case in body1.find_all('div', class_='lp-grid-box-contianer card1 lp-grid-box-contianer1 list_view'):
                url_fiche="https://ween.tn"+(case.h4.a['href'])
                dic_type=case.find('ul',class_='search-list-cat')
                dic['Type'].append(clean_txt(dic_type.text.strip()))
                fiche_extract(url_fiche,dic)
                #afficher(dic)
            pagination=soup1.body.find('ul',class_='pagination')
            if pagination is None or pagination.find('a',rel='next') is None:
                break
            else:
                url_scrap="https://ween.tn"+pagination.find('a',rel='next')['href']
    elif ch.lower()=='actuelle':
        url_scrap=url 
        soup1=url_access(url_scrap)
        body1=soup1.body
        for case in body1.find_all('div', class_='lp-grid-box-contianer card1 lp-grid-box-contianer1 list_view'):
            url_fiche="https://ween.tn"+(case.h4.a['href'])
            dic_type=case.find('ul',class_='search-list-cat')
            dic['Type'].append(clean_txt(dic_type.text.strip()))
            fiche_extract(url_fiche,dic)
    elif deb!='0' and fin=='0'and ch.lower()=='personnaliser':
        url_scrap=url_base + deb
        soup1=url_access(url_scrap)
        body1=soup1.body
        for case in body1.find_all('div', class_='lp-grid-box-contianer card1 lp-grid-box-contianer1 list_view'):
            url_fiche="https://ween.tn"+(case.h4.a['href'])
            dic_type=case.find('ul',class_='search-list-cat')
            dic['Type'].append(clean_txt(dic_type.text.strip()))
            fiche_extract(url_fiche,dic)

    elif deb!='0' and fin!='0' and ch.lower()=='personnaliser':
        for i in range(int(deb),int(fin)+1):
            url_scrap=url_base + str(i)
            soup1=url_access(url_scrap)
            body1=soup1.body
            for case in body1.find_all('div', class_='lp-grid-box-contianer card1 lp-grid-box-contianer1 list_view'):
                url_fiche="https://ween.tn"+(case.h4.a['href'])
                dic_type=case.find('ul',class_='search-list-cat')
                dic['Type'].append(clean_txt(dic_type.text.strip()))
                fiche_extract(url_fiche,dic)
            pagination=soup1.body.find('ul',class_='pagination')
            if pagination is None or pagination.find('a',rel='next') is None :
                break

    elif listpage != [] and ch.lower()=='personnaliser':
        for i in listpage: 
            if isinstance(i, list):
                for j in range(int(i[0]), int(i[1])+1):
                    url_scrap=url_base + str(j)
                    soup1=url_access(url_scrap)
                    body1=soup1.body
                    for case in body1.find_all('div', class_='lp-grid-box-contianer card1 lp-grid-box-contianer1 list_view'):
                        url_fiche="https://ween.tn"+(case.h4.a['href'])
                        dic_type=case.find('ul',class_='search-list-cat')
                        dic['Type'].append(clean_txt(dic_type.text.strip()))
                        fiche_extract(url_fiche,dic)
                    pagination=soup1.body.find('ul',class_='pagination')
                    if pagination is None or pagination.find('a',rel='next') is None:
                        break
                    else:
                        url_scrap="https://ween.tn"+pagination.find('a',rel='next')['href']
            
            else:
                url_scrap=url_base + i
                soup1=url_access(url_scrap)
                body1=soup1.body
                for case in body1.find_all('div', class_='lp-grid-box-contianer card1 lp-grid-box-contianer1 list_view'):
                    url_fiche="https://ween.tn"+(case.h4.a['href'])
                    dic_type=case.find('ul',class_='search-list-cat')
                    dic['Type'].append(clean_txt(dic_type.text.strip()))
                    fiche_extract(url_fiche,dic)

    elif numpage != [] and ch.lower()=='personnaliser':
        for i in numpage:
            url_scrap=url_base + i
            soup1=url_access(url_scrap)
            body1=soup1.body
            for case in body1.find_all('div', class_='lp-grid-box-contianer card1 lp-grid-box-contianer1 list_view'):
                url_fiche="https://ween.tn"+(case.h4.a['href'])
                dic_type=case.find('ul',class_='search-list-cat')
                dic['Type'].append(clean_txt(dic_type.text.strip()))
                fiche_extract(url_fiche,dic)

    return dic




    

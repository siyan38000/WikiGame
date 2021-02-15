from bs4 import BeautifulSoup
import requests
import urllib.request
import random
import tkinter as tk

window = tk.Tk()
window.title('Wikigame')
var = tk.StringVar()
global start_links
global startURL


#Definition des deux pages aléatoires
def getRandomPage():
    return requests.get('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard').content

#Fonction que filtre les liens afin de ne garder que les liens vers d'autree articles
def linksFilter(url):
    linksList = []
    with urllib.request.urlopen(url) as page:
        actualPage = BeautifulSoup(page.read(), 'html.parser')
        for anchor in actualPage.find_all('div', {"class":"mw-parser-output"}):
            for links in anchor.find_all('a'):
                link = formatage(str(links.get('href')))

                #On s'assure que le lien pointe bien vers un article et qu'il n'existe pas déja dans la liste
                if not ('/w/') in link:
                    if not ('#') in link:
                        if not ('Fichier:') in link:
                            if not ('http:') in link:
                                if not ('https:') in link:
                                    if not ('Modèle:') in link:
                                        if not ('/API') in link:
                                            if not ('Spécial:') in link:
                                                if not ('Catégorie:') in link:
                                                    if not (':') in link:
                                                        if not ('None') in link:
                                                            if link not in linksList:
                                                                linksList.append(link)

    return linksList

def formatage(arg):
    return arg.replace("%20"," ").replace("%27","'").replace("%C3%A8","è").replace("%C3%A9","é").replace('%C3%AA','ê').replace("%C3%A2","â").replace("%C5%93","œ").replace("%C3%B",'ü').replace("%C3%AC","ì").replace('%C3%A7','ç').replace('%C3%A0','à').replace('%C3%B4','ô').replace('%C3%89','É').replace("%C3%AF","ï")

#Fonction qui s'execute au clic sur un bouton radio et recupere sa valeur
def askForChoice():
    choice = var.get()
    updateWindow(choice)

depart = BeautifulSoup(getRandomPage(), 'html.parser')
arrive = BeautifulSoup(getRandomPage(), 'html.parser')
url1 = depart.find('li', attrs={'id': 'ca-nstab-main'}).find('a')['href']
url2 = arrive.find('li', attrs={'id': 'ca-nstab-main'}).find('a')['href']

def wikigame(start, end):
    startURL = start.find('li', attrs={'id': 'ca-nstab-main'}).find('a')['href']
    global endURL
    endURL = end.find('li', attrs={'id': 'ca-nstab-main'}).find('a')['href']
    updateWindow(startURL)


#Met a jour l'affichage a chaque changement de page
#le paramètre cpt compte le nombre de fois que la fonction est appelée
def updateWindow(url, cpt=[0]):

    #Suppression de tout les objets de la fenetre
    for widget in window.winfo_children():
        widget.destroy()

    if url == endURL:
        tk.Label(window, text="BRAVO !").pack()
        tk.Label(window, text="Page trouvée en {} coups".format(cpt)).pack()
    else:    
        tk.Label(window, text="Page actuelle : {}(URL = https://fr.wikipedia.org{})".format(url.replace("/wiki/",""), url)).pack()
        tk.Label(window, text="Page d'arrivée :{} (URL : https://fr.wikipedia.org{})".format(arrive.find(id='firstHeading').text,url2)).pack()
        #Ajout de la scrollbar pour la liste des liens
        canvas = tk.Canvas(window)
        scroll = tk.Scrollbar(window, orient='vertical', command=canvas.yview)


        start_links = linksFilter('https://fr.wikipedia.org'+url)
        i = 0
        for link in start_links:
            rb = tk.Radiobutton(canvas, text="{} - {}".format(i, link), variable=var, value = link, command=askForChoice)
            canvas.create_window(0, i*50, anchor='nw', window=rb, height=50)
            i = i + 1

        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll.set)
        canvas.pack(fill='both', expand=True, side='left')
        scroll.pack(fill='y', side='right')
        
        cpt[0] += 1


wikigame(depart, arrive)
tk.mainloop()

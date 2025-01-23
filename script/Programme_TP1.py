"""
Avant de commencer à lire les fonctions, pour lancer chaque fonction , il vous suffit d'enlever le # devant l'exécution de la fonction pour la lancer et remettre le # devant
pour ne pas la relancer la prochaine fois et obtenir seulement le résultat de la fonction que vous voulez lancer.
"""

### Partie 1 ###

import requests
response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
#print(response.text) 

### Partie 2 ###

#1)
import requests
import json
response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
data = response.json()

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

with open('data.json') as file:
    data = json.load(file)

#print(data)

#2)
"""
La fonction renvoie le nombre de places disponibles dans chaque parking et les sauvegardes dans un fichier texte.
Dans un premier temps, je récupère les données sur le site puis je le converties au format JSON
Ensuite, j'initialise une liste vide afin d'y intégrer le nombres de places libres par la suite.
Maintenant, je crée une boucle qui va me permettre de vérifier pour chaque parking s'il est ouvert.
Je crée une condition que s'il est ouvert, on ajoute dans la liste places le nombre de places libres du parking.
Enfin, j'enregistre dans un fichier le nombre de places libres pour chaque parking et je les affiches.
"""

def exo2():
    places=[]
    response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    data = response.json()
    for parking in data:
        ouvert=parking.get("status",{}).get("value")
        if ouvert=="Open":
            libres=parking.get("availableSpotNumber",{}).get("value")
            places.append(libres)
    with open("places.txt","w",encoding="utf-8") as f:
        for val in places:
            f.write(f'{val}\n')

    with open("places.txt","r",encoding="utf-8") as f:
        for ligne in f:
            print(ligne.rstrip())
#exo2()

#3)
"""
Cette fonction sauvegarde dans un fichier, pour chaque ligne : le nom du parking puis le nombre de places libres.
Tout d'abord, je reprends le même programme que pour l'exo mais je le modifie. Je change places en un dictionnaire maitenant et non une liste.
Egalement, je rajoute dans la condition que si le parking est ouvert, je rajoute dans le dictionnaire comme clé le nom du parking et comme valeur le nombre de places libres.
Enfin je modifie légèrement la fonction pour enregistrer car il s'agit maintenant d'un dictionnaire et non d'une liste.
"""
def exo3():
    places={}
    response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    data = response.json()
    for parking in data:
        ouvert=parking.get("status",{}).get("value")
        if ouvert=="Open":
            libres=parking.get("availableSpotNumber",{}).get("value")
            nom=parking.get("name",{}).get("value")
            places[nom]=libres
    with open("nom_et_places.txt","w",encoding="utf-8") as f:
        for cle,val in places.items():
            f.write(f'{cle} : {val} places libres \n')

    with open("nom_et_places.txt","r",encoding="utf-8") as f:
        for ligne in f:
            print(ligne.rstrip())
#exo3()

#4)
"""
Cette fonction renvoie le pourcentage de places libres pour chaque parking ainsi que le pourcentage de places libres dans toute la ville.
Je reprends le programme précédent en y ajoutant cette fois ci un calcul du pourcentage de place libre en divisant le nombre de places libres
par le nombre de places total.
Je rajoute aussi une variable ville qui calcule le pourcentage des places libres dans toute la ville.
Enfin dans la partie où j'enregistre le fichier je rajoute une ligne où apparait le pourcentage de places libres dans toute la ville.
"""

def exo4():
    places={}
    total_places=0
    total_libres=0
    response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    data = response.json()
    for parking in data:
        ouvert=parking.get("status",{}).get("value")
        if ouvert=="Open":
            libres=parking.get("availableSpotNumber",{}).get("value")
            total=parking.get("totalSpotNumber",{}).get("value")
            pourcentage=round(libres/total*100,2)
            nom=parking.get("name",{}).get("value")
            places[nom]=pourcentage
            total_places+=total
            total_libres+=libres
        ville=round(total_libres/total_places*100,2)
    with open("nom_et_places.txt","w",encoding="utf-8") as f:
        for cle,val in places.items():
            f.write(f'{cle} : {val}% de places libres \n')
        f.write(f'Il y a {ville}% de places libres dans toute ville.')

#    with open("nom_et_places.txt","r",encoding="utf-8") as f:
#        for ligne in f:
#            print(ligne.rstrip())

    return places
#exo4()

### Partie 3 ###
#8)

"""
La première fonction récupère l'occupation du parking nommé Corum et la seconde fait la fonction précédente toutes les 10 secondes pendant 5 minutes.
Pour cette fonction, j'ai repris les fonctions précédentes en modifiant la condition pour qu'elle se fasse seulement si le parking a Corum comme nom.
La fonction nous renvoie le nombres de places libres et totale du parking.
C'est le second programme qui permet d'envoyer toutes les données pendant 5 min (300s) toutes les 10s.
J'ai créer une boucle qui dure le nombre de cycles qu'il y a de 10 secondes pendant 5 min.
Je calcule le pourcentage et j'écris dans le fichier sur une ligne l'heure où la donnée a été prise ainsi que le pourcentage de places libres.
time.sleep permet de faire la fonction toute les 10s.
"""

import time

def corum():
    verif=0
    response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
    data = response.json()
    for parking in data:
        ouvert=parking.get("status",{}).get("value")
        nom_corum=parking.get("name", {}).get("value")
        if ouvert=="Open" and nom_corum=="Corum":
            libres=parking.get("availableSpotNumber",{}).get("value")
            total=parking.get("totalSpotNumber",{}).get("value")
            verif+=1
    if verif==1:           
        return libres,total
    print('Le parking Corum est fermé.')
    return None,None   

#corum()

def corum_time():
    duree=300
    i= 10 
    with open("corum_time.txt", "w") as fichier:
        nbr = duree // i
        for x in range(nbr):
            libres, total = corum()
            if libres is not None and total is not None:
                pourcentage = round(libres/total*100,2)         
                fichier.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Places libres : {pourcentage}%\n")
                print(f"Places libres à {time.strftime('%H:%M:%S')} : {pourcentage}%")
            else:
                fichier.write('Le parking n\'est pas ouvert')
                print("Le parking n'est pas ouvert.")
            time.sleep(i)


#corum_time()

#9)
"""
Cette fonction enregistre dans un fichier, pour chaque parking son pourcentage de places libres pour un échantillon, une durée et le nom du fichier donné.
Pour réaliser ce programme je passe en paramètres la durée de l'échantillonage, la durée de l'acquisition ainsi que le nom du fichier (pas besoin de mettre l'extension)
Attention, il faut rentrer les valeurs en secondes (1min = 60s) !
J'ai combiné la fonction exo2 avec celle corum_time afin d'obtenir le résultat suivant.
"""


def exo9(Te,duree,fichier):
    places={}
    nom_fichier=str(fichier)+'.txt'
    nbr = duree // Te
    with open(nom_fichier, "w") as fichier:
        for x in range(nbr):
            response=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
            data = response.json()
            for parking in data:
                ouvert=parking.get("status",{}).get("value")
                libres=None
                total=None
                if ouvert=="Open":
                    libres=parking.get("availableSpotNumber",{}).get("value")
                    total=parking.get("totalSpotNumber",{}).get("value")
                    pourcentage=round(libres/total*100,2)
                    nom=parking.get("name",{}).get("value")
                    places[nom]=pourcentage
                if libres is not None and total is not None:        
                    fichier.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Places libres : {pourcentage}% pour le parking {nom}\n")
                    print(f"Places libres à {time.strftime('%H:%M:%S')} : {pourcentage}% pour le parking {nom}.")
                else:
                    fichier.write(f'Le parking {nom} n\'est pas ouvert')
                    print(f"Le parking {nom} n'est pas ouvert.")
            fichier.write('\n')
            print('\n')
            time.sleep(Te)

#exo9(5,15,'test')

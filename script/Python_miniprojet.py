import Programme_TP1
import Formules_Python_DM
import requests
import json
import time

response1=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
data_parking=response1.json()
response2=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
data_velo=response2.json()

#Programme_TP1.exo2()

def velo(Te,duree,fichier):
    places={}
    nom_fichier=str(fichier)+'.txt'
    nbr = duree // Te
    with open(nom_fichier, "w") as fichier:
        for x in range(nbr):
            for velo in data_velo:
                libres=velo.get("freeSlotNumber",{}).get("value")
                occupe=velo.get("availableBikeNumber",{}).get("value")               
                nom=velo.get("address",{}).get("value",{}).get("streetAddress")
                if occupe==0:
                    pourcentage=100
                else:
                    pourcentage=round(libres/(libres+occupe)*100,2)
                places[nom]=pourcentage      
                fichier.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Places libres : {pourcentage}% pour la rue {nom}\n")
                print(f"Places libres à {time.strftime('%H:%M:%S')} : {pourcentage}% pour la rue {nom}.")               
            fichier.write('\n')
            print('\n')
            time.sleep(Te)

#velo(5,15,"velo_test")

def moyenne(dic):
    somme=0
    for cle,val in dic.items():
        somme+=val
    return round(somme/len(dic),2)


def velo_parking(Te,duree,fichier):
    places={}
    moy_des_moy_velo=[]
    moy_des_moy_voitures=[]
    nom_fichier=str(fichier)+'.txt'
    nbr = duree // Te
    i=0
    T=[]
    with open(nom_fichier, "w") as fichier:
        for x in range(nbr):
            response1=requests.get("https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000")
            data_parking=response1.json()
            response2=requests.get("https://portail-api-data.montpellier3m.fr/bikestation?limit=1000")
            data_velo=response2.json()
            for velo in data_velo:
                libres=velo.get("freeSlotNumber",{}).get("value")
                occupe=velo.get("availableBikeNumber",{}).get("value")               
                nom=velo.get("address",{}).get("value",{}).get("streetAddress")
                if occupe==0:
                    pourcentage=100
                else:
                    pourcentage=round(libres/(libres+occupe)*100,2)
                places[nom]=pourcentage      
                fichier.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Places libres : {pourcentage}% pour la rue {nom}\n")              
            fichier.write('\n')
            moy=moyenne(places)
            moy_des_moy_velo.append(moy)
            fichier.write(f'Il y a en moyenne : {moy}% de places libres pour les vélos.\n')
            fichier.write('\n')
            places={}
            for parking in data_parking:
                ouvert=parking.get("status",{}).get("value")
                libres=None
                total=None
                nom=parking.get("name",{}).get("value")
                if ouvert=="Open" or ouvert=="Full":
                    libres=parking.get("availableSpotNumber",{}).get("value")
                    total=parking.get("totalSpotNumber",{}).get("value")
                    pourcentage=round(libres/total*100,2)
                    places[nom]=pourcentage
                if libres is not None and total is not None:        
                    fichier.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Places libres : {pourcentage}% pour le parking {nom}\n")
                else:
                    fichier.write(f'Le parking {nom} n\'est pas ouvert')
            fichier.write('\n')
            moy=moyenne(places)
            moy_des_moy_voitures.append(moy)
            fichier.write(f'Il y a en moyenne : {moy}% de places libres pour les parkings de voitures.\n')
            fichier.write('\n')
            fichier.write('\n')
            fichier.write('\n')
            i+=1
            print(i)
            timestamp = time.time()
            local_time = time.localtime(timestamp)
            date_formattee = time.strftime("%d/%m/%Y %H:%M:%S", local_time)
            T.append(str(date_formattee))
            time.sleep(Te)
        Formules_Python_DM.courbe(T,moy_des_moy_voitures,'Pourcentage de places libres dans tous les parkings de Montpellier','Date','Places libres (en %)')
        Formules_Python_DM.courbe(T,moy_des_moy_velo,'Pourcentage de places libres dans tous les vélomaggs de Montpellier','Date','Places libres (en %)')
        pre=Formules_Python_DM.moyenne(moy_des_moy_velo)
        fichier.write(f'Il y a dans cette période en moyenne : {pre}% de places libres pour les vélos.\n')
        deu=Formules_Python_DM.moyenne(moy_des_moy_voitures)
        fichier.write(f'Il y a dans cette période en moyenne : {deu}% de places libres pour les parkings de voitures.')
        
    print('fini')
velo_parking(5,15,"graphe_test")



response_historique=requests.get("https://portail-api-data.montpellier3m.fr/parking_timeseries/urn%3Angsi-ld%3Aparking%3A001/attrs/availableSpotNumber?fromDate=2025-01-06T00%3A00%3A00&toDate=2025-01-12T23%3A59%3A59")
data_historique=response_historique.json()

def min_historique():
    dic={}
    liste_date=data_historique.get("index")
    liste_val=data_historique.get("values")
    for date,val in zip(liste_date,liste_val):
        dic[date]=val
    dic_min={}
    for x in range(10):
        date_min=liste_date[x]
        val_min=liste_val[x]
        for cle,val in dic.items():
            if val<val_min:
                val_min=val
                date_min=cle
        del dic[date_min]
        dic_min[date_min]=val_min
    return dic_min

def max_historique():
    dic={}
    liste_date=data_historique.get("index")
    liste_val=data_historique.get("values")
    for date,val in zip(liste_date,liste_val):
        dic[date]=val
    dic_max={}
    for x in range(10):
        date_max=liste_date[x]
        val_max=liste_val[x]
        for cle,val in dic.items():
            if val>=val_max:
                val_max=val
                date_max=cle
        del dic[date_max]
        dic_max[date_max]=val_max
    return dic_max

#print(min_historique()) #Cela signifie que sur une semaine, le moins de places libres c'est le samedi.
#print(max_historique()) #Cela signifie que sur une semaine, le plus de places libres c'est le dimanche.

url='https://portail-api-data.montpellier3m.fr/parking_timeseries/urn%3Angsi-ld%3Aparking%3A001/attrs/availableSpotNumber?fromDate=2023-01-01T00%3A00%3A00&toDate=2023-12-31T23%3A59%3A59'


def min_historique_tout_les_parkings():  
    liste_num=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","22","24"]
    for i in liste_num:
        nom='https://portail-api-data.montpellier3m.fr/parking_timeseries/urn%3Angsi-ld%3Aparking%3A0'+str(i)+'/attrs/availableSpotNumber?fromDate=2023-01-01T00%3A00%3A00&toDate=2023-12-31T23%3A59%3A59'
        fichier=requests.get(nom)
        fichier_data=fichier.json()
        dic={}
        dic_min={}
        liste_date=fichier_data.get("index")
        liste_val=fichier_data.get("values")
        for date,val in zip(liste_date,liste_val):
            dic[date]=val
        dic_min['parking']=i
        for x in range(2):
            date_min=liste_date[0]
            val_min=liste_val[0]
            for cle,val in dic.items():
                if val<=val_min:
                    val_min=val
                    date_min=cle
            del dic[date_min]
            dic_min[date_min]=val_min
        print(dic_min)
    return dic_min

def max_historique_tout_les_parkings():
    liste_num=["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","22","24"]
    for i in liste_num:
        nom='https://portail-api-data.montpellier3m.fr/parking_timeseries/urn%3Angsi-ld%3Aparking%3A0'+str(i)+'/attrs/availableSpotNumber?fromDate=2023-01-01T00%3A00%3A00&toDate=2023-12-31T23%3A59%3A59'
        fichier=requests.get(nom)
        fichier_data=fichier.json()
        dic={}
        dic_max={}
        liste_date=fichier_data.get("index")
        liste_val=fichier_data.get("values")
        for date,val in zip(liste_date,liste_val):
            dic[date]=val
        dic_max['parking']=i
        for x in range(2):
            date_max=liste_date[0]
            val_max=liste_val[0]
            for cle,val in dic.items():
                if val>val_max:
                    val_max=val
                    date_max=cle
            del dic[date_max]
            dic_max[date_max]=val_max
        print(dic_max)
    return dic_max

#min_historique_tout_les_parkings()
#max_historique_tout_les_parkings()

#Les Parkings à vélos sont souvent libres s'ils sont à côté de parkings à voitures.
#Les parkings à vélos sont souvent pleins s'ils sont proche du tramway.

def renvoi_courbe():
    dico_places=Programme_TP1.exo4()
    liste_noms=[]
    liste_valeurs=[]
    for cle,val in dico_places.items():
        liste_noms.append(cle)
        liste_valeurs.append(val)
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    date_formattee = time.strftime("%d/%m/%Y %H:%M", local_time)
    Formules_Python_DM.courbe(liste_noms,liste_valeurs,'Pourcentage de places libres dans les parkings de Montpellier le '+str(date_formattee),'Noms des parkings','Places libres (en %)')

#renvoi_courbe()

def courbe_pourcentage_velo():
    places_velo={}
    liste_noms=[]
    liste_valeurs=[]
    for velo in data_velo:
        libres=velo.get("freeSlotNumber",{}).get("value")
        occupe=velo.get("availableBikeNumber",{}).get("value")
        nom=velo.get("address",{}).get("value",{}).get("streetAddress")
        if occupe==0:
            pourcentage=100
        else:
            pourcentage=round(libres/(libres+occupe)*100,2)
        places_velo[nom]=pourcentage
    for cle,val in places_velo.items():
        liste_noms.append(cle)
        liste_valeurs.append(val)
    timestamp = time.time()
    local_time = time.localtime(timestamp)
    date_formattee = time.strftime("%d/%m/%Y %H:%M", local_time)
    Formules_Python_DM.courbe(liste_noms,liste_valeurs,'Pourcentage de places libres dans les vélomaggs de Montpellier le '+str(date_formattee),'Rue des vélomaggs','Places libres (en %)')

#courbe_pourcentage_velo()



"""
def vrai_courbe_voiture():
    liste_num=["01","02","03","04","05","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","24","25"]
    date=["06"]
    liste_moy=[]
    T=[]
    for i in liste_num:
        nom='https://portail-api-data.montpellier3m.fr/parking_timeseries/urn%3Angsi-ld%3Aparking%3A0'+str(i)
        for j in date:
            nom=str(nom)+'/attrs/availableSpotNumber?fromDate=2025-01-'+str(j)+'T00%3A00%3A00&toDate=2025-01-'+str(j)+'T23%3A59%3A59'
            fichier=requests.get(nom)
            fichier_data=fichier.json()
            dic={}
            liste_date=fichier_data.get("index")
            liste_val=fichier_data.get("values")
            liste_moy.append(Formules_Python_DM.moyenne(liste_val))
            T.append(liste_date[0])
    Formules_Python_DM.courbe(T,liste_moy,'Nombre de places libres dans les parkings de Montpellier','Date','Places libres')

vrai_courbe_voiture()

C'est nul cette fonction
"""

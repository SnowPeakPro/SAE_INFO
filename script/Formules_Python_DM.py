import matplotlib.pyplot as plt
from math import sqrt


T=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
L1=[3,3,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,8,7,4]
L2=[103,203,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,-92,-93,-96]


#Fonction de calcul de la moyenne.
#La fonction moyenne prend en paramètre une liste. Ensuite, on divise la somme des nombres de cette liste par la quantité de nombres dans la liste.
#La fonction round permet d'arrondir le résultat, ici à deux chiffres après la virgule.

def moyenne(liste):
    return round(sum(liste)/len(liste),2)

#Fonction de calcul de la variance.
#La fonction variance prend en paramètre une liste. Dans cette fonction, on va 
#calculé la moyenne grâce à la fonction précédente. Puis on va prendre toutes les valeurs de la liste et
#la soustraire à la moyenne pour l'élevé au carré et j'ajoute ces résultats dans une liste.
#Enfin je divise la somme des valeurs de la nouvelle liste var et je la divise par le nombre de valeurs de la liste.

def variance(liste):
    var=[]
    moy=moyenne(liste)
    for i in liste:
        x=(i-moy)**2
        var.append(x)
    return round(sum(var)/len(liste),2)

#Fonction de l'écart-type.
#Je mets en parametre de la fonction ecart une liste.
#Dans la fonction, j'utilise le résultat de la fonction précédente et je l'a met
# à la racine carré grâce à la bibliothèque math.

def ecart(liste):
    return round(sqrt(variance(liste)),2)

#Fonction de calcul de la covariance.
#La fonction covariance prend en paramètre deux listes de même taille.
#Dans un premier temps on calcule la moyenne des deux listes grâce à la précédente fonction moyenne
#Ensuite, on créer une liste vide dans laquelle on va ajouter (Xi - moy_x)*(Yi - moy_y)
#Pour cela j'utilise la fonction zip qui permet de combiner plusieurs itérateurs

def covariance(x,y):
    moy_x=moyenne(x)
    moy_y=moyenne(y)
    cov=[]
    for i,j in zip(x,y):
        valeur=(i-moy_x)*(j-moy_y)
        cov.append(valeur)
    return round(sum(cov)/len(x),2)

#Fonction de calcul du coefficient de corrélation
#La fonction correlation calcule le quotient entre la covalence des deux listes en paramètres
#avec la multiplication des deux écarts types des listes.

def correlation(x,y):
    cov=covariance(x,y)
    ecart_x=ecart(x)
    ecart_y=ecart(y)
    return round(cov/(ecart_x*ecart_y),2)



#Fonction de la matrice
#La fonction matrice prend en paramètre la liste des liste et la liste des noms des listes. Dans un premier temps créer une matrice carrée vide de la taille de la liste
#de tous les paramètres. Ensuite on ajoute dans la matrice lignes par ligne les valeurs des coefficient de corrélation pour chaque paramètres.
#Evidemment pour que à l'affichage on comprenne, on ajoute le nom de chaque liste en paramètre devant.
#Enfin la dernière boucle for ajoute une ligne pour que les noms apparaissent en bas.
#Je créer ensuite une fonction affichematrice pour afficher la matrice de manière plus lisible.
#Pour ce faire je met en paramètre une matrice et je la parcours en affichant son contenu ligne par ligne.


listes = [L1,L2,T]
noms = ["L1", "L2", "T"]

def matrice(liste,nom):
    matr=[]
    z=0
    for i in range(len(liste)+1):
        matr.append([])
    for x in liste:
        matr[z].append(nom[z])
        for y in liste:
            coef=correlation(x,y)
            matr[z].append(coef)
        z+=1
    matr[z].append("  ")
    for val in nom:
        matr[z].append(val)
        matr[z].append(" ")       
    return matr


def affichematrice(matr):
    for i in range(len(matr)):
        for j in range(len(matr[i])):
            print(matr[i][j],end=" ")
        print() 

#print(matrice(listes,noms))
#affichematrice(matrice(listes,noms))


#Fonction de la courbe
#Pour faire fonctionner la fonction, il faut entrer en paramètres la liste pour l'axe des abcsisses, celle des ordonnees, le titre du graphe, le nom de l'axe des abcsisse et de l'axe des ordonnees.
#Pour créer cette fonction, ne connaissant pas trop matplotlib, j'ai fait des longues recherches sur Internet pour trouver comment créer cette fonction.
#Dans un premier temps je créer la figure en choisissant les dimensions.
#Ensuite, la fonction plot me permet de tracer la courbe sur le graphe. Pour avoir une bonne lecture de la courbe, marker ajoute des points sur à l'endroit des valeurs.
#linestyle permet de dire la courbe est continu et color c'est la couleur
#La boucle permet de placer les valeurs au dessus de leur points en modifiant la valeur en str et en choisissant son emplacement.
#Enfin, title ajoute le titre, xlabel, un nom à l'abcsisse, ylabel un nom à l'ordonnee, grid ajoute des cadrillage sur le graphe, tight_layout ajuste les marges et show affiche le graphe.


def courbe(abscisse, ordonnee, titre, nom_abcsisse, nom_ordonnee):

    plt.figure(figsize=(12, 6))
    plt.plot(abscisse, ordonnee, marker='o', linestyle='-', color='red')
    
    for t, v in zip(abscisse, ordonnee):
        plt.text(t, v+0.3 , str(v), fontsize=9, ha='center', va='bottom')

    plt.title(titre)
    plt.xlabel(nom_abcsisse)
    plt.ylabel(nom_ordonnee)
    plt.xticks(ticks=range(len(abscisse)), labels=abscisse, rotation=90, ha='right', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

#courbe(T,L1,"Evolution de la température","Temps (h)","Température (°C)")


"""
print(f'Voici la moyenne de la liste L1 : {moyenne(L1)}')
print(f'Voici la moyenne de la liste L2 : {moyenne(L2)}')
print(f'Voici le sigma de la liste L1 : {ecart(L1)}')
print(f'Voici le sigma de la liste L2 : {ecart(L2)}')
print(f'Voici la variance de la liste L1 : {variance(L1)}')
print(f'Voici la variance de la liste L2 : {variance(L2)}')
print(f'Voici la covarience entre les deux listes L1 et L2 : {covariance(L1,L2)}')
print(f'Voici le coefficient de correlation entre les deux listes L1 et L2 : {correlation(L1,L2)}')
print('Voici la matrice de correlation entre les listes L1, L2 et T : \n')
affichematrice(matrice(listes,noms))
print('Voici la courbe de l\'évolution de la liste L1 en fonction du temps de la liste T : \n')
courbe(T,L1,"Evolution de la température","Temps (h)","Température (°C)")
print('Voici la courbe de l\'évolution de la liste L2 en fonction du temps de la liste T : \n')
courbe(T,L2,"Evolution de la température","Temps (h)","Température (°C)")
"""
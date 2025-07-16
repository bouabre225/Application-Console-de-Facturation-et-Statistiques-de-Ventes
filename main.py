import sys 
import os
import time
import random
from utils.pdf import generer_facture_pdf
def menu():
    while True:
        print("Menu principal")
        print("1. Consulter un fichier ")
        print("2. Generer une facture")
        print("3.Ajouter une facture")
        print("4. Quitter l'application")

        choix = input("Que voulez-vous faire ?")
        if choix == "1":
            print("function pour generer une facture")
            #fonction pour consulter un fichier
            print("\n\n\n\n")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choix == "2":
            #fonction pour generer une facture
            generer_facture_pdf()
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choix == "3":
            print("function pour ajouter une facture")
            #Fonction pour ajouter une facture
            message= "chargement "
            duree = 3
            for i in range(duree):
                print(message + "." * (i % 4), end="\r")
                time.sleep(1)
                print(" " * 30, end="\r")  # nettoie la ligne
        elif choix == "4":
            print("Bye bye")
            sys.exit()
        else:
            print("Saisie incorrecte. veuillez reessayer")


menu()
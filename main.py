import sys 
import os
import time

def menu():
    while True:
        print("Menu principal")
        print("1. Consulter un fichier ")
        print("2. Generer une facture")
        print("3.Ajouter une facture")
        print("4. Quitter l'application")
        print("5. ")

        choix = input("Que voulez-vous faire ?")
        if choix == "1":
            print("function pour generer une facture")
            #fonction pour consulter un fichier
            print("\n\n\n\n")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif choix == "2":
            print("function pour generer une facture")
            #fonction pour generer une factur
        elif choix == "3":
            print("function pour ajouter une facture")
            #Fonction pour ajputer une factire
        elif choix == "4":
            print("Bye bye")
            sys.exit()
        else:
            print("Saisie incorrecte. veuillez reessayer")

menu()
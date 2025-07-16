import sys
import os
import time
from colorama import init, Fore, Style
import index  

# Initialiser colorama
init(autoreset=True)

def effacer_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_titre(titre):
    print(Fore.CYAN + Style.BRIGHT + "="*50)
    print(Fore.CYAN + Style.BRIGHT + f"{titre.center(50)}")
    print(Fore.CYAN + Style.BRIGHT + "="*50)

def menu():
    while True:
        effacer_console()
        afficher_titre("APPLICATION DE FACTURATION")

        print(Fore.GREEN + "1." + Fore.WHITE + " Consulter un fichier")
        print(Fore.GREEN + "2." + Fore.WHITE + " Générer une facture")
        print(Fore.GREEN + "3." + Fore.WHITE + " Ajouter une facture")
        print(Fore.RED + "4." + Fore.WHITE + " Quitter l'application")

        choix = input(Fore.YELLOW + "\nQue voulez-vous faire ? " + Fore.WHITE)

        if choix == "1":
            index.sous_menu_consultation()
            print(Fore.CYAN + "\nRetour au menu principal dans 2 secondes...")
            time.sleep(2)

        elif choix == "2":
            print(Fore.BLUE + "Fonction pour générer une facture (à implémenter)")
            time.sleep(2)

        elif choix == "3":
            print(Fore.BLUE + "Fonction pour ajouter une facture (à implémenter)")
            time.sleep(2)

        elif choix == "4":
            print(Fore.MAGENTA + "Merci d'avoir utilisé l'application. À bientôt !")
            sys.exit()

        else:
            print(Fore.RED + "Saisie incorrecte. Veuillez réessayer.")
            time.sleep(2)

if __name__ == "__main__":
    menu()

import sys
import time
from utils.pdf import generer_facture_pdf
from colorama import init, Fore, Style
from modules.index import sous_menu_consultation
from utils.effacer import effacer_console
from modules.generate_facture import generer_facture

# Initialiser colorama
init(autoreset=True)

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
            sous_menu_consultation()
            print(Fore.CYAN + "\nRetour au menu principal dans 2 secondes.")
            effacer_console()

        elif choix == "2":
            generer_facture()
            generer_facture_pdf()
            effacer_console()
        elif choix == "3":
            message= "chargement "
            duree = 3
            for i in range(duree):
                print(message + "." * (i % 4), end="\r")
                time.sleep(1)
                print(" " * 30, end="\r")
            print(Fore.BLUE + "Fonction pour générer une facture (à implémenter)")
            effacer_console()

        elif choix == "4":
            print(Fore.MAGENTA + "Merci d'avoir utilisé l'application. À bientôt !")
            effacer_console()
            sys.exit()

        else:
            print(Fore.RED + "Saisie incorrecte. Veuillez réessayer.")

if __name__ == "__main__":
    menu()

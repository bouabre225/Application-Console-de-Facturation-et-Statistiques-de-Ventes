from modules.consultation import afficher_clients, afficher_produits, afficher_cartes
from colorama import init, Fore
import os

# Initialiser Colorama
init(autoreset=True)

def effacer_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def sous_menu_consultation():
    while True:
        effacer_console()
        print(Fore.CYAN + "==== MENU CONSULTATION ====")
        print(Fore.GREEN + "1." + Fore.WHITE + " Afficher les clients")
        print(Fore.GREEN + "2." + Fore.WHITE + " Afficher les produits")
        print(Fore.GREEN + "3." + Fore.WHITE + " Afficher les cartes de fidélité")
        print(Fore.RED + "4." + Fore.WHITE + " Retour menu principal")

        choix = input(Fore.YELLOW + "\nVotre choix : ")

        if choix == "1":
            afficher_clients()
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

        elif choix == "2":
            afficher_produits()
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

        elif choix == "3":
            afficher_cartes()
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")

        elif choix == "4":
            break
        else:
            print(Fore.RED + "Saisie incorrecte.")
            time.sleep(2)




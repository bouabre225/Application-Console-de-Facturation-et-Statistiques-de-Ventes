import sys
import time
from colorama import init, Fore, Style

# Utils
from utils.effacer import effacer_console
from utils.pdf import generer_facture_pdf

# Modules
from modules.index import sous_menu_consultation  # Ange 1
from modules.client import ajouter_client, verifier_code_client  # Membre 2
#from modules.produits_manager import ajouter_produit  # Membre 3
from modules.facture import generer_facture  # Membre 4


# Init colorama
init(autoreset=True)

def afficher_titre(titre):
    print(Fore.CYAN + Style.BRIGHT + "="*60)
    print(Fore.CYAN + Style.BRIGHT + f"{titre.center(60)}")
    print(Fore.CYAN + Style.BRIGHT + "="*60)

def menu():
    while True:
        effacer_console()
        afficher_titre("APPLICATION DE FACTURATION")

        print(Fore.GREEN + "1." + Fore.WHITE + " Consulter un fichier")
        print(Fore.GREEN + "2." + Fore.WHITE + " Générer une facture")
        print(Fore.GREEN + "3." + Fore.WHITE + " Ajouter un produit")
        print(Fore.RED + "4." + Fore.WHITE + " Quitter l'application")

        choix = input(Fore.YELLOW + "\nVotre choix : " + Fore.WHITE)

        if choix == "1":
            sous_menu_consultation()
            input(Fore.LIGHTBLUE_EX + "\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "2":
            facture_data = generer_facture()
            if facture_data:
                generer_facture_pdf(
                    nom_client=facture_data["nom_client"],
                    facture_num=facture_data["numero_facture"],
                    produits=facture_data["produits"],
                    total_ttc=facture_data["total_ttc"]
                )
            input(Fore.GREEN + "\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "3":
            ajouter_produit()
            input(Fore.GREEN + "\nProduit ajouté. Appuyez sur Entrée pour revenir au menu...")

        elif choix == "4":
            print(Fore.MAGENTA + "\nMerci d'avoir utilisé l'application. À bientôt !")
            time.sleep(1)
            sys.exit()

        else:
            print(Fore.RED + "Choix invalide. Veuillez réessayer.")
            time.sleep(2)

if __name__ == "__main__":
    menu()

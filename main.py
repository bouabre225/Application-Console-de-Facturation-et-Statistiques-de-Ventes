import sys
import time
from colorama import init, Fore, Style

from utils.effacer import effacer_console
from utils.pdf import generer_facture_pdf

from modules.index import sous_menu_consultation
from modules.client import ajouter_client, verifier_code_client
from modules.produits_manager import ajouter_produit
from modules.facture import generer_facture

init(autoreset=True)

def afficher_titre(titre):
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + f"{titre.center(60)}")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)

def menu():
    while True:
        effacer_console()
        afficher_titre("APPLICATION DE FACTURATION")

        print(Fore.GREEN + "1." + Fore.WHITE + " Consulter un fichier")
        print(Fore.GREEN + "2." + Fore.WHITE + " Générer une facture")
        print(Fore.GREEN + "3." + Fore.WHITE + " Ajouter un produit")
        print(Fore.RED + "4." + Fore.WHITE + " Quitter l'application")

        choix = input(Fore.YELLOW + "\nVotre choix : " + Fore.WHITE).strip()

        if choix == "1":
            sous_menu_consultation()
            input(Fore.LIGHTBLUE_EX + "\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "2":
            code_client = input(Fore.YELLOW + "Entrez le code du client : ").strip()
            if not verifier_code_client(code_client):
                print(Fore.RED + "Le code client est invalide ou inexistant.")
                input(Fore.YELLOW + "\nAppuyez sur Entrée pour revenir au menu...")
                continue

            produits_commandes = []

            while True:
                code_produit = input("Code du produit (ou 'q' pour terminer) : ").strip()
                if code_produit.lower() == 'q':
                    break

                quantite_str = input("Quantité : ").strip()
                if not quantite_str.isdigit():
                    print(Fore.RED + "Quantité invalide. Entrez un nombre entier positif.")
                    continue

                quantite = int(quantite_str)
                produits_commandes.append({"code_produit": code_produit, "quantite": quantite})

            if len(produits_commandes) == 0:
                print(Fore.RED + "Aucun produit saisi. Facture annulée.")
            else:
                facture_data = generer_facture(code_client, produits_commandes)

                if facture_data:
                    generer_facture_pdf(
                        nom_client=facture_data["nom_client"],
                        facture_num=facture_data["numero_facture"],
                        produits=facture_data["produits"],
                        total_ttc=facture_data["total_ttc"]
                    )

            input(Fore.GREEN + "\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "3":
            try:
                ajouter_produit()
            except Exception as e:
                print(Fore.RED + f"Erreur lors de l'ajout du produit : {e}")
            input(Fore.GREEN + "\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "4":
            print(Fore.MAGENTA + "\nMerci d'avoir utilisé l'application. À bientôt !")
            time.sleep(1)
            sys.exit()

        else:
            print(Fore.RED + "Choix invalide. Veuillez entrer un chiffre entre 1 et 4.")
            time.sleep(2)

menu()

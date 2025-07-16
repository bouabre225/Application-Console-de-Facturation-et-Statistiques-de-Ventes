import pandas as pd
import os
import random
from colorama import init, Fore, Style

# Initialiser Colorama
init(autoreset=True)

# Chemin vers le dossier data
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data')

def lire_fichier_excel(nom_fichier):
    """Lit un fichier Excel depuis le dossier data et retourne un DataFrame."""
    chemin_complet = os.path.join(DATA_PATH, nom_fichier)
    try:
        df = pd.read_excel(chemin_complet)
        return df
    except FileNotFoundError:
        print(Fore.RED + f"Erreur : fichier {nom_fichier} introuvable.")
        return None

def afficher_clients():
    df = lire_fichier_excel('Clients.xlsx')
    if df is not None:
        print(Fore.CYAN + "\n===== Liste des clients =====")
        print(Fore.WHITE + df.to_string(index=False))
        print(Fore.CYAN + "==============================\n")

def afficher_produits():
    df = lire_fichier_excel('Produits.xlsx')
    if df is not None:
        print(Fore.GREEN + "\n===== Liste des produits =====")
        print(Fore.WHITE + df.to_string(index=False))
        print(Fore.GREEN + "===============================\n")

def afficher_cartes():
    df = lire_fichier_excel('Cartes.xlsx')
    if df is not None:
        print(Fore.MAGENTA + "\n===== Liste des cartes de fidélité =====")
        print(Fore.WHITE + df.to_string(index=False))
        print(Fore.MAGENTA + "=========================================\n")


def sous_menu_consultation():
    while True:
        print(Fore.YELLOW + "\n=== Menu Consultation ===")
        print(Fore.BLUE + "1." + Fore.WHITE + " Afficher les clients")
        print(Fore.BLUE + "2." + Fore.WHITE + " Afficher les produits")
        print(Fore.BLUE + "3." + Fore.WHITE + " Afficher les cartes")
        print(Fore.RED + "0." + Fore.WHITE + " Retour")
        choix = input(Fore.CYAN + "Votre choix : ")

        if choix == '1':
            afficher_clients()
        elif choix == '2':
            afficher_produits()
        elif choix == '3':
            afficher_cartes()
        elif choix == '0':
            break
        else:
            print(Fore.RED + "Choix invalide, veuillez réessayer.\n")

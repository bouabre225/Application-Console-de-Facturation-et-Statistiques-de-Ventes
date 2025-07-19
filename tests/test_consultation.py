import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import consultation
from colorama import init, Fore
import os

# Initialiser Colorama
init(autoreset=True)

def test_affichage_clients():
    print(Fore.YELLOW + "\nTest : Affichage des clients")
    consultation.afficher_clients()

def test_affichage_produits():
    print(Fore.YELLOW + "\nTest : Affichage des produits")
    consultation.afficher_produits()

def test_generation_cartes():
    print(Fore.YELLOW + "\nTest : Génération des cartes de fidélité")
    consultation.generer_cartes()

    chemin_cartes = os.path.join(os.path.dirname(__file__), '..', 'data', 'Cartes.xlsx')
    if os.path.exists(chemin_cartes):
        print(Fore.GREEN + f"✅ Fichier 'Cartes.xlsx' bien généré dans {chemin_cartes}")
    else:
        print(Fore.RED + "❌ Fichier 'Cartes.xlsx' non trouvé après génération.")

def test_affichage_cartes():
    print(Fore.YELLOW + "\nTest : Affichage des cartes de fidélité")
    consultation.afficher_cartes()

if __name__ == "__main__":
    test_affichage_clients()
    test_affichage_produits()
    test_generation_cartes()
    test_affichage_cartes()

#fichiers statistiques a parir de client et produit 
import pandas as pd
import os
from colorama import init, Fore, Style
from modules.client import trouver_client_par_code
#from modules.produits_manager import trouver_produit_par_code
from modules.consultation import lire_fichier_excel
from modules.facture import generer_facture
from utils.effacer import effacer_console
from utils.pdf import generer_facture_pdf
import matplotlib.pyplot as plt
import time
import re

init(autoreset=True)

def statistiques_client(): 
    while True:
        effacer_console()
        print(Fore.CYAN + "==== STATISTIQUES D’UN CLIENT ====")
        factures = lire_fichier_excel("Factures.xlsx")
        clients = lire_fichier_excel("Clients.xlsx")

        if clients is None or clients.empty:
            print(Fore.RED + "Aucun client trouvé.")
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
            return

        print(Fore.GREEN + "\n===== Liste des clients =====")
        print(Fore.WHITE + clients.to_string(index=False))
        print(Fore.GREEN + "===============================")

        code = input(Fore.YELLOW + "\nEntrez le code du client : ").strip()

        if factures is None or factures.empty:
            print(Fore.RED + "Aucune facture trouvée.")
        else:
            try:
                factures["date"] = pd.to_datetime(factures["date"])
                factures["mois"] = factures["date"].dt.to_period("M")

                client_factures = factures[
                    (factures["code_client"] == code) | (factures["nom_client"] == code)
                ]

                if client_factures.empty:
                    print(Fore.RED + f"Aucune facture trouvée pour le client '{code}'")
                else:
                    montant_total = client_factures["total_ttc"].sum()
                    print(Fore.GREEN + f"\n💰 Montant total des achats du client '{code}' : {montant_total:.2f} €")

                    # === GRAPHIQUE : Total des achats du client par mois ===
                    achats_mensuels = client_factures.groupby("mois")["total_ttc"].sum()

                    plt.figure(figsize=(8, 5))
                    achats_mensuels.plot(kind="bar", color="mediumslateblue")
                    plt.title(f"Achats mensuels du client '{code}'")
                    plt.xlabel("Mois")
                    plt.ylabel("Montant (€)")
                    plt.grid(axis="y")
                    plt.tight_layout()
                    plt.show()
            except KeyError:
                print(Fore.RED + "Colonne 'code_client' ou 'nom_client' manquante dans Factures.xlsx")

        input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
        break


def statistiques_produit():
    while True:
        effacer_console()
        print(Fore.CYAN + "==== STATISTIQUES PRODUIT PAR MOIS ====")
        factures = lire_fichier_excel("Factures.xlsx")

        if factures is None or factures.empty:
            print(Fore.RED + "Aucune facture trouvée.")
            input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
            return

        if "date" not in factures.columns:
            print(Fore.RED + "La colonne 'date' est manquante dans Factures.xlsx")
            return

        try:
            factures["date"] = pd.to_datetime(factures["date"])
            factures["mois"] = factures["date"].dt.to_period("M")

            grouped = factures.groupby(["mois", "produit"])["quantite"].sum()
            bests = grouped.groupby(level=0).idxmax()  # meilleur produit par mois

            print(Fore.GREEN + "\n📦 Produit le plus vendu par mois :")
            for mois, (mois_val, produit) in bests.items():
                print(Fore.WHITE + f"{mois_val} → {produit}")

            # === GRAPHIQUE : Quantité vendue par produit chaque mois ===
            pivot = grouped.unstack().fillna(0)

            pivot.plot(kind="bar", stacked=True, figsize=(10, 6), colormap="tab20")
            plt.title("Quantités vendues par produit par mois")
            plt.xlabel("Mois")
            plt.ylabel("Quantité")
            plt.legend(title="Produit", bbox_to_anchor=(1.05, 1), loc="upper left")
            plt.tight_layout()
            plt.grid(axis="y")
            plt.show()

        except Exception as e:
            print(Fore.RED + f"Erreur : {e}")

        input(Fore.CYAN + "\nAppuyez sur Entrée pour continuer...")
        break




def statistiques():
    while True:
        effacer_console()
        print(Fore.CYAN + "==== MENU STATISTIQUES ====")
        print(Fore.GREEN + "1." + Fore.WHITE + " Statistiques pour un client")
        print(Fore.GREEN + "2." + Fore.WHITE + " Produit le plus vendu par mois")
        print(Fore.RED + "0." + Fore.WHITE + " Retour menu principal")

        choix = input(Fore.YELLOW + "\nVotre choix : ")

        if choix == "1":
            statistiques_client()
        elif choix == "2":
            statistiques_produit()
        elif choix == "0":
            break
        else:
            print(Fore.RED + "Saisie incorrecte.")
            time.sleep(1)


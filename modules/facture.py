import pandas as pd
from datetime import datetime
import os
from modules.consultation import lire_fichier_excel


# Constantes
TAUX_TVA = 0.18
SEUILS_REDUCTION = {
    100000: 10,
    50000: 5
}

def obtenir_remise(total_ht):
    for seuil, taux in sorted(SEUILS_REDUCTION.items(), reverse=True):
        if total_ht >= seuil:
            return taux
    return 0

def client_a_une_carte(code_client, cartes_df):
    return code_client in cartes_df["code_client"].values

def creer_carte_reduction(code_client, total_ht, cartes_df):
    if not client_a_une_carte(code_client, cartes_df):
        taux = obtenir_remise(total_ht)
        if taux > 0:
            nouveau_numero = str(len(cartes_df) + 1).zfill(6)
            nouvelle_carte = {
                "numero_carte": nouveau_numero,
                "code_client": code_client,
                "taux_reduction": taux
            }
            cartes_df = pd.concat([cartes_df, pd.DataFrame([nouvelle_carte])], ignore_index=True)
            cartes_df.to_excel("data/CartesReduction.xlsx", index=False)
            print(f"Carte de réduction créée ({taux}%) pour le client {code_client}")
    return cartes_df

def generer_facture(code_client, produits_commandes, is_premiere_facture=False):
    clients_df = lire_fichier_excel("Clients.xlsx")
    produits_df = lire_fichier_excel("Produits.xlsx")
    cartes_df = lire_fichier_excel("CartesReduction.xlsx")

    if clients_df is None or clients_df.empty:
        clients_df = pd.DataFrame(columns=["code_client", "nom", "contact", "IFU"])
    if produits_df is None or produits_df.empty:
        produits_df = pd.DataFrame(columns=["code_produit", "libelle", "prix_unitaire"])
    if cartes_df is None or cartes_df.empty:
        cartes_df = pd.DataFrame(columns=["numero_carte", "code_client", "taux_reduction"])

    client = clients_df[clients_df["code_client"] == code_client]
    if client.empty:
        print(f"Erreur : Client {code_client} non trouvé.")
        return None
    
    lignes = []
    total_ht = 0

    for code_produit, quantite in produits_commandes.items():
        produit = produits_df[produits_df["code_produit"] == code_produit]
        if produit.empty:
            print(f"Erreur : Produit {code_produit} non trouvé.")
            continue
        produit = produit.iloc[0]
        libelle = produit["libelle"]
        prix_unitaire = float(produit["prix_unitaire"])
        if prix_unitaire < 0 or quantite < 0:
            print(f"Erreur : Prix unitaire ou quantité invalide pour {code_produit}.")
            return None
        total_ligne = prix_unitaire * quantite
        total_ht += total_ligne
        lignes.append([code_produit, libelle, prix_unitaire, quantite, total_ligne])


    tva = round(total_ht * TAUX_TVA, 2)

    remise = 0
    taux_remise = 0
    if not is_premiere_facture and client_a_une_carte(code_client, cartes_df):
        taux_remise = cartes_df[cartes_df["code_client"] == code_client]["taux_reduction"].iloc[0]
        remise = round(total_ht * (taux_remise / 100), 2)

    total_apres_remise = total_ht - remise
    total_ttc = round(total_apres_remise + tva, 2)

    if is_premiere_facture:
        cartes_df = creer_carte_reduction(code_client, total_ht, cartes_df)

    factures_df = lire_fichier_excel("Factures.xlsx")
    if factures_df is None or factures_df.empty:
        factures_df = pd.DataFrame(columns=["numero_facture"])
        factures_df.to_excel("data/Factures.xlsx", index=False)
        numero_facture = "F0001"
    else:
        numero_facture = f"F{len(factures_df) + 1:04d}"

    nouvelle_facture = pd.DataFrame([{"numero_facture": numero_facture}])
    factures_df = pd.concat([factures_df, nouvelle_facture], ignore_index=True)
    factures_df.to_excel("data/Factures.xlsx", index=False)

    return {
        "nom_client": client["nom"].iloc[0],
        "numero_facture": numero_facture,
        "lignes": lignes,
        "total_ht": total_ht,
        "remise": remise,
        "taux_remise": taux_remise,
        "tva": tva,
        "total_ttc": total_ttc,
        "produits": lignes,
        "date": datetime.now().strftime("%d/%m/%Y")
    }

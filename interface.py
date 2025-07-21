import sys
import os
import time
import re
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from colorama import init, Fore, Style
from modules import index
from utils.effacer import effacer_console
from utils.pdf import generer_facture_pdf
from modules.consultation import afficher_clients, afficher_produits, afficher_cartes, lire_fichier_excel
from modules.index import sous_menu_consultation
from modules.client import ajouter_client, verifier_code_client, generer_code_client, donnees_sont_valides
from modules.produits_manager import ajouter_produit
from modules.facture import generer_facture

init(autoreset=True)

root = tk.Tk()
root.title("APPLICATION DE FACTURATION RETRO")
root.geometry("800x600")
root.configure(bg="black")
FONT = ("Courier", 12)

content_frame = tk.Frame(root, bg="gray20", relief="raised", borderwidth=5)
content_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)

menu_frame = tk.Frame(root, bg="black", width=200)
menu_frame.pack(side=tk.LEFT, fill="y", padx=5, pady=5)

title_label = tk.Label(menu_frame, text="FACTURATION", font=("Courier", 16, "bold"), fg="white", bg="black")
title_label.pack(pady=20)

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_clients():
    clear_content()
    df = afficher_clients()
    if df is not None and not df.empty:
        tree = ttk.Treeview(content_frame, columns=list(df.columns), show="headings")
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))
        tree.pack(fill="both", expand=True, padx=5, pady=5)
    else:
        tk.Label(content_frame, text="AUCUN CLIENT", font=FONT, fg="white", bg="gray20").pack(pady=20)

def show_products():
    clear_content()
    df = lire_fichier_excel('Produits.xlsx')
    if df is not None and not df.empty:
        tree = ttk.Treeview(content_frame, columns=list(df.columns), show="headings")
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))
        tree.pack(fill="both", expand=True, padx=5, pady=5)
    else:
        tk.Label(content_frame, text="AUCUN PRODUIT", font=FONT, fg="white", bg="gray20").pack(pady=20)

def generate_invoice_form():
    clear_content()
    produits_list = []

    tk.Label(content_frame, text="NOUVEAU CLIENT ? (oui/non)", font=FONT, fg="white", bg="gray20").pack()
    nouveau_client_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
    nouveau_client_entry.pack(pady=5)

    def etape_suivante():
        reponse = nouveau_client_entry.get().strip().lower()
        clear_content()

        if reponse == "oui":
            tk.Label(content_frame, text="Nom du client :", font=FONT, fg="white", bg="gray20").pack()
            nom_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
            nom_entry.pack(pady=5)

            tk.Label(content_frame, text="Contact du client :", font=FONT, fg="white", bg="gray20").pack()
            contact_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
            contact_entry.pack(pady=5)

            tk.Label(content_frame, text="IFU (13 chiffres ou vide) :", font=FONT, fg="white", bg="gray20").pack()
            ifu_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
            ifu_entry.pack(pady=5)

            def valider_client():
                nom = nom_entry.get().strip()
                contact = contact_entry.get().strip()
                ifu = ifu_entry.get().strip()

                if not nom or not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nom):
                    messagebox.showerror("Erreur", "Nom invalide.")
                    return
                if not contact or not contact.isdigit():
                    messagebox.showerror("Erreur", "Contact invalide.")
                    return
                if ifu and (not ifu.isdigit() or len(ifu) != 13):
                    messagebox.showerror("Erreur", "IFU doit avoir 13 chiffres.")
                    return

                code_client = generer_code_client("data/Clients.xlsx")
                donnees = {
                    "code_client": code_client,
                    "nom": nom,
                    "contact": contact,
                    "IFU": ifu if ifu else None
                }

                if not donnees_sont_valides(donnees):
                    messagebox.showerror("Erreur", "Données invalides.")
                    return

                if not ajouter_client(donnees, "data/Clients.xlsx"):
                    messagebox.showerror("Erreur", "Ajout client échoué.")
                    return

                demander_premiere_facture(code_client)

            tk.Button(content_frame, text="Valider client", font=FONT, bg="gray50", fg="white", command=valider_client).pack(pady=10)

        elif reponse == "non":
            tk.Label(content_frame, text="Code client :", font=FONT, fg="white", bg="gray20").pack()
            code_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
            code_entry.pack(pady=5)

            def verifier_client_existant():
                code = code_entry.get().strip().upper()
                if not verifier_code_client(code, "data/Clients.xlsx"):
                    messagebox.showerror("Erreur", "Code client invalide.")
                    return
                demander_premiere_facture(code)

            tk.Button(content_frame, text="Valider code", font=FONT, bg="gray50", fg="white", command=verifier_client_existant).pack(pady=5)
        else:
            messagebox.showerror("Erreur", "Veuillez répondre par 'oui' ou 'non'.")

    def demander_premiere_facture(code_client_final):
        clear_content()
        tk.Label(content_frame, text="Première facture ? (oui/non)", font=FONT, fg="white", bg="gray20").pack()
        premiere_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
        premiere_entry.pack(pady=5)

        def valider_facture():
            is_premiere = premiere_entry.get().strip().lower() == "oui"
            demander_produits(code_client_final, is_premiere)

        tk.Button(content_frame, text="Continuer", font=FONT, bg="gray50", fg="white", command=valider_facture).pack(pady=5)

    def demander_produits(code_client_final, is_premiere):
        clear_content()
        tk.Label(content_frame, text="Code produit :", font=FONT, fg="white", bg="gray20").pack()
        code_prod_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
        code_prod_entry.pack(pady=5)

        tk.Label(content_frame, text="Quantité :", font=FONT, fg="white", bg="gray20").pack()
        quantite_entry = tk.Entry(content_frame, font=FONT, bg="gray80", fg="black")
        quantite_entry.pack(pady=5)

        def ajouter_et_continuer():
            code_p = code_prod_entry.get().strip().upper()
            qte = quantite_entry.get().strip()
            if not qte.isdigit() or int(qte) <= 0:
                messagebox.showerror("Erreur", "Quantité invalide.")
                return
            produits_list.append({"code_produit": code_p, "quantite": int(qte)})
            demander_produits(code_client_final, is_premiere)

        def terminer_facture():
            if not produits_list:
                messagebox.showerror("Erreur", "Aucun produit ajouté.")
                return
            prod_dict = {p["code_produit"]: p["quantite"] for p in produits_list}
            facture = generer_facture(code_client_final, prod_dict, is_premiere)
            if facture:
                generer_facture_pdf(
                    nom_client=facture["nom_client"],
                    facture_num=facture["numero_facture"],
                    produits=facture["produits"],
                    total_ttc=facture["total_ttc"]
                )
                messagebox.showinfo("Succès", f"Facture générée: {facture['numero_facture']}")
            else:
                messagebox.showerror("Erreur", "Erreur lors de la génération.")

        tk.Button(content_frame, text="Ajouter produit", font=FONT, bg="gray50", fg="white", command=ajouter_et_continuer).pack(pady=5)
        tk.Button(content_frame, text="Terminer facture", font=FONT, bg="gray50", fg="white", command=terminer_facture).pack(pady=5)

    tk.Button(content_frame, text="Valider", font=FONT, bg="gray50", fg="white", command=etape_suivante).pack(pady=10)

tk.Button(menu_frame, text="1. Clients", font=FONT, bg="gray50", fg="white", width=15, anchor="w", command=show_clients).pack(pady=5, padx=5)
tk.Button(menu_frame, text="2. Produits", font=FONT, bg="gray50", fg="white", width=14, anchor="w", command=show_products).pack(pady=5, padx=5)
tk.Button(menu_frame, text="3. Générer Facture", font=FONT, bg="gray50", fg="white", width=17, anchor="w", command=generate_invoice_form).pack(pady=5, padx=5)
tk.Button(menu_frame, text="4. Quitter", font=FONT, bg="red", fg="white", width=15, anchor="w", command=root.quit).pack(pady=5, padx=5)

root.mainloop()

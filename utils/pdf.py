from fpdf import FPDF
from datetime import datetime
from num2words import num2words
import os

class FacturePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, "Groupe :", ln=1)
        noms = [
            "ANAGONOU Richard",
            "BOUDZOUMOU Florent",
            "KORE Ange",
            "SISSO Lionel",
            "ODJO Immaculee"
        ]

        for nom in noms:
            self.cell(0, 7, nom, ln=1)

        self.ln(2) 
        self.set_font("Arial", "", 11)
        self.cell(0, 8, f"Date : {datetime.now().strftime('%d/%m/%Y')}", ln=1, align="R")

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "Merci de votre confiance !", 0, 0, "C")

def generer_facture_pdf(nom_client, facture_num, produits, total_ttc, fichier_pdf="facture.pdf"):
    try:
        montant_en_lettres = num2words(total_ttc, lang="fr").capitalize() + " francs CFA"
    except Exception as e:
        print(f"Erreur lors de la conversion du montant en lettres : {e}")
        montant_en_lettres = "Montant non convertible en lettres"

    pdf = FacturePDF()
    pdf.add_page()

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Client : {nom_client}", ln=1)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"FACTURE N° {facture_num}", ln=1, align="C")

    pdf.set_font("Arial", "B", 11)
    pdf.cell(30, 10, "Code", 1)
    pdf.cell(60, 10, "Libellé", 1)
    pdf.cell(25, 10, "PU", 1)
    pdf.cell(20, 10, "Qté", 1)
    pdf.cell(35, 10, "Total HT", 1, ln=1)

    pdf.set_font("Arial", "", 11)
    for code, libelle, pu, quantite, total_ht in produits:
        pdf.cell(30, 10, code, 1)
        pdf.cell(60, 10, libelle, 1)
        pdf.cell(25, 10, f"{pu:.2f}", 1)
        pdf.cell(20, 10, str(quantite), 1)
        pdf.cell(35, 10, f"{total_ht:.2f}", 1, ln=1)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total TTC : {total_ttc:.2f} FCFA", ln=1, align="R")

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, f"Arrêtée, la présente facture à la somme de : {montant_en_lettres}")

    output_path = os.path.join("factures", f"facture_{facture_num}.pdf")
    try:
        pdf.output(output_path)
        print(f"La facture a été générée avec succès : {output_path}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du PDF : {e}")
    return output_path
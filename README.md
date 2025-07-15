# 💼 Application Console de Facturation et Statistiques de Ventes (Python)

## 🎓 Objectif pédagogique

Ce projet a été réalisé dans le cadre d’un apprentissage de la manipulation de fichiers Excel, de l’utilisation des DataFrames avec la bibliothèque **Pandas**, et de la production de **factures automatisées**. Il vise à :

- Consolider les bases de Python appliqué à un projet complet
- Gérer des fichiers Excel comme source de données dynamique
- Générer des documents PDF (factures)
- Travailler en équipe avec répartition claire des tâches

---

## 🗃️ Données utilisées

L'application utilise **trois fichiers Excel** comme base de données :

1. **Clients.xlsx**
   - `code_client` : identifiant unique
   - `nom` : nom du client
   - `contact` : téléphone ou email
   - `IFU` : identifiant fiscal unique (13 caractères)

2. **Produits.xlsx**
   - `code_produit` : 6 caractères
   - `libelle` : nom du produit
   - `prix_unitaire` : prix en devise locale

3. **CartesReduction.xlsx**
   - `numero_carte` : identifiant de la carte
   - `code_client` : lien avec le client
   - `taux_reduction` : pourcentage

> ⚠️ Les fichiers initiaux contiennent : **10 produits** et **2 clients**

---

## 📋 Fonctionnalités de l'application

### 🔹 Menu principal (console)

```text
1. Consulter un fichier
2. Générer une facture
3. Ajouter un produit
4. Quitter

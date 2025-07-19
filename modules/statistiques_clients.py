#fichiers statistiques a parir de client et produit 
import pandas as pd
import os
from colorama import init, Fore, Style
from modules.client import trouver_client_par_code
from modules.produits_manager import trouver_produit_par_code
from modules.consultation import lire_fichier_excel
from modules.facture import generer_facture
from utils.effacer import effacer_console
import time
import re

init(autoreset=True)


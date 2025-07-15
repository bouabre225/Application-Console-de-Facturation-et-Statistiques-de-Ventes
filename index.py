from modules import consultation 
from colorama import init, Fore

# Initialiser Colorama
init(autoreset=True)

def menu_principal():
    while True:
        print(Fore.YELLOW + "\n=== Menu Principal ===")
        print(Fore.BLUE + "1." + Fore.WHITE + " Consultation")
        print(Fore.RED + "0." + Fore.WHITE + " Quitter")
        choix = input(Fore.CYAN + "Votre choix : ")

        if choix == '1':
            consultation.sous_menu_consultation()
        elif choix == '0':
            print(Fore.GREEN + "Fermeture de l'application.")
            break
        else:
            print(Fore.RED + "Choix invalide.\n")

if __name__ == "__main__":
    menu_principal()

from getpass import getpass

from manager import Manager
from password import check_strength
from util import Password


def menu():
    while True:
        print("Bienvenue sur le gestionnaire de mots de passe !\n")
        print("1 - Se connecter")
        print("2 - Créer un nouvel utilisateur")
        print("3 - Quitter")
        choice = input("Que voulez-vous faire ?").strip()
        match choice:
            case '1':
                login()
            case '2':
               register()
            case '3':
                "A la prochaine !"
                exit(0)
            case _:
                print("Veuillez faire un choix correct")


def login():
    while True:
        username = input("Nom d'utilisateur: ").strip()
        password = getpass("Veuillez saisir le mot de passe:")
        has_logged_in = manager.login(username, password)
        if has_logged_in:
           user_menu()
        else:
            while True:
                choice = input("Voulez-vous réessayer ? (o/n)").strip()
                if choice == 'o':
                    break
                else:
                    menu()


def register():
    while True:
        username = input("Nom d'utilisateur: ").strip()
        password = getpass("Veuillez saisir le mot de passe:")
        confirm_password = getpass("Veuillez confirmer le mot de passe")

        if password != confirm_password:
            print("Les mots de passe ne correspondent pas !")
        else:
            score, message = check_strength(password)
            print(message)
            if score < 3:
                print("Pour des raisons de sécuritéc, veuillez saisir un mot de passe plus fort")
                while True:
                    confirm = input("Voulez-vous abandonner (o/n)?").strip().lower()
                    if confirm == 'o':
                        menu()
                    elif confirm == 'n':
                       break
            else:
                manager.create_user(username, password)
                while True:
                    confirm = input("Voulez-vous vous connecter avec ce nouveau compte (o/n) ?").strip()
                    if confirm == 'o':
                        manager.login(username, password)
                        user_menu()
                    elif confirm == 'n':
                        menu()

def user_menu():
    while True:
        print("Bienvenue " + manager.user.username + "!\n")
        print("1 - Gérer mes mots de passe")
        print("2 - Se déconnecter")
        choice = input("Que voulez-vous faire ?").strip()
        match choice:
            case '1':
                manage_passwords()
            case '2':
                manager.logout()
                menu()
            case _:
                print("Veuillez faire un choix correct")
                continue

def add_password():
    while True:
        label = input("Veuillez donner le libelle: ").strip()
        password = getpass("Veuillez saisir le mot de passe:")
        confirm_password = getpass("Confirmez le mot de passe:")

        if password != confirm_password:
            print("Les mots de passe ne correspondent pas !")
            continue

        score, message = check_strength(password)
        print(message)

        if score < 3:
            while True:
                response = input("Voulez-vous quand meme ajouter ce mot de passe (o/n) ?").strip().lower()
                if response == 'o':
                    manager.add_password(label, password)
                    manage_passwords()
                elif response == 'n':
                    break

def update_password(password_id:str):
    while True:
        password = getpass("Veuillez saisir le mot de passe:")
        confirm_password = getpass("Confirmez le mot de passe:")

        if password != confirm_password:
            print("Les mots de passe ne correspondent pas !")
            continue

        score, message = check_strength(password)
        print(message)

        if score < 3:
            while True:
                response = input("Voulez-vous quand meme ajouter ce mot de passe (o/n) ?").strip().lower()
                if response == 'o':
                    manager.update_password(password_id, password)
                    return
                elif response == 'n':
                    break

def manage_passwords():
    passwords: dict[str,Password] = {}
    while True:
        print("Liste des mots de passe")
        for password in manager.user.passwords:
            passwords[password.label] = password
            print("- " + password.label)

        print('\n Que voulez-vous faire ?')
        print('1 - Sélectionner un mot de passe')
        print('2 - Ajouter un nouveau mot de passe')
        print('3 - Retour au menu précédent\n')
        choice = input().strip()
        match choice:
            case '1':
                if len(passwords) == 0:
                    print("Aucun mot de passe n'a encore été créé")
                    continue
                can_break = False
                while not can_break:
                    label = input("Veuillez saisir le libellé du mot de passe: ")
                    if label in passwords.keys():
                        can_break = True
                        manage_password(passwords[label])
                    else:
                        print("Mot de passe non existant")
                        while True:
                            response = input("Voulez-vous retourner au menu (o/n) ?").strip().lower()
                            if response == 'o':
                                can_break = True
                                break
                            elif response == 'n':
                                break
            case '2':
                add_password()
            case '3':
                user_menu()
            case _ :
                print("Veuillez faire un choix correct")

def manage_password(password: Password):
    while True:
        print('\n Que voulez-vous faire ?')
        print('1 - Afficher le mot de passe')
        print('2 - Mettre à jour le mot de passe')
        print('3 - Supprimer le mot de passe')
        print('4 - Retour au menu précédent\n')
        choice = input().strip()
        match choice:
            case '1':
               print(password.get_password())
            case '2':
                update_password(password.password_id)
            case '3':
                manager.delete_password(password)
                manage_passwords()
            case '4':
                manage_passwords()
            case _ :
                print("Veuillez faire un choix correct")

if __name__ == '__main__':
    manager = Manager()
    menu()

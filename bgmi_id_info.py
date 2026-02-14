#!/usr/bin/env python3

import requests
import json
import sys
from urllib.parse import unquote
from colorama import init, Fore, Style
import time
import itertools
import threading

init(autoreset=True)

# =====================================
#               BANNER
# =====================================

BANNER = f"""
{Fore.RED}██████╗  ██████╗ ███╗   ███╗██╗
{Fore.YELLOW}██╔══██╗██╔════╝ ████╗ ████║██║
{Fore.GREEN}██████╔╝██║  ███╗██╔████╔██║██║
{Fore.CYAN}██╔══██╗██║   ██║██║╚██╔╝██║██║
{Fore.MAGENTA}██████╔╝╚██████╔╝██║ ╚═╝ ██║██║
{Fore.BLUE}╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝

{Style.BRIGHT}{Fore.CYAN}            BGMI ID INFO
------------------------------------------------
{Fore.WHITE}Developer : Anubhav Kashyap
GitHub/Telegram : @anubhavanonymous
------------------------------------------------
"""

# =====================================
#         SPINNER LOADER
# =====================================

def spinner():
    for char in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write(f"\r{Fore.YELLOW}Fetching data... {char}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r")

# =====================================
#        GET AUTH TOKEN (SAFE)
# =====================================

def get_authorization_token(session):
    url = "https://www.rooter.gg/"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html",
    }

    response = session.get(url, headers=headers)

    user_auth = session.cookies.get("user_auth")
    if not user_auth:
        return None

    try:
        access_token_json = unquote(user_auth)
        access_token_data = json.loads(access_token_json)
        return access_token_data.get("accessToken")
    except:
        return None

# =====================================
#        GET BGMI USER INFO
# =====================================

def get_bgmi_username(user_id):
    global done
    session = requests.Session()

    done = False
    t = threading.Thread(target=spinner)
    t.start()

    access_token = get_authorization_token(session)

    if not access_token:
        done = True
        print(f"{Fore.RED}[!] Failed to get access token.")
        return

    url = f"https://bazaar.rooter.io/order/getUnipinUsername?gameCode=BGMI_IN&id={user_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Device-Type": "web",
        "App-Version": "1.0.0",
        "Device-Id": "cli-tool",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = session.get(url, headers=headers)
    done = True
    t.join()

    try:
        data = response.json()

        if data.get("transaction") == "SUCCESS":
            print(f"\n{Fore.GREEN}{Style.BRIGHT}=========== RESULT ===========")
            print(f"{Fore.CYAN}[✓] Username : {Fore.YELLOW}{data['unipinRes']['username']}")
            print(f"{Fore.CYAN}[✓] UID      : {Fore.YELLOW}{user_id}")
            print(f"{Fore.CYAN}[✓] Server   : {Fore.YELLOW}BGMI")
            print(f"{Fore.CYAN}[✓] Region   : {Fore.YELLOW}India")
            print(f"{Fore.GREEN}{Style.BRIGHT}==============================\n")
        else:
            print(f"{Fore.RED}[!] Error: {data.get('message', 'Unknown error')}")

    except:
        print(f"{Fore.RED}[!] Invalid response received.")

# =====================================
#               MAIN
# =====================================

def main():
    print(BANNER)

    if len(sys.argv) != 2:
        print(f"{Fore.YELLOW}Usage: python bgmi_id_info.py <BGMI_UID>")
        sys.exit(1)

    user_id = sys.argv[1]
    get_bgmi_username(user_id)

if __name__ == "__main__":
    main()

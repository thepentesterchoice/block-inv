import requests
import json
from bs4 import BeautifulSoup
import argparse
from colorama import Fore, Back, Style
import random
import argparse
agents = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36")
Agent = agents[random.randrange(len(agents))]
headers = {'user-agent': Agent}

def logo():
    print(f"""
{Fore.RED}█▄▄ {Fore.WHITE}█░░ █▀█ █▀▀ █▄▀ █▀▀ ▄▄ █ █▄░█ █░█
{Fore.RED}█▄█ {Fore.WHITE}█▄▄ █▄█ █▄▄ █░█ █▄▄ ░░ █ █░▀█ ▀▄▀ [@thepentesterchoice] [BTC]
---
    """)
def btc_balance(wallet):
    api = f'https://api.blockchair.com/bitcoin/dashboards/address/{wallet}'
    api_r = requests.get(api).json()
    data = json.dumps(api_r)
    data = json.loads(data)
    try:
        return data["data"][wallet]["address"]["balance"]
    except TypeError:
        return "0"
    except:
        pass
def btransaction_details(trid):
    api_btr = f"""https://api.blockchair.com/bitcoin/dashboards/transaction/{trid}"""
    api_btr_r = requests.get(api_btr, headers=headers).json()
    api_btr_dump = json.dumps(api_btr_r)
    api_btr_d = json.loads(api_btr_dump)
    data = api_btr_d["data"][trid]["inputs"]
    size = len(data)
    print(f"{Fore.BLUE}[Sender]{Fore.WHITE}")
    for num in range(0,size):
        wallet = data[num]["recipient"]
        print(f'{Fore.RED}[Wallet]{Fore.WHITE} [{wallet}] ({data[num]["time"]}) {Fore.BLUE}[Transferred Amount: {Fore.RED}{data[num]["value"]}{Fore.BLUE}] {Fore.GREEN}[Current Balance: {Fore.RED}{btc_balance(wallet)}{Fore.GREEN}]{Fore.WHITE}')
    data = api_btr_d["data"][trid]["outputs"]
    size = len(data)
    print(f"{Fore.BLUE}[Recipients]{Fore.WHITE}")
    for num in range(0,size):
        wallet = data[num]["recipient"]
        print(f'{Fore.RED}[Wallet]{Fore.WHITE} [{wallet}] ({data[num]["time"]}) {Fore.BLUE}[Transferred Amount: {Fore.RED}{data[num]["value"]}{Fore.BLUE}] [Current Balance: {Fore.RED}{btc_balance(wallet)}{Fore.GREEN}]{Fore.WHITE}')
    

def bitcoin_history(address):
    api_btc_1 = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}?transaction_details=true"
    api_btc_1_r = requests.get(api_btc_1, headers=headers).json()
    api_btc_1_dump = json.dumps(api_btc_1_r)
    api_btc_1_d = json.loads(api_btc_1_dump)
    print(f"""
{Fore.RED}[ Address ]{Fore.WHITE} [{address}]
{Fore.RED}[ BALANCE ]{Fore.WHITE} {Fore.GREEN}[in_BTC]{Fore.WHITE} [{api_btc_1_d["data"][address]["address"]["balance"]}] {Fore.GREEN}[in_USD]{Fore.WHITE} [{api_btc_1_d["data"][address]["address"]["balance_usd"]}]
{Fore.RED}[ Recived ]{Fore.WHITE} {Fore.GREEN}[in_BTC]{Fore.WHITE} [{api_btc_1_d["data"][address]["address"]["received"]}] {Fore.GREEN}[in_USD]{Fore.WHITE} [{api_btc_1_d["data"][address]["address"]["received_usd"]}] {Fore.BLUE}(Time:- {api_btc_1_d["data"][address]["address"]["first_seen_receiving"]}{Fore.RED} - {Fore.BLUE}{api_btc_1_d["data"][address]["address"]["last_seen_receiving"]}){Fore.WHITE}
{Fore.RED}[ Sent    ]{Fore.WHITE} {Fore.GREEN}[in_BTC]{Fore.WHITE} [{api_btc_1_d["data"][address]["address"]["spent"]}] {Fore.GREEN}[in_USD]{Fore.WHITE} [{api_btc_1_d["data"][address]["address"]["spent_usd"]}] {Fore.BLUE}(Time:- {api_btc_1_d["data"][address]["address"]["first_seen_spending"]}{Fore.RED} - {Fore.BLUE}{api_btc_1_d["data"][address]["address"]["last_seen_spending"]}){Fore.WHITE}
{Fore.RED}[ Total Transaction ]{Fore.WHITE} [{api_btc_1_d["data"][address]["address"]["transaction_count"]}]      
-------
{Fore.RED}* {Fore.GREEN}Transaction History{Fore.RED} *{Fore.WHITE}
    """)
    for trans in api_btc_1_d["data"][address]["transactions"]:
        balance=str(trans["balance_change"])
        if "-" in balance:
            hash = trans["hash"]
            print(f"""
{Fore.LIGHTGREEN_EX}[Sent History]
{Fore.RED}[Transc. HASH] {Fore.BLUE} [{hash}]
{Fore.RED}[Sent        ] {Fore.BLUE} [{trans["balance_change"]}] {Fore.GREEN} [in] {Fore.WHITE} [{trans["time"]}]
            """)
            btransaction_details(hash)

        else:
            hash = trans["hash"]
            print(f"""
{Fore.LIGHTGREEN_EX}[Recived HISTORY]
{Fore.RED}[Transc. HASH  ] {Fore.BLUE} [{trans["hash"]}]
{Fore.RED}[Recived       ] {Fore.BLUE} [{trans["balance_change"]}] {Fore.GREEN} [in] {Fore.WHITE} [{trans["time"]}]
            """)
            btransaction_details(hash)

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", help="Enter The bitcoin wallet address ex: -a '3NrmFTx3uwfWFW2ABCD4doT5ZYYFJABCD' ", type=str)
    args = parser.parse_args()
    address = args.address
    logo()
    bitcoin_history(address)
except TypeError:
    print("Type -h To See all the options")
except():
    exit()

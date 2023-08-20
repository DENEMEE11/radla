import time
from hdwallet import HDWallet
from hdwallet.symbols import BTG as SYMBOL
from hexer import mHash
import requests
from colorama import init, Fore, Back, Style
import lxml.html as lh
from concurrent.futures import ThreadPoolExecutor

# Set the title of the console window
def set_console_title(title):
    print("\033]0;" + title + "\007", end="")  # This sets the terminal title

init()

def get_bal(addr):
    url = str('https://bgold.atomicwallet.io/address/' + str(addr))
    response = requests.get(url)
    doc = lh.fromstring(response.content)
    tr_elements = doc.xpath('/html/body/main/div/div[2]/div[1]/table/tbody/tr[1]/td[2]')
    bal = tr_elements[0].text_content()
    return bal

def process_address(hex64):
    PRIVATE_KEY: str = hex64
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL)
    hdwallet.from_private_key(private_key=PRIVATE_KEY)
    priv = hdwallet.private_key()
    addr = hdwallet.p2sh_address()
    xtxid = get_bal(addr)
    
    if xtxid == '0 BTG':
        print(Fore.RED, 'ADRES:', str(addr), 'PRİVATE KEY:', str(priv), 'BALLANCE:', str(xtxid), Style.RESET_ALL)
    else:
        print(Fore.GREEN, 'ADRES:', str(addr), 'PRİVATE KEY:', str(priv), 'BALLANCE:', str(xtxid), Style.RESET_ALL)

        ifer = '0 BTG'
        if str(xtxid) != str(ifer):
            hit_info = f"ADRES: {addr} PRİVATE KEY: {priv} BALLANCE: {xtxid}\n"
            with open("hits.txt", "a") as f:
                f.write(hit_info)
                f.write("PRİVATE KEY = " + str(priv))
                f.write("\n================[DΞİTY#5637]================")

def main():
    set_console_title("BTG Wallet Miner - Checked: 0 | EARN: 0 BTG ~ 0₺")

    with ThreadPoolExecutor(max_workers=50) as executor:
        while True:
            hex64_list = [mHash() for _ in range(400)]
            for hex64 in hex64_list:
                executor.submit(process_address, hex64)

if __name__ == "__main__":
    main()

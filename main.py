import time
import multiprocessing
from hdwallet import HDWallet
from hdwallet.symbols import BTG as SYMBOL
from hexer import mHash
import requests
from colorama import init, Fore, Style
import lxml.html as lh

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
        print(Fore.RED, 'ADRES:', str(addr), 'PRİVATE KEY:', str(priv), 'BALANCE:', str(xtxid), Style.RESET_ALL)
    else:
        print(Fore.GREEN, 'ADRES:', str(addr), 'PRİVATE KEY:', str(priv), 'BALANCE:', str(xtxid), Style.RESET_ALL)

def main():
    num_cores = multiprocessing.cpu_count()
    target_cpu_percent = 60
    num_processes = int(num_cores * target_cpu_percent / 100)
    
    pool = multiprocessing.Pool(processes=num_processes)

    while True:
        hex64_list = [mHash() for _ in range(400)]
        pool.map(process_address, hex64_list)
        time.sleep(1)

if __name__ == "__main__":
    main()

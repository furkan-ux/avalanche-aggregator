from updator_joepegs import updator_joepegs
from updator_nftrade import updator_nftrade
from updator_kalao import updator_kalao
from reverse_updator_nftrade import reverse_updator_nftrade
from reverse_updator_kalao import reverse_updator_kalao
from database_initalizer import addAllPrices
from collections_saver import collections_main
from info_collections import info_contracts
from mongo_save import inital_set_attributes,contract_stats_inital
import time

def main():
    print("[DRIVER] Starting...")
    req_input = input("[DRIVER] What do you want to do? (i = initiaize, u =update,r = reverse listeners): ")

    if req_input == "i":
        print("[DRIVER] Initializing...")
        collections_main()
        info_contracts()
        addAllPrices()
        inital_set_attributes()
        contract_stats_inital()

    elif req_input == "u":
        while True:
            print("[DRIVER] Updating...")

            updator_nftrade()
            time.sleep(5)
            updator_kalao()
            time.sleep(5)
            updator_joepegs()
            
            

    elif req_input == "r":
        print("[DRIVER] Reverse listeners...")
        while True:
            reverse_updator_nftrade()
            reverse_updator_kalao()
            time.sleep(5)
if __name__ == "__main__":
    main()

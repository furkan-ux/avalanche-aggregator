import requests
import json
from mongo_save import isContractExist,isTokenExist, tokenPriceUpdate,tokenCreateFromNftrade,nftradeOrderIDUpdate,contract_stats_update,update_attributes,uptade_collection_attributes
from info_collections import info_contracts
from database_initalizer import addForOneContract


def updator_nftrade():
    for i in range(500, -100, -100):
        nftradeURI = "https://api.nftrade.com/api/v1/tokens?limit=50&skip="+str(i)+"&chains[]=43114&search=&order=true&verified=true&sort=listed_desc"
        nftradeREQ = requests.get(nftradeURI, headers={"Referer": "https://nftrade.com/"})
        nftradeJSON = json.loads(nftradeREQ.text)
        print("[NFTRADE] Updating Page", i)
        for keys in nftradeJSON:
            id = keys["contractAddress"] + "-" + str(keys["tokenID"])
            contract_address = keys["contractAddress"]
            token_id = keys["tokenID"]
            price = str(keys["price"])
            nftrade_id = str(keys["id"])
            order_id = keys["orderId"]
            
            if not isContractExist(contract_address):
                    print("[NFTRADE] New Contract: ", contract_address)
                    info_contracts()
                    addForOneContract(contract_address)
                    uptade_collection_attributes(contract_address)

            elif isTokenExist(contract_address, token_id):
                tokenPriceUpdate(contract_address, token_id, price,"nftrade","null")
                nftradeOrderIDUpdate(id, nftrade_id, order_id)
                contract_stats_update(contract_address, price,"listing","exist")

            elif not isTokenExist(contract_address, token_id):
                if isContractExist(contract_address):
                    tokenCreateFromNftrade(keys,"updator")
                    contract_stats_update(contract_address, price,"listing","new")
                    update_attributes(id, contract_address)
                
            else:
                print("[ERROR] Check: ", id)

        

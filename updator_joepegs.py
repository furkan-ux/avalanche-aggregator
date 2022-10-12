import requests
import json
from mongo_save import isContractExist,isTokenExist, tokenPriceUpdate, tokenCreateFromJoePegs,contract_stats_update,update_attributes,uptade_collection_attributes
from info_collections import info_contracts
from database_initalizer import addForOneContract

def updator_joepegs():
    for i in range(6,0,-1):
        print("[JOEPEGS] Updating Page", i)
        joeURI = "https://api.joepegs.dev/v2/items?pageSize=50&pageNum="+str(i)+"&orderBy=recent_listing&filters=buy_now&verified=true"
        headers = {"x-joepegs-api-key":"XrnqVcauKOtROXdzrFJbvHAYFnCx316sWnGE"}
        joeREQ = requests.get(joeURI, headers=headers)
        joeJSON = json.loads(joeREQ.text)
        for keys in joeJSON:            
            contract_address = keys["collection"]
            token_id = keys["tokenId"]
            id = contract_address + "-" + str(token_id)
            price = float(keys["currentAsk"]["price"]) / 1000000000000000000
            nonce = keys["currentAsk"]["nonce"]
            owner = keys["currentAsk"]["signer"]
            nonce_and_owner = [nonce,owner]

            if not isContractExist(contract_address):
                    print("[JOEPEGS] New Contract: ", contract_address)
                    info_contracts()
                    if isContractExist(contract_address):
                        addForOneContract(contract_address)
                        uptade_collection_attributes(contract_address)
                    else:
                        print("[ERROR] Contract exist, but not found in JoePegs's 'contracts': ", contract_address)
            elif isTokenExist(contract_address, token_id):
                tokenPriceUpdate(contract_address, token_id, price,"joepegs",nonce_and_owner)
                contract_stats_update(contract_address, price,"listing","exist")
            elif not isTokenExist(contract_address, token_id):
                if isContractExist(contract_address):
                    tokenCreateFromJoePegs(keys,"updator")
                    contract_stats_update(contract_address, price,"listing","new")
                    update_attributes(id, contract_address)
                
                    
            else:
                print("[ERROR] Check: ", id)

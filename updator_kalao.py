import requests
import json
from mongo_save import isContractExist,isTokenExist, tokenPriceUpdate,tokenCreateFromKalao, kalaoOrderIDUpdate,contract_stats_update,update_attributes,uptade_collection_attributes
import time
from info_collections import info_contracts
from database_initalizer import addForOneContract

def updator_kalao():

    for i in range(3,0,-1):
        kalaoURI = "https://backend.kalao.io/query"
        data = {"query": "query Activity($input: ActivityRequest!, $pagination: Page) {\n  activity(input: $input, pagination: $pagination) {\n    activities {\n     type\n      price\n      nft {\n        name\n        thumbnail\n        asset_id\n        collection {\n          avatar\n          name\n          certified\n        }\n      }\n      attributes\n      collection {\n        avatar\n        address\n        name\n        certified\n      }\n    }\n    hasMore\n  }\n}", "variables": {
            "input": {"target": "global", "types": ["listing"]}, "pagination": {"page": i, "size": 50}}, "operationName": "Activity"}
        headers = {"Content-Type": "application/json"}
        kalaoREQ = requests.post(kalaoURI, headers=headers, json=data)
        kalaoJSON = json.loads(kalaoREQ.text)
        for keys in reversed(kalaoJSON["data"]["activity"]["activities"]):
            contract_address = keys["collection"]["address"]
            asset_id = str(keys["nft"]["asset_id"])
            token_id = asset_id.split("_")[1]
            id = contract_address + "-" + str(token_id)
            price = keys["price"]
            if keys["collection"]["certified"] == True:

                if not isContractExist(contract_address):
                        print("[KALAO] New Contract:", contract_address)
                        info_contracts()
                        addForOneContract(contract_address)
                        uptade_collection_attributes(contract_address)

                elif isTokenExist(contract_address, token_id):
                    time.sleep(0.5)
                    data = {"query":"query Nft($assetId: String!) {\n  nft(assetId: $assetId) {\n    sale {\n      sale_id\n     }\n  }\n}","variables":{"assetId":asset_id},"operationName":"Nft"}
                    headers = {"Content-Type": "application/json"}
                    kalaoREQ = requests.post(kalaoURI, headers=headers, json=data)
                    kalaoJSON = json.loads(kalaoREQ.text)
                    if kalaoJSON["data"]["nft"]["sale"] == None:
                        pass
                    else:
                        sale_id = kalaoJSON["data"]["nft"]["sale"]["sale_id"]
                        kalaoOrderIDUpdate(id, sale_id)
                        tokenPriceUpdate(contract_address, token_id, price,"kalao","null")
                        contract_stats_update(contract_address, price,"listing","exist")
                        
                elif not isTokenExist(contract_address, token_id):
                        tokenCreateFromKalao(keys,"updator")
                        contract_stats_update(contract_address, price,"listing","new")
                        update_attributes(id, contract_address)
                        
                else:
                    print("[ERROR] Check: ", id)
            else:
                pass # Collection is not verified
            


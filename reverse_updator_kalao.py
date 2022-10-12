import requests
import json
from mongo_save import kalaoSoldListener,contract_stats_update
import time

def reverse_updator_kalao():
    n = 0
    nfts = {}
    for i in range(1,0,-1):
        kalaoURI = "https://backend.kalao.io/query"
        data = {"query":"query Activity($input: ActivityRequest!, $pagination: Page) {\n  activity(input: $input, pagination: $pagination) {\n    activities {\n      from\n      from_login\n      to\n      to_login\n      transaction_hash\n      timestamp\n      type\n      price\n      quantity\n      nft {\n        name\n        thumbnail\n        asset_id\n        collection {\n          avatar\n          name\n          certified\n        }\n      }\n      attributes\n      collection {\n        avatar\n        address\n        name\n        certified\n      }\n    }\n    hasMore\n  }\n}","variables":{"input":{"target":"global","types":["sale"]},"pagination":{"page":i,"size":100}},"operationName":"Activity"}
        headers = {"Content-Type": "application/json"}
        kalaoREQ = requests.post(kalaoURI, headers=headers, json=data)
        kalaoJSON = json.loads(kalaoREQ.text)
        for keys in reversed(kalaoJSON["data"]["activity"]["activities"]):
            contract_address = keys["collection"]["address"]
            asset_id = str(keys["nft"]["asset_id"])
            token_id = asset_id.split("_")[1]
            id = contract_address + "-" + str(token_id)
            price = str(keys["price"])
            if keys["collection"]["certified"] == True:
                # Adding nfts to dict to prevent duplicates (last one is added later so it's the latest)
                nfts.update({asset_id:price})   
        
            else:
                pass
        # Checking if nft is put sale again or not after being sold
        for key, value in nfts.items():
            id = key.split("_")[0] + "-" + key.split("_")[1]
            data_nft = {"query":"query Nft($assetId: String!) {\n  nft(assetId: $assetId) {\n    base {\n      asset_id\n      token_id\n      kind\n      address\n      owner\n      editions\n      total_owners\n      owners_avatars\n    }\n   sale {\n      sale_id\n      seller\n      unitary_price\n      unitary_price_float\n      quantity\n      start_date\n      expiration_date\n      kind\n      status\n      floor_diff\n    }\n  }\n}","variables":{"assetId":key},"operationName":"Nft"}
            headers = {"Content-Type": "application/json"}
            time.sleep(0.5)
            kalaoREQ = requests.post(kalaoURI, headers=headers, json=data_nft)
            kalaoJSON = json.loads(kalaoREQ.text)
            if kalaoJSON["data"]["nft"]["sale"] == None:
                if kalaoSoldListener(id):
                    contract_stats_update(contract_address, value,"sold","null")
                    print("[KALAO] Sold: ", id, "for price: ", value)
                n += 1


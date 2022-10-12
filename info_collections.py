import requests
import json
from mongo_save import isContractExists,contractVerificationUpdate,contractCreate

def info_contracts_kalao():
    for i in range(1,100):
        kalaoURI = "https://backend.kalao.io/query"
        data = {"query":"query Collections($input: SearchRequest!, $pagination: Page) {\n  search(input: $input, pagination: $pagination) {\n    collections {\n      collection {\n        address\n        avatar\n        owner\n        name\n        certified\n        description\n        banner\n        thumbnails\n      }\n      stats {\n        total_minted\n        total_owners\n        volume\n        floor_price\n        average_price\n      }\n    }\n    hasMore\n  }\n}","variables":{"input":{"category_tags":[],"keywords":"","sort":"top","target":"collections","certified":True},"pagination":{"page":i,"size":100}},"operationName":"Collections"}
        headers = {"Content-Type": "application/json"}
        kalaoREQ = requests.post(kalaoURI, headers=headers, json=data)
        kalaoJSON = json.loads(kalaoREQ.text)
        for keys in kalaoJSON["data"]["search"]["collections"]:

            id = keys["collection"]["address"]
            contract_name = keys["collection"]["name"]
            contract_avatar = keys["collection"]["avatar"]
            contract_banner = keys["collection"]["banner"]
            contract_description = keys["collection"]["description"]
            contract_stats = {"total_minted":int(keys["stats"]["total_minted"]),"total_listed":0,"total_volume":0,"floor_price":0,"average_price":0}
            contract_verification = {"verified_kalao":True,"verified_joepegs":False,"verified_nftrade":False}
            attributes_count = []
            contract_dict = {"_id": id, "contract_name": contract_name, "contract_avatar": contract_avatar, "contract_banner": contract_banner, "contract_description": contract_description,"contract_verification":contract_verification ,"contract_stats": contract_stats}
            if isContractExists(id):
                contractVerificationUpdate(id,"kalao")
                
            elif not isContractExists(id):
                contractCreate(contract_dict)
                print("[INFO] Contract created: ", id)
        if kalaoJSON["data"]["search"]["hasMore"] == False:
            print("[INFO] Kalao Contracts Finished.")
            break

def info_contracts_joepegs():
    for i in range(1, 100):
        joeURI = "https://api.joepegs.dev/v2/collections?pageSize=100&pageNum="+str(i)
        headers = {"x-joepegs-api-key":"XrnqVcauKOtROXdzrFJbvHAYFnCx316sWnGE"}
        joeREQ = requests.get(joeURI, headers=headers)
        if len(joeREQ.text) < 3 or joeREQ.status_code != 200:
            print("[INFO] Joepegs Contracts Finished.")
            break
        else:
            joeJSON = json.loads(joeREQ.text)
            for keys in joeJSON:
                if keys["verified"] == "verified":
                    id = keys["address"]
                    contract_name = keys["name"]
                    contract_avatar = keys["pfpUrl"]
                    contract_banner = keys["bannerUrl"]
                    contract_description = keys["description"]
                    contract_stats = {"total_minted":keys["numItems"],"total_listed":0,"total_volume":0,"floor_price":0,"average_price":0}
                    contract_verification = {"verified_kalao":False,"verified_joepegs":True,"verified_nftrade":False}
                    attributes_count = []
                    contract_dict = {"_id": id, "contract_name": contract_name, "contract_avatar": contract_avatar, "contract_banner": contract_banner, "contract_description": contract_description,"contract_verification":contract_verification ,"contract_stats": contract_stats}
                    
                    if isContractExists(id):
                        contractVerificationUpdate(id,"joepegs")
                        
                    elif not isContractExists(id):
                        contractCreate(contract_dict)
                        print("[INFO] Contract created: ", id)

def info_contracts_nftrade():
    nftrade_verifiedURI = "https://api.nftrade.com/api/v1/contracts?limit=10000&skip=0&chains[]=43114&verified=true&search="
    headers={"Referer": "https://nftrade.com/"}
    nftrade_verifiedREQ = requests.get(nftrade_verifiedURI, headers=headers)
    nftrade_verifiedJSON = json.loads(nftrade_verifiedREQ.text)
    print("[INFO] NFTrade Contracts Finished.")
    for keys in nftrade_verifiedJSON:
        id = keys["address"]
        contract_name = keys["name"]
        contract_avatar = keys["image"]
        contract_banner = "null"
        contract_description = keys["description"]
        contract_stats = {"total_minted":0,"total_listed":0,"total_volume":0,"floor_price":0,"average_price":0}
        contract_verification = {"verified_kalao":False,"verified_joepegs":False,"verified_nftrade":True}
        attributes_count = []
        contract_dict = {"_id": id, "contract_name": contract_name, "contract_avatar": contract_avatar, "contract_banner": contract_banner, "contract_description": contract_description,"contract_verification":contract_verification ,"contract_stats": contract_stats}
        if isContractExists(id):
            contractVerificationUpdate(id,"nftrade")
            
        elif not isContractExists(id):
            contractCreate(contract_dict)
            print("[INFO] Contract created: ", id)

def info_contracts():
    info_contracts_joepegs()
    info_contracts_kalao()
    info_contracts_nftrade()


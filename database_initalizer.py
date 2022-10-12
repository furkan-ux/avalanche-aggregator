import requests
import json
from mongo_save import isTokenExist, isTokenPriceSame,tokenPriceUpdate,tokenCreateFromKalao,tokenCreateFromJoePegs,tokenCreateFromNftrade,nftradeOrderIDUpdate,kalaoOrderIDUpdate
import time

def inital_nftrade(single_address, verified_address_path, unverified_address_path):
    # Get All NFTs on sale from NFTrade
    if verified_address_path != "null":
        with open(verified_address_path,"r") as f:
            nftrade_address = [line.rstrip('\n') for line in f]
            f.close()

    with open(unverified_address_path,"r") as f:
        nftrade_uuid_address = [line.rstrip('\n') for line in f]
        f.close()

    if single_address != "null":                   # for single address
        nftrade_address = [single_address] 

        for address in nftrade_address:
            for uuid in nftrade_uuid_address:
                if address == uuid[37:80]:
                    nftrade_uuid = uuid[0:36]
                    for i in range(0, 10000, 100):
                        nftradeURI = "https://api.nftrade.com/api/v1/tokens?limit=100&skip="+str(i)+"&contracts[]="+str(nftrade_uuid)+"&chains[]=43114&search=&order=true&sort=listed_desc"
                        nftradeREQ = requests.get(nftradeURI, headers={"Referer": "https://nftrade.com/"})
                        if len(nftradeREQ.text) < 3 or nftradeREQ.status_code != 200:
                            print("[DONE] NFTrade: ", address, " Page: ", int(i/100))
                            break
                        else:
                            nftradeJSON = json.loads(nftradeREQ.text)
                            for keys in nftradeJSON:
                                contract_address = keys["contractAddress"]
                                token_id = keys["tokenID"]
                                price = str(keys["price"])
                                id = contract_address + "-" + str(token_id)
                                if isTokenExist(contract_address,token_id):
                                    if isTokenPriceSame(contract_address, token_id, price,"nftrade"):
                                        pass
                                    else:
                                        tokenPriceUpdate(contract_address, token_id, price,"nftrade","null")
                                        nftradeOrderIDUpdate(id,keys["id"],keys["orderId"])
                                elif not isTokenExist(contract_address, token_id):
                                    tokenCreateFromNftrade(keys,"inital")
                                else:
                                    print("[ERROR] Check: ", id)
    elif single_address == "null":
        for address in nftrade_address:
            for uuid in nftrade_uuid_address:
                if address == uuid[37:80]:
                    nftrade_uuid = uuid[0:36]
                    for i in range(0, 10000, 100):
                        nftradeURI = "https://api.nftrade.com/api/v1/tokens?limit=100&skip="+str(i)+"&contracts[]="+str(nftrade_uuid)+"&chains[]=43114&search=&order=true&verified=true&sort=listed_desc"
                        nftradeREQ = requests.get(nftradeURI, headers={"Referer": "https://nftrade.com/"})
                        if len(nftradeREQ.text) < 3 or nftradeREQ.status_code != 200:
                            print("[DONE] NFTrade: ", address, " Page: ", int(i/100))
                            break
                        else:
                            nftradeJSON = json.loads(nftradeREQ.text)
                            for keys in nftradeJSON:
                                contract_address = keys["contractAddress"]
                                token_id = keys["tokenID"]
                                price = str(keys["price"])
                                id = contract_address + "-" + str(token_id)
                                if isTokenExist(contract_address,token_id):
                                    if isTokenPriceSame(contract_address, token_id, price,"nftrade"):
                                        pass
                                    else:
                                        tokenPriceUpdate(contract_address, token_id, price,"nftrade","null")
                                        nftradeOrderIDUpdate(id,keys["id"],keys["orderId"])
                                elif not isTokenExist(contract_address, token_id):
                                    tokenCreateFromNftrade(keys,"inital")
                                else:
                                    print("[ERROR] Check: ", id)


def inital_joepegs(single_address,path):
    # Get All NFTs on sale from JoePegs
    if path != "null":
        with open(path,"r") as f:
            joepegs_address = [line.rstrip('\n') for line in f]
            f.close()
    if single_address != "null":                   # for single address
        joepegs_address = [single_address]
    for address in joepegs_address:
        for i in range(1,100):
            joeURI = "https://api.joepegs.dev/v2/items?collectionAddress="+address+"&pageSize=100&pageNum="+str(i)+"&orderBy=price_asc&filters=buy_now&query=&attributeFilters=%5B%5D"
            headers = {"x-joepegs-api-key":"XrnqVcauKOtROXdzrFJbvHAYFnCx316sWnGE"}
            joeREQ = requests.get(joeURI, headers=headers)
            if len(joeREQ.text) < 3 or joeREQ.status_code != 200:
                print("[DONE] JoePegs: ", address, " Page: ", i)
                break
            joeJSON = json.loads(joeREQ.text)
            for keys in joeJSON:
                contract_address = keys["collection"]
                token_id = keys["tokenId"]
                int_price = int(keys["currentAsk"]["price"]) / 1000000000000000000
                price = str(int_price)
                nonce = keys["currentAsk"]["nonce"]
                owner = keys["currentAsk"]["signer"]
                id = contract_address + "-" + str(token_id)
                nonce_and_owner = [nonce,owner]
                if isTokenExist(contract_address,token_id):
                    if isTokenPriceSame(contract_address, token_id, price,"joepegs"):
                        pass
                    else:
                        tokenPriceUpdate(contract_address, token_id, price,"joepegs",nonce_and_owner)
                elif not isTokenExist(contract_address, token_id):
                    tokenCreateFromJoePegs(keys,"inital")
                else:
                    print("[ERROR] Check: ", id)

def inital_kalao(single_address,path):
    # Get All NFTs on sale from Kalao
    if path != "null":
        with open(path,"r") as f:
            kalao_address = [line.rstrip('\n') for line in f]
            f.close()
    if single_address != "null":                   # for single address
        kalao_address = [single_address]
    for address in kalao_address:
        for i in range(1,1000):
            data = {"query":"query Nfts($pagination: Page, $input: SearchRequest!) {\n  search(pagination: $pagination, input: $input) {\n    hasMore\n    nfts {\n      name\n      thumbnail\n      token_id\n      likes\n      asset_id\n      animation_url\n      animation_mime\n      balance\n      collection {\n        address\n        avatar\n        address\n        certified\n        kind\n        name\n      }\n      sale {\n        sale_id\n        unitary_price_float\n        quantity\n        kind\n        seller\n      }\n      offer {\n        offer_id\n        buyer\n        unitary_price_float\n        start_date\n        expiration_date\n      }\n    }\n  }\n}","variables":{"input":{"target":"nfts","keywords":"","sort":"price_asc","category_tags":[],"sale_type":"direct","price_range":{"min":"0.01"},"collection_address":address},"pagination":{"page":i,"size":100}},"operationName":"Nfts"}
            kalaoURI = "https://backend.kalao.io/query"
            headers = {"Content-Type":"application/json"}
            time.sleep(0.34)
            kalaoREQ = requests.post(kalaoURI, json=data, headers=headers)
            if kalaoREQ.status_code != 200:
                print("[ERROR] (initalizer) Kalao: ", address, " Page: ", i)
                break
            elif kalaoREQ.status_code == 429:
                print("[ERROR] (initalizer) Kalao: ", address, " Page: ", i, " Code: 429, Sleeping for 10 seconds")
                time.sleep(10)
                continue
            else:
                kalaoJSON = json.loads(kalaoREQ.text)
                for keys in kalaoJSON["data"]["search"]["nfts"]:
                    contract_address = keys["collection"]["address"]
                    token_id = keys["token_id"]
                    price = str(keys["sale"]["unitary_price_float"])
                    sale_id = keys["sale"]["sale_id"]
                    id = contract_address + "-" + str(token_id)
                    kalaoOrderIDUpdate(id,sale_id)
                    if isTokenExist(contract_address,token_id):
                        if isTokenPriceSame(contract_address, token_id, price,"kalao"):
                            pass
                        else:
                            tokenPriceUpdate(contract_address, token_id, price,"kalao","null")
                    elif not isTokenExist(contract_address, token_id):
                        tokenCreateFromKalao(keys,"inital")
                    else:
                        print("[ERROR] Check: ", id)
            if kalaoJSON["data"]["search"]["hasMore"] == False:
                print("[DONE] Kalao: ", address, " Page: ", i)
                break



def addAllPrices():

    kalao_address_path = "/home/rtest/aggregation/addresses/kalao-address.txt"
    joepegs_address_path = "/home/rtest/aggregation/addresses/joepegs-address.txt"
    nftrade_address_path = "/home/rtest/aggregation/addresses/nftrade-address.txt"
    nftrade_unverified_address_path = "/home/rtest/aggregation/addresses/nftrade-unverified-address.txt"

    from pymongo import MongoClient
    CONNECTION_STRING = "mongodb://admin-1:db-yoneticisi-1@127.0.0.1:27017/?authMechanism=DEFAULT"
    client = MongoClient(CONNECTION_STRING)
    dbname = client["V2"]

    inital_joepegs("null",joepegs_address_path)
    inital_kalao("null",kalao_address_path)
    inital_nftrade("null",nftrade_address_path,nftrade_unverified_address_path)

    for contract in dbname["contracts"].find():
        if contract["contract_verification"]["verified_kalao"] == False:
            inital_kalao(contract["_id"],"null")
        if contract["contract_verification"]["verified_joepegs"] == False:
            inital_joepegs(contract["_id"],"null")
        if contract["contract_verification"]["verified_nftrade"] == False:
            inital_nftrade(contract["_id"],"null",nftrade_unverified_address_path)
            

def addForOneContract(contract_address):

    kalao_address_path = "/home/rtest/aggregation/addresses/kalao-address.txt"
    joepegs_address_path = "/home/rtest/aggregation/addresses/joepegs-address.txt"
    nftrade_address_path = "/home/rtest/aggregation/addresses/nftrade-address.txt"
    nftrade_unverified_address_path = "/home/rtest/aggregation/addresses/nftrade-unverified-address.txt"

    from pymongo import MongoClient
    CONNECTION_STRING = "mongodb://admin-1:db-yoneticisi-1@127.0.0.1:27017/?authMechanism=DEFAULT"
    client = MongoClient(CONNECTION_STRING)
    dbname = client["V2"]

    inital_joepegs(contract_address,joepegs_address_path)
    inital_kalao(contract_address,kalao_address_path)
    inital_nftrade(contract_address,nftrade_address_path,nftrade_unverified_address_path)

    for contract in dbname["contracts"].find({"_id":contract_address}):
        if contract["contract_verification"]["verified_kalao"] == False:
            inital_kalao(contract["contract_address"])
        if contract["contract_verification"]["verified_joepegs"] == False:
            inital_joepegs(contract["contract_address"])
        if contract["contract_verification"]["verified_nftrade"] == False:
            inital_nftrade(contract["contract_address"])
    
    print("[DONE] Initalizing new contract: ", contract_address)


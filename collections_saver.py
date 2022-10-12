from email import header
import requests
import json
import os


def contracts_kalao(path):
    if os.path.exists(path):
        os.remove(path)
        with open(path, "w") as f:
            f.write("")
            f.close()
    for i in range(1, 100):
        kalaoURI = "https://backend.kalao.io/query"
        headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3","Content-Type":"application/json","Origin":"https://marketplace.kalao.io/","Referer":"https://marketplace.kalao.io/"}
        data = {"query":"query Collections($input: SearchRequest!, $pagination: Page) {\n  search(input: $input, pagination: $pagination) {\n    collections {\n      collection {\n        address\n        avatar\n        owner\n        name\n        certified\n        description\n        banner\n        thumbnails\n      }\n      stats {\n        total_minted\n        total_owners\n        volume\n        floor_price\n        average_price\n      }\n    }\n    hasMore\n  }\n}","variables":{"input":{"category_tags":[],"keywords":"","sort":"top","target":"collections","certified":True},"pagination":{"page":i,"size":100}},"operationName":"Collections"}
        kalaoREQ = requests.post(kalaoURI, headers=headers, json=data)
        kalaoJSON = json.loads(kalaoREQ.text)
        for keys in kalaoJSON['data']['search']['collections']:
                address = keys["collection"]["address"]
                with open(path, "a") as f:
                    f.write(address + "\n")
                    f.close()
        if kalaoJSON['data']['search']['hasMore'] == False:
            break

def contracts_joepegs(path):
    if os.path.exists(path):
        os.remove(path)
        with open(path, "w") as f:
            f.write("")
            f.close()
    for i in range(1, 100):
        joeURI = "https://api.joepegs.dev/v2/collections?pageSize=100&pageNum="+str(i)
        headers = {"x-joepegs-api-key":"XrnqVcauKOtROXdzrFJbvHAYFnCx316sWnGE"}
        joeREQ = requests.get(joeURI, headers=headers)
        if len(joeREQ.text) < 3 or joeREQ.status_code != 200:
            break
        else:
            joeJSON = json.loads(joeREQ.text)
            for keys in joeJSON:
                if keys["verified"] == "verified":
                    address = keys["address"]
                    with open(path, "a") as f:
                        f.write(address + "\n")
                        f.close()

          
def contracts_nftrade(verified_path, unverified_path):
    if os.path.exists(unverified_path):
        os.remove(unverified_path)
        with open(unverified_path, "w") as f:
            f.write("")
            f.close()
    if os.path.exists(verified_path):
        os.remove(verified_path)
        with open(verified_path, "w") as f:
            f.write("")
            f.close()
    nftrade_unverifiedURI = "https://api.nftrade.com/api/v1/contracts?limit=100000&skip=0&chains[]=43114&verified=&search="
    headers={"Referer": "https://nftrade.com/"}
    nftrade_unverifiedREQ = requests.get(nftrade_unverifiedURI, headers=headers)
    nftrade_unverifiedJSON = json.loads(nftrade_unverifiedREQ.text)
    for keys in nftrade_unverifiedJSON:
        unverified_string = str(keys['id'])+" "+str(keys['address']) +"\n"
        with open(unverified_path, "a") as f:
            f.write(unverified_string)
            f.close()
    
    nftrade_verifiedURI = "https://api.nftrade.com/api/v1/contracts?limit=10000&skip=0&chains[]=43114&verified=true&search="
    nftrade_verifiedREQ = requests.get(nftrade_verifiedURI, headers=headers)
    nftrade_verifiedJSON = json.loads(nftrade_verifiedREQ.text)
    for keys in nftrade_verifiedJSON:
        verified_string = str(keys['address']) +"\n"
        with open(verified_path, "a") as f:
            f.write(verified_string)
            f.close()
        

def collections_main():
    kalao_address_path = "/home/rtest/aggregation/addresses/kalao-address.txt"
    joepegs_address_path = "/home/rtest/aggregation/addresses/joepegs-address.txt"
    nftrade_address_path = "/home/rtest/aggregation/addresses/nftrade-address.txt"
    nftrade_unverified_address_path = "/home/rtest/aggregation/addresses/nftrade-unverified-address.txt"

    contracts_kalao(kalao_address_path)
    print("[KALAO] Verified contracts saved. Count: ", len(open(kalao_address_path).readlines()))
    contracts_joepegs(joepegs_address_path)
    print("[JoePegs] Verified contracts saved. Count: ", len(open(joepegs_address_path).readlines()))
    contracts_nftrade(nftrade_address_path, nftrade_unverified_address_path)
    print("[NFTrade] Verified contracts saved. Count: ", len(open(nftrade_address_path).readlines()))


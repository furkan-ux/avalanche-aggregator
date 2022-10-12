import requests
import json
from mongo_save import nftradeSoldListener,contract_stats_update

def reverse_updator_nftrade():

    nftradeSoldURI = "https://api.nftrade.com/api/v1/tokens?limit=100&skip=0&search=&order=&verified=true&sort=sold_desc"
    nftradeSoldREQ = requests.get(nftradeSoldURI, headers={"Referer": "https://nftrade.com/"})
    nftradeSoldJSON = json.loads(nftradeSoldREQ.text)
    for keys in reversed(nftradeSoldJSON):
        id = keys["contractAddress"] + "-" + str(keys["tokenID"])
        price = keys["price"]
        last_sell_price = keys["last_sell"]
        if price != None:
            pass
        else:
            if nftradeSoldListener(id):
                contract_stats_update(keys["contractAddress"], last_sell_price,"sold","null")
                print("[NFTRADE] Sold: ", id, "for price: ", str(last_sell_price))

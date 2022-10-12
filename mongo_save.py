import simplejson as json
from pymongo import MongoClient
import time
import datetime
import requests




CONNECTION_STRING = "mongodb://admin-1:db-yoneticisi-1@127.0.0.1:27017/?authMechanism=DEFAULT"
client = MongoClient(CONNECTION_STRING)
dbname = client["V2"]


def isContractExist(contract_address):

    if dbname["contracts"].find_one({"_id": contract_address}):

        return True

    else:

        return False

def isTokenExist(contract_address, token_id):

    id = contract_address + "-" + token_id
    return dbname["NFTS"].find_one({"_id": id})



def isTokenPriceSame(contract_address, token_id, price, market):

    id = contract_address + "-" + token_id
    coll_name = dbname["NFTS"]

    if market == "joepegs":

        old_price = coll_name.find_one({"_id": id})["price_joepegs"]
        str_price = float(price)

        if old_price == str_price:

            return True

        else:

            return False

    elif market == "nftrade":

        old_price = coll_name.find_one({"_id": id})["price_nftrade"]
        str_price = float(price)

        if old_price == str_price:

            return True
        else:

            return False

    elif market == "kalao":

        old_price = coll_name.find_one({"_id": id})["price_kalao"]
        str_price = float(price)

        if old_price == str_price:

            return True

        else:

            return False

def tokenPriceUpdate(contract_address, token_id, price, market, nonce):  # if market is joepegs add it also to joepegs db, so nonce field default is null

    id = contract_address + "-" + token_id
    coll_name = dbname["NFTS"]

    if market == "joepegs":

        old_price = coll_name.find_one({"_id": id})["price_joepegs"]
        str_price = float(price)

        if dbname["joepegs"].find_one({"_id": id}):

                dbname["joepegs"].update_one({"_id": id}, {"$set": {"nonce": nonce[0],"owner": nonce[1]}})

        elif not dbname["joepegs"].find_one({"_id": id}):

                dbname["joepegs"].insert_one({
                    "_id": id,
                    "nonce": nonce[0],
                    "owner": nonce[1]
                })

        if old_price != str_price:

            dbname["NFTS"].update_one({"_id": id}, {"$set": {"price_joepegs": str_price}})
            dbname["history"].insert_one({"_id": id + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), "price": str_price, "market": "joepegs"})
            print("[JOEPEGS] Price updated for", id," price: ",str_price)

            
        else:

            pass


    elif market == "nftrade":

        old_price = coll_name.find_one({"_id": id})["price_nftrade"]
        str_price = float(price)
        
        if old_price != str_price:
            dbname["NFTS"].update_one({"_id": id}, {"$set": {"price_nftrade": str_price}})
            print("[NFTRADE] Price updated for", id)
            dbname["history"].insert_one({"_id": id + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), "price": str_price, "market": "nftrade"})

        else:

            pass


    elif market == "kalao":

        old_price = coll_name.find_one({"_id": id})["price_kalao"]
        str_price = float(price)

        if old_price != str_price:
            dbname["NFTS"].update_one({"_id": id}, {"$set": {"price_kalao": str_price}})
            print("[KALAO] Price updated for", id, "to", str_price)
            time.sleep(1)
            dbname["history"].insert_one({"_id": id + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), "price": str_price, "market": "kalao"})

        else:

            pass
    

def tokenCreateFromJoePegs(keys,type):

    coll_name = dbname["NFTS"]
    id = keys["collection"] + "-" + str(keys["tokenId"])
    price = float(keys["currentAsk"]["price"]) / 1000000000000000000
    str_price = float(price)

    try:
        for key in keys["metadata"]["attributes"]:
            del key["displayType"]
            del key["countPercentage"]
            del key["rarityScore"]
            del key["count"]
            key["count"] = 0
        metadata = keys["metadata"]["attributes"]
    except:
        metadata = []
    str_keys = str(keys)

    try:
        str_keys.replace("None", '"null"')
        keys = json.loads(str_keys)
    except:
        pass   

    try: 
        coll_name.insert_one({
            "_id": keys["collection"] + "-" + keys["tokenId"],
            "contract_address": str(keys["collection"]),
            "token_id": str(keys["tokenId"]),
            "contract_name": str(keys["collectionName"]),
            "token_name": str(keys["metadata"]["name"]),
            "image": str(keys["metadata"]["image"]),
            "thumbnail": str(keys["metadata"]["image"]),
            "token_uri": str(keys["metadata"]["tokenUri"]),
            "external_url": str(keys["metadata"]["externalUrl"]),
            "price_nftrade": "null",
            "price_joepegs": str_price,
            "price_kalao": "null",
            "price_yeti": "null",
            "price_campfire": "null",
            "metadata": metadata
        })
    except:  # Sometimes metadatas are not refreshed so, metadata comes as null, to handle this, we are saving all metadata related fields as null
        coll_name.insert_one({
            "_id": keys["collection"] + "-" + keys["tokenId"],
            "contract_address": str(keys["collection"]),
            "token_id": str(keys["tokenId"]),
            "contract_name": str(keys["collectionName"]),
            "token_name": "null",
            "image": "null",
            "thumbnail": "null",
            "token_uri": "null",
            "external_url": "null",
            "price_nftrade": "null",
            "price_joepegs": str_price,
            "price_kalao": "null",
            "price_yeti": "null",
            "price_campfire": "null",
            "metadata": metadata
        })
        
    dbname["history"].insert_one({"_id": id + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), "price": str_price, "market": "joepegs"})

    if dbname["joepegs"].find_one({"_id": id}):
        dbname["joepegs"].update_one({"_id": id}, {"$set": {"nonce": keys["currentAsk"]["nonce"],"owner": keys["currentAsk"]["signer"]}})
    elif not dbname["joepegs"].find_one({"_id": id}):
        dbname["joepegs"].insert_one({
                    "_id": id,
                    "nonce": keys["currentAsk"]["nonce"],
                    "owner": keys["currentAsk"]["signer"]})

    if type == "updator":
        print("[SUCCESS] Token created for", keys["collection"] + "-" + keys["tokenId"], " price: ",str_price)
    elif type == "inital":
        pass

def tokenCreateFromNftrade(keys,type):

    coll_name = dbname["NFTS"]
    id = keys["contractAddress"] + "-" + str(keys["tokenID"])
    price = float(keys["price"])
    order_id = keys["orderId"]
    nftrade_id = str(keys["id"])

    try:
        metadata_url = "https://api.nftrade.com/api/v1/tokens/"+str(keys["id"])+"/traits"
        metadata_req = requests.get(metadata_url, headers={"Referer": "https://nftrade.com/"})
        metadata_json = json.loads(metadata_req.text)
        metadata = []
        for meta in metadata_json:
            metadata.append({"traitType": meta["key"], "value": meta["value"],"count": 0})
    except:
        metadata = None

    coll_name.insert_one({
        "_id": id,
        "contract_address": str(keys["contractAddress"]),
        "token_id": str(keys["tokenID"]),
        "contract_name": str(keys["contractName"]),
        "token_name": str(keys["name"]),
        "image": str(keys["image"]),
        "thumbnail": str(keys["thumb"]),
        "token_uri": str(keys["tokenURI"]),
        "external_url": str(keys["external_url"]),
        "price_nftrade": price,
        "price_joepegs": "null",
        "price_kalao": "null",
        "price_yeti": "null",
        "price_campfire": "null",
        "metadata": metadata
    })
    dbname["history"].insert_one({"_id": id + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), "price": price, "market": "nftrade"})

    if type == "updator":

        print("[SUCCESS] Token created for", id)
        
        if dbname["nftrade"].find_one({"_id": id}):
            dbname["nftrade"].update_one({"_id": id}, {"$set": {"nftradeID": nftrade_id,"orderID": order_id}})
        else:
            dbname["nftrade"].insert_one({
                        "_id": id,
                        "nftradeID": nftrade_id,
                        "orderID": order_id})

    elif type == "inital":

        if dbname["nftrade"].find_one({"_id": id}):
            old_order_id = dbname["nftrade"].find_one({"_id": id})["orderID"]
            if old_order_id != order_id:
                dbname["nftrade"].update_one({"_id": id}, {"$set": {"nftradeID": nftrade_id,"orderID": order_id}})

        else:
            dbname["nftrade"].insert_one({
                        "_id": id,
                        "nftradeID": nftrade_id,
                        "orderID": order_id})


def tokenCreateFromKalao(keys,type):

    if type == "updator":
        
        asset_id = str(keys["nft"]["asset_id"])
        kalaoURI = "https://backend.kalao.io/query"
        data = {"query": "query Nft($assetId: String!) {\n  nft(assetId: $assetId) {\n    base {\n      asset_id\n      token_id\n      kind\n      address\n      owner\n      editions\n      total_owners\n      owners_avatars\n    }\n    metadatas {\n      name\n      description\n      thumbnail_url\n      thumbnail_mime\n      animation_url\n      background_color\n      external_url\n      youtube_url\n      extra\n    }\n    attributes {\n      trait_type\n      value\n      proba\n    }\n    collection {\n      address\n      avatar\n      owner\n      name\n      certified\n      description\n      kind\n       }\n  }\n}", "variables": {"assetId": asset_id}, "operationName": "Nft"}
        headers = {"Content-Type": "application/json"}
        time.sleep(0.5)
        kalaoREQ = requests.post(kalaoURI, data=json.dumps(data), headers=headers)
        kalaoJSON = json.loads(kalaoREQ.text)
        coll_name = dbname["NFTS"]
        metadata = []

        try:
            for key in kalaoJSON["data"]["nft"]["attributes"]:
                metadata.append({"traitType": key["trait_type"], "value": key["value"],"count": 0})
        except:
            metadata = []
    
        id = kalaoJSON["data"]["nft"]["base"]["address"] + "-" + str(kalaoJSON["data"]["nft"]["base"]["token_id"])
        image = kalaoJSON["data"]["nft"]["metadatas"]["thumbnail_url"][:-9] + "details"
        thumbnail = kalaoJSON["data"]["nft"]["metadatas"]["thumbnail_url"]

        coll_name.insert_one({
            "_id": id,
            "contract_address": str(kalaoJSON["data"]["nft"]["base"]["address"]),
            "token_id": str(kalaoJSON["data"]["nft"]["base"]["token_id"]),
            "contract_name": str(keys["collection"]["name"]),
            "token_name": str(keys["nft"]["name"]),
            "image": image,
            "thumbnail": thumbnail,
            "token_uri": "null",
            "external_url": "null",
            "price_nftrade":"null",
            "price_joepegs":"null",
            "price_kalao": float(keys["price"]),
            "price_yeti": "null",
            "price_campfire": "null",
            "metadata": metadata
        })

        dbname["history"].insert_one({"_id": id + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), "price": str(keys["price"]), "market": "kalao"})
        print("[SUCCESS] Token created for", str(kalaoJSON["data"]["nft"]["base"]["address"])+ "-" + str(kalaoJSON["data"]["nft"]["base"]["token_id"]), "price: ",float(keys["price"]))

    elif type == "inital":

        asset_id = str(keys["asset_id"])
        kalaoURI = "https://backend.kalao.io/query"
        data = {"query":"query Nft($assetId: String!) {\n  nft(assetId: $assetId) {\n    base {\n      asset_id\n      token_id\n      kind\n      address\n      owner\n      }\n    metadatas {\n      name\n      description\n      thumbnail_url\n      thumbnail_mime\n      animation_url\n      background_color\n      external_url\n      youtube_url\n      extra\n    }\n    attributes {\n      trait_type\n      value\n      proba\n    }\n    collection {\n      address\n      avatar\n      owner\n      name\n      certified\n      description\n      kind\n       }\n  }\n}","variables":{"assetId":asset_id},"operationName":"Nft"}
        headers = {"Content-Type": "application/json"}
        time.sleep(0.5)
        kalaoREQ = requests.post(kalaoURI, data=json.dumps(data), headers=headers)

        if kalaoREQ.status_code != 200:
            print("[ERROR] Kalao API is down", kalaoREQ.status_code)
            time.sleep(30)

        kalaoJSON = json.loads(kalaoREQ.text)
        coll_name = dbname["NFTS"]
        metadata = []

        try:
            for key in kalaoJSON["data"]["nft"]["attributes"]:
                metadata.append({"traitType": key["trait_type"], "value": key["value"],"count": 0})
        except:
            metadata = []

        id = kalaoJSON["data"]["nft"]["base"]["address"] + "-" + str(kalaoJSON["data"]["nft"]["base"]["token_id"])
        image = kalaoJSON["data"]["nft"]["metadatas"]["thumbnail_url"][:-9] + "details"
        thumbnail = kalaoJSON["data"]["nft"]["metadatas"]["thumbnail_url"]

        coll_name.insert_one({
            "_id": id,
            "contract_address": str(kalaoJSON["data"]["nft"]["base"]["address"]),
            "token_id": str(kalaoJSON["data"]["nft"]["base"]["token_id"]),
            "contract_name": str(keys["collection"]["name"]),
            "token_name": str(keys["name"]),
            "image": image,
            "thumbnail": thumbnail,
            "token_uri": "null",
            "external_url": "null",
            "price_nftrade":"null",
            "price_joepegs":"null",
            "price_kalao": float(keys["sale"]["unitary_price_float"]),
            "price_yeti": "null",
            "price_campfire": "null",
            "metadata": metadata
        })
        dbname["history"].insert_one({"_id": id + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), "price": str(keys["sale"]["unitary_price_float"]), "market": "kalao"})


def nftradeOrderIDUpdate(id,nftrade_id, order_id):

    if dbname["nftrade"].find_one({"_id": id}):

        old_order_id = dbname["nftrade"].find_one({"_id": id})["orderID"]

        if old_order_id != order_id:

            dbname["nftrade"].update_one({"_id": id}, {"$set": {"nftradeID": nftrade_id,"orderID": order_id}})
    else:

        dbname["nftrade"].insert_one({
            "_id": id,
            "nftradeID": nftrade_id,
            "orderID": order_id})



def kalaoOrderIDUpdate(id,order_id):

    if dbname["kalao"].find_one({"_id": id}):

        old_order_id = dbname["kalao"].find_one({"_id": id})["orderID"]

        if old_order_id != order_id:

            dbname["kalao"].update_one({"_id": id}, {"$set": {"orderID": order_id}})
    else:

        dbname["kalao"].insert_one({
            "_id": id,
            "orderID": order_id})

def isContractExists(address):

    if dbname["contracts"].find_one({"_id": address}):

        return True

    else:

        return False

def contractVerificationUpdate(address,market):

    if market == "kalao":

        dbname["contracts"].update_one({"_id": address}, {"$set": {"contract_verification.verified_kalao": True}})

    elif market == "nftrade":

        dbname["contracts"].update_one({"_id": address}, {"$set": {"contract_verification.verified_nftrade": True}})

    elif market == "joepegs":

        dbname["contracts"].update_one({"_id": address}, {"$set": {"contract_verification.verified_joepegs": True}})


def contractCreate(keys):

    dbname["contracts"].insert_one(keys)

def nftradeSoldListener(id):

    if dbname["NFTS"].find_one({"_id": id}):

        dbname["NFTS"].update_one({"_id": id}, {"$set": {"price_nftrade": "null"}})
        return True

def kalaoSoldListener(id):

    if dbname["NFTS"].find_one({"_id": id}):

        dbname["NFTS"].update_one({"_id": id}, {"$set": {"price_kalao": "null"}})
        return True


def inital_set_attributes():
    n = 0
    for collection in dbname["contracts"].find():
        collection_address = collection["_id"]
        traits = []
        
        
        for nft in dbname["NFTS"].find({"contract_address": collection_address}):
                if nft["metadata"] != None:
                    for trait in nft["metadata"]:
                        lol = {
                            "traitType": trait["traitType"],
                            "value": trait["value"],
                            "count": 1,
                        }

                        flag = False
                        for x in traits:
                            if (
                                lol["traitType"] == x["traitType"]
                                and lol["value"] == x["value"]
                            ):
                                x["count"] += 1
                                flag = True
                                break
                        if flag == False:
                            traits.append(lol)
        n += 1

        dbname["contracts"].update_one({"_id": collection_address}, {"$set": {"attributes_count": traits}})
    print("[TRAITS] Updated attributes for " + str(n) + " collections")

def uptade_collection_attributes(contract_address):
    n = 0
    for collection in dbname["contracts"].find({"_id": contract_address}):
        collection_address = collection["_id"]
        traits = []
        
        
        for nft in dbname["NFTS"].find({"contract_address": collection_address}):
                if nft["metadata"] != None:
                    for trait in nft["metadata"]:
                        lol = {
                            "traitType": trait["traitType"],
                            "value": trait["value"],
                            "count": 1,
                        }

                        flag = False
                        for x in traits:
                            if (
                                lol["traitType"] == x["traitType"]
                                and lol["value"] == x["value"]
                            ):
                                x["count"] += 1
                                flag = True
                                break
                        if flag == False:
                            traits.append(lol)
        n += 1

        dbname["contracts"].update_one({"_id": collection_address}, {"$set": {"attributes_count": traits}})
    print("[TRAITS] Updated attributes for " + str(n) + " collections")


def update_attributes(id,contract_address):
    traits = []
    
    for contract in dbname["contracts"].find({"_id": contract_address}):
        traits = contract["attributes_count"]

    for nft in dbname["NFTS"].find({"_id": id}):
        if nft["metadata"] != None:
            for trait in nft["metadata"]:
                lol = {
                        "traitType": trait["traitType"],
                        "value": trait["value"],
                        "count": 1,
                    }

                flag = False
                for x in traits:
                    if (
                        lol["traitType"] == x["traitType"]
                        and lol["value"] == x["value"]
                        ):
                        x["count"] += 1
                        flag = True
                        break
                if flag == False:
                    traits.append(lol)
        

    dbname["contracts"].update_one({"_id": contract_address}, {"$set": {"attributes_count": traits}})
    


def contract_stats_inital():

    contract_addresses = []
    for contract in dbname["contracts"].find():
        contract_address = contract["_id"]
        contract_addresses.append(contract_address)
    
    for contract_address in contract_addresses:
        total_listed = 0
        total_volume = 0
        floor_prices = []
        for nft in dbname["NFTS"].find({"contract_address": contract_address}):
            total_listed += 1
            for keys in nft:
                floor_price_per_nft = 0
                prices_per_nft = []
                if keys == "price_nftrade" and nft[keys] != "null":
                    prices_per_nft.append(float(nft[keys]))
                elif keys == "price_kalao" and nft[keys] != "null":
                    prices_per_nft.append(float(nft[keys]))
                elif keys == "price_joepegs" and nft[keys] != "null":
                    prices_per_nft.append(float(nft[keys]))
                elif keys == "price_yeti" and nft[keys] != "null":
                    prices_per_nft.append(float(nft[keys]))
                elif keys == "price_campfire" and nft[keys] != "null":
                    prices_per_nft.append(float(nft[keys]))

                if len(prices_per_nft) > 0:
                    floor_price_per_nft = min(prices_per_nft)
                    floor_prices.append(floor_price_per_nft)
        try:
            floor_price = min(floor_prices)
            average_price = sum(floor_prices) / len(floor_prices)    
        except:
            floor_price = 0
            average_price = 0       

        dbname["contracts"].update_one({"_id": contract_address}, {"$set": {"contract_stats.total_listed": total_listed, "contract_stats.total_volume": total_volume, "contract_stats.average_price": average_price, "contract_stats.floor_price": floor_price}})
    
    print("[STATS] Updated stats for ",len(contract_addresses)," contracts")
 
def contract_stats_update(contract_address,price,type,type2):
    
    if type == "listing":
        if type2 == "exist":
           
            old_floor = dbname["contracts"].find_one({"_id": contract_address})["contract_stats"]["floor_price"]
            if float(price) < float(old_floor):
                dbname["contracts"].update_one({"_id": contract_address}, {"$set": {"contract_stats.floor_price": price}})

        elif type2 == "new":

            total_listed = dbname["contracts"].find_one({"_id": contract_address})["contract_stats"]["total_listed"]
            total_listed += 1
            dbname["contracts"].update_one({"_id": contract_address}, {"$set": {"contract_stats.total_listed": total_listed}})

            old_floor = dbname["contracts"].find_one({"_id": contract_address})["contract_stats"]["floor_price"]
            if float(price) < float(old_floor):
                dbname["contracts"].update_one({"_id": contract_address}, {"$set": {"contract_stats.floor_price": price}})

    elif type == "sold":
        total_listed = dbname["contracts"].find_one({"_id": contract_address})["contract_stats"]["total_listed"]
        total_listed -= 1
        dbname["contracts"].update_one({"_id": contract_address}, {"$set": {"contract_stats.total_listed": total_listed}})
        old_floor = dbname["contracts"].find_one({"_id": contract_address})["contract_stats"]["floor_price"]
        if float(price) > float(old_floor):
            pass
        else:
            floor_prices = []
            for nft in dbname["NFTS"].find({"contract_address": contract_address}):
                for keys in nft:
                    floor_price_per_nft = 0
                    prices_per_nft = []
                    if keys == "price_nftrade" and nft[keys] != "null":
                        prices_per_nft.append(float(nft[keys]))
                    elif keys == "price_kalao" and nft[keys] != "null":
                        prices_per_nft.append(float(nft[keys]))
                    elif keys == "price_joepegs" and nft[keys] != "null":
                        prices_per_nft.append(float(nft[keys]))
                    elif keys == "price_yeti" and nft[keys] != "null":
                        prices_per_nft.append(float(nft[keys]))
                    elif keys == "price_campfire" and nft[keys] != "null":
                        prices_per_nft.append(float(nft[keys]))

                    if len(prices_per_nft) > 0:
                        floor_price_per_nft = min(prices_per_nft)
                        floor_prices.append(floor_price_per_nft)
            try:
                floor_price = min(floor_prices)
                dbname["contracts"].update_one({"_id": contract_address}, {"$set": {"contract_stats.floor_price": floor_price}})
            except:
                pass

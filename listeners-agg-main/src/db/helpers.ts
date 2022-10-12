import { UpdateResult } from "mongodb/mongodb";
import mongoose from "mongoose";
import { HISTORY_TYPE, OPERATION_TYPE } from "../enums";
import { IDecode } from "../helpers/nftrade";
import { History } from "../models/history";
import getNFTModel from "../models/nft";

/**
 * @description - This function is used to check if a collection exists on mongoDB
 * @param collectionName Name of the collection
 * @returns true if collection exist on MongoDB, false otherwise
 */
export const isCollectionExistOnMongoDB = async (
  collectionName: string
): Promise<boolean> => {
  const collections = await mongoose.connection.db.listCollections().toArray();
  return collections.some(
    (collection: { name: string }) =>
      collection.name.toLowerCase() === collectionName.toLowerCase()
  );
};

/**
 * @description - This function is used to check if a collection exists on mongoDB
 * @param collectionAddress Name of the collection
 * @param tokenID tokenID of the NFT
 * @returns true if NFT exist in collection exist on MongoDB, false otherwise
 */
export const isNFTExistInCollection = async (
  collectionAddress: string,
  tokenID: string
): Promise<boolean> => {
  const collection = mongoose.connection.db.collection(
    collectionAddress.toLowerCase()
  );
  const count = await collection.find({ tokenID }).toArray();
  return count.length > 0;
};

/**
 *
 * @param address Address of the collection
 * @param tokenID Token id of the NFT
 * @param timestamp Timestamp of the event (block timestamp) (optional)
 * @returns {boolean} true if NFT updated, false otherwise
 */
export const setAllPricesToNull = async (
  address: string,
  tokenID: string,
  timestamp?: string
): Promise<boolean> => {
  const model = await getNFTModel(address.toLowerCase());
  if (!model) return false;
  var updateResult: UpdateResult | null;

  if (!timestamp) {
    updateResult = await model.updateOne(
      { tokenID },
      {
        $set: {
          nftradePrice: "null",
          kalaoPrice: "null",
          campfirePrice: "null",
          joePegsPrice: "null",
          yetiSwapPrice: "null",
        },
      }
    );
  } else {
    updateResult = await model.updateOne(
      { tokenID },
      {
        $set: {
          nftradePrice: "null",
          kalaoPrice: "null",
          campfirePrice: "null",
          joePegsPrice: "null",
          yetiSwapPrice: "null",
          lastSell: timestamp,
        },
      }
    );
  }

  return updateResult?.matchedCount > 0;
};

/**
 *
 * @param type Type of the event
 * @param data Data of the event
 * @param hash Transaction hash of the event
 * @returns True if event is successfully saved, false otherwise
 */
export const createHistoryAndSave = async (
  type: HISTORY_TYPE,
  data: IDecode,
  hash: String
): Promise<boolean> => {
  const history = new History({
    address: data.tokenAddress.toLowerCase(),
    tokenID: data.tokenID,
    buyer: data.from,
    timestamp: data.timestamp,
    value: data.value,
    transactionHash: hash,
    type,
  });
  try {
    await history.save();
    return true;
  } catch (e) {
    console.log(e);
    return false;
  }
};

/**
 *
 * @param type Type of the event
 * @param tokenID Token ID of NFT
 * @param tokenAddress Token address of NFT
 * @param timestamp Timestamp
 * @param hash Transaction hash of the event
 * @returns True if event is successfully saved, false otherwise
 */
export const createNFTradeCancelHistoryAndSave = async (
  type = HISTORY_TYPE.NFTRADE_CANCEL,
  tokenID: string,
  tokenAddress: string,
  timestamp: string,
  hash: string
): Promise<boolean> => {
  const history = new History({
    address: tokenAddress.toLowerCase(),
    tokenID,
    buyer: "",
    timestamp: timestamp,
    value: "",
    transactionHash: hash,
    type,
  });
  try {
    await history.save();
    return true;
  } catch (e) {
    return false;
  }
};

/**
 *
 * @param collectionName Name of the collection
 * @param tokenID  Token ID of NFT
 * @param kalaoIndex  Index of the NFT in the kalao collection
 * @param price  Price of the NFT
 * @returns  True if NFT is successfully updated, false otherwise
 */
export const saveKalaoAddMarketplaceEvent = async (
  collectionName: string,
  tokenID: string,
  kalaoIndex: string,
  price: string
): Promise<boolean> => {
  try {
    const collection = mongoose.connection.db.collection(
      collectionName.toLowerCase()
    );
    const updateResult: UpdateResult = await collection.updateOne(
      { tokenID },
      {
        $set: {
          kalaoIndex,
          kalaoPrice: price,
        },
      }
    );
    return updateResult.modifiedCount > 0;
  } catch (e) {
    return false;
  }
};

export interface IPrice {
  totalPrice: string;
  avgPrice: string;
  lowestPrice: string;
  totalListed: string;
}

/**
 *
 * @param collectionName Name of the collection
 */
export const getLowestPriceOfCollection = async (collectionName: string) => {
  const model = await getNFTModel(collectionName.toLowerCase());

  if (!model) return null;

  const nftradeLowestPrice = await model
    .findOne({
      nftradePrice: { $ne: "null" },
    })
    .sort({ nftradePrice: 1 })
    .limit(1);

  console.log(nftradeLowestPrice);
};
/**
 *
 * @param value Value of the NFT sell (in ether) (optional)
 * @param tokenID  Token ID of NFT
 * @param address  Address of the collection
 * @param market  Market of the NFT
 * @param operation  Operation type of the NFT
 * @returns  True if NFT is successfully updated, false otherwise
 */
export const updatePricesField = async (
  value: string,
  tokenID: string,
  address: string,
  operation: OPERATION_TYPE
): Promise<boolean> => {
  const collection = mongoose.connection.db.collection("contracts"); // Get contract document from "contracts" collection
  const doc = await collection.findOne({ address: address.toLowerCase() }); // Find contract document
  if (!doc) return false; // If contract document is not found, return false

  const infos = doc.market_total_infos; // Get infos of the contract

  if (operation == OPERATION_TYPE.BUY) {
    infos.totalPrice = parseInt(infos.totalPrice) + Number(value); // Add value to total price
  } else if (operation == OPERATION_TYPE.ADD_MARKETPLACE) {
  }

  if (infos == doc.market_total_infos) {
    return true; // If infos are not updated, return true
  }

  const updateResult: UpdateResult = await collection.updateOne(
    { address: address.toLowerCase() },
    {
      $set: {
        market_total_infos: infos,
      },
    }
  );
  return updateResult.modifiedCount > 0;
};

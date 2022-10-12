// Websocket Instance for listening events from particular contract
import { WebSocketInstance } from "./index";

// Yetiswap Contract ABI
import YETI_ABI from "../abi/yeti.json";

import JOE_ABI from "../abi/joe.json";

// Web3 Types
import { AbiItem } from "web3-utils";
import { Contract, EventData } from "web3-eth-contract";

// .env Configuration
import dotenv from "dotenv";
dotenv.config();

// Nonces MongoDB Model
import { Nonces } from "../models/nonces";
import { setAllPricesToNull } from "../db/helpers";
import { History } from "../models/history";
import { HISTORY_TYPE } from "../enums";

// Logger
import logger from "../helpers/logger";
import getNFTModel from "../models/nft";
import Web3 from "web3";

const yetiContract: Contract = new WebSocketInstance.eth.Contract(
  YETI_ABI as AbiItem[],
  process.env.YETI_CONTRACT_ADDRESS
);

yetiContract.events
  .TokenOnSale({}, (error: any, event: any) => {
    if (error) console.log(error);
  })
  .on("data", async (data: any) => {
    const { nftContract, nftId, price, saleIndex } = data.returnValues;

    const nftModel = await getNFTModel(nftContract.toLowerCase());
    if (!nftModel) return;

    await nftModel.findOneAndUpdate(
      {
        tokenID: nftId,
      },
      {
        $set: {
          yetiIndex: saleIndex,
          yetiSwapPrice: Web3.utils.fromWei(price, "ether"),
        },
      }
    );

    const newHistory = new History({
      address: nftContract.toLowerCase(),
      tokenID: nftId,
      timestamp: Date.now(),
      type: HISTORY_TYPE.YETI_ADD_MARKETPLACE,
      transactionHash: data.transactionHash,
    });

    await newHistory.save();

    logger.info(
      `[${HISTORY_TYPE.YETI_ADD_MARKETPLACE}] - ${data.transactionHash} - Success`
    );
  });

yetiContract.events
  .TokenRemovedFromSale({}, (error: any, event: any) => {
    if (error) console.log(error);
  })
  .on("data", async (data: any) => {
    const { nftContract, nftId, price, saleIndex } = data.returnValues;

    const nftModel = await getNFTModel(nftContract.toLowerCase());
    if (!nftModel) return;

    await nftModel.findOneAndUpdate(
      {
        tokenID: nftId,
      },
      {
        $set: {
          yetiIndex: "null",
          yetiSwapPrice: "null",
          joePegsPrice: "null",
          kalaoPrice: "null",
          nftradePrice: "null",
        },
      }
    );

    const newHistory = new History({
      address: nftContract.toLowerCase(),
      tokenID: nftId,
      timestamp: Math.round(new Date().getTime() / 1000).toString(),
      type: HISTORY_TYPE.YETI_CANCEL,
      transactionHash: data.transactionHash,
    });

    await newHistory.save();
  });

/**
 * Joe Contract Listener
 */
const joeContract: Contract = new WebSocketInstance.eth.Contract(
  JOE_ABI as AbiItem[],
  process.env.JOE_CONTRACT_ADDRESS
);

/**
 * Joe Contract Listener for cancelled multiple orders
 * @returns {user} user - User Address
 * @returns {orderNonces} orderNonces - Integer array of nonces
 */
joeContract.events
  .CancelMultipleOrders({}, (err: any, event: any) => {
    if (err) console.error(err);
  })
  .on("data", async (data: any) => {
    const { user, orderNonces } = data.returnValues;

    const docs = await Nonces.find({
      owner: user.toLowerCase(),
      nonce: { $in: orderNonces },
    });

    for (const nonceDoc of docs) {
      const res = await setAllPricesToNull(
        nonceDoc.contractAddress,
        nonceDoc.tokenID
      );
      console.log("Res from setAllPricesToNull => ", res);

      await Nonces.findByIdAndDelete(nonceDoc._id);

      const newHistory = new History({
        address: nonceDoc.contractAddress.toLowerCase(),
        tokenID: nonceDoc.tokenID,
        timestamp: Math.round(new Date().getTime() / 1000).toString(),
        type: HISTORY_TYPE.JOE_CANCEL,
        transactionHash: data.transactionHash,
      });

      await newHistory.save();
    }
  })
  .on("error", () => {
    console.log("Error on event listener JOE");
  });

/**
 * Joe Contract Listener for cancelled multiple orders
 * @returns {user} user - User Address
 * @returns {orderNonces} orderNonces - Integer array of nonces
 */
joeContract.events
  .TakerAsk({}, (err: any, event: any) => {
    if (err) console.error(err);
  })
  .on("data", async (data: EventData) => {
    const { price, tokenId, collection, currency, taker } = data.returnValues;

    await Nonces.findOneAndDelete({
      contractAddress: collection.toLowerCase(),
      tokenID: tokenId,
    });

    const newHistory = new History({
      address: collection.toLowerCase(),
      tokenID: tokenId,
      timestamp: Math.round(new Date().getTime() / 1000).toString(),
      type: HISTORY_TYPE.JOE_BUY,
      transactionHash: data.transactionHash,
      value: price,
      buyer: taker,
    });

    await newHistory.save();

    await setAllPricesToNull(collection.toLowerCase(), tokenId);

    console.log("TakerAsk with tokenID & collection address => ");
    console.log({
      tokenID: tokenId,
      collection: collection.toLowerCase(),
    });
  })
  .once("connected", () => {
    logger.info("Connected to Joe Contract for listening events");
  })
  .on("error", () => {
    console.log("Error on event listener JOE");
  });

/**
 * Joe Contract Listener for cancelled multiple orders
 * @returns {user} user - User Address
 * @returns {orderNonces} orderNonces - Integer array of nonces
 */
joeContract.events
  .TakerBid({}, (err: any, event: any) => {
    if (err) console.error(err);
  })
  .on("data", async (data: any) => {
    const { price, tokenId, collection, currency, taker } = data.returnValues;

    await Nonces.findOneAndDelete({
      contractAddress: collection.toLowerCase(),
      tokenID: tokenId,
    });

    const newHistory = new History({
      address: collection.toLowerCase(),
      tokenID: tokenId,
      timestamp: Math.round(new Date().getTime() / 1000).toString(),
      type: HISTORY_TYPE.JOE_BUY,
      transactionHash: data.transactionHash,
      value: price,
      buyer: taker,
    });

    await newHistory.save();

    await setAllPricesToNull(collection.toLowerCase(), tokenId);

    console.log("TakerBid with tokenID & collection address => ");
    console.log({
      tokenID: tokenId,
      collection: collection.toLowerCase(),
    });
  })
  .on("error", () => {
    console.log("Error on event listener JOE");
  });

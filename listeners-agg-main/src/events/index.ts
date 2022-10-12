// Global Events
import {
  EVENT_TYPE,
  HISTORY_TYPE,
  OPERATION_TYPE,
  PRICES_MARKETPLACE_TYPE,
  PRICES_NFT,
} from "../enums";

// Event Module Initialization
import EventEmitter from "events";
const emitter: EventEmitter = new EventEmitter();

// Logger
import logger from "../helpers/logger";

// Helpers
import { sleep } from "../helpers";
import {
  IDecode,
  nftradeBuyHelper,
  nftradeCancelHelper,
} from "../helpers/nftrade";

// HTTP Instance
import { HTTPInstance } from "../providers/index";
import {
  isNFTExistInCollection,
  saveKalaoAddMarketplaceEvent,
  setAllPricesToNull,
  updatePricesField,
} from "../db/helpers";
import {
  kalaoAddMarketplaceHelper,
  kalaoBuyHelper,
  kalaoCancelHelper,
} from "../helpers/kalao";
import { History } from "../models/history";
import { joeBuyHelper, joeCancelHelper } from "../helpers/joe";
import mongoose from "mongoose";
import getNFTModel from "../models/nft";

/**
 * @description - NFTrade Cancel Event Handler
 */
emitter.on(EVENT_TYPE.NFTRADE_CANCEL, async (log: any) => {
  logger.info(`[${EVENT_TYPE.NFTRADE_CANCEL}] - ${log.transactionHash}`);
  await sleep(1000);
  const { tokenAddress, tokenID, timestamp } = await nftradeCancelHelper(
    HTTPInstance,
    log.transactionHash
  );

  if (tokenAddress == "") return;

  try {
    if (tokenAddress == "0x0") {
      logger.info(
        `[${EVENT_TYPE.NFTRADE_CANCEL}] - ${log.transactionHash} - Offer Cancelled`
      );
      return;
    }

    const res = await setAllPricesToNull(tokenAddress, String(tokenID));
    if (!res) throw new Error("Failed to set all prices to null");

    const nft = await getNFTModel(tokenAddress);
    if (!nft) throw new Error("Failed to get NFT Model");

    const newHistory = new History({
      address: tokenAddress.toLowerCase(),
      tokenID,
      timestamp,
      type: HISTORY_TYPE.NFTRADE_CANCEL,
      transactionHash: log.transactionHash,
    });

    await newHistory.save();
    logger.info(
      `[${EVENT_TYPE.NFTRADE_CANCEL}] - ${log.transactionHash} - Success`
    );
  } catch (e) {
    logger.error(
      `Error on [${EVENT_TYPE.NFTRADE_CANCEL}] - ${log.transactionHash} - ${e}`
    );
  }
});

/**
 * @description - Kalao Buy Event Handler
 */
emitter.on(EVENT_TYPE.KALAO_BUY, async (log) => {
  logger.info(`[${EVENT_TYPE.KALAO_BUY}] - ${log.transactionHash}`);
  await sleep(1000);
  const returnValue = await kalaoBuyHelper(HTTPInstance, log.transactionHash);

  if (!returnValue) {
    logger.error(`[${EVENT_TYPE.KALAO_BUY}] - ${log.transactionHash} - Failed`);
    return;
  }

  try {
    const { kalaoIndex, tokenAddress, tokenID, from, value, timestamp } =
      returnValue;

    const updateCollectionPrice = await updatePricesField(
      value as string,
      tokenID.toString(),
      tokenAddress,
      OPERATION_TYPE.BUY
    );
    if (!updateCollectionPrice) throw new Error("Update prices failed");

    const res = await setAllPricesToNull(tokenAddress, tokenID, timestamp);
    if (!res) throw new Error("Failed to set all prices to null");

    const nft = await getNFTModel(tokenAddress);
    if (!nft) throw new Error("Failed to get NFT Model");

    const nftData = await nft.findOne({ tokenID: tokenID });
    if (!nftData) throw new Error("Failed to get NFT Data");

    const newHistory = new History({
      address: tokenAddress.toLowerCase(),
      tokenID,
      buyer: from,
      timestamp,
      value: value,
      transactionHash: log.transactionHash,
      type: HISTORY_TYPE.KALAO_BUY,
      reference: nftData?._id,
    });

    await newHistory.save();
    logger.info(`[${EVENT_TYPE.KALAO_BUY}] - ${log.transactionHash} - Success`);
  } catch (e) {
    logger.error(
      `Error on [${EVENT_TYPE.KALAO_BUY}] - ${log.transactionHash} - ${e}`
    );
  }
});

/**
 * @description - Kalao Cancel Event Handler
 */
emitter.on(EVENT_TYPE.KALAO_CANCEL, async (log) => {
  logger.info(`[${EVENT_TYPE.KALAO_CANCEL}] - ${log.transactionHash}`);
  await sleep(1000);
  const returnValue = await kalaoCancelHelper(
    HTTPInstance,
    log.transactionHash
  );

  if (!returnValue) {
    logger.error(
      `[${EVENT_TYPE.KALAO_CANCEL}] - ${log.transactionHash} - Failed`
    );
    return;
  }

  try {
    const { kalaoIndex, tokenAddress, tokenID, from, timestamp } = returnValue;

    const updateCollectionPrice = await updatePricesField(
      "",
      tokenID.toString(),
      tokenAddress,
      OPERATION_TYPE.REMOVE_MARKETPLACE
    );
    if (!updateCollectionPrice) throw new Error("Update prices failed");

    const res = await setAllPricesToNull(tokenAddress, tokenID);
    if (!res) throw new Error("Failed to set all prices to null");

    const nft = await getNFTModel(tokenAddress);
    if (!nft) throw new Error("Failed to get NFT Model");

    const nftData = await nft.findOne({ tokenID: tokenID });
    if (!nftData) throw new Error("Failed to get NFT Data");

    const newHistory = new History({
      address: tokenAddress.toLowerCase(),
      tokenID,
      timestamp,
      transactionHash: log.transactionHash,
      type: HISTORY_TYPE.KALAO_CANCEL,
      reference: nftData?._id,
    });

    await newHistory.save();
    logger.info(
      `[${EVENT_TYPE.KALAO_CANCEL}] - ${log.transactionHash} - Success`
    );
  } catch (e) {
    logger.error(
      `Error on [${EVENT_TYPE.KALAO_CANCEL}] - ${log.transactionHash} - ${e}`
    );
  }
});

/**
 * @description - Kalao Buy Add Marketplace Handler
 */
emitter.on(EVENT_TYPE.KALAO_ADD_MARKETPLACE, async (log) => {
  logger.info(`[${EVENT_TYPE.KALAO_ADD_MARKETPLACE}] - ${log.transactionHash}`);
  await sleep(1000);
  const returnValue = await kalaoAddMarketplaceHelper(
    HTTPInstance,
    log.transactionHash
  );

  if (!returnValue) {
    logger.error(
      `[${EVENT_TYPE.KALAO_ADD_MARKETPLACE}] - ${log.transactionHash} - Failed`
    );
    return;
  }

  try {
    const isNFTExist = await isNFTExistInCollection(
      returnValue.tokenAddress,
      returnValue.tokenID
    );
    if (isNFTExist) {
      console.log("Return Value ", returnValue);

      const updateCollectionPrice = await updatePricesField(
        "",
        returnValue.tokenID.toString(),
        returnValue.tokenAddress,
        OPERATION_TYPE.ADD_MARKETPLACE
      );
      if (!updateCollectionPrice) throw new Error("Update prices failed");

      const isUpdated = await saveKalaoAddMarketplaceEvent(
        returnValue.tokenAddress,
        returnValue.tokenID,
        returnValue.kalaoIndex as string,
        returnValue.value as string
      );
      if (!isUpdated) throw new Error("Failed to update NFT");

      const nft = await mongoose.connection.db
        .collection(returnValue.tokenAddress.toLowerCase())
        .findOne({ tokenID: returnValue.tokenID });
      const newHistory = new History({
        address: returnValue.tokenAddress.toLowerCase(),
        tokenID: returnValue.tokenID,
        timestamp: returnValue.timestamp,
        transactionHash: log.transactionHash,
        type: HISTORY_TYPE.KALAO_ADD_MARKETPLACE,
        reference: nft?._id,
      });

      await newHistory.save();
      logger.info(
        `[${EVENT_TYPE.KALAO_ADD_MARKETPLACE}] - ${log.transactionHash} - Success`
      );
    } else {
      console.log(
        "Creating NFT with kalaoIndex" +
          returnValue.kalaoIndex +
          " tokenAddress => " +
          returnValue.tokenAddress +
          " tokenID => " +
          returnValue.tokenID
      );
    }
  } catch (e) {
    logger.error(
      `Error on [${EVENT_TYPE.KALAO_ADD_MARKETPLACE}] - ${log.transactionHash} - ${e}`
    );
  }
});

export { emitter };

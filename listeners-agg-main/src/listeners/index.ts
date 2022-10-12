// Filters
import { KALAO_FILTERS, NFTRADE_FILTERS, JOE_FILTERS } from "./filters";

// Web3 websocket instance
import { WebSocketInstance } from "../providers";

// Logger
import logger from "../helpers/logger";

// Event emitter
import { emitter } from "../events";

// Sleep function to wait for events
import { sleep } from "../helpers/index";

/**
 * @description - NFTrade Event Handler
 * @param filters - NFTRADE_FILTERS
 * @returns Subscriptions for NFTrade
 */
const setNFTradeFilters = (filters = NFTRADE_FILTERS) => {
  const cancelValues = filters.canceled;

  let nftTradeCancelSubscription = WebSocketInstance.eth
    .subscribe("logs", cancelValues.filter, (error, result) => {
      if (error) logger.error("Error setting NFTrade event listener: ", error);
    })
    .on("connected", (id) =>
      logger.info(`[${cancelValues.eventName}] - Subscription ID: ${id}`)
    )
    .on("data", async (log) => {
      await sleep(1000);
      emitter.emit(cancelValues.eventName, log);
    });

  logger.info("NFTrade listeners set!");

  return { nftTradeCancelSubscription };
};

/**
 * @description - Joe Pegs Handler
 * @param filters - JOE_FILTERS
 * @returns Subscriptions for Joe Pegs Marketplace
 */
const setJOEListeners = (filters = JOE_FILTERS) => {
  const cancelValues = filters.cancelled;
  const buyValues = filters.buyed;

  let joeCancel = WebSocketInstance.eth
    .subscribe("logs", cancelValues.filter, (error, result) => {
      if (error) logger.error("Error setting JOE event listener: ", error);
    })
    .on("connected", (id) =>
      logger.info(`[${cancelValues.eventName}] - Subscription ID: ${id}`)
    )
    .on("data", async (log) => {
      await sleep(1000);
      emitter.emit(cancelValues.eventName, log);
    });

  let joeBuy = WebSocketInstance.eth
    .subscribe("logs", buyValues.filter, (error, result) => {
      if (error) logger.error("Error setting JOE event listener: ", error);
    })
    .on("connected", (id) =>
      logger.info(`[${buyValues.eventName}] - Subscription ID: ${id}`)
    )
    .on("data", async (log) => {
      await sleep(1000);
      emitter.emit(buyValues.eventName, log);
    });

  logger.info("JOE listeners set!");

  return { joeCancel, joeBuy };
};

/**
 * @description - Kalao Event Handler
 * @param filters - KALAO_FILTERS
 * @returns Subscriptions for Kalao
 */
const setKalaoListeners = (filters = KALAO_FILTERS) => {
  const buyValues = filters.buyed;
  const cancelValues = filters.cancel;
  const addValues = filters.add;

  let kalaoBuy = WebSocketInstance.eth
    .subscribe("logs", buyValues.filter, (error, result) => {
      if (error) logger.error("Error setting NFTrade event listener: ", error);
    })
    .on("connected", (id) =>
      logger.info(`[${buyValues.eventName}] - Subscription ID: ${id}`)
    )
    .on("data", async (log) => {
      await sleep(1500);
      emitter.emit(buyValues.eventName, log);
    });

  let kalaoCancel = WebSocketInstance.eth
    .subscribe("logs", cancelValues.filter, (error, result) => {
      if (error) logger.error("Error setting NFTrade event listener: ", error);
    })
    .on("connected", (id) =>
      logger.info(`[${cancelValues.eventName}] - Subscription ID: ${id}\n`)
    )
    .on("data", async (log) => {
      await sleep(1000);
      emitter.emit(cancelValues.eventName, log);
    });

  let kalaoAdd = WebSocketInstance.eth
    .subscribe("logs", addValues.filter, (error, result) => {
      if (error) logger.error("Error setting NFTrade event listener: ", error);
    })
    .on("connected", (id) => {
      logger.info(`[${addValues.eventName}] - Subscription ID: ${id}`);
    })
    .on("data", async (log) => {
      await sleep(1000);
      emitter.emit(addValues.eventName, log);
    });

  logger.info("Kalao listeners set!");

  return { kalaoBuy, kalaoCancel, kalaoAdd };
};

/**
 * @description Set listeners for Kalao and NFTrade events and repeat this subscription every 55 seconds
 */
export const setListeners = () => {
  var kalaoSubs = setKalaoListeners();
  var nftradeSubs = setNFTradeFilters();
  // var joeSubs = setJOEListeners();

  var kalaoBuy = kalaoSubs.kalaoBuy;
  var kalaoCancel = kalaoSubs.kalaoCancel;
  var kalaoAdd = kalaoSubs.kalaoAdd;

  var nftTradeCancelSubscription = nftradeSubs.nftTradeCancelSubscription;

  // var joeCancel = joeSubs.joeCancel;
  // var joeBuy = joeSubs.joeBuy;
  logger.info("All listeners set!");

  setInterval(() => {
    for (let subs of [
      kalaoBuy,
      kalaoCancel,
      kalaoAdd,
      nftTradeCancelSubscription,
      // joeCancel,
      // joeBuy,
    ]) {
      subs.unsubscribe((error, success) => {
        if (error) logger.error("Error unsubscribing: ", error);
      });
    }

    logger.info("Unsubscribed successfully!");

    kalaoSubs = setKalaoListeners();
    nftradeSubs = setNFTradeFilters();
    // joeSubs = setJOEListeners();

    kalaoBuy = kalaoSubs.kalaoBuy;
    kalaoCancel = kalaoSubs.kalaoCancel;
    kalaoAdd = kalaoSubs.kalaoAdd;

    nftTradeCancelSubscription = nftradeSubs.nftTradeCancelSubscription;

    // joeCancel = joeSubs.joeCancel;
    // joeBuy = joeSubs.joeBuy;
  }, 55 * 1000);
};

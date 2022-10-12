import dotenv from "dotenv";
dotenv.config();

// Mongoose
import "./db/mongoose";
import mongoose from "mongoose";

import { HTTPInstance, WebSocketProvider } from "./providers/index";
import { setListeners } from "./listeners";

import logger from "./helpers/logger";

// Contract Events listeners
import "./providers/contracts";
import { nftradeCancelHelper } from "./helpers/nftrade";

WebSocketProvider.on("connect", async () => {
  const blockNumber = await HTTPInstance.eth.getBlockNumber();
  const timestamp = (await HTTPInstance.eth.getBlock(blockNumber)).timestamp;
  logger.info(
    `Connected to Avalanche network at ${new Date(timestamp).toLocaleString()}`
  );
  setListeners();
});

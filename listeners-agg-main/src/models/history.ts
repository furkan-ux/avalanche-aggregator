import { Schema, model } from "mongoose";
import { HISTORY_TYPE } from "../enums";

/**
 * @description - MongoDB History Model
 * @param {string} address - Address of the contract
 * @param {string} tokenID - TokenID of the NFT
 * @param {HISTORY_TYPE} type - Name of the event
 * @param {string} buyer - Address of the buyer
 * @param {string} timestamp - Epoch timestamp of the event
 * @param {string} transactionHash - Transaction hash of the event
 */
const historySchema = new Schema(
  {
    address: {
      type: String,
      required: true,
      trim: true,
      unique: false,
    },
    tokenID: {
      type: String,
      required: true,
      trim: true,
      unique: false,
    },
    buyer: {
      type: String,
      required: false,
      trim: true,
      unique: false,
      default: "",
    },
    timestamp: {
      type: String,
      required: true,
      trim: true,
      unique: false,
    },
    value: {
      type: String,
      required: false,
      trim: true,
      unique: false,
    },
    transactionHash: {
      type: String,
      required: false,
      trim: true,
      unique: false,
      default: "null",
    },
    type: {
      type: String,
      enum: HISTORY_TYPE,
      required: true,
      unique: false,
    },
  },
  {
    timestamps: true,
    autoCreate: true,
  }
);

export const History = model("History", historySchema);

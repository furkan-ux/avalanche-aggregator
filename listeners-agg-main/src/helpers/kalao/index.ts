// Web3
import Web3 from "web3";
import { setDataArr } from "..";
import logger from "../logger";

// Decode Interface
import { IDecode } from "../nftrade";

/**
 *
 * @param web3 Web3 instance
 * @param hash Transaction Hash
 * @returns If transaction is valid return IDecode instance otherwise return null
 */
export const kalaoBuyHelper = async (
  web3: Web3,
  hash: string
): Promise<IDecode | null> => {
  try {
    const transaction = await web3.eth.getTransaction(hash);
    const from = transaction.from;
    const value = transaction.value;
    const kalaoIndex = parseInt(
      transaction.input.replace("0x51ed8288", ""),
      16
    ).toString();

    const transactionReceipt = await web3.eth.getTransactionReceipt(hash);
    const transferLog =
      transactionReceipt.logs[transactionReceipt.logs.length - 2];
    const tokenID = parseInt(
      transferLog.topics.at(-1) as string,
      16
    ).toString();
    const tokenAddress = transferLog.address;
    const timestamp = Math.round(new Date().getTime() / 1000).toString();

    return {
      kalaoIndex,
      tokenAddress,
      tokenID,
      from,
      value,
      timestamp,
    };
  } catch (e) {
    return null;
  }
};

/**
 *
 * @param web3 Web3 instance
 * @param hash Transaction Hash
 * @returns If transaction is valid return IDecode instance otherwise return null
 */
export const kalaoCancelHelper = async (
  web3: Web3,
  hash: string
): Promise<IDecode | null> => {
  try {
    const transaction = await web3.eth.getTransaction(hash);
    const from = transaction.from;
    const kalaoIndex = parseInt(
      transaction.input.replace("0x40e58ee5", ""),
      16
    ).toString();

    const transactionReceipt = await web3.eth.getTransactionReceipt(hash);
    const transferLog =
      transactionReceipt.logs[transactionReceipt.logs.length - 2];

    const tokenID = parseInt(
      transferLog.topics.at(-1) as string,
      16
    ).toString();
    const tokenAddress = transferLog.address;
    const timestamp = Math.round(new Date().getTime() / 1000).toString();

    return {
      kalaoIndex,
      tokenAddress,
      tokenID,
      from,
      timestamp,
    };
  } catch (e) {
    logger.error(e);
    return null;
  }
};

/**
 *
 * @param web3 Web3 instance
 * @param hash Transaction Hash
 * @returns  If transaction is valid return IDecode instance otherwise return null
 */
export const kalaoAddMarketplaceHelper = async (
  web3: Web3,
  hash: string
): Promise<IDecode | null> => {
  try {
    const transaction = await web3.eth.getTransaction(hash);
    const from = transaction.from;

    const transactionReceipt = await web3.eth.getTransactionReceipt(hash);

    const kalaoLog = transactionReceipt.logs.filter(
      (log) => log.address === "0x11AC3118309A7215c6d87c7C396e2DF333Ae3A9C"
    );

    const dataArr = setDataArr(kalaoLog[0].data.slice(2));

    const kalaoIndex = parseInt(dataArr.at(-2) as string, 16).toString();
    const value = parseInt(dataArr.at(-3) as string, 16).toString();

    const transferLog =
      transactionReceipt.logs[transactionReceipt.logs.length - 2];
    const tokenID = parseInt(
      transferLog.topics.at(-1) as string,
      16
    ).toString();
    const tokenAddress = transferLog.address;
    const timestamp = Math.round(new Date().getTime() / 1000).toString();

    return { kalaoIndex, tokenAddress, tokenID, from, value, timestamp };
  } catch (e) {
    console.log(e);
    return null;
  }
};

export const updateKalaoBuyNFT = async (web3: Web3) => {};

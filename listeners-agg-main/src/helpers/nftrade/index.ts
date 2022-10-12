// Logger
import logger from "../logger";

// Helper Functions
import { destroyDataArr, setDataArr } from "../index";

// Web3 Types
import Web3 from "web3";
import { Transaction, TransactionReceipt, Log } from "web3-core";

/**
 * @description - Return interface for decoded log
 */
export interface IDecode {
  tokenAddress: string;
  tokenID: string;
  from?: string;
  value?: string;
  timestamp?: string;
  kalaoIndex?: string;
}

/**
 *
 * @param web3 Web3 instance
 * @param topics Transaction topics for decode
 * @returns Transaction value on WAVAX
 */
export const calculateWAVAXValueOfTransaction = (
  web3: Web3,
  topics: Log[]
): string => {
  let sum: number = 0;
  for (const t of topics) {
    if (
      t?.topics[0] === (process.env.WAVAX_LOG_TOPIC as string) &&
      t?.address == (process.env.WAVAX_ADDRESS as string)
    ) {
      sum += parseInt(t.data, 16);
    }
  }
  return web3.utils.fromWei(sum.toString(), "ether");
};

/**
 *
 * @param web3 Web3 instance
 * @param data Transaction hash
 * @returns { tokenAddress , tokenID , from , value , timestamp } of transaction
 */
export const nftradeBuyHelper = async (
  web3: Web3,
  data: string
): Promise<IDecode> => {
  const transaction: Transaction = await web3.eth.getTransaction(data);
  const from = transaction.from;
  const timestamp = Math.round(new Date().getTime() / 1000).toString();

  const transactionReceipt: TransactionReceipt =
    await web3.eth.getTransactionReceipt(data);
  const log = transactionReceipt.logs[transactionReceipt.logs.length - 1];

  var value = web3.utils.fromWei(transaction.value, "ether");
  var tokenID = parseInt(String(log.topics.at(-1)), 16).toString();

  if (value === "0") {
    const dataArr = setDataArr(transactionReceipt.logs[0].data.slice(2));

    if (dataArr.length !== 25) return { tokenAddress: "", tokenID: "" };

    tokenID = dataArr
      .at(-12)
      ?.slice(10)
      .concat(dataArr.at(-11)?.slice(0, 8) as string) as string;

    console.log(tokenID);
    tokenID = parseInt(tokenID, 16).toString();
    value = calculateWAVAXValueOfTransaction(web3, transactionReceipt.logs);
  }

  console.log("[nftrade-buy-helper] => tokenID => ", tokenID.toString());

  return { tokenAddress: log.address, tokenID, from, value, timestamp };
};

/**
 *
 * @param web3 Web3 instance
 * @param hash Transaction Hash
 * @returns {tokenAddress : string , tokenID : number} Token Address and Token ID of cancelled NFT
 */
export const nftradeCancelHelper = async (
  web3: Web3,
  hash: string
): Promise<{ tokenAddress: string; tokenID: number; timestamp: string }> => {
  const transactionReceipt = await web3.eth.getTransactionReceipt(hash);
  const logData = transactionReceipt.logs[0].data.slice(2);

  const dataArr = setDataArr(logData);
  const timestamp = Math.round(new Date().getTime() / 1000).toString();

  if (dataArr.length !== 10) {
    console.log("[nftrade-cancel-helper] => dataArr.length !== 10");
    return { tokenAddress: "0x0", tokenID: 0, timestamp };
  }
  const { tokenAddress, tokenID } = destroyDataArr(dataArr);

  return { tokenAddress, tokenID, timestamp };
};

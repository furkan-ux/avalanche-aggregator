import Web3 from "web3";

import axios from "axios";
import { setDataArr, sleep } from "../index";
import { IDecode } from "../nftrade";

/**
 *
 * @param web3 Web3 instance
 * @param hash Transaction Hash
 * @returns If transaction is valid return IDecode instance otherwise return null
 */
export const joeCancelHelper = async (web3: Web3, hash: string) => {
  try {
    const transaction = await web3.eth.getTransaction(hash);
    const from = transaction.from;
    const transactionReceipt = await web3.eth.getTransactionReceipt(hash);
    const arr = setDataArr(
      transactionReceipt.logs.at(0)?.data.slice(2) as string
    );
    const nonceID = parseInt(arr.at(-1) as string, 16).toString();

    const res = await axios.get(
      `https://barn.joepegs.com/v2/users/${from}/items?pageSize=100&pageNum=1&connectedUserAddress=`
    );

    const items = res.data;
    for (const saleNft of items) {
      console.log("Nonce => ", saleNft?.currentAsk?.nonce);
      if (saleNft?.currentAsk?.nonce == nonceID) {
        console.log("Cancel Transaction Successful", saleNft);
        const timestamp = Math.round(new Date().getTime() / 1000).toString();
        return {
          nonceID,
          from,
          tokenAddress: saleNft.collection,
          tokenID: saleNft.tokenId,
          timestamp,
        };
      }
    }
    return null;
  } catch (e) {
    console.log(e);
    return null;
  }
};

export const joeBuyHelper = async (
  web3: Web3,
  hash: string
): Promise<IDecode | null> => {
  try {
    await sleep(5000);
    const transaction = await web3.eth.getTransaction(hash);
    const from = transaction.from;

    const transactionReceipt = await web3.eth.getTransactionReceipt(hash);
    const joeLog = transactionReceipt.logs.at(-1)?.data as string;

    const dataArr = setDataArr(joeLog.slice(2));
    if (dataArr.length !== 7) return null;

    const timestamp = Math.round(new Date().getTime() / 1000).toString();
    const value = parseInt(dataArr.at(-1) as string, 16).toString();
    const tokenID = parseInt(dataArr.at(-3) as string, 16).toString();
    const tokenAddress = web3.eth.abi
      .decodeParameter("address", dataArr.at(-4) as string)
      .toString()
      .toLocaleLowerCase();

    return {
      tokenAddress,
      tokenID,
      from,
      value: web3.utils.fromWei(value, "ether"),
      timestamp,
    };
  } catch (e) {
    console.log(e);
    return null;
  }
};

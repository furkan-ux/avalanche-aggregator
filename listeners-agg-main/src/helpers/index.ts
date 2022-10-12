// Global Helpers

export const sleep = (time: number) => {
  return new Promise((resolve) => setTimeout(resolve, time));
};

/**
 *
 * @param data - Data to be converted to string array from hex string
 * @returns - String array from hex string
 */
export const setDataArr = (data: string): string[] => {
  const dataArr = [];
  for (let i = 0; i < data.length / 64; i += 1) {
    dataArr.push(data.slice(64 * i, 64 * (i + 1)));
  }
  return dataArr;
};

/**
 *
 * @param {string[]} data - Array of strings
 * @returns {Object} tokenAddress : string & tokenID : number
 */
export const destroyDataArr = (
  data: string[]
): { tokenAddress: string; tokenID: number } => {
  var tokenAddress = data[4].slice(-32).concat(data[5].slice(0, 8));
  tokenAddress = "0x" + tokenAddress;
  var tokenID = data[5].slice(-56).concat(data[6].slice(0, 8));

  return { tokenAddress, tokenID: parseInt(tokenID, 16) };
};

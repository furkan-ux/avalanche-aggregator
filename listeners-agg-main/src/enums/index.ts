/**
 *  @description - For Nodejs Emitter
 */
export enum EVENT_TYPE {
  // NFTrade Events
  NFTRADE_BUY = "nft-trade-buy",
  NFTRADE_CANCEL = "nft-trade-cancel",

  // Kalao Events
  KALAO_BUY = "kalao-buy",
  KALAO_CANCEL = "kalao-cancel",
  KALAO_ADD_MARKETPLACE = "kalao-add-marketplace",

  // Joe Events
  JOE_CANCEL = "joe-cancel",
  JOE_BUY = "joe-buy",
}

/**
 *  @description - For MongoDB History Model
 */

export enum HISTORY_TYPE {
  // NFTrade Events
  NFTRADE_BUY = "nft-trade-buy",
  NFTRADE_CANCEL = "nft-trade-cancel",

  // Kalao Events
  KALAO_BUY = "kalao-buy",
  KALAO_CANCEL = "kalao-cancel",
  KALAO_ADD_MARKETPLACE = "kalao-add-marketplace",

  // Joe Events
  JOE_CANCEL = "joe-cancel",
  JOE_BUY = "joe-buy",

  // Yeti Events
  YETI_CANCEL = "yeti-cancel",
  YETI_BUY = "yeti-buy",
  YETI_ADD_MARKETPLACE = "yeti-add-marketplace",
}

/**
 * @description - Update related fields depending on operation
 */
export enum OPERATION_TYPE {
  ADD_MARKETPLACE = "add-marketplace",
  REMOVE_MARKETPLACE = "remove-marketplace",

  BUY = "buy",
}

/**
 * @description - Prices fields depending on marketplace name
 */
export enum PRICES_MARKETPLACE_TYPE {
  KALAO = "price_on_kalao",
  JOE = "price_on_joepegs",
  YETI = "price_on_yetiswap",
  NFT_TRADE = "price_on_nftrade",
}

/**
 * @description - Nft prices depending on marketplace name
 */
export enum PRICES_NFT {
  KALAO = "kalaoPrice",
  YETI = "yetiSwapPrice",
  CAMPFIRE = "campfirePrice",
  JOE = "joePegsPrice",
  NFT_TRADE = "nftradePrice",
}

/**
 * @description - Nft marketplaces to be used in the prices
 */
export const MARKETPLACE_TO_PRICE_FIELD = {
  price_on_kalao: PRICES_MARKETPLACE_TYPE.KALAO,
  price_on_joepegs: PRICES_MARKETPLACE_TYPE.JOE,
  price_on_yetiswap: PRICES_MARKETPLACE_TYPE.YETI,
  price_on_nftrade: PRICES_MARKETPLACE_TYPE.NFT_TRADE,
};

export const MARKETPLACE_TO_NFT_FIELD = {
  kalaoPrice: PRICES_NFT.KALAO,
  yetiSwapPrice: PRICES_NFT.YETI,
  campfirePrice: PRICES_NFT.CAMPFIRE,
  joePegsPrice: PRICES_NFT.JOE,
  nftradePrice: PRICES_NFT.NFT_TRADE,
};

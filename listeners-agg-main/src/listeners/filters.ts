import { EVENT_TYPE } from "../enums";

export interface IEvent {
  filter: {
    address: string;
    topics: (string | null)[];
  };
  eventName: EVENT_TYPE;
}

export interface IFilter {
  buyed?: IEvent;
  canceled: IEvent;
  addedToMarketplace?: IEvent;
}

export const NFTRADE_FILTERS: IFilter = {
  canceled: {
    filter: {
      address: process.env.NFTTRADE_CONTRACT_ADDRESS as string,
      topics: [
        "0x02c310a9a43963ff31a754a4099cc435ed498049687539d72d7818d9b093415c",
        null,
        null,
        null,
      ],
    },
    eventName: EVENT_TYPE.NFTRADE_CANCEL,
  },
};

export const KALAO_FILTERS = {
  buyed: {
    filter: {
      address: process.env.KALAO_CONTRACT_ADDRESS as string,
      topics: [
        "0x410787feaee69e25111c916ccc79ee0fb3dd27b169bcb00209efdd59c5148f36",
      ],
    },
    eventName: EVENT_TYPE.KALAO_BUY,
  },
  cancel: {
    filter: {
      address: process.env.KALAO_CONTRACT_ADDRESS as string,
      topics: [
        "0x2c56893f6f6026d19bd17b7d05c9f15c522de1ae2b1c3a825f91a73c799321f2",
      ],
    },
    eventName: EVENT_TYPE.KALAO_CANCEL,
  },
  add: {
    filter: {
      address: process.env.KALAO_CONTRACT_ADDRESS as string,
      topics: [
        "0x20d6e702eee1123eedfe89f5b021b18ca74d59a9789e11e463c679facae7649c",
      ],
    },
    eventName: EVENT_TYPE.KALAO_ADD_MARKETPLACE,
  },
};

export const JOE_FILTERS = {
  cancelled: {
    filter: {
      address: process.env.JOE_CONTRACT_ADDRESS as string,
      topics: [
        "0xfa0ae5d80fe3763c880a3839fab0294171a6f730d1f82c4cd5392c6f67b41732",
        null,
      ],
    },
    eventName: EVENT_TYPE.JOE_CANCEL,
  },
  buyed: {
    filter: {
      address: process.env.JOE_CONTRACT_ADDRESS as string,
      topics: [
        "0x95fb6205e23ff6bda16a2d1dba56b9ad7c783f67c96fa149785052f47696f2be",
        null,
        null,
        null,
      ],
    },
    eventName: EVENT_TYPE.JOE_BUY,
  },
};

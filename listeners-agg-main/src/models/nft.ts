import mongoose, { Schema, model, Model } from "mongoose";
import { isCollectionExistOnMongoDB } from "../db/helpers";

const CollectionNames: {
  [key: string]: any;
} = {};

export interface INFT extends mongoose.Document {
  _id: Schema.Types.ObjectId;
  contractAddress: string;
  t_id: string;
  contractName: string;
  name: string;
  tokenID: string;
  tokenURI: string;
  image: string;
  external_url: string | null;
  thumb: string;
  nftradePrice: string;
  kalaoPrice: string;
  campfirePrice: string;
  joePegsPrice: string;
  yetiSwapPrice: string;
  yetiIndex: string;
  kalaoIndex: string;
  mintTime: string;
  lastSell: string;
  blacklist: boolean;
  metadata?: any[];
  history: Schema.Types.ObjectId[];
}

const nftSchema = new Schema<INFT>(
  {
    contractAddress: {
      type: String,
      required: true,
      trim: true,
      unique: false,
    },
    t_id: {
      type: String,
      required: true,
      trim: true,
      unique: true,
    },
    contractName: {
      type: String,
      required: true,
      trim: true,
      unique: false,
    },
    name: {
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
    tokenURI: {
      type: String,
      required: true,
      trim: true,
      unique: false,
    },
    image: {
      type: String,
      required: true,
      trim: true,
      unique: false,
    },
    external_url: {
      type: String,
      required: false,
      trim: true,
    },
    thumb: {
      type: String,
      required: false,
      trim: true,
    },
    nftradePrice: {
      type: String,
      required: false,
      default: "null",
    },
    kalaoPrice: {
      type: String,
      required: false,
      default: "null",
    },
    campfirePrice: {
      type: String,
      required: false,
      default: "null",
    },
    joePegsPrice: {
      type: String,
      required: false,
      default: "null",
    },
    yetiSwapPrice: {
      type: String,
      required: false,
      default: "null",
    },
    yetiIndex: {
      type: String,
      required: false,
      default: "null",
    },
    kalaoIndex: {
      type: String,
      required: false,
      default: "null",
    },
    mintTime: {
      type: String,
      required: false,
      default: "null",
    },
    lastSell: {
      type: String,
      required: false,
      default: "null",
    },
    blacklist: {
      type: Boolean,
      required: false,
      default: false,
    },
    metadata: {
      type: Array,
      required: false,
      default: ["metadata"],
    },
    history: [
      {
        type: Schema.Types.ObjectId,
        ref: "History",
      },
    ],
  },
  {
    timestamps: true,
    autoCreate: false,
  }
);

const dynamicModel = (collectionName: string): mongoose.Model<INFT> => {
  return model(collectionName, nftSchema);
};

const getNFTModel = async (
  collectionName: string
): Promise<mongoose.Model<INFT> | null> => {
  const isExist = await isCollectionExistOnMongoDB(collectionName);

  if (!isExist) return null;

  if (!CollectionNames[collectionName]) {
    CollectionNames[collectionName] = dynamicModel(collectionName);
  }

  return CollectionNames[collectionName];
};

export default getNFTModel;

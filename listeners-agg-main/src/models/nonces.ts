import mongoose, { Schema, model, Model } from "mongoose";
import { isCollectionExistOnMongoDB } from "../db/helpers";

export interface INonces extends mongoose.Document {
  _id: Schema.Types.ObjectId;
  contractAddress: string;
  tokenID: string;
  nonce: string;
  owner: string;
}

const noncesSchema = new Schema<INonces>({
  contractAddress: {
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
  nonce: {
    type: String,
    required: true,
    trim: true,
    unique: false,
  },
  owner: {
    type: String,
    required: true,
    trim: true,
    unique: false,
  },
});

export const Nonces: Model<INonces> = model<INonces>("nonces", noncesSchema);

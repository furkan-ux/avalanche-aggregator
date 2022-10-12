import mongoose, { ConnectOptions } from "mongoose";

// .env configuration
import dotenv from "dotenv";

// Logger Helper
import logger from "../helpers/logger";

dotenv.config();

mongoose.connect(
  process.env.MONGODB_URL as string as string,
  {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  } as ConnectOptions,
  (err) => {
    if (err) throw new Error("Error connecting to mongoDB");
  }
);

mongoose.connection.on("open", async (ref) => {
  logger.info("Connected to Mongo!");
});

import Web3 from "web3";
import { WebsocketProvider } from "web3-core/types";

// .env Configuration
import dotenv from "dotenv";
dotenv.config();


var WebSocketProvider: WebsocketProvider = new Web3.providers.WebsocketProvider( process.env.WS_PROVIDER_URL as string );

var WebSocketInstance: Web3 = new Web3( WebSocketProvider );

var HTTPInstance: Web3 = new Web3( new Web3.providers.HttpProvider( process.env.HTTP_PROVIDER_URL as string ) );

export { WebSocketInstance, HTTPInstance, WebSocketProvider };
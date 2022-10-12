import axios from 'axios';


// Client for the Kalao API
export const kalaoClient = axios.create( {
    baseURL: "https://marketplace.kalao.io/api",
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Referer: "https://marketplace.kalao.io/explore",
    },
} )

/**
 * @param address - Address of the NFT
 * @returns - Boolean value for if the collection is verified on Kalao Marketplace
 */
export const isVerifiedOnKalao = async ( address: string ): Promise<boolean> => {
    const { data } = await kalaoClient.get( `/certified_collections` );
    const resp = Object.values( data ).some(
        ( item ) => String( item ).toUpperCase() === String( address ).toUpperCase()
    );
    return resp;
}
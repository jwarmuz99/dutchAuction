# Dutch Auction smart contract

In this project, a smart contract for a Dutch Auction is implemented.
The auction works for NFTs (ERC-721 contracts).
Two functions are implemented within a DutchAuction smart contract:
- getCurrentPrice() - this function allows the user to get the current price of item of the auction. 
- buy() - allows a user to buy an item of the auction at or above the current price.

In order to run the project and the testing suite:
- import the dependencies with ```pip install -r requirements.txt```
- compile the smart contract with ```brownie compile```
- run the tests with ```brownie test```

In order to run the tests on the Rinkeby testnet, 
you need to provide the private keys to two accounts funded with ETH on the Rinkeby testnet.
This can be done by filling out the variables in the .env file. 
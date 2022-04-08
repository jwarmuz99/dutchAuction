from brownie import (
    accounts,
    config,
    network,
    Contract,
    interface,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat",
    "development",
    "ganache-local",
    "mainnet-fork",
    "ganache",
]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(account_number, index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS) or (
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"][account_number])

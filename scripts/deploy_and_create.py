from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible, DutchAuction, config, network, accounts
from web3 import Web3

sample_token_uri = "https://ipfs.io/ipfs/QmQoj6HYjDLKaZf2PBGUq7dmwqZ13TRxLawULxf6CEsSJs?filename=0-FRACTAL_UNIVERSE.json"
START_PRICE = Web3.toWei(0.001, "ether")
START_DATE = 1648141200  # 24.03.2022 10:00:00 UTC
END_DATE = 1648659600  # 30.03.2022 10:00:00 UTC
RESERVE_PRICE = Web3.toWei(0.0001, "ether")
NFT_ID = 0


def deploy_erc721():
    account = get_account(0)
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"Awesome, you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button. ")
    return account, simple_collectible


def deploy_auction(nft_owner, nft):
    auction = DutchAuction.deploy(
        START_PRICE,
        START_DATE,
        END_DATE,
        RESERVE_PRICE,
        NFT_ID,
        nft,
        {"from": nft_owner},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    return auction


def approve_auction(nft_owner, nft, auction):
    tx = nft.approve(auction, NFT_ID, {"from": nft_owner})
    tx.wait(1)
    print(f"Approved auction contract {auction.address}")


def sell_nft(auction, seller):
    buyer = get_account(1)
    assert buyer != seller
    current_price = auction.getCurrentPrice()
    print(f"Current price is {current_price}")
    tx = auction.buy({"from": buyer, "value": current_price})
    tx.wait(1)
    print(f"Selling NFT {NFT_ID}")


def main():
    nft_owner, nft = deploy_erc721()
    auction = deploy_auction(nft_owner, nft)
    approve_auction(nft_owner, nft, auction)
    sell_nft(auction, nft_owner)

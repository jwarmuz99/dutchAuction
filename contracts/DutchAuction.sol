// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ISimpleCollectible {
    function transferFrom(
        address _from,
        address _to,
        uint _nftId
    ) external;
}

contract DutchAuction {
    // define the variables
    ISimpleCollectible public immutable nft;
    uint public immutable nftId;

    address payable public immutable seller;
    uint public immutable startPrice;
    uint public immutable reservePrice;
    uint public immutable startDate;
    uint public immutable endDate;

    constructor(
        uint _startPrice,
        uint _startDate,
        uint _endDate,
        uint _reservePrice,
        uint _nftId,
        address _nft
    ) {
        seller = payable(msg.sender);
        startPrice = _startPrice;
        startDate = _startDate;
        endDate = _endDate;
        reservePrice = _reservePrice;
        nft = ISimpleCollectible(_nft);
        nftId = _nftId;
    }


    // helper function to calculate the current price
    function getCurrentPrice() public view returns (uint) {
        // multiplier==10^18 - this is used to calculate the elapsed time percentage with a high precision
        // given the values of the timestamps, I don't see how this can overflow
        uint multiplier = 10000000000000000;
        uint tmp = startPrice * (multiplier - ((block.timestamp - startDate) * multiplier / (endDate - startDate)));
        return  (tmp / multiplier) + reservePrice;
    }

    function buy() public payable {
        // check if the auction is still running
        require(block.timestamp < endDate, "Auction has expired");
        // calculate the current price
        uint price = getCurrentPrice();
        // check if the buyer's bid is at or above the current price
        require(msg.value >= price, "Not enough ether");
        // transfer the token to the buyer
        nft.transferFrom(seller, msg.sender, nftId);
        // calculate the remaining ether
        uint refund = msg.value - price;
        // refund the remaining ether (if there is any
        if (refund > 0) {
            payable(msg.sender).transfer(refund);
        }
        // after the auction ends, the remaining ether is refunded to the seller and the contract is deleted
        selfdestruct(seller);
    }

}

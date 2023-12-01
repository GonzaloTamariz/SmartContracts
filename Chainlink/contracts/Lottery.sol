// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    //0=Open, 1=Closed, 2=Selecting
    enum STATE {
        OPEN,
        CLOSED,
        PROCESSING
    }
    address payable[] public lottery_players = new address payable[](0);
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    STATE public state;
    address payable public last_winner;
    uint256 public random_number;
    uint256 public random_index;
    uint256 public fee;
    bytes32 public keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 5 * (10**18); // 5$
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        state = STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function buyTicket() public payable {
        //5$
        require(state == STATE.OPEN);
        require(msg.value >= getTicketPrice(), "Not enough ETH!");
        lottery_players.push(msg.sender);
    }

    function getTicketPrice() public view returns (uint256) {
        //Calling priceFeed - Chainlink
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; //18 decimals
        uint256 ticketCost = (usdEntryFee * 10**18) / adjustedPrice;
        return ticketCost;
    }

    function startLottery() public onlyOwner {
        require(
            state == STATE.CLOSED,
            "There is a lottery in progress!You can't open a new lottery"
        );
        state = STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        state = STATE.PROCESSING;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(state == STATE.PROCESSING, "Incorrect State");
        require(_randomness > 0, "Random not found");
        random_number = _randomness;
        random_index = random_number % lottery_players.length;
        last_winner = lottery_players[random_index];
        last_winner.transfer(address(this).balance);
        //Reset
        lottery_players = new address payable[](0);
        state = STATE.CLOSED;
    }
}

// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

contract Oracle {
    struct Request {
        uint256 id;
        string url;
        uint256 value;
        mapping(address => uint256) oracles; //1 if hasn't send answer, 2 if has send answer
    }

    event NewRequest(uint256 id, string url);
    event UpdatedRequest(uint256 id, string url, uint256 value);

    Request[] public requests;
    uint256 currentId;

    function newRequest(string memory _url) internal returns (uint256) {
        requests.push(Request(currentId, _url, 0));
        uint256 length = requests.length;
        Request storage r = requests[length - 1];
        //Trusted oracle address - Address of account that are trusted to give the final solution.
        //===============================
        //Rinkeby
        r.oracles[address(0xbB8147F66FaF71A5bA41E5bD074d6562bd9DB362)] = 1; //Rinkeby
        //Local
        r.oracles[address(0xB5fB12fd8148441fE7Ad208135dC376923Ff349B)] = 1; //Local ganache
        //Emit new event. Oracles off-chain will be listening
        emit NewRequest(currentId, _url);
        //Increase request current id;
        currentId++;
        return (currentId - 1);
    }

    function updateRequest(uint256 _id, uint256 _value) public {
        Request storage currentRequest = requests[_id];
        //Check if the oracle is a trusted one.
        if (currentRequest.oracles[address(msg.sender)] == 1) {
            //Oracle has voted
            currentRequest.oracles[address(msg.sender)] = 2;
            currentRequest.value = _value;
            fulfillRandomness(_id);
            emit UpdatedRequest(
                currentRequest.id,
                currentRequest.url,
                currentRequest.value
            );
        }
    }

    function fulfillRandomness(uint256 _requestId) internal virtual {}

    function getValue(uint256 _id) public view returns (uint256) {
        return requests[_id].value;
    }
}

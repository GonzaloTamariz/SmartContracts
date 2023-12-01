// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

contract Oracle {
    struct Request {
        uint256 id;
        string url;
        uint256 votes_number;
        uint256 value;
        uint256[] answers;
        mapping(address => uint256) oracles; //1 if hasn't send answer, 2 if has send answer
    }
    event NewRequest(uint256 id, string url);
    event UpdatedRequest(uint256 id, string url, uint256 value);

    Request[] public requests;
    uint256 currentId;
    uint256 min_votes = 3;

    function newRequest(string memory _url) internal returns (uint256) {
        requests.push(Request(currentId, _url, 0, 0, new uint256[](0)));
        uint256 length = requests.length;
        Request storage r = requests[length - 1];
        //Trusted oracle address - Address of account that are trusted to give the final solution.
        //===============================
        //Rinkeby
        r.oracles[address(0xbB8147F66FaF71A5bA41E5bD074d6562bd9DB362)] = 1; //Rinkeby
        r.oracles[address(0xC9A5E426bC9af443A1D3Cb0539ef96d17db8bea1)] = 1; //Rinkeby
        r.oracles[address(0xc9c68d75123Aa15dcFFcF52ad965bCDF0D3Ec216)] = 1; //Rinkeby
        //Ganache
        r.oracles[address(0xB5fB12fd8148441fE7Ad208135dC376923Ff349B)] = 1; //Ganache
        r.oracles[address(0x3aD774db8f3d772f214Ae509C41D990b05221EAD)] = 1; //Ganache
        r.oracles[address(0x8EC83D8Fd96A13beD7984796B3aC8A3B48FbAD0A)] = 1; //Ganache
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
            //Save answer
            currentRequest.answers.push(_value);
            //Aggregate all answers in the final value.
            currentRequest.value = currentRequest.value + _value / min_votes;
            //Increase count of oracles who have voted.
            currentRequest.votes_number++;
            //If enough oracles have voted
            if (currentRequest.votes_number >= min_votes) {
                //If enough oracles have voted, we have a valid random number.
                fulfillRandomness(_id);
            }
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

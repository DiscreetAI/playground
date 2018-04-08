pragma solidity 0.4.21;


contract Query {

    uint public vectorLength;
    int public totalNumData = 0;
    int public numberOfResponses = 0;
    bool public moreThanOne = false;

    int[] public keyList;
    mapping(int => int[]) public weights;

    /////////////
    // Structs //
    /////////////

    ///////////////
    // Modifiers //
    ///////////////

    //////////////
    //  Events  //
    //////////////

    event ClientSelected(address client);
    event ResponseReceived(int n);
    // event FederatedAveragingComplete();

    ///////////////
    // Functions //
    ///////////////

    function Query(uint _vectorLength, int[] _keyList) {
        vectorLength = _vectorLength;
        keyList = _keyList;
        uint keyLength = keyList.length;
        for (uint i = 0; i < keyLength; i++) {
            weights[keyList[i]] = new int[](keyLength);
        }
    }

    function pingClients(address[] clientList) internal {
        uint clientLen = clientList.length;
        for (uint i = 0; i < clientLen; i++) {
            emit ClientSelected(clientList[i]);
        }
    }

    function sendResponse(
        int[] update,
        int key,
        int numData)
        external
        returns (bool)
        // needs permissioning
    {
        uint i;
        uint keyLen = keyList.length;
        if (moreThanOne) {
            int[] memory newUpdate = new int[](vectorLength);
            
            // scaling
            for (i = 0; i < keyLen; i++) {
                newUpdate[i] = update[i] * numData;
            }
            
            // summation
            for (i = 0; i < keyLen; i++) {
                weights[key][i] = weights[key][i] + newUpdate[i];
            }
        } else {
            for (i = 0; i < keyLen; i++) {
                weights[key][i] = update[i];
            }
            if (weights[key].length == vectorLength) {
                moreThanOne = true;
            }
        }
        numberOfResponses++;
        emit ResponseReceived(numberOfResponses);
        return true;
    }

    function inverseScale()
        external returns (bool)
        // check against threshold
    {
        uint i;
        uint j;
        uint keyLen = keyList.length;
        for (i = 0; i < keyLen; i++) {
            for (j = 0; j < vectorLength; j++) {
                weights[keyList[i]][j] = weights[keyList[i]][j] / totalNumData;
            }
        }
        return true;
    }
}

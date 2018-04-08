pragma solidity 0.4.21;


contract Query {

    int totalNumData = 0;
    int numberOfResponses = 0;
    uint vectorLength = 0;
    bool moreThanOne = false;

    int[] keyList;
    mapping(int => int[]) weights;

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
    event ResponseReceived(int amount);

    ///////////////
    // Functions //
    ///////////////

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
            int[] memory newUpdate;
            
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

pragma solidity 0.4.21;
//pragma experimental ABIEncoderV2;


contract Query {
    // address public parent;
    // address public originator;
    // uint256 public bounty;
    // bytes public searchFields;
    // uint256 public id;
    // uint32 public numberOfDataPoints;
    // // uint32 public targetAverage;           // needs to be talked about
    // bool public active;
    // address[] public contributors;
    // mapping(address => uint8) public contributionLevel;
    // Model public model;

    // // Structs

    // struct IPFS {
    //     string addr;
    // }

    // struct Model {
    //     bytes data;
    //     mapping(uint => int[]) weights;
    // }

    // Modifiers

    // modifier mustBe(address caller) {
    //     require(caller == msg.sender);
    //     _;
    // }
    
    // modifier targetAchieved() {
    //     _;
    // }

    // modifier targetAchieved() {
    //     require(model.currentAverage >= targetAverage);
    //     _;
    // }

    //////////////
    //  Events  //
    //////////////

    event ClientSelected(address client);
    event ResponseReceived(uint amount);

    // Functions

    // function Query(
    //     address _originator,
    //     uint256 _bounty,
    //     bytes _searchFields,
    //     uint256 _id,
    //     address[] outreach) internal
    // {
    //     parent = msg.sender;
    //     originator = _originator;
    //     bounty = _bounty;
    //     searchFields = _searchFields;
    //     id = _id;
    //     active = true;
    //     model = Model(
    //         "abc"
    //     );
    //     for (uint i = 0; i < outreach.length; i++) {
    //         // apiCall(outreach[i]);   // needs to be implemented
    //     }
    // }

    // function () public payable {
    //     msg.sender.transfer(msg.value);        // necessary?
    // }

// ===================

    function pingClients(address[] clientList) internal {
        uint clientLen = clientList.length;
        for (uint i = 0; i < clientLen; i++) {
            emit ClientSelected(clientList[i]);
        }
    }

    // function getModel() external view returns(bytes) { // needs permissioning
    //     return model.data;
    // }

    // mapping(string => int[])[] public respArray;
    // bytes[] metagraphArray;
    // uint[] numDataArray;
    int totalNumData;
    uint numberOfResponses = 0;
    mapping(uint => int[]) weights;
    uint[] keyList;

    // function copy(uint[] arr) private returns(uint[]) {
    //     uint len = arr.length;
    //     uint[len] cp;
    //     for (uint i = 0; i < len; i++) {
    //         cp[i] = arr[i];
    //     }
    //     return cp;
    // }

    function sendResponse(
        //int[][] update,
        int[] update,
        uint[] keys,
        //bytes metagraph,
        int numData)
        external
    {  // needs permissioning
        // scaling
        uint i;
        uint j;
        uint keyLen = keys.length;
        int[][] memory newUpdates;
        // int[] memory newUpdates;
        int[] memory vector;
        uint vectorLength;
        for (i = 0; i < keyLen; i++) {
            //vectorLength = update[i].length;
            vectorLength = update.length / keyLen;
            for (j = 0; j < vectorLength; j++) {
                // vector[j] = update[i][j] * numData;
                vector[j] = update[i * j] * numData;
            }
            newUpdates[i] = vector;
            delete(vector);
        }
        // summation
        for (i = 0; i < keyLen; i++) {
            vectorLength = newUpdates[i].length;
            // vectorLength = newUpdates[i] / keyLen;
            for (j = 0; j < vectorLength; j++) {
                //weights[i][j] = weights[i][j] + newUpdates[i][j];
                weights[keys[i]][j] = weights[keys[i]][j]  + newUpdates[i][j];
            }
        }
        totalNumData = totalNumData + numData;
        numberOfResponses++;
        emit ResponseReceived(numberOfResponses);
    }

    function inverseScale(int[] a)
        external returns (int[])
    { // check against threshold
        uint keyLen = keyList.length;
        for (uint i = 0; i < keyLen; i++) {
            uint vectorLength = weights[keyList[i]].length;
            for (uint j = 0; j < vectorLength; j++) {
                weights[keyList[i]][j] = weights[keyList[i]][j] / totalNumData;
            }
        }
        return a;
    }

// ===================

    // function cancel() public mustBe(parent) {
    //     active = false;
    //     selfdestruct(parent);
    // }

    // function retrieve() internal targetAchieved() {            // finer-grain distribution required
    //     uint256 smallAmount = bounty / numberOfDataPoints;       // remember to account for leftover
    //     // Master master = Master(parent);
    //     address contributor;
    //     uint256 amount;
    //     for (uint i = 0; i < contributors.length; i++) {
    //         contributor = contributors[i];
    //         amount = smallAmount * contributionLevel[contributor];
    //         // master.allocate(contributor, amount);
    //     }
    // }

    // function verify() internal returns (bool) {} // truebit
}

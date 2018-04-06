pragma solidity 0.4.21;


contract Query is Master {
    address public parent;
    address public originator;
    uint256 public bounty;
    bytes public searchFields;
    uint256 public id;
    uint32 public numberOfDataPoints;
    uint32 public targetAverage;           // needs to be talked about
    bool public active;
    address[] public contributors;
    mapping(address => uint8) public contributionLevel;
    Model public model;

    // Structs

    struct IPFS {
        string addr;
    }

    struct Model {
        bytes data;
        mapping(string => int[]) weights;
    }

    // Modifiers

    modifier mustBe(address caller) {
        require(caller == msg.sender);
        _;
    }

    // modifier targetAchieved() {
    //     require(model.currentAverage >= targetAverage);
    //     _;
    // }

    //////////////
    //  Events  //
    //////////////

    event ClientSelected(address client);

    // Functions

    function Query(
        address _originator,
        uint256 _bounty,
        bytes _searchFields,
        uint256 _id,
        address[] outreach) internal
    {
        parent = msg.sender;
        originator = _originator;
        bounty = _bounty;
        searchFields = _searchFields;
        id = _id;
        active = true;
        model = new Model(
            data = "abc",
            weights = [1, 2, 3]
        );
        for (int i = 0; i < outreach.length; i++) {
            apiCall(outreach[i]);   // needs to be implemented
        }
    }

    function () {
        this.value.transfer(parent);        // necessary?
    }

// ===================

    function pingClients(address[] clientList) internal {
        uint clientLen = clientList.length;
        for (uint i = 0; i < clientLen; i++) {
            ClientSelected(clientList[i]);
        }
    }

    function getModel() external pure { // needs permissioning
        return model;
    }

    // mapping(string => int[])[] public respArray;
    // bytes[] metagraphArray;
    // uint[] numDataArray;
    uint totalNumData;
    uint numberOfResponses = 0;

    function sendResponse(
        mapping(uint => int[]) update,
        uint[] keys,
        bytes metagraph,
        uint numData)
        external
        returns(mapping(uint => int[]))
    {  // needs permissioning
        // scaling
        uint keyLen = keys.length;
        mapping(string => int[]) memory newUpdates = update;
        mapping(string => int[]) memory weights = model.weights;
        for (uint i = 0; i < keyLen; i++) {
            newUpdates[keys[i]] = update[keys[i]] * numData;
        }
        for (uint i = 0; i < keyLen; i++) {
            weights[keys[i]] = weights[keys[i]] + newUpdates[keys[i]];
        }
        totalNumData = totalNumData + numData;
        numberOfResponses++;
        return weights;
    }

    function inverseScale(mapping(uint => int[]) update,
        uint[] keys)
        external
        returns(mapping(string => int[]))
    { // check against threshold
        uint keyLen = keys.length;
        mapping(string => int[]) memory newUpdates = update;
        for (uint i = 0; i < keyLen; i++) {
            newUpdates[keys[i]] = update[keys[i]] / totalNumData;
        }
        return newUpdates;
    }

// ===================

    function cancel() public mustBe(parent) {
        active = false;
        selfdestruct(parent);
    }
    
    function retrieve() internal targetAchieved() {            // finer-grain distribution required
        uint256 smallAmount = bounty / numberOfDataPoints       // remember to account for leftover
        Master master = Master(parent);
        address contributor;
        uint256 amount;
        for (int i = 0; i < contributors.length; i++) {
            contributor = contributors[i];
            amount = smallAmount * contributionLevel[contributor];
            master.allocate(contributor, amount);
        }
    }

    function verify() internal returns (bool) {} // truebit
}

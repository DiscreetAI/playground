pragma solidity 0.4.19;


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

    struct Model {
        bytes data;
        uint32 evolutions;
        uint32 currentAverage;
        function(bytes memory) loss;
    }

    modifier mustBe(address caller) {
        require(caller == msg.sender);
        _;
    }

    modifier targetAchieved() {
        require(model.currentAverage >= targetAverage);
        _;
    }

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
            data = "...",
            evolutions = 0,
            currentAverage = 0
            loss = //          ??????????
        );
        for (int i = 0; i < outreach.length; i++) {
            apiCall(outreach[i]);   // needs to be implemented
        }
    }

    function () {
        this.value.transfer(parent);        // necessary?
    }

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
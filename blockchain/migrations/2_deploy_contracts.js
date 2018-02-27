var UserData = artifacts.require('./UserData.sol')

module.exports = function (deployer) {
  deployer.deploy(UserData,{ gas: 3000000 })
}
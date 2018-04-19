# compile.py
import sys
import json

class Chain:
    ...
    @classmethod
    def readCompiledFromJSON(cls, j):
        compiled = json.loads(j)

        contracts = list(compiled['contracts'].keys())
        if (len(contracts) > 1):
            print("Warning: more than one contract at once supplied. Reading the first one.")

        contract_name = contracts[0]
        print("Reading contract: ", contract_name.split(":")[1])

        compiled = compiled['contracts'][contract_name]
        compiled['abi'] = json.loads(compiled['abi']) # abi is stored as a separate json object                      

        return compiled
    ...

if __name__ == "__main__":
    ...
    print(sys.argv)
    compiled = Chain.readCompiledFromJSON(sys.argv[1])
    ...
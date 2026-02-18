# On-chain trace (verifiable receipts)

This document records **verifiable** chain receipts only.
Anything speculative belongs in the private lab repo.

## Contract anchor
- CAW contract: `0xf3b9569F82B18aEf890De263B84189bd33EBe452`
- Chain: Ethereum mainnet

## Proxy-admin / implementation slots (EIP-1967)
These slots being zero indicates **no standard proxy admin/implementation configured**.

- implementation slot: `0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc`
- admin slot:          `0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103`

### Receipts
Command environment:
- RPC: `https://ethereum-rpc.publicnode.com`
- cast: `1.5.1-stable`

`cast storage` outputs:
- implementation slot value: `0x0000000000000000000000000000000000000000000000000000000000000000`
- admin slot value:          `0x0000000000000000000000000000000000000000000000000000000000000000`

## Creation flow (receipts)
- SHIB deployer → intermediary tx: `0xb5b81a63c957fcc33469d59f9c969e860d24574bb72d8b2fc482c7232cb13062`
- intermediary → CAW deployer tx: `0xbfed9c9fe98cf7705b6668afbe9f01c81310f062ae5853b2ac31efd2847f44f0`
- CAW contract creation tx: `0x4d160fb54fbfbf23725f03cc0b780b6666a66c9884f6d1024ef1287321c22515`


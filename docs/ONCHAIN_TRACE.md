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
- SHIB deployer → intermediary tx: `0x...`
- intermediary → CAW deployer tx: `0x...`
- CAW contract creation tx: `0x...`


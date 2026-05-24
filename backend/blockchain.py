import json
import os
from pathlib import Path
from web3 import Web3
from web3.exceptions import Web3Exception

# 1. Import infrastructure targets cleanly from your configuration file
from config import CONTRACT_ADDRESS, GANACHE_URL

# 2. Resilient Path Resolution: Resolves contract artifact locations reliably from any execution directory
SCRIPT_DIR = Path(__file__).resolve().parent
ARTIFACT_PATH = SCRIPT_DIR / "../bike-security-dpp/build/contracts/BikeSecurity.json"

def initialize_blockchain_session():
    """
    Validates environment connectivity, checks address format compliance, 
    and instantiates smart contract tracking objects securely.
    """
    # Initialize the primary network provider node link
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    if not w3.is_connected():
        raise ConnectionError(
            f"CRITICAL: Unable to establish RPC connection lanes with the Ethereum node at: {GANACHE_URL}"
        )

    # Clean compile the target contract address to match standard hexadecimal format requirements
    try:
        checksum_contract_address = w3.to_checksum_address(CONTRACT_ADDRESS)
    except ValueError:
        raise ValueError(
            f"CRITICAL: The configured contract address '{CONTRACT_ADDRESS}' is not a valid hexadecimal string layout."
        )

    # Read smart contract compilation data safely using explicit text encoding markers
    if not ARTIFACT_PATH.exists():
        raise FileNotFoundError(
            f"CRITICAL: Smart contract JSON artifact was not found at expected path: {ARTIFACT_PATH.resolve()}"
        )

    try:
        with open(ARTIFACT_PATH, "r", encoding="utf-8") as artifact_file:
            contract_json = json.load(artifact_file)
            abi = contract_json.get("abi")
            
            if not abi:
                raise KeyError("The contract JSON artifact lacks a valid 'abi' property array.")
    except (json.JSONDecodeError, KeyError) as parse_error:
        raise RuntimeError(f"Failed to process target contract schema metadata: {parse_error}")

    # Build the live smart contract wrapper abstraction instance
    contract = w3.eth.contract(address=checksum_contract_address, abi=abi)

    # Extract an unlocked account profile wrapper safely to assign transaction gas funds
    if not w3.eth.accounts:
        raise RuntimeError(
            "CRITICAL: The targeted Ethereum node contains zero unlocked accounts inside its ledger storage."
        )
        
    signer_account = w3.eth.accounts[0]

    print(f"✅ Web3 layer mapped successfully. Linked to Contract: {checksum_contract_address}")
    return w3, contract, signer_account


# Global execution exposure references
try:
    w3, contract, account = initialize_blockchain_session()
except Exception as init_failure:
    print(f"❌ Blockchain Initialization Aborted: {init_failure}")
    raise SystemExit(1)

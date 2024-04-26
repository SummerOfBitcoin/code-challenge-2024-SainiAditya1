import os
import json
import hashlib
import re

# Set the difficulty target
difficulty_target = '0000ffff00000000000000000000000000000000000000000000000000000000'

# Set the block header
block_header = 'Block Header'

# Set the coinbase transaction
coinbase_tx = {'txid': 'coinbase', 'inputs': [], 'outputs': [{'value': 50, 'address': 'miner_address'}]}

def get_transaction(txid):
    # Get the transaction with the given transaction ID

    # Initialize an empty list to store the transactions
    transactions = []

    # Read the transactions from the mempool
    mempool_dir = 'mempool'
    for filename in os.listdir(mempool_dir):
        with open(os.path.join(mempool_dir, filename), 'r') as f:
            tx = json.load(f)
            transactions.append(tx)

    # Find the transaction with the given transaction ID
    for tx in transactions:
        if 'txid' in tx and tx['txid'] == txid:
            # If the transaction is found, return it
            return tx

    # If the transaction is not found, return None
    return None

def check_input_transaction(vin):
    # Get the previous transaction ID and output index
    prev_txid = vin['txid']
    prev_vout = vin['vout']

    # Check if the previous transaction exists
    prev_transaction = get_transaction(prev_txid)
    if prev_transaction is None:
        return False

    # Check if the previous output exists
    prev_output = prev_transaction['vout'][prev_vout]
    if prev_output is None:
        return False

    # Check if the input value is valid
    if vin['value'] > prev_output['value']:
        return False

    # If the input transaction is valid, return True
    return True


def validate_transaction(tx):
    # Check if the transaction is valid

    # Check if the transaction version is valid
    if tx['version'] != 2:
        return False

    # Check if the transaction locktime is valid
    if tx['locktime'] != 0:
        return False

    # Check if the transaction inputs are valid
    for vin in tx['vin']:
        # Check if the input is a coinbase transaction
        if vin['is_coinbase']:
            # Check if the coinbase transaction is valid
            if not check_coinbase_transaction(vin):
                return False
        else:
            # Check if the input transaction is valid
            if not check_input_transaction(vin):
                return False

    # Check if the transaction outputs are valid
    for vout in tx['vout']:
        # Check if the output is valid
        if not check_output_transaction(vout):
            return False

    # If the transaction is valid, return True
    return True

# Initialize the block transactions list
block_transactions = [coinbase_tx]

# Process the transactions in the mempool
mempool_dir = 'mempool'
for filename in os.listdir(mempool_dir):
    with open(os.path.join(mempool_dir, filename), 'r') as f:
        tx = json.load(f)
        # Validate the transaction
        if validate_transaction(tx):
            block_transactions.append(tx)
            
            
def mine_block(transactions):
    # Create a block string by concatenating the transactions
    block_string = ''.join([json.dumps(tx) for tx in transactions])
    # Calculate the block hash
    block_hash = hashlib.sha256(block_string.encode()).hexdigest()
    # Set the initial nonce value
    nonce = 0
    # Check if the block hash meets the difficulty target
    while int(block_hash, 16) >= int(difficulty_target, 16):
        # Increment the nonce
        nonce += 1
        # Create a new block string with the updated nonce
        block_string = ''.join([json.dumps(tx) for tx in transactions]) + str(nonce)
        # Calculate the new block hash
        block_hash = hashlib.sha256(block_string.encode()).hexdigest()
    # Return the block hash and nonce
    return block_hash, nonce            

# Mine the block
block_hash = mine_block(block_transactions)

# Write the output to a file
with open('output.txt', 'w') as f:
    f.write(block_header + '\n')
    f.write(json.dumps(coinbase_tx) + '\n')
    for tx in block_transactions:
        f.write(tx['txid'] + '\n')

# def validate_transaction(tx):
#     # Check if the transaction is valid

#     # Check if the transaction version is valid
#     if tx['version'] != 2:
#         return False

#     # Check if the transaction locktime is valid
#     if tx['locktime'] != 0:
#         return False

#     # Check if the transaction inputs are valid
#     for vin in tx['vin']:
#         # Check if the input is a coinbase transaction
#         if vin['is_coinbase']:
#             # Check if the coinbase transaction is valid
#             if not check_coinbase_transaction(vin):
#                 return False
#         else:
#             # Check if the input transaction is valid
#             if not check_input_transaction(vin):
#                 return False

#     # Check if the transaction outputs are valid
#     for vout in tx['vout']:
#         # Check if the output is valid
#         if not check_output_transaction(vout):
#             return False

#     # If the transaction is valid, return True
#     return True

def check_coinbase_transaction(vin):
    # Check if the coinbase transaction is valid

    # Check if the input is a coinbase transaction
    if not vin['is_coinbase']:
        return False

    # Check if the input has a single output
    if len(vin['outputs']) != 1:
        return False

    # Check if the output value is valid
    if vin['outputs'][0]['value'] <= 0:
        return False

    # If the coinbase transaction is valid, return True
    return True

def check_input_transaction(vin):
    # Get the previous transaction ID and output index
    prev_txid = vin['txid']
    prev_vout = vin['vout']

    # Check if the previous transaction exists
    prev_transaction = get_transaction(prev_txid)
    if prev_transaction is None:
        return False

    # Check if the previous output exists
    prev_output = prev_transaction['vout'][prev_vout]
    if prev_output is None:
        return False

    # If the previous transaction and output are valid, return True
    return True

def is_valid_address(address):
    # Check if the address is a valid Bitcoin address using a regular expression
    pattern = re.compile('^[13][a-zA-HJ-NP-Z1-9]{25,34}$')
    if pattern.match(address):
        return True
    else:
        return False




def check_output_transaction(vout):
    # Check if the output is valid

    # Check if the output value is valid
    if vout['value'] < 0:
        return False

    # Check if the output address is valid
    if not is_valid_address(vout['address']):
        return False

    # If the output is valid, return True
    return True

def get_transaction(txid):
    # Get the transaction with the given transaction ID

    # Initialize an empty list to store the transactions
    transactions = []

    # Read the transactions from the mempool
    mempool_dir = 'mempool'
    for filename in os.listdir(mempool_dir):
        with open(os.path.join(mempool_dir, filename), 'r') as f:
            tx = json.load(f)
            transactions.append(tx)

    # Find the transaction with the given transaction ID
    for tx in transactions:
        if tx['txid'] == txid:
            # If the transaction is found, return it
            return tx

    # If the transaction is not found, return None
    return None

# def mine_block(transactions):
#     # Create a block string by concatenating the transactions
#     block_string = ''.join([json.dumps(tx) for tx in transactions])
#     # Calculate the block hash
#     block_hash = hashlib.sha256(block_string.encode()).hexdigest()
#     # Set the initial nonce value
#     nonce = 0
#     # Check if the block hash meets the difficulty target
#     while int(block_hash, 16) >= int(difficulty_target, 16):
#         # Increment the nonce
#         nonce += 1
#         # Create a new block string with the updated nonce
#         block_string = ''.join([json.dumps(tx) for tx in transactions]) + str(nonce)
#         # Calculate the new block hash
#         block_hash = hashlib.sha256(block_string.encode()).hexdigest()
#     # Return the block hash and nonce
#     return block_hash, nonce
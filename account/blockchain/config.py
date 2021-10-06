'''
Configs for blockchain module
'''

CHAINDATA_DIR = 'chaindata/'
BROADCASTED_BLOCK_DIR = CHAINDATA_DIR + 'blocs/'
NUM_ZEROS = 3

PEERS = [
    'http://localhost:5000/',
    'http://localhost:5001/',
    'http://localhost:5002/',
    'http://localhost:5003/',
    ]

BLOCK_VAR_CONVERSIONS = {
    'index': int,
    'nonce': int, 
    'hash': str, 
    'prev_hash': str, 
    'timestamp': str,
    }


# https://github.com/jackschultz/jbc/blob/part-2/block.py

# len(self) in class python
# **kwargs in function
# **kwargs in function as dictionary
# glob
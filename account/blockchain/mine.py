from block import Block
import sync
from config import *
import utils

import json, hashlib, requests, os, glob
import datetime as date

def mine_for_block():
    print('[ACTION]:mine for block sync')
    current_chain = sync.sync_local()           #gather last node
    print('[DONE]:mine for block sync')
    prev_block = current_chain.most_recent_block()
    new_block = mine_blocks(prev_block)
    new_block.self_save()
    return new_block

def mine_blocks(block):
    index = int(block.index) + 1
    timestamp = date.datetime.now().strftime('%s')
    data = f'I am a block #{index}'
    prev_hash = block.hash
    nonce = 0

    block_info_dict = utils.dict_from_block_attributes(index=index, timestamp=timestamp, data=data, prev_hash=prev_hash, nonce=nonce)
    new_block = Block(block_info_dict)
    return find_valid_nonce(new_block)

def find_valid_nonce(new_block):
    print('[ACTION]:finding valid nonce')
    new_block.update_self_hash()
    while new_block.is_valid():
        new_block.nonce += 1
    print(f'[DONE]:block is mined. nonce = {new_block.nonce}')
    assert new_block.is_valid(), 'Block is not valid'
    return new_block

if __name__ == '__main__':
    mine_for_block()



# def generate_header(index, prev_hash, data, timestamp, nonce):
#     return str(index) + prev_hash + data + str(timestamp) + str(nonce)

# def calculate_hash(index, prev_hash, data, timestamp, nonce):
#     header_string = generate_header(index, prev_hash, data, timestamp, nonce)
#     sha = hashlib.sha256()
#     sha.update(header_string)
#     return sha.hexdigest()

# node_blocks = sync.sync()

# def mine(last_block):
#     index = int(last_block.index) + 1
#     timestamp = date.datetime.now()
#     data = "I block #%s" % (index) #random string for now, not transactions
#     prev_hash = last_block.hash
#     nonce = 0

#     block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)

#     while str(block_hash[0:NUM_ZEROS] != '0' * NUM_ZEROS):
#         nonce += 1
#         block_hash = calculate_hash(index, prev_hash, data, timestamp, nonce)
    
#     block_data = {}
#     block_data['index'] = index
#     block_data['timestamp'] = timestamp
#     block_data['data'] = data
#     block_data['prev_hash'] = prev_hash
#     block_data['hash'] = block_hash
#     block_data['nonce'] = nonce
#     return Block(block_data)

# if __name__ == '__main__':
#     node_blocks = sync.sync() #gather last node
#     prev_block = node_blocks[-1]
#     new_block = mine(prev_block)
#     new_block.self_save()
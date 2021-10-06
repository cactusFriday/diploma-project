# creates first genesis block
from block import Block
from mine import find_valid_nonse
from config import *
import datetime as date
import os, json


def create_first_block():
    block_data = {}
    block_data['index'] = 0
    block_data['timestamp'] = date.datetime.now().strftime('%s')
    block_data['data'] = 'First block data'
    block_data['prev_hash'] = ''
    block_data['nonce'] = 0
    return Block(block_data)

if __name__ == '__main__':
    if not os.path.exists(CHAINDATA_DIR):
        os.mkdir(CHAINDATA_DIR)
        first_block = create_first_block()
        # function return Block() object with valid hash
        first_block = find_valid_nonse(first_block)
        first_block.self_save()

    if os.listdir(CHAINDATA_DIR) == []:
        print('Chaindata dir already exists with blocks.\nIf you want to regenerate the blocks, delete /chaindata and rerun')
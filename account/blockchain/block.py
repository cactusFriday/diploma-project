import datetime as date
import hashlib
import os
import json

from .config import *

class Block(object):
    def __init__(self, dictionary):
        '''
        we are looking for the index, timestamp, prev_hash, data, nonce
        '''
        for key, val in dictionary.items():
            if key in BLOCK_VAR_CONVERSIONS:
                # checks what dict BLOCK_VAR_CONVERSIONS contains next to [key] (<class int>) and return int number, that in val, or converts it
                setattr(self, key, BLOCK_VAR_CONVERSIONS[key](val))
            else:
                setattr(self, key, val)
        if not hasattr(self, 'hash'):
            self.hash = self.update_self_hash()
        if not hasattr(self, 'nonce'):
            self.nonce = 'None'
    
    def header_string(self):
        return (str(self.index) + self.prev_hash + self.data + str(self.timestamp) + str(self.nonce)).encode()

    # def generate_header(self, index, prev_hash, data, timestamp, nonce):
    #     return str(index) + prev_hash + data + str(timestamp) + str(nonce)

    def update_self_hash(self):
        sha = hashlib.sha256()
        sha.update(self.header_string())
        new_hash = sha.hexdigest()
        self.hash = new_hash
        return new_hash

    def self_save(self):
        index_string  = str(self.index).zfill(6)
        filename = f'{CHAINDATA_DIR}/{index_string}.json'
        if not os.path.exists(CHAINDATA_DIR):
            os.mkdir(CHAINDATA_DIR)
        with open(filename, 'w') as block_file:
            json.dump(self.to_dict(), block_file)

    def to_dict(self):
        info = {}
        info['index'] = str(self.index)
        info['timestamp'] = str(self.timestamp)
        info['prev_hash'] = str(self.prev_hash)
        info['hash'] = str(self.hash)
        info['data'] = str(self.data)
        info['nonce'] = str(self.nonce)
        return info

    def is_valid(self):
        self.update_self_hash()
        if self.hash[0:NUM_ZEROS] == '0' * NUM_ZEROS:
            return True
        else:
            return False

    def __repr__(self):
        return f'Block <index: {self.index}>, <hash: {self.hash}>'
    
    def __eq__(self, other):
        return (self.index == other.index and
            self.timestamp == other.timestamp and
            self.prev_hash == other.prev_hash and
            self.hash == other.hash and
            self.data == other.data and
            self.nonce == other.nonce)

    def __ne__(self, value):
        return not self.__eq__(value)
    
    def __gt__(self, value):
        return self.timestamp < value.timestamp
    
    def __lt__(self, value):
        return self.timestamp > value.timestamp

# def create_first_block():
#     block_data = {}
#     block_data['index'] = 0
#     block_data['timestamp'] = date.datetime.now()
#     block_data['data'] = 'First block data'
#     block_data['prev_hash'] = ''
#     block_data['nonce'] = 0
#     return Block(block_data)

# if __name__ == '__main__':
#     chaindata_dir = 'chaindata'
#     if not os.path.exists(chaindata_dir):
#         os.mkdir(chaindata_dir)
#     if os.listdir(chaindata_dir) == []:
#         first_block = create_first_block()
#         first_block.self_save()
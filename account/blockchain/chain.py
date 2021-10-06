from .block import Block

class Chain(object):
    def __init__(self, blocks):
        self.blocks = blocks
    
    def is_valid(self):
        for index, block in enumerate(self.blocks[1:]):
            prev_block = self.blocks[index]
            if block.index != prev_block.index:             # check for rightful indexes sequence
                return False
            if not block.is_valid():                        # check for valid block's hash
                return False
            if block.prev_hash != prev_block.hash:
                return False
            return True
    
    def self_save(self):
        for b in self.blocks:
            b.self_save()
        return True
    
    def find_block_by_index(self, index):
        if len(self) <= index:
            return self.blocks[index]
        else:
            return False
        # for block in self.blocks:
        #     if block.index == index:
        #         return block
    def find_block_by_hash(self, hash):
        for block in self.blocks:
            if block.hash == hash:
                return block
        return False
    
    def __len__(self):
        return len(self.blocks)
    # equal
    def __eq__(self, value):
        if len(self) != len(value):
            return False
        for self_block, anoth_block in zip(self.blocks, value.blocks):
            if self_block != anoth_block:
                return False
        return True
    # not equal
    def __ne__(self, other):
        return not self.__eq__(other)
    # greater than
    def __gt__(self, other):
        return len(self.blocks) > len(other.blocks)
    # lesser than
    def __lt__(self, other):
        return len(self.blocks) < len(other.blocks)
    # greater or equal
    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    # lesser or equal
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def most_recent_block(self):
        return self.blocks[-1]
    
    def max_index(self):
        return self.blocks[-1].index

    def add_block(self, new_block):
        if new_block.index > len(self):
            pass
        self.blocks.append(new_block)
        return True
    
    def block_list_dict(self):
        return [b.to_dict() for b in self.blocks]
import datetime
import hashlib
import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.cur_products=[]
        self.nodes = set()

        _init_block = self.new_block(prev_hash = '1', proof = 100)
        
    def new_block(self, proof, prev_hash = None):
        # Creates a new Block and adds it to the chain
        _new_block = Block()
        _new_block._init(len(self.chain) + 1)
        _new_block.prev_hash = prev_hash or self.chain[-1].cur_hash
        _new_block.proof = proof

        #
        #_new_block.product = _new_product

        self.chain.append(_new_block)
        return _new_block
    
    def _new_product(self, name, manufacturer):
        _new_product = {'name':name, 'manufacturer':manufacturer}
        self.cur_products.append(_new_product)
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            #print(f'{last_block}')
            #print(f'{block}')
            #print("\n-----------\n")
            # Check that the hash of the block is correct
            if block.prev_hash != last_block.cur_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block.proof, block.proof):
                return False

            last_block = block
            current_index += 1

        return True
    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
class Block:
    def __init__(self):
        self.index = -1
        self.product = None
        self.timestamp = None
        self.prev_hash = None
        self.cur_hash= None
        self.proof = None
    
    def _hash_block(self):
        return hashlib.sha256(bytearray(str(self.prev_hash) + str(self.timestamp) + str(self.index), "utf-8")).hexdigest()

    def _init(self, index):
        self.timestamp = time.time()
        self.cur_hash = self._hash_block()
        self.index = index

    def _validate(self):
        pass
    
    def _show(self):
        return 'Block<index: {}, timestamp: {}, prev_hash: {}, hash: {}, product: {}>'.format(
			self.index, self.timestamp, self.prev_hash, self.cur_hash, self.product)
    



import hashlib
import json
from time import time

class SimpleBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()
        
    def create_genesis_block(self):
        # Create the genesis block with a predetermined proof and previous hash
        self.create_new_block(previous_hash='1', proof=100)
        
    def create_new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def create_new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.latest_block['index'] + 1

    @staticmethod
    def hash_block(block):
        # Ensure the block is ordered before hashing
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def latest_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.is_valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def is_valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Example usage
blockchain = SimpleBlockchain()
last_proof = blockchain.latest_block['proof']
proof = blockchain.proof_of_work(last_proof)

blockchain.create_new_transaction(sender="address1", recipient="address2", amount=5)
previous_hash = blockchain.hash_block(blockchain.latest_block)
block = blockchain.create_new_block(proof, previous_hash)

print("Blockchain:", blockchain.chain)

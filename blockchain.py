import datetime as _dt
import hashlib as _hashlib
import json as _json
import timeit

max_block=dict()
class Blockchain:

    def __init__(self) -> None:
        self.chain=list()
        genesis_block=self._create_block(data=["iam the genesis block","Hello"],proof=1,previous_hash="0",index=0)
        self.chain.append(genesis_block)
        max_block.update({self:len(self.chain)})
    def mine_block(self,data:list) ->dict:
        a=False
        for x,y in max_block.items():
            if len(self.chain)< y:
                a=True
                self=x
                break
        previous_block=self.get_previous_block()
        previous_proof=previous_block["proof"]
        index=len(self.chain)+1
        proof=self._proof_of_work(previous_proof,index,data)
        previous_hash=self._hash(block=previous_block)
        block=self._create_block(data=data,proof=proof,previous_hash=previous_hash,index=index)
        self.chain.append(block)
        max_block.update({self: len(self.chain)})
        return block
    def _hash(self,block:dict) ->str:
        encoded_block=_json.dumps(block,sort_keys=True).encode()
        return _hashlib.sha256(encoded_block).hexdigest()
        pass


    def _to_digest(self,new_proof:int,previous_proof:int,index:str,data:list)->bytes:
        str1 = ""
        for ele in data:
            str1 += ele
        to_digest=str(new_proof**2-previous_proof**2+index)+str1
        return to_digest.encode()





    def _proof_of_work(self,previous_proof:str,index:int,data:list)-> int:
        new_proof=1
        check_proof=False
        while not check_proof:
            to_digest=self._to_digest(new_proof=new_proof,previous_proof=previous_proof,index=index,data=data)
            hash_value=_hashlib.sha256(to_digest).hexdigest()
            if hash_value[:5]== "00000":
                check_proof=True
            else:
                new_proof+=1

        return new_proof
    def get_previous_block(self)->dict:
        return self.chain[-1]

    def _create_block(self,data:list,proof:int,previous_hash:str,index:int) -> dict:
        block={
            "index":index,
            "timestamp":str(_dt.datetime.now()),
            "data":data,
            "proof":proof,
            "previous_hash":previous_hash
        }
        return block
    def is_chain_valid(self) ->bool:
        current_block=self.chain[0]
        block_index=1
        while block_index < len(self.chain):
            next_block=self.chain[block_index]
            if next_block["previous_hash"] != self._hash(current_block):
                print("next_block="+next_block["previous_hash"])
                print("current_block=" + self._hash(current_block))


                return False
            current_proof=current_block["proof"]
            next_index,next_data,next_proof=(next_block["index"],next_block["data"],next_block["proof"])
            hash_value=_hashlib.sha256(
                self._to_digest(new_proof=next_proof,previous_proof=current_proof,index=next_index,data=next_data)
            ).hexdigest()
            if hash_value[:5]!="00000":
                return False
            current_block=next_block
            block_index+=1
        return True



initial_block=Blockchain()
initial_block.mine_block(["mostafa","mohsen"])
second_block=Blockchain()
second_block.mine_block(["eldeeb"])
second_block.mine_block(["eldeeb"])
second_block.mine_block(["eldeeb"])
initial_block.mine_block(["mostafa","mohsen"])
print(initial_block.chain)

"""
start = timeit.default_timer()
initial_block.mine_block(["ahmed pays ali 200 L.E","ali plays mossad 5002.5 L.E","moftah takes from mohsen 700 L.E","Mohsen takes 20000 L.E","zaherz buy 20.7 L.E"])
stop = timeit.default_timer()
print('Time: ', stop - start)
print(initial_block.chain)

print(initial_block.chain)
b=initial_block.is_chain_valid()
"""



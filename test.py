import datetime
import hashlib
import time
from urllib.parse import urlparse
import requests
import json
from blockchain import Blockchain

if(__name__ == '__main__'):
    chains = Blockchain()

    chains.new_block(100)
    #print(chains.chain[0]._show())
    #print(chains.chain[1]._show())

    print("***************\n")
    json_string = json.dumps([ob.__dict__ for ob in chains.chain])
    print(json_string)
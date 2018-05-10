import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from blockchain import Blockchain

import requests
# from flask import Flask, jsonify, request
from flask import Flask, request, redirect, render_template, flash, jsonify


# Instantiate the Node
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/') 
def index():       
  return render_template('index.html')

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'products': block['products'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    # return jsonify(response), 200
    flash(response['message'])
    return	render_template('index.html', new_block = response)

@app.route('/products/new', methods=['POST'])
def new_product():
    # values = request.get_json()
    values = {
        'name': request.form['name'],
        'ptype': request.form['type'],
        'manufacturer': request.form['manu'],
        'description': request.form['description']
    }
    # Check that the required fields are in the POST'ed data
    for key, value in values.items():
        if len(value) < 1:
            flash('Missing values')
            # return 'Missing values', 400
            return	render_template('index.html')
    # Create a new Product
    index = blockchain.new_product(values['name'], values['ptype'], values['manufacturer'], values['description'])
    # response = {
    #     'message': f'New food will be added to Block {index}',
    #     'food': values
    # }
    # return jsonify(response), 201
    flash(f'New food will be added to Block {index}')
    return	render_template('index.html', added_food = values)


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    # return jsonify(response), 200
    return	render_template('index.html', chain = response)

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    # values = request.get_json()
    values = {
        'nodes': request.form['nodes'],
    }

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return render_template('index.html', nodes = response)


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
    flash(response['message'])
    # return jsonify(response), 200
    return render_template('index.html', chain = response)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
from flask import jsonify, request
from uuid import uuid4
from src import app
from src.models.Blockchain import Blockchain


node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(node_address, 'Ivo', 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'done!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transaction': block['transactions']}
    return jsonify(response), 200


@app.route('/', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    if blockchain.is_chain_valid(blockchain.chain):
        response = {'is_valid': True}
        return jsonify(response), 200
    else:
        response = {'is_valid': False}
        return jsonify(response), 400


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']

    if not all(key in json for key in transaction_keys):
        return 'Missing elements', 400

    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'queued transaction to block {index}'}

    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    if nodes is None:
        return "Empty", 400

    for node in nodes:
        blockchain.add_node(node)

    response = {'message': 'All nodes was connected',
                'total_nodes': list(blockchain.nodes)}

    return jsonify(response), 201


@app.route('/sync', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'the nodes have been replaced',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'there was no replacement',
                    'actual_chain': blockchain.chain}

    return jsonify(response), 201

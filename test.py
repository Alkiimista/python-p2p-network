#######################################################################################################################
# AVANS - BLOCKCHAIN - MINOR MAD                                                                                      #
#                                                                                                                     #
# Author: Maurice Snoeren                                                                                             #
# Version: 0.1 beta (use at your own risk)                                                                            #
#                                                                                                                     #
# Example python script to show the working principle of the TcpServerNode Node class.                                #
#######################################################################################################################

import time
import json
import pprint
import hashlib
from TcpServerNode import Node
from jsonNode import Node as jsonnode
from jsonTransaction import Transaction
from jsonTransaction import TransactionClass
from jsonNode import Message
from jsonBlock import Block
from jsonKey import Key
from jsonKey import KeyClass

node1 = None
node2 = None


def callbackNodeEvent(event, node, other, data):
    print(event)
    print(data)
    if event == "DISCOVERY":
        nodesarr = []
        for n in node.nodesOut:
            if n.port != other.port:
                temp = jsonnode(n.host, n.port)
                nodesarr.append(temp)
        senddata = Message('RETURNDISCOVERY', nodesarr).to_dict()
        print(senddata)
        dumpdata = json.dumps(senddata)
        print(dumpdata)
        node.send_to_node(other, dumpdata)

    else:
        if event == "RETURNDISCOVERY":
            print("nodes received")
            temp = Message.from_dict(data)
            nodes = temp.nodes

            for n in nodes:
                i = 0
                for n2 in node.nodesOut:
                    if n.port == n2.port:
                        i = 1
                if i == 0:
                    node.connect_with_node(n.ip, n.port)
                    print("connect with %s %d" % (n.ip, n.port))

        else:
            if event == "BLOCK":
                # TODO implement logic
                print("block received")

                block_hash = hashlib.sha3_256(json.dumps(data).encode()).hexdigest()
                print("Received block: " + block_hash)
                block = Block.from_dict(data)
                if block_hash.startswith('abcde') and block not in node.block_chain:
                    # TODO also verify the transactions in this block
                    node.block_chain.append(block)
                    for blocktransaction in block.transactions:
                        if blocktransaction.to_other_transaction() in node.transaction_data_pool:
                            node.transaction_data_pool.remove(blocktransaction.to_other_transaction())

                    for n in node.nodesOut:
                        if n.port != other.port:
                            # print("Broadcasting block")
                            block_to_send = block.to_dict()
                            node.send_to_node(n, json.dumps(block_to_send))
            else:
                if event == "TRANSACTION":
                    transaction_hash = hashlib.sha3_256(json.dumps(data).encode()).hexdigest()
                    print("Received hash " + transaction_hash)
                    if transaction_hash not in node.transaction_pool:
                        tx = Transaction.from_dict(data)
                        if tx.transaction.to and tx.transaction.transaction_from and tx.transaction.amount:
                            node.transaction_pool.append(transaction_hash)
                            node.transaction_data_pool.append(tx)
                            # print(node.transaction_pool)
                            # print(tx.transaction.transaction_from)
                            for n in node.nodesOut:
                                if n.port != other.port:
                                    # print("Broadcasting transaction")
                                    transaction_to_send = tx.to_dict()
                                    node.send_to_node(n, json.dumps(transaction_to_send))
                else:
                    if event == "PUBKEY":
                        key = Key.from_dict(data)
                        tempKey = key.to_dict()

                        # Check if the keylist is empty
                        if not bool(node.keyList):
                            # node.keyList.update({"originID": tempKey.get("key").get("originID"),
                            #                      "publicKey": tempKey.get("key").get("publicKey")})
                            node.keyList.update({"key": tempKey.get("key")})
                        else:

                            # Check if there are any existing connections
                            for i, j in node.keyList.items():
                                if(j["originID"] != tempKey.get("key").get("originID")):
                                    # TODO fix bug where key gets overwritten
                                     node.keyList.update({"key": tempKey.get("key")})
                                    # node.keyList.update([(tempKey.get("key").get("originID"), tempKey.get("key").get("publicKey"))])


    #TODO blocks

node1 = Node('localhost', 10000, callbackNodeEvent)
node2 = Node('localhost', 20000, callbackNodeEvent)
node3 = Node('localhost', 30000, callbackNodeEvent)

node2.start()
node3.start()

node2.connect_with_node('localhost', 30000)

node1.start()
node1.connect_with_node('localhost', 20000)

#node1.terminate_flag.set()  # Stopping the thread

data = {}
data['event'] = "DISCOVERY"
senddata = json.dumps(data)

node1.send_to_nodes(senddata)
data = {}

node4 = Node('localhost', 40000, callbackNodeEvent)
node4.start()
node4.connect_with_node('localhost', 10000)
node4.send_to_nodes(senddata)

new_transaction = Transaction("TRANSACTION", TransactionClass("Chris", "Max", 100))
serialized_transaction = new_transaction.to_dict()
dump_transaction = json.dumps(serialized_transaction)
node4.send_to_nodes(dump_transaction)

new_transaction = Transaction("TRANSACTION", TransactionClass("Max", "Duc", 50))
serialized_transaction = new_transaction.to_dict()
dump_transaction = json.dumps(serialized_transaction)
node4.send_to_nodes(dump_transaction)


def send_block(node: Node):
    block_hash = ''
    nonce = 0
    block_transactions = []
    for transaction in node.transaction_data_pool:
        block_transactions.append(transaction.transaction.to_block_transaction())

new_key = Key("PUBKEY", KeyClass(node1.id, "Secret_Key"))
serialized_key = new_key.to_dict()
dump_key = json.dumps(serialized_key)
node1.send_to_nodes(dump_key)
new_key = Key("PUBKEY", KeyClass("2", "Secret_Key"))
serialized_key = new_key.to_dict()
dump_key = json.dumps(serialized_key)
node1.send_to_nodes(dump_key)
node1.send_to_nodes(dump_key)

    block = Block("BLOCK", nonce, '0', block_transactions)
    while not block_hash.startswith('abcde'):
        serialized_block = json.dumps(block.to_dict())
        block_hash = hashlib.sha3_256(serialized_block.encode()).hexdigest()
        block.nonce += 1
    node.send_to_nodes(serialized_block)

sent_block = False
while (True):
    time.sleep(2)
    if (len(node3.transaction_pool) > 1) and not sent_block:
        send_block(node3)
        sent_block = True

    # print("------------------------- node1 connected with %d" % (len(node1.nodesIn)+len(node1.nodesOut)))
    # print("------------------------- node2 connected with %d" % (len(node2.nodesIn)+len(node2.nodesOut)))
    # print("------------------------- node3 connected with %d" % (len(node3.nodesIn)+len(node3.nodesOut)))
    # print("------------------------- node4 connected with %d" % (len(node4.nodesIn)+len(node4.nodesOut)))


node1.stop()
node2.stop()

node1.join()
node2.join()

print("main stopped")


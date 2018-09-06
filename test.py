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

#from DP2PNodeClass import DP2PNode
from TcpServerNode import Node
from jsonNode import Node as jsonnode
from jsonNode import Message

node1 = None
node2 = None

def callbackNodeEvent(event, node, other, data):
    if(event == "DISCOVERY"):
        nodesarr = []
        for n in node.nodesOut:
            if(n.port != other.port):
                temp = jsonnode(n.host, n.port)
                nodesarr.append(temp)
        senddata = Message('RETURNDISCOVERY',nodesarr).to_dict()
        print(senddata)
        dumpdata = json.dumps(senddata)
        print(dumpdata)
        node.send2node(other,dumpdata)


    if(event == "RETURNDISCOVERY"):
        print("nodes recieved")
        temp = Message.from_dict(data)
        nodes = temp.nodes


        for n in nodes:
            i = 0
            for n2 in node.nodesOut:
                if n.port == n2.port:
                    i = 1
            if i == 0:
                node.connectWithNode(n.ip, n.port)
                print("connect with %s %d" %(n.ip ,n.port))


node1 = Node('localhost', 10000, callbackNodeEvent)
node2 = Node('localhost', 20000, callbackNodeEvent)
node3 = Node('localhost', 30000, callbackNodeEvent)

node2.start()
node3.start()

node2.connectWithNode('localhost', 30000)

node1.start()
node1.connectWithNode('localhost', 20000)

#server.terminate_flag.set() # Stopping the thread

data = {}
data['event'] = "DISCOVERY"
senddata = json.dumps(data)

node1.send2nodes(senddata)


node4 = Node('localhost', 40000, callbackNodeEvent)
node4.start()
node4.connectWithNode('localhost', 10000)
node4.send2nodes(senddata)


while (True):
    time.sleep(2)

node1.stop()
node2.stop()

node1.join()
node2.join()

#node = DP2PNode(10000)

#node2 = DP2PNode(12000)

print("main stopped")


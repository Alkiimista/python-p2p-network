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
        node.send_to_node(other,dumpdata)


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
                node.connect_with_node(n.ip, n.port)
                print("connect with %s %d" %(n.ip ,n.port))


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


node4 = Node('localhost', 40000, callbackNodeEvent)
node4.start()
node4.connect_with_node('localhost', 10000)
node4.send_to_nodes(senddata)


while (True):
    time.sleep(2)
    #print("------------------------- node1 connected with %d" % (len(node1.nodesIn)+len(node1.nodesOut)))
    #print("------------------------- node2 connected with %d" % (len(node2.nodesIn)+len(node2.nodesOut)))
    #print("------------------------- node3 connected with %d" % (len(node3.nodesIn)+len(node3.nodesOut)))
    #print("------------------------- node4 connected with %d" % (len(node4.nodesIn)+len(node4.nodesOut)))


node1.stop()
node2.stop()

node1.join()
node2.join()

print("main stopped")


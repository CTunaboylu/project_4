from abc import ABC, abstractmethod
from multiprocessing import Process, Manager
from threading import Thread
from typing import Dict
import zmq, random, json, sys

# REST API

# builds the fingertables and make new peers join the network 
 
def root(IP:str): #network additionally implements a REST API for the other peers to join the network and builds their finger tables 
# Considerations: ports must be different for every peer, check that 	
# ID = SHA256(IPAddress) (mod 2m), where m= 128. m bit identifier 
# REST API for updates, checks and goodbyes"
IP = "127.0.0.1:" #9000
class Network():
	__network = dict()
	__id_array = []
	def __init__(self, rootNode, network:Dict):
		__network[rootNode.getID()] = 
	# Nodes see where to go from here 
	#finger table length 
	# ring yapısı  
#for flooding, determine ranges from nodes to other nodes for them to send the message afterwards, they should not send to every fingertable element  	

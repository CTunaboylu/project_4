# Message Channel Agent 
import queue 
import json
import zmq
from typing import List,Dict
class MCAgent:
	# Messages given to MCA are already in json format, updating the MCAgent fingertable can be avoided with giving the destination to it separately, asynchronous calls of MCAgent  
	__m_queue = queue.Queue() # no size limits for now 
	__id = 0
	__context = zmq.Context()
	__channel_destination_socket = (zmq.REQ) # create request socket
	__sender_IP = ""	
	_dest_add = "tcp://"
	__fingertable = []
	def __init__(self,id_ :int, Ip_1:str):
		__sender_IP = Ip_1
		__id = id_
		print(f"Message Channel Agent - {__id}, bridges between {Ip_1} and other nodes are set \n")
	def __propagate(self,message):
		# propagate to the other IP 
		print(f"Propagating the message \"{message['payload']} \" to destination {message[destination_ID]}from sender {Ip_1}")
		destination_IP = __fingertable[message[destination_ID]]
		if __channel_destination_socket.connect(_dest_add+destination_IP) == 0:
			print(f"Connection to {destination_IP} is successful. Sending the message...")
			__channel_destination_socket.send_json(message) 
			reply = __channel_destination_socket.recv() # block until response
			print(reply)
			
		else :
			print(f"Could not connect to {destination_IP})")
	def __channel_message(self,message:json):
		if message['destination_ID'] in fingertable : # if we have the destination id in our fingertable assuming that the update_MCA_fingertable is called beforehand 
			#bind the socket to address OR change the binding according to the ID 
			__propagate(message) 
			

	def update_MCA_fingertable(self, new_table: Dict ): # new_table type unknown dict or list? for good practice call before channeling a maessage 
		if hash(__fingertable) != hash(new_table):
			__fingertable = new_table
		return 	
	
""" dict sample d = {1:2, 3:4}
if 4 in d.itervalues():
    print 'Aha!'"""
# JSON Sample
"""
# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y = json.loads(x)

# the result is a Python dictionary:
# convert into JSON:
y = json.dumps(x)

print(y["age"])"""

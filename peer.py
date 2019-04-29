from multiprocessing import Process, Manager
from threading import Thread
import zmq, json, sys
from MCA import MCAgent 
from typing import Dict, List
# subprocess link : https://docs.python.org/3/library/subprocess.html
#client-server : https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/client_server.html
#chord : https://python-graph-gallery.com/chord-diagram/
#listening the same port https://github.com/mcollina/node-coap/issues/39
#variables 
class Peer(Thread):
	__id = 0
	__ip = ''
	__recieved_messages = []
	# inherifts the Thread for simplicity
	def __init__(self, _IP:str, id_array_from_Network:List):
		Thread.__init__(self)
		# given the IP, ID will be formed -> SHA256 -> int
		__ip = _IP
		# __id = calculate_ID(id_array_from_Network) 
	def getID(self):
		return __id
	def getIP(self):
		return __ip
	def run(self):
		pass
	def start(self):
		pass	
	def listen(self):
		
	
	def calculate_ID(existing_IDs:List):
	# do calculation of the ID with IP 
		"""if current_calculated_ip in existing_IDs: # handle the collisions -> if exists linear_probing : add port_number to the calculated ip to form a new ID ?? 
		return the_id 
		"""
		pass   
def decision():
	#python peer.py IPAddress first=TRUE	
	if _DEBUG:
		print(len(sys.argv))
		print(sys.argv[1]) #IPAddress
	# get the arg coming from the terminal first=TRUE 
	boolean_ = sys.argv[2]
	boolean_ = boolean_[boolean_.find("=")+1::]
	if _DEBUG:
		print(boolean_)
	if "TRUE" in boolean_ : #first config
		first_root_routine(str(sys.argv[1]))
	elif "FALSE" in boolean_:#other sub-peers
		secondary_peers_routine(str(sys.argv[1]))
	else:
		print("Second parameter is invalid")

#network additionally implements a REST API for the other peers to join the network and builds their finger tables 
# Considerations: ports must be different for every peer, check that 	
# REST API for updates, checks and goodbyes"

port = 5153
host = '127.0.0.1:'
_DEBUG = True

decision()

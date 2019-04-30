from multiprocessing import Process, Manager
from threading import Thread
import zmq, json, sys,random, 
from hashlib import SHA256
from MCA import MCAgent
from typing import Dict, List, Tuple
# subprocess link : https://docs.python.org/3/library/subprocess.html
# client-server : https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/client_server.html
# chord : https://python-graph-gallery.com/chord-diagram/
# listening the same port https://github.com/mcollina/node-coap/issues/39
# variables

# With the help of : https://github.com/pedrotgn/python-p2p/blob/master/chord/chord.py
k = 6
MAX = 2 ** k


def decr(value, size):
    if size <= value:
        return value - size
    else:
        return MAX - (size - value)


def between(value, init, end):
    if init == end:
        return True
    elif init > end:
        shift = MAX - init
        init = 0
        end = (end + shift) % MAX
        value = (value + shift) % MAX
    return init < value < end


def Ebetween(value, init, end):
    if value == init:
        return True
    else:
        return between(value, init, end)


def betweenE(value, init, end):
    if value == end:
        return True
    else:
        return between(value, init, end)
# end help 

def decision():
    # python peer.py IPAddress first=TRUE
    if _DEBUG:
        print(len(sys.argv))
        print(sys.argv[1])  # IPAddress
    # get the arg coming from the terminal first=TRUE
    boolean_ = sys.argv[2]
    boolean_ = boolean_[boolean_.find("=") + 1::]
    if _DEBUG:
        print(boolean_)
    if "TRUE" in boolean_:  # first config
        first_root_routine(str(sys.argv[1]))
    elif "FALSE" in boolean_:
        # other sub-peers
        secondary_peers_routine(str(sys.argv[1]))
    else:
        print("Second parameter is invalid")


id_array_from_Network= [None] * 50  # gelcek olan idler
id_array_from_Network[0]=101119102484248423
id_array_from_Network[10]=101119102484248429
id_array_from_Network[11]=1031014861119101114


#id_array_from_Network[1]=57501011191141191
#print(id_array_from_Network[10])

def insert_in2_array(val:int, arr:List):
	length = len(arr)
	for index, element in enumerate(arr):
		if element>val:
			arr[index:(length-index)]=val # insertion by slicing 
			break
	arr.extend(val)
def calculate_ID(hash_value, id_array_from_Network:List)->int:
	# if current_calculated_ip in existing_IDs: # handle the collisions -> if exists linear_probing : add port_number to the calculated ip to form a new ID ??
	# return the_id

	# modlar oylesine suanda test amaclı son halde modlar kalıcak o telefonda konustugumuz sıkıntı yuzunden mod alıyorum.
	hash_value = hash_value[-1:] # 1 byte = 8 bits -> mod 128: 2^7 extracting 8 least significant bits equates to taking the mod 256
	
	
	#for ch in hash_value:
	#   hash_to_int = hash_to_int + str(ord(ch))
	id_int_form = int.from_bytes(hash_value, byteorder='big')	
	probe = 1
	while id_int_form in id_array_from_Network:
		id_int_form = (id_int_form + probe) % 128
		probe = pow(probe+1,2,128) # quadratic probing : according to Gonnet and Baeza-Yates -> quadratic probing is fastest among the collision handling strategies
		
	insert_in2_array(id_int_form, id_array_from_Network)
	if _DEGUB:
		print(id_array_from_Network)
		print("Calculated id is:" + str(id_int_form)
	
	return id_int_form
def find_successor(val:int, arr:Dict)->List: # arr(dict) must be sorted for ring structure according to IDs : [ID, IP]
	for index, elm in enumerate(arr):
		if elm > val: # successor found 
			return [index, elm, ]	

class Peer(Thread):
    def __init__(self, ip, id_array_from_Network):
        Thread.__init__(self)
        self.ip = ip
        #alt satırdaki id aslında gelenin hashı ola
	sha_module = hashlib.SHA256()
	sha_module.update(ip.encode())
	ident = sha_module.digeest()
	self.id = calculate_ID(ident, id_array_from_Network)
	self.finger = {}
	self.start = {}
	for i in range(k):
		c = pow(2,i,MAX)
		val_to_find_successor = (self.id + c)
		successor = find_successor(val_to_find_successor, id_array_from_Network)
		self.finger[i] = [successor[0], successor[1].] = 
	def successor(self):
		return self.finger[0]

	def find_successor(self, ident):
		if betweenE(ident, self.predecessor.id, self.id):
			return self
		n = self.find_predecessor(ident)
		return n.successor()

	def find_predecessor(self, ident):
		if ident == self.id:
			return self.predecessor
		n1 = self
		while not betweenE(ident, n1.id, n1.successor().id):
			n1 = n1.closest_preceding_finger(ident)
		return n1

	def closest_preceding_finger(self, ident):
		for i in range(k - 1, -1, -1):
			if between(self.finger[i].id, self.id, ident):
				return self.finger[i]
		return self

	def join(self, n1):
		if self == n1:
			for i in range(k):
				self.finger[i] = self
				self.predecessor = self
		else:
			self.init_finger_table(n1)
			self.update_others()
	    # Move keys !!!

	def init_finger_table(self, n1):
		self.finger[0] = n1.find_successor(self.start[0])
		self.predecessor = self.successor().predecessor
		self.successor().predecessor = self
		self.predecessor.finger[0] = self
		for i in range(k - 1):
	    		if Ebetween(self.start[i + 1], self.id, self.finger[i].id):
				self.finger[i + 1] = self.finger[i]
			else:
				self.finger[i + 1] = n1.find_successor(self.start[i + 1])

	def update_others(self):
		for i in range(k):
			prev = decr(self.id, 2 ** i)
			p = self.find_predecessor(prev)
			if prev == p.successor().id:
				p = p.successor()
			p.update_finger_table(self, i)

	def update_finger_table(self, s, i):
		if Ebetween(s.id, self.id, self.finger[i].id) and self.id != s.id:
			self.finger[i] = s
			p = self.predecessor
			p.update_finger_table(s, i)

	def update_others_leave(self):
		for i in range(k):
			prev = decr(self.id, 2 ** i)
			p = self.find_predecessor(prev)
			p.update_finger_table(self.successor(), i)

	# not checked
	def leave(self):
	self.successor().predecessor = self.predecessor
	self.predecessor.setSuccessor(self.successor())
	self.update_others_leave()

	def setSuccessor(self, succ):
	self.finger[0] = succ

	def run(self):
	pass

	def start(self):
	pass

	def listen(self):
	pass


# def hash(line):
# import sha
# key = (sha.new(line).hexdigest(), 16)
# return key



def printNodes(node):
    print(
        ' Ring nodes:')
    end = node
    print(
        node.id)
    while end != node.successor():
        node = node.successor()
        print(
            node.id)
    print(
        '-----------')


def showFinger(node):
    print('Finger table of node ' + str(node.id))
    print('start:node')
    for i in range(k):
        print(str(node.finger[i].id) + ' : ' + str(node.ip))
    print('-----------')




port = 5153
host = '127.0.0.1:'
_DEBUG = True

#decision()

'''

n1 = Node(ip,351)
n2 = Node(ip1,390)
n3 = Node(ip2,396)
n4 = Node('32423423424',630)
n5 = Node('32423424',647)
n6 = Node('34234234234',350)
n7 = Node('543535432342',479)
n8 = Node('123123123',413)
n9 = Node('3123123123123',710)
n10 = Node('432432432742',393)
'''

ip = '123.322.234.43'
ip1 = '12.322.234.43'
ip2 = '13.32.23224.43'

# ikinci kısım ip nin hasni koyacagımız kısım

n1 = Peer(ip, '103243232fewf0*0*')
n2 = Peer(ip1, '1298989893erw')
n3 = Peer(ip2, '129898989')
n4 = Peer('32423423424','129898989bhhbj?erwr')
n5 = Peer('32423424','129898989rewge0=wer')
n6 = Peer('34234234234', '12989898769032*492ewrwr')
n7 = Peer('543535432342','1298987t98909er=)werw')
n8 = Peer('123123123', '129898989?=?')
n9 = Peer('3123123123123','129898989//2342lkwmnf?')
n10 = Peer('432432432742', '1279898989==?=??32*0*')



